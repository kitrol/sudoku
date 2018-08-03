#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import platform
import random
import math


class MouseEventsDistributer():
	"""docstring for MouseEventsDistributer"""
	Instance_ = None;
	
	def __init__(self):
		self.delegateList_ = [];
		self.FailureDelegates_ = [];
	@classmethod
	def getControler(cls):
		if MouseEventsDistributer.Instance_ == None:
			MouseEventsDistributer.Instance_ = MouseEventsDistributer();
			return MouseEventsDistributer.Instance_;
		else:
			return MouseEventsDistributer.Instance_;
	def removeFailureDelegates(self):
		for failedDelegate in self.FailureDelegates_[:]:
			if failedDelegate in self.delegateList_:
				self.delegateList_.remove(failedDelegate);
		self.FailureDelegates_ = [];
		
	def regeistDelegate(self,delegate):
		if delegate not in self.delegateList_:
			self.delegateList_.append(delegate);
	def unregistDelegate(self,oldDelegate):
		if oldDelegate in self.delegateList_:
			self.delegateList_.remove(oldDelegate);

	def OnMouseClickStart(self,mouse,pressed_array):
		for delegate in self.delegateList_:
			if hasattr(delegate,"mouseClickStart"):
				delegate.mouseClickStart(mouse,pressed_array);
			else:
				self.FailureDelegates_.append(delegate);
			
	def OnMouseMove(self,mouse):
		for delegate in self.delegateList_:
			if hasattr(delegate,"onMouseMove"):
				delegate.onMouseMove(mouse);
			else:
				self.FailureDelegates_.append(delegate);
		self.removeFailureDelegates();

	def OnMouseClickEnd(self,mouse):
		for delegate in self.delegateList_:
			if hasattr(delegate,"mouseClickEnd"):
				delegate.mouseClickEnd(mouse);
			else:
				self.FailureDelegates_.append(delegate);
		self.removeFailureDelegates();

	def dealMouseEvents(self,event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if sum(pg.mouse.get_pressed())>0:
				self.OnMouseClickStart(pg.mouse,pg.mouse.get_pressed());
		elif event.type == pg.MOUSEMOTION:
			self.OnMouseMove(pg.mouse);
		elif event.type == pg.MOUSEBUTTONUP:
			self.OnMouseClickEnd(pg.mouse);
		self.removeFailureDelegates();	


class MouseEventDelegate():
	"""docstring for MouseEventDelegate"""
	def __init__(self):
		self.LEFT_CLICK = False;
		self.MID_CLICK = False;
		self.RIGHT_CLICK = False;
		self.STARTPOS = None;
	def mouseClickStart(self,mouse,pressed_array):
		# print(pressed_array);
		self.STARTPOS = mouse.get_pos();
		# print("MouseEventDelegate::mouseClickStart"+str(mouse.get_pos()));
		if pressed_array[0]:
			self.LEFT_CLICK = True;
			self.mouseLeftClickStart(mouse);
		elif pressed_array[1]:
			self.MID_CLICK = True;
			self.mouseMidClickStart(mouse);
		elif pressed_array[2]:
			self.RIGHT_CLICK = True;
			self.mouseRightClickStart(mouse);
	# delegate onMouseMove
	def onMouseMove(self,mouse):
		pass;
	def mouseClickEnd(self,mouse):
		if self.STARTPOS == None:
			return False;
		endPos = mouse.get_pos();
		if self.LEFT_CLICK:
			self.mouseLeftClickEnd(mouse);
		elif self.MID_CLICK:
			self.mouseMidClickEnd(mouse);
		else:
			self.mouseRightClickEnd(mouse);
		self.LEFT_CLICK = False;
		self.MID_CLICK = False;
		self.RIGHT_CLICK = False;
		
		if math.sqrt((endPos[1]-self.STARTPOS[1])**2+(endPos[0]-self.STARTPOS[0])**2)> 20:
			return False;
		# print(mouse.get_pos());

	# delegate for clickevent
	def mouseLeftClickStart(self,mouse):
		print("MouseEventDelegate::mouseLeftClickStart "+str(mouse.get_pos()));
	def mouseMidClickStart(self,mouse):
		print("MouseEventDelegate::mouseMidClickStart "+str(mouse.get_pos()));
	def mouseRightClickStart(self,mouse):
		print("MouseEventDelegate::mouseRightClickStart "+str(mouse.get_pos()));
	def mouseLeftClickEnd(self,mouse):
		print("MouseEventDelegate::mouseLeftClickEnd "+str(mouse.get_pos()));
	def mouseMidClickEnd(self,mouse):
		print("MouseEventDelegate::mouseMidClickEnd "+str(mouse.get_pos()));
	def mouseRightClickEnd(self,mouse):
		print("MouseEventDelegate::mouseRightClickEnd "+str(mouse.get_pos()));