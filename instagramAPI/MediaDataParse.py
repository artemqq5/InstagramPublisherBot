import io
from collections import namedtuple

import requests


def parseAllPosts(jsonListMedia):
    listPosts = []

    for item in jsonListMedia['data']:
        photo = io.BytesIO(requests.get(item['media_url']).content)

        caption = item['caption']
        id_post = item['id']
        likes = item['like_count']
        comments = item['comments_count']
        time = item['timestamp']

        description = f"id post: {id_post}\n\n{caption}\n\nlikes: {likes}\ncomments: {comments}\n\n{time}"

        post = namedtuple('Post', ['img', 'desc'])(photo, description)
        listPosts.append(post)

    return listPosts
