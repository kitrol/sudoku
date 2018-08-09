#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import GameLogicManager as GM
import Common

# class test(pg.Surface):
# 	"""docstring for test"""
# 	def __init__(self, imageName):
		
# 		image = pg.image.load("/Users/junliang/Documents/sudoku/images/close.png");
# 		imageRect = image.get_rect();
# 		pg.Surface.__init__(self,(imageRect.width,imageRect.height));
# 		self.blit(image,imageRect);
# 		print(imageName);
		

# t = test("/Users/junliang/Documents/sudoku/images/close.png");



def main(argv):
	###### init common module
	Common.initConstValues(argv);
	###### start game logic
	manager = GM.GameLogicManager.getManager();
	manager.initEnv();
	manager.initStaticLayout();
	manager.initDynamicLayout();
	manager.startMainLoop();

if __name__ == '__main__':
   main(sys.argv)