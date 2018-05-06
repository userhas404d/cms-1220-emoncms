# cms-1220-emoncms
GET request rewriter for Brultech CMS 1220

## Overview

 As written the current firmware of the CMS-1220 (v4.20) does not send a properly formatted GET request to the EmonCMS instance. This project aims to correct that.

## PreReqs
A properly configured EmonCMS instance (tested with [emonpi](https://github.com/openenergymonitor/emonpi) via [emonsd](https://github.com/openenergymonitor/emonpi/wiki/emonSD-pre-built-SD-card-Download-&-Change-Log))

Add the necessary modules to your emoncms by following the Adding Brultech Devices to EmonCMS [guide](https://www.brultech.com/community/viewtopic.php?f=40&t=1577)


```
sudo cd /var/www/html/emoncms/Modules
sudo git clone https://github.com/brultech/device.git
sudo chown www-data:www-data -R /var/www/html/Modules
```

On the CMS-1220:

```
Configure GEM device with EmonCMS Packet Format (Format #10)
Under "Data Post" fill out the following:

- URL Address: RPi IP Address (eg. 192.168.2.222)
- URL Extension: /webhook/cms1220 << different from original
- Token: Read & Write Input API Token
- Note: If using the Device Module in the original Post, use the same Node Name you defined in Device Setup.
- The rest aren't used.
```

On the EmonCMS instance:
```

Create the GEM device:

1. Go to Setup -> Device Setup in EmonCMS.
2. Click New Device.
3. Click the Edit button (pencil icon).
4. Enter a Node Name (this will be defined in the GEM HTTP settings).
5. Choose GEM Direct.
6. Click the checkbox.
7. Click the folder icon, and then initialize, this will create your device and feeds.
8. Configure and start real-time data on the GEM.
```

## Post PreReqs

Configure emonpi for write operations

```
rpi-rw
```

Install [captainwebhook](https://github.com/skorokithakis/captainwebhook) (requires at python 2.7+)
```
pip install captainwebhook
```

Run captainwebhook and set it to auto-start

```
cptwebhook "echo {apikey} {node} {json}" -p 8282 -i 0.0.0.0 --template
```

Add the required apache2 modules to allow for the use of a reverse proxy

```
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_ajp
a2enmod rewrite
a2enmod deflate
a2enmod headers
a2enmod proxy_balancer
a2enmod proxy_connect
a2enmod proxy_html
```

Edit `/etc/apache2/sites-enabled/000-default.conf` to include a reverse proxy by adding these lines between the `VirtualHost` tags

```
ProxyPreserveHost On
ProxyPass /webhook/brultech http://0.0.0.0:8282/webhook/cms-1220/
ProxyPassReverse /webhook/brultech http://0.0.0.0:8282/webhook/cms-1220/
```

Restart apache

```
service apache2 restart
```
