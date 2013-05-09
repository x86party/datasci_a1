# term_sentiment.py
# Author: Tom Ravenscroft
# Any word not in AFINN-111.txt should be given a score of 0.

import sys
import json
import re

# -------------------------------------------------------------------------------
# ingest_scores()
# -------------------------------------------------------------------------------
def ingest_scores(fn):

    sentiment_file = open(fn)

    # initialize an empty dictionary
    scores = {}

    for line in sentiment_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    # Return the complete dictionary.
    return scores

# -------------------------------------------------------------------------------
# ingest_tweets()
# -------------------------------------------------------------------------------
# Build a dictionary containing tweet text.
def ingest_tweets(fn):

    tweets_file = open(fn)

    # Initialise empty array
    tweets = []

    for tweet in tweets_file:
        # Parse input strings as JSON.
        json_tweet = json.loads(tweet)

        # Check that there is a text field.
        if "text" in json_tweet.keys():
            text = json_tweet["text"].encode('utf-8')
            tweets.append(text)

    return tweets

# -------------------------------------------------------------------------------
# judge_sentiments()
# -------------------------------------------------------------------------------
def judge_sentiments(tweets, sentiments):
    """Compile a sentiment score for every tweet in a list."""

    # Iterate over tweets.
    for tweet in tweets:
        tweet_score = 0
        tweet_words = re.findall(r"[\w']+", tweet)

        # Get the score of a tweet.
        for word in tweet_words:
            word_score = sentiments[word.lower()] if word.lower() in sentiments else 0
            tweet_score += word_score

        # Print the score of all words.
        for word in tweet_words:
            word_score = sentiments[word.lower()] if word.lower() in sentiments else (float(tweet_score)/len(tweet_words))
            print word + " " + str(float(word_score))

# -------------------------------------------------------------------------------
# main()
# -------------------------------------------------------------------------------
def main():
    # Populate the sentiment scores dictionary.
    scores = ingest_scores(sys.argv[1])

    # Populate the list of tweets.
    tweets = ingest_tweets(sys.argv[2])

    # Parse tweets and return scores.
    judge_sentiments(tweets, scores)

if __name__ == '__main__':
    main()

