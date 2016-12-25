#-*- coding: utf-8 -*-
from __future__ import division # To forace float point division

"""
Title: Mathematical Model and Algorithm Design for Quotation Network Analysis in News Article
Author : Deokwoo Jung, Advanced Digital Science Center (ADSC), Illinois at Singapore
e-mail : deokwoo.jung@adsc.com.sg

Abstract: 
--------------------
This study present a novel mathematical model and its algorithmic design for analyzing network structure of quotations in news article. For our analysis, we use two main features, semantic similarity and article association to discover network connectivity among quotations. Our algorithm first performs a clustering algorithm using similarity matrix computed from the semantic similarity and a user-provided threshold value for quotation similarity of the same cluster. Then it computes adjacent matrix of centers of the clusters, that we refer to as exemplar, from association matrix of article association. The resultant adjacent matrix G is a MxM square matrix, where M is the number of clusters for quotations. Then our algorithm uses power graph analysis framework of graph theory which computes an N multiplicative adjacent matrix to discover reachable paths within N hops (distances). From which, our algorithm provides the degree of quotations (i.e. number of neighbor nodes). Using our well-defined mathematical model and its algorithmic implementation, we successfully implements software system demonstrating producing network analysis result from a large news article quotation sources given any user inputs of similarity threshold, the number of quotations, and the number of hops. Our software is not complexity-optimal as it give polynomial complexity for computation which could require a strong computing server with distributed commutations processing for a large number of quotations more than 1000 quotations. 

Acknowledge: This study is funded by Korea News Foundation ("한국언론진흥재단") by 10,000 USD
from Aug 1 ~ Oct 31. 2015.

"""


"""
(*) Important Notice: na_build.pyc has been implemented prior to the project of this report, which is a part of DDEA (Data Driven Energy Analytics) software that is fully and exclusively copyrighted to Dr. Deokwoo Jung during his appointment at Advanced Digital Sciences Center (ADSC). Permission to make digital or hard copies of all or part of the library for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, to republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.
"""
# newly imported
import sys
from na_config import *
import na_config as conf
from na_build import *
import na_renderer
import warnings

__author__ = "Deokwoo Jung"
__copyright__ = "Copyright 2015, Deokwoo Jung, All rights reserved."
__credits__ = ["한국언론진흥재단"]
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "deokwoo.jung@gmail.com"


if __name__ == "__main__":
    print '****************************************************************************'
    print " Start News Source Analysis for Quotations "
    print '****************************************************************************'
    warnings.filterwarnings("ignore")
    if len(sys.argv) == 4:
        conf.setMaxConnectivity(int(sys.argv[1]))
        conf.setSimilarityThreshold(float(sys.argv[2]))
        conf.setMaxNumberOfQuotationRows(int(sys.argv[3]))

    elif len(sys.argv) == 2 and sys.argv[1] == 'help':
        print "usage) python na_analysis.py N sim_thr MAX_NUM_QUO_ROWS"
        sys.exit(0)

    else:
        print "usage) python na_analysis.py N sim_thr MAX_NUM_QUO_ROWS"

        ret = raw_input('N? (default:%d)' % conf.maxConnectivity())
        try:
            conf.setMaxConnectivity(int(ret))
        except ValueError:
            pass

        ret = raw_input('sim_thr? (default:%f)' % conf.similarityThreshold())
        try:
            conf.setSimilarityThreshold(float(ret))
        except ValueError:
            pass

        ret = raw_input('MAX_NUM_QUO_ROWS? (default:%f)' % conf.maxNumberOfQuotationRows())
        try:
            conf.setMaxNumberOfQuotationRows(int(ret))
        except ValueError:
            pass


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
        

    print '----------------------------------------------'
    print 'Clustering quotaitons by Dq'
    print '----------------------------------------------'
    print 'Start clustering.... '
    # construct similarity matrix
    Dq=np.asarray(AnalMatObj.Dq)
    sim_thr=conf.similarityThreshold()
    SIMM_MAT=(np.sign(Dq-sim_thr)+1)/2
    start_time = time.time()
    #exemplars_, labels_ = cluster.affinity_propagation(SIMM_MAT,damping=0.5)
    #change cluster algorithm    
    exemplars_,labels_ =sim_cluser(Dq,sim_thresh=sim_thr)
    print("Clustering done --- %s seconds ---" % (time.time() - start_time))


    quo_cluster=\
    nt.obj({'exemplars_':exemplars_,'labels_':labels_})
    nt.saveObjectBinaryFast(quo_cluster, QUO_CLUSTER_OBJ)
    
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
        label = int(labels_[idx])
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
    r2.render(os.path.join(os.getcwd(), 'output/output.xlsx'), conf.maxConnectivity())
    print '****************************************************************************'
    print " Analysis is done, The result is stored in NLP/output/output.xlsx "
    print '****************************************************************************'