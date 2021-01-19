"""
Broken Links Visualiser.

Amjad Karim

4th November 2017.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd
from io import StringIO
import csv
from sys import argv

# Get base links
if len(argv) > 1:
    site = argv[1]
else:
    site = 'https://example.com'

base = urlparse(site).netloc
to_visit = [site]
outlinks = []
visited = {}
external_visited = {}

# set up csv
output = StringIO()
writer = csv.writer(output)
writer.writerow(['source', 'target'])

while to_visit:
    l = to_visit.pop()
    print(l)
    url = urljoin(site, l)

    # try:
    r = requests.get(url)
    visited[l] = r.status_code

    if r.status_code == 200:
        print(f'visiting: {url}')
        soup = BeautifulSoup(r.content, 'html5lib')
        links = [l['href'] for l in soup.find_all('a', href=True)]
        for link in links:
            parsed_link = urlparse(link)
            loc = parsed_link.netloc
            path = parsed_link.path
            joined_url = urljoin(site, link)

            if loc == '':
                if joined_url not in to_visit and joined_url not in visited.keys() and joined_url[0:4] == 'http':
                    print(f'adding to internal links: {joined_url}')
                    to_visit.append(joined_url)
                    writer.writerow([url, joined_url])

            elif loc == base:
                if link not in to_visit and link not in visited.keys():
                    print(f'adding to internal links: {link}')
                    to_visit.append(link)
                    writer.writerow([url, link])

            else:
                if link not in outlinks and link not in visited.keys():
                    print(f'adding to external links: {link}')
                    outlinks.append(link)
                    writer.writerow([url, link])

# check the status of external links
while outlinks:
    l = outlinks.pop()

    try:
        r = requests.get(l)
        external_visited[l] = r.status_code

    except:
        external_visited[l] = None

# Create a DataFrame
s = pd.Series(visited, name='Response')
s.index.name = 'URL'
df1 = pd.DataFrame(s)
df1['Type'] = 'Internal'

s = pd.Series(external_visited, name='Response')
s.index.name = 'URL'
df2 = pd.DataFrame(s)
df2['Type'] = 'External'

results = pd.concat([df1, df2])

output.seek(0)
link_pairs = pd.read_csv(output)
final_df = link_pairs.merge(results, left_on='target', right_on='URL')
final_df.to_csv('link_analysis.csv')
