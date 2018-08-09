#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import sys
import NumberBoard as NB;
import MouseEventDelegate as MD
import TimeEventController as TC
import GameEventBroadcaster as GB
import sudoku
import SudokuFinalBoardGenerator
import Common
import ToturialPopup as TP
from LevelSelectPopup import *


import FinishLevelPopup as FLP

class GameLogicManager(MD.MouseEventDelegate):
	Instance_ = None;
	def __init__(self):
		super(GameLogicManager, self).__init__()
		self.baseDisplay_ = None;

		#########   BROADCASTER   ############
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_MISTAKE",self,self.initMistakeLabels));
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_LEVEL_ACCOMPLISH",self,self.onLevelAccomplished));
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_NEW_GAME",self,self.startNewGame));
		#########   TOUCH   ############
		self.setRect((0,0,Common.SCREEN_SIZE[0],Common.SCREEN_SIZE[1]));
		self.regeistTouch();

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
		self.initBtns();
		self.baseDisplay_ = Common.DISPLAY.copy();

	def initDynamicLayout(self,level=0):
		self.initStageLabels(level);
		self.initMistakeLabels();
		self.initBoards(level);
		

	def regeistTouch(self):
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);

	def initBtns(self):

		self.NewGameBtn_ = BB.ButtonBase("newGame.png",self.onNewGameClicked);
		self.NewGameBtn_.showBtn(Common.DISPLAY,(70,20));

		self.tipBtn_ = BB.ButtonBase("tipsBtn.png",self.onTipBtnClicked);
		self.tipBtn_.showBtn(Common.DISPLAY,(405,115));

		self.toturial_ = BB.ButtonBase("tpturial.png",self.onToturialBtnClicked);
		self.toturial_.showBtn(Common.DISPLAY,(460,118));

		self.reset_ = BB.ButtonBase("reset.png",self.onResetBtnClicked);
		self.reset_.showBtn(Common.DISPLAY,(520,118));

	def initStageLabels(self,level):
		labelStr = "Current Stage: "+Common.LEVELSTR[level];
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"BlackAdderII-Normal.TTF");
		fontObj = pg.font.Font(fontFile, 30);
		self.currentLevelLabel_ = fontObj.render(labelStr, True, (0,0,0));
		textRectObj = self.currentLevelLabel_.get_rect();
		textRectObj.center = (300, 20);
		Common.DISPLAY.blit(self.currentLevelLabel_,textRectObj);

	def initMistakeLabels(self,mistakes=0):
		labelStr = "Mistakes:%d/%d"%(mistakes,Common.MISTAKE_MAX);
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"BlackAdderII-Normal.TTF");
		fontObj = pg.font.Font(fontFile, 30);
		self.mistakeLabel_ = fontObj.render(labelStr, True, (0,0,0));
		textRectObj = self.currentLevelLabel_.get_rect();
		textRectObj.midleft = (400, 180);
		max_rect = pg.Rect(400,165,195,31);
		# paint to the background color first
		Common.DISPLAY.fill(Common.BG_COLOR,max_rect);
		# redraw the mistake label
		Common.DISPLAY.blit(self.mistakeLabel_,textRectObj);
		if mistakes >=Common.MISTAKE_MAX:
			print("LEVEL FAILED!");
	
	def initBoards(self,level):
		finalBoard = SudokuFinalBoardGenerator.initFinalBoard();
		print(str(finalBoard));
		self.board_ = NB.NumberBoard(Common.DISPLAY,finalBoard,level);
		self.board_.drawBoard(60,60,30);
		self.sideBoard_ = NB.SideBoard(Common.DISPLAY);
		self.sideBoard_.drwaSideBoard(414,218,30);

	##############  BUTTON CALL BACK  ############
	def onToturialBtnClicked(self):
		newPopup = TP.ToturialPopup();
		newPopup.popupShpw();
	def onResetBtnClicked(self):
		if self.board_:
			self.board_.restartLevel();
	def onTipBtnClicked(self):
		if self.board_:
			self.board_.useTip();

	def onNewGameClicked(self):
		newPopup = LevelSelectPopup();
		newPopup.popupShpw();

	##############  BROADCASTER EVENT  ############
	def onLevelAccomplished(self,data):
		print("onLevelAccomplished   "+str(data));
		newPopup = FLP.FinishLevelPopup();
		newPopup.popupShpw();
		
	def startNewGame(self,data):
		Common.DISPLAY.blit(self.baseDisplay_,(0,0));
		if self.board_:
			self.board_.destroy();
		if self.sideBoard_:
			self.sideBoard_.destroy();
		# do not have to destroy new game button and setting button
		self.initDynamicLayout(data['level']);
	##############  TOUCH DELEGATE  ############
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
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.envokeEvent("GAME_EVENT_CANCLE_SELECT_CELL");
	##############  MAIN LOOP  ############
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

