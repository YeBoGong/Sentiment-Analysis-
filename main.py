"""
Ye Bo Gong
11/17/2023
This file should take input from the user and call the functions in sentiment_analysis.py
"""

# Import the sentiment_analysis module
from sentiment_analysis import *


from sentiment_analysis import *

def main():
    # Prompting the user for file names for keywords, tweets, and output report

    keyword_file = input("Input keyword filename (.tsv file): ")
    tweet_file = input("Input tweet filename (.csv file): ")
    report_file = input("Input filename to output report in (.txt file): ")

    try:
        # Reading keywords and validating if the list is not empty

        keywords = read_keywords(keyword_file)
        if not keywords:
            raise Exception("Tweet list or keyword dictionary is empty!")
        # Reading tweets and validating if the list is not empty

        tweets = read_tweets(tweet_file)
        if not tweets:
            raise Exception("Tweet list or keyword dictionary is empty!")
        # Generating the sentiment analysis report

        report = make_report(tweets, keywords)
        write_report(report, report_file)
    except Exception as e:
        print(e)
#Calling the main function

main()





# Add code for main() here.
# This should get input from the user and call the
# required functions from sentiment_analysis.py

#Calling the main function

main()