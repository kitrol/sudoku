#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import math
import random
import operator
import os
import sys
import time
import platform
import Common

isPrintEnable = False;
def localPrint(argv):
	if isPrintEnable:
		print(argv);

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
def isCanFill(matrix,num,line,column):
	result = checkAndFillBlank(matrix,[num],line,column);
	# print("isCanFill line%d  column%d  old_num_is%d num%d result%s"%(line,column,matrix[line][column],num,str(result>0)));
	return (result>0);

def checkLegal(matrix):
	def isUnique(array,num):
		counter = 0;
		for item in array:
			if num == item:
				counter += 1;
		return (counter<=1);
	for line in range(0,9):
		for column in range(0,9):
			num = matrix[line,column];
			if num==0:
				continue;
			box_x = int(math.floor(column/3));
			box_y = int(math.floor(line/3));
			box_array = np.array(matrix[box_y*3:box_y*3+3,box_x*3:box_x*3+3]).copy();
			box_array.shape = -1;
			vertical_array = np.array(matrix[:,column]).copy();
			horizon_array = np.array(matrix[line,:]).copy();

			if isUnique(box_array,num) and isUnique(vertical_array,num) and isUnique(horizon_array,num):
				return True;
	return False;

def initFinalBoard():
	# A   B   C
	# D   E   F
	# G   H   I
	finalBoard = np.zeros([9,9],dtype=np.uint32);
	tempArray = np.array([1,2,3,4,5,6,7,8,9]);
	random.shuffle(tempArray);
	finalBoard[0,:] = tempArray;

	rest =  tempArray[3:];
	random.shuffle(rest);
	finalBoard[1,0:3] = rest[:3];
	finalBoard[2,0:3] = rest[3:6];
	# A
	rest = removeElements(removeElements(tempArray,finalBoard[0,3:6]),finalBoard[1,0:3]);
	rest = getPosibleElements(rest,finalBoard[2,0:3]);
	finalBoard[1,3:6] = rest[:3];
	rest = removeElements(removeElements(tempArray,finalBoard[0,3:6]),finalBoard[1,3:6]);
	finalBoard[2,3:6] = rest[:3];
	# if not checkLegal(finalBoard):
	# 	print("isDeadEnd DEAD END!");
	# 	return initFinalBoard();
	# B
	rest = removeElements(tempArray,finalBoard[1,0:6]);
	finalBoard[1,6:9] = rest[:3];
	rest = removeElements(tempArray,finalBoard[2,0:6]);
	finalBoard[2,6:9] = rest[:3];
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
	if not checkLegal(finalBoard):
		localPrint("isDeadEnd DEAD END ****H****!");
		return initFinalBoard();
	#####################################
	for column in range(0,3):
		rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[6,0:6]);
		fitNum = checkAndFillBlank(finalBoard,rest,6,column);
		if fitNum>0:
			finalBoard[6,column] = fitNum;

	leftSet = removeElements(tempArray,finalBoard[6,0:6]);
	counter = 0;
	while (operator.eq(leftSet,list(finalBoard[:3,6])))or(operator.eq(leftSet,list(finalBoard[:3,7])))or(operator.eq(leftSet,list(finalBoard[:3,7]))):
		if counter>20:
			localPrint("isDeadEnd DEAD END ****G****!");
			return initFinalBoard();
		for column in range(0,3):
			rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[6,0:6]);
			fitNum = checkAndFillBlank(finalBoard,rest,6,column);
			if fitNum>0:
				finalBoard[6,column] = fitNum;
		counter += 1;
	for column in range(0,3):
		rest = removeElements(removeElements(tempArray,finalBoard[:,column]),finalBoard[7,0:6]);
		rest = getPosibleElements(rest,finalBoard[8,3:6]);
		fitNum = checkAndFillBlank(finalBoard,rest,7,column);
		if fitNum>0:
			finalBoard[7,column] = fitNum;
		elif len(rest) == 0:
			localPrint("isDeadEnd DEAD END! ****G****");
			localPrint(finalBoard);
			return initFinalBoard();
		else:
			should_Num = rest[0];
			for temp_column in range(0,column):
				if isCanFill(finalBoard,should_Num,7,temp_column):
					old_num = finalBoard[7,temp_column];
					finalBoard[7,temp_column] = should_Num;
					finalBoard[7,column] = old_num;
			# for t in range(0,3):
	rest = removeElements(removeElements(tempArray,finalBoard[6,0:3]),finalBoard[7,0:3]);
	for column in range(0,3):
		fitNum = checkAndFillBlank(finalBoard,rest,8,column);
		if fitNum>0:
			rest.remove(fitNum);
			finalBoard[8,column] = fitNum;
		else:
			should_Num = rest[0];
			for temp_column in range(0,column):
				if isCanFill(finalBoard,should_Num,8,temp_column):
					old_num = finalBoard[8,temp_column];
					finalBoard[8,temp_column] = should_Num;
					finalBoard[8,column] = old_num;
	if not checkLegal(finalBoard):
		localPrint("isDeadEnd DEAD END! ****G****");
		return initFinalBoard();
	#  G
	#####################################
	for line in range(6,9):
		rest = removeElements(tempArray,finalBoard[line,0:6]);
		is_can = 0;
		counter = 0;
		# print(rest);
		while (is_can == 0) and (counter < 20):
			counter += 1;
			random.shuffle(rest);
			is_can = checkAndFillBlank(finalBoard,[rest[0]],line,6)and(checkAndFillBlank(finalBoard,[rest[1]],line,7))and(checkAndFillBlank(finalBoard,[rest[2]],line,8));
		finalBoard[line,6:9]=rest[:3];
	if not checkLegal(finalBoard):
		localPrint("isDeadEnd DEAD END! ****I****");
		return initFinalBoard();

	#  I
	#####################################
	for column in range(0,3):
		rest = removeElements(removeElements(tempArray,finalBoard[0:3,column]),finalBoard[6:9,column]);
		is_can = 0;
		counter = 0;
		# print(rest);
		while (is_can == 0) and (counter < 50):
			counter += 1;
			random.shuffle(rest);
			is_can = checkAndFillBlank(finalBoard,[rest[0]],3,column)and(checkAndFillBlank(finalBoard,[rest[1]],4,column))and(checkAndFillBlank(finalBoard,[rest[2]],5,column));
		finalBoard[3:6,column]=rest[:3];
	# #  D
	# #####################################
	tempArray = list(tempArray);
	for line in range(3,6):
		for column in range(6,9):
			fitNum = checkAndFillBlank(finalBoard,tempArray,line,column);
			if fitNum == 0:
				localPrint("isDeadEnd DEAD END! ****F****");
				try:
				    file = open(Common.initFileNameInDir(Common.WORKDIR,"failedBoard.txt"), "a");
				    file.write(str(finalBoard)+"\n\n");
				    file.close();
				except IOError:
					pass;
				return initFinalBoard();
			finalBoard[line,column] = fitNum;		
	 # F
	#####################################
	return finalBoard;

# initFinalBoard();
def main(argv):
	Common.initConstValues(argv);
	time0 = time.time();
	outputFile = Common.initFileNameInDir(Common.WORKDIR,"finalBoard.txt");
	file = open(outputFile, "w+");
	for counter in range(0,30):
		print(counter);
		file.write("Num.%d\n"%(counter));
		file.write(str(initFinalBoard()));
		file.write("\n\n");
	file.close();
	print((time.time()-time0));
if __name__ == '__main__':
   main(sys.argv)