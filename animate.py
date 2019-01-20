# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


    
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

def countdown(ctime):
    disp.clear()
    disp.display()
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    padding = 2
    x = padding
    shape_width = 30
    top = padding + 25
    bottom = height-padding
    # Load default font.
    font = ImageFont.load_default()

    for sec in range(ctime,0,-1):
        disp.clear()
        disp.display()
        #draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Write two lines of text.
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.text((x+22, top),   "Photo in...{}".format(sec),  font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(1)
        disp.clear()
        disp.display()

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((x+15, top),   "Composing Song...",  font=font, fill=255)
    disp.image(image)
    disp.display()





    
def run_display(print_text, emotion):
    # Clear display.
    disp.clear()
    disp.display()

    # Create image buffer.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (width, height))

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as this python script!
    # Some nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('basic_font.ttf', 12)

    # Create drawing object.
    draw = ImageDraw.Draw(image)

    # Define text and get total width.
    #text = 'Song Currently Playing: DESPACITO'
    text = emotion + print_text
    maxwidth, unused = draw.textsize(text, font=font)

    # Set animation and sine wave parameters.
    amplitude = height/4
    offset = height/2 - 4
    velocity = -3
    startpos = width

    # Animate text moving in sine wave.
    #print('Press Ctrl-C to quit.')
    pos = startpos
    #start_time = time.time()
    #elapsed_time = time.time() - start_time

    
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Enumerate characters and draw them offset vertically based on a sine wave.
        x = pos
        for i, c in enumerate(text):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            # Calculate offset from sine wave.
            y = offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
            # Draw text.
            draw.text((x, y), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        disp.image(image)
        disp.display()
        # Move position for next frame.
        pos += velocity
        # Start over if text has scrolled completely off left side of screen.
        if pos < -maxwidth:
            pos = startpos
        # Pause briefly before drawing next frame.
        time.sleep(0.1)
       

if __name__ == "__main__":
    countdown(10)
    
