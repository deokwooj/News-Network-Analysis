#-*- coding: utf-8 -*-

# this is news source analyis program. 
# read articles and discover network structure of news sources based on quataions in artticles. 

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

import pickle
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
QuoLabel={'eco':0, 'phil':1,'culture':2}

TotalNum_NewsSources=4
TotalNum_Quotations=1000
# class definition : news source. 

# Dicitonary Definition
# Using 'set' data structure to extract a set of elements in each column of excel file. 
#Org_Name={1:'외무부', 2:'신한국당':,3:'서울대':,...}
#Job_Title={1: '변호사', 2:'사장':,3:'교수':,...};
# Function to extract sets from excel file. 
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
        self.pos = [] # pos_set
        self.src=[] # ???
        self.isc=[] # ???
    def add(self, x):
        self.data.append(x)

class NewsQuotation:
    def __init__(self):
        self.gth_label = [] 	# uuid 
        self.quo_unicode = [] 	# unicode
        self.quo_date=[] 		# date of quotations , defined by datetime. 
        self.quo_nouns = [] 	# position, need to be initionalized by kkd_functions. 
        self.quo_article=get_ArticleLabel() # Article Label ...
        # many other featured to beArticleLabel added....
    # sentecne parsing functions. 
    def kkd_funcs(self, x):
        self.data.append(x)

def get_excel_informers():
	wb=load_workbook('wholetable.xlsx')
	sheetList = wb.get_sheet_names()
	sheet = wb.get_sheet_by_name('wholetable')
	row_count = sheet.get_highest_row()

	all_cellValue=[]

	for i in range(2,row_count):
		cell_ns=NewsSource() # create an instance of news sources
		cell_ns.id = str(uuid.uuid4())
		cell_ns.name = sheet.cell(row=i, column=3).value
		cell_ns.org = sheet.cell(row=i, column=4).value
		cell_ns.pos = sheet.cell(row=i, column=6).value
		
		print cell_ns.name

		all_cellValue.append(cell_ns)
	return all_cellValue


# get a vector of nones from quatations
#def get_nouns(i):
#	return None

def get_excel_nouns():
	wb=load_workbook('reference.xlsx')
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
    
    
def get_all_NS():

	all_NS=[]
	# total number of news sources 
	total_ns=TotalNum_NewsSources

	excel_informers = pickle.load(open("informers.p","rb"))
	print excel_informers[4].name
	print excel_informers[4].org
	print excel_informers[4].pos
	
	# to be filled all members and details...
	#return all_NS
	return None


def get_all_Quo():
	all_Quo=[]
	total_quo=TotalNum_Quotations

	excel_nouns = pickle.load(open("nouns.p","rb"))
	
	for i in range(0, len(excel_nouns)) :
		temp_nq = NewsQuotation() # create an instance of news quotations
        	# To be manually or automatically (preferred)...
        	temp_nq.gth_label = QuoLabel['eco'] # this is example. 
        	#temp_nq.quo_nouns=get_nouns(temp_nq.quo_unicode) # to be done...
        	temp_nq.quo_nouns = excel_nouns[i] # to be done...
        	temp_nq.quo_date = '2015/07/30'# date of quotations , defined by datetime. 
        	temp_nq.quo_article = '1' # Article Label ...

        	all_Quo.append(temp_nq)
		print all_Quo[i].quo_nouns
    	# Fill all members and details...
    	return all_Quo
 
    
if __name__ == "__main__":

	print " running news source analysis..... "

	# excel noun to binary file
	if os.path.isfile("nouns.p"):
		print " nouns-binay-file existed" 
	else:
		try :
			excel_nouns = get_excel_nouns() 
			pickle.dump( excel_nouns, open( "nouns.p", "wb" ) )
			print " now nouns-binary-file create " 
		except :
			print " nouns file make error "

	# excel informers to binary file
	if os.path.isfile("informers.p"):
		print " informers-binay-file existed " 
	else:
		try :
			excel_informers = get_excel_informers() 
			pickle.dump( excel_informers, open( "informers.p", "wb" ) )
			print " now informers-binary-file create " 
		except :
			print " informers file make error "

	# Load class list of NewsSource object. 
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