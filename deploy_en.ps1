# Simple deployment script

# Configuration
$serverIP = "192.144.142.60"
$username = "root"
$password = "oeasy"
$remotePath = "/root/poetry_app/"

Write-Host "Starting deployment to server $serverIP..."

# Create start script content
$startScript = @"
#!/bin/bash

# Start script
cd /root/poetry_app/

# Install dependencies
pip install -r requirements.txt

# Start application
nohup python app.py > app.log 2>&1 &
echo "Application started, PID: $!"
"@

# Save start script
$startScript | Out-File -FilePath "start_server.sh" -Encoding ASCII

# Upload files
echo "Uploading application files..."
try {
    # Create directory on server first
    sshpass -p "$password" ssh "${username}@${serverIP}" "mkdir -p ${remotePath}"
    
    # Upload all files
    sshpass -p "$password" scp -r "./*" "${username}@${serverIP}:${remotePath}"
    
    Write-Host "Files uploaded successfully!"
    
    # Set execute permission
    Write-Host "Setting execute permission..."
    sshpass -p "$password" ssh "${username}@${serverIP}" "chmod +x ${remotePath}start_server.sh"
    
    Write-Host "Deployment completed!"
    Write-Host "To start the application, run:"
    Write-Host "sshpass -p $password ssh $username@$serverIP 'cd $remotePath && ./start_server.sh'"
} catch {
    Write-Host "Deployment failed. Check network connection or server details."
}
