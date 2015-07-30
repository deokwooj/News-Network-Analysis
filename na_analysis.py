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


# defintion of class strutures. 
# Quotation label classfication defined by dictionary...
# Tempoary defition --> need to be checked by Dr.Park....

# Article is stroed in harddisk or DB,... 
QuoLabel={'eco':0, 'phil':1,'culture':2}

TotalNum_NewsSources=3
TotalNum_Quotations=10000
# class definition : news source. 
class NewsSource:
    def __init__(self, id, name, org, pos):
        self.id = id # uuid 
        self.name = name # name
        self.org = org # orgnizaiton
        self.pos = pos # position
    def add(self, x):
        self.data.append(x)


class NewsQuotation:
    def __init__(self):
        self.gth_label = [] # uuid 
        self.quo_unicode = [] # unicode
        self.quo_date=[] # date of quotations , defined by datetime. 
        self.quo_nouns = [] # position, need to be initionalized by kkd_functions. 
        self.quo_article=get_ArticleLabel() # Article Label ...
        # many other featured to beArticleLabel added....
    # sentecne parsing functions. 
    def kkd_funcs(self, x):
        self.data.append(x)

# get a vector of nones from quatations
def get_nouns(sentence):
    return None

# return artice label.
def get_ArticleLabel():
    # this body to be filled
    return None
    # to be filled...     
    
    
def get_all_NS():

	wb=load_workbook('reference.xlsx')
	sheetList = wb.get_sheet_names()
	sheet = wb.get_sheet_by_name(sheetList[0])
	
	all_NS=[]
	# total number of news sources 
	total_ns=TotalNum_NewsSources
	
	for i in range(2, total_ns):
		id = str(uuid.uuid4())
		name = sheet.cell(row=i, column=1).value
		org = 'test1'
		pos = 'test2'

		temp_ns=NewsSource(id, name, org, pos) # create an instance of news sources
		all_NS.append(temp_ns)
		# to be filled all members and details...
		return all_NS


def get_all_Quo():
    all_Quo=[]
    total_quo=TotalNum_Quotations
    for i in range(total_quo):
        temp_nq=NewsQuotation() # create an instance of news quotations
        all_Quo.append(temp_nq)
        # To be manually or automatically (preferred)...
        temp_nq.gth_label=QuoLabel['eco'] # this is example. 
        temp_nq.quo_nouns=get_nouns(temp_nq.quo_unicode) # to be done...
    # Fill all members and details...
    return all_Quo
 
    
if __name__ == "__main__":
    print " running news source analysis..... "
    
    # Load class list of NewsSource object. 
    all_ns=get_all_NS()
    
    # Load class list of Quatation object. 
    all_quo=get_all_Quo()
    


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

    

    
    
