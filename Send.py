import asyncio
import getpass
import json
import os
import sys
import aiofiles
from nio import AsyncClient, LoginResponse
import markdown

CONFIG_FILE = "credentials.json"

def write_details_to_disk(resp: LoginResponse, homeserver) -> None:
    """Writes the required login details to disk so we can log in later without
    using a password.

    Arguments:
        resp {LoginResponse} -- the successful client login response.
        homeserver -- URL of homeserver, e.g. "https://matrix.example.org"
    """
    # open the config file in write-mode
    with open(CONFIG_FILE, "w") as f:
        # write the login details to disk
        json.dump(
            {
                "homeserver": homeserver,  # e.g. "https://matrix.example.org"
                "user_id": resp.user_id,  # e.g. "@user:example.org"
                "device_id": resp.device_id,  # device ID, 10 uppercase letters
                "access_token": resp.access_token,  # cryptogr. access token
            },
            f,
        )

async def get_matrix_client() -> AsyncClient:
    """
    初始化并登录 Matrix 客户端。
    如果未找到凭据文件，则会提示用户输入信息。
    """
    if not os.path.exists(CONFIG_FILE):
        print(
            "首次使用。未找到凭据文件。需要输入 homeserver、用户和密码来创建凭据文件。"
        )
        homeserver = "https://matrix.example.org"
        homeserver = input(f"输入您的 homeserver URL: [{homeserver}] ")

        if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
            homeserver = "https://" + homeserver

        user_id = "@user:example.org"
        user_id = input(f"输入您的完整用户 ID: [{user_id}] ")

        device_name = "matrix-nio"
        device_name = input(f"为该设备选择一个名称: [{device_name}] ")

        client = AsyncClient(homeserver, user_id)
        pw = getpass.getpass()

        resp = await client.login(pw, device_name=device_name)

        if isinstance(resp, LoginResponse):
            write_details_to_disk(resp, homeserver)
            print(
                "已使用密码登录。凭据已存储。",
                "请再次运行脚本以使用凭据登录。",
            )
            return client
        else:
            print(f'homeserver = "{homeserver}"; user = "{user_id}"')
            print(f"登录失败: {resp}")
            sys.exit(1)
    else:
        async with aiofiles.open(CONFIG_FILE) as f:
            contents = await f.read()
        config = json.loads(contents)
        client = AsyncClient(config["homeserver"])
        
        client.access_token = config["access_token"]
        client.user_id = config["user_id"]
        client.device_id = config["device_id"]
        print("已使用存储的凭据登录。")
        return client

def convert_markdown_to_matrix_content(md_text: str) -> dict:
    """
    将 Markdown 文本转换为 Matrix 支持的消息格式。
    返回 content 字段的内容。
    """
    html = markdown.markdown(
        md_text,
        extensions=['mdx_truly_sane_lists']
    )
    
    return {
        "msgtype": "m.text",
        "body": md_text,
        "format": "org.matrix.custom.html",
        "formatted_body": html,
    }

async def send_matrix_message(client: AsyncClient, room_id: str, md_text: str) -> bool:
    try:
        content = convert_markdown_to_matrix_content(md_text)
        await client.room_send(room_id, message_type="m.room.message", content=content)
        print(f"消息已发送到 Matrix 房间 {room_id}。")
        return True
    except Exception as e:
        print(f"发送消息到 Matrix 失败: {e}")
        return False

if __name__ == "__main__":
    async def test_send():
        client = None
        try:
            client = await get_matrix_client()
            # 此处填写测试用房间id 感叹号开头
            room_id = "" 
            await send_matrix_message(client, room_id, "Hello from Send.py test!")
        finally:
            if client:
                await client.close()
    
    asyncio.run(test_send())
