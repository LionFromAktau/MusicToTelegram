import logging
import os
import yt_dlp
from googleapiclient.discovery import build
import asyncio
from telebot.async_telebot import AsyncTeleBot
from datetime import datetime
from multiprocessing import Pool

SAVE_PATH = 'Downloaded_Music'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'extractaudio': True,
    'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s',
    'quiet': True,
    # 'audioformat': 'mp3',
}

bot = AsyncTeleBot(token='5936760145:AAHddQ6maPEdphMMkwbx7yHDe1TQsCSQncg')
channel_id = '-1001937677342'
# Set up the YouTube API client
api_key = 'AIzaSyDeqsv9mMSOQUPS1XUt9eZe96nH7dTnN0Q'
youtube = build('youtube', 'v3', developerKey=api_key)
ydl = yt_dlp.YoutubeDL(ydl_opts)
urls = []

async def send(file_name):
    print("FIRST")
    with open(file_name.path, 'rb') as file:
        await bot.send_audio(chat_id=channel_id, title=file_name.name, audio=file)

    print("Second")


def playlist_links(playlist_url):
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'dump_single_json': True,
        'playlist_items': '1-',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as y:
        playlist_info = y.extract_info(playlist_url, download=False)

    playlist_items = playlist_info['entries']
    for item in playlist_items:
        urls.append(item['url'])


async def find_music(search_term:str):
    try:
        request = youtube.search().list(
            part='snippet',
            q=search_term,
            type='video',
            videoDefinition='high',
            maxResults=1,
        )
        response = request.execute()
        videoID = response["items"][0]["id"]["videoId"]
        urls.append(f'https://www.youtube.com/watch?v={videoID}')
    except Exception as e:
        logging.error(f"\n{e}"
                      f"\nError in downloading music."
                        f"\nProbably it can't be found in website."
                        f"\nTry to write more specifically.\n"
                        )





async def file_read():
    tasks = []
    with open('../music_list.txt', 'r') as file:
        for file_name in file:
            tasks.append(
                asyncio.create_task(find_music(file_name))
        )
    await asyncio.gather(*tasks)

async def start_send(files = os.scandir("Downloaded_Music")):
    tasks = []
    for i in files:
        tasks.append( asyncio.create_task(send(i)) )
    await asyncio.gather(*tasks)
    await bot.close_session()


def download(url):
    ydl.download([url])


def run(link:str = None):
    begin = datetime.now()

    if link == None:
        asyncio.run(file_read())

    else:
        if 'list' in link:
            playlist_links(link)
        else:
            urls.append(link)

    pool = Pool(len(urls))
    pool.map(download, urls)
    asyncio.run(start_send())
    files = os.scandir('Downloaded_Music')
    for i in files:
        os.remove(i)
    print(f'Done {datetime.now() - begin} sec')

# run()



# begin = datetime.now()
# ydl.download('https://www.youtube.com/playlist?list=PLglAHdOeJRlZORtCQj6qGbVumADhfY30d')
# print(datetime.now() - begin)
# files = os.scandir('Downloaded_Music')
# for i in files:
#     os.remove(i)

info = ydl.extract_info(url='https://www.youtube.com/watch?v=hmpPf1rHfmU', download=False)
print(info['url'])
