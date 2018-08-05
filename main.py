#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import GameLogicManager as GM
import Common

def main(argv):
	Common.initConstValues(argv);


	manager = GM.GameLogicManager.getManager();
	manager.initEnv();
	manager.initStaticLayout();
	manager.startMainLoop();

if __name__ == '__main__':
   main(sys.argv)