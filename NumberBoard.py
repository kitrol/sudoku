#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import platform
import random
import math

def initFileNameInDir(dirName,fileName):
	if platform.system() == 'Darwin':
		return dirName+"/"+fileName;
	return dirName+"\\"+fileName;
	
fontFile = None;

class NumberBoard:
	offset = 30;
	start_X = 60;
	start_Y = 60;
	hardness = ((41,50),(51,53),(54,58),(59,60));
	normal_line_size = 2;
	bold_line_size = 4;
	BLACK = (0,0,0);
	worktDir_ = None;

	def __init__(self, display, finalBoard, level,worktDir):
		self.display_ = display;
		self.finalBoard_ = finalBoard;
		self.testBoard_ = np.array(finalBoard);
		self.level_ = level;
		self.worktDir_ = worktDir;
		emptyNumArray = self.createEmptyArray();
	
	def createEmptyArray(self):
		hardNessLevel = NumberBoard.hardness[self.level_];
		hardNess = random.randint(hardNessLevel[0]-1,hardNessLevel[1]+1);
		emptyNumArray = [0,0,0,0,0,0,0,0,0];
		each = math.ceil(hardNess/9);
		for x in range(0,9):
			emptyNumArray[x] = random.randint(each-2,each+2);
		while sum(emptyNumArray)<hardNessLevel[0]:
			index = emptyNumArray.index(min(emptyNumArray));
			emptyNumArray[index] += random.randint(1,2);
			
		while sum(emptyNumArray)>hardNessLevel[1]:
			index = emptyNumArray.index(max(emptyNumArray));
			emptyNumArray[index] -= random.randint(1,2);
		for line in range(0,9):
			lineArray = self.testBoard_[line];
			emptyNumCnt = emptyNumArray[line];
			indexArray = random.sample(range(0,9),9-emptyNumCnt);
			for index in range(0,9):
				if index not in indexArray:
					lineArray[index] = 0;
		return emptyNumArray;

	def drawBoard(self,start_X,start_Y,offset):
		display = self.display_;
		# offset = NumberBoard.offset;
		BLACK = NumberBoard.BLACK;
		normal_line_size = NumberBoard.normal_line_size;
		bold_line_size = NumberBoard.bold_line_size;
		# start_X = NumberBoard.start_X;
		# start_Y = NumberBoard.start_Y;
		global fontFile;
		fontFile = initFileNameInDir(initFileNameInDir(self.worktDir_,"fonts"),"Bank Gothic Medium BT.TTF");

		for column in range(4,7):
			color = (220,230,235,125);
			display.fill(color,(start_X, start_Y+(column-1)*offset,offset*9,offset));
			display.fill(color,(start_X+(column-1)*offset, start_Y,offset,offset*9));

		for column in range(1,11):
			lineSize = normal_line_size;
			if column%3==1:
				lineSize = bold_line_size;			
			pg.draw.line(display, BLACK, (start_X, start_Y+(column-1)*offset), (start_X+9*offset, start_Y+(column-1)*offset), lineSize);
			pg.draw.line(display, BLACK, (start_X+(column-1)*offset, start_Y), (start_X+(column-1)*offset, start_Y+9*offset), lineSize);
		
		fontObj = pg.font.Font(fontFile, 24);
		for line in range(0,9):
			for column in range(0,9):
				num = self.testBoard_[line,column];
				if num > 0:
					textSurfaceObj = fontObj.render(str(num), True, (0,0,0));
					textRectObj = textSurfaceObj.get_rect();
					textRectObj.center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
					display.blit(textSurfaceObj,textRectObj);		



class SideBoard():
	normal_line_size =2;
	bold_line_size = 4;
	BLACK = (0,0,0);
	worktDir_ = None;
	def __init__(self, display,worktDir):
		self.display_ = display;
		self.worktDir_ = worktDir;

	def drwaSideBoard(self,start_X,start_Y,offset):
		global fontFile;
		BLACK = self.BLACK;
		display = self.display_;
		for column in range(1,5):
			lineSize = SideBoard.normal_line_size;
			if column%3==1:
				lineSize = SideBoard.bold_line_size;			
			pg.draw.line(display, BLACK, (start_X, start_Y+(column-1)*offset), (start_X+3*offset, start_Y+(column-1)*offset), lineSize);
			pg.draw.line(display, BLACK, (start_X+(column-1)*offset, start_Y), (start_X+(column-1)*offset, start_Y+3*offset), lineSize);
		fontObj = pg.font.Font(fontFile, 24);
		for line in range(0,3):
			for column in range(0,3):
				num = line*3+column+1;
				if num > 0:
					textSurfaceObj = fontObj.render(str(num), True, (0,0,0));
					textRectObj = textSurfaceObj.get_rect();
					textRectObj.center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
					display.blit(textSurfaceObj,textRectObj);
		