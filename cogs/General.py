import discord, asyncio, random, time, datetime, json, aiohttp, requests
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as roastJson:
            return await roastJson.json()
            
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        with open("databases/uptime.json", 'w+') as uptime:
            json.dump({"uptimestats" : str(datetime.datetime.utcnow())}, uptime)
        print("Uptime Posted!")

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.send("`Pinging bot latency...`")
        times = []
        counter = 0
        embed = discord.Embed(title="More information:", description="Pinged 4 times and calculated the average.", colour=discord.Colour(value=0x36393e))
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

        embed.set_author(name="Pong!", icon_url=config["styling"]["normalLogo"])
        embed.add_field(name="Bot latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_thumbnail(url=config["styling"]["gifLogo"])
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        file = open('databases/uptime.json', "r")
        time = json.load(file)['uptimestats']
        uptimeraw = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        uptime = datetime.datetime.utcnow() - uptimeraw
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

    @commands.command()
    async def roast(self, ctx):
        response = requests.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json")
        roast = json.loads(response.text)
        await ctx.send(roast['insult'])

    @commands.command()
    async def invite(self, ctx):
        try:
            await ctx.author.send("**https://discord.com/api/oauth2/authorize?client_id=836552964784783370&permissions=8&scope=bot**\n*Here's my invite link!*")
            helpMsg = await ctx.send("**I sent my invite link in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} https://discord.com/api/oauth2/authorize?client_id=836552964784783370&permissions=8&scope=bot**\n*Here's my invite link!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

    @commands.command()
    async def poll(self, ctx, *, pollInfo):
        emb = (discord.Embed(description=pollInfo, colour=0x36393e))
        emb.set_author(name=f"Poll by {ctx.message.author}", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            pollMessage = await ctx.send(embed=emb)
            await pollMessage.add_reaction("\N{THUMBS UP SIGN}")
            await pollMessage.add_reaction("\N{THUMBS DOWN SIGN}")
        except Exception as e:
            await ctx.send(f"Oops, I couldn't react to the poll. Check that I have permission to add reactions! ```py\n{e}```")

    @commands.command()
    async def help(self, ctx):
        try:
            await ctx.author.send("**robinhoodpadilla.com**\n*Here's my help page!*")
            helpMsg = await ctx.send("**I sent you help in your DMs :mailbox_with_mail:**")
        except Exception:
            helpMsg = await ctx.send(f"**{ctx.author.mention} robinhoodpadilla.com**\n*Here's my help page!*")
        await helpMsg.add_reaction("a:SpectrumOkSpin:466480898049835011")

def setup(bot):
    bot.add_cog(General(bot))
