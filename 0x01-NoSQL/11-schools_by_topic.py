#!/usr/bin/env python3
"""Python function that returns the list
of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of schools having a specific topic"""
    query = {"topics": {"$in": [topic]}}
    schools = mongo_collection.find(query)
    return schools
