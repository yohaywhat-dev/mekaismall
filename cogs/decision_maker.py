import discord
from discord.ext import commands
from discord import app_commands
import random

class DecisionMaker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 使用 @app_commands.command 確保它是斜線指令
    @app_commands.command(name="choose", description="幫你從多個選項中隨機挑一個")
    @app_commands.describe(options="用空格分隔的選項，例如：蘋果 香蕉 橘子")
    async def decide(self, interaction: discord.Interaction, options: str):
        # 1. 將輸入字串以空格分割並去除多餘空格
        choices = [opt.strip() for opt in options.split() if opt.strip()]

        # 2. 檢查選項數量
        if len(choices) < 2:
            await interaction.response.send_message("❌ 請提供至少兩個選項，用空格分隔", ephemeral=True)
            return

        # 3. 隨機挑選一個
        selected = random.choice(choices)

        # 4. 把所有選項組合成字串（例如：蘋果, 香蕉, 橘子）
        all_options_str = "、".join(choices)

        # 5. 回傳完整訊息
        # 這裡會顯示：從「蘋果、香蕉、橘子」中，我選了：**蘋果**
        await interaction.response.send_message(
            f" 從「{all_options_str}」中...\n 選 **{selected}** 就對了！"
        )
        
# 這是在 main.py 呼叫 load_extension 時會執行的函式
async def setup(bot: commands.Bot):
    await bot.add_cog(DecisionMaker(bot))
