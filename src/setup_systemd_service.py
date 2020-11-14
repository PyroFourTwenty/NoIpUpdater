import os

path = os.getcwd()
service_text = """[Unit]
Description=No-IP updater
After=network.target

[Service]
User=pi
WorkingDirectory={}
ExecStart=python SimpleUpdater.py
Restart=always

[Install]
WantedBy=multi-user.target""".format(path)

os.system('rm /etc/systemd/system/noipupdater.service')
os.system('echo "{}" >> /etc/systemd/system/noipupdater.service'.format(service_text))
os.system('systemctl enable noipupdater.service')
os.system('systemctl start noipupdater.service')

print('created and started service')

