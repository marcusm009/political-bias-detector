import tweepy # Uses tweepy library for Twitter API routes

consumer_key = 'X2hKM4bqPkeD4iVkQLF9YhCjD'
consumer_secret = 'd9qYqBGDAU56h5g0fVLRhapk8bvIF1kH9EIwetwJpXE5XqeNZz'

access_token = '1229514152609116160-MW0QV583dFmA8CoE68NSkOOLgL9FJZ'
access_token_secret = 'DiyhhsFvX3Rq1Zj4YR8xYoRjNqmwPn4QThNjO7IRKHM7w'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Gets tweet as a JSON value with tweet ID
tweet = api.get_status(1230878481543725056)
print('\n' + tweet.text + '\n')


