#-*- coding: utf-8 -*-

# this is news source analyis program. 
# read articles and discover network structure of news sources based on quataions in artticles. 

# Deokwoo Jung 's update 23 Aug. 
# modules to be imported
from __future__ import division # To forace float point division
import os
import sys
import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm
import uuid
import pylab as pl
from scipy import signal
from scipy import stats
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from multiprocessing import Pool
#from datetime import datetime
import datetime as dt
from dateutil import tz
import shlex, subprocess
import time
import itertools
import calendar
import random
from matplotlib.collections import LineCollection
import pprint

from openpyxl.workbook import Workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.cell import get_column_letter

from openpyxl import load_workbook

from extraction import *
import cPickle as pickle

from sets import Set

# Two stages :
# Stg 1. Excel files -->  Python data structure --> store binary format in hard disk as *.bin
# Stg 2. Load binary files, *.bin files into memory and performs data analytics with the loaded bin files. 
#
# TODO: define INPUT files with formatting definition
# TODO:  define output data structures after processing input files 
# TODO: import pasring module 
# TODO: parsing quation excel files. 
# TODo: define data structures after parsing

# defintion of class strutures. 
# Quotation label classfication defined by dictionary...
# Tempoary defition --> need to be checked by Dr.Park....

# Article is stroed in harddisk or DB,... 
QuoLabel={'pol':1, 'eco':2, 'tec':2,'cul':3, 'ent':3,'soc':4,'int':5, 'spo':6, 'etc':7}

TotalNum_Quotations=1000
# class definition : news source. 

# Dicitonary Definition
# Using 'set' data structure to extract a set of elements in each column of excel file. 
# Org_Name={1:'외무부', 2:'신한국당':,3:'서울대':,...}
# Job_Title={1: '변호사', 2:'사장':,3:'교수':,...};
# Function to extract sets from excel file. 


# R : no name yes org,    I : yes name yes org,    N : yes name no org,    O : org,    s : only last name
# NewsSource Type = {1:S, 2:R, 3:I, 4:N ,5:O, 6:s}

def get_excel_sets(excel_dict):
	# load excel_dict
	name_set={} # Source's name
	org_set={} # Organization affiliated. 
	pos_set={} # Position held in the organization. 
	src_set={} # explain what it is  ???
	isc_set={} # explain what it is  ???
	return org_set,pos_set,src_set,isc_set
	
class NewsSource:
	def __init__(self):
		self.id = [] # uuid 
        	self.name = [] # name_set
        	self.org = [] # org_set
		self.type=[] # check name or organization 
        	self.pos = [] # pos_set
		self.code=[] # organization code
		self.classified=[] # isclassified 

	def _str_(self):
		return self.id, self.name, self.org, self.pos, self.code

	def add(self, x):
        	self.data.append(x)

class NewsQuotation:
	def __init__(self):
        	self.gth_label = [] 	# uuid 
        	self.quo_unicode = [] 	# unicode
        	self.quo_date=[] 	# date of quotations , defined by datetime. 
        	self.quo_nouns = [] 	# position, need to be initionalized by kkd_functions. 
        	self.quo_article=get_ArticleLabel() # Article Label ...
        # many other featured to beArticleLabel added....
    # sentecne parsing functions. 
	def kkd_funcs(self, x):
        	self.data.append(x)

def excel_open():
	wb=load_workbook('./file/wholetable.xlsx')
	sheetList = wb.get_sheet_names()
	sheet = wb.get_sheet_by_name('wholetable')
	return sheet

def print_dictionary(items):
	for i in range(0, len(items)):
		if items[i] != None:
			print str(i) + " : " + items[i]

def get_excel_org():

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	dict_org={}
	org_items = set() 

	for i in range(2,row_count):
		#cell_ns=NewsSource() # create an instance of news sources
		org = sheet.cell(row=i, column=4).value   # organization

		if org=='null':
			org=None

		org_items.add(org)

	org_items = list(org_items)

	for j in range(0, len(org_items)):
		dict_org[j] = org_items[j]    # dictionary   index : organization
		#print dict_org[j]

	#print_dictionary(dict_org)

	return dict_org 


def get_excel_type():

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	dict_type={}
	count = 0

	for i in range(2,row_count):
		#cell_ns=NewsSource() # create an instance of news sources
		type_tmp = sheet.cell(row=i, column=5).value   # type
		if type_tmp == 'S':
			dict_type[str(count)] = 1 
		elif type_tmp == 'R':
			dict_type[str(count)] = 2 
		elif type_tmp == 'I':
			dict_type[str(count)] = 3 
		elif type_tmp == 'N':
			dict_type[str(count)] = 4 
		elif type_tmp == 'O':
			dict_type[str(count)] = 5 
		elif type_tmp == 's':
			dict_type[str(count)] = 6 
		#print type_tmp + " " + str(dict_type[str(count)])
		count = count + 1

	#print_dictionary(dict_type)
	count = 0
	return dict_type 


