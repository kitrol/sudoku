#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pygame as pg
import GameEventBroadcaster as GB
import TimeEventController as TC

class DestroyableNode(object):
	# base class of all destroyable node
	#
	def __init__(self):
		super(DestroyableNode, self).__init__()
		self.__isDestroyed = False;
		self.childNodes_ = [];
	# anchor = 
	# {topleft, bottomleft, topright, bottomright
	#  midtop, midleft, midbottom, midright
	#  center}
	def addChildNode(self,parentNode,childNode,pos,anchor):
		nodeRectObj = childNode.get_rect();
		setattr(nodeRectObj,anchor,pos);
		if hasattr(childNode,"rect_"):
			setattr(childNode,"rect_",nodeRectObj);
		parentNode.blit(childNode,nodeRectObj);
		self.childNodes_.append(childNode);
		
	def destroy(self):
		self.__isDestroyed = True;
		GB.GameEventBroadcaster.getControler().unregistTargetForEvent(self);
		TC.TimeEventController.getControler().unregistEvent(self);
		for item in self.childNodes_:
			if isinstance(item,DestroyableNode):
				item.destroy();

	def destroyed(self):
		return self.__isDestroyed;
