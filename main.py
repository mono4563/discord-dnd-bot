import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = os.getenv("ROLE_ID")
ROLE_MENTION = f"<@&{ROLE_ID}>" if ROLE_ID else "@here"

# Example: Sunday (6) at 19:00 UTC — change as needed
EVENT_TIMES = [
    {"weekday": 6, "hour": 19, "minute": 0}
]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    check_event.start()

@tasks.loop(minutes=1)
async def check_event():
    now = datetime.utcnow()
    target = now + timedelta(hours=1)
    for ev in EVENT_TIMES:
        next_event = now.replace(hour=ev["hour"], minute=ev["minute"], second=0, microsecond=0)
        days = (ev["weekday"] - now.weekday()) % 7
        next_event += timedelta(days=days)
        if abs((next_event - target).total_seconds()) < 30:
            chan = bot.get_channel(CHANNEL_ID)
            if chan:
                await chan.send(f"{ROLE_MENTION} Reminder: Event starts in 1 hour at {next_event.strftime('%A %H:%M UTC')}!")
            break

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()
bot.run(TOKEN)

