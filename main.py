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
import MouseEventDelegate as MD
import TimeEventController as TC

LEFT_CLICK = False;
STARTPOS = None;

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

	mouseControler = MD.MouseEventsDistributer.getControler();
	timeEventController = TC.TimeEventController.getControler();
	################ draw board
	board = NumberBoard.NumberBoard(display,finalBoard,0,worktDir_);
	board.drawBoard(60,60,30);
	mouseControler.regeistDelegate(board);
	# print(hasattr(board,"drawBoard"));
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
			elif (event.type == pg.MOUSEBUTTONDOWN) or (event.type == pg.MOUSEMOTION) or (event.type == pg.MOUSEBUTTONUP):
				mouseControler.dealMouseEvents(event);
			elif event.type == pg.USEREVENT:
				pass;
				timeEventController.tryTriggerEvent();
		pg.display.update();
		fpsClock.tick(60);



if __name__ == '__main__':
   main(sys.argv)