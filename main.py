from tweet.twitter import Twitter

all_tweets = Twitter("elonmusk").get_tweets(pages=1)

n = 0
for tweet in all_tweets['tweets'][0]['result']['tweets']:
    if n < 10:
        print(f"{tweet['created_on']}\n{tweet['tweet_body']}\n")
        n += 1