def get_excel_code():

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	dict_code={}
	count = 0

	for i in range(2,row_count):
		#cell_ns=NewsSource() # create an instance of news sources
		code_tmp = sheet.cell(row=i, column=7).value   # type
		dict_code[str(count)] = str(code_tmp) 

		#print code_tmp , dict_code[str(count)] 
		count = count + 1

	#print_dictionary(dict_classified)

	count = 0
	return dict_code



def get_excel_classified():

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	dict_classified={}
	count = 0

	for i in range(2,row_count):
		#cell_ns=NewsSource() # create an instance of news sources
		classified_tmp = sheet.cell(row=i, column=8).value   # type
		if classified_tmp == '\\N':
			dict_classified[str(count)] = 0 
		elif classified_tmp == '\\Y':
			dict_classified[str(count)] = 1 

		#print classified_tmp + " " + str(dict_classified[str(count)])
		count = count + 1

	#print_dictionary(dict_classified)

	count = 0
	return dict_classified



def get_excel_informers():

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	dict_id_name={}
	dict_org={}
	dict_pos={}

	org_items = set() 
	pos_items = set() 

	for i in range(2,row_count):
		#cell_ns=NewsSource() # create an instance of news sources
		id = sheet.cell(row=i, column=1).value   # id
		name = sheet.cell(row=i, column=3).value   # name
		org = sheet.cell(row=i, column=4).value   # organization
		pos = sheet.cell(row=i, column=6).value   # position
		dict_id_name[id] = name   # dictionary   id : name

		if org=='null':
			org=None
		if pos=='null':
			pos=None

		org_items.add(org)
		pos_items.add(pos)

	org_items = list(org_items)
	pos_items = list(pos_items)

	for j in range(0, len(org_items)):
		dict_org[j] = org_items[j]    # dictionary   index : organization
		#print dict_org[j]


	for k in range(0, len(pos_items)):
		dict_pos[k] = pos_items[k]    # dictiionary   index : position
		#print str(k) + dict_pos[k]

	print_dictionary(dict_org)
	print ""
	print_dictionary(dict_pos)
	print ""

	return dict_id_name, dict_org, dict_pos 


def informer_save():
	id_name_load = pickle.load(open("./file/dict_id_name.p","rb"))
	org_load = pickle.load(open("./file/dict_org.p","rb"))
	type_load = pickle.load(open("./file/dict_type.p","rb"))
	pos_load = pickle.load(open("./file/dict_pos.p","rb"))
	code_load = pickle.load(open("./file/dict_code.p","rb"))
	classified_load = pickle.load(open("./file/dict_classified.p","rb"))

	sheet = excel_open()
	row_count = sheet.get_highest_row()

	all_ns = []

	#id = sheet.cell(row=i, column=1).value   # id
	count = 0

	for i in range(2, row_count):
		ns_ins = NewsSource() # create an instance of news sources

		 
		id = sheet.cell(row=i, column=1).value   # id 
		org = sheet.cell(row=i, column=4).value   # org
		pos = sheet.cell(row=i, column=6).value   # pos

		code = sheet.cell(row=i, column=7).value   # organization type

		ns_ins.id = id
		ns_ins.code = code_load[str(count)]
		ns_ins.type = type_load[str(count)]
		ns_ins.classified = classified_load[str(count)]

		if org == 'null':
			org = None
		if pos == 'null':
			pos = None

		for j in range(0, len(org_load)):
			if org == org_load[j]:
				ns_ins.org = org_load.keys()[j]

		for k in range(0, len(pos_load)):
			if pos == pos_load[k]:
				ns_ins.pos = pos_load.keys()[k]
		count = count + 1
		all_ns.append(ns_ins)

	count = 0

	return all_ns

	
def get_all_NS():
	all_ns = pickle.load(open("./file/dict_informer.p","rb"))

	U=np.matrix(np.ones((len(all_ns),6)))

	for i in range(0, len(all_ns)):
		#print all_ns[i].id, all_ns[i].org, all_ns[i].pos
		a=i
		b=i+1

		U[a:b,0]=all_ns[i].id
		U[a:b,1]=all_ns[i].org
		U[a:b,2]=all_ns[i].type
		U[a:b,3]=all_ns[i].pos
		U[a:b,4]=all_ns[i].code
		U[a:b,5]=all_ns[i].classified

	print U

	return U
		


# get a vector of nones from quatations
#def get_nouns(i):
#	return None

