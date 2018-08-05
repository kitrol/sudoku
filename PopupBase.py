#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import Common

class PopupBase(pg.sprite.Sprite):
	
	def __init__(self,bgFileName=None,closeFileName=None):
		super(PopupBase, self).__init__()
		self.spriteGroup_ = [];
		self.title_ = None;
		imageDir = Common.initFileNameInDir(Common.WORKDIR,"images");
		DefaultBgFileName_ = Common.initFileNameInDir(imageDir,"finishLevel.png");
		DefaultCloseFileName_ = Common.initFileNameInDir(imageDir,"close.png");
		if bgFileName != None:
			try:
				bgFileName = Common.initFileNameInDir(imageDir,bgFileName);
				self.background_ = pg.image.load(bgFileName);
			except Exception as e:
				pass;
		if closeFileName != None:
			try:
				closeFileName = Common.initFileNameInDir(imageDir,closeFileName);
				self.closeBtn_ = pg.image.load(closeFileName);
			except Exception as e:
				pass;
		self.background_ = pg.image.load(DefaultBgFileName_);
		self.closeBtn_ = pg.image.load(DefaultCloseFileName_);
		self.background_.blit(self.closeBtn_,(20,20));
		
	def popupShpw(self):
		display = pg.display.get_surface();
		display.blit(self.background_,(0,0));
		self.update();
		
        


		
		