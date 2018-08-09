#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import Common
import PopupBase as PB
import ButtonBase as BB

class FinishLevelPopup(PB.PopupBase):
	def __init__(self,):
		super(FinishLevelPopup,self).__init__();
		
	def initTitle(self):
		titleDir = Common.initFileNameInDir(self.imageDir_,"congratulations.png");
		self.title_ = pg.image.load(titleDir);
		rectObj = self.title_.get_rect();
		rectObj.center = (300, 111);
		self.background_.blit(self.title_,rectObj);

	def initBtns(self):
		PB.PopupBase.initBtns(self);
		self.quitBtn_ = BB.ButtonBase("btn_1.png",self.onCloseClicked,btnLabelStr="CLOSE");
		self.addChildNode(self,self.quitBtn_,(250,300),"center");

	def initContent(self):
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"Assimilate.TTF");
		fontObj = pg.font.Font(fontFile, 46);
		textSurfaceObj = fontObj.render("Level Clear", True, (0,0,0));
		textRectObj = textSurfaceObj.get_rect();
		textRectObj.center = (300, 220);
		self.background_.blit(textSurfaceObj,textRectObj);

		
