# 简化版部署脚本

# 配置信息
$serverIP = "192.144.142.60"
$username = "root"
$password = "oeasy"
$remotePath = "/root/poetry_app/"

Write-Host "开始部署应用到云服务器 $serverIP..."

# 创建启动脚本内容
$startScript = @"
#!/bin/bash

# 启动脚本
cd /root/poetry_app/

# 安装依赖
pip install -r requirements.txt

# 启动应用
nohup python app.py > app.log 2>&1 &
echo "应用已启动，进程ID: $!"
"@

# 保存启动脚本
$startScript | Out-File -FilePath "start_server.sh" -Encoding ASCII

# 上传文件的命令
echo "正在上传应用文件..."
# 使用简化的方式，不使用复杂的排除参数
& "sshpass" -p "$password" "scp" -r "./*" "${username}@${serverIP}:${remotePath}"

if ($LASTEXITCODE -eq 0) {
    Write-Host "文件上传成功！"
    
    # 设置启动脚本权限
    Write-Host "正在设置启动脚本权限..."
    & "sshpass" -p "$password" "ssh" "${username}@${serverIP}" "chmod +x ${remotePath}start_server.sh"
    
    Write-Host "部署完成！"
    Write-Host "可以通过以下命令在服务器上启动应用："
    Write-Host "sshpass -p $password ssh $username@$serverIP 'cd $remotePath && ./start_server.sh'"
} else {
    Write-Host "文件上传失败，请检查网络连接或服务器信息。"
}
