#!/usr/bin/python
# -*- coding: UTF-8 -*-
import platform
import os

WORKDIR = None;
SCREEN_SIZE = (600,400);
DISPLAY = None;
LEVELSTR = ("EASY","MID","HARD","HELL");
MISTAKE_MAX = 5;
TIPS_MAX = 5;

BG_COLOR = (244,244,244,125);
DARK_COLOR = (220,230,235,125);
SELECT_COLOR = (200,200,200,125);

# TOUCH_PRIORITY

TOUCH_PRIORITY_POPUP = -100;

TOUCH_PRIORITY_PLAY = 0
def initFileNameInDir(dirName,fileName):
	if platform.system() == 'Darwin':
		return dirName+"/"+fileName;
	return dirName+"\\"+fileName;

def initConstValues(argv):
	global WORKDIR;
	WORKDIR = os.path.dirname(argv[0]);

def setDisplay(display):
	global DISPLAY;
	DISPLAY = display;