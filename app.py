import json
import snscrape.modules.twitter
import time


def lambda_handler():
    LIMIT = 100
    TIMEOUT = 240
    tweets = []

    query = f"nyc -n {LIMIT}"
    print("Running query:", query)

    start_time = time.time()  # utc seconds

    try:
        snscrape_output = enumerate(
            snscrape.modules.twitter.TwitterSearchScraper(query).get_items()
        )

        for i, tweetObject in snscrape_output:
            print(f"{query} TWEET INDEX: {i}")

            tweet = json.loads(tweetObject.json())
            tweets.append(tweet)

            elapsed_time = time.time() - start_time
            if (i >= (LIMIT - 1)) or (elapsed_time > TIMEOUT):
                print(f'Elapsed Time: {elapsed_time}')
                break

        scraped_tweets = []
        for tweet in tweets:
          scraped_tweet = {
            'url': tweet['url'],
            'date': tweet['date'],
            'rawContent': tweet['rawContent'],
            # 'links': tweet['links'],
            'username': tweet['user']['username'],
            'userProfile': tweet['user']['url']
          }

          scraped_tweets.append(scraped_tweet)


        json_object = json.dumps(scraped_tweets, indent=4)

        file_name = query.replace(" ", "_")
        with open(f"{file_name}.json", "w") as outfile:
            outfile.write(json_object)

        print('🚰 data pull complete 🚰')

    except Exception as e:
        print(f"Error: {str(e)}")

        output = {
            "count": len(tweets),
            "results": tweets
        }

        return {
            'statusCode': 500,
            'Error': e,
            'body': json.dumps(output)
        }
