import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randint

import math

listwl = ["Bienvenue", "Willkommen", "Bonjour", "Degemer Mat", "Welcome", "Tervetuloa", "Bienvenido", "Bem-vindo", "Welkom"]
listgb = ["A bientôt", "Bis bald", "Au revoir", "Kenavo", "Nähdään pian", "Adios", "Adeus", "See you soon", "Hasta la vista", "Tot ziens"]
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isn't used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load font with size equal to display height.
font_size = height
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

def welcome(name):
    draw.rectangle((0, 0, width, height), outline=255, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(0.6)

    # Draw the text.
    text = str(listwl[randint(0, len(listwl)-1)]+", "+ name+ " !")
    text_width, text_height = draw.textsize(text, font=font)
    x = 0
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)

    # Shift the text.
    for i in range(int(text_width/4)):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        x -= 4
        if x < -text_width:
            x = 0
        draw.text((x, y), text, font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.001)

def goodbye(name):
    draw.rectangle((0, 0, width, height), outline=255, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(0.6)

    # Draw the text.
    text = str(listgb[randint(0, len(listgb)-1)]+", "+ name+ " !")
    text_width, text_height = draw.textsize(text, font=font)
    x = 0
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)

    # Shift the text.
    for i in range(int(text_width/4)):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        x -= 4
        if x < -text_width:
            x = 0
        draw.text((x, y), text, font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.001)

def admin():
    draw.rectangle((0, 0, width, height), outline=255, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(0.6)

    # Draw the text.
    text = 'Openlab terminé !'
    text_width, text_height = draw.textsize(text, font=font)
    x = 0
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)

    # Shift the text.
    for i in range(int(text_width/4)):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        x -= 4
        if x < -text_width:
            x = 0
        draw.text((x, y), text, font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.001)

def idle(event):
    text = str('SCANNEZ-MOI !           '*10)
    maxwidth, unused = draw.textsize(text, font=font2)

    # Set animation and sine wave parameters.
    amplitude = height/4
    offset = height/2 - 4
    velocity = -8
    startpos = width

    # Animate text moving in sine wave.
    pos = startpos
    while not event.is_set():
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
                char_width, char_height = draw.textsize(c, font=font2)
                x += char_width
                continue
            # Calculate offset from sine wave.
            y = offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
            # Draw text.
            draw.text((x, y), c, font=font2, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font2)
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


def init():
    draw.rectangle((0, 0, width, height), outline=255, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(0.6)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Display image.
    disp.image(image)
    disp.display()

def error():
    text = 'X'
    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) / 2
    y = (height - text_height) // 2 -5
    draw.text((x, y), text, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(0.6)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Display image.
    disp.image(image)
    disp.display()