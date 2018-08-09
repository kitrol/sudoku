#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import Common
import PopupBase as PB

class TipPopup(PB.PopupBase):
	def __init__(self,contentStr):
		self.contentStr_ = contentStr;
		print("TipPopup  "+self.contentStr_);
		PB.PopupBase.__init__(self);
	
	def initBg(self):
		PB.PopupBase.initBg(self);
		secondBgFileName_ = Common.initFileNameInDir(self.imageDir_,"tipPopupBg.png");
		backg2 = pg.image.load(secondBgFileName_);
		rectObj = backg2.get_rect();
		rectObj.center = (300, 200);
		self.blit(backg2,rectObj);


	def initContent(self):
		fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"Anklepants.TTF");
		fontObj = pg.font.Font(fontFile, 20);
		textSurfaceObj = fontObj.render(self.contentStr_, True, (0,0,0));
		textRectObj = textSurfaceObj.get_rect();
		textRectObj.center = (300, 190);
		self.blit(textSurfaceObj,textRectObj);

	def initTitle(self):
		pass