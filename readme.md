## Introduction
Simple python scripts to identify broken links on a site and export the results to csv.
Not tested on js rich sites but will work on wordpress blogs etc., in fact this is what it was created for. To see what links were broken or had rotted on a site.

~~Also visualisation with ```networkx```.~~

## Installation
1. Clone repository

2. Create conda environment from yml file or install the following:
 * pandas
 * BeautifulSoup
 * requests
 * networkx

## Usage
```
python simple_broken_links.py https://d-science.com
```
Will generate link_analysis.csv containing details on links from the target site.
