from datetime import datetime
import aiohttp
import logging
from bs4 import BeautifulSoup
import asyncio
from telebot.async_telebot import AsyncTeleBot

BASE_DIR = 'https://z2.fm/'
bot = AsyncTeleBot(token='5936760145:AAHddQ6maPEdphMMkwbx7yHDe1TQsCSQncg')
channel_id = '-1001937677342'
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


async def findMusic(url:str, file_name:str):
    try:
        soup = BeautifulSoup(url, 'lxml')
        id = soup.find('div', class_='whb_gr_r') \
            .find('div', class_='song song-xl')['data-play']
        link = BASE_DIR + 'download/' + id
        print('Sending')
        message = await bot.send_audio(chat_id=channel_id, audio=link)
        # await bot.delete_message(chat_id=channel_id, message_id=message.message_id)
    except Exception as e:
        logging.error(f"\nError in downloading {file_name}."
                        f"\nProbably it can't be found in website."
                        f"\nTry to write more specifically.\n"
                        )


async def start():
    search_url = f'{BASE_DIR}/mp3/search/?keywords='
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        with open('../music_list.txt', 'r') as file:
            for file_name in file:
                file_name = file_name.split()
                url = search_url
                for i in file_name:
                    url += i + '+'
                url = url[:-1]
                print('first')
                async with session.get(url, headers=headers, cookies=cookies) as response:
                    tasks.append(
                        asyncio.create_task(findMusic(await response.text(), (' ').join(file_name)))
                    )

        await asyncio.gather(*tasks)
        await bot.close_session()


def run():
    print("Loading Musics")
    begin = datetime.now()
    asyncio.run(start())
    finish = datetime.now()
    print(finish - begin)
    print("Done")
    print('------------------------------------------------------')
run()