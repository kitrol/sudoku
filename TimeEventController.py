#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg
import traceback

class TimeEvent(object):
	def __init__(self,eventType,delayTime,target,callbackFunc,callbackData=None,repeatTime=1):
		super(TimeEvent, self).__init__();
		self.startTime_ = pg.time.get_ticks();
		self.eventType_ = eventType;
		self.delayTime_ = delayTime;
		self.target_ = target;
		self.callbackFunc_ = callbackFunc;
		self.callbackData_ = callbackData;
		# how many times should the callback be called
		self.repeatTime_ = repeatTime;
		# TimeEventController tryTriggerEvent is called every 0.1 second so the mix time unit of delay should at least equals to 0.1

		
class TimeEventController(object):
	Instance_ = None;
	def __init__(self):
		self.eventList_ = [];
		self.FailureEventList_ = [];
		###########################
		###########################
		# called by sys every 0.1s
		pg.time.set_timer(pg.USEREVENT, 100);
		###########################
		###########################
	@classmethod
	def getControler(cls):
		if TimeEventController.Instance_ == None:
			TimeEventController.Instance_ = TimeEventController();
			return TimeEventController.Instance_;
		else:
			return TimeEventController.Instance_;

	def removeFailureEvent(self):
		for event in self.FailureEventList_[:]:
			if event in self.eventList_:
				self.eventList_.remove(event);
		self.FailureEventList_ = [];

	def tryTriggerEvent(self):
		currentTime = pg.time.get_ticks();
		for event in self.eventList_:
			if (currentTime-event.startTime_)/1000>=event.delayTime_:
				try:
					event.callbackFunc_(event.callbackData_);
					if event.repeatTime_-1<=0:
						self.FailureEventList_.append(event);
					else:
						event.repeatTime_-=1;
				except Exception as e:
					traceback.print_exc();
					self.FailureEventList_.append(event);
		self.removeFailureEvent();

	def regeistEvent(self,event):
		if event not in self.eventList_:
			self.eventList_.append(event);
		print(len(self.eventList_));
	def unregistEvent(self,target,eventType=None):
		if event in self.eventList_:
			if eventType!=None:
				# remove one event for one target and one event type
				if event.target == target and event.eventType_ == eventType:
					self.eventList_.remove(oldEvent);
				else:
					# remove all event for one target
					if event.target == target:
						self.FailureEventList_.append(event);
			self.removeFailureEvent();