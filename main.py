import shutil

import telegram
import urllib3
from bs4 import BeautifulSoup
import requests
import os
import asyncio

BASE_DIR = 'https://z2.fm/'
bot = telegram.Bot(token='5936760145:AAHddQ6maPEdphMMkwbx7yHDe1TQsCSQncg')
cookies = {
    'ZvcurrentVolume': '100',
    'zvApp': 'detect2',
    'PHPSESSID': '1fa49jdrc6ntb52ls29ve7nf72',
    'zvAuth': '1',
    'zvLang': '0',
    'YII_CSRF_TOKEN': '66c358d860f4e87f0e078a5fb9b4ae663de5bda8',
    'zv': 'tak-tak-tak',
    'ZvcurrentVolume': '100',
}

headers = {
    'authority': 'z2.fm',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'ZvcurrentVolume=100; zvApp=detect2; PHPSESSID=1fa49jdrc6ntb52ls29ve7nf72; zvAuth=1; zvLang=0; YII_CSRF_TOKEN=66c358d860f4e87f0e078a5fb9b4ae663de5bda8; zv=tak-tak-tak; ZvcurrentVolume=100',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
def download_music(link:str, file_name:str):
    with open(f'Downloaded_Music/{file_name}.mp3', "wb") as file:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(link, verify=False)
        file.write(response.content)

# class="song-download btn4 download visited"
def findMusic(url:str, file_name:str):
    soup = BeautifulSoup(url, 'lxml')
    id = soup.find('div', class_='whb_gr_r')\
        .find('div', class_='song song-xl')['data-play']
    url = BASE_DIR + 'download/' + id
    download_music(url, file_name)

# https://z2.fm/mp3/search?keywords=prince+Sueta

def start():
    search_url = f'{BASE_DIR}/mp3/search/?keywords='
    try:
        os.mkdir('Downloaded_Music')
    except FileExistsError:
        ...
    with open('music_list.txt', 'r') as file:
        for music_name in file:
            music_name = music_name.split()
            url = search_url
            for i in music_name:
                url += i + '+'
            url = url[:-1]
            findMusic(requests.get(url, cookies=cookies, headers=headers).text, ' '.join(music_name))


async def send_audio():
    channel_id = '-1001937677342'
    files = os.listdir('Downloaded_Music')
    for f in files:
        with open(f'Downloaded_Music/{f}', 'rb') as audio_file:
            audio_name = f[:f.index('.')].split()
            title = (' ').join(audio_name[:-1])
            await bot.send_audio( chat_id=channel_id, audio=audio_file, title=title, performer=audio_name[-1] )


print("Loading Musics")
start()
print("Done")
print('------------------------------------------------------')


# print('Sending to Telegram')
# asyncio.run(send_audio())
# print('Done')
shutil.rmtree('Downloaded_Music')
