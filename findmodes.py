#!/usr/bin/env python
import json
import urlparse


with open("links.json") as lfile:
    links = json.load(lfile)


total = set()
explicit = set()
scrape = set()
crawl = set()


for project, from_url, download_url in links:
    # Make sure we account for every project
    total.add(project)

    # If this download target came from a crawled url then add it to the list
    #   of projects that require crawling
    if urlparse.urlparse(from_url).netloc != "pypi.python.org":
        crawl.add(project)
    # If this download target came _from_ pypi, but it is not itself hosted on
    #   PyPI then add it to the list of projects that require scraping
    elif urlparse.urlparse(download_url).netloc != "pypi.python.org":
        scrape.add(project)


# Remove anything from scraping that requires crawling
scrape = scrape - crawl


# Anything that doesn't require crawling or scraping is an explicit
explicit = total - (crawl | scrape)


print("%s total projects" % len(total))
print("%s explicit projects" % len(explicit))
print("%s scrape projects" % len(scrape))
print("%s crawl projects" % len(crawl))


with open("migration.json", "w") as mfile:
    json.dump({
            "pypi-scrape-crawl": sorted(crawl),
            "pypi-scrape": sorted(scrape),
            "pypi-explicit": sorted(explicit),
        },
        mfile, indent=4, sort_keys=True)
