import requests

from PrivateConfig import FB_ID, FB_SECRET, TOKEN_FB_60DAYS, INSTAGRAM_BUSINESS_ID


def getUserInfo():
    return requests.get(f"https://google.com/").json()


def getAllPost():
    return requests.get("https://graph.facebook.com/v16.0/"
                        f"{INSTAGRAM_BUSINESS_ID}"
                        "/media?"
                        "fields=id%2Ccaption%2Cmedia_type%2Cmedia_url%2Cthumbnail_url%2Cpermalink%2Ctimestamp"
                        f"&access_token={TOKEN_FB_60DAYS}").json()


def getLongToken(access_token):
    return requests.get("https://graph.facebook.com/"
                        "v16.0/oauth/"
                        "access_token?"
                        "grant_type=fb_exchange_token&"
                        f"client_id={FB_ID}&"
                        f"client_secret={FB_SECRET}&"
                        f"fb_exchange_token={access_token}").json()
