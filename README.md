# homekit-neopixel-rpi
homekit-neopixel-rpi 

[Demo Video](https://www.youtube.com/watch?v=IMnxmEtBPBE&feature=youtu.be)

<img src="image.jpg" width="100%">

## You need

Hardware:

  Raspberry Pi
  Neopixel strip

Software

  homebridge on Raspberry Pi
  python3
  nodejs


### Install 

```
sudo npm install -g pm2 homebridge homebridge-neopixel --unsafe-perm
```


### setting
```
# .homebridge/config
# add 
{     "accessory": "HTTP-NEO",
        "name": "Neo Lamp",

        "switch": {
        "status": "http://localhost:5000/status",
        "powerOn": "http://localhost:5000/on",
        "powerOff": "http://localhost:5000/off"
        },

        "color": {
        "status": "http://localhost:5000/color",
        "url": "http://localhost:5000/set/%s"
        },

        "brightness": {
        "status": "http://localhost:5000/bright",
        "url": "http://localhost:5000/set/%s"
        }
```

### Start the homebridge
```
pm2 start homebridge
```

### Start the server
```python
sudo FLASK_APP=server.py flask run
```



[homebridge neopixel](https://www.studiopieters.nl/homebridge-neopixel-light/)
[RPi neipixel](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring)