def get_excel_nouns():
	wb=load_workbook('./file/reference.xlsx')
	sheetList = wb.get_sheet_names()
	sheet = wb.get_sheet_by_name('extraction')
	row_count = sheet.get_highest_row()

	all_cellValue=[]

	for i in range(2,row_count):
		if sheet.row_dimensions[i].visible :
			pass
		else :
			continue	

		cellValue = sheet.cell(row=i, column=3).value
		all_cellValue.append(cellValue)

	return all_cellValue 

# return artice label.
def get_ArticleLabel():
    # this body to be filled
    return None
    # to be filled...     
    

def get_all_Quo():
	all_Quo=[]
	total_quo=TotalNum_Quotations

	excel_nouns = pickle.load(open("./file/nouns.p","rb"))
	
	for i in range(0, len(excel_nouns)) :
		temp_nq = NewsQuotation() # create an instance of news quotations
        	# To be manually or automatically (preferred)...
        	temp_nq.gth_label = QuoLabel['eco'] # this is example. 
        	#temp_nq.quo_nouns=get_nouns(temp_nq.quo_unicode) # to be done...
        	temp_nq.quo_nouns = excel_nouns[i] # to be done...
        	temp_nq.quo_date = '2015/07/30'# date of quotations , defined by datetime. 
        	temp_nq.quo_article = '1' # Article Label ...

        	all_Quo.append(temp_nq)
		#print all_Quo[i].quo_nouns
    	# Fill all members and details...
    	return all_Quo
 
    
if __name__ == "__main__":

	print " running news source analysis..... "

	# excel_noun processing
	try : 
		wb = load_workbook('./file/reference.xlsx')
		sheet = wb.get_sheet_by_name('extraction')

		print " excel_noun existed"
	except :
		excel_noun()
		#print "no reference.xlsx"
	

	# nouns.p file check
	if os.path.isfile("./file/nouns.p"):
		print " nouns.p file existed" 
	else:
		try :
			excel_nouns = get_excel_nouns() 
			pickle.dump( excel_nouns, open( "./file/nouns.p", "wb" ) )
			print " now nouns.p file create " 
		except :
			print " nouns.p file make error "


	# id, org, pos dictionary file check

	if os.path.isfile("./file/dict_id_name.p") and os.path.isfile("./file/dict_org.p") and os.path.isfile("./file/dict_pos.p"):
		print " dict_id_name.p file existed " 
		print " dict_org.p file existed " 
		print " dict_pos.p file existed " 
	else:
		try :
			excel_id_name, excel_org, excel_pos = get_excel_informers() 
			pickle.dump( excel_id_name, open( "./file/dict_id_name.p", "wb" ) )
			pickle.dump( excel_org, open( "./file/dict_org.p", "wb" ) )
			pickle.dump( excel_pos, open( "./file/dict_pos.p", "wb" ) )

			print " now dict_id_name.p file create " 
			print " now dict_org.p file create " 
			print " now dict_pos.p file create " 
		except :
			print " get_excel_informers file make error "

	if os.path.isfile("./file/dict_type.p") and os.path.isfile("./file/dict_code.p") and os.path.isfile("./file/dict_classified.p") :
		print " dict_type.p file existed " 
		print " dict_code.p file existed " 
		print " dict_classified.p file existed " 
	else:
		try :
			excel_type = get_excel_type() 
			pickle.dump( excel_type, open( "./file/dict_type.p", "wb" ) )

			excel_code = get_excel_code() 
			pickle.dump( excel_code, open( "./file/dict_code.p", "wb" ) )

			excel_classified = get_excel_classified() 
			pickle.dump( excel_classified, open( "./file/dict_classified.p", "wb" ) )

			print " now dict_type.p file create " 
			print " now dict_code.p file create " 
			print " now dict_classified.p file create " 
		except :
			print " dict_type, code, classified file make error "


	if os.path.isfile("./file/dict_informer.p"):
		print " dict_informer.p file existed"

	else :
		try:
			informer_tmp = informer_save()
			pickle.dump( informer_tmp, open( "./file/dict_informer.p", "wb" ) )
		except :
			print " informer save  error"

	#excel_org = get_excel_org()
	#pickle.dump( excel_org, open( "./file/dict_org.p", "wb" ) )
	#org_load = pickle.load(open("./file/dict_org.p","rb"))
	#print org_load[1]
	#get_excel_code()
	informer_save()

	all_ns=get_all_NS()

	# Load class list of Quatation object. 
	#all_quo=get_all_Quo()
	
	#####################################################
	# Simulation test 
	# This part is for simulations
	#####################################################
	
	#S-A associatoin matrix 
	
	U=np.matrix(np.ones((5,2)))
	U[3:5,0]=0
	U[1:3,1]=0
	S=U*U.T
	pprint.pprint(S)

	
