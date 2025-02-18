import asyncio
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import logging
from twikit import Client, TooManyRequests

# Configure logging
logging.basicConfig(filename='tweet_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MINIMUM_TWEETS = 100000
QUERY = 'Kenya Ministry of Agriculture until:2025-02-18 since:2006-01-01'

async def get_tweets(tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(0, 15)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)  # Use asyncio sleep to avoid blocking
        tweets = await tweets.next()
    return tweets

async def main():
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    try:
        global client  # Make client accessible to get_tweets
        client = Client(language='en-US')
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')  # Save cookies after successful login
        client.load_cookies('cookies.json')  # Load cookies

        with open('Kenya Ministry of Agriculture.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

        tweet_count = 0
        tweets = None

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = rate_limit_reset - datetime.now()
                await asyncio.sleep(wait_time.total_seconds())
                continue
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                break  # Exit the loop on other errors

            if not tweets:
                print(f'{datetime.now()} - No more tweets found')
                break

            for tweet in tweets:
                tweet_count += 1
                tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

                with open('Price of Kales Kenya.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

            print(f'{datetime.now()} - Got {tweet_count} tweets')

        print(f'{datetime.now()} - Done! Got {tweet_count} tweets')

    except Exception as e: # Catch any errors during setup
        logging.error(f"A setup error occurred: {e}")

    finally:
        if 'client' in locals() and client: # Check if client was initialized
            await client.close()


if __name__ == "__main__":
    asyncio.run(main())