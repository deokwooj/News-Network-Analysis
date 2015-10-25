#-*- coding: utf-8 -*-
from __future__ import division # To forace float point division

"""Provides statistical analysis for news articles .

 Read articles and discover network structure of news sources based on quataions in artticles. 
 Two stages :
 Stg 1. Excel files -->  Python data structure --> store binary format in hard disk as *.bin
 Stg 2. Load binary files, *.bin files into memory and performs data analytics with the loaded bin files. 

 File dependcy is following. 
 1. na_build.py
 2. na_config.py
 3. na_const.py
 4. na_extraction.py
"""
# newly imported
from na_config import *
from na_build import *
from sklearn import cluster
from sklearn.cluster import Ward
from sklearn.cluster import KMeans
from sklearn.neighbors.kde import KernelDensity
from scipy.stats import stats 
from sklearn import cluster, covariance, manifold
import networkx as nx
from sklearn.cluster import KMeans
import na_renderer

__author__ = "Deokwoo Jung"
__copyright__ = "Copyright 2015, Deokwoo Jung, All rights reserved."
__credits__ = ["Deokwoo Jung"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deokwoo Jung"
__email__ = "deokwooj@gmail.com"
__status__ = "Prototype"

# Class for a set of matrix for quotation network computation
class AnalMat:
    def __init__(self):
        self.s = [] ;  self.a = [];   self.q = []
        self.U = [];   self.V = [];   self.Z = []
        self.Q_v= [];  self.Q_z= [];  self.Dq = []
        self.U_sparse= None;   self.V_sparse= None
        self.Z_sparse= None;   self.Q_v_sparse= None
        self.Q_z_sparse= None; self.Dq_sparse= None
    def sparsify_mat(self):
        # for sparse form
        self.U_sparse= sparse.bsr_matrix(self.U, dtype=np.int8)
        self.V_sparse= sparse.bsr_matrix(self.V, dtype=np.int8)
        self.Z_sparse= sparse.bsr_matrix(self.Z, dtype=np.int8)
        self.Q_v_sparse= sparse.bsr_matrix(self.Q_v, dtype=np.int8)
        self.Q_z_sparse= sparse.bsr_matrix(self.Q_z, dtype=np.int8)
        self.Dq_sparse= sparse.bsr_matrix(self.Dq, dtype=np.float)
        # Initialize original matrix        
        self.U=[]; self.V=[];self.Z=[]; self.Q_v=[]; self.Q_z=[]; self.Dq = []
    def densify_mat(self):
        self.U,self.V,self.Z=\
        self.U_sparse.todense(), self.V_sparse.todense(), self.Z_sparse.todense()
        # Convert sparse matrix to dense mastrix for Q_v, Q_z, Dq, D_opt
        self.Q_v, self.Q_z, self.Dq=\
        self.Q_v_sparse.todense(), self.Q_z_sparse.todense(), self.Dq_sparse.todense()
        self.U_sparse= None; self.V_sparse= None; self.Z_sparse= None
        self.Q_v_sparse= None;self.Q_z_sparse= None; self.Dq_sparse= None


def Constrct_matrix_for_network(NewsQuoObjs_):
    # Matrix for news source analysis
    AnalMatObj=AnalMat()
    # News Sources by s = {s_1 , · · · , s_m }
    s=[]
    # News Article by a = {a_1 , · · · , a_l }
    a=[]
    # Quotations in articles  by q = {q_1 , · · · , q_n }
    q=[]
    # U_{mxl} ~ Association matrix between News Sources S and Articles A
    U_idx_1=[]   
    # V_{mxn} ~ Association matrix between News Sources S and Quotations Q.
    V_idx_1=[]   
    # Z_{nxl}~ Association matrix between Quotations − Articles.
    Z_idx_1=[]   
    print '-----------------------------------------------------'
    print 'The array for News Sources, News Articles, Quotations are  s,a,q'
    print '-----------------------------------------------------'
    print 'qid : ', 
    for i,(qid,obj) in enumerate(NewsQuoObjs_):
        print qid,
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
            raise NameError('quotation_key must be unique')
        U_idx_1.append((len(s)-1,len(a)-1))
        V_idx_1.append((len(s)-1,len(q)-1)) 
        Z_idx_1.append((len(q)-1,len(a)-1)) 
    print "" 
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
    # Quotation network by News Sources
    Q_v = V.T*V
    print 'construt Qz...'
    # Quotatoin network by Articles
    Q_z = Z*Z.T
    print 'construt Dq...'
    # Build distance matrix for quotations      
    Dq=Build_Distq(NewsQuoObjs)
    AnalMatObj.s = s; AnalMatObj.a = a;  AnalMatObj.q = q
    AnalMatObj.U = U;  AnalMatObj.V = V;  AnalMatObj.Z = Z
    AnalMatObj.Q_v= Q_v; AnalMatObj.Q_z= Q_z; AnalMatObj.Dq = Dq
    # Sparsify matrix for storing
    AnalMatObj.sparsify_mat()
    nt.saveObjectBinaryFast(AnalMatObj, ANAL_MAT_OBJ)
    # Desnify matrix back and return it
    AnalMatObj.densify_mat()
    return AnalMatObj


# Return diatance matrix of Quatations
def Build_Distq(NewsQuoObjs_):
    # Compute Cosine similiarty. 
    # using w_param (weight coefficients for various distance matrix for Quatations 
    # w_param is given by DM's excel table ...
    n=len(NewsQuoObjs)    
    Distq=np.zeros((n,n))
    print '+++++++++++++++++++++++++++++++++++++++++++'
    print 'qid ', 
    for k,(qid_a, obj_a) in enumerate(NewsQuoObjs_):
        print k, 
        print '------------'
        for j,(qid_b, obj_b) in enumerate(NewsQuoObjs_):
            #print k, ': ',obj.nounvec
            noun_a=set(obj_a.nounvec.split(","))
            noun_b=set(obj_b.nounvec.split(","))
            all_nouns=list(noun_a.union(noun_b))
            #import pdb;pdb.set_trace()
            vec_a=[ 1 if d in noun_a else 0 for d in all_nouns]
            vec_b=[ 1 if d in noun_b else 0 for d in all_nouns]
            sim_val= np.dot(vec_a,vec_b) /(np.linalg.norm(vec_b)*np.linalg.norm(vec_a))
            Distq[k][j]=sim_val

    print "" 
    print '+++++++++++++++++++++++++++++++++++++++++++'
    return np.mat(Distq)

def sim_cluser(Dq,sim_thresh=0.8):
    labels_=np.inf*ones(Dq.shape[0])
    labels_id=0
    exemplars_=[]
    used_idx_set=set([])
    for k,rows in enumerate(Dq):
        idx=np.where(rows>sim_thresh)[0]
        #print update_idx, list(used_idx_set)    
        update_idx=np.array(list(set(idx)-used_idx_set))
        #print labels_
        #print k,labels_id
        if len(update_idx)==0:
            singular_idx_set=np.where(labels_==inf)[0]
            for idx_ in singular_idx_set:
                labels_[idx_]=labels_id
                exemplars_.append(idx_)
                labels_id=labels_id+1
            break
        else:
            labels_[update_idx]=labels_id
            exemplars_.append(k)
            used_idx_set=set(list(np.where(labels_<inf)[0]))
            labels_id=labels_id+1
    return  exemplars_,labels_


def compute_network(Q_z,Dq,sim_thresh=0.5):
    #W_v=0 # dont consider network by News Sources
    #W_z=0 # dont need to consider, computed by min function. 
    # below threshold 
    Dq_cut=(np.sign(Dq-sim_thresh)+1)/2
    D_opt=np.minimum(np.ones(Dq.shape),Dq_cut+Q_z)
    return D_opt

def show_graph(adjacency_matrix):
    # given an adjacency matrix use networkx and matlpotlib to plot the graph
    import networkx as nx
    import matplotlib.pyplot as plt

    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    # nx.draw(gr) # edited to include labels
    nx.draw_networkx(gr)
    # now if you decide you don't want labels because your graph
    # is too busy just do: nx.draw_networkx(G,with_labels=False)
    plt.show() 
    
    
def verify_AnalMatObj(AnalMatObj):
    # For debugging...
    tmp_a=AnalMatObj.Dq.diagonal()
    z_idx=np.where(tmp_a<10e-3)[1]
    z_qid=[NewsQuoObjs[idx_][1].quotation_key  for idx_ in z_idx ]
    #NewsQuoObjs[z_idx]
    for i,idx_ in enumerate(z_qid):
        print i, list(dict_news_info[idx_])[0][2]
    dict_news_info=nt.loadObjectBinaryFast(DICT_NEWS_INFO)
    for key_,val_ in dict_news_info.iteritems():
        if list(val_)[0][2]==None:
            print key_
            print list(val_)[0][0], ',', list(val_)[0][1]
        if val_==None:
            print key_
        if list(val_)[0][2]==None:
            print key_
    for idx_ in z_idx:
        print '---------------------------'
        print NewsQuoObjs[idx_][1].quotation_key
        print NewsQuoObjs[idx_][1].quotation
        print NewsQuoObjs[idx_][1].nounvec
        print '---------------------------'
    
    

if __name__ == "__main__":
    print " running news source analysis.....version 2.56"
    NewsSrcObjs, NewsQuoObjs=na_build_main(SRC_OBJ=False,QUO_OBJ=True, argv_print=False)
    #import pdb;pdb.set_trace(); ##

    if os.path.exists(ANAL_MAT_OBJ):
        print 'Loading ' +ANAL_MAT_OBJ
        AnalMatObj=nt.loadObjectBinaryFast(ANAL_MAT_OBJ)
        AnalMatObj.densify_mat()        
    else:
        print 'Cannot find ' +ANAL_MAT_OBJ
        print 'Construct '  +ANAL_MAT_OBJ
        AnalMatObj=Constrct_matrix_for_network(NewsQuoObjs)
        
    
    """ MaxPackCluster algorithm is the algorith developed and copyrighted by 
    Deokwoo Jung in 2014 for DDEA (Data Driven Energy Analysis) Developemtnt
    Use of MaxPackCluster algorithm will be strictly abiding to NLPNNA project only. 
    For Test max pack cluster, use test data below
    SIMM_MAT_temp=np.array([\
    [0.50 ,   0.92 ,   0.95 ,  0.12 ,  0.23], \
    [0.00 ,   0.50 ,   0.95 ,  0.32 ,  0.13],\
    [0.00 ,   0.00 ,   0.50 ,  0.50 ,  0.60],\
    [0.00 ,   0.00 ,   0.00 ,  0.50 ,  0.96],\
    [0.00 ,   0.00 ,   0.00 ,  0.00 ,  0.50]\
    ])
    SIMM_MAT=SIMM_MAT_temp+SIMM_MAT_temp.T
    DIST_MAT=1-SIMM_MAT
    """    
    """
    #import pdb; pdb.set_trace()
    num_empty_nouns=0
    for obj_ in NewsQuoObjs:
        print '-----------------------------'
        if len(obj_[1].nounvec)==0:
            print 'error'
            num_empty_nouns=num_empty_nouns+1
        else:
            print obj_[1].nounvec
    k=3;
    sort_idx=np.argsort(SIMM_MAT[k,:])[::-1][:5]
    key_quo=NewsQuoObjs[k][1].nounvec
    print key_quo
    print '-----------------------'
    for i,idx in enumerate(sort_idx):
        cmp_quo=NewsQuoObjs[idx][1].nounvec
        print i, ': ',cmp_quo, ':', SIMM_MAT[k,idx]
        
    """    
    print '----------------------------------------------'
    print 'Clustering quotaitons by Dq'
    print '----------------------------------------------'
    print 'Start clustering.... '
    # construct similarity matrix
    Dq=np.asarray(AnalMatObj.Dq)

    sim_thr=0.8
    SIMM_MAT=(np.sign(Dq-sim_thr)+1)/2
    start_time = time.time()
    #exemplars_, labels_ = cluster.affinity_propagation(SIMM_MAT,damping=0.5)
    #change cluster algorithm    
    exemplars_,labels_ =sim_cluser(Dq,sim_thresh=sim_thr)
    print("Clustering done --- %s seconds ---" % (time.time() - start_time))


    quo_cluster=\
    nt.obj({'exemplars_':exemplars_,'labels_':labels_})
    nt.saveObjectBinaryFast(quo_cluster, QUO_CLUSTER_OBJ)
    
    """    
    quo_cluster=\
    nt.obj({'exemplars_':exemplars_,'labels_':labels_,\
    'cluster_alg':CLUSTER_ALG,\
    'in_cluster_cutoff':IN_CLUSTER_SIM_CUTOFF,\
    'out_cluster_cutoff':OUT_CLUSTER_SIM_CUTOFF})
    """    
    ############################    
    # computer Intra, Inter..
    ############################    
    """
    #TODO: fill by junguk. 
    Dq_inter=[] # outside cluster
    Dq_intra=[] # inside cluster
    for i in range(SIMM_MAT.shape[0]):
        for j in range(SIMM_MAT.shape[0]):
            if i<j:
                print i,j,SIMM_MAT[i,j]+1, labels_[i],labels_[j]
    """
    ############################    
    # Construct G_q
    ############################    
    sz = len(exemplars_)
    G_q = np.zeros(shape=(sz, sz))
    for i in range(sz):
        for j in range(i+1, sz):
            e1 = exemplars_[i]
            e2 = exemplars_[j]
            if AnalMatObj.Q_z[e1, e2]:
                G_q[i, j] = 1
                G_q[j, i] = 1

    G_q = np.matrix(G_q)

    ############################    
    # Render to Excel file
    ############################    
    #import pdb;pdb.set_trace(); ##
    obj = na_renderer.Context()

    numQuotations = len(NewsQuoObjs)

    for idx in range(numQuotations):
        qobj = NewsQuoObjs[idx][1]
        label = labels_[idx]
        qid = int(qobj.quotation_key)
        print '[%d] %s' % (qid, qobj.quotation)
        obj.setQuotationText(qid, qobj.quotation)
        obj.setQuotationLabel(qid, label)
        obj.setQuotationDate(qid, qobj.date)
        obj.setQuotationArticleID(qid, qobj.article_id)

    for (idx, idx2) in enumerate(exemplars_):
        label = idx
        qobj = NewsQuoObjs[idx2][1]
        qid = int(qobj.quotation_key)
        obj.setLabelExamplar(label, qid)

    obj.setConnectivityMatrix(G_q)
    r2 = na_renderer.ExcelRenderer(obj)
    r2.render(os.path.join(os.getcwd(), 'output/output.xlsx'), 4)


    """
    q_id={0:23, 1:10, 2:39, 3:44, 4:14, 5:33, 6:21, 7:66, 8:88, 9:11}
    q_label={0:0, 1:4, 2:1, 3:2, 4:3, 5:4, 6:1, 7:2, 8:2, 9:1}
    q_exemplar={0:23, 1:39, 2:44, 3:14, 4:33}
    
    G_q = np.matrix([\
        [1, 0, 1, 0, 0],\
        [0, 1, 1, 0, 1],\
        [1, 1, 1, 1, 0],\
        [0, 0, 1, 1, 0],\
        [0, 1, 0, 0, 1]])
    """
    
    """
    quo_cluster=nt.loadObjectBinaryFast(QUO_CLUSTER_OBJ)
    for label_ in set(quo_cluster.labels_):
        quo_cluster.labels_[quo_cluster.labels_==label_]

    for label_ in set(quo_cluster.labels_):
        print label_
        #quo_cluster.labels_[quo_cluster.labels_==label_]
        a=SIMM_MAT[quo_cluster.labels_==label_,quo_cluster.labels_==label_]
        print a.shape
        
    all_set=set(range(SIMM_MAT.shape[0]))
    cluster_set=[]
    for i,col in enumerate(SIMM_MAT):
        print i, len(col)
        cluster_idx=np.where(col>0.9)[0]
        if len(cluster_idx)==0:
            break 
        #cluster_set.append(list(cluster_idx))
    """
    #import pdb;pdb.set_trace()
    
    # TODO  1. compute clusters of quotations using 
    # Clustering Algorithm 
    
    
    #D_opt=compute_network(AnalMatObj.Q_z,Dq,sim_thresh=0.5)
    

     #nt.saveObjectBinaryFast(D_opt_sparse, DUMP_OBJ)
    """
    정의
    0 같거나 매우 유사한 인용문
    1 같은 기사에 등장한 서로 다른 두 인용문
    2 서로 다른 두 기사에 모두 등장한 인용문(s1, s4)에 의해 매개된 두 기사에 등장한 모든 서로 다른 인용문
    3 서로 다른 두 인용문에 의해 매개된 서로 다른 두 기사의 인)용문
    ≥4 공통 인용문에 의해 연결되는 서로 다른 둘 이상의 기사에 의해 매개된 서로 다른 두 기사 간의 인용문
    """
    
    
    
    """
    G = nx.DiGraph(D_opt[0:1000,0:1000])
    nx.draw(G)
    
    G = nx.DiGraph(Q_z)
    nx.draw(G)
    
    import pdb; pdb.set_trace()
    
    plt.hist(Dq_distvals,arange(0,1.01,0.01))
    hist(Dq_distvals[Dq_distvals>0.0],arange(0,1.01,0.02))
    
    kde = KernelDensity(kernel='gaussian', bandwidth=0.01).fit(Dq_distvals)
    log_dens = KernelDensity(kernel='gaussian').fit(Dq_distvals).score_samples(X_plot)
    X_plot = np.linspace(Dq_distvals.min(), Dq_distvals.max(), 1000)[:, np.newaxis]
    log_dens = kde.score_samples(arange(0,1.01,0.01))
    
    ax[1, 1].fill(X_plot[:, 0], np.exp(log_dens), fc='#AAAAFF')
    ax[1, 1].text(-3.5, 0.31, "Gaussian Kernel Density")
    
    print 'Extract  and store it as exp_result_hist_1.png '
    Dopt_distvals=np.array(np.fliplr(D_opt)[np.triu_indices(D_opt.shape[0])])[0]
    Dq_distvals=np.array(np.fliplr(Dq)[np.triu_indices(Dq.shape[0])])[0]
    Qz_distvals=np.array(np.fliplr(Q_z)[np.triu_indices(Q_z.shape[0])])[0]
    Qv_distvals=np.array(np.fliplr(Q_v)[np.triu_indices(Q_v.shape[0])])[0]

    
    bin_size=[0.1,0.1,0.001,0.001]
    title_set=['(1)Co-occurrence by Article ', '(2)Co-occurrence by New Sources','(3)Sentence Similarity', 'All Combined (1)+(2)+(3)']
    for k,D_ in enumerate((Qv_distvals,Qz_distvals,Dq_distvals,Dopt_distvals)):
        plt.subplot(2,2,k+1)
        plt.hist(D_,arange(0,1.01,bin_size[k]))
        plt.ylabel('# of occurances')
        plt.xlabel('Similarity')
        plt.title(title_set[k]+',  bin size: '+str(bin_size[k]))
        plt.xlim([0,1])

    

    #edge_model = covariance.GraphLassoCV()    
    #edge_model.fit(Dq)
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