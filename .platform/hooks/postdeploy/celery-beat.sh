#!/usr/bin/env bash

# Create the celery systemd service file
echo "[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
EnvironmentFile=/opt/elasticbeanstalk/deployment/env
WorkingDirectory=/var/app/current
ExecStart=$PYTHONPATH/celery -A djangoawsrest beat --logfile=/var/log/celery/beat.log --pidfile=/var/run/celery/beat.pid --loglevel=INFO

[Install]
WantedBy=multi-user.target
" | tee /etc/systemd/system/celery-beat.service

# Start celery service
systemctl restart celery-beat.service

# Enable celery service to load on system start
systemctl enable celery-beat.service