import re
import sys
import traceback

from tweet.utils import *


class Twitter:
    def __init__(self, profile_name=None):
        if profile_name:
            self.profile_url = f"https://twitter.com/{profile_name}"
        else:
            sys.exit(f"Script Aborting : Need profile name")
        self.user_by_screen_url = "https://twitter.com/i/api/graphql/B-dCk4ph5BZ0UReWK590tw/UserByScreenName?variables="
        self.tweets_url = "https://twitter.com/i/api/graphql/Lya9A5YxHQxhCQJ5IPtm7A/UserTweets?variables="
        self.guest_token_url = "https://api.twitter.com/1.1/guest/activate.json"
        self.proxy = {"http": random.choice(get_proxy())}
        self.guest_token = self.__get_guest_token()
        self.guest_headers = get_headers(self.guest_token)

    def __get_guest_token(self, max_retries=10):
        try:
            guest_token = ""
            for i in range(0, int(max_retries)):
                response = requests.get(self.profile_url, headers=get_headers(), proxies=self.proxy)
                guest_token_ = re.findall(
                    'document\.cookie = decodeURIComponent\("gt=(.*?); Max-Age=10800; Domain=\.tweet\.com; Path=/; Secure"\);',
                    response.text)
                try:
                    if guest_token_[0]:
                        guest_token = guest_token_[0]
                        return guest_token
                except IndexError:
                    try:
                        headers = get_headers()
                        headers['x-csrf-token'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                        headers[
                            'authorization'] = "Bearer " + "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
                        headers['content-type'] = 'application/x-www-form-urlencoded'
                        headers['accept'] = "*/*"
                        response = requests.post(self.guest_token_url, headers=headers, proxies=self.proxy)
                        guest_token = response.json()['guest_token']
                        return response.json()['guest_token']
                    except:
                        continue
            if guest_token == "":
                sys.exit(f"Script Aborting : Guest Token couldn't be found after {max_retries} retires.")
        except Exception as e:
            traceback.print_exc()
            sys.exit(f"Script Aborting : Guest Token couldn't be found after {max_retries} retires.\n{e}")

    def __verify_user(self):
        user = self.profile_url.split("/")[-1]
        data = str(get_graph_ql_query(2, user))
        response = requests.get(f"{self.user_by_screen_url}{data}", headers=self.guest_headers, proxies=self.proxy)
        try:
            if response.json()['data']['user']['result']['legacy']['profile_banner_extensions']:
                json_ = response.json()
                return json_
        except:
            return {f"error": "Either User not Found or is Restricted"}

    def get_user_info(self):
        try:
            if self.profile_url:
                json_ = self.__verify_user()
                return json_
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_user_id(self):
        try:
            if self.profile_url:
                user = self.get_user_info()
                try:
                    if "error" in user:
                        return 0
                    else:
                        return user['data']['user']['result']['rest_id']
                except:
                    return 0
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_tweets(self, pages=None, include_extras=False, simplify=True) -> dict:
        try:
            if self.profile_url:
                user_id = self.get_user_id()
                if user_id == 0:
                    return {"error": "Either User not Found or is Restricted"}
                else:
                    result = {"tweets": []}
                    data = str(get_graph_ql_query(1, user_id))
                    response = requests.get(f"{self.tweets_url}{data}", headers=self.guest_headers,
                                            proxies=self.proxy)
                    tweet, __nextCursor = format_tweet_json(response, include_extras=include_extras, simplify=simplify)
                    result['tweets'].append(tweet)
                    if not pages or pages == 1 or pages == "1":
                        return result
                    else:
                        for io in range(2, pages + 1):
                            next_cursor = __nextCursor[0]
                            data = str(get_graph_ql_query(1, user_id, next_cursor))
                            response = requests.get(f"{self.tweets_url}{data}", headers=self.guest_headers,
                                                    proxies=self.proxy)
                            tweet, __nextCursor = format_tweet_json(response, include_extras=include_extras,
                                                                     simplify=simplify)
                            result['tweets'].append(tweet)
                    return result
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)
