#!/usr/bin/env python3
"""list all collections"""


def list_all(mongo_collection):
    """ lists all documents in a collection"""
    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents
