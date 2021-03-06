#!/usr/bin/env bash

# Create the celery systemd service file
echo "[Unit]
Name=Celery
Description=Celery service for My App
After=network.target
StartLimitInterval=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
WorkingDirectory=/var/app/current
ExecStart=$PYTHONPATH/celery -A djangoawsrest worker --logfile=/var/log/celery/worker.log --pidfile=/var/run/celery/%n.pid --loglevel=INFO -n worker.%%h
EnvironmentFile=/opt/elasticbeanstalk/deployment/env

[Install]
WantedBy=multi-user.target
" | tee /etc/systemd/system/celery.service

# Start celery service
systemctl restart celery.service

# Enable celery service to load on system start
systemctl enable celery.service