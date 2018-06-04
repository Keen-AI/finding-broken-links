"""
Broken Links Visualiser.

Amjad Karim

4th November 2017.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import networkx as nx
import pandas as pd

# Get base links
site = ''
base = urlparse(site).netloc

to_visit = [site]
outlinks = []
visited = []
responses = []
nodes = {site: 1}

# Initialise Graph
G = nx.DiGraph()
G.add_node(1, page=site)

while to_visit:
    l = to_visit.pop()
    print(l)

    # Updated the nodes dictionary
    current_node = nodes[l]
    url = urljoin(site, l)
    r = requests.get(url)
    visited.append(l)
    responses.append(r.status_code)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html5lib')
        links = [l['href'] for l in soup.find_all('a', href=True)]
        for link in links:
            parsed_link = urlparse(link)
            loc = parsed_link.netloc
            path = parsed_link.path

            if loc == '':

                joined_url = urljoin(site, link)

                if joined_url in visited:
                    G.add_edge(current_node, nodes[joined_url])

                else:

                    if joined_url not in to_visit:
                        to_visit.append(joined_url)
                        m = G.number_of_nodes() + 1
                        G.add_node(m, page=link)
                        G.add_edge(current_node, m)
                        nodes[joined_url] = m

                    else:
                        m = nodes[joined_url]
                        G.add_edge(current_node, m)

            elif loc == base:

                if link in visited:
                    G.add_edge(current_node, nodes[link])

                else:

                    if link not in to_visit:
                        to_visit.append(link)
                        m = G.number_of_nodes() + 1
                        G.add_node(m, page=link)
                        G.add_edge(current_node, m)
                        nodes[link] = m

                    else:
                        m = nodes[link]
                        G.add_edge(current_node, m)

            else:

                if link not in outlinks:
                    m = G.number_of_nodes() + 1
                    G.add_node(m, page=link)
                    G.add_edge(current_node, m)
                    outlinks.append(link)
                    nodes[link] = m

                else:
                    m = nodes[link]
                    G.add_edge(current_node, m)

outcome = dict(zip(visited, responses))
nx.write_gexf(G, 'ng.gexf' % site)
