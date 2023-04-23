import requests

from PrivateConfig import FB_ID, FB_SECRET, INSTAGRAM_BUSINESS_ID

BASE_URL_API = "https://graph.facebook.com/v16.0/"


def getAllPost(token_60days):
    return requests.get(BASE_URL_API +
                        f"{INSTAGRAM_BUSINESS_ID}"
                        "/media?"
                        "fields=id%2Ccaption%2Clike_count%2Cmedia_url%2Ctimestamp%2Ccomments_count%2Ccomments"
                        f"&access_token={token_60days}").json()


def getLongToken(access_token):
    return requests.get(BASE_URL_API +
                        "oauth/"
                        "access_token?"
                        "grant_type=fb_exchange_token&"
                        f"client_id={FB_ID}&"
                        f"client_secret={FB_SECRET}&"
                        f"fb_exchange_token={access_token}").json()
