from discord.ext import commands
import discord
import os
from keep_alive import keep_alive
from utils.json_loader import read_json, write_json
from datetime import datetime
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from discord import Embed
from discord import utils

intents = discord.Intents.default()
# we need members intent too
intents.members = True

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("=")(bot, message)

    prefixes = read_json("prefixes")

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("=")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():	
    print("The bot is online!")
    bot.load_extension("cogs.onMessage")
    bot.load_extension("cogs.prefix")    
    bot.load_extension("cogs.logging")     

@bot.command()
async def C(ctx):
    for user in bot.user.friends:
        profile = await user.profile()
        await ctx.send(profile)
        if not profile.mutual_guilds:
            print ("Friend: " + user.name+"#"+user.discriminator)

@bot.command()
async def paginate(ctx):
    embeds = [
        Embed(title="Ayee Support Help Menu", description="Thank you for using ModMail! Please direct message me if you wish to contact staff. You can also invite me to your server with the link below, or join our support server if you need further help.\n\n\n**Invite**\nhttps://www.dsc.gg/modmail\n\n**Support Server**\nhttps://www.dsc.gg/stormsupport", color=discord.Colour.red()),
        Embed(title="test page 2", description="Nothing interesting here.", color=0x5599ff),
        Embed(title="test page 3", description="Why are you still here?", color=0x191638)
    ]

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@bot.command()
async def help(ctx):
    """Sends the help message"""

    embed = discord.Embed(
        title=f"Set Up Instructions",
        description=
        "This bot automatically sets itself up creating a specific Category for Modmail.",
        colour=discord.Colour.red())
    embed.add_field(name=f"Close Channel Command",
                    value=f"Type `=close`\n"
                    f"In the desired Modmail channel to close the channel.\n",
                    inline=False)
    embed.add_field(name=f"Change Prefix Command",
                    value=f"Type `=prefix change <newprefix>`\n"
                    f"To change your servers prefix, run `=prefix change <newprefix>` (If it contains a space, you need to surround it with quotations)\n",
                    inline=False)
    embed.add_field(name=f"Reset Prefix Command",
                    value=f"Type `=prefix reset`\n"
                    f"To reset your servers prefix, run `=prefix reset` and your prefix will be changed back to `=`.\n",
                    inline=False)
    embed.add_field(name=f"Prefix Help Command",
                    value=f"Type `=prefix`\n"
                    f"Shows the Current Server prefix and the Prefix commands.\n",
                    inline=False)
    embed.add_field(name=f"Anonymous Reply Command",
                    value=f"Type `=areply <user> <message>`\n"
                    f"Replies to the mentioned user Anonymously\n",
                    inline=False)		    		    		    		    
    embed.add_field(
        name=f"FAQ",
        value=f"**How do we reply?**\n"
        f"In the desired Modmail channel just message to reply to that person.\n\n**I Need Help, where do I go?**\nJoin our Support Server [Here](https://discord.gg/jcKUHR8pV8)",
        inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=["anonymousreply"])
async def areply(ctx, *, message: str,):
                topic = ctx.channel.topic
                if topic:
                    member = ctx.guild.get_member(int(topic))                
                    if member:
                        await member.send(f"**Staff#0000:** {message}")

@bot.group(aliases=["snp"])
async def snippet(ctx):
        if ctx.invoked_subcommand is None:
                await ctx.send(f"**Available Snippets**\n`=snippet hi <userid>`\n`=snippet faq <userid>`")





            
@bot.event
async def on_message(message):
    # If the message sender is the bot itself, stop to prevent endless loop.
    if message.author.id == bot.user.id:
        return

    # Reacting to bot being mentioned
    if bot.user in message.mentions:
        embed = discord.Embed(title="Current prefix: `=`",
                              description=None,
                              color=discord.Colour.red())
        await message.channel.send(embed=embed)

    # Make sure to process commands if no on_message event was triggered, else commands won't work.
    # This only applies to the @client.event variant (because it overwrites the default one)
    await bot.process_commands(message)


@snippet.command(aliases=["welcome"])
async def greet(ctx):
                topic = ctx.channel.topic
                if topic:
                    member = ctx.guild.get_member(int(topic))                
                    if member:
                        await member.send(f"**{ctx.author.name}#{ctx.author.discriminator}: ** Hi {member.name}.")

@snippet.command(aliases=["hello"])
async def hi(ctx):
                topic = ctx.channel.topic
                if topic:
                    member = ctx.guild.get_member(int(topic))                
                    if member:
                        await member.send(f"**{ctx.author.name}#{ctx.author.discriminator}: **How may I help?")

@snippet.command()
async def faq(ctx):
                topic = ctx.channel.topic
                if topic:
                    member = ctx.guild.get_member(int(topic))                
                    if member:
                        await member.send(f"**{ctx.author.name}#{ctx.author.discriminator}: **Remember to Read our FAQ before asking. Thanks!")

keep_alive()
bot.run(os.environ.get("TOKEN"))
