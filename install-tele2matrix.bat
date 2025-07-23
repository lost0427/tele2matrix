@echo off
:: 创建 conda 环境，Python 3.11，环境名为 tele2matrix
echo 正在创建 conda 环境 tele2matrix...
call conda create -n tele2matrix python=3.11 -y

:: 激活 conda 环境
echo 正在激活环境 tele2matrix...
call conda activate tele2matrix

:: 安装 requirements.txt 中的依赖（使用 pip）
echo 正在安装 requirements.txt 中的依赖...
pip install -r requirements.txt

echo 环境 tele2matrix 已创建并安装好依赖。
pause