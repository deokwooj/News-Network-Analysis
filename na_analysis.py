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
from sklearn import cluster
from sklearn.cluster import Ward
from sklearn.cluster import KMeans
from scipy.stats import stats 
from sklearn import cluster, covariance, manifold


# Article is stroed in harddisk or DB,... 
#QuoLabel={'pol':1, 'eco':2, 'tec':2,'cul':3, 'ent':3,'soc':4,'int':5, 'spo':6, 'etc':7}
# class definition : news source. 
# Dicitonary Definition
# Using 'set' data structure to extract a set of elements in each column of excel file. 
# Org_Name={1:'외무부', 2:'신한국당':,3:'서울대':,...}
# Job_Title={1: '변호사', 2:'사장':,3:'교수':,...};
# Function to extract sets from excel file. 

# R : no name yes org,    I : yes name yes org,    N : yes name no org,    O : org,    s : only last name
# NewsSource Type = {1:S, 2:R, 3:I, 4:N ,5:O, 6:s}

# Return diatance matrix of Quatations
def Build_Distq(NewsQuoObjs_):
    # Compute Cosine similiarty. 
    # using w_param (weight coefficients for various distance matrix for Quatations 
    # w_param is given by DM's excel table ...
    n=len(NewsQuoObjs)    
    Distq=np.zeros((n,n))
    print '+++++++++++++++++++++++++++++++++++++++++++'
    for k,(qid_a, obj_a) in enumerate(NewsQuoObjs_):
        print 'qid ', k
        print '------------'
        for j,(qid_b, obj_b) in enumerate(NewsQuoObjs_):
            try:
                #print k, ': ',obj.nounvec
                noun_a=set(obj_a.nounvec.split(","))
                noun_b=set(obj_b.nounvec.split(","))
                all_nouns=list(noun_a.union(noun_b))
                #import pdb;pdb.set_trace()
                vec_a=[ 1 if d in noun_a else 0 for d in all_nouns]
                vec_b=[ 1 if d in noun_b else 0 for d in all_nouns]
                sim_val= np.dot(vec_a,vec_b) /(np.linalg.norm(vec_b)*np.linalg.norm(vec_a))
                Distq[k][j]=sim_val
            except:
                Distq[k][j]=0
    print '+++++++++++++++++++++++++++++++++++++++++++'
    return np.mat(Distq)


if __name__ == "__main__":
    print " running news source analysis.....version 2.56"
    NewsSrcObjs, NewsQuoObjs=na_build_main(SRC_OBJ=False,QUO_OBJ=True, argv_print=False)
    # Note that NewsSrcObjc are used only for lookup reference. 
    # It contains 102878 distinctive number of news sources which is way too much 
    # for current number of news sources in NewsQuoObjs 
    
    # We decided not to use NewsSrcObjs due to too many ambiguous names.
    #names_in_ns=[obj.name for nid,obj in NewsSrcObjs]
    # 9x duplicated names.     
    #len(names_in_ns) =903440
    #len(set(names_in_ns))=102878 
    
    # Use only NewsQuoObjs
    #names_in_quo=[obj.news_src.name for qid,obj in NewsQuoObjs]
    # 2x duplicated names    
    # len(names_in_quo)=2522
    # len(set(names_in_quo)) =1223
    
    
    # Create array of News Sources
    # News Sources by s = {s_1 , · · · , s_m }
    #s=np.array([name_ for name_ in set(names_in_quo)])
        
    # News Article by a = {a_1 , · · · , a_l }
    #articles_in_quo=[obj.article_id for qid,obj in NewsQuoObjs]
    
    # Quotations in articles  by q = {q_1 , · · · , q_n }
    
    # News Sources by s = {s_1 , · · · , s_m }    
    s=[]
    # News Article by a = {a_1 , · · · , a_l }
    a=[]
    # Quotations in articles  by q = {q_1 , · · · , q_n }
    q=[]
    # U_{mxl} ~ Association matrix between News Sources S and Articles A
    U_idx_1=[]   
    # V_{mxn} ~ Association matrix  between News Sources S and Quotations Q.
    V_idx_1=[]   
    # Z_{nxl}~ Association matrix  between Quotations − Articles.
    Z_idx_1=[]   
    print '-----------------------------------------------------'
    print 'The array for News Sources, News Articles, Quotations are  s,a,q'
    print '-----------------------------------------------------'
    for i,(qid,obj) in enumerate(NewsQuoObjs):
        print 'qid : '+ str(qid)
        name_=obj.news_src.name
        article_=obj.article_id
        quotation_=obj.quotation_key
        if name_ not in s:
            s.append(name_)
        if article_ not in a:
            a.append(article_)
        if quotation_ not in q:
            q.append(quotation_)
        else:
            raise NameError('quotation_key must be uniqBuild_Distque')
        U_idx_1.append((len(s)-1,len(a)-1))
        V_idx_1.append((len(s)-1,len(q)-1)) 
        Z_idx_1.append((len(q)-1,len(a)-1)) 
    print '-----------------------------------------------------'
        
    m,l,n =len(s), len(a),len(q)
    print 'The length of s,a,q array are ',m,l,n
    U,V,Z=np.zeros((m,l)),np.zeros((m,n)), np.zeros((n,l))        
    print 'The shape of U,V,Z matrix are ', U.shape,V.shape,Z.shape
    
    for row,col in U_idx_1:
        U[row,col]=1
    for row,col in V_idx_1:
        V[row,col]=1
    for row,col in Z_idx_1:
        Z[row,col]=1
        
    # Convert nparray to matrix
    U,V,Z=np.mat(U),np.mat(V),np.mat(Z)
    print 'construt Qv...'
    Q_v = V.T*V
    print 'construt Qz...'
    Q_z = Z*Z.T
    print 'construt Dq...'
    Dq=Build_Distq(NewsQuoObjs)
    
    D_opt=(Q_v+Q_z+Dq)/3
    
    
    print 'Extract  and store it as exp_result_hist_1.png '
    Dopt_distvals=np.array(np.fliplr(D_opt)[np.triu_indices(D_opt.shape[0])])[0]
    Dq_distvals=np.array(np.fliplr(Dq)[np.triu_indices(Dq.shape[0])])[0]
    Qz_distvals=np.array(np.fliplr(Q_z)[np.triu_indices(Q_z.shape[0])])[0]
    Qv_distvals=np.array(np.fliplr(Q_v)[np.triu_indices(Q_v.shape[0])])[0]
    
    bin_size=[0.1,0.1,0.005,0.005]
    title_set=['(1)Co-occurrence by Article ', '(2)Co-occurrence by New Sources','(3)Sentence Similarity', 'All Combined (1)+(2)+(3)']
    for k,D_ in enumerate((Qv_distvals,Qz_distvals,Dq_distvals,Dopt_distvals)):
        plt.subplot(2,2,k+1)
        plt.hist(D_,arange(0,1.01,bin_size[k]))
        plt.ylabel('# of occurances')
        plt.xlabel('Similarity')
        plt.title(title_set[k]+',  bin size: '+str(bin_size[k]))
        plt.xlim([0,1])

    

    """"    
    edge_model = covariance.GraphLassoCV()    
    X=Dq
    edge_model.fit(X)
    aff_exemplars, aff_labels = cluster.affinity_propagation(Dq,damping=0.5)
    """

   
    """        
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