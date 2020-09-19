from scrape_reddit import *


def format_comments(comments_dict):
    """
    args:
        comments_dict: dict with 'body' and 'created_utc' keys
    """
    bad_bodies = (
        "[removed]", 
        "[deleted]"
    )
    bad_phrases = (
        "I am a bot, and this action was performed automatically",
        "https://www.",
        "http://www.",
    )

    bodies = [i["body"] for i in comments_dict]
    # remove bad stuff
    bodies = [i for i in bodies if i not in bad_bodies]
    bodies = [i for i in bodies if not any(j in i for j in bad_phrases)]
    # remove punctuation
    bodies = [re.sub(r"[^\w\s]", "", i) for i in bodies]
    # replaces all whitespace with single spaces
    bodies = [re.sub(r"\s+", " ", i) for i in bodies]
    # lowercaseify
    bodies = [i.lower() for i in bodies]
    return bodies




