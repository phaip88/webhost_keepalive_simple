#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webhostmost 账号登录保活脚本 (轻量优化版)
使用 requests 库实现，无需 Playwright 和 Chromium
检测到倒计时元素即视为成功，优化 TG 通知内容
"""

import os
import requests
import re
import urllib.parse
from datetime import datetime, timedelta
import time

# -------------------------------
log_buffer = []
success_count = 0
fail_count = 0
account_results = []  # 存储每个账号的结果

def log(msg):
    print(msg)
    log_buffer.append(msg)
# -------------------------------

# Telegram 推送函数
def send_tg_log():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("⚠️ Telegram 未配置，跳过推送")
        return

    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    now_str = beijing_now.strftime("%Y-%m-%d %H:%M:%S") + " UTC+8"

    # 构建优化的通知内容
    status_emoji = "✅" if fail_count == 0 else "⚠️"
    summary = f"{status_emoji} 成功: {success_count} | 失败: {fail_count}"
    
    # 账号详情
    account_details = []
    for result in account_results:
        status = "✅" if result['success'] else "❌"
        account_details.append(f"{status} {result['username']}")
        if result.get('countdown'):
            account_details.append(f"   ⏱️ {result['countdown']}")
        if result.get('error'):
            account_details.append(f"   ⚠️ {result['error']}")
    
    final_msg = f"""📌 WebHostMost 保活报告
🕒 {now_str}

📊 执行结果
{summary}

👤 账号详情
{chr(10).join(account_details)}

💡 提示: 请确保每 45 天至少登录一次
"""

    # 分块发送（如果内容过长）
    for i in range(0, len(final_msg), 3900):
        chunk = final_msg[i:i+3900]
        try:
            resp = requests.get(
                f"https://api.telegram.org/bot{token}/sendMessage",
                params={"chat_id": chat_id, "text": chunk},
                timeout=10
            )
            if resp.status_code == 200:
                print(f"✅ Telegram 推送成功 [{i//3900 + 1}]")
            else:
                print(f"⚠️ Telegram 推送失败 [{i//3900 + 1}]: HTTP {resp.status_code}, 响应: {resp.text}")
        except Exception as e:
            print(f"⚠️ Telegram 推送异常 [{i//3900 + 1}]: {e}")

# 从环境变量解析多个账号
accounts_env = os.environ.get("SITE_ACCOUNTS", "")
accounts = []

for item in accounts_env.split(";"):
    if item.strip():
        try:
            username, password = item.split(",", 1)
            accounts.append({"username": username.strip(), "password": password.strip()})
        except ValueError:
            log(f"⚠️ 忽略格式错误的账号项: {item}")

URL_LOGIN = "https://client.webhostmost.com/login"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

def login_account(username, password, max_retries=2):
    global success_count, fail_count
    
    attempt = 0
    while attempt <= max_retries:
        attempt += 1
        log(f"🚀 开始登录账号: {username} (尝试 {attempt}/{max_retries + 1})")
        
        result = {
            'username': username,
            'success': False,
            'countdown': None,
            'error': None
        }
        
        try:
            # 创建会话
            client = requests.session()
            
            # 第一步：获取登录页面和 CSRF token
            response = client.get(URL_LOGIN, timeout=30)
            response.raise_for_status()
            
            # 提取 CSRF token（尝试多种模式）
            tokens = re.findall(r'name="token" value="(.*?)"', response.text)
            if not tokens:
                tokens = re.findall(r"csrfToken = '(.*?)'", response.text)
            if not tokens:
                tokens = re.findall(r'token: "(.*?)"', response.text)
            
            if not tokens:
                log(f"❌ 无法提取 CSRF token")
                result['error'] = "无法提取 CSRF token"
                raise RuntimeError("token-not-found")
            
            token = tokens[0]
            
            # 第二步：提交登录表单
            params = f'token={token}&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}'
            response2 = client.post(URL_LOGIN, data=params, headers=HEADERS, timeout=30)
            response2.raise_for_status()
            
            # 第三步：检查登录结果
            html = response2.text
            
            # 检查失败标识
            fail_keywords = ["Invalid credentials", "Invalid login", "Incorrect", "Login failed"]
            if any(keyword.lower() in html.lower() for keyword in fail_keywords):
                log(f"❌ 账号 {username} 登录失败（检测到错误提示）")
                result['error'] = "登录凭据无效"
                raise RuntimeError("login-failed")
            
            # 检查成功标识
            success_keywords = ["Client Area", "Dashboard", "My Services", "clientarea.php"]
            if any(keyword.lower() in html.lower() for keyword in success_keywords):
                log(f"✅ 账号 {username} 登录成功")
                
                # 检查倒计时元素（多语言支持）
                countdown_keywords = {
                    "Time until suspension": "英语",
                    "Tijd tot schorsing": "荷兰语", 
                    "Zeit bis zur Sperrung": "德语",
                    "停止までの時間": "日语",
                    "Tiempo hasta la suspensión": "西班牙语"
                }
                
                found_countdown = False
                detected_language = None
                
                for keyword, language in countdown_keywords.items():
                    if keyword.lower() in html.lower():
                        log(f"⏱️ 检测到倒计时元素 (语言: {keyword})")
                        result['countdown'] = f"倒计时元素已确认 ({language})"
                        detected_language = language
                        found_countdown = True
                        break
                
                # 如果没有通过关键词找到，检查 custom-timer 元素
                if not found_countdown:
                    if 'id="custom-timer"' in html or "id='custom-timer'" in html:
                        log("⏱️ 检测到倒计时元素 (通过 custom-timer ID)")
                        result['countdown'] = "倒计时元素已确认"
                        found_countdown = True
                
                # 只有检测到倒计时元素才算完全成功
                if found_countdown:
                    result['success'] = True
                    success_count += 1
                    account_results.append(result)
                    return True
                else:
                    log("⚠️ 登录成功，但未检测到倒计时元素")
                    result['error'] = "未检测到倒计时元素"
                    fail_count += 1
                    account_results.append(result)
                    return False
            else:
                log("⚠️ 未检测到成功或失败标识，可能页面结构变化")
                result['error'] = "页面结构异常"
                raise RuntimeError("login-unknown")
                
        except Exception as e:
            log(f"❌ 账号 {username} 尝试 ({attempt}) 异常: {e}")
            if attempt <= max_retries:
                wait_sec = 5 + attempt * 5
                log(f"⏳ {wait_sec}s 后重试...")
                time.sleep(wait_sec)
                continue
            else:
                log(f"❌ 账号 {username} 登录最终失败（{max_retries + 1} 次尝试）")
                if not result['error']:
                    result['error'] = str(e)
                fail_count += 1
                account_results.append(result)
                return False

def run():
    if not accounts:
        log("❌ 未配置 SITE_ACCOUNTS 环境变量，请按 'username,password;...' 格式配置")
        return
    
    for acc in accounts:
        login_account(acc["username"], acc["password"])
        time.sleep(2)

if __name__ == "__main__":
    run()
    send_tg_log()
