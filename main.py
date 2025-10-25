import os
from flask import Flask, request
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

API_ID = 29169428
API_HASH = "55742b16a85aac494c7944568b5507e5"
BOT_TOKEN = "8303813448:AAEy5txrGzcK8o_0AhX-40YudvdEa0hpgNY"

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
flask_app = Flask(__name__)

def download_video(url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@app.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    await message.reply("Hi! Send me a video link, and I will download it for you.")

@app.on_message(filters.private & filters.text)
async def handle_link(client, message: Message):
    url = message.text.strip()
    msg = await message.reply("Downloading your video... ⏳")
    try:
        file_path = download_video(url)
        await msg.edit("Uploading your video... 🚀")
        await message.reply_video(file_path)
        os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Failed to download video.\nError: {e}")

@flask_app.route("/", methods=["GET", "POST", "HEAD"])
def keep_alive():
    return "Bot is alive", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def run_bot():
    app.run()

Thread(target=run_flask).start()
run_bot()
