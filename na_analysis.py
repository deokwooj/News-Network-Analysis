#-*- coding: utf-8 -*-
from __future__ import division # To forace float point division

#########################################################
# Authors
#########################################################
# bla. bla...
#
#########################################################

#########################################################
# Liscence
#########################################################
# bla bla..
#
#########################################################

#########################################################
# Program Decsription
#########################################################
# this is news source analyis program. 
# read articles and discover network structure of news sources based on quataions in artticles. 
# Two stages :
# Stg 1. Excel files -->  Python data structure --> store binary format in hard disk as *.bin
# Stg 2. Load binary files, *.bin files into memory and performs data analytics with the loaded bin files. 
#
# bla bla...
#########################################################



# Deokwoo Jung 's update 23 Aug by jdw-2. 
# modules to be imported

# newly imported
from na_config import *
#from na_build import *
from na_build import *

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
 
# Return diatance matrix of Quatations
def generate_Qdist (w_param):
    # using w_param (weight coefficients for various distance matrix for Quatations 
    # w_param is given by DM's excel table ...
    return D_q


def quo_network_analysis(D_q,ns_param):
    # discover the best network structure given ns_param
    # D_q: Distance matrix for quoatations. 
    # 1. Clustering using D_q

    # 2. Applying na_param and cutoff neighbor max number of neighbor. 
    # 3. generate ns_structure = n by n binaryt matrix. 
    return ns_structutre
    

if __name__ == "__main__":
    print " running news source analysis.....version 2.56"
    NewsSrcObjs, NewsQuoObjs=na_build_main()
    
    
"""
    np.array([obj_.name for (sid, obj_) in NewsSrcObjs])
    print 'Generate News Source  '
    # News Sources by s = {s_1 , · · · , s_m }

    import pdb; pdb.set_trace()
    
    # Print list dictionary for news source. 
    print '------------------------------------'    
    print ' List of names in news sources '
    print '------------------------------------'
    listofname=[obj.name for nid,obj in NewsSrcObjs]
    for name_t in listofname:
        print name_t

    # List of names in quotations        
    names_in_ns=list(set([obj.name for nid,obj in NewsSrcObjs]))
    
    names_in_quo=list(set([obj.news_src.name for qid,obj in NewsQuoObjs]))
    
    # print all names in quotations.     
    for name_ in list(set(names_in_quo)):
                
        print name_
    

    for (qid, obj_) in NewsQuoObjs:
        print '==================================================='
        print 'Quotation ID : ', qid 
        print '=========================build_NewsQuoObjs=========================='
        obj_.whoami()
        print '********************************************************************'



        
    # constrcut news source array 
    #for key in src_name.keys(): 
    #    print src_name[key]
    #print MyPrettyPrinter().pprint(src_name)
    print '------------------------------------'


    print '--------------------------build_NewsQuoObjs----------'    
    print ' List of organizations set '
    print '------------------------------------'

    print '------------------------------------'

    print '------------------------------------'    
    print ' List of position set '
    print '------------------------------------'
    #print MyPrettyPrinter().pprint(src_pos_set)
    print '------------------------------------'

    print '------------------------------------'    
    print ' List of organizations in news sources '
    print '------------------------------------'
    #for key in src_org.keys():
    #    print src_org[key]
    #print MyPrettyPrinter().pprint(src_org)
    print '------------------------------------'

   
    print '------------------------------------'    
    print ' List of positions in news sources '
    print '------------------------------------'
    #for key in src_pos.keys(): 
    #    print src_pos[key]
    #print MyPrettyPrinter().pprint(src_pos)
    print '------------------------------------'

    print '------------------------------------'    
    print ' List of informer class in news sources '
    print '------------------------------------'
    #for key in src_pos.keys(): 
    #    print src_pos[key]


    #print MyPrettyPrinter().pprint(test)

    # News Article by a = {a_1 , · · · , a_l }
    


    # Quotations in articles  by q = {q_1 , · · · , a_n }

    # U_{lxm} ~ Association matrix between News Sources S and Articles A

    # V_{mxn} ~ Association matrix  between News Sources S and Quotations Q.
    
    # Z_{nxl}~ Association matrix  between Quotations − Articles.
    build_NewsQuoObjs
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
    """