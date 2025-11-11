#!/usr/bin/env python3
import os, requests, markdown, datetime
from pathlib import Path

APP_ID   = os.getenv('WECHAT_APP_ID')
APP_SEC  = os.getenv('WECHAT_APP_SECRET')
ARTICLE  = Path('test.md')

# ---------- 函数 ----------
def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SEC}"
    try:
        r = requests.get(url, timeout=10).json()
        
        # 检查是否返回了错误
        if 'errcode' in r:
            print(f"❌ 获取 Token 失败: 错误码 {r['errcode']}, 信息: {r['errmsg']}")
            print(f"   APP_ID: {APP_ID}")
            print(f"   请检查 APP_ID 和 APP_SECRET 是否正确")
            exit(1)
        
        if 'access_token' not in r:
            print(f"❌ 响应中未找到 access_token: {r}")
            exit(1)
            
        print(f"🔑 Token 获取成功 (有效期 2 小时)")
        return r['access_token']
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        exit(1)

def publish_draft(token, title, html, cover_id=""):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {
        "title": title,
        "content": html,
        "digest": title[:54],
        "thumb_media_id": cover_id,
        "show_cover_pic": 1 if cover_id else 0
    }
    try:
        r = requests.post(url, json=data, timeout=10).json()
        
        if 'errcode' in r:
            print(f"❌ 发布失败: 错误码 {r['errcode']}, 信息: {r['errmsg']}")
            # 常见错误码说明
            if r['errcode'] == 40001:
                print("   可能原因: APP_SECRET 错误或 access_token 过期")
            elif r['errcode'] == 40013:
                print("   可能原因: APP_ID 错误")
            elif r['errcode'] == 45009:
                print("   可能原因: 接口调用频率超限")
            exit(1)
        
        if 'media_id' in r:
            print(f"✅ 发布成功！草稿 media_id = {r['media_id']}")
        else:
            print(f"❌ 发布失败: 响应格式异常 {r}")
            exit(1)
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        exit(1)

# ---------- 主流程 ----------
if not APP_ID or not APP_SEC:
    print("❌ 请先设置微信 APP_ID 和 APP_SECRET 环境变量")
    exit(1)

if not ARTICLE.exists():
    print(f"❌ 找不到文章：{ARTICLE}")
    exit(1)

try:
    html = markdown.markdown(ARTICLE.read_text(encoding='utf-8'))
except Exception as e:
    print(f"❌ 读取或转换 Markdown 失败: {e}")
    exit(1)

title = f"自动日报 {datetime.date.today()}"

print(f"📝 准备发布: {title}")
token = get_token()
publish_draft(token, title, html)
