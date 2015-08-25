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
import sys, traceback
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
        self.i_type=[] # check name or organization 
        self.pos = [] # pos_set
        self.code=[] # organization code
        self.classified=[] # isclassified 

    def _str_(self):
        return self.id, self.name, self.org, self.i_type, self.pos, self.code,self.classified

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

# for print key value
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):
        if isinstance(_object, unicode):
            return "'%s'" % _object.encode('utf8'), True, False
        elif isinstance(_object, str):
            _object = unicode(_object,'utf8')
            return "'%s'" % _object.encode('utf8'), True, False
        return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)


def load_wholetable_excel():
    #wb=load_workbook('./file/wholetable.xlsx')
    wb=load_workbook(WHOLETABLE_EXCEL)
    sheetList = wb.get_sheet_names()
    #sheet = wb.get_sheet_by_name('wholetable')
    sheet = wb.get_sheet_by_name(WHOLETABLE_SHEET)
    return sheet


def org_set_dict():

    sheet = load_wholetable_excel()
    row_count = sheet.get_highest_row()

    dict_org_set={}
    org_items = set()

    for i in range(2,row_count):
        org = sheet.cell(row=i, column=4).value   # organization
        org_items.add(org)

    org_items = list(org_items)

    for j in range(0, len(org_items)):
        dict_org_set[j] = org_items[j]    # dictionary   index : organization
        #print dict_org_set[j]
        #print_dictionary(dict_org_set)

    return dict_org_set

def pos_set_dict():

    sheet = load_wholetable_excel()
    row_count = sheet.get_highest_row()

    dict_pos_set={}
    pos_items = set()

    for i in range(2,row_count):
        pos = sheet.cell(row=i, column=6).value   # 
        pos_items.add(pos)

    pos_items = list(pos_items)

    for j in range(0, len(pos_items)):
        dict_pos_set[j] = pos_items[j]    # dictionary   index : position 
        #print dict_org_set[j]
    #print_dictionary(dict_org_set)

    return dict_pos_set


def get_excel_type(type):
    if type == 'S':
        re_type = 1
    elif type == 'R':
        re_type = 2 
    elif type == 'I':
        re_type = 3
    elif type == 'N':
        re_type = 4
    elif type == 'O':
        re_type = 5
    elif type == 's':
        re_type = 6
    return re_type 


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



def get_excel_classified(classified_tmp):


    if classified_tmp == '\\N':
        re_classified = 0 
    elif classified_tmp == '\\Y':
        re_classified= 1 

    #print classified_tmp + " " + str(dict_classified[str(count)])

    #print_dictionary(dict_classified)

    return re_classified 



def get_excel_informers():

<<<<<<< HEAD
    src_org_set = nt.loadObjectBinaryFast(DICT_ORG_SET)
    src_pos_set = nt.loadObjectBinaryFast(DICT_POS_SET)

    inv_src_org_set = {v: k for k, v in src_org_set.items()}
    inv_src_pos_set = {a: b for b, a in src_pos_set.items()}
=======
    inv_src_org = {v: k for k, v in src_org.items()}
    inv_src_pos = {a: b for b, a in src_pos.items()}
>>>>>>> origin/master

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
        i_type = sheet.cell(row=i, column=5).value   # organization
        pos = sheet.cell(row=i, column=6).value   # position
        code = sheet.cell(row=i, column=7).value   # organization
        classified = sheet.cell(row=i, column=8).value   # organization

        dict_id_name[id] = name   # dictionary id : name
        dict_type[id] = get_excel_type(i_type)   # dictionary   id : type
        dict_code[id] = code   # dictionary   id : code
<<<<<<< HEAD
        dict_classified[id] = get_excel_classified(classified)   # dictionary   id : classified
=======
        dict_classified[id] = classified   # dictionary   id : classified

>>>>>>> origin/master

        try:
	    idx_org = sorted(inv_src_org.keys()).index(org)
	    dict_org[id] = idx_org
	except ValueError:
	    idx_org = -1

<<<<<<< HEAD
        try:
	    idx_org = inv_src_org_set.keys().index(org)
	    dict_org[id] = idx_org
	    print dict_org[id]
	except ValueError:
	    idx_org = -1
=======
	
>>>>>>> origin/master

        try:
	    idx_pos = inv_src_pos_set.keys().index(pos)
	    dict_pos[id] = idx_pos
	except ValueError:
	    idx_pos = -1

    return dict_id_name, dict_org, dict_type, dict_pos, dict_code, dict_classified 


