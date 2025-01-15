
from dataclasses import dataclass
import datetime
import os
from PIL import Image
from discord_webhook import DiscordWebhook

from autoplayer.utils import discord_webhook

@dataclass
class Debug:
    debug : bool = False
    discordHook : bool = False
    
    def dmessage(self, msg : str):
        if not self.debug:
            return
        
        webhook_url = os.getenv("DISCORD_WEBHOOK")
        if not webhook_url:
            print(f"No webhook URL provided for: {msg}")
            return

        webhook = DiscordWebhook(url=webhook_url)
        webhook.content = msg
        webhook.execute()

    def dscreenshot(self):
        if not self.discordHook or not self.debug:
            return

        import pyscreeze

        image = pyscreeze.screenshot()

        discord_webhook(image)

    def dimage(self, image : Image.Image):
        if not self.debug:
            return

        os.makedirs("debug", exist_ok=True)
        image.save(f"debug/{datetime.datetime.now().timestamp()}.png")