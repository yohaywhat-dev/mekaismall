import datetime  # 👈 必須加這行
import random    # 👈 必須加這行

TOPIC_THEMES = [
    "人體", "色彩", "表情", "質感", "二分光影", "手"
]

def get_today_topic():
    """基於日期生成今日主題"""
    # 這裡要改成 datetime.datetime.utcnow() 配合 import datetime
    today = datetime.datetime.utcnow().date()
    
    # 使用日期作為種子，確保同一天得到相同的主題
    random.seed(today.toordinal())
    return random.choice(TOPIC_THEMES) 