def informer_class_dict():

    all_ns = []

    for i in range(0, len(src_name)):
        ns_ins = NewsSource() # create an instance of news sources

        #ns_ins.id = src_name.keys.index[i] 
        #ns_ins.id = src.org.values()[i] 
        ns_ins.id = i 
        ns_ins.org = src_org.values()[i] 
        ns_ins.code = src_code.values()[i] 
        ns_ins.pos = src_pos.values()[i]
        ns_ins.i_type = src_type.values()[i] 
        ns_ins.classified = src_classified.values()[i]

        all_ns.append(ns_ins)

    return all_ns

    
def get_all_NS():
    #all_ns = pickle.load(open(DICT_INFORMER,"rb"))
    #TODO: dont hardcode constant, replace 6 with constant variables or get from class functions.   
    U=np.matrix(np.ones((len(src_mat),6)))

    for i in range(0, len(src_mat)):
        #print all_ns[i].id, all_ns[i].org, all_ns[i].pos
        #TODO: it is bad to use a, b in this for loop. 
        a=i
        b=i+1

        U[a:b,0]=src_mat[i].id
        U[a:b,1]=src_mat[i].org
        U[a:b,2]=src_mat[i].i_type
        U[a:b,3]=src_mat[i].pos
        U[a:b,4]=src_mat[i].code
        U[a:b,5]=src_mat[i].classified

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

        # organization set dict
        src_org_set=nt.loadObjectBinaryFast(DICT_ORG_SET)
        # position set dict
        src_pos_set=nt.loadObjectBinaryFast(DICT_POS_SET)

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
        src_classified=nt.loadObjectBinaryFast(DICT_CLASSIFIED) 
        
    else:
        try :
            print  'Save a dictionary for news sources'

            # organization set()
            org_set = org_set_dict()
            nt.saveObjectBinaryFast(org_set, DICT_ORG_SET )

            # position set()
            pos_set = pos_set_dict()
            nt.saveObjectBinaryFast(pos_set, DICT_POS_SET )

            excel_id_name, excel_org, excel_type, excel_pos, excel_code, excel_classified \
            = get_excel_informers()
            nt.saveObjectBinaryFast(excel_id_name, DICT_ID_NAME )
            nt.saveObjectBinaryFast(excel_org, DICT_ORG )
            nt.saveObjectBinaryFast(excel_type, DICT_TYPE )
            nt.saveObjectBinaryFast(excel_pos,  DICT_POS )
            nt.saveObjectBinaryFast(excel_code, DICT_CODE)
            nt.saveObjectBinaryFast(excel_classified,  DICT_CLASSIFIED  )
            
        except :
	    traceback.print_exc()
            print " get_excel_informers file make error "


    get_excel_informers()
    # Print list dictionary for news source. 
    print '------------------------------------'    
    print ' List of names in news sources '
    print '------------------------------------'
    #for key in src_name.keys(): 
    #    print src_name[key]
    print MyPrettyPrinter().pprint(src_name)
    print '------------------------------------'


    print '------------------------------------'    
    print ' List of organizations set '
    print '------------------------------------'
    print MyPrettyPrinter().pprint(src_org_set)
    print '------------------------------------'

    print '------------------------------------'    
    print ' List of position set '
    print '------------------------------------'
    print MyPrettyPrinter().pprint(src_pos_set)
    print '------------------------------------'

    print '------------------------------------'    
    print ' List of organizations in news sources '
    print '------------------------------------'
    #for key in src_org.keys():
    #    print src_org[key]
    print MyPrettyPrinter().pprint(src_org)
    print '------------------------------------'
   
    print '------------------------------------'    
    print ' List of positions in news sources '
    print '------------------------------------'
    #for key in src_pos.keys(): 
    #    print src_pos[key]
    print MyPrettyPrinter().pprint(src_pos)
    print '------------------------------------'

    print '------------------------------------'    
    print ' List of informer class in news sources '
    print '------------------------------------'
    #for key in src_pos.keys(): 
    #    print src_pos[key]


    if os.path.isfile(DICT_INFORMER):
        print " Found a class  list for news sources "
        # News Source Matrix        
        src_mat=nt.loadObjectBinaryFast(DICT_INFORMER)

    else :
        try:
            informer_tmp = informer_class_dict()
            nt.saveObjectBinaryFast(informer_tmp,DICT_INFORMER) # replace with a shorter func.       
        except :
	    traceback.print_exc()
            print " informer save  error"
    

    all_ns=get_all_NS()



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

    
