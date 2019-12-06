from graph import Node
from dotenv import load_dotenv
import twitter
import arrow
import os

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN_KEY = os.getenv("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

API = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET)


def check_rate_limit():
    url_followers = "https://api.twitter.com/1.1/followers/list.json"
    url_friends = "https://api.twitter.com/1.1/friends/list.json"

    rr_followers = API.CheckRateLimit(url_followers)
    rr_friends = API.CheckRateLimit(url_friends)
    print(rr_followers, rr_friends)
    if (rr_followers.remaining == 0):
        print(
            f"LIMIT on Followers: Try {arrow.get(rr_followers.reset).humanize()}"
        )
        raise Exception("Rate Limit Exceeded")
    if (rr_friends.remaining == 0):
        print(
            f"LIMIT on Friends: Try {arrow.get(rr_friends.reset).humanize()}")
        raise Exception("Rate Limit Exceeded")


def get_next_mutuals(node: Node):
    followers = API.GetFollowers(node.id)
    friends = API.GetFriends(node.id)
    mutuals = list(set(followers) & set(friends))
    ans = [Node(mutual.id, mutual.name) for mutual in mutuals]
    return ans


def get_current_id_name():
    user = API.VerifyCredentials()
    user_id = user.id
    user_name = user.screen_name
    return user_id, user_name
