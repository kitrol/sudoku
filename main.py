#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import GameLogicManager as GM

def main(argv):
	worktDir = os.path.dirname(argv[0]);
	manager = GM.GameLogicManager.getManager();
	manager.initEnv(worktDir);
	manager.initStaticLayout();
	manager.startMainLoop();

if __name__ == '__main__':
   main(sys.argv)