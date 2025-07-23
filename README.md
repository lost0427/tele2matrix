# Telegram-Matrix-Bridge

## 📌 超简单 Telegram 到 Matrix 消息转发工具

[🇨🇳 中文版](README.md) | [🇺🇸 English](README-en.md)

这是一个**极其简单**的 Telegram 频道消息转发器，**无需 Telegram 账号/key，无需 matrix 服务器权限**，只需频道的公开网页链接即可工作！

✅ **零配置 Telegram 认证** - 不需要 Telegram Bot Token  
✅ **快速部署** - 简单几步即可运行  
✅ **自动转发** - 实时监控频道更新并转发到 Matrix  

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/lost0427/tele2matrix.git  
cd tele2matrix
```

### 2. 安装依赖

#### 方法一：使用 Conda (推荐 Windows 用户)
直接运行 `install-tele2matrix.bat` 文件，它会自动创建 Python 3.11 环境并安装所有依赖。

#### 方法二：使用 pip
```bash
pip install -r requirements.txt
```

### 3. 配置文件设置

复制配置模板并修改： `config.json`：
```json
{
    "target_url": "https://t.me/s/your_channel_name  ",
    "check_interval_seconds": 300,
    "matrix_room_id": "!your_room_id:example.com"
}
```

**配置说明：**
- `target_url`: Telegram 公开频道的网页链接（注意是 `t.me/s/` 格式）
- `check_interval_seconds`: 检查间隔时间（秒），建议不少于 60 秒
- `matrix_room_id`: 目标 Matrix 房间的 ID

### 4. 配置 Matrix 凭据

首次运行时，程序会自动提示你输入 Matrix 服务器信息和登录凭据。只需运行：
```bash
python Send.py
```
按照提示输入相关信息即可完成配置。

### 5. 运行程序

#### Windows 用户：
直接运行 `start-tele2matrix.bat` 文件启动程序。

或者手动执行：
```bash
call conda activate tele2matrix
python main.py
pause
```

#### 其他系统：
```bash
python main.py
```

## 🛠️ 工作原理

1. 定期访问 Telegram 频道的公开网页
2. 解析页面内容提取最新消息
3. 比较历史记录避免重复转发
4. 通过 Matrix 客户端发送到指定房间

## 📦 依赖

- Python 3.8+ (推荐 3.11)
- matrix-nio
- aiofiles
- markdown
- requests
- beautifulsoup4
- mdx_truly_sane_lists

## ⚠️ 局限性

⚠️ **仅支持公开频道** - 频道必须可以通过网页浏览器直接访问（如 `https://t.me/s/channelname`）  
⚠️ **依赖网页结构** - 如果 Telegram 改变网页布局可能需要调整代码  

## 📝 注意事项

- 确保目标 Telegram 频道是公开的且可通过网页访问
- 建议设置合理的检查间隔，避免过于频繁的请求
- 第一次运行时会发送所有当前页面的消息，请确保这是你想要的行为

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License