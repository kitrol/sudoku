#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import Common
import ButtonBase as BB
import MouseEventDelegate as MD

class PopupBase(pg.sprite.Sprite,MD.MouseEventDelegate):
	def __init__(self,bgFileName=None,closeFileName=None):
		super(PopupBase, self).__init__();
		self.formerScreen_ = Common.DISPLAY.copy();
		self.spriteGroup_ = [];
		self.title_ = None;
		self.bgFileName_ = bgFileName;
		self.closeFileName_ = closeFileName;
		self.imageDir_ = Common.initFileNameInDir(Common.WORKDIR,"images");

		self.initBg();
		self.initTitle();
		self.initContent();
		self.initBtns();
		self.setRect((0,0,Common.SCREEN_SIZE[0],Common.SCREEN_SIZE[1]));

	def initBg(self):
		DefaultBgFileName_ = Common.initFileNameInDir(self.imageDir_,"popupBg.png");
		if self.bgFileName_ != None:
			try:
				self.bgFileName_ = Common.initFileNameInDir(self.imageDir_,self.bgFileName_);
				self.background_ = pg.image.load(self.bgFileName_);
			except Exception as e:
				self.background_ = pg.image.load(DefaultBgFileName_);
		else:
			self.background_ = pg.image.load(DefaultBgFileName_);

	def initTitle(self):
		pass
	def initBtns(self):
		self.closeBtn_ = BB.ButtonBase("close.png",self.background_,self.onCloseClicked);
		self.closeBtn_.showBtn((25,25));
	def initContent(self):
		pass
	def onCloseClicked(self):
		Common.DISPLAY.blit(self.formerScreen_,(0,0));
		self.formerScreen_ = None;
	def popupShpw(self):
		Common.DISPLAY.blit(self.background_,(0,0));
		self.update();
		
        


		
		