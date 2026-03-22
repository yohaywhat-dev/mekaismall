import asyncio
import discord
from discord.ext import commands
from config import TOKEN, GUILD_ID
from keep_alive import keep_alive
from decision_maker import setup as setup_decide

# ---------- Bot 設定 ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

setup_decide(bot)

# ---------- 載入 Cogs ----------
async def load_cogs():
    await bot.load_extension("cogs.reaction_roles")
    await bot.load_extension("cogs.daily_reminder")
    await bot.load_extension("cogs.daily_topic")

# ---------- on_ready ----------
@bot.event
async def on_ready():
    print(f"✅ 已登入：{bot.user}")
    print(f"監控伺服器 ID: {GUILD_ID}")

    guild = bot.get_guild(GUILD_ID)
    if guild:
        print(f"🤖 機器人暱稱: {guild.me.display_name}")

    # 同步 Slash Commands
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Slash Commands 已同步到伺服器 {GUILD_ID}")
    except Exception as e:
        print(f"⚠️ 伺服器同步失敗 ({e})，嘗試全局同步...")
        try:
            await bot.tree.sync()
            print("✅ Slash Commands 已全局同步")
        except Exception as e2:
            print(f"❌ 全局同步也失敗: {e2}")

# ---------- 啟動 ----------
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    if TOKEN:
        keep_alive()
        asyncio.run(main())
    else:
        print("❌ 找不到 DISCORD_TOKEN 環境變數！")
