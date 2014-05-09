#!/usr/bin/env python2
import fileinput
import json
import re
import urlparse


_hash_re = re.compile(r'(sha1|sha224|sha384|sha256|sha512|md5)=([a-f0-9]+)')


def has_hash(link):
    match = _hash_re.search(link)
    return bool(match)


def is_internal(link):
    return urlparse.urlparse(link).netloc == "pypi.python.org"


links = json.loads("".join(line for line in fileinput.input()))


all_projects = set()
all_internal_projects = set()
all_external_projects = set()
all_unverifiable_projects = set()
only_internal_projects = set()
only_external_projects = set()
only_unverifiable_projects = set()


for project, source_url, file_url in links:
    # Add this project to the list of all projects
    all_projects.add(project)

    if is_internal(file_url):
        # Add this project to the list of projects that have any internal files
        all_internal_projects.add(project)

        # Check to see if this project exists in only_external_projects or
        # only_unverifiable_projects, and if it does, remove it.
        if project in only_external_projects:
            only_external_projects.remove(project)
        if project in only_unverifiable_projects:
            only_unverifiable_projects.remove(project)

        # Check to see if this project exists in external or unverifiable
        # if not, then add it to only_internal_projects
        if project not in all_external_projects | all_unverifiable_projects:
            only_internal_projects.add(project)
    elif is_internal(source_url) and has_hash(file_url):
        # Add this project to the list of projects that have any external files
        all_external_projects.add(project)

        # Check to see if this project exists in only_internal_projects or
        # only_unverifiable_projects, and if it does, remove it.
        if project in only_internal_projects:
            only_internal_projects.remove(project)
        if project in only_unverifiable_projects:
            only_unverifiable_projects.remove(project)

        # Check to see if this project exists in internal or unverifiable
        # if not, then add it to only_internal_projects
        if project not in all_internal_projects | all_unverifiable_projects:
            only_external_projects.add(project)
    else:
        # Add this project to the list of projects that have any unverifiable
        # files
        all_unverifiable_projects.add(project)

        # Check to see if this project exists in only_internal_projects or
        # only_external_projects, and if it does, remove it.
        if project in only_internal_projects:
            only_internal_projects.remove(project)
        if project in only_external_projects:
            only_external_projects.remove(project)

        # Check to see if this project exists in internal or unverifiable
        # if not, then add it to only_internal_projects
        if project not in all_internal_projects | only_external_projects:
            only_unverifiable_projects.add(project)


print "* Projects with Any Files: %d" % len(all_projects)
print "* Projects with Any Files Hosted on PyPI: %d" % len(all_internal_projects)
print "* Projects with Any Files Hosted Safely off PyPI: %d" % len(all_external_projects)
print "* Projects with Any Files Hosted Unsafely off PyPI: %d" % len(all_unverifiable_projects)
print "* Projects with Only Files Hosted on PyPI: %d" % len(only_internal_projects)
print "* Projects with Only Files Hosted Safely off PyPI: %d" % len(only_external_projects)
print "* Projects with Only Files Hosted Unsafely off PyPI: %d" % len(only_unverifiable_projects)
