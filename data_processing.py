from scrape_reddit import *


def format_comments(comments_dict):
    """
    args:
        comments_dict: dict with 'body' and 'created_utc' keys
    """
    bad_bodies = ("[removed]", "[deleted]")

    bodies = [i["body"] for i in comments_dict]
    bodies = [i for i in bodies if i not in bad_bodies]
    # remove punctuation
    bodies = [re.sub(r"[^\w\s]", "", i) for i in bodies]
    # replaces all whitespace with single spaces
    bodies = [re.sub(r"\s+", " ", i) for i in bodies]
    # lowercaseify
    bodies = [i.lower() for i in bodies]
    return bodies




