#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "Installing Message Clips Service..."

# 1. Create service user
echo "Creating service user: discord_bot_user..."
useradd -r -s /sbin/nologin -M discord_bot_user || echo "User already exists"

# 2. Create directories
echo "Creating application directories..."
mkdir -p /opt/message_clips/src
mkdir -p /opt/message_clips/venv

# 3. Create virtual environment and install dependencies
echo "Setting up virtual environment..."
python3 -m venv /opt/message_clips/venv
/opt/message_clips/venv/bin/pip install --upgrade pip
/opt/message_clips/venv/bin/pip install -r requirements.txt

# 4. Copy source files
echo "Copying source files..."
cp main.py /opt/message_clips/src/
chown -R discord_bot_user:discord_bot_user /opt/message_clips

# 5. Handle environment file and Discord Token
echo "Configuring environment variables..."
read -p "Enter your Discord Token: " DISCORD_TOKEN
echo "TOKEN=$DISCORD_TOKEN" > /etc/message_clips.env
chmod 600 /etc/message_clips.env
chown discord_bot_user:discord_bot_user /etc/message_clips.env

# 6. Install systemd service
echo "Installing systemd service..."
cp message_clips.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable message_clips.service

echo "Installation complete!"
echo "You can start the service with: systemctl start message_clips.service"
echo "Check logs with: journalctl -u message_clips.service -f"
