#!/usr/bin/env python
from signal import *
from subprocess import Popen, PIPE
import os, sys, random, time
import RPi.GPIO as GPIO
import argparse


# Set arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lighting', action='store_true', help='Run in light-reading mode')
parser.add_argument('-t', '--threshold', help='Set the light threshold for when the music should play (use --lighting to figure out what you need).', default=2000, type=int)
args = parser.parse_args()

# Global variables
lightOn          = False                     # Whether or not the light is on
playing          = False                     # Whether or not a song is currently playing
hasPlayedOnce    = False                     # Keep track of whether or not we've played a song yet so we don't overwrite the initial status message
music            = None                      # mpg123 process that is playing a song
song             = None                      # Name of the song playing
songPath         = "/root/poop-tunes/music/" # Directory to grab songs from
lastSong         = None                      # Name of the last song played
threshold        = args.threshold            # Threshold for the photoresistor that tells us whether or not the light is on
canceled         = False                     # Keep track of whether or not we just canceled a song. Gets reset when the light turns off.
buttonDown       = False                     # Track button state
buttonEventFired = False                     # For debouncing the cancel button
poopistCount     = 0                         # Keep track of how many times the light has turned on

# Set these to whichever GPIO pins you used
BUTTON_PIN       = 17
LIGHT_SENSOR_PIN = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Cancel button
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Print a static message instead of a new line per message
def printInline(message):
	# Clear out what we previously wrote. TODO: keep track of length of previous message to be more precise
	spaces = " " * 80
	sys.stdout.write(spaces + "\r")
	sys.stdout.write(message + "\r")
	sys.stdout.flush()

# Get the reading of the photo resistor
def RCtime (RCpin):
	reading = 0
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.output(RCpin, GPIO.LOW)
	time.sleep(0.1)

	GPIO.setup(RCpin, GPIO.IN)
	while (GPIO.input(RCpin) == GPIO.LOW):
		reading += 1
	return reading

# Find a new song to play
def GetSong():
	global lastSong
	while True:
		choice = random.choice(os.listdir(songPath))
		# Don't play the same song twice in a row!
		if (choice != lastSong):
			lastSong = choice
			return choice

# Stops the currently playing song, if there is one.
def StopMusic():
	global playing, music, canceled
	playing = False
	if (music != None):
		music.terminate()
		music = None
		if (canceled == True):
			printInline("Playback canceled.")
		else:
			printInline("Awaiting next poopist...")

# Before we exit, stop the music if it's still playing
def clean(*args):
	StopMusic()
	sys.exit(0)

# Run our 'clean' function if the script is interrupted
for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
	signal(sig, clean)

if (args.lighting == True):
	# Only print out the photo resistor reading
	while True:
		printInline("Light level: " + str(RCtime(LIGHT_SENSOR_PIN)))

print ""
print ""
print "PoopTunes 0.0.1 (alpha)"
print ""
print ""

print("                   ______                             ")
print("                   \     \.                           ")
print("                   |`\_____\               ____------ ")
print("                   |` |    |              ||       || ")
print("                   |  |    |              ||       || ")
print("      __-====-__  _|  |    |              ||       || ")
print("     (~<       >~>  \ |    |              ||      (#) ")
print("     !~~-====-~~/----`+----/            (#)           ")
print("      \         \___     /                            ")
print("       >------\     \  <                              ")
print("      <_________________>                             ")


print ""
print ""

printInline("Awaiting first poopist...")

# The main loop
while True:

	# Set flags for button state
	if (GPIO.input(BUTTON_PIN) == False):
		buttonDown = True
	else:
		buttonDown = False
		# Debouncing with buttonEventFired to see if we've handled the button
		buttonEventFired = False
	if (buttonDown and buttonEventFired == False):
		buttonEventFired = True
		# The button stops the song
		if (playing == True and music != None):
			canceled = True
			StopMusic()

	# See if the light is on or not
	lightOn = RCtime(LIGHT_SENSOR_PIN) < threshold

	# Only start a song if the light is on and one isn't currently playing. And make sure we didn't just hit the cancel button
	if (playing == False and lightOn == True and canceled == False):
		playing = True
		# Get a random song
		song = GetSong()
		# Start the song
		music = Popen(['mpg123', "-q", songPath + song])
		poopistCount += 1
		hasPlayedOnce = True
		printInline("Playing: " + song)
	elif (playing == True and lightOn == False and music != None):
		# Lights turned off and music is playing; stop the music!
		StopMusic()
	if (lightOn == False):
		# If the light is off, set the canceled flag to False to reset it so we can cancel again next time.
		canceled = False
		if (hasPlayedOnce == True):
			# Check if it's played once so we don't overwrite the initial message
			printInline("Awaiting next poopist...")

