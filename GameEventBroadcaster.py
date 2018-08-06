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

GAME_EVENT = (
	"GAME_EVENT_INPUT_NUM",
	"GAME_EVENT_DEL_NUM",
	"GAME_EVENT_NUM_FULL",
	"GAME_EVENT_LEVEL_ACCOMPLISH",
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
	def envokeEvent(self,messageType,data):
		print("envokeEvent "+str(len(self.messageItems_)));
		for message in self.messageItems_:
			if message.messageType_ == messageType:
				try:
					message.func_(data);
				except Exception as e:
					traceback.print_exc();
					self.FailureMessageItems_.append(message);
		self.removeFailureMessage();	
	def regeistMessage(self,message):
		if message not in self.messageItems_:
			self.messageItems_.append(message);
	def unregistMessage(self,oldMessage):
		if oldMessage in self.messageItems_:
			self.messageItems_.remove(oldMessage);