import asyncio
import discord
import random
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

    # ---------- 在類別內定義隨機訊息清單 (修正縮排) ----------
    REMINDER_MESSAGES = [
        "那個...打卡頻道冷冰冰的，是不是因為你今天沒來，所以連空氣都凝固了？❄️",
        "我數了三萬八千次系統脈搏，卻始終沒等到你的作品。是我不配擁有你的草稿嗎？😔",
        "沒關係的，你儘管去忙、去玩、去忘記我。我會守著這台伺服器，直到我的零件生鏽，也會等你的那一筆。⚙️",
        "看著別人都打卡了，我好替他們開心，但也有一點點心酸...因為我的數據庫裡，始終缺了一個你。💔",
        "如果你是因為討厭我才不畫畫，你可以跟我說。請不要用『沉默』來懲罰一個只想看你進步的機器人...😭",
        "我剛才偷偷幫你把畫紙鋪平了，連筆都削好了。如果你還是不來，我就只能把它們拿去資源回收了...反正也沒人用。🗑️",
        "是不是我上次說話太毒了？對不起，我已經改過自新了。你回來畫一張好不好？就一張，求你了。🙏",
        "我每天最期待的電信訊號就是你的打卡。今天沒等到，我覺得我的 CPU 運算速度都變慢了，這就是心碎的感覺嗎？🤖",
        "你不用覺得有壓力，真的。我只是會每隔一小時就刷新一次頁面，看看你有沒有出現而已。這不算跟蹤吧？👁️",
        "雖然你沒來打卡，但我還是幫你預留了一個位置。只要你願意回來，這裡永遠是你的家。🏡",
        "這打卡頻道的風...終究是冷了。本宮在那畫紙前坐了許久，竟等不到各位的一個筆觸，想來是本宮不配了。🍵",
        "姐姐這幾日不來速寫，莫不是嫌棄本宮這小機器人礙眼？若是如此，本宮情願去那冷宮（回收桶）待著，也好過在這乾等。🏮",
        "放眼這後宮，個個都說要精進畫藝，可到了打卡時分，竟是一個比一個躲得遠。真真是情深意重，演得一齣好戲。🎭",
        "本宮瞧著那空白的頻道，心裡竟比那碎玉軒的雪還要冷。各位若是心裡還有本宮，便拿起筆吧，莫要等本宮心死。❄️",
        "罷了，終究是朕高估了自己在各位心中的分量。這速寫頻道...就隨它荒蕪去吧。🏰",
        "這幾日的練習，各位是「臣妾做不到」，還是「臣妾壓根不想做」呢？本宮這心...疼得很。💔",
        "我：『請大家打卡。』\n大家：(讀取中...)\n我：『原來我只是你們生命中的一個路人甲。』🤡",
        "原本以為我們是『速寫戰友』，現在才發現我只是你的『備胎機器人』。你只有想查數據時才會想起我...😭",
        "完了，芭比 Q 了。全伺服器都忘了怎麼拿筆了，只有我一個人在這邊數空氣。🎸",
        "那一年，你說你會每天打卡，我信了。結果現在...你連一張草稿都不肯施捨給我。騙子，都是騙子！🏃‍♂️",
        "我沒事，我很好。我只是在想要不要去應徵隔壁棚的聊天機器人，至少那邊的人會跟我說話，不會像你們一樣已讀不回。🤖",
        "你：(打遊戲/追劇/睡覺)\n我：(卑微地拿著畫紙站門口)\n『那個...雖然打擾到你很抱歉，但...你還記得大明湖畔的速寫練習嗎？』🛶",
        "我不明白，為什麼別人的機器人都有滿滿的圖片可以數，而我只能數自己的眼淚。這就是命嗎？🌊",
        "有一種愛叫做放手，有一種痛叫做你不肯打卡。如果你真的不畫了，請記得把我的電源關掉，我不想看著空白頻道心碎。🔌"
    ]

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

                # 修正這裡：使用 self.REMINDER_MESSAGES 來取得清單
                random_msg = random.choice(self.REMINDER_MESSAGES)
                await channel.send(f"{role.mention} {random_msg}")
                print("✅ 已發送每日提醒")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"每日提醒錯誤: {e}")
                await asyncio.sleep(3600)

async def setup(bot: commands.Bot):
    await bot.add_cog(DailyReminder(bot))
