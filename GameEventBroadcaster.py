#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import platform
import random
import math
import traceback
from DestroyableNode import *

GAME_EVENT = (
	"GAME_EVENT_INPUT_NUM",
	"GAME_EVENT_DEL_NUM",
	"GAME_EVENT_NUM_FULL",
	"GAME_EVENT_LEVEL_ACCOMPLISH",
	"GAME_EVENT_MISTAKE",
	"GAME_EVENT_CANCLE_SELECT_CELL",
	)
class BoundMessage:
	def __init__(self,messageType,target,func):
		self.messageType_ = messageType;
		self.target_ = target;
		self.func_ = func;

		
class GameEventBroadcaster():
	"""docstring for GameEventBroadcsater"""
	Instance_ = None;
	def __init__(self):
		self.messageItems_ = [];
		self.FailureMessageItems_ = [];
	@classmethod
	def getControler(cls):
		if GameEventBroadcaster.Instance_ == None:
			GameEventBroadcaster.Instance_ = GameEventBroadcaster();
			return GameEventBroadcaster.Instance_;
		else:
			return GameEventBroadcaster.Instance_;
	def removeFailureMessage(self):
		for message in self.FailureMessageItems_[:]:
			if message in self.messageItems_:
				self.messageItems_.remove(message);
		self.FailureMessageItems_ = [];
	def envokeEvent(self,messageType,data=None):
		for message in self.messageItems_:
			if message.target_.destroyed():
				self.FailureMessageItems_.append(message);
			elif message.messageType_ == messageType:
				try:
					if data:
						message.func_(data);
					else:
						message.func_();
				except Exception as e:
					traceback.print_exc();
					self.FailureMessageItems_.append(message);
		self.removeFailureMessage();	
	def regeistMessage(self,message):
		if message not in self.messageItems_:
			self.messageItems_.append(message);
	def unregistTargetForEvent(self,target,messageType=None):
		for message in self.messageItems_:
			if messageType != None:
				if (message.target_ == target) and (message.messageType_ == messageType) :
					self.FailureMessageItems_.append(message);
			else:
				if (message.target_ == target):
					self.FailureMessageItems_.append(message);
		self.removeFailureMessage();
					
		