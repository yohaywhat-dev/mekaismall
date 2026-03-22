import discord
from discord.ext import commands
from config import GUILD_ID, REACTION_CHANNEL, REACTION_EMOJI, REACTION_ROLE_NAME


class ReactionRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------- 核心邏輯 ----------
    async def process_reaction_role(
        self,
        guild_id: int,
        channel_id: int,
        user_id: int,
        emoji,
        add_role: bool,
    ):
        if guild_id != GUILD_ID:
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        channel = guild.get_channel(channel_id)
        if not channel or channel.name != REACTION_CHANNEL:
            return

        if str(emoji) != REACTION_EMOJI:
            return

        role = discord.utils.get(guild.roles, name=REACTION_ROLE_NAME)
        if not role:
            print(f"找不到身份組: {REACTION_ROLE_NAME}")
            return

        member = guild.get_member(user_id)
        if not member:
            try:
                member = await guild.fetch_member(user_id)
            except (discord.NotFound, discord.Forbidden):
                return

        try:
            if add_role and role not in member.roles:
                await member.add_roles(role)
                print(f"✅ 已為 {member.display_name} 添加身份組: {REACTION_ROLE_NAME}")
            elif not add_role and role in member.roles:
                await member.remove_roles(role)
                print(f"✅ 已為 {member.display_name} 移除身份組: {REACTION_ROLE_NAME}")
        except discord.Forbidden:
            print("❌ Bot 沒有權限管理身份組")
        except Exception as e:
            print(f"❌ 操作身份組時發生錯誤: {e}")

    # ---------- 事件監聽 ----------
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        await self.process_reaction_role(
            reaction.message.guild.id,
            reaction.message.channel.id,
            user.id, reaction.emoji, add_role=True,
        )

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        await self.process_reaction_role(
            reaction.message.guild.id,
            reaction.message.channel.id,
            user.id, reaction.emoji, add_role=False,
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        await self.process_reaction_role(
            payload.guild_id, payload.channel_id,
            payload.user_id, payload.emoji, add_role=True,
        )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        await self.process_reaction_role(
            payload.guild_id, payload.channel_id,
            payload.user_id, payload.emoji, add_role=False,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionRoles(bot))
