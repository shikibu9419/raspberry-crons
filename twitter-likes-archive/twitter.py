from twikit import Client
import os
import json
from time import time

next_cursor = None

with open('NEXT_CURSOR', 'r') as f:
    next_cursor = f.read()


def get_likes():
    global next_cursor
    client = Client('ja-JP')

    try:
        client.load_cookies("cookies.json")
    except:
        client.login(
            auth_info_1=os.environ['TWITTER_USERNAME'],
            auth_info_2=os.environ['TWITTER_EMAIL'],
            password=os.environ['TWITTER_PASSWORD']
        )

    client.save_cookies('cookies.json')

    tweets = client.get_user_tweets(os.environ['TWITTER_USER_ID'], 'Likes', count=500, cursor=next_cursor)
    next_cursor = tweets.next_cursor
    print(tweets.next_cursor, next_cursor)

    with open('NEXT_CURSOR', 'w') as f:
        f.write(next_cursor)

    return tweets


def archive_likes():
    tweets = get_likes()

    if len(tweets) == 0:
        return

    data = []

    for tweet in tweets:
#         print('--------------------')
#         print('ID:', tweet.id)
#         print('URL:', f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}")
#         print('text:', tweet.text)
#         print('Thumbnail', tweet.thumbnail_url)
#         print('Related URLs', tweet.urls)
#         if tweet.media:
#             print('Photos', [m['media_url_https'] for m in tweet.media if m['type'] == 'photo'])
#             print('Videos', [m['video_info']['variants'][-1]['url'].split('?')[0] for m in tweet.media if m['type'] == 'video'])

        media = []
        for m in tweet.media or []:
            m_json = { 'type': m['type'], 'image_url': m['media_url_https'] }
            if m['type'] == 'video':
                m_json['video_url'] = m['video_info']['variants'][-1]['url'].split('?')[0]
            media.append(m_json)

        data.append({
            'id': tweet.id,
            'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
            'text': tweet.text,
            'thumbnail': tweet.thumbnail_url,
            'urls': tweet.urls,
            'media': media
        })

    with open(f'output/{int(time())}.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    archive_likes()
