# Telegram-Matrix Bridge

## 📌 Super Simple Telegram to Matrix Message Forwarder

[🇨🇳 中文版](README.md) | [🇺🇸 English](README-en.md)

This is an **extremely simple** message forwarder from Telegram channels — **no Telegram account or API key required**, and **no Matrix server permissions needed**. It works with just the public web link of a channel!

✅ **Zero Telegram Authentication Required** – No need for a Telegram Bot Token  
✅ **Quick Setup** – Get it running in just a few steps  
✅ **Auto Forwarding** – Real-time monitoring and forwarding to Matrix  

## 🚀 Quick Start

### 1. Clone the Project
```bash
git clone https://github.com/lost0427/tele2matrix.git    
cd tele2matrix
```

### 2. Install Dependencies

#### Option 1: Using Conda (Recommended for Windows users)
Simply run the `install-tele2matrix.bat` file, which will automatically create a Python 3.11 environment and install all dependencies.

#### Option 2: Using pip
```bash
pip install -r requirements.txt
```

### 3. Configure Settings

Copy and modify the configuration template `config.json`:
```json
{
    "target_url": "https://t.me/s/your_channel_name",
    "check_interval_seconds": 300,
    "matrix_room_id": "!your_room_id:example.com"
}
```

**Configuration Explanation:**
- `target_url`: The public Telegram channel web page URL (note the format: `t.me/s/channelname`)
- `check_interval_seconds`: Interval between checks (in seconds), recommended at least 60 seconds
- `matrix_room_id`: The target Matrix room ID

### 4. Configure Matrix Credentials

On first run, the program will automatically prompt you to enter your Matrix server information and login credentials. Just run:
```bash
python Send.py
```
Follow the prompts to complete the setup.

### 5. Run the Program

#### For Windows Users:
Double-click the `start-tele2matrix.bat` file to start the program.

Or manually run:
```bash
call conda activate tele2matrix
python main.py
pause
```

#### For Other Systems:
```bash
python main.py
```

## 🛠️ How It Works

1. Periodically visits the public webpage of the Telegram channel  
2. Parses the page content to extract new messages  
3. Compares with history to avoid duplicate forwarding  
4. Sends messages to the specified Matrix room via a Matrix client  

## 📦 Dependencies

- Python 3.8+ (Recommended: 3.11)
- matrix-nio
- aiofiles
- markdown
- requests
- beautifulsoup4
- mdx_truly_sane_lists

## ⚠️ Limitations

⚠️ **Public Channels Only** – The channel must be accessible via a web browser (e.g., `https://t.me/s/channelname`)  
⚠️ **Relies on Web Page Structure** – May require code adjustments if Telegram changes its layout  

## 📝 Notes

- Make sure the target Telegram channel is public and accessible via the web  
- Set a reasonable check interval to avoid excessive requests  
- On first run, all messages currently visible on the page will be sent — make sure this behavior is intended  

## 🤝 Contributing

Feel free to submit Issues or Pull Requests to help improve this project!

## 📄 License

MIT License