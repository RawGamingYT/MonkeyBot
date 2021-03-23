from discord.ext import commands
import os
from Reddit import Reddit

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="m!")
bot.add_cog(Reddit(bot))

@bot.event
async def on_ready():
	print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))


bot.run(BOT_TOKEN)