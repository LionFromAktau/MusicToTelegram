import asyncio
from Converter.m3u82mp3 import run_from_cmd
import aiohttp
import vk_api
from vk_api.audio import VkAudio
from multiprocessing import Pool
import itertools
from youtube import start_send

# Authenticate with VK API using your login and password
# token='vk1.a.Gf4ZsuOeGqmnebUNwRjqmPcNYsaJ1MLS5tXG8W8cxtby78dZTVO_MgKYe7oRu3ABNkBdJgcRwoq8M5aiG-5JfA-_PqEyyrtK9K9CyNISSEbK0r-M0E3o168VICRD-3ERviq---Jwh61erndLs8CTlCK1O-nOS0wL8F09QhvBEgTAROspTdLBRPv469oUC4x0qsfDBDR2YXnktns_D4zsLA'
vk_session = vk_api.VkApi(login='87078084465', password="Bratan21012004$")
vk_session.auth()
vk_audio = VkAudio(vk_session)


async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open("../Converter/m3u8Files/"+filename+".m3u8", 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)


async def start_download(urls: list, file_names: list):
    tasks = []
    for i in range(len(urls)):
        tasks.append(asyncio.create_task(download_file(urls[i], file_names[i])))

    await asyncio.gather(*tasks)


def run(id: str | int, number: int):
    global track_iter
    try:
        track_iter = vk_audio.get_iter(owner_id=str(id))
    except Exception as e:
        print(e)
        return
    songs = list(itertools.islice(track_iter, number))
    urls = []
    file_names = []
    for song in songs:
        file_names.append(song['title'])
        urls.append(song['url'])

    asyncio.run(start_download(urls, file_names))

    pool = Pool(len(urls))
    args = list(zip(file_names, file_names))
    pool.starmap(run_from_cmd, args)
    asyncio.run(start_send())

    pool.close()
    pool.join()

run('236866267', 3)