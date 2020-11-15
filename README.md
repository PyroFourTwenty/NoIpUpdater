# Welcome to NoIpUpdater

 I got a few Raspberry Pi's running services i want to portforward to access them from outside my home network. 
 For this i use the free dynamic DNS service of [noip.com](https://www.noip.com).  This worked fine for me from the 
 beginning but as some time passed my router got assigned a new public IP from my ISP, which rendered the usage of my 
 DDNS useless. I frequently had to contact someone at home to tell me the freshly assigned IP so i could change it in 
 the WebUI of noip.com .  Of course this is a tiresome process, especially if the router gets a new IP every single day.
 At some point i found out about the Update API of noip.com and decided to write a little service to periodically tell 
 noip.com that my router's IP has been changed. 
 
 This is supposed to run on a Raspberry Pi, but other devices that are capable of running Python should be able to use it, too.    

# Files in this repo

## SimpleUpdater.py

This script uses an external API (api.ipify.org) to determine the public IP and compare it to the last locally saved IP 
(initially the IP is empty). If the public IP has been changed, an update will be sent to noip.com (only regarding your 
configured hostname).

## config.py

Possibly there are better ways to save a configuration file, but i wanted to keep it stupid simple.
***Keep this file a SECRET as it will contain your PASSWORD and USERNAME!!!!***

The config file contains the following fields:
|                |default                         | comment |
|----------------|---|-|
|update_interval_in_seconds|60 | Your hostname will be unreachable for this amout of seconds at most, so keep this number small, to not overflood your network with useless requests. Normally the hostname does not change this frequently|            |
|username|your@email.com            | Enter your noip.com-username here
|password|y0urPässw0r7| Enter your noip.com-password here
|hostname|example.ddns.net| This will be your noip.com-hostname, which will be updated
|update_url| http://{}:{}@dynupdate.no-ip.com/nic/update?hostname={}&myip={} | **Don't change this** unless the syntax of noip's Update API syntax changes and i am too lazy to update this repo |



## setup_systemd_service.py

This little script will setup a Systemd service (filename will be noipupdater.service) for you in the following form: 


> [Unit]  
Description=No-IP updater  
After=network.target    
[Service]  
User=pi  
WorkingDirectory= THIS WILL BE DETERMINED AUTOMATICALLY  
ExecStart=python3 src/SimpleUpdater.py  
Restart=always   
[Install]  
WantedBy=multi-user.targetBlockquote

To make sure that you have the rights to create and enable this service run this as sudo:

    sudo python3 setup_systemd_service.py

To check if the script worked correctly, enter the following command

    nano /etc/systemd/system/noipupdater.service
and check the content of noipupdater.service. 

After this you can reboot your pi using

    sudo reboot
After rebooting, check the service's status using

    sudo systemctl status noipupdater.service

# Used libraries

 - requests 
	 - install using `pip install requests`
 - pathlib
	 - install using `pip install pathlib`

# Used API's / services

 - [ipify.org](https://www.ipify.org) to get the public IP
 - [No-IP update api ](https://www.noip.com/integrate/request) to tell our DDNS our new public IP in case it changed

# Used tool for the creation of this readme

 - [stackedit.io](https://stackedit.io)
