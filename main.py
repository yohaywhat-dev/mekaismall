import asyncio
import discord
from discord.ext import commands
from config import TOKEN, GUILD_ID
from keep_alive import keep_alive
#from decision_maker import setup as setup_decide

# ---------- Bot 設定 ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

#setup_decide(bot)

# ---------- 載入 Cogs ----------
async def load_cogs():
    await bot.load_extension("cogs.reaction_roles")
    await bot.load_extension("cogs.daily_reminder")
    await bot.load_extension("cogs.daily_topic")
    await bot.load_extension("cogs.decision_maker")
    await self.load_extension("cogs.fortune")

# ---------- on_ready ----------
@bot.event
async def on_ready():
    print(f"✅ 已登入：{bot.user}")
    print(f"監控伺服器 ID: {GUILD_ID}")

# --- 加入這段檢查 ---
    # 檢查 Tree 裡面到底抓到了哪些指令
    all_commands = bot.tree.get_commands() 
    print(f"🔍 目前 Tree 內的指令清單: {[cmd.name for cmd in all_commands]}")
    
    if not all_commands:
        print("❌ 警告：Tree 是空的！請檢查指令定義位置。")
        
    
    guild = bot.get_guild(GUILD_ID)
    if guild:
        print(f"🤖 機器人暱稱: {guild.me.display_name}")


    # 同步 Slash Commands - 優先嘗試伺服器同步，失敗則全局同步
    sync_success = False
    try:
        target_guild = discord.Object(id=int(GUILD_ID)) # 這裡加上 int()
        
        # 建議在同步前先做一次 copy_global_to，確保 Cogs 裡的指令被抓進來
        #bot.tree.copy_global_to(guild=target_guild)
        
        await bot.tree.sync(guild=target_guild)
        print(f"✅ Slash Commands 已同步！數量：{len(synced)} 個")
        print(f"✅ Slash Commands 已同步到伺服器 {GUILD_ID}")
        sync_success = True
    except Exception as e:
        print(f"⚠️ 伺服器同步失敗 ({e})，嘗試全局同步...")
        try:
            await bot.tree.sync()
            print(f"✅ Slash Commands 已全局同步")
            sync_success = True
        except Exception as e2:
            print(f"❌ 全局同步也失敗: {e2}")
    
    if not sync_success:
        print("❌ Slash Commands 同步失敗，指令可能無法使用")
        
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
