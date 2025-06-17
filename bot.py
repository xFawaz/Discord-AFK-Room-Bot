import asyncio
from colorama import init, Fore
import discord

init(autoreset=True)

# ============================================
#                 قسم الإعدادات 
# ============================================
# " " الصق التوكين حق البوت بين علامتين الاقتباس في السطر 19
# Channel ID ضع ايدي الروم الصوتي الخاص بك
# اختر حالة البوت مثل:
# "playing:AFK"
# "listening:Lo-fi"
# "watching:Tutorial"
# "stream:Live Now:https://twitch.tv/example"

channels_data = {
    "Your Bot Token": (
        1111111111111111111,#<<< ضع ايدي الروم بدل الأرقام 
        "playing:AFK Mode"#<<< حالة البوت
    )
}

# ============================================
#              لا تغير اي شيء هنا
# ============================================

def display_bot_info(user, channel_id):
    print(Fore.CYAN + "="*50)
    print(Fore.CYAN + f"[+] Bot: {user}")
    print(Fore.YELLOW + f"    Connected to Voice Channel: {channel_id}")
    print(Fore.CYAN + "="*50 + "\n")

async def run_bot(token):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    async def connect_to_voice():
        await client.wait_until_ready()
        info = channels_data.get(token)
        if not info:
            print(Fore.RED + "[-] No configuration found for the token.")
            return

        channel_id = info[0]
        for guild in client.guilds:
            ch = guild.get_channel(channel_id)
            if isinstance(ch, discord.VoiceChannel):
                try:
                    await ch.connect(self_deaf=True)
                    display_bot_info(client.user, channel_id)
                except Exception as e:
                    print(Fore.RED + f"[-] Failed to connect to channel {channel_id}: {e}")

    @client.event
    async def on_ready():
        print(Fore.GREEN + f"[+] {client.user} is ready.")
        info = channels_data.get(token)
        if info and len(info) == 2:
            status = info[1]
            parts = status.split(":", 2)
            atype = parts[0].lower()
            name = parts[1]
            url = parts[2] if len(parts) == 3 else None

            activity = None
            if atype == "playing":
                activity = discord.Game(name=name)
            elif atype == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=name)
            elif atype == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=name)
            elif atype == "stream" and url:
                activity = discord.Streaming(name=name, url=url)

            if activity:
                await client.change_presence(activity=activity)
        
        await connect_to_voice()

    await client.start(token)

async def main():
    print(Fore.YELLOW + "Starting bot...\nDeveloped By Myth, For Support - Instagram @x4y\n")
    tasks = [run_bot(token) for token in channels_data]
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    asyncio.run(main())