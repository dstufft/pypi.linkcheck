#!/usr/bin/env python
"""
Collects all installable looking links from PyPI
"""
import itertools
import json
import traceback
import xmlrpclib

import gevent
import gevent.queue
import lxml.html
import requests

from pkg_resources import safe_name
from setuptools.package_index import distros_for_url


WORKERS = 100


def memoize(f):
    cache = {}

    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf


def installable(project, url):
    normalized = safe_name(project).lower()
    return bool([dist for dist in distros_for_url(url) if safe_name(dist.project_name).lower() == normalized])


@memoize
def process_links(item, queue, results):
    project, url, spider, session = item

    print "Processing %s for urls (For %s)" % (url.encode("utf-8"), project.encode("utf-8"))

    resp = session.get(url)
    resp.raise_for_status()

    html = lxml.html.document_fromstring(resp.content)

    if spider:
        for link in itertools.chain(html.find_rel_links("download"), html.find_rel_links("homepage")):
            try:
                link.make_links_absolute(url)
            except ValueError:
                continue

            if "href" in link.attrib and not installable(project, link.attrib["href"]):
                queue.put((project, link.attrib["href"], False, session))

    # Process all links in html for installable items
    for link in html.xpath("//a"):
        try:
            link.make_links_absolute(url)
        except ValueError:
            continue

        if "href" in link.attrib and installable(project, link.attrib["href"]):
            results.put((project, url, link.attrib["href"]))


def worker(queue, results):
    while True:
        item = queue.get()
        try:
            process_links(item, queue, results)
        except Exception:
            traceback.print_exc()
        finally:
            queue.task_done()


def main():
    # Queues for storing tasks and results
    queue = gevent.queue.JoinableQueue()
    results = gevent.queue.Queue()

    # Final urls container
    urls = set()

    # Spawn our workers
    for _ in xrange(WORKERS):
        gevent.spawn(worker, queue, results)

    # Grab a list of projects from PyPI
    projects = xmlrpclib.Server("http://pypi.python.org/pypi").list_packages()

    # Session for processing links
    session = requests.session()
    session.verify = False

    # Add some urls to our queue
    for project in projects:
        queue.put((project, "https://pypi.python.org/simple/" + project + "/", True, session))

    # Wait for our queue to empty
    queue.join()

    # Process our results
    try:
        while True:
            urls.add(results.get(block=False))
    except gevent.queue.Empty:
        pass

    print "Found a total of %s file links" % (len(urls),)

    with open("links.json", "w") as links:
        _urls = sorted([list(url) for url in urls])
        json.dump(_urls, links, indent=2)


if __name__ == "__main__":
    main()
