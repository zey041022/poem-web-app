# 部署脚本 - 将应用上传到云服务器

# 配置信息
$serverIP = "192.144.142.60"
$username = "root"  # 假设使用root用户登录，可根据实际情况修改
$password = "oeasy"
$localPath = ".\"  # 当前目录
$remotePath = "/root/poetry_app/"  # 云服务器上的目标路径

Write-Host "开始部署应用到云服务器 $serverIP..."

# 创建目标目录（如果不存在）
try {
    Write-Host "正在连接服务器并创建目标目录..."
    $createDirCommand = "sshpass -p '$password' ssh $username@$serverIP 'mkdir -p $remotePath'"
    Invoke-Expression $createDirCommand
    Write-Host "目标目录创建成功！"
} catch {
    Write-Host "创建目标目录失败: $_"
    exit 1
}

# 上传应用文件
try {
    Write-Host "正在上传应用文件..."
    # 排除不需要上传的文件和目录
    $excludeFiles = @(".git", "__pycache__", "*.pyc", "*.log", "*.zip", "deploy.ps1", "start.sh", "deploy.sh")
    
    # 使用scp上传所有文件（排除指定的文件和目录）
    $excludeArgs = $excludeFiles -join " --exclude='"  
    $excludeArgs = "--exclude='" + $excludeArgs + "'"
    
    $uploadCommand = "sshpass -p '$password' scp -r $excludeArgs $localPath* $username@$serverIP:$remotePath"
    Invoke-Expression $uploadCommand
    
    Write-Host "应用文件上传成功！"
} catch {
    Write-Host "上传文件失败: $_"
    exit 1
}

# 上传启动脚本
try {
    Write-Host "正在创建并上传启动脚本..."
    $startScriptContent = @"
#!/bin/bash

# 启动脚本 - 在云服务器上运行应用

cd /root/poetry_app/

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=production

# 启动应用
nohup python app.py > app.log 2>&1 &
echo "应用已启动，进程ID: $!"
echo "应用日志文件: app.log"
"@
    
    # 保存启动脚本到本地
    $startScriptContent | Out-File -FilePath "start_server.sh" -Encoding ASCII
    
    # 上传启动脚本
    $uploadStartScript = "sshpass -p '$password' scp start_server.sh $username@$serverIP:$remotePath"
    Invoke-Expression $uploadStartScript
    
    # 设置脚本权限
    $setPermission = "sshpass -p '$password' ssh $username@$serverIP \"chmod +x $remotePath/start_server.sh\""
    Invoke-Expression $setPermission
    
    Write-Host "启动脚本上传并设置权限成功！"
} catch {
    Write-Host "创建或上传启动脚本失败: $_"
    exit 1
}

Write-Host "部署完成！应用已上传到云服务器。"
Write-Host "接下来可以连接到服务器并运行: cd $remotePath && ./start_server.sh"
