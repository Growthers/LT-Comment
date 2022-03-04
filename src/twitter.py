import json
import os
import time

import requests
from dotenv import load_dotenv

from process import process

load_dotenv()
TwitterBearerToken = os.environ["TWITTER_BEARER_TOKEN"]
StreamAPIURL = "https://api.twitter.com/2/tweets/search/stream"

Expansions = [
    "attachments.poll_ids",
    "attachments.media_keys",
    "author_id",
    "entities.mentions.username",
    "geo.place_id",
    "in_reply_to_user_id",
    "referenced_tweets.id",
    "referenced_tweets.id.author_id",
]

TweetFields = [
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    "non_public_metrics",
    "public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "possibly_sensitive",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text",
    "withheld",
]

UserFields = [
    "created_at",
    "description",
    "entities",
    "id",
    "location",
    "name",
    "pinned_tweet_id",
    "profile_image_url",
    "protected",
    "public_metrics",
    "url",
    "username",
    "verified",
    "withheld",
]

header = {"Authorization": f"Bearer {TwitterBearerToken}"}

streamParams = {
    "expansions": Expansions,
    "tweet_fields": TweetFields,
    "user_fields": UserFields,
}


# パラメーターの展開
def expand_params(params):
    # expansions の展開
    if "expansions" in params:
        params["expansions"] = ",".join(params["expansions"])

    # tweet_fields の展開
    if "tweet_fields" in params:
        params["tweet.fields"] = ""

        for v in params["tweet_fields"]:
            params["tweet.fields"] += f"{v},"

        params["tweet.fields"] = params["tweet.fields"].rstrip(",")
        del params["tweet_fields"]

    # user_fields の展開
    if "user_fields" in params:
        params["user.fields"] = ""

        for v in params["user_fields"]:
            params["user.fields"] += f"{v},"

        params["user.fields"] = params["user.fields"].rstrip(",")
        del params["user_fields"]

    return params


# ストリーム
def stream() -> None:
    params = expand_params(streamParams)
    while True:
        res = requests.get(StreamAPIURL, headers=header, params=params, stream=True)

        if res.status_code == 429:
            time.sleep(10)
            continue
        elif res.status_code != 200:
            continue

        for line in res.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                try:
                    process(data)
                except Exception:
                    pass
