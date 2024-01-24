#!/usr/bin/env python3
"""sorting by average score"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """returns sorted collection"""
    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1, "name": 1}
        }
    ]

    result = list(mongo_collection.aggregate(pipeline))

    for student in result:
        student["_id"] = str(student["_id"])  # Convert ObjectId to string

    return result
