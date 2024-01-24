#!/usr/bin/env python3
"""Python script that provides some stats
about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def print_stats():
    """prints stats"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})
    print('{} logs'.format(total_logs))

    # Count of each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, method_count))

    # Count of logs with method=GET and path=/status
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print('{} status check'.format(status_check_count))


if __name__ == "__main__":
    """main"""
    print_stats()
