#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import Common
import PopupBase as PB
import ButtonBase as BB

class LevelSelectPopup(PB.PopupBase):
	def __init__(self,):
		super(LevelSelectPopup, self).__init__();

	def initBtns(self):
		PB.PopupBase.initBtns(self);
		btnPos = [(200,220),(400,220),(200,300),(400,300)];
		for level in range(0,4):
			btnLabelStr = Common.LEVELSTR[level];
			levelBtn = BB.ButtonBase("btn_1.png",self.onLevelBtnClicked,callbackData={'level':level},btnLabelStr=btnLabelStr);
			self.addChildNode(self,levelBtn,btnPos[level],"center");
	
	def initBg(self):
		PB.PopupBase.initBg(self);
		secondBgFileName_ = Common.initFileNameInDir(self.imageDir_,"newGamePopup.png");
		backg2 = pg.image.load(secondBgFileName_);
		rectObj = backg2.get_rect();
		rectObj.center = (300, 200);
		self.blit(backg2,rectObj);


	def initContent(self):
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"Assimilate.TTF");
		fontObj = pg.font.Font(fontFile, 46);
		textSurfaceObj = fontObj.render("New Game", True, (0,0,0));
		textRectObj = textSurfaceObj.get_rect();
		textRectObj.center = (300, 140);
		self.blit(textSurfaceObj,textRectObj);

	def onLevelBtnClicked(self,data):
		print("onLevelBtnClicked "+str(data));
		self.destroy();
		import GameEventBroadcaster as GB
		broadcaster = GB.GameEventBroadcaster.getControler();
		broadcaster.envokeEvent("GAME_EVENT_NEW_GAME",data);
