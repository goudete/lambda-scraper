import json
import snscrape.modules.twitter
import time
import jsonpickle


def lambda_handler(event, context):
    LIMIT = 10
    TIMEOUT = 90
    tweets = []

    query = f"porsche 911 turbo -n {LIMIT}"
    print("Running query:", query)

    start_time = time.time()  # utc seconds

    try:
        snscrape_output = enumerate(
            snscrape.modules.twitter.TwitterSearchScraper(query).get_items()
        )

        for i, tweetObject in snscrape_output:
            print(f"{query} TWEET INDEX: {i}")
            tweets.append(
                jsonpickle.decode(
                    jsonpickle.encode(
                        tweetObject
                    )
                )
            )

            elapsed_time = time.time() - start_time
            if (i >= (LIMIT - 1)) or (elapsed_time > TIMEOUT):
                print(f'Elapsed Time: {elapsed_time}')
                break

        output = {
            "count": len(tweets),
            "results": tweets
        }

        print(tweets)

        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }
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
