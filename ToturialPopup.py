#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import Common
import PopupBase as PB

class ToturialPopup(PB.PopupBase):
	def __init__(self):
		PB.PopupBase.__init__(self);
	
	def initBg(self):
		PB.PopupBase.initBg(self);
		secondBgFileName_ = Common.initFileNameInDir(self.imageDir_,"toturial.png");
		backg2 = pg.image.load(secondBgFileName_);
		rectObj = backg2.get_rect();
		rectObj.center = (300, 200);
		self.blit(backg2,rectObj);
