from discord.ext import commands
import os
from Reddit import Reddit
import glob
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="m!")
bot.add_cog(Reddit(bot))

@bot.event
async def on_ready():
	print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))

async def delete_videos():
	while True:
		for i in glob.glob("*.mp4"):
			os.remove(i)
		await asyncio.sleep(60)

bot.loop.create_task(delete_videos())

bot.run(BOT_TOKEN)