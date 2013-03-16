#!/usr/bin/env python
import collections
import json
import posixpath
import urlparse


def is_internal(link):
    return urlparse.urlparse(link).netloc == "pypi.python.org"


with open("links.json") as links_file:
    links = json.load(links_file)


internal = list(link for link in links if is_internal(link[2]))
external = list(link for link in links if not is_internal(link[2]))

internal_pairs = set((project, posixpath.basename(urlparse.urlparse(link).path)) for project, source, link in links if is_internal(link))
external_only = [link for link in links if not (link[0], posixpath.basename(urlparse.urlparse(link[2]).path)) in internal_pairs]

internal_filenames = set((link[0], posixpath.basename(urlparse.urlparse(link[2]).path)) for link in internal)
external_filenames = set((link[0], posixpath.basename(urlparse.urlparse(link[2]).path)) for link in external)

internal_projects = set(project for project, _, _ in internal)
external_only_projects = set(project for project, _, _ in external_only)
only_external_only_projects = set(project for project in external_only_projects if project not in internal_projects)

domains = collections.Counter(urlparse.urlparse(link[2]).netloc for link in links)
top_domains = domains.most_common(21)[1:]


with open("external_only_links.json", "w") as external_links_file:
    _external_links_project = {}
    for project, _, link in external_only:
        _external_links_project.setdefault(project, []).append(link)
    json.dump(_external_links_project, external_links_file, sort_keys=True, indent=4)

with open("only_external_projects.json", "w") as projects_file:
    json.dump(sorted(only_external_only_projects), projects_file, indent=4)

with open("any_external_projects.json", "w") as projects_file:
    json.dump(sorted(external_only_projects), projects_file, indent=4)


print " PyPI Link Checker Stats"
print "=" * 60
print "  internal file links: %d" % len(internal)
print "  external file links: %d" % len(external)
print "  external only file links: %d" % len(external_only)
print ""
print "  internal file names: %d" % len(internal_filenames)
print "  external file names: %d" % len(external_filenames)
print ""
print "  projects with any external only links: %d" % len(external_only_projects)
print "  projects with only external only links: %d" % len(only_external_only_projects)
print ""

_padding = max(len(domain) for domain, _ in top_domains)
print " Top External Link Domains"
print "=" * 60
for domain, count in top_domains:
    print "  %s: %d" % ((" " * (_padding - len(domain))) + domain, count)


# import pdb; pdb.set_trace()
