import os
import yt_dlp
import pyrogram

# Replace with your Telegram API ID and API hash
API_ID = '23200408'
API_HASH = 'd6d1c07f075c5d3d028169e408cc892a'
PHONE_NUMBER = '+77078084465'
CHANNEL_NAME = "-1001937677342"

# Create a Pyrogram client
client = pyrogram.Client(
    'my_session',
    bot_token='5936760145:AAHddQ6maPEdphMMkwbx7yHDe1TQsCSQncg',
)

# Start the client
client.start()

# Get the audio file from a YouTube URL using yt_dlp
# url = 'https://www.youtube.com/watch?v=yMBYDHDi-ak'
# with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#     info_dict = ydl.extract_info(url, download=False)
#     audio_url = info_dict['url']
#     print( audio_url )

# Send the audio file to the Telegram channel
client.send_audio(
    chat_id=CHANNEL_NAME,
    audio='https://rr1---sn-n3cgv5qc5oq-0noe.googlevideo.com/videoplayback?expire=1684059904&ei=oGJgZMifBIaz2roPleSg4AQ&ip=58.126.54.160&id=o-ACCIog89ckgIz4YXVDuRDo_NMjESkq0tI3kW9tvbbk9D&itag=251&source=youtube&requiressl=yes&mh=Pr&mm=31%2C29&mn=sn-n3cgv5qc5oq-0noe%2Csn-n3cgv5qc5oq-bh2sz&ms=au%2Crdu&mv=m&mvi=1&pl=25&initcwndbps=2256250&spc=qEK7B_K_Q5CU2E47lg-t7fDV5gVyQm4&vprv=1&svpuc=1&mime=audio%2Fwebm&gir=yes&clen=2909527&dur=170.441&lmt=1683366960842400&mt=1684037824&fvip=7&keepalive=yes&fexp=24007246%2C24363393&beids=24472435&c=ANDROID&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAL92Wnun32Uy8eqWEqz2yT2erzdRDBETXnJHY-VGTmtdAiEAzp5XBRiiBnQIY8zGIKmWdseh0D_w6vDT9wVmJdax1e8%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAJIxFqqjq8aby-oi4CmeL4RXTj1MJ0sBbMq4fmElnNcOAiARWWgNHh8Cu11UI1OkbM2LJ5FfHMcGarYRNV7zRBNOrA%3D%3D',
    title='Audio title',
    performer='Audio performer'
)

# Stop the client
client.stop()
