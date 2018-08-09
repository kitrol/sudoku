#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame as pg
import math
from DestroyableNode import *


class MouseEventsDistributer(object):
	"""docstring for MouseEventsDistributer"""
	Instance_ = None;
	
	def __init__(self):
		super(MouseEventsDistributer, self).__init__();
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
			# new added delegate always on the top of the array
			# when mouse event happend first be actived
			self.delegateList_.insert(0,delegate);
	def unregistDelegate(self,oldDelegate):
		if oldDelegate in self.delegateList_:
			self.delegateList_.remove(oldDelegate);

	def OnMouseClickStart(self,mouse,pressed_array):
		for delegate in self.delegateList_:
			# if delegate.__class__.__name__ == "SideBoard":
			# 	print(delegate.rect_);
			# 	print(mouse.get_pos());
			# print("CLASS NAME "+delegate.__class__.__name__);
			if delegate.destroyed() or not hasattr(delegate,"mouseClickStart"):
				self.FailureDelegates_.append(delegate);
			else:
				if delegate.enableTouch_ and delegate.rect_.collidepoint(mouse.get_pos()):
					print("CLASS NAME "+delegate.__class__.__name__);
					delegate.mouseClickStart(mouse,pressed_array);
					if delegate.swallowTouch_:
						return;
			
	def OnMouseMove(self,mouse):
		for delegate in self.delegateList_:
			if delegate.destroyed() or not hasattr(delegate,"onMouseMove"):
				self.FailureDelegates_.append(delegate);
			elif delegate.enableTouch_ and hasattr(delegate,"STARTPOS") and delegate.STARTPOS!=(-1,-1):
				delegate.onMouseMove(mouse);
				print("CLASS NAME "+delegate.__class__.__name__);
				print(isinstance(delegate,MouseEventDelegate));
				if delegate.swallowTouch_:
					return;
		self.removeFailureDelegates();

	def OnMouseClickEnd(self,mouse):
		for delegate in self.delegateList_:
			if delegate.destroyed() or not hasattr(delegate,"mouseClickEnd"):
				self.FailureDelegates_.append(delegate);
			elif delegate.enableTouch_ and hasattr(delegate,"STARTPOS") and delegate.STARTPOS!=(-1,-1):
				delegate.mouseClickEnd(mouse);
				if delegate.swallowTouch_:
					return;
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


class MouseEventDelegate(DestroyableNode):
	"""docstring for MouseEventDelegate"""
	def __init__(self):
		super(MouseEventDelegate, self).__init__();
		self.LEFT_CLICK = False;
		self.MID_CLICK = False;
		self.RIGHT_CLICK = False;
		self.STARTPOS = (-1,-1);
		self.swallowTouch_ = True;
		self.enableTouch_ = True;
		# IMPORTANT sub class should set the enable click region before showed
		# IMPORTANT sub class should set the enable click region before showed
		# IMPORTANT sub class should set the enable click region before showed
		self.rect_ = (0,0,0,0);
		# IMPORTANT sub class should set the enable click region before showed
		# IMPORTANT sub class should set the enable click region before showed
		# IMPORTANT sub class should set the enable click region before showed
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

	def setRect(self,newRect):
		self.rect_ = pg.Rect(newRect);

	def destroy(self):
		DestroyableNode.destroy(self);
		MouseEventsDistributer.getControler().unregistDelegate(self);
		self.enableTouch_ = False;
		self.swallowTouch_ = False;
		
	# delegate onMouseMove
	def onMouseMove(self,mouse):
		pass;
	def mouseClickEnd(self,mouse):	
		if self.STARTPOS == (-1,-1):
			return False;
		endPos = mouse.get_pos();
		if self.LEFT_CLICK:
			self.mouseLeftClickEnd(mouse);
			self.LEFT_CLICK = False;
		elif self.MID_CLICK:
			self.mouseMidClickEnd(mouse);
			self.MID_CLICK = False;
		else:
			self.mouseRightClickEnd(mouse);
			self.RIGHT_CLICK = False;
		self.STARTPOS = (-1,-1);
		
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