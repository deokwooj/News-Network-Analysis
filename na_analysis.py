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

# class definition : news source. 
class new_source:
    def __init__(self):
        self.id = [] # uuid 
        self.org = [] # orgnizaiton
        self.pos = [] # position
    def add(self, x):
        self.data.append(x)
     


if __name__ == "__main__":
    main()
