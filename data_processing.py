from scrape_reddit import *


def format_comments(data):
    """
    args:
        data: list of dicts with 'body'/'selftext' and 'created_utc' keys
    """
    bad_bodies = (
        "[removed]", 
        "[deleted]",
    )
    bad_phrases = (
        "I am a bot, and this action was performed automatically",
        "https://www.",
        "http://www.",
    )

    if any("body" in i for i in data):
        bodies = [i["body"] for i in data if "body" in i]
    elif any("selftext" in i for i in data):
        bodies = [i["selftext"] for i in data if "selftext" in i]
    else:
        raise KeyError("The expected keys werent found...")
    # remove empty, bad stuff
    bodies = [i for i in bodies if len(i) > 25]
    bodies = [i for i in bodies if i not in bad_bodies]
    bodies = [i for i in bodies if not any(j in i for j in bad_phrases)]
    # remove punctuation
    bodies = [re.sub(r"[^\w\s]", "", i) for i in bodies]
    # replaces all whitespace with single spaces
    bodies = [re.sub(r"\s+", " ", i) for i in bodies]
    # lowercaseify
    bodies = [i.lower() for i in bodies]
    return bodies




