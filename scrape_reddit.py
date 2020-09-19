import datetime
import json
import re
from urllib.request import urlopen

import matplotlib
import matplotlib.pyplot as plt




def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Args:
        url: str
    
    Thank you Martin Thoma from stack overflow for this function
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def pushshift_comment(q = None, ids = None, size = None, fields = None, sort = None, 
    sort_type = None, aggs = None, author = None, subreddit = None, after = None, before = None, 
    frequency = None, metadata = None):
    """
    Returns a dictionary of the data returned from the pushift request 
    
    Input:
        q - Search term. (String)
        ids - Get specific comments via their ids (list of base36 ids)
        size - Number of search terms to return (0 < int < 501)
        fields - Which fields to return (list of strings)
        sort - Sort results in a specific order ("asc", "desc")
        sort_type - Sort by a specific attribute ("score", "num_comments", "created_utc")
        aggs - Return aggregation summary ("author", "link_id", "created_utc", "subreddit")
        author - Limit to specific author (string)
        subreddit - Limit to specific subreddit (string)
        after - Search after this time (int of epoch value or Integer + "s,m,h,d" (i.e. 30d for 30 days))
        before - Search before this time (int of epoch value or Integer + "s,m,h,d" (i.e. 30d for 30 days))
        frequency - Used with the aggs parameter when set to created_utc ("second", "minute", "hour", "day")
        metadata - display metadata about the query (bool)

    Output:
        dict - a dictionary of comments/info
    
    Thank you to Jason Baumgartner who hosts and maintains pushshift
    https://github.com/pushshift/api
    """
    # Make one giant dictonary for east formatting
    args = {"q":q,"ids":ids,"size":size,"fields":fields,"sort":sort,
        "sort_type":sort_type,"aggs":aggs,"author":author,"subreddit":subreddit,
        "after":after,"before":before,"frequency":frequency,"metadata":metadata}
    
    # Get rid of unused fields
    args = {key:value for key,value in args.items() if value is not None}

    # Prep list for url reqest
    for key, value in args.items():
        # deal with search terms
        if key == "q":
            value = "\"" + value + "\""

        # make sure ints are ints
        if key in ["size"]:
            value = int(value)

        # Format lists as csv
        if isinstance(value, list):
            temp = ""
            for el in value:
                temp = temp + el + ","
            args[key] = temp[:-1] # [:-1] to get rid of last comma
        
        # Make everything into strings
        if not isinstance(value, str):
            args[key] = str(value)

    # Create url for request   
    url = "https://api.pushshift.io/reddit/search/comment/?"
    for key, value in args.items():
        # deal with spaces
        value = value.replace(" ", "%20")

        url += key + "=" + value + "&"
        
    url = url[:-1] # Get rid of last &


    # Use url to get dictionary of info
    return get_jsonparsed_data(url)


def get_comments(term=None, before=None, after=None, subreddit=None):
    """
    input:
        - term: the string to include comments for
        - before: epoch date to include comments before
        - after: epoch date to include comments after
        - subreddit: str
    output:
        - A list of dictionaries [{'body': str, 'created_utc': int, 'score':int},...]
    """
    sort = "desc"
    sort_type = "created_utc"
    fields = "created_utc,body"
    size = 100

    data = pushshift_comment(q = term, before = before, after = after,\
        subreddit = subreddit, sort = sort, sort_type = sort_type, 
        fields = fields, size = size)

    return data["data"]
