#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import sys
import NumberBoard as NB;
import MouseEventDelegate as MD
import TimeEventController as TC
import GameEventBroadcaster as GB
import sudoku
import Common

import FinishLevelPopup as FLP

class GameLogicManager(object):
	Instance_ = None;
	def __init__(self):
		super(GameLogicManager, self).__init__()
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_LEVEL_ACCOMPLISH",self,self.onLevelAccomplished));

	@classmethod
	def getManager(cls):
		if GameLogicManager.Instance_ == None:
			GameLogicManager.Instance_ = GameLogicManager();
			return GameLogicManager.Instance_;
		else:
			return GameLogicManager.Instance_;

	def initEnv(self):
		pg.init();
		display = pg.display.set_mode(Common.SCREEN_SIZE);
		pg.display.set_caption("Sudoku Challange");
		display.fill((244,244,244,125));
		Common.setDisplay(display);

	def initStaticLayout(self):
		finalBoard = sudoku.initFinalBoard();
		print(str(finalBoard));
		################ draw board
		display = pg.display.get_surface();
		level = 0;# level = 0 1 2 3
		board = NB.NumberBoard(display,finalBoard,level);
		board.drawBoard(60,60,30);
		mouseControler = MD.MouseEventsDistributer.getControler();
		timeEventController = TC.TimeEventController.getControler();
		mouseControler.regeistDelegate(board);
		# print(hasattr(board,"drawBoard"));
		sideBoard = NB.SideBoard(display);
		sideBoard.drwaSideBoard(400,60,30);
		##############

		##########TEST##########
		# self.onLevelAccomplished({'a':123,'b':456});
		##########TEST##########

	def startMainLoop(self):
		fpsClock = pg.time.Clock();
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
					MD.MouseEventsDistributer.getControler().dealMouseEvents(event);
				elif event.type == pg.USEREVENT:
					TC.TimeEventController.getControler().tryTriggerEvent();
			pg.display.update();
			fpsClock.tick(60);


	def onLevelAccomplished(self,data):
		print("onLevelAccomplished   "+str(data));
		# show finish popup with back and play again two btns.
		# fileName = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"images"),"finishLevel.png");
		# finishBg = pg.image.load(fileName);
		newPopup = FLP.FinishLevelPopup();
		newPopup.popupShpw();
		pass;