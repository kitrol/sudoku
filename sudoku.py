#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import math
import random

# def randomArray(sorceArray):
# 	tempArray=[1,2,3,4,5,6,7,8,9];
# 	random.shuffle(sorceArray);
# 	# print(tempArray);
# 	return tempArray; 
	# if arrayA gets an element also in arrayB, remove it from arrayA
def removeElements(arrayA,arrayB):
	rest = (set(list(arrayA)).difference(set(list(arrayB))));
	rest = list(rest);
	random.shuffle(rest);
	return rest;
	# return the elements both in arrayA and arrayB
def commonElements(arrayA,arrayB):
	union_set = set(arrayA).union(set(arrayB));
	# remove whole A set from union set, includes the common part
	no_arrayA_set = union_set^set(arrayA);
	# commonset 
	common = set(arrayB)^no_arrayA_set;
	return list(common);
	# careful that arrayA is longer than arrayB
def getPosibleElements(arrayA,arrayB):
	common = commonElements(arrayA,arrayB);
	rest = removeElements(arrayA,common);
	if len(common) < 3:
		common.extend(rest[:(3-len(common))]);
	random.shuffle(list(common));
	print(common);
	return common;

def checkAndFillBlank(matrix,rest,line,column):
	box_x = int(math.floor(column/3));
	box_y = int(math.floor(line/3));
	box_array = np.array(matrix[box_y*3:box_y*3+3,box_x*3:box_x*3+3]).copy();
	box_array.shape = -1;
	vertical_array = np.array(matrix[:,column]).copy();
	horizon_array = np.array(matrix[line,:]).copy();
	for rest_item in rest:
		if (rest_item in vertical_array) or (rest_item in horizon_array) or (rest_item in box_array):
			continue;
		else:
			return rest_item;
	return 0;

def initFinalBoard():
	# A   B   C
	# D   E   F
	# G   H   I
	finalBoard = np.zeros([9,9],dtype=np.uint32);
	tempArray = np.array([1,2,3,4,5,6,7,8,9]);
	random.shuffle(tempArray);
	finalBoard[0,:] = tempArray;

	shuffle_1 =  tempArray[3:];
	random.shuffle(shuffle_1);

	temp_1 = tempArray[0:3];
	temp_2 = shuffle_1[3:6];
	temp_3 = removeElements(shuffle_1,temp_2);
	random.shuffle(temp_2);
	random.shuffle(temp_3);
	finalBoard[1,0:3] = temp_2;
	finalBoard[2,0:3] = temp_3;

	# print(list(finalBoard[0,3:6]));
	# print(list(temp_2));
	rest = removeElements(removeElements(tempArray,temp_2),finalBoard[0,3:6]);
	random.shuffle(rest);

	finalBoard[1,3:6] = rest[:3];
	rest = removeElements(removeElements(tempArray,finalBoard[0,3:6]),finalBoard[1,3:6]);
	finalBoard[2,3:6] = rest[:3];

	rest = removeElements(tempArray,finalBoard[1,:6]);
	finalBoard[1,6:] = rest[:3];

	rest = removeElements(tempArray,finalBoard[2,:6]);
	finalBoard[2,6:] = rest[:3];
	# A   B   C
	###################################
	rest = removeElements(tempArray,finalBoard[:3,3]);
	finalBoard[3:6,3] = rest[:3];

	rest = removeElements(tempArray,finalBoard[3:6,3]);
	rest = removeElements(rest,finalBoard[0:3,4]);
	rest = getPosibleElements(rest,finalBoard[0:3,5]);
	finalBoard[3:6,4] = rest[:3];

	rest = removeElements(removeElements(tempArray,finalBoard[3:6,3]),finalBoard[3:6,4]);
	finalBoard[3:6,5] = rest[:3];
	# E	 
	###################################
	rest = removeElements(tempArray,finalBoard[:6,3]);
	finalBoard[6:,3] = rest[:3];

	for line in range(6,9):
		rest = removeElements(tempArray,finalBoard[:line,4]);
		fitNum = checkAndFillBlank(finalBoard,rest,line,4);
		if fitNum>0:
			finalBoard[line:,4] = fitNum;
	for line in range(6,9):
		rest = removeElements(tempArray,finalBoard[:line,5]);
		fitNum = checkAndFillBlank(finalBoard,rest,line,5);
		if fitNum>0:
			finalBoard[line:,5] = fitNum;
	#  H	
	#####################################
	for line in range(6,9):
		for column in range(0,3):
			rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[line,0:6]);
			rest = getPosibleElements(rest,finalBoard[0:3,5]);
			fitNum = checkAndFillBlank(finalBoard,rest,line,column);
			if fitNum>0:
				finalBoard[line,column] = fitNum;
	#  G
	#####################################
	# for line in range(6,9):
	# 	for column in range(6,9):
	# 		rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[line,0:6]);
	# 		fitNum = checkAndFillBlank(finalBoard,rest,line,column);
	# 		if fitNum>0:
	# 			finalBoard[line,column] = fitNum;
	#  I
	#####################################
	# for line in range(3,6):
	# 	for column in range(0,3):
	# 		rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[line,0:6]);
	# 		fitNum = checkAndFillBlank(finalBoard,rest,line,column);
	# 		if fitNum>0:
	# 			finalBoard[line,column] = fitNum;
	#  D
	#####################################
	# for line in range(3,6):
	# 	for column in range(6,9):
	# 		rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[line,0:6]);
	# 		fitNum = checkAndFillBlank(finalBoard,rest,line,column);
	# 		if fitNum>0:
	# 			finalBoard[line,column] = fitNum;
	#  F
	#####################################
	print(finalBoard);
	# print(type(finalBoard));



initFinalBoard();
