#!/bin/bash

# 进入项目目录
cd {remote_path}

# 设置环境变量，确保Flask应用能正确处理反向代理请求
export FLASK_ENV=production
export FLASK_APP=app.py
# 设置信任代理头，使Flask能正确识别客户端IP和协议
export PROXY_FIX=true

# 安装依赖
pip install -r requirements.txt

# 确保uploads目录存在并设置权限
mkdir -p uploads
chmod 755 uploads

# 启动应用
nohup python app.py > app.log 2>&1 &
echo "应用已启动，进程ID: $!"
echo "应用可通过 http://192.144.142.60/o202301073006/newweb/ 访问"