import discord

from discord.ext import commands

from utils.json_loader import read_json, write_json


class Prefix(commands.Cog):

    """Prefix Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, brief="Prefix Options")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx):
        """Prefix Commands group."""

        prefixes = read_json("prefixes")
        try:
            prefix = prefixes[str(ctx.guild.id)]
        except KeyError:
            prefix = "="

        embed = discord.Embed(
            title="Prefix Commands",
            description=f"My prefix for this server is `{prefix}`. "
            "I will also respond if you mention me.",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(
            name="Changing your servers prefix",
            value="To change your servers prefix, "
            f"run `{prefix}prefix change <newprefix>` "
            "(If it contains a space, you need to surround it with quotations)",
            inline=False,
        )
        embed.add_field(
            name="Resetting your servers prefix",
            value=f"To reset your servers prefix, "
            f"run `{prefix}prefix reset` and your prefix will be changed back to `=`.",
            inline=False,
        )
        await ctx.send(embed=embed)

    @prefix.command(aliases=["change", "new", "swap", "switch"], brief="Change prefix")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def changeprefix(self, ctx, prefix):
        """Change my prefix for this server."""

        if len(prefix) > 6:
            return await ctx.send(
                "The prefix must be less than 6 charachters in length."
            )

        prefixes = read_json("prefixes")
        prefixes[str(ctx.guild.id)] = prefix
        write_json(prefixes, "prefixes")

        await ctx.send(f"Prefix changed to: {prefix}")

    @prefix.command(aliases=["delete", "reset", "remove"], brief="Reset Prefix")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def deleteprefix(self, ctx):
        """Reset my prefix for this server."""

        prefixes = read_json("prefixes")

        try:
            prefixes.pop(str(ctx.guild.id))
        except KeyError:
            return await ctx.send("This servers prefix is already `=`.")

        write_json(prefixes, "prefixes")

        await ctx.send(
            "Resetted this servers prefix back to `=`. "
            "If you ever want to change it, run `=prefix change <newprefix>`"
        )


def setup(bot):
    bot.add_cog(Prefix(bot))
