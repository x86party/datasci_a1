import urllib
import json

# Open a URL and store the response.
response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")

# Assert that the result is JSON.
json_response = json.load(response)

# print type(json_response)
# print type(json_response["results"])
# print json_response["results"][0].keys()

for tweet in json_response["results"]:
    print "TWEET: " + tweet["text"] + "\n"

