import time
import board
import neopixel
import threading

from flask import Flask

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)
app = Flask(__name__)

rgb=(255,255,255)
status = 0
enableRainbow = False

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rainbow_cycle():
  wait = 0.000001
  for j in range(255):
    for i in range(num_pixels):
      pixel_index = (i * 256 // num_pixels) + j
      pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(wait)
  global enableRainbow
  if(enableRainbow):
    rainbow_cycle()
  else:
    off()


@app.route("/status")
def status():
  global status
  return str(status)


@app.route("/bright")
def bright():
  global rgb
  r = round(rgb[0]/2.55,2)
  g = round(rgb[1]/2.55,2)
  b = round(rgb[2]/2.55,2)
  x = max(r,g)
  V = max(x,b)
  return str(V)

@app.route("/color")
def color():
  global rgb
  value = rgb_to_hex(rgb)
  return str(value)


@app.route("/rainbow")
def rainbow():
  global enableRainbow
  global status
  status = 1
  global rgb
  pixels.fill(rgb)
  pixels.show()
  if(enableRainbow==False):
    t = threading.Thread(target = rainbow_cycle)
    t.start()
  enableRainbow=True
  return "on"



@app.route("/on")
def on():
  global status
  status = 1
  global rgb
  pixels.fill(rgb)
  pixels.show()
  return "on"

@app.route("/off")
def off():
  global status
  status = 0
  global enableRainbow
  enableRainbow=False
  pixels.fill((0,0,0))
  pixels.show()
  return "off"

@app.route("/set/<values>")
def set(values):
  global enableRainbow
  enableRainbow=False
  h = values
  #h = values.replace("NA","0").replace("N","1")
  global rgb
  #rgb=hex_to_rgb(h)
  rgb=tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
  pixels.fill(rgb)
  pixels.show()
  return "ok"
