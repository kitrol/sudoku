#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import NumberBoard as NB;
import MouseEventDelegate as MD
import TimeEventController as TC
import GameEventBroadcaster as GB
import ButtonBase as BB
from LevelSelectPopup import *
import Common

class GameScene(MD.MouseEventDelegate):
	def __init__(self):
		MD.MouseEventDelegate.__init__(self);
		# self.fill((244,244,244,125));
		self.baseDisplay_ = None;
		self.board_ = None;
		self.sideBoard_ = None;
		#########   TOUCH   ############
		self.setRect((0,0,Common.SCREEN_SIZE[0],Common.SCREEN_SIZE[1]));
		#########   BROADCASTER   ############
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.regeistMessage(GB.BoundMessage("GAME_EVENT_MISTAKE",self,self.initMistakeLabels));

	def initStaticLayout(self):
		self.initBtns();
		self.baseDisplay_ = Common.DISPLAY.copy();
		
	def initDynamicLayout(self,finalBoard,level=0):
		self.initStageLabels(level);
		self.initMistakeLabels();
		self.initBoards(finalBoard,level);

	def initBtns(self):

		self.settingBtn_ = BB.ButtonBase("setting.png",self.showSettingPopup);
		self.settingBtn_.showBtn(self,(70,20));

		self.NewGameBtn_ = BB.ButtonBase("newGame.png",self.onNewGameClicked);
		self.NewGameBtn_.showBtn(self,(200,20));

		self.tipBtn_ = BB.ButtonBase("tipsBtn.png",self.onTipBtnClicked);
		self.tipBtn_.showBtn(self,(405,115));


		self.toturial_ = BB.ButtonBase("tpturial.png",self.onResetBtnClicked);
		self.toturial_.showBtn(self,(460,118));

		self.reset_ = BB.ButtonBase("reset.png",self.onResetBtnClicked);
		self.reset_.showBtn(self,(520,118));

	def initStageLabels(self,level):
		labelStr = "Current Stage: "+Common.LEVELSTR[level];
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"BlackAdderII-Normal.TTF");
		fontObj = pg.font.Font(fontFile, 30);
		self.currentLevelLabel_ = fontObj.render(labelStr, True, (0,0,0));
		textRectObj = self.currentLevelLabel_.get_rect();
		textRectObj.midleft = (350, 20);
		self.blit(self.currentLevelLabel_,textRectObj);

	def initMistakeLabels(self,mistakes=0):
		labelStr = "Mistakes:%d/%d"%(mistakes,Common.MISTAKE_MAX);
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"BlackAdderII-Normal.TTF");
		fontObj = pg.font.Font(fontFile, 30);
		self.mistakeLabel_ = fontObj.render(labelStr, True, (0,0,0));
		textRectObj = self.currentLevelLabel_.get_rect();
		textRectObj.center = (496, 181);
		self.blit(self.mistakeLabel_,textRectObj);

		if mistakes >=Common.MISTAKE_MAX:
			print("LEVEL FAILED!");
	
	def initBoards(self,finalBoard,level):
		self.board_ = NB.NumberBoard(self,finalBoard,level);
		self.board_.drawBoard(60,60,30);
		self.sideBoard_ = NB.SideBoard(self);
		self.sideBoard_.drwaSideBoard(414,218,30);

	def fillBoard(self):
		if self.board_ and self.board_.destroyed()==False:
			board.autoMark(2);

	def onResetBtnClicked(self):
		print("onResetBtnClicked");

	def onTipBtnClicked(self):
		print("onTipBtnClicked");

	def showSettingPopup(self):
		print("showSettingPopup");

	def onNewGameClicked(self):
		newPopup = LevelSelectPopup();
		newPopup.popupShpw();

	def startNewGame(self,finalBoard,newLevel):
		Common.DISPLAY.blit(self.baseDisplay_,(0,0));
		if self.board_:
			self.board_.destroy();
		if self.sideBoard_:
			self.sideBoard_.destroy();
		# do not have to destroy new game button and setting button
		self.initDynamicLayout(finalBoard,newLevel);

	def regeistTouch(self):
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);
	# click region is beyond button and boards
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
		Common.DISPLAY.blit(self,(0,0));


