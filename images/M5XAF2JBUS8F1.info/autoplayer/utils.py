from functools import cache as _cache
import os
import subprocess
from dotenv import load_dotenv
from time import sleep
import ctypes
import psutil
from PIL import Image
import io
from discord_webhook import DiscordWebhook

load_dotenv()

LDPLAYER_PATH = os.environ.get("LDPLAYER_PATH", None)
LDPLAYER9_PATH = os.environ.get("LDPLAYER9_PATH", None)
LDPLAYER4_PATH = os.environ.get("LDPLAYER4_PATH", None)
@_cache
def ldplayer9():
    import reldplayer
    path = LDPLAYER9_PATH if LDPLAYER9_PATH else LDPLAYER_PATH
    if not path:
        return None
    return reldplayer.Player(
        reldplayer.PlayerConfig(path)
    )

@_cache
def ldplayer4():
    import reldplayer
    path = LDPLAYER4_PATH if LDPLAYER4_PATH else LDPLAYER_PATH
    if not path:
        return None
    return reldplayer.Player(
        reldplayer.PlayerConfig(path)
    )

# DEFINED
def ldplayer_kill(player, name : str = None, query : str = None):
    import reldplayer 
    
    player : reldplayer.Player = player
    player.raw_console.quit(mnq_name=name)

def process_kill(name : str):
    for proc in psutil.process_iter():
        if proc.name() == name or proc.cmdline() == name:
            proc.kill()

def ldplayer_startex(player, pkg : str, name : str= None, query : str = None):
    import reldplayer 
    
    player : reldplayer.Player = player
    player.raw_console.launchex(mnq_name=name, apk_package_name=pkg)

def ldplayer_start(player, pkg : str, name : str= None, query : str = None):
    import reldplayer
    
    player : reldplayer.Player = player
    player.raw_console.launch(mnq_name=name, apk_package_name=pkg)

def handle_script(script : str):
    match script:
        case script.endswith(".py"):
            subprocess.Popen(["python", script])
        case script.endswith(".sh"):
            subprocess.Popen(["sh", script])
        case script.endswith(".js"):
            subprocess.Popen(["node", script])
        case _:
            os.startfile(script)

# WEBHOOK

def discord_webhook(image: Image.Image):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        print("No webhook URL provided. (for screenshot image)")
        return

    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # move to the start of the byte array

    webhook = DiscordWebhook(url=webhook_url)

    # Attach the image file
    webhook.add_file(file=img_byte_arr.getvalue(), filename='image.png')

    # Execute the webhook
    response = webhook.execute()
    if response.status_code == 200 or response.status_code == 204:
        print("Image sent successfully.")
    else:
        print(f"Failed to send image. Status code: {response.status_code}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except: #noqa
        return False