#!/home/admin/tft-display/v_env/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import json
import requests
import subprocess
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

# Fonts
font_path   = '/usr/share/fonts/truetype/dejavu/'
clock_font  = ImageFont.truetype(font_path + "DejaVuSans.ttf", 55)
large_font  = ImageFont.truetype(font_path + "DejaVuSans.ttf", 55)
medium_font = ImageFont.truetype(font_path + "DejaVuSans.ttf", 38)
small_font  = ImageFont.truetype(font_path + "DejaVuSans.ttf", 25)
tiny_font   = ImageFont.truetype(font_path + "DejaVuSans.ttf", 15)

# HTTP info
baseurl = "http://"
server  = "192.168.11.96:81"
mdata  = "/api/track/metadata"
status  = "/api/player/status"
volume  = "/api/volume"

url_mdata  = baseurl + server + mdata
url_status = baseurl + server + status
url_volume = baseurl + server + volume

# logging.basicConfig(level=logging.DEBUG)

# disp prototype. Don't create multiple disp objects!
# disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
disp = LCD_2inch4.LCD_2inch4()
# Init display. Clear if needed: disp.clear()
disp.Init()

def server_request(debug):
    """Return json data from the server

    Get artist, title, playerName, playerStat and volume percent.
    """

    logging.info('Get player info...')
    connflag = 0
    server_data = {}

    try:
        resp = requests.get(url_mdata)
    except requests.exceptions.RequestException as e:
        connflag = 1

    if(connflag == 0):
        x_status = requests.get(url_status)
        json_status = x_status.json()

        x_mdata  = requests.get(url_mdata)
        json_mdata = x_mdata.json()

        x_volume = requests.get(url_volume)
        json_volume = x_volume.json()

        if debug == 1:
            print(url_status, json.dumps(x_status.json()),'\n')
            print(url_mdata, json.dumps(x_mdata.json()),'\n')
            print(url_volume, json.dumps(x_volume.json()),'\n')

        server_data = {'artist': json_mdata['artist'], 'title': json_mdata['title'], 'playerName': json_mdata['playerName'],\
        'playerState': json_mdata['playerState'], 'percent': json_volume['percent']}

        # Need a check for null or None data types.
        # server_data['artist'] = 'Thing'

    else:
        print('Could not connect to: ', url_mdata)
        server_data = {'artist': '--00--', 'title': 'Trying: ' + server, 'playerName': 'Con Error',\
        'playerState': 'Con Error', 'percent': 0}

    return server_data

def lcd_draw(server_json, ip_addr):
    """Draw server_data on the LCD

    Draw artist, title, playerName, playerStat and volume percent.
    """
    now = datetime.now()
    y = 0
    x = 0
    xclock = 60
    speaker_icon = Image.open("/home/admin/tft-display/pic/speaker-icon-sm.jpg")
    play_icon    = Image.open("/home/admin/tft-display/pic/play-icon-sm.jpg")
    pause_icon   = Image.open("/home/admin/tft-display/pic/pause-icon-sm.jpg")

    # Get the height of the fonts using getbbox = (left, top, right, bottom)
    a,b,c, clock_h  = clock_font.getbbox("Text")
    a,b,c, large_h  = large_font.getbbox("Text")
    a,b,c, medium_h = medium_font.getbbox("Text")
    a,b,c, small_h  = small_font.getbbox("Text")
    a,b,c, tiny_h   = tiny_font.getbbox("Text")

    canvas_layer = Image.new('RGB', (disp.width, disp.height), "BLACK")
    #img_draw = ImageDraw.Draw(canvas_layer) <- is this needed?
    text_layer = Image.new('RGB', (320, 320))

    text_draw = ImageDraw.Draw(text_layer)

    text_draw.text((xclock, y), now.strftime("%I:%M"), font=large_font, fill="#FFFFFF")
    text_draw.text((xclock+160, y+5), now.strftime("%p"), font=small_font, fill="#FFFFFF")
    y += clock_h + 6

    text_draw.text((x, y), server_json['artist'], font=medium_font, fill="#FFFFFF")
    y += medium_h + 6

    text_draw.text((x, y), server_json['title'][:20], font=small_font, fill="#FFFFFF")
    y += small_h + 6

    text_draw.text((x, y), server_json['title'][20:], font=small_font, fill="#FFFFFF")
    y += small_h + 20

    # Status line section of the display
    text_draw.line((0, y, 320, y), fill="white", width=1)
    y += tiny_h

    text_layer.paste(speaker_icon, (215,y+2))
    text_draw.text((245, y), str(int(server_json['percent'])) + "%", font=small_font, fill="white")

    if server_json['playerState'] == 'playing':
        text_layer.paste(pause_icon, (x,y+2))
    if server_json['playerState'] == 'paused':
        text_layer.paste(play_icon, (x,y+2))
    if server_json['playerState'] == None:
        text_draw.text((x+3,y), '?', font=small_font, fill="white")

    text_draw.text((x+27, y), server_json['playerName'].capitalize(), font=small_font, fill="white")

    text_draw.text((x, 220), "SecondWave v0.2   IP:" + ip_addr, font=tiny_font, fill="#FFFFFF")

    rotated_text_layer = text_layer.rotate(90)
    canvas_layer.paste(rotated_text_layer, (0,0))
    disp.ShowImage(canvas_layer)

def getip():
    cmd = "hostname -I"
    ip_all = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    ip_addr = ip_all.split()
    return ip_addr[1]

def main():
    server_json = server_request(0)
    ip_addr = getip()
    lcd_draw(server_json, ip_addr)

while True:
    main()
    time.sleep(5)
