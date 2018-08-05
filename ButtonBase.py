#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg

class ButtonBase(g.sprite.Sprite,MouseEventDelegate):
	def __init__(self, normalImageName,btnLabelStr):
		super(ButtonBase, self).__init__()
		bgFileName = Common.initFileNameInDir(Common.WORKDIR,bgFileName);
		self.btn_ = pg.image.load(bgFileName).convert_alpha();
		self.btnLabelStr_ = btnLabelStr;
		self.rect_ = self.btn_.fill((255,255,255),None,BLEND_ADD);
		print(self.rect_);
		self.rect_.center = (0,0);
		self.createBtnLabel();

	def createBtnLabel(self):
		if self.btnLabelStr_ != None:
			color = (100,100,100);
			fontObj = pg.font.Font(fontFile, 24);
			textSurfaceObj = fontObj.render(str(self.btnLabelStr_), True, color);
			textRectObj = textSurfaceObj.get_rect();
			textRectObj.center = (0,0);
			self.image.blit(textSurfaceObj,textRectObj);
    # delegate for clickevent
    def mouseLeftClickEnd(self,mouse):
		print("ButtonBase::mouseLeftClickEnd "+str(mouse.get_pos()));


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