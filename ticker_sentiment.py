import re
import asyncpraw
import asyncio
from requests.models import HTTPError
import yfinance
import simfin as sf
from urllib.error import HTTPError
from collections import Counter
from datetime import datetime

sf.set_api_key('free')
sf.set_data_dir('~/simfin_data/')
df = sf.load_income(variant='annual', market='us')

tickerRE = re.compile(r"(?:\s)?([A-Z\-\.]{1,5})(?![a-z’'\.]+)(?:\s)?")

async def run():

    username = 'REDDIT_USER'
    passwd = 'REDDIT_PASSWORD'

    reddit = asyncpraw.Reddit(
    client_id='CLIENT_ID',
    client_secret='CLIENT_SECRET',
    password=f'{passwd}',
    username=f'{username}',
    user_agent=f'Ticker Sentiment Tracker (by u/{username})'
    )
    reddit.read_only = True

    tickersSentiment = {}
    started = datetime.now()

    sub = await reddit.subreddit('wallstreetbets')
    async for comment in sub.stream.comments(skip_existing=True):
        match = tickerRE.findall(comment.body)
        if match:
            potentialTickers = set(match)
            if len(potentialTickers) > 5:
                # Don't need spam
                continue
            for ticker in potentialTickers:
                if ticker in df.index:
                    if ticker in tickersSentiment.keys():
                        tickersSentiment[ticker] += 1
                    else:
                        tickersSentiment[ticker] = 1
                else:
                    try:
                        stock = yfinance.Ticker(ticker)
                        open = stock.info['regularMarketOpen']
                        if ticker in tickersSentiment.keys():
                            tickersSentiment[ticker] += 1
                        else:
                            tickersSentiment[ticker] = 1
                    except (KeyError, ValueError, HTTPError, IndexError):
                        continue
            print('\n\n\n\n\n')
            print(f'Started: {started} - mentions for {datetime.now()}:')
            for ticker, mentions in dict(Counter(tickersSentiment).most_common(20)).items():
                print(f'{ticker}: {mentions} mentions')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())