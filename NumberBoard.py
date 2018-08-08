#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import random
import math
import MouseEventDelegate as MD
import GameEventBroadcaster as GB
import TimeEventController as TC
import PixelProgressBar as PPG
from DestroyableNode import *
import Common

BG_COLOR = (244,244,244,125);
DARK_COLOR = (220,230,235,125);
SELECT_COLOR = (200,200,200,125);
ONANIMATION = False;
	
class NumberBoard(MD.MouseEventDelegate,object):
	hardness = ((41,50),(51,53),(54,58),(59,60));
	normal_line_size = 2;
	bold_line_size = 4;
	BLACK = (0,0,0);

	def __init__(self, display, finalBoard, level):
		super(NumberBoard, self).__init__();
		self.display_ = display;
		self.finalBoard_ = finalBoard;
		self.testBoard_ = np.array(finalBoard);
		self.tryBoard_ = None;
		self.level_ = level;
		self.start_X = 0;
		self.start_Y = 0;
		self.offset = 0;
		self.emptyCeils_ = 0;
		self.selected_coordinate = (-1,-1);
		self.createEmptyArray();
		self.numberSurface_ = None;
		self.progressBar_ = None;
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_INPUT_NUM",self,self.onUpdateNum));
	
	def createEmptyArray(self):
		hardNessLevel = NumberBoard.hardness[self.level_];
		self.emptyCeils_ = random.randint(hardNessLevel[0]-1,hardNessLevel[1]+1);
		emptyNumArray = [0,0,0,0,0,0,0,0,0];
		each = math.ceil(self.emptyCeils_/9);
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

	def drawBoard(self,start_X,start_Y,offset,selected_line=-1,selected_column=-1):
		display = self.display_;
		BLACK = NumberBoard.BLACK;
		normal_line_size = NumberBoard.normal_line_size;
		bold_line_size = NumberBoard.bold_line_size;
		self.setRect((start_X,start_Y,offset*9,offset*9));
		self.start_X = start_X;
		self.start_Y = start_Y;
		self.offset = offset;
		selected_num = 0;
		global fontFile;
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"Bank Gothic Medium BT.TTF");
		self.numberSurface_ = pg.Surface((offset*9,offset*9));
		self.numberSurface_.fill((244,244,244,125));
		for column in range(4,7):
			global DARK_COLOR;
			self.numberSurface_.fill(DARK_COLOR,(0, (column-1)*offset,offset*9,offset));
			self.numberSurface_.fill(DARK_COLOR,((column-1)*offset, 0,offset,offset*9));

		if selected_line >=0 and selected_column>=0:
			selected_num = self.tryBoard_[selected_line,selected_column];
			self.numberSurface_.fill(SELECT_COLOR,(0, selected_line*self.offset,self.offset*9,self.offset));
			self.numberSurface_.fill(SELECT_COLOR,(selected_column*self.offset, 0,self.offset,self.offset*9));
			# if self.testBoard_[selected_line][selected_column] > 0:
			# 	return False;
			if self.testBoard_[selected_line][selected_column]==0:
				self.selected_coordinate = (selected_line,selected_column);
		display.blit(self.numberSurface_,(start_X,start_Y));
		# Draw board
		for column in range(1,11):
			lineSize = normal_line_size;
			if column%3==1:
				lineSize = bold_line_size;			
			pg.draw.line(display, BLACK, (start_X, start_Y+(column-1)*offset), (start_X+9*offset, start_Y+(column-1)*offset), lineSize);
			pg.draw.line(display, BLACK, (start_X+(column-1)*offset, start_Y), (start_X+(column-1)*offset, start_Y+9*offset), lineSize);
		# draw lines
		fontObj = pg.font.Font(fontFile, 24);
		color = (100,100,100);
		for line in range(0,9):
			for column in range(0,9):
				num = self.tryBoard_[line,column];
				if num > 0:
					# make the default num showed different with that user input
					if self.testBoard_[line,column] != num:
						color = (150,80,80);
					else:
						color = (15,15,15);
					isBold = False;
					# something like high light the same number on board
					if selected_num >0 and self.tryBoard_[line,column]==selected_num:
						fontObj = pg.font.Font(fontFile, 26);
						isBold = True;
					else:
						fontObj = pg.font.Font(fontFile, 24);
					fontObj.set_bold(isBold);
					textSurfaceObj = fontObj.render(str(num), True, color);
					textRectObj = textSurfaceObj.get_rect();
					center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
					setattr(textRectObj,"center",center);

					
					# textRectObj.center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
					# print(textRectObj.center);
					display.blit(textSurfaceObj,textRectObj);
		# add progress bar
		# width,height,bgColor,barColor,percent,
		count = self.getFilledNums();
		self.progressBar_ = PPG.PixelProgressBar(270,10,(150,150,150),(0,0,0),float(count)/81);
		self.progressBar_.drawProgressBar(display,60,350);

	def getFilledNums(self):
		tempArray = self.tryBoard_.copy();
		tempArray.shape = -1;
		count = 0;
		for x in tempArray:
			if x != 0:
				count+=1;
		return count;

	def onUpdateNum(self,data):
		if self.selected_coordinate == (-1,-1):
			return;
		line = self.selected_coordinate[0];
		column = self.selected_coordinate[1];
		if self.testBoard_[line,column] > 0:
			return;
		if int(data) == self.finalBoard_[line,column]:
			# FILL IN A RIGHT NUMBER
			self.tryBoard_[line,column] = int(data);
			self.drawBoard(self.start_X,self.start_Y,self.offset,line,column);
			count = self.getFilledNums();
			self.progressBar_.setPercent(float(count)/81);
			self.checkIsNumFinish(int(data));
			self.checkFinish();
		else:
			# FILL IN A WRONG NUMBER
			self.drawGuessWrong(line,column,int(data));
	def restStatus(self,data):
		global ONANIMATION;
		ONANIMATION = False;
		self.drawBoard(self.start_X,self.start_Y,self.offset,data[0],data[1]);

	def drawGuessWrong(self,line,column,num):
		global fontFile;
		fontObj = pg.font.Font(fontFile, 24);
		textSurfaceObj = fontObj.render(str(num), True, (255,0,0));
		textRectObj = textSurfaceObj.get_rect();
		textRectObj.center = (self.start_X+column*self.offset+self.offset/2, self.start_Y+line*self.offset+self.offset/2+2);
		self.display_.blit(textSurfaceObj,textRectObj);
		global ONANIMATION;
		ONANIMATION = True;
		timeEventController = TC.TimeEventController.getControler();
		# eventType,delayTime,target,callbackFunc
		callbackEvent = TC.TimeEvent("TET_Callback",2.0,self,self.restStatus,callbackData=(line,column));
		timeEventController.regeistEvent(callbackEvent);
		
	def checkIsNumFinish(self,targetNum):
		tempArray = self.tryBoard_.copy();
		tempArray.shape = -1;
		counter = 0;
		for num in tempArray:
			if num == targetNum:
				counter += 1;
		if counter>=9:
			broadcaster = GB.GameEventBroadcaster.getControler();
			broadcaster.envokeEvent("GAME_EVENT_NUM_FULL",targetNum);
			
	def checkFinish(self):
		for line in range(0,9):
			if 0 in self.tryBoard_[line]:
				return False;
		# post notification when finished
		def showFinish(data):
			GB.GameEventBroadcaster.getControler().envokeEvent("GAME_EVENT_LEVEL_ACCOMPLISH",{"level":1,"timeCost":100});
		callbackEvent = TC.TimeEvent("TET_Callback",1.0,self,showFinish,callbackData=(1,2));
		timeEventController = TC.TimeEventController.getControler();
		timeEventController.regeistEvent(callbackEvent);

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
		elif (self.STARTPOS[0]-self.start_X)>=self.offset*9 or (self.STARTPOS[0]-self.start_X)<=0 or (self.STARTPOS[1]-self.start_Y)>=self.offset*9 or (self.STARTPOS[1]-self.start_Y)<=0:
			return False;
		if ONANIMATION:
			return False;
		column = int(math.floor((self.STARTPOS[0]-self.start_X)/self.offset));
		line = int(math.floor((self.STARTPOS[1]-self.start_Y)/self.offset));
		self.drawBoard(self.start_X,self.start_Y,self.offset,line,column);

	def autoMark(self,leftCount):
		emptyCeils = self.emptyCeils_;
		for line in range(0,9):
			for column in range(0,9):
				if self.tryBoard_[line,column] == 0:
		 			self.selected_coordinate = (line,column);
		 			# self.tryBoard_[line,column] = self.finalBoard_[line,column];
		 			self.onUpdateNum(self.finalBoard_[line,column]);
		 			emptyCeils -= 1;
		 			if emptyCeils==leftCount:
		 				return emptyCeils;

class SideBoard(MD.MouseEventDelegate):
	normal_line_size =2;
	bold_line_size = 4;
	BLACK = (0,0,0);
	def __init__(self, display):
		MD.MouseEventDelegate.__init__(self);
		self.display_ = display;
		self.start_X = 0;
		self.start_Y = 0;
		self.offset = 0;
		self.rect_ = (0,0,0,0);
		self.finishedNums_ = [];
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_NUM_FULL",self,self.deleteFullNum));

	def drwaSideBoard(self,start_X,start_Y,offset):
		fontObj = pg.font.Font(fontFile, 25);
		BLACK = self.BLACK;
		self.start_X = start_X;
		self.start_Y = start_Y;
		self.offset = offset;
		self.setRect((start_X,start_Y,offset*3,offset*3));
		display = self.display_;
		display.fill(DARK_COLOR,(start_X, start_Y,offset*3,offset*3));

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
				if num not in self.finishedNums_:
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
		if num in self.finishedNums_:
			# have filled all this num
			return False;
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.envokeEvent("GAME_EVENT_INPUT_NUM",num);

	def deleteFullNum(self,targetNum):
		self.finishedNums_.append(int(targetNum));
		start_X	=	self.start_X;
		start_Y = self.start_Y;
		offset = self.offset;
		self.drwaSideBoard(start_X,start_Y,offset);