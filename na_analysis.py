#-*- coding: utf-8 -*-

# this is news source analyis program. 
# read articles and discover network structure of news sources based on quataions in artticles. 
#
# Below a general TODO lists are suggested by deokwooj
# TODO : Put detailed comments on alll functions and variables. 
# TODO : briefly summrize all functions and global variables here below. 
# functions....
# global variables....
# TODO: change all variables and function names to more intuitive one that corresponds to contexts in use. 
# TODO: use na_config.py to set default configuration for all global constants.


# Deokwoo Jung 's update 23 Aug by jdw-2. 
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
# newly imported
from na_config import *
import na_tools as nt

# Two stages :
# Stg 1. Excel files -->  Python data structure --> store binary format in hard disk as *.bin
# Stg 2. Load binary files, *.bin files into memory and performs data analytics with the loaded bin files. 
#
#TODO: define INPUT files with formatting definition
#TODO: define output data structures after processing input files 
#TODO: import pasring module 
#TODO: parsing quation excel files. 
#TODO: define data structures after parsing

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
        return self.id, self.name, self.org, self.pos, self.code,self.classified

    def add(self, x):
            self.data.append(x)

class NewsQuotation:
    def __init__(self):
            self.gth_label = []     # uuid 
            self.quo_unicode = []     # unicode
            self.quo_date=[]     # date of quotations , defined by datetime. 
            self.quo_nouns = []     # position, need to be initionalized by kkd_functions. 
            self.quo_article=get_ArticleLabel() # Article Label ...
        # many other featured to beArticleLabel added....
    # sentecne parsing functions. 
    def kkd_funcs(self, x):
            self.data.append(x)

def load_wholetable_excel():
    #wb=load_workbook('./file/wholetable.xlsx')
    wb=load_workbook(WHOLETABLE_EXCEL)
    sheetList = wb.get_sheet_names()
    #sheet = wb.get_sheet_by_name('wholetable')
    sheet = wb.get_sheet_by_name(WHOLETABLE_SHEET)
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

    inv_src_org = {v: k for k, v in src_org.items()}
    inv_src_pos = {a: b for b, a in src_pos.items()}

    sheet = load_wholetable_excel()
    row_count = sheet.get_highest_row() 

    dict_id_name = {}
    dict_org = {}
    dict_type = {}
    dict_pos = {}
    dict_code = {}
    dict_classified = {}

    for i in range(2,row_count):
        id = sheet.cell(row=i, column=1).value   # id
        name = sheet.cell(row=i, column=3).value   # name
        org = sheet.cell(row=i, column=4).value   # organization
        type = sheet.cell(row=i, column=5).value   # organization
        pos = sheet.cell(row=i, column=6).value   # position
        code = sheet.cell(row=i, column=7).value   # organization
        classified = sheet.cell(row=i, column=8).value   # organization

        dict_id_name[id] = name   # dictionary id : name
        dict_type[id] = type   # dictionary   id : type
        dict_code[id] = code   # dictionary   id : code
        dict_classified[id] = classified   # dictionary   id : classified


        try:
	    idx_org = sorted(inv_src_org.keys()).index(org)
	    dict_org[id] = idx_org
	except ValueError:
	    idx_org = -1

	

    print_dictionary(dict_org)
    print ""
    print_dictionary(dict_pos)
    print ""

    return dict_id_name, dict_org, dict_type, dict_pos, dict_code, dict_classified 

def informer_save():
    id_name_load = pickle.load(open(DICT_ID_NAME,"rb"))
    org_load = pickle.load(open(DICT_ORG,"rb"))
    type_load = pickle.load(open(DICT_TYPE,"rb"))
    pos_load = pickle.load(open(DICT_POS,"rb"))
    code_load = pickle.load(open(DICT_CODE,"rb"))
    classified_load = pickle.load(open(DICT_CLASSIFIED,"rb"))

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
    all_ns = pickle.load(open(DICT_INFORMER,"rb"))
    #TODO: dont hardcode constant, replace 6 with constant variables or get from class functions.   
    U=np.matrix(np.ones((len(all_ns),6)))
    for i in range(0, len(all_ns)):
        #print all_ns[i].id, all_ns[i].org, all_ns[i].pos
        #TODO: it is bad to use a, b in this for loop. 
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
#    return None

def get_excel_nouns():
    #wb=load_workbook('./file/reference.xlsx')
    wb=load_workbook(REFERENCE_EXCEL)
    sheetList = wb.get_sheet_names()
    #sheet = wb.get_sheet_by_name('extraction')
    sheet = wb.get_sheet_by_name(EXTRACTION_SHEET)
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
    #excel_nouns = pickle.load(open("./file/nouns.p","rb"))
    excel_nouns = pickle.load(open(DICT_NOUNS,"rb"))
    
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
        #wb = load_workbook('./file/reference.xlsx')
        wb = load_workbook(REFERENCE_EXCEL)
        #sheet = wb.get_sheet_by_name('extraction')
        sheet = wb.get_sheet_by_name(EXTRACTION_SHEET)
        print " excel_noun existed"
    except :
        excel_noun()
        #print "no reference.xlsx"
    
    # nouns.p file check
    #if os.path.isfile("./file/nouns.p"):
    if os.path.isfile(DICT_NOUNS):
        print " nouns.p file existed" 
    else:
        try :
            excel_nouns = get_excel_nouns()  
            pickle.dump( excel_nouns, open( DICT_NOUNS, "wb" ) )
            print " now nouns.p file create " 
        except :
            print " nouns.p file make error " 

    # id, org, pos dictionary file check
    if os.path.isfile(DICT_ID_NAME) and os.path.isfile(DICT_ORG) \
    and os.path.isfile(DICT_TYPE) and os.path.isfile(DICT_POS) \
    and os.path.isfile(DICT_CODE)  and os.path.isfile(DICT_CLASSIFIED): 
        print  'Found a dictionary for news sources'
        """
        table_define.xlsx : 정보원 정의
        | infoSrc_ID                   | 정보원 ID |
        | name                         | 이름 |
        | orgName                      | 소속이름 |
        | type                         | 정보원 구분 |
        | position                     | 직함 |
        | etc_position                 | 기타 직함 정보 |
        | yearOfBirth                  | 생년 |
        | person_id(FK)                | 사전의 인물 ID |
        | code                         | 인물의 소속 분류 |
        | is_classified_paper_category | 신문 지면 정보에 의해 정보원의 분류되었는지 여부 |
        | INFOSRC_GLOBAL_ID            | 전기간
        | infosrc_id_whole    | 5 |
        | infosrc_id_day      | 2003/10/10_408 |
        | infosrc_name        | 김수행 |
        | infosrc_org         | 서울대 |
        | infosrc_type        | I |
        | infosrc_pos         | 교수 |
        | infosrc_code        | 13 |
        | infosrc_isclassified| \N |        에 걸친 UniqueID |
        
        Each column is extracted from wholetable.xlsx (정보원 자료 엑셀 파일)
        """
        
        src_name=nt.loadObjectBinaryFast(DICT_ID_NAME)
        src_org=nt.loadObjectBinaryFast(DICT_ORG)
        """ 
        type
      | S | 익명 - 소속 없는 사람 |
      | R | 익명 - 소속 있는 사람 |
      | I | 실명 개인 - 소속 있음 |
      | N | 무속속 실명 |
      | O | 조직 |
      | s | 성만 나와 있는 익명 |        
       """
       # dictionary of type
        src_type=nt.loadObjectBinaryFast(DICT_TYPE)
        # dictionary of position 
        src_pos=nt.loadObjectBinaryFast(DICT_POS)
        # dictionary of code
        src_code=nt.loadObjectBinaryFast(DICT_CODE)
        """
        is_classified_paper_category
      | Y | 본 정보원이 나온 신문지면의 분류에 의해 코딩 |
      | N | 본 정보원이 직함이나, 소속에 의해 코딩이 된 것 |
        """
        src_classifed=nt.loadObjectBinaryFast(DICT_CLASSIFIED) 
        
    else:
        try :
            print  'Save a dictionary for news sources'
            excel_id_name, excel_org, excel_type, excel_pos, excel_code, excel_classified \
            = get_excel_informers()
            nt.saveObjectBinaryFast(excel_id_name, DICT_ID_NAME )
            nt.saveObjectBinaryFast(excel_org, DICT_ORG )
            nt.saveObjectBinaryFast(excel_type, DICT_TYPE )
            nt.saveObjectBinaryFast(excel_pos,  DICT_POS )
            nt.saveObjectBinaryFast( excel_code, DICT_CODE)
            nt.saveObjectBinaryFast(excel_classified,  DICT_CLASSIFIED  )
            
        except :
            print " get_excel_informers file make error "


    # Print list dictionary for news source. 
    print '------------------------------------'    
    print ' List of names in news sources '
    print '------------------------------------'
    for key in src_name.keys(): 
        print src_name[key]
    print '------------------------------------'
    
    print '------------------------------------'    
    print ' List of organizations in news sources '
    print '------------------------------------'
    for key in src_org.keys():
        print src_org[key]
    print '------------------------------------'
   
    print '------------------------------------'    
    print ' List of positions in news sources '
    print '------------------------------------'
    for key in src_pos.keys(): 
        print src_pos[key]
    print '------------------------------------'


    if os.path.isfile(DICT_INFORMER):
        print " Found a class  list for news sources "
        # News Source Matrix        
        src_mat=nt.loadObjectBinaryFast(DICT_INFORMER)

    else :
        try:
            informer_tmp = informer_save()
            nt.saveObjectBinaryFast(informer_tmp,DICT_INFORMER) # replace with a shorter func.       
        except :
            print " informer save  error"
    
    #all_ns=get_all_NS()



    # News Article by a = {a_1 , · · · , a_l }


    

    
    # News Sources by s = {s_1 , · · · , s_m }




    # Quotations in articles  by q = {q_1 , · · · , a_n }
    


    # U_{lxm} ~ Association matrix between News Sources S and Articles A




    # V_{mxn} ~ Association matrix  between News Sources S and Quotations Q.
    
    
    
    
    # Z_{nxl}~ Association matrix  between Quotations − Articles.
    
    
    
    # Q_v = V*V' 
    
    
    
    # Q_z = Z*Z'
    
    
    
    # \hat{q}_i ~ Projection of q_i into n-dimensional Euclidian space E_n    
    
    
    # D_q ~ Distance of matrix for \hat{q}_i s
        
    
    
    # D^_q = w_d D_q + w_v* Q_v + w_z*Q_z
    
    
    
    
    
    








    # Load class list of Quatation object. 
    #all_quo=get_all_Quo()
    
    
    # TODO: Create U, V, Z matrix here, (sample is ok ) --> check for paper. 
    # note: must be done after you clean your code with complete comments , 
    
    #####################################################
    # Simulation test 

    # This part is for simulations
    #####################################################
    
    #S-A associatoin matrix 
    
    #U=np.matrix(np.ones((5,2)))
    #U[3:5,0]=0
    #U[1:3,1]=0
    #S=U*U.T
    #pprint.pprint(S)

    
