#!/usr/bin/env python
"""
Collects all installable looking links from PyPI
"""
import itertools
import json
import traceback
import urlparse
import xmlrpclib

import gevent
import gevent.queue
import lxml.html
import redis
import requests

from pkg_resources import safe_name
from setuptools.package_index import distros_for_url


WORKERS = 100


redis = redis.StrictRedis()

session = requests.session()
session.verify = False


def installable(project, url):
    normalized = safe_name(project).lower()
    return bool([dist for dist in distros_for_url(url) if safe_name(dist.project_name).lower() == normalized])


def process_links(project, url, spider):
    if redis.sismember("seen", json.dumps([project, url, spider])):
        print "Skipping %s; it has already been processed (For %s)" % (url.encode("utf-8"), project.encode("utf-8"))
    else:
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
                parsed = urlparse.urlparse(link.attrib["href"])
                if parsed.scheme.lower() in ["http", "https"]:
                    redis.rpush("queue", json.dumps([project, link.attrib["href"], False]))

    # Process all links in html for installable items
    for link in html.xpath("//a"):
        try:
            link.make_links_absolute(url)
        except ValueError:
            continue

        if "href" in link.attrib and installable(project, link.attrib["href"]):
            redis.rpush("results", json.dumps([project, url, link.attrib["href"]]))

    redis.sadd("seen", json.dumps([project, url, spider]))


def worker():
    while True:
        item = redis.lpop("queue")

        if item is None:
            break

        try:
            process_links(*json.loads(item))
        except Exception:
            traceback.print_exc()


def main():
    # Grab a list of projects from PyPI
    projects = xmlrpclib.Server("http://pypi.python.org/pypi").list_packages()

    # Add some urls to our queue
    for project in projects:
        redis.rpush("queue", json.dumps([project, "https://pypi.python.org/simple/" + project + "/", True]))

    workers = [gevent.spawn(worker) for _ in xrange(WORKERS)]
    gevent.joinall(workers)


if __name__ == "__main__":
    main()
