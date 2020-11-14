import os
from pathlib import Path
path = Path(os.getcwd()).parent
service_text = """[Unit]
Description=No-IP updater
After=network.target

[Service]
User=pi
WorkingDirectory={}
ExecStart=python3 src/SimpleUpdater.py
Restart=always

[Install]
WantedBy=multi-user.target""".format(path)

print('Removing existing service')
os.system('rm /etc/systemd/system/noipupdater.service')
print('Writing to service file')
os.system('echo "{}" >> /etc/systemd/system/noipupdater.service'.format(service_text))
print('Enabling service')
os.system('systemctl enable noipupdater.service')
print('done')
print('created and started service')

