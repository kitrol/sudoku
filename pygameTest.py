#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
import pygame as pg

pg.init();
display = pg.display.set_mode((600,400));
pg.display.set_caption("game test");

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit();
			sys.exit();
	pg.display.update();