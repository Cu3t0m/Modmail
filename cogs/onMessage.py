from discord.ext import commands
from discord import utils
import discord
import asyncio
from utils.json_loader import read_json, write_json




async def embedme(message):
	embedme = discord.Embed(description = message.content, colour = 0x696969)
	embedme.set_author(name = message.author, icon_url = message.author.avatar_url)


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
	
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            
            guild = self.bot.get_guild(guild_id_here)
            categ = utils.get(guild.categories, name="Modmail tickets")
            if not categ:
                overwrites = {
                    guild.default_role:
                    discord.PermissionOverwrite(read_messages=False),
                    guild.me:
                    discord.PermissionOverwrite(read_messages=True)
                }
                categ = await guild.create_category(name="Modmail tickets",
                                                    overwrites=overwrites)

            channel = utils.get(categ.channels, topic=str(message.author.id))
            if not channel:
                channel = await categ.create_text_channel(
                    name=
                    f"{message.author.name}#{message.author.discriminator}",
                    topic=str(message.author.id))
                await channel.send(
                    f"New modmail created by {message.author.mention}")

            embed = discord.Embed(description=message.content, colour=0x696969)
            embed.set_author(name=message.author,
                             icon_url=message.author.avatar_url)
            await channel.send(embed=embed)

        elif isinstance(message.channel, discord.TextChannel):
            if message.content.startswith("="):
                pass
            else:
                topic = message.channel.topic
                if topic:
                    member = message.guild.get_member(int(topic))                
                    if member:
                        await member.send(
                            str('**' + f'{message.author}'[:-5] + ':**') +
                            ' ' + str(message.content))

    @commands.command()
    async def close(self, ctx):
        if ctx.channel.category.name == "Modmail tickets":
            await ctx.send("Deleting the channel...")
            await asyncio.sleep(2)
            await ctx.channel.delete()




def setup(bot):
    bot.add_cog(onMessage(bot))
