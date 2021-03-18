import logging

import discord

from discord.ext import commands
from utils.paginator import Paginator


log = logging.getLogger(__name__)


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(add_reactions=True)
    @commands.command(
        description="Shows the help menu or information for a specific command when specified.",
        usage="help [command]",
        aliases=["h", "commands"],
    )
    async def helptest(self, ctx, *, command: str = None):
        if command:
            command = self.bot.get_command(command.lower())
            if not command:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"That command does not exist. Use `{ctx.prefix}help` to see all the commands.",
                        colour=discord.Colour.red(),
                    )
                )
                return
            embed = discord.Embed(title=command.name, description=command.description, colour=discord.Colour.red())
            usage = "\n".join([ctx.prefix + x.strip() for x in command.usage.split("\n")])
            embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
            if len(command.aliases) > 1:
                embed.add_field(name="Aliases", value=f"`{'`, `'.join(command.aliases)}`")
            elif len(command.aliases) > 0:
                embed.add_field(name="Alias", value=f"`{command.aliases[0]}`")
            await ctx.send(embed=embed)
            return
        all_pages = []
        page = discord.Embed(
            title=f"{self.bot.user.name} Help Menu",
            description="Thank you for using ModMail! Please direct message me if you wish to contact staff. You can "
            "also invite me to your server with the link below, or join our support server if you need further help."
            "\n\nWe released Wyvor - The best feature rich Discord music bot! Check it out now: https://wyvor.xyz.",
            colour=discord.Colour.red(),
        )
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_footer(text="Use the reactions to flip pages.")
        page.add_field(name="Invite", value="https://modmail.xyz/invite", inline=False)
        page.add_field(name="Support Server", value="https://discord.gg/wjWJwJB", inline=False)
        all_pages.append(page)
        page = discord.Embed(title=f"{self.bot.user.name} Help Menu", colour=discord.Colour.red())
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_footer(text="Use the reactions to flip pages.")
        page.add_field(
            name="About ModMail",
            value="ModMail is a feature-rich Discord bot designed to enable your server members to contact staff "
            "easily. A new channel is created whenever a user messages the bot, and the channel will serve as a shared "
            "inbox for seamless communication between staff and the user.",
            inline=False,
        )
        page.add_field(
            name="Getting Started",
            value="Follow these steps to get the bot all ready to serve your server!\n1. Invite the bot with "
            f"[this link](https://modmail.xyz/invite)\n2. Run `{ctx.prefix}setup`, there will be an interactive guide."
            f"\n3. All done! For a full list of commands, see `{ctx.prefix}help`.",
            inline=False,
        )
        all_pages.append(page)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            page = discord.Embed(
                title=cog_name,
                description=f"My prefix is `{ctx.prefix}`. Use `{ctx.prefix}"
                "help <command>` for more information on a command.",
                colour=discord.Colour.red(),
            )
            page.set_author(name=f"{self.bot.user.name} Help Menu", icon_url=self.bot.user.avatar_url)
            page.set_thumbnail(url=self.bot.user.avatar_url)
            page.set_footer(text="Use the reactions to flip pages.")
            for cmd in cog_commands:
                if cmd.hidden is False:
                    page.add_field(name=cmd.name, value=cmd.description, inline=False)
            all_pages.append(page)
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)


    @commands.guild_only()
    @commands.command(
        description="Show some information about yourself or the member specified.",
        usage="userinfo [member]",
        aliases=["memberinfo"],
    )
    async def userinfo(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        roles = [role.name for role in member.roles]
        embed = discord.Embed(title="User Information", colour=discord.Colour.red())
        embed.add_field(name="Name", value=str(member))
        embed.add_field(name="ID", value=member.id)
        embed.add_field(
            name="Status", value=str(member.status).title() + (" (mobile)" if member.is_on_mobile() else "")
        )
        embed.add_field(name="Avatar", value=f"[Link]({member.avatar_url_as(static_format='png')})")
        embed.add_field(
            name="Joined Server", value=member.joined_at.replace(microsecond=0) if member.joined_at else "Unknown"
        )
        embed.add_field(name="Account Created", value=member.created_at.replace(microsecond=0))
        embed.add_field(name="Roles", value=f"{len(roles)} roles" if len(", ".join(roles)) > 1000 else ", ".join(roles))
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(
        description="Get some information about this server.",
        usage="serverinfo",
        aliases=["guildinfo"],
    )
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server Information", colour=discord.Colour.red())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=str(guild.owner) if guild.owner else "Unknown")
        embed.add_field(
            name="Icon", value=f"[Link]({guild.icon_url_as(static_format='png')})" if guild.icon else "*Not set*"
        )
        embed.add_field(name="Server Created", value=guild.created_at.replace(microsecond=0))
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.text_channels) + len(guild.voice_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Emojis", value=len(guild.emojis))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))