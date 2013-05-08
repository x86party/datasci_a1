# frequency.py
# Author: Tom Ravenscroft  - 2013

import sys
import json
import re

me = "frequency.py"

def load_tweets(fn):
    """Parses tweets to JSON and returns a list of the text content."""

    #print me+"::load_tweets"

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


def extract_terms(words):
    """Builds a list of whitespace delimited tokens from a list of strings."""

    #print me+"::extract_terms"
    terms_unique = []

    # Get un-unique terms.
    # terms_non_unique = re.findall(r"[\w']+", words)
    terms_non_unique = words.split()

    for term in terms_non_unique:
        if term not in terms_unique: terms_unique.append(term)

    return terms_unique


def calculate_frequencies(terms, words):
    """Calculates the histogram values for terms in a series of tweets."""

    #print me+"::calculate_frequencies"

    # Calculate number of terms in all tweets.
    terms_total = len(re.findall(r"[\w']+", words))

    # Count all the occurrences.
    for term in terms:
        count = words.lower().count(term.lower())
        frequency = float(count)/float(terms_total)
        print term + " " + str(frequency)


def main():
    "Main method."
    #print me+"::main"

    input_file_name = sys.argv[1]
    #print me+"::main:input_file_name #=> " + input_file_name

    # Get list of tweets.
    tweets = load_tweets(input_file_name)

    # Merge tweets into a string.
    tweets_joined = ' '.join(tweets)

    # Get list of terms.
    terms = extract_terms(tweets_joined)

    # Calculate list of frequencies.
    calculate_frequencies(terms, tweets_joined)

if __name__ == '__main__':
    main()
