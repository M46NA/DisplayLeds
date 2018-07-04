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

#Import of the neopixel library
from neopixel import *

Active = True#boolean für beenden der Schleife

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



# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
strip.begin()

class Menu():

	menu=0
	menuButton=0
	buttonValue=0
	def CheckButtons(self):
		try:
			while Active:
				LTaster = not gpio.input(14)
				RTaster = not gpio.input(15)
				if LTaster or RTaster:
					self.MenuControl(LTaster,RTaster)
					time.sleep(0.2)
		except KeyboardInterrupt:
			self.Destroy()
			
	def MenuControl(self,LTaster,RTaster):
		#Todo add 
		if LTaster:#advances button value when the left button is pushed
			self.menuButton +=1
		if self.menuButton>7:
			self.menuButton=0

		if RTaster:#what happens when the right button is pushed. Changes in and out of menus	
			if self.menu==0:
				if self.menuButton==7:
					self.Destroy()
				else:
					self.menu=self.menuButton+1
					self.menuButton=0
			else:

				if self.menu==1:#Colors Menu
					if self.menuButton==0:
						Leds.simpleColor(strip,Color(0,255,0))
					if self.menuButton==1:
						Leds.simpleColor(strip,Color(255,0,0))
					if self.menuButton==2:
						Leds.simpleColor(strip, Color(0,0,255))
					if self.menuButton==3:
						Leds.simpleColor(strip,Color(255,0,255))
					if self.menuButton==4:
						Leds.simpleColor(strip,Color(0,255,255))
					if self.menuButton==5:
						Leds.simpleColor(strip,Color(69,255,0))
					if self.menuButton==6:
						Leds.simpleColor(strip,Color(255,255,0))
					if self.menuButton==7:
						self.menu=0

				if self.menu==2:
					if self.menuButton==0:#Todo add function to control Leds
						Col =[0,255,0]
						Leds.wave(strip,Col)
					if self.menuButton==1:
						Col =[169,255,0]
						Leds.wave(strip,Col)
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0

				if self.menu==3:
					if self.menuButton==1:#Todo add function to control Leds
						pass
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0

				if self.menu==4:
					if self.menuButton==1:#Todo add function to control Leds
						pass
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0

				if self.menu==5:
					if self.menuButton==1:#Todo add function to control Leds
						pass
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0

				if self.menu==6:
					if self.menuButton==1:#Todo add function to control Leds
						pass
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0

				if self.menu==7:
					if self.menuButton==1:#Todo add function to control Leds
						pass
					if self.menuButton==7:
						self.menu=0
						self.menuButton=0


		if LTaster and RTaster:#goes back to the base menu when both buttons are pushed as an emergency
			self.menu=0
			self.menuButton=0
		if Active:
			self.Render(self.menu, self.menuButton,self.buttonValue)

	def Render(self,menu,menuButton,buttonValue):

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

	def Destroy(self): #when called turns off display and takes care of all the loose ends
		global Active
		Active=False
		time.sleep(0.5)
		disp.clear()#clears display
		disp.display()#updates display
		gpio.cleanup()#releases gpio resources back
		Leds.simpleColor(strip,Color(0,0,0))


class LED():
	def simpleColor(self,strip,color):
		#displays the color chosen
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
		strip.show()

	def wave(self,strip,color=[]):

		for a in range(14):
			for i in range(20,100):
				for j in range(strip.numPixels()):
					strip.setPixelColor(j,Color(color[0]*i/100,color[1]*i/100,color[2]*i/100))
				strip.show()
			time.sleep(0.1)
			for i in range(100,20,-1):
				for j in range(strip.numPixels()):
					strip.setPixelColor(j,Color(color[0]*i/100,color[1]*i/100,color[2]*i/100))
				strip.show()
			time.sleep(0.1)



Menu = Menu()
Leds =LED()
Menu.Render(0,0,0)#Initialisation of the menu
Menu.CheckButtons()