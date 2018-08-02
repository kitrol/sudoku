#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import sudoku
import platform
import random
import math

def gameStart():
	pass;
def initFileNameInDir(dirName,fileName):
	if platform.system() == 'Darwin':
		return dirName+"/"+fileName;
	return dirName+"\\"+fileName;

def initTestBoard(testBoard,hardNessLevel):
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
	return emptyNumArray;

def main(argv):
	finalBoard = sudoku.initFinalBoard();
	print(str(finalBoard));
	testBoard = np.array(finalBoard);
	level = (0,1,2,3);
	hardness = ((41,50),(51,53),(54,58),(59,60));
	emptyNumArray = initTestBoard(testBoard,hardness[2]);
	print(emptyNumArray);
	for line in range(0,9):
		lineArray = testBoard[line];
		emptyNumCnt = emptyNumArray[line];
		indexArray = random.sample(range(0,9),9-emptyNumCnt);
		print(indexArray);



	if 1:
		return;
	worktDir_ = os.path.dirname(argv[0]);
	fontFile = initFileNameInDir(initFileNameInDir(worktDir_,"fonts"),"Bank Gothic Medium BT.TTF");

	pg.init();
	display = pg.display.set_mode((600,400));
	pg.display.set_caption("Sudoku Challange");
	display.fill((244,244,244,125));
	fpsClock = pg.time.Clock();
	offset = 30;
	BLACK = (0,0,0);
	start_X = 60;
	start_Y = 60;
	normal_line_size = 2;
	bold_line_size = 4;
	for column in xrange(4,7):
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
			num = finalBoard[line,column];
			textSurfaceObj = fontObj.render(str(num), True, (0,0,0));
			textRectObj = textSurfaceObj.get_rect();
			textRectObj.center = (start_X+column*offset+offset/2, start_Y+line*offset+offset/2+2);
			display.blit(textSurfaceObj,textRectObj);
			
	while True:
		keys = pg.key.get_pressed();
		if keys[310] and keys[113]:# 
			pg.quit();
			sys.exit();
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit();
				sys.exit();

		pg.display.update();
		fpsClock.tick(60);



if __name__ == '__main__':
   main(sys.argv)