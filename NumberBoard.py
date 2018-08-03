#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import platform
import random
import math
import MouseEventDelegate as MD
import GameEventBroadcaster as GB

BG_COLOR = (244,244,244,125);
DARK_COLOR = (220,230,235,125);
SELECT_COLOR = (200,200,200,125);

def initFileNameInDir(dirName,fileName):
	if platform.system() == 'Darwin':
		return dirName+"/"+fileName;
	return dirName+"\\"+fileName;
	
fontFile = None;
		
class NumberBoard(MD.MouseEventDelegate,object):
	hardness = ((41,50),(51,53),(54,58),(59,60));
	normal_line_size = 2;
	bold_line_size = 4;
	BLACK = (0,0,0);
	worktDir_ = None;

	def __init__(self, display, finalBoard, level,worktDir):
		super(MD.MouseEventDelegate, self).__init__();
		self.display_ = display;
		self.finalBoard_ = finalBoard;
		self.testBoard_ = np.array(finalBoard);
		self.tryBoard_ = None;
		self.level_ = level;
		self.worktDir_ = worktDir;
		self.start_X = 0;
		self.start_Y = 0;
		self.offset = 0;
		self.selected_coordinate = (-1,-1);
		self.createEmptyArray();
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_INPUT_NUM",self,self.onUpdateNum));
	
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
		self.tryBoard_ = np.array(self.testBoard_);
		return emptyNumArray;

	def drawBoard(self,start_X,start_Y,offset):
		display = self.display_;
		BLACK = NumberBoard.BLACK;
		normal_line_size = NumberBoard.normal_line_size;
		bold_line_size = NumberBoard.bold_line_size;
		self.start_X = start_X;
		self.start_Y = start_Y;
		self.offset = offset;
		global fontFile;
		fontFile = initFileNameInDir(initFileNameInDir(self.worktDir_,"fonts"),"Bank Gothic Medium BT.TTF");

		for column in range(4,7):
			global DARK_COLOR;
			display.fill(DARK_COLOR,(start_X, start_Y+(column-1)*offset,offset*9,offset));
			display.fill(DARK_COLOR,(start_X+(column-1)*offset, start_Y,offset,offset*9));

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
	# delegate got from parent MouseEventDelegate
	def onSelectTile(self,line,column):
		global DARK_COLOR;
		display = self.display_;
		# for column_1 in range(4,7):
		# 	display.fill(DARK_COLOR,(self.start_X, self.start_Y+(column_1-1)*self.offset,self.offset*9,self.offset));
		# 	display.fill(DARK_COLOR,(self.start_X+(column_1-1)*self.offset, self.start_Y,self.offset,self.offset*9));

		# display.fill(SELECT_COLOR,(self.start_X, self.start_Y+line*self.offset,self.offset*9,self.offset));
		# display.fill(SELECT_COLOR,(self.start_X+column*self.offset, self.start_Y,self.offset,self.offset*9));
		if self.testBoard_[line][column] > 0:
			return False;
		if self.testBoard_[line][column]==0:
			self.selected_coordinate = (line,column);
			print("onSelectTile  "+str(self.selected_coordinate));

	def onUpdateNum(self,data):
		print("NumberBoard::onUpdateNum "+str(data));
		if self.selected_coordinate == (-1,-1):
			return;
		line = self.selected_coordinate[0];
		column = self.selected_coordinate[1];
		if self.testBoard_[line][column]:

			self.selected_coordinate == (-1,-1);
			return;
		else:
			self.tryBoard_[line][column] = int(data);
			global fontFile;
			start_X = self.start_X;
			start_Y = self.start_Y;
			offset = self.offset;
			fontObj = pg.font.Font(fontFile, 24);
			textSurfaceObj = fontObj.render(str(data), True, (255,0,0));
			textRectObj = textSurfaceObj.get_rect();
			textRectObj.center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
			self.display_.blit(textSurfaceObj,textRectObj);


	def mouseLeftClickStart(self,mouse):
		pass;
	def mouseMidClickStart(self,mouse):
		pass;
	def mouseRightClickStart(self,mouse):
		pass;
	def mouseMidClickEnd(self,mouse):
		pass;
	def mouseRightClickEnd(self,mouse):
		pass;

	def mouseLeftClickEnd(self,mouse):
		endPos = mouse.get_pos();
		if math.sqrt((endPos[1]-self.STARTPOS[1])**2+(endPos[0]-self.STARTPOS[0])**2)> 20:
			return False;
		elif (self.STARTPOS[0]-self.start_X)>self.offset*9 or (self.STARTPOS[0]-self.start_X)<=0 or (self.STARTPOS[1]-self.start_Y)>self.offset*9 or (self.STARTPOS[1]-self.start_Y)<=0:
			return False;
		
		column = int(math.floor((self.STARTPOS[0]-self.start_X)/self.offset));
		line = int(math.floor((self.STARTPOS[1]-self.start_Y)/self.offset));
		self.onSelectTile(line,column);


class SideBoard(MD.MouseEventDelegate):
	normal_line_size =2;
	bold_line_size = 4;
	BLACK = (0,0,0);
	worktDir_ = None;
	def __init__(self, display,worktDir):
		super(MD.MouseEventDelegate, self).__init__();
		self.display_ = display;
		self.worktDir_ = worktDir;
		self.start_X = 0;
		self.start_Y = 0;
		self.offset = 0;
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);

	def drwaSideBoard(self,start_X,start_Y,offset):
		global fontFile;
		BLACK = self.BLACK;
		self.start_X = start_X;
		self.start_Y = start_Y;
		self.offset = offset;
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
	def mouseLeftClickStart(self,mouse):
		pass;
	def mouseMidClickStart(self,mouse):
		pass;
	def mouseRightClickStart(self,mouse):
		pass;
	def mouseMidClickEnd(self,mouse):
		pass;
	def mouseRightClickEnd(self,mouse):
		pass;
	def mouseLeftClickEnd(self,mouse):
		endPos = mouse.get_pos();
		if math.sqrt((endPos[1]-self.STARTPOS[1])**2+(endPos[0]-self.STARTPOS[0])**2)> 20:
			return False;
		elif (self.STARTPOS[0]-self.start_X)>self.offset*3 or (self.STARTPOS[0]-self.start_X)<=0 or (self.STARTPOS[1]-self.start_Y)>self.offset*3 or (self.STARTPOS[1]-self.start_Y)<=0:
			return False;

		column = math.floor((self.STARTPOS[0]-self.start_X)/self.offset);
		line = math.floor((self.STARTPOS[1]-self.start_Y)/self.offset);
		num = int(line*3+column+1);
		
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.envokeEvent("GAME_EVENT_INPUT_NUM",num);