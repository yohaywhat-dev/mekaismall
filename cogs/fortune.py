import discord
from discord.ext import commands
from discord import app_commands
import random

class Fortune(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="draw", description="抽一張今日運勢籤")
    async def draw(self, interaction: discord.Interaction):
        # 1. 定義選項
        fortunes = ["超級好", "好像還不錯喔", "還好", "有點不太好", "別想了"]
        
        # 2. 隨機挑選
        result = random.choice(fortunes)

        # 3. 設定對應的圖示（記得可以換成你的 <:name:ID> 自定義表符）
        color_map = {
            "超級好": "✨", 
            "好像還不錯喔": "✅",
            "還好": "🟡",
            "有點不太好": "❓",
            "別想了": "❌"
        }
        
        icon = color_map.get(result, "📜")

        # 4. 回傳訊息
        # 使用 # 讓整行變超大，並去掉「抽到了：」
        await interaction.response.send_message(
            f"# {icon} **{result}**"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Fortune(bot))
