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
        """
        使用者輸入：/choose 選項1 選項2 選項3
        """
        # 將輸入字串以空格分割
        choices = [opt.strip() for opt in options.split() if opt.strip()]

        if len(choices) < 2:
            await interaction.response.send_message("❌ 請提供至少兩個選項，用空格分隔", ephemeral=True)
            return

        selected = random.choice(choices)
        await interaction.response.send_message(f"🎲 我選了：**{selected}**")

# 這是在 main.py 呼叫 load_extension 時會執行的函式
async def setup(bot: commands.Bot):
    await bot.add_cog(DecisionMaker(bot))
