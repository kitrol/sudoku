#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
from DestroyableNode import *


class PixelProgressBar(DestroyableNode):
	def __init__(self, width,height,bgColor,barColor,percent,direction=0):
		super(PixelProgressBar, self).__init__()
		self.width_ = width;
		self.height_ = height;
		self.bgColor_ = bgColor;
		self.barColor_ = barColor;
		self.percent_ = percent;
		self.direction_ = direction=0;# 0 is horizon 1 is vertical 
		self.pos_x = 0;
		self.pos_y = 0;
		self.parrent = None;
		
	def drawProgressBar(self,parrent,pos_x,pos_y):
		self.pos_x = pos_x;
		self.pos_y = pos_y;
		self.parrent = parrent;
		# draw progress bar bg
		parrent.fill(self.bgColor_,(pos_x, pos_y, self.width_ ,self.height_ ));
		offset_x = self.width_%0.1;
		offset_y = self.height_%0.1;
		if self.direction_ == 1:
			# draw bar
			parrent.fill(self.barColor_,(pos_x+offset_x, pos_y+offset_y, self.width_-2*offset_x ,(self.height_-2*offset_y)*self.percent_));
		else:
			# draw bar
			parrent.fill(self.barColor_,(pos_x+offset_x, pos_y+offset_y, (self.width_-2*offset_x)*self.percent_,self.height_-2*offset_y ));
	
	def setPercent(self,newPercent):
		if self.percent_ == newPercent:
			return False;
		self.percent_ = percent;
		self.drawProgressBar(self.parrent,self.pos_x,self.pos_y);
