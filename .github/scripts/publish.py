#!/usr/bin/env python3   #!使用 Python3 环境：/usr/bin/env python3
import os, requests, markdown, datetime导入 os、requests、markdown 和 datetime 模块
from pathlib import Path   从 pathlib 导入 Path

APP_ID   = os.getenv('WECHAT_APP_ID')APP_ID = os.getenv('WECHAT_APP_ID'   “WECHAT_APP_ID”)  # 获取环境变量 WECHAT_APP_ID 的值并赋给 APP_ID 变量Get the value of the environment variable WECHAT_APP_ID and assign it to the APP_ID variable.
APP_SEC  = os.getenv('WECHAT_APP_SECRET')APP_SEC = os.getenv('WECHAT_APP_SECRET'   “WECHAT_APP_SECRET”)  # APP_SEC 等于从环境变量中获取的 WECHAT_APP_SECRET 的值# APP_SEC is equal to the value of WECHAT_APP_SECRET obtained from the environment variable.
ARTICLE  = Path('test.md')文章 = Path   路径('test.md

# ---------- 函数 ----------
def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SEC}"
    try:   试一试:   试一试:
        r = requests.get(url, timeout=10).json()r = requests.get(url, timeout=10).json()  # r 等于使用 requests 库发送 GET 请求获取 url 对应的 JSON 格式
        
        # 检查是否返回了错误
        if 'errcode' in r:   如果‘errcode’在r中：
            print(f"❌ 获取 Token 失败: 错误码 {r['errcode']}, 信息: {r['errmsg']}")
            print(f"   APP_ID: {APP_ID}")
            print(f"   请检查 APP_ID 和 APP_SECRET 是否正确")
            exit(1)   退出(1)
        
        if 'access_token' not in r:   如果 r 中不存在 'access_token' ：
            print(f"❌ 响应中未找到 access_token: {r}")
            exit(1)   退出(1)
            
        print(f"🔑 Token 获取成功 (有效期 2 小时)")
        return r['access_token']
        
    except Exception as e:   例外情况如下：   例外情况如下：
        print(f"❌ 请求失败: {e}")
        exit(1)   退出(1)

def publish_draft(token, title, html, cover_id=""):def publish_draft(token, title, html, cover_id=""):  # 定义发布草稿的函数
    pass  # 函数体为空，此处仅作
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {   数据= {
        "title": title,   “标题”:标题、
        "content": html,   “内容”:html、
        "digest": title[:54],   摘要：标题的前 54 个字符
        "thumb_media_id": cover_id,"封面图片的媒体 ID"： 封面图片的 ID
        "show_cover_pic": 1 if cover_id else 0
    }
    try:   试一试:   试一试:
        r = requests.post(url, json=data, timeout=10).json()r = requests.post(url, json=data, timeout=10).json()  # 发送一个 POST 请求，将 data 作为 JSON 数据发送到 url，设置超时时间为 10 
        
        if 'errcode' in r:   如果‘errcode’在r中：
            print(f"❌ 发布失败: 错误码 {r['errcode']}, 信息: {r['errmsg']}")
            # 常见错误码说明
            if r['errcode'] == 40001:
                print("   可能原因: APP_SECRET 错误或 access_token 过期")
            elif r['errcode'] == 40013:
                print("   可能原因: APP_ID 错误")
            elif r['errcode'] == 45009:
                print("   可能原因: 接口调用频率超限")
            exit(1)   退出(1)
        
        if 'media_id' in r:   如果‘media_id’在r中：
            print(f"✅ 发布成功！草稿 media_id = {r['media_id']}")
        else:   其他:   其他:
            print(f"❌ 发布失败: 响应格式异常 {r}")
            exit(1)   退出(1)
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        exit(1)   退出(1)

# ---------- 主流程 ----------
if not APP_ID or not APP_SEC:   如果 APP_ID 或 APP_SEC 不存在：
    print("❌ 请先设置微信 APP_ID 和 APP_SECRET 环境变量")
    exit(1)   退出(1)

if not ARTICLE.exists():   如果不存在文章：
    print(f"❌ 找不到文章：{ARTICLE}")
    exit(1)   退出(1)

try:   试一试:
    html = markdown.markdown(ARTICLE.read_text(encoding='utf-8'))
except Exception as e:   例外情况如下：
    print(f"❌ 读取或转换 Markdown 失败: {e}")
    exit(1)   退出(1)

title = f"自动日报 {datetime.date.today()}"

print(f"📝 准备发布: {title}")
token = get_token()   Token = get_token（）
publish_draft(token, title, html)
