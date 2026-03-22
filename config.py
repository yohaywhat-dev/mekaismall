import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "1106103292922171474"))
ROLE_ID = int(os.getenv("ROLE_ID", "1420809167588823110"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1420805879111880774"))

# 反應身份組
REACTION_CHANNEL  = os.getenv("REACTION_CHANNEL",  "速寫公告")
REACTION_EMOJI    = os.getenv("REACTION_EMOJI",    "🔥")
REACTION_ROLE_NAME = os.getenv("REACTION_ROLE_NAME", "我要被情勒")

# 每日主題
TOPIC_CHANNEL = os.getenv("TOPIC_CHANNEL", "速寫交流")
