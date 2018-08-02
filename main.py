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
import NumberBoard;

LEFT_CLICK = False;
STARTPOS = None;

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

def mouseClickStart(mouse,pressed_array):
	offset = 30;
	start_X = 60;
	start_Y = 60;
	global LEFT_CLICK;
	global STARTPOS;
	print(pressed_array);
	if pressed_array[0]:
		LEFT_CLICK = True;
		STARTPOS = mouse.get_pos();
		print('Pressed LEFT Button!');
	elif pressed_array[1]:
		pass;
	elif pressed_array[2]:
		pass;
	print(mouse.get_pos());

def mouseClickEnd(mouse):
	global LEFT_CLICK;
	LEFT_CLICK = False;
	if STARTPOS == None:
		return False;
	endPos = mouse.get_pos();
	if math.sqrt((endPos[1]-STARTPOS[1])**2+(endPos[0]-STARTPOS[0])**2)> 20:
		return False;

	print(mouse.get_pos());

def main(argv):
	finalBoard = sudoku.initFinalBoard();
	print(str(finalBoard));
	level = (0,1,2,3);
	worktDir_ = os.path.dirname(argv[0]);
	################# start engine
	pg.init();
	display = pg.display.set_mode((600,400));
	pg.display.set_caption("Sudoku Challange");
	display.fill((244,244,244,125));
	fpsClock = pg.time.Clock();

	################ draw board
	board = NumberBoard.NumberBoard(display,finalBoard,2,worktDir_);
	board.drawBoard(60,60,30);
	sideBoard = NumberBoard.SideBoard(display,worktDir_);
	sideBoard.drwaSideBoard(400,60,30);
    ##############

	while True:
		keys = pg.key.get_pressed();
		if (keys[310] and keys[113]) or (keys[306] and keys[113]):# 
			pg.quit();
			sys.exit();
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit();
				sys.exit();
			elif event.type == pg.MOUSEBUTTONDOWN:
				if sum(pg.mouse.get_pressed())>0:
					mouseClickStart(pg.mouse,pg.mouse.get_pressed());
			elif event.type == pg.MOUSEBUTTONUP:
				mouseClickEnd(pg.mouse);
		pg.display.update();
		fpsClock.tick(60);



if __name__ == '__main__':
   main(sys.argv)