import json

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


def getAccountInfo(token_60days):
    return requests.get(
        BASE_URL_API +
        INSTAGRAM_BUSINESS_ID +
        "?fields=biography,"
        "followers_count,"
        "follows_count,"
        "media_count,"
        "name,"
        "profile_picture_url,"
        "username,"
        "website"
        f"&access_token={token_60days}"
    )


def createContainerMEDIA(token_60days, data):
    data['access_token'] = token_60days

    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        BASE_URL_API + INSTAGRAM_BUSINESS_ID + "/media",
        data=json_data,
        headers=headers
    )

    print(f"response createContainerMEDIA {response.json()}")

    return response.json()


def publishMEDIA(token_60days, id_container):
    response = requests.post(BASE_URL_API +
                             INSTAGRAM_BUSINESS_ID +
                             "/media_publish"
                             f"?creation_id={id_container}"
                             f"&access_token={token_60days}")

    print(f"response publishMEDIA {response.json()}")

    return response.json()


def getStatistic(token_60days, data, total_value=False):

    if total_value:
        sub = "&metric_type=total_value"
    else:
        sub = ""

    return requests.get(BASE_URL_API +
                        INSTAGRAM_BUSINESS_ID +
                        "/insights"
                        f"?metric={data}"
                        "&period=day" +
                        sub +
                        f"&access_token={token_60days}"
                        ).json()
