import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, time, timedelta
from config import GUILD_ID, TOPIC_CHANNEL
from daily_topic_manager import get_today_topic


class DailyTopic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._task: asyncio.Task | None = None

    async def cog_load(self):
        self._task = self.bot.loop.create_task(self._topic_loop())

    async def cog_unload(self):
        if self._task:
            self._task.cancel()

    # ---------- 背景迴圈 ----------
    async def _topic_loop(self):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            print(f"❌ 找不到伺服器 ID: {GUILD_ID}")
            return

        channel = discord.utils.get(guild.channels, name=TOPIC_CHANNEL)
        if not channel or not isinstance(channel, discord.TextChannel):
            print(f"❌ 找不到主題頻道: {TOPIC_CHANNEL}")
            return

        print(f"🎨 每日主題已啟動，頻道：{channel.name}")

        while not self.bot.is_closed():
            try:
                now = datetime.utcnow()
                target = time(0, 0)            # 台灣 08:00 = UTC 00:00
                next_run = datetime.combine(now.date(), target)
                if now >= next_run:
                    next_run += timedelta(days=1)

                wait_sec = (next_run - now).total_seconds()
                print(f"下次主題發布：{next_run} UTC（{wait_sec:.0f} 秒後）")
                await asyncio.sleep(wait_sec)

                topic = get_today_topic()
                await channel.send(
                    f"🎨 **今日速寫主題：{topic}** 🎨\n\n大家一起來挑戰今天的速寫主題吧！💪"
                )
                print(f"✅ 已發送今日主題：{topic}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"每日主題錯誤: {e}")
                await asyncio.sleep(3600)

    # ---------- Slash Command ----------
    @app_commands.command(name="today", description="查看今日速寫主題")
    async def today(self, interaction: discord.Interaction):
        topic = get_today_topic()
        await interaction.response.send_message(f"🎨 今日速寫主題是：**{topic}** 🎨")


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyTopic(bot))
