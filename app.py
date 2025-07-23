import requests
from bs4 import BeautifulSoup
import json
import time
import os
import asyncio

# 从 Send.py 模块导入相关内容
from Send import get_matrix_client, send_matrix_message

MESSAGE_HISTORY_FILE = 'message_history.json'

def load_message_history():
    """
    从 JSON 文件加载历史消息。
    """
    if os.path.exists(MESSAGE_HISTORY_FILE):
        with open(MESSAGE_HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("错误：无法解析历史消息文件，将创建一个新的。")
                return []
    return []

def save_message_history(messages):
    """
    将消息保存到 JSON 文件。
    """
    with open(MESSAGE_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

async def send_to_matrix(client, room_id, message_content):
    """
    将消息发送到 Matrix。
    """
    print(f"--- 正在发送到 Matrix ---")
    print(message_content)
    print("------------------------")
    return await send_matrix_message(client, room_id, message_content)

def scrape_telegram_channel(url):
    """
    抓取 Telegram 频道页面上的消息内容。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"错误：抓取 URL {url} 失败：{e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    channel_history = soup.find('section', class_='tgme_channel_history')
    if not channel_history:
        print("未找到 class 为 'tgme_channel_history' 的元素。")
        return []

    messages = channel_history.find_all('div', class_='tgme_widget_message_wrap')
    
    scraped_messages = []
    for message_wrap in messages:
        message_bubble = message_wrap.find('div', class_='tgme_widget_message_bubble')
        if message_bubble:
            reactions = message_bubble.find('div', class_='tgme_widget_message_reactions')
            if reactions:
                reactions.decompose()

            footer = message_bubble.find('div', class_='tgme_widget_message_footer')
            if footer:
                footer.decompose()
 
            reply_content = ""
            reply_element = message_bubble.find('a', class_='tgme_widget_message_reply')
            if reply_element:
                reply_text = reply_element.get_text(separator="\n", strip=True)
                reply_content = "> " + reply_text.replace("\n", "\n> ") + "\n\n"
                reply_element.decompose()

            message_text_element = message_bubble.find('div', class_='tgme_widget_message_text')
            if message_text_element:
                processed_message_parts = []
                for content in message_text_element.children:
                    if content.name == 'a':
                        link_text = content.get_text(strip=True)
                        link_href = content.get('href', '')
                        processed_message_parts.append(f"[{link_text}]({link_href})")
                    elif content.name == 'br':
                        processed_message_parts.append("  \n")
                    elif content.name == 'pre':
                        code_content = content.get_text(separator="\n", strip=True)
                        lines = code_content.splitlines()
                        formatted_lines = [f'```{line}```' for line in lines]
                        result = '  \n'.join(formatted_lines)
                        processed_message_parts.append(result)
                    elif content.name in ['b', 'code', 'i', 'em', 'strong']:
                        processed_message_parts.append(content.get_text(strip=True))
                    elif content.string:
                        processed_message_parts.append(content.string.strip())
                
                message_content = "".join(processed_message_parts)
                
            else:
                message_content = message_bubble.get_text(separator="\n", strip=True)
            
            full_message_content = reply_content + message_content
            scraped_messages.append(full_message_content)
    
    return scraped_messages

async def load_config():
    """加载配置文件"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def main_loop():
    config = await load_config()
    target_url = config['target_url']
    check_interval_seconds = config['check_interval_seconds']
    matrix_room_id = config['matrix_room_id']

    client = None
    try:
        client = await get_matrix_client()
        print("开始监控 Telegram 频道。按 Ctrl+C 停止。")

        while True:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 尝试抓取：{target_url}")
            history_messages = load_message_history()
            current_scraped_messages = scrape_telegram_channel(target_url)
            
            if current_scraped_messages:
                new_messages = [msg for msg in current_scraped_messages if msg not in history_messages]
                
                if new_messages:
                    print(f"发现 {len(new_messages)} 条新消息。")
                    for msg in new_messages:
                        await send_to_matrix(client, matrix_room_id, msg)
                    
                    save_message_history(current_scraped_messages)
                    print("历史消息已更新。")
                else:
                    print("没有发现新消息。")
            else:
                print("未能抓取到任何消息。")
            
            print(f"等待 {check_interval_seconds} 秒后再次检查...")
            await asyncio.sleep(check_interval_seconds)
    finally:
        if client:
            await client.close()
            print("Matrix 客户端已关闭。")

if __name__ == "__main__":
    asyncio.run(main_loop())
