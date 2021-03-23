from discord.ext import commands
from discord import FFmpegPCMAudio
from redvid import Downloader


class Reddit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if not ctx.guild:
			raise commands.NoPrivateMessage("This command can't be used in DM channels.")
		return True
	
	async def cog_command_error(self, ctx, error):
		await ctx.send(f"An error occurred: {str(error)}")

	@commands.command(name='join', invoke_without_subcommand=True)
	@commands.has_role("DJ")
	async def _join(self, ctx):
		if ctx.author.voice:
			destination = ctx.author.voice.channel
			if ctx.voice_client:
				await ctx.voice_client.move_to(destination)
				if ctx.voice_client:
					await ctx.send("Joined your channel.")
			else:
				await destination.connect()
				if ctx.voice_client:
					await ctx.send("Joined your channel.")
		else:
			await ctx.send("You must be in a voice channel first.")

	@commands.command(name='leave', aliases=['stop', 'disconnect'])
	@commands.has_role("DJ")
	async def _leave(self, ctx):
		if ctx.voice_client:
			await ctx.guild.voice_client.disconnect()
			if not ctx.voice_client:
				await ctx.send("Left the channel.")
		else:
			await ctx.send("Not connected to voice channel.")

	@commands.command(name='play')
	@commands.has_role("DJ")
	async def _play(self, ctx, url):
		if url == None:
            await ctx.send('You must provide a reddit link.')
		else:
			reddit = Downloader(max_q=True)
			reddit.overwrite = True
			reddit.url = url
			reddit.check()
			if reddit.duration <= 300:
				await ctx.invoke(self._join)
				source = FFmpegPCMAudio(reddit.download())
				ctx.voice_client.play(source)
				if ctx.voice_client.is_playing():
					await ctx.send("Playing audio.")
			else:
				await ctx.send("The video can not be longer than 5 mins.")