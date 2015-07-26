# this is news source analyis program. 
# read articles and discover network structure of news sources based on quataions in artticles. 

# modules to be imported
from __future__ import division # To forace float point division
import os
import sys
import numpy as np
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

# defintion of class strutures. 
# Quation label classfication defined by dictionary...
# Tempoary defition --> need to be checked by Dr.Park....

# Article is stroed in harddisk or DB,... 
QuaLabel={'eco':0, 'phil':1,'culture'2}

# class definition : news source. 
class NewsSource:
    def __init__(self):
        self.id = [] # uuid 
        self.org = [] # orgnizaiton
        self.pos = [] # position
    def add(self, x):
        self.data.append(x)


class NewsQuation:
    def __init__(self):
        self.gth_label = [] # uuid 
        self.qua_unicode = [] # unicode
        self.qua_nouns = [] # position, need to be initionalized by kkd_functions. 
        self.qua_artile=get_ArticleLabel() # Article Label ...
        # many other featured to beArticleLabel added....
    # sentecne parsing functions. 
    def kkd_funcs(self, x):
        self.data.append(x)
# to be done...     
def get_all_NS():
    all_NS=[]
    total_ns=100
    for i in range(total_ns):
        all_NS.append(NewsSource())
    # Fill all members and details...
    retrun all_NS    

def get_all_Qua():
    all_Qua=[]
    total_quo=10000
    for i in range(total_qua):
        all_NS.append(NewsQuation()qua_)
        # To be manually or automatically (preferred)...
        all_NS[i].gth_label=QuaLabel['eco'] # this is example. 
        all_NS[i].qua_nouns()  # to be done...
    # Fill all members and details...
    return all_Quo
    
if __name__ == "__main__":
    print " running news source analysis..... "
    
    # Load class list of NewsSource object. 
    all_ns=get_all_NS()
    all_qua=get_all_Qua()
    

    
    
    
    
