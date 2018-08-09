#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import MouseEventDelegate as MD
import Common

class ButtonBase(pg.Surface,MD.MouseEventDelegate):
	def __init__(self,normalImageName,callback,callbackData=None,btnLabelStr=None):

		bgFileName = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"images"),normalImageName);
		bgImage = pg.image.load(bgFileName);
		imageRect = bgImage.get_rect();
		pg.Surface.__init__(self,(imageRect.width,imageRect.height),pg.SRCALPHA, 32);
		self.convert_alpha();
		self.blit(bgImage,imageRect);
		MD.MouseEventDelegate.__init__(self);

		self.btnLabelStr_ = btnLabelStr;
		self.swallowTouch_ = True;
		self.isClicked_ = False;
		self.btnCallback_ = callback;
		self.callbackData_ = callbackData;
		self.createBtnLabel();
		self.regeistMouseEvent();

	def createBtnLabel(self):
		if self.btnLabelStr_ != None:
			color = (100,100,100);
			fontFile = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"fonts"),"Assimilate.TTF");
			fontObj = pg.font.Font(fontFile, 24);
			textSurfaceObj = fontObj.render(str(self.btnLabelStr_), True, color);
			parentRect = self.get_rect();
			textRectObj = textSurfaceObj.get_rect();
			textRectObj.center = (parentRect[2]/2,parentRect[3]/2);
			self.blit(textSurfaceObj,textRectObj);
	# delegate for clickevent
	def mouseLeftClickEnd(self,mouse):
		if self.isClicked_:
			print("ButtonBase::mouseLeftClickEnd "+str(mouse.get_pos()));
			try:
				if self.callbackData_:
					self.btnCallback_(self.callbackData_);
				else:
					self.btnCallback_();
			except Exception as e:
				import traceback
				traceback.print_exc();
				print("Button Call back Failed: "+str(e));
		self.isClicked_ = False;

	def regeistMouseEvent(self):
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);

	def showBtn(self,parentNode,pos):
		rectObj = self.get_rect();
		rectObj.center = pos;
		self.setRect(rectObj);
		parentNode.blit(self,rectObj);
	def mouseLeftClickStart(self,mouse):
		if self.rect_.collidepoint(mouse.get_pos()):
			self.isClicked_ = True;

	def mouseMidClickStart(self,mouse):
		pass;
	def mouseRightClickStart(self,mouse):
		pass;
	def mouseMidClickEnd(self,mouse):
		pass;
	def mouseRightClickEnd(self,mouse):
		pass;