import asyncio
import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
from config import CHANNEL_ID, ROLE_ID


class DailyReminder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._task: asyncio.Task | None = None

    async def cog_load(self):
        self._task = self.bot.loop.create_task(self._reminder_loop())

    async def cog_unload(self):
        if self._task:
            self._task.cancel()

    # ---------- 背景迴圈 ----------
    async def _reminder_loop(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel or not isinstance(channel, discord.TextChannel):
            print(f"❌ 找不到提醒頻道 ID: {CHANNEL_ID}")
            return

        role = channel.guild.get_role(ROLE_ID)
        if not role:
            print(f"❌ 找不到身份組 ID: {ROLE_ID}")
            return

        print(f"⏰ 每日提醒已啟動，頻道：{channel.name}")

        while not self.bot.is_closed():
            try:
                now = datetime.utcnow()
                target = time(14, 0)           # 台灣 22:00 = UTC 14:00
                next_run = datetime.combine(now.date(), target)
                if now >= next_run:
                    next_run += timedelta(days=1)

                wait_sec = (next_run - now).total_seconds()
                print(f"下次提醒：{next_run} UTC（{wait_sec:.0f} 秒後）")
                await asyncio.sleep(wait_sec)

                await channel.send(f"{role.mention} 請...記得...打卡...！")
                print("✅ 已發送每日提醒")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"每日提醒錯誤: {e}")
                await asyncio.sleep(3600)


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyReminder(bot))
