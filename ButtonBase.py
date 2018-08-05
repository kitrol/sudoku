#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import MouseEventDelegate as MD
import Common

class ButtonBase(pg.sprite.Sprite,MD.MouseEventDelegate):
	def __init__(self, normalImageName,parent,callback,callbackData=None,btnLabelStr=None):
		super(ButtonBase, self).__init__()
		bgFileName = Common.initFileNameInDir(Common.initFileNameInDir(Common.WORKDIR,"images"),normalImageName);
		self.btn_ = pg.image.load(bgFileName);
		self.btnLabelStr_ = btnLabelStr;
		self.parent_ = parent;
		self.rect_ = (0,0,0,0); # record the position of the button
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
			parentRect = self.btn_.get_rect();
			textRectObj = textSurfaceObj.get_rect();
			textRectObj.center = (parentRect[2]/2,parentRect[3]/2);
			self.btn_.blit(textSurfaceObj,textRectObj);
	# delegate for clickevent
	def mouseLeftClickEnd(self,mouse):
		if self.isClicked_:
			print("ButtonBase::mouseLeftClickEnd "+str(mouse.get_pos()));
			try:
				print("ButtonBase mouseLeftClickEnd "+str(self.callbackData_));
				self.btnCallback_();
			except Exception as e:
				print("Button Call back Failed "+str(e));
		self.isClicked_ = False;
		

	def regeistMouseEvent(self):
		mouseControler = MD.MouseEventsDistributer.getControler();
		mouseControler.regeistDelegate(self);

	def showBtn(self,pos):
		rectObj = self.btn_.get_rect();
		rectObj.center = pos;
		self.rect_ = rectObj;
		self.parent_.blit(self.btn_,rectObj);
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