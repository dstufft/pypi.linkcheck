#!/usr/bin/env python
"""
Writes all of the collected links from linkcollector.py into json files.
"""
import json
import redis

redis = redis.StrictRedis()

urlset = set([tuple(json.loads(x)) for x in redis.lrange("results", 0, redis.llen("results") - 1)])
urls = sorted(urlset)

with open("links.json", "w") as links:
    json.dump([list(x) for x in urls], links, indent=4)
