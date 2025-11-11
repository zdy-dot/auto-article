#!/usr/bin/env python3
import os
import requests
import markdown
import datetime
from pathlib import Path

APP_ID   = os.getenv('WECHAT_APP_ID')
APP_SEC  = os.getenv('WECHAT_APP_SECRET')
ARTICLE  = Path('test.md')

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SEC}"
    r = requests.get(url, timeout=10).json()
    return r['access_token']

def publish_draft(token, title, html, cover_id=""):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {
        "title": title,
        "content": html,
        "digest": title[:54],
        "thumb_media_id": cover_id,
        "show_cover_pic": 1 if cover_id else 0
    }
    r = requests.post(url, json=data, timeout=10).json()
    if 'media_id' in r:
        print(f"✅ 发布成功！草稿 media_id = {r['media_id']}")
    else:
        print(f"❌ 发布失败: {r}")
        exit(1)

if not APP_ID or not APP_SEC:
    print("请先设置微信 APP_ID 和 APP_SECRET")
    exit(1)

if not ARTICLE.exists():
    print(f"找不到文章：{ARTICLE}")
    exit(1)

html = markdown.markdown(ARTICLE.read_text(encoding='utf-8'))
title = f"自动日报 {datetime.date.today()}"

token = get_token()
publish_draft(token, title, html)
