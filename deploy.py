import os
import paramiko
import sys
import time

def deploy_app():
    # 配置信息
    server_ip = "192.144.142.60"
    username = "admin"  # 尝试使用另一个常见的云服务器用户名
    password = "oeasy"
    remote_path = "/home/admin/poetry_app/"
    local_path = "."
    
    print(f"开始部署应用到服务器 {server_ip}...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接SSH
        print("连接到服务器...")
        ssh.connect(server_ip, username=username, password=password, timeout=20)
        
        # 创建远程目录
        print(f"创建远程目录: {remote_path}")
        stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {remote_path}")
        stdout.channel.recv_exit_status()  # 等待命令完成
        
        # 创建启动脚本
        start_script = '''#!/bin/bash

# 启动脚本
cd /home/admin/poetry_app/

# 安装依赖
pip install -r requirements.txt

# 启动应用
nohup python app.py > app.log 2>&1 &
echo "应用已启动，进程ID: $!"
'''
        
        # 写入启动脚本到服务器
        print("创建启动脚本...")
        with open("start_server.sh", "w") as f:
            f.write(start_script)
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 上传启动脚本
        sftp.put("start_server.sh", f"{remote_path}start_server.sh")
        
        # 上传应用文件
        print("开始上传应用文件...")
        
        # 定义要排除的文件和目录
        exclude = [".git", "__pycache__", "*.pyc", "*.log", "*.zip", "deploy.py", "deploy.ps1", "deploy_simple.ps1", "deploy_en.ps1", "start.sh", "deploy.sh", "start_server.sh"]
        
        # 遍历本地目录并上传文件
        uploaded_count = 0
        for root, dirs, files in os.walk(local_path):
            # 过滤目录
            dirs[:] = [d for d in dirs if d not in exclude and not any(d.endswith(ext) for ext in exclude if "*" in ext)]
            
            # 创建远程目录结构
            remote_root = root.replace(local_path, remote_path).replace("\\", "/")
            if remote_root != remote_path:
                ssh.exec_command(f"mkdir -p {remote_root}")
            
            # 上传文件
            for file in files:
                # 过滤文件
                if any(file.endswith(ext.replace("*", "")) for ext in exclude if "*" in ext) or file in exclude:
                    continue
                
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_root, file).replace("\\", "/")
                
                try:
                    sftp.put(local_file, remote_file)
                    uploaded_count += 1
                    if uploaded_count % 10 == 0:
                        print(f"已上传 {uploaded_count} 个文件...")
                except Exception as e:
                    print(f"上传文件失败 {local_file}: {e}")
        
        # 关闭SFTP
        sftp.close()
        
        # 设置启动脚本权限
        print("设置启动脚本权限...")
        ssh.exec_command(f"chmod +x {remote_path}start_server.sh")
        
        print(f"部署完成！共上传 {uploaded_count} 个文件。")
        print("接下来可以在服务器上启动应用。")
        
    except paramiko.AuthenticationException:
        print("认证失败，请检查用户名和密码。")
        return False
    except paramiko.SSHException as e:
        print(f"SSH连接错误: {e}")
        return False
    except Exception as e:
        print(f"部署过程中出错: {e}")
        return False
    finally:
        # 关闭SSH连接
        ssh.close()
    
    return True

if __name__ == "__main__":
    # 检查是否安装了paramiko
    try:
        import paramiko
    except ImportError:
        print("正在安装paramiko库...")
        os.system(f"{sys.executable} -m pip install paramiko")
        print("请重新运行脚本。")
        sys.exit(1)
    
    deploy_app()
