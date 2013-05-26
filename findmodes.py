#!/usr/bin/env python
import json
import urlparse


with open("links.json") as lfile:
    links = json.load(lfile)


total = set()
explicit = set()
crawl = set()


for project, from_url, download_url in links:
    # Make sure we account for every project
    total.add(project)

    # If this download target came from a crawled url then add it to the list
    #   of projects that require crawling
    if urlparse.urlparse(from_url).netloc != "pypi.python.org":
        crawl.add(project)


# Anything that doesn't require crawling is an explicit
explicit = total - crawl


print("%s total projects" % len(total))
print("%s explicit projects" % len(explicit))
print("%s crawl projects" % len(crawl))


with open("migration.json", "w") as mfile:
    json.dump({
            "pypi-scrape-crawl": sorted(crawl),
            "pypi-explicit": sorted(explicit),
        },
        mfile, indent=4, sort_keys=True)
