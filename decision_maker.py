#decision_maker.py
import random
from discord import app_commands

def setup(bot):
    @bot.tree.command(name="choose", description="幫你從多個選項中隨機挑一個")  # 改名
    @app_commands.describe(options="用空格分隔的選項，例如：蘋果 香蕉 橘子")
    async def decide(interaction: 'discord.Interaction', *, options: str):
        """
        /choose 選項1 選項2 選項3
        """
        # 將輸入字串以空格分割
        choices = [opt.strip() for opt in options.split() if opt.strip()]

        if len(choices) < 2:
            await interaction.response.send_message("❌ 請提供至少兩個選項，用空格分隔")
            return

        selected = random.choice(choices)
        await interaction.response.send_message(f"🎲 我選了：{selected}")
