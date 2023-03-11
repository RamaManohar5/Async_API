import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import os
import time
import aiohttp
import asyncio
from key import key
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

start_time = time.time()
async def channel_data(url) :
    if url != None:
        try : 
            api_key = key
            soup = BeautifulSoup(urlopen(url), 'html.parser')
            # fetch channel id
            channel_id = soup.find_all('meta', {'itemprop' : 'channelId'})[0].attrs['content']
            # establish a connection to fetch Video_ids of a channel
            channel_url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=25"
            resp = requests.get(channel_url).json() # Jsonifying the data
            video_ids = [item['id']['videoId'] for item in resp['items']] # fetching videoIDs from json data
            
            data = main_sessions(video_ids)
            # run the async process for all the videoIDs
            #asyncio.run(main_sessions(video_ids))
        except Exception as e :
            logging.INFO(e)
            
    return data

async def main_sessions(video_ids) :

    async with aiohttp.ClientSession() as session: # creating single session for all the video_ids APIs calls
        tasks = []
        for video_id in video_ids :
            task = asyncio.ensure_future(video_details(session, video_id))
            tasks.append(task)
    
        scrapped_data = await asyncio.gather(*tasks) # awaiting asynchronisaton for all tasks
        
    print(scrapped_data)

async def video_details(session, video_id) :
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={key}"
    async with session.get(url) as resp :
        resp_json = resp.json()
        return resp_json
    
stop_time = time.time() 

if __name__ == "__main__" : 
    asyncio.run(channel_data('https://www.youtube.com/@prettyprinted/videos'))