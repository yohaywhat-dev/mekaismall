#每日主題選項
TOPIC_THEMES = [
    "人體", "色彩", "表情", "質感", "二分光影", "手"
]

def get_today_topic():
    """基於日期生成今日主題"""
    today = datetime.utcnow().date()
    # 使用日期作為種子，確保同一天得到相同的主題
    random.seed(today.toordinal())
    return random.choice(TOPIC_THEMES)
