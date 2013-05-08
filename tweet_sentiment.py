# Author: Tom Ravenscroft
# Any word not in AFINN-111.txt should be given a score of 0.

import sys
import json
import re

def build_dict(fn):

    sentiment_file = open(fn)

    # initialize an empty dictionary
    scores = {}

    for line in sentiment_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    # Return the complete dictionary.
    return scores

# Build a dictionary containing tweet text.
def extract_tweets(fn):

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

def judge_sentiments(tweets, sentiments):
    """Compile a sentiment score for every tweet in a list."""

    # Iterate over tweets.
    for tweet in tweets:
        tweet_score = 0
        tweet_words = re.findall(r"[\w']+", tweet)

        # Iterate over words in tweet.
        for word in tweet_words:
            word_score = sentiments[word.lower()] if word.lower() in sentiments else 0
            tweet_score += word_score

        # Requirement that answer is printed as a float.
        print float(tweet_score)



# Print number of lines in a file.
def lines(fp):
    print str(len(fp.readlines()))

def main():
    # Populate the sentiment scores dictionary.
    scores = build_dict(sys.argv[1])

    # Populate the list of tweets.
    tweets = extract_tweets(sys.argv[2])

    # Parse tweets and return scores.
    sentiments = judge_sentiments(tweets, scores)

if __name__ == '__main__':
    main()
