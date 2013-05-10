# term_sentiment.py
# Author: Tom Ravenscroft
# Any word not in AFINN-111.txt must have a new score calculated
# based on the score of other tweets it appears in.

import sys
import json

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
# Note: This is definitely not the most efficient approach. But it does work.
# -------------------------------------------------------------------------------
def judge_sentiments(tweets, sentiments):
    """Compile a sentiment score for every tweet in a list."""

    tweet_scores = []
    term_sentiments = {}

    # Iterate over tweets.
    for tweet in tweets:
        tweet_score = 0
        tweet_words = tweet.split()

        # Iterate over words in tweet.
        for word in tweet_words:
            # Score the current word and add its score to the corresponding tweet score.
            word_score = sentiments[word.lower()] if word.lower() in sentiments else 0
            tweet_score += word_score

            # Add the term and its sentiment to the dict.
            if word not in term_sentiments.keys():
                term_sentiments[word] = word_score

        # Add the tweet and score to tweet_scores.
        tweet_scores.append([tweet,tweet_score])

    # Every term in the dictionary of terms.
    for term in term_sentiments:

        # Check if a term is in the known sentiments.
        if term not in sentiments:
            # Unknown terms have a base score of zero and we assume we've seen them at least once.
            new_score = 0
            num_occurances = 1

            # Find all of the tweets that contain the new term.
            for i in range(0,len(tweet_scores)):
                if term in tweet_scores[i][0]:
                    new_score += tweet_scores[i][1]
                    num_occurances += 1

            # Normalise the new score by number of occurrences.
            new_score /= num_occurances
            term_sentiments[term] = new_score

        print term+" "+str(float(term_sentiments[term]))

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

