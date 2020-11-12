import os
import subprocess
import re

dhcpcd_path = "/etc/dhcpcd.conf"
ip_config_check = "#CONFIGURED DONT RECONFIGURE"
ip_config = ("\r\n\r\n#CONFIGURED DONT RECONFIGURE\r\ninterface wlan0\r\nstatic ip_address=" +
             "192.168.4.1/24\r\nstatic routers=192.168.1.1\r\nstatic domain_name_servers=192.168.1.1\r" +
             "\nnohook wpa_supplicant\r\n")

dns_path = "/etc/dnsmasq.conf"
dns_config = "interface=wlan0\r\ndhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h"

daemon_config = "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""
hostapd_location = "/etc/default/hostapd"
daemon_conf = "/etc/hostapd/hostapd.conf"

host_config = ("interface=wlan0\ndriver=nl80211\nssid=Setup\nhw_mode=g\nchannel=7" +
                "\nwmm_enabled=0\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0" +
                "\nwpa=2\nwpa_passphrase=ANSULRED\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP" +
                "\nrsn_pairwise=CCMP\n")

startup = "iptables-restore < /etc/iptables.ipv4.nat\r\nsudo /home/pi/startup.sh\r\nexit 0"

#os.system("sudo python ./depend.py")
#os.system("sudo python3 ./mount.py")

#configure DHCPCD-------------------------       
with open(dhcpcd_path, 'a+') as file:
    file.seek(0,0)
    if(ip_config_check in file.read()):
        print("DHCPCD already configured")
    
    else:
        print("Just configured DHCPCD")
        file.write(ip_config)

os.system("sudo systemctl restart dhcpcd")

#Configure DNSMASQ -----------------------------
with open(dns_path, 'w+') as file :
    file.write(dns_config)
    
os.system("sudo systemctl reload dnsmasq")

#configure daemon ------------------------------
with open(hostapd_location, 'w+') as file:
    file.write(daemon_config);

with open(daemon_conf, 'w+') as file:
    file.write(host_config)
    
os.system("sudo systemctl unmask hostapd")
os.system("sudo systemctl enable hostapd")
os.system("sudo systemctl start hostapd")

with open("/etc/sysctl.conf", 'r') as file :
    file_data = file.read();
    
file_data = file_data.replace("#net.ipv4.ip_forward=1", "net.ipv4.ip_forward=1")

with open("/etc/sysctl.conf", 'w') as file :
    file.write(file_data);
    
os.system("sudo sh -c \"echo 1 > /proc/sys/net/ipv4/ip_forward\"")  
os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
os.system("sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
os.system("sudo sh -c \"iptables-save > /etc/iptables.ipv4.nat\"")

with open("/etc/rc.local", 'r') as file :
    file_data = file.read();

file_data = file_data.replace("exit 0", startup)

with open("/etc/rc.local", 'w') as file :
    file.write(file_data);

with open('/home/pi/7365747570.txt', 'w+') as file:
        file.write('done')

with open("/boot/config.txt", 'r') as file :
    file_data = file.read();
    
file_data = file_data.replace("start_x=0", "start_x=1")
file_data = file_data.replace("#dtparam=i2c_arm=on", "dtparam=i2c_arm=on") 

with open("/boot/config.txt", 'w') as file :
    file.write(file_data);