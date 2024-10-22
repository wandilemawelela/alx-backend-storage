#!/usr/bin/env python3

"""
This module lists all documents in a collection.
"""


def list_all(mongo_collection):
    """
    This will list all documents in a collection.
    """
    return [doc for doc in mongo_collection.find()]
