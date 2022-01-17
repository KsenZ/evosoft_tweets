import random
import string
from bs4 import BeautifulSoup as bs
import requests


def get_proxy() -> list:
    result = requests.get("https://free-proxy-list.net/")
    soup = bs(result.content, "html.parser")
    tds = soup.find("tbody").find_all("tr")
    proxies = []
    for td in tds:
        proxies.append(f"{td.find_all('td')[0].text}:{td.find_all('td')[1].text}")
    return proxies


def get_graph_ql_query(typed, user, pages=None) -> str:
    if typed == 1:
        """
        {
            "userId":"",
            "count":20,
            "cursor":""
            "withTweetQuoteCount":true,
            "includePromotedContent":true,
            "withSuperFollowsUserFields":false,
            "withUserResults":true,
            "withBirdwatchPivots":false,
            "withReactionsMetadata":false,
            "withReactionsPerspective":false,
            "withSuperFollowsTweetFields":false,
            "withVoice":true
        }
        """
        if pages:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22cursor%22%3A%22''' + pages + '''%22%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
        else:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
    else:
        """
        {
             "screen_name":f"{user}",
             "withSafetyModeUserFields":True,
             "withSuperFollowsUserFields":False
         }
        """
        data = '''%7B%22screen_name%22%3A%22''' + user + '''%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%7D'''
    return data


def get_headers(typed=None) -> dict:
    if not typed:
        headers = {
            "authority": "tweet.com",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "x-tweet-client-language": "en",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "upgrade-insecure-requests": "1",
            "sec-ch-ua-platform": 'Windows"',
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
    else:
        headers = {
            'x-csrf-token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'authorization': "Bearer " + "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            'content-type': "application/json",
            'referer': "https://twitter.com/AmitabhJha3",
            "authority": "tweet.com",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "x-tweet-client-language": "en",
            "upgrade-insecure-requests": "1",
            "sec-ch-ua-platform": 'Windows"',
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "x-guest-token": typed
        }
    return headers


def simplify_tweet(tweet, rest_id):
    try:
        created_on = tweet['created_at'] if tweet['created_at'] else ""
    except KeyError:
        created_on = ""
    rest_id = rest_id
    try:
        is_retweet = True if str(tweet['full_text']).startswith("RT") else False
    except:
        is_retweet = False
    try:
        if is_retweet:
            text = tweet['retweeted_status_result']['result']['legacy']['full_text']
        else:
            text = tweet['full_text'] if tweet['full_text'] else ""
    except KeyError:
        text = ""
    try:
        is_reply = True if tweet['in_reply_to_status_id'] is not None or tweet[
            'in_reply_to_user_id'] is not None else False
    except:
        is_reply = False
    try:
        language = tweet['lang'] if tweet['lang'] else ""
    except KeyError:
        language = ""
    try:
        likes = tweet['favorite_count'] if tweet['favorite_count'] else ""
    except KeyError:
        likes = ""
    try:
        retweet_count = tweet['retweet_count'] if tweet['retweet_count'] else ""
    except KeyError:
        retweet_count = ""
    try:
        source = str(tweet['source']).split(">")[1].split("<")[0] if tweet['source'] else ""
    except KeyError:
        source = ""
    try:
        media = tweet['entities']['media'] if tweet['entities']['media'] else ""
    except KeyError:
        media = ""
    try:
        mentions = tweet['entities']['user_mentions'] if tweet['entities']['user_mentions'] else ""
    except KeyError:
        mentions = ""
    try:
        urls = tweet['entities']['urls'] if tweet['entities']['urls'] else ""
    except KeyError:
        urls = ""
    try:
        hashtags = tweet['entities']['hashtags'] if tweet['entities']['hashtags'] else ""
    except KeyError:
        hashtags = ""
    try:
        symbols = tweet['entities']['symbols'] if tweet['entities']['symbols'] else ""
    except KeyError:
        symbols = ""
    result = {
        "created_on": created_on,
        "is_retweet": is_retweet,
        "is_reply": is_reply,
        "tweet_id": rest_id,
        "tweet_body": text,
        "language": language,
        "likes": likes,
        "retweet_counts": retweet_count,
        "source": source,
        "media": media,
        "user_mentions": mentions,
        "urls": urls,
        "hashtags": hashtags,
        "symbols": symbols
    }
    return result


def format_tweet_json(response, include_extras, simplify):
    tweet = {
        "result": {
            "tweets": []
        }
    }
    __cursor = []
    for i in response.json()['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']:
        if str(i['entryId']).split("-")[0] == "tweet":
            try:
                if simplify:
                    tweet['result']['tweets'].append(
                        simplify_tweet(i['content']['itemContent']['tweet_results']['result']['legacy'],
                                       i['content']['itemContent']['tweet_results']['result']['rest_id']))
                else:
                    tweet['result']['tweets'].append(i['content']['itemContent']['tweet_results']['result']['legacy'])
            except:
                pass
        elif str(i['entryId']).split("-")[0] == "cursor":
            if i['content']['cursorType'] == "Bottom":
                __cursor.append(i['content']['value'])
        else:
            if include_extras is True:
                if str(i['entryId']).split("-")[0] in tweet['result']:
                    pass
                else:
                    tweet['result'][f"{str(i['entryId']).split('-')[0]}"] = []
                tweet['result'][f"{str(i['entryId']).split('-')[0]}"].append(i)
            else:
                pass
    return tweet, __cursor
