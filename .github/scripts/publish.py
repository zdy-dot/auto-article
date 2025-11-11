#!/usr/bin/env python3   #!使用 Python3 环境：/usr/bin/env python3
import os, requests, markdown, datetime导入 os,requests,markdown 和 datetime 模块
from pathlib    从 pathlib 导入 Pathimport Path

APP_ID   = os.APP_ID = os.getenv('WECHAT_APP_ID')  # 获取环境变量 WECHAT_APP_ID 的值并赋给 APP_ID 变量getenv('WECHAT_APP_ID')
APP_SEC  = os.APP_SEC = os.getenv('WECHAT_APP_SECRET')  # APP_SEC 等于从环境变量中获取的 WECHAT_APP_SECRET 的值getenv('WECHAT_APP_SECRET')
ARTICLE  = ARTICLE = Path('test.md')  # Default to this one, can be changed laterPath('test.md')          # 默认发这篇，后面可改

# ---------- 函数 ----------
def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SEC}"
    r = requests.r = requests.get(url, timeout=10).json()  # r 等于使用 requests 库发送 GET 请求获取 url 对应的 JSON 格式get(url, timeout=10).json()
       返回 r 中的“access_token”值return r['access_token']

def def publish_draft(token, title, html, cover_id=""):  # 定义发布草稿的函数
    pass  # 函数体为空，此处仅作publish_draft(token, title, html, cover_id=""):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data =    数据= {{
           “标题”:标题、"title": title,
           “内容”:html、"content": html,
           摘要：标题的前 54 个字符"digest": title[:54],
        "封面图片的媒体 ID"： 封面图片的 ID"thumb_media_id": cover_id,
        "show_cover_pic": 1 if cover_id else 0
    }
    r = requests.post(url, json=data, timeout=10).json()r = requests.post(url, json=data, timeout=10).json()  # 发送一个 POST 请求，将 data 作为 JSON 数据发送到 url，设置超时时间为 10 
    if 'media_id' in r:
        print(f"✅ 发布成功！草稿 media_id = {r['media_id']}")
    else:   其他:
        print(f"❌ 发布失败: {r}")
        exit(1)   退出(1)

# ---------- 主流程 ----------
if not APP_ID or not APP_SEC:
    print("请先设置微信 APP_ID 和 APP_SECRET")
    exit(1)   退出(1)

if not ARTICLE.exists():
    print(f"找不到文章：{ARTICLE}")
    exit(1)   退出(1)

html = markdown.markdown(ARTICLE.read_text(encoding='utf-8'))
title = f"自动日报 {datetime.date.today()}"

token = get_token()   Token = get_token（）
publish_draft(token, title, html)
