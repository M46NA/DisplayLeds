#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python Version 2.7
# display.py
#------------------------------------------------------------


# Einbindung der notwendigen Grundbibliotheken
import RPi.GPIO as gpio
import time, os, sys, threading

# Einbindung 0,96 Zoll OLED Display 128x64 Pixel
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

TasterAktiv = True#boolean für beenden der Schleife

#setup of gpio
gpio.setmode(gpio.BCM)
gpio.setup(14,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(15,gpio.IN,pull_up_down=gpio.PUD_UP)
RST=24#RPi pin config
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)# Display 128x64 display with hardware I2C:
disp.begin()#initialize library
disp.clear()#clear Display
disp.display()#update Display image

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
w = disp.width
width=w
h = disp.height
height=h
image = Image.new('1', (w, h))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,w-1,h-1), outline=0, fill=0)#fill display with black
# Load default font.
font = ImageFont.load_default()

#defining some constants for ease of use
padding=2
w2=width/2
h2=height/2
h4=height/4



class Menu():
	menu=0
	menuButton=0
	buttonValue=0

	def MenuControl(self,LTaster,RTaster):
		if LTaster:
			menuButton +=1
		if menuButton>7:
			menuButton=0
		Render(menu, menuButton,buttonValue)


	def Render(self,menu,menuButton,buttonValue):
		print("made it here")

		draw.rectangle((0,0,width-1,height-1), outline=255, fill=0) #Display leeren

		#boxes on the Left side
		draw.rectangle((0,0,width/2-1,height/4-1),outline=255,fill=0)#1st top box left 
		draw.rectangle((0,height/4-1,width/2-1,height/2-1),outline=255,fill=0)#2nd top box left
		draw.rectangle((0,height/2-1,width/2-1,height/4*3-1),outline=255,fill=0)#3rd box left
		draw.rectangle((0,height/4*3-1,width/2-1,height-1),outline=255,fill=0)#4th box left

		#boxes on the right side
		draw.rectangle((width/2-1,0,width-1,height/4-1),outline=255,fill=0)#1st top box right 
		draw.rectangle((width/2-1,height/4-1,width-1,height/2-1),outline=255,fill=0)#2nd top box right
		draw.rectangle((width/2-1,height/2-1,width-1,height/4*3-1),outline=255,fill=0)#3rd box right
		draw.rectangle((width/2-1,height/4*3-1,width-1,height-1),outline=255,fill=255)#4th box right

		#Todo alle menus vereinen durch arrays für die menueinträge
		if menu==0:#draws menu 0
			if menuButton<4:
				draw.rectangle((padding,padding+menuButton*h4,w2-1-padding,(menuButton+1)*h4-1-padding),outline=255,fill=0)
			if menuButton>3 and menuButton<7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=255,fill=0)
			if menuButton==7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=0,fill=255)
			draw.text((5+padding,padding),'Color',font=font,fill=255)#Adds text to menu 0
			draw.text((5+padding,padding+h4),'Wave',font=font,fill=255)
			draw.text((5+padding,padding+h2),'Multi',font=font,fill=255)
			draw.text((5+padding,padding+h4*3),'Rainbow',font=font,fill=255)
			draw.text((5+padding+w2,padding),'Values',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4),'Programs',font=font,fill=255)
			draw.text((5+padding+w2,padding+h2),'Fades',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4*3),'OFF',font=font,fill=0)

		if menu==1:
			if menuButton<4:
				draw.rectangle((padding,padding+menuButton*h4,w2-1-padding,(menuButton+1)*h4-1-padding),outline=255,fill=0)
			if menuButton>3 and menuButton<7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=255,fill=0)
			if menuButton==7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=0,fill=255)
			draw.text((5+padding,padding),'Red',font=font,fill=255)#Adds text to menu 0
			draw.text((5+padding,padding+h4),'Green',font=font,fill=255)
			draw.text((5+padding,padding+h2),'Blue',font=font,fill=255)
			draw.text((5+padding,padding+h4*3),'Cyan',font=font,fill=255)
			draw.text((5+padding+w2,padding),'Purple',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4),'Orange',font=font,fill=255)
			draw.text((5+padding+w2,padding+h2),'Yellow',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4*3),'BACK',font=font,fill=0)

		if menu==2:
			if menuButton<4:
				draw.rectangle((padding,padding+menuButton*h4,w2-1-padding,(menuButton+1)*h4-1-padding),outline=255,fill=0)
			if menuButton>3 and menuButton<7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=255,fill=0)
			if menuButton==7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=0,fill=255)
			draw.text((5+padding,padding),'Red',font=font,fill=255)#Adds text to menu 0
			draw.text((5+padding,padding+h4),'Green',font=font,fill=255)
			draw.text((5+padding,padding+h2),'Blue',font=font,fill=255)
			draw.text((5+padding,padding+h4*3),'Cyan',font=font,fill=255)
			draw.text((5+padding+w2,padding),'Purple',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4),'Orange',font=font,fill=255)
			draw.text((5+padding+w2,padding+h2),'Turquoise',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4*3),'BACK',font=font,fill=0)

		if menu==3:
			if menuButton<4:
				draw.rectangle((padding,padding+menuButton*h4,w2-1-padding,(menuButton+1)*h4-1-padding),outline=255,fill=0)
			if menuButton>3 and menuButton<7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=255,fill=0)
			if menuButton==7:
				draw.rectangle((w2-1+padding,padding+(menuButton-4)*h4,w-1-padding,(menuButton-3)*h4-1-padding),outline=0,fill=255)
			draw.text((5+padding,padding),'Polar',font=font,fill=255)#Adds text to menu 0
			draw.text((5+padding,padding+h4),'Heart',font=font,fill=255)
			draw.text((5+padding,padding+h2),'Sunrise',font=font,fill=255)
			draw.text((5+padding,padding+h4*3),'Sky',font=font,fill=255)
			draw.text((5+padding+w2,padding),'Ocean',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4),'Sound',font=font,fill=255)
			draw.text((5+padding+w2,padding+h2),'Rainbow',font=font,fill=255)
			draw.text((5+padding+w2,padding+h4*3),'BACK',font=font,fill=0)	




		disp.image(image)#outputs image to screen
		disp.display()


Menu = Menu()
Menu.MenuControl#Rendert das menu