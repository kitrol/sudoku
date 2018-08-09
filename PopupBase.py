#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import Common
import ButtonBase as BB
import MouseEventDelegate as MD
from DestroyableNode import *

class PopupBase(pg.Surface,MD.MouseEventDelegate):
	def __init__(self,bgFileName=None,closeFileName=None):
		MD.MouseEventDelegate.__init__(self);
		pg.Surface.__init__(self,(Common.SCREEN_SIZE[0],Common.SCREEN_SIZE[1]),pg.SRCALPHA, 32);
		self.convert_alpha();
		self.formerScreen_ = Common.DISPLAY.copy();
		self.spriteGroup_ = [];
		self.title_ = None;
		self.bgFileName_ = bgFileName;
		self.closeFileName_ = closeFileName;
		self.imageDir_ = Common.initFileNameInDir(Common.WORKDIR,"images");
		self.setRect((0,0,Common.SCREEN_SIZE[0],Common.SCREEN_SIZE[1]));
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);
		
		self.initBg();
		self.initTitle();
		self.initContent();
		self.initBtns();
		

	def initBg(self):
		DefaultBgFileName_ = Common.initFileNameInDir(self.imageDir_,"popupBg.png");
		bg = None;
		if self.bgFileName_ != None:
			try:
				self.bgFileName_ = Common.initFileNameInDir(self.imageDir_,self.bgFileName_);
				bg = pg.image.load(self.bgFileName_);
			except Exception as e:
				bg = pg.image.load(DefaultBgFileName_);
		else:
			bg = pg.image.load(DefaultBgFileName_);

		imageRect = bg.get_rect();
		imageRect.center = (Common.SCREEN_SIZE[0]/2,Common.SCREEN_SIZE[1]/2);
		self.blit(bg,imageRect);

	def initTitle(self):
		pass
	def initBtns(self):
		self.closeBtn_ = BB.ButtonBase("close.png",self.onCloseClicked);
		# self.closeBtn_.showBtn((25,25));
		self.addChildNode(self,self.closeBtn_,(25,25),"center");
		
	def initContent(self):
		pass

	def onCloseClicked(self):
		self.destroy();
		print(str(self.destroyed()));
		Common.DISPLAY.blit(self.formerScreen_,(0,0));
		self.formerScreen_ = None;

	def popupShpw(self):
		Common.DISPLAY.blit(self,(0,0));
		
	# stop mouse event from passing through
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
		pass;	
        


		
		