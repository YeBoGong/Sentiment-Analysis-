"""
Ye Bo Gong
11/17/2023
This file will analyze the sentiment of tweets, it will read keywords, clean tweets and calculate sentiments
"""


def read_keywords(keyword_file_name):
    """
        Reads a keyword file and returns a dictionary  keywords to their sentiment scores.

        :param keyword_file_name: Name of the keyword file.
        :return: A dictionary with keywords as keys and their scores as values.
        """
    try:
              #open the keyword file

        with open(keyword_file_name, 'r') as file:
            #split each line by a tab

            return {line.split('\t')[0]: int(line.split('\t')[1]) for line in file}
    except IOError:
        # Handling the exception if the file cannot be opened/read, and printing an error message.

        print(f"Could not open file {keyword_file_name}!")
        return {}



def clean_tweet_text(tweet_text):
    # Cleans the tweet text by removing non-alphabetical characters and converting to lower case

    return ''.join(char.lower() for char in tweet_text if char.isalpha() or char.isspace())

def calc_sentiment(tweet_text, keyword_dict):
    #Calculates the sentiment score of a tweet based on the keyword dictionary.

    return sum(keyword_dict.get(word, 0) for word in tweet_text.split())



def classify(score):
    #Classifies the sentiment score as positive, negative, or neutral.

    return 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'



def read_tweets(tweet_file_name):
    #Reads tweet data from a file and returns a list of tweets.

    try:
        # Attempt to open the specified file for reading

        with open(tweet_file_name, 'r') as file:
            tweets = [] # Initialize an empty list to store tweets
            for line in file:
                # Splitting the CSV line into components
                components = line.strip().split(',')

                # Constructing the tweet dictionary
                tweet = {
                    'date': components[0], #Tweet Date
                    'text': clean_tweet_text(components[1]), #Cleaned text
                    'user': components[2], #Username
                    'retweet': int(components[3]), # # of retweets
                    'favorite': int(components[4]), # # of favorites
                    'lang': components[5], # language

                    #Checking for 'NULL' values
                    'country': components[6] if components[6] != 'NULL' else 'NULL',
                    'state': components[7] if components[7] != 'NULL' else 'NULL',
                    'city': components[8] if components[8] != 'NULL' else 'NULL',
                    'lat': float(components[9]) if components[9] != 'NULL' else 'NULL',
                    'lon': float(components[10]) if components[10] != 'NULL' else 'NULL'
                }
                tweets.append(tweet)  # Add the tweet dictionary to the list
            return tweets
    except IOError:
        # Handling the exception if the file cannot be opened/read, and printing an error message.

        print(f"Could not open file {tweet_file_name}!")
        # Returning an empty list in case of an error

        return []




def make_report(tweet_list, keyword_dict):

    #   Writes the sentiment analysis report to a file.

    # Initialize counters and accumulators
    num_tweets = len(tweet_list)
    total_sentiment = 0
    num_positive = num_negative = num_neutral = 0
    num_retweet = 0
    num_favorite = 0
    tot_retweet = 0
    tot_favorite = 0
    country_sentiment = {}
    country_counts = {}

    # Process each tweet
    for tweet in tweet_list:
        sentiment = calc_sentiment(tweet['text'], keyword_dict)
        total_sentiment += sentiment
        classification = classify(sentiment)
        # Track retweeted and favorited tweet statistics

        if tweet['retweet'] > 0:
            num_retweet += 1
            tot_retweet += sentiment
        # Count tweets by sentiment classification

        if tweet['favorite'] > 0:
            num_favorite += 1
            tot_favorite += sentiment
        # Count positive, negative, neutral tweets
        if classification == 'positive':
            num_positive += 1
        elif classification == 'negative':
            num_negative += 1
        else:
            num_neutral += 1

        # Country statistics
        country = tweet.get('country')
        if country and country != 'NULL':
            country_sentiment[country] = country_sentiment.get(country, 0) + sentiment
            country_counts[country] = country_counts.get(country, 0) + 1

    # Compute averages and top countries
    avg_sentiment = round(total_sentiment / num_tweets, 2) if num_tweets else 'NAN'
    sorted_countries = sorted(country_sentiment, key=lambda k: country_sentiment[k] / country_counts[k], reverse=True)[:5]

    if num_retweet == 0:
        tot_retweet = 'NAN'
    else:
        tot_retweet = round(tot_retweet/num_retweet, 2)

    if num_favorite == 0:
        tot_favorite = 'NAN'
    else:
        tot_favorite = round(tot_favorite/num_favorite, 2)


    # Compile report
    report = {
        'avg_favorite': tot_favorite,
        'avg_retweet': tot_retweet,
        'avg_sentiment': avg_sentiment,
        'num_tweets': num_tweets,
        'num_favorite': num_favorite,
        'num_retweet': num_retweet,
        'num_positive': num_positive,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'top_five': ', '.join(sorted_countries)
    }

    return report

def write_report(report, output_file):
    #   Writes the sentiment analysis report to the specified output file.

    try:
        # Attempt to open the specified output file in write mode
        with open(output_file, 'w') as file:
            # Writing each piece of information from the report to the file
            file.write(f"Average sentiment of all tweets: {report['avg_sentiment']}\n")
            file.write(f"Total number of tweets: {report['num_tweets']}\n")
            file.write(f"Number of positive tweets: {report['num_positive']}\n")
            file.write(f"Number of negative tweets: {report['num_negative']}\n")
            file.write(f"Number of neutral tweets: {report['num_neutral']}\n")
            file.write(f"Number of favorited tweets: {report['num_favorite']}\n")
            file.write(f"Average sentiment of favorited tweets: {report['avg_favorite']}\n")
            file.write(f"Number of retweeted tweets: {report['num_retweet']}\n")
            file.write(f"Average sentiment of retweeted tweets: {report['avg_retweet']}\n")
            file.write(f"Top five countries by average sentiment: {report['top_five']}\n")
            # Confirmation message for successful writing
            print(f"Wrote report to {output_file}")
    except IOError:
        # Handling the exception if the file cannot be opened/written to, and printing an error message.
        print(f"Could not open file {output_file}")

