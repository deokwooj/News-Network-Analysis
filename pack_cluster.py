# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 16:34:54 2014

@author: deokwooj
"""
from __future__ import division # To forace float point division
import numpy as np
from sklearn import cluster
from sklearn.cluster import Ward
from sklearn.cluster import KMeans
import time

__author__ = "Deokwoo Jung"
__copyright__ = "Copyright 2014, Deokwoo Jung, All rights reserved."
__credits__ = ["Deokwoo Jung"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deokwoo Jung"
__email__ = "deokwooj@gmail.com"
__status__ = "Development"

 
def pair_in_idx(a,b=[],FLATTEN=True):
    pair_set=[]
    if len(b)==0:
        for idx1 in range(len(a)):
            for idx2 in range(idx1+1,len(a)):
                if FLATTEN==True:
                    if (isinstance(a[idx1],list)==True) and (isinstance(a[idx2],list)==True):
                        pair_set.append([a[idx1]+a[idx2]][0])
                    elif isinstance(a[idx1],list)==True and isinstance(a[idx2],list)==False:
                        pair_set.append([list([a[idx2]])+a[idx1]][0])
                    elif isinstance(a[idx1],list)==False and isinstance(a[idx2],list)==True:
                        pair_set.append([a[idx2]+list([a[idx1]])][0])
                    else:
                        pair_set.append([a[idx1],a[idx2]])
                else:
                    pair_set.append([a[idx1],a[idx2]])
    else:
        for idx1 in a:
            for idx2 in b:
                if FLATTEN==True:
                    if (isinstance(idx1,list)==True) and (isinstance(idx2,list)==True):
                        pair_set.append([idx1+idx2][0])
                    elif isinstance(idx1,list)==True and isinstance(idx2,list)==False:
                        pair_set.append([idx1+list([idx2])][0])
                    elif isinstance(idx1,list)==False and isinstance(idx2,list)==True:
                        pair_set.append([list([idx1])+idx2][0])
                    else:
                        pair_set.append([idx1,idx2])
                else:
                    pair_set.append([idx1,idx2])
    return pair_set


def max_diff_dist_idx(dist_mat,min_dist,max_dist):
    num_nodes=dist_mat.shape[0]
    dist_diff=[]
    max_diff=-1
    max_diff_row=0
    max_diff_label=[]
    max_cluster_idx=[]
    for i,dist_vals in enumerate(dist_mat):
        # exclude its own distance
        idx_set=np.r_[np.r_[0:i:1],np.r_[i+1:num_nodes:1]]
        #print i,'th row k-mean cluster'    
        temp=dist_vals[idx_set]
        if np.min(temp)>max_dist:
            exemplar_idx=i
            max_cluster_idx=i
            #import pdb;pdb.set_trace()
            return exemplar_idx,max_cluster_idx
        
        ########################################
        # K-mean
        #_,label,_=cluster.k_means(temp[:,None],2)      
        # Herichical Binary Clutering
        ward = Ward(n_clusters=2).fit(temp[:,None])
        label=ward.labels_
        #kmean=KMeans(n_clusters=2).fit(temp[:,None])
        #label=kmean.labels_
        
        # max is default
        centroid=np.zeros(2)
        #import pdb;pdb.set_trace()
        centroid[0]=np.max(temp[label==0])
        centroid[1]=np.max(temp[label==1])
        #idx0=idx_set[np.nonzero(label==0)]
        #idx1=idx_set[np.nonzero(label==1)]
        #dist01=np.round([dist_mat[v0,v1] for v0 in idx0 for v1 in idx1],2)
        #num_min_dist_violation=len(np.nonzero(dist01<min_dist)[0])
        ########################################
        temp_1=abs(centroid[0]-centroid[1])
        cent_diff=centroid[0]-centroid[1]
        dist_diff.append(abs(cent_diff))
        if max_diff< temp_1:
        #if (max_diff< temp_1) and (num_min_dist_violation==0):
            max_idx_set=idx_set
            max_diff_row=i
            max_diff=temp_1
            max_diff_label=label
            max_cent_diff=cent_diff

    #import pdb;pdb.set_trace()
    cur_cent_idx=set([])
    if max_cent_diff>0:
        cur_cent_idx=cur_cent_idx| set(np.nonzero(max_diff_label==1)[0])
    else:
        cur_cent_idx=cur_cent_idx| set(np.nonzero(max_diff_label==0)[0])
    max_cluster_idx=list(set(max_idx_set[list(cur_cent_idx)]) |set([max_diff_row]))
    exemplar_idx=max_diff_row
    
    return exemplar_idx,max_cluster_idx

def signle_let_cluster_idx(dist_mat,max_dist):
    print max_dist
    num_nodes=dist_mat.shape[0]
    nodes_all_alone=[]
    exemplar_idx=[];
    max_cluster_idx=[]
    for i,dist_vals in enumerate(dist_mat):
        # exclude its own distance
        idx_set=np.r_[np.r_[0:i:1],np.r_[i+1:num_nodes:1]]
        temp=dist_vals[idx_set]
        #import pdb;pdb.set_trace()
        num_nodes_away_more_than_max_dist=len(np.nonzero(temp>max_dist)[0])
        #print temp
        if  num_nodes_away_more_than_max_dist==num_nodes-1:
            print '-----------------------------------------------------------'
            print i,'th node check'
            print '*** all nodes are away beyond max_dist **'
            nodes_all_alone.append(i)
            #exemplar_idx.append([i])
            exemplar_idx.append(i)
            #max_cluster_idx.append([i])
            max_cluster_idx.append(i)
    return exemplar_idx,max_cluster_idx
    

def udiag_min(a):
    return min([min(a[i,i+1:]) for i in range(a.shape[0]-1)])

def udiag_max(a):
    return max([max(a[i,i+1:]) for i in range(a.shape[0]-1)])
    
def udiag_avg(a):
    return sum([sum(a[i,i+1:]) for i in range(a.shape[0]-1)])\
    /((a.shape[0]-0)*(a.shape[0]-1)/2)


def max_pack_cluster(DIST_MAT,min_dist=0.3,max_dist=1.0):
    # minium distance for clusters set by max_dist=1.0 , min_dist=0.3
    # Initionalize
    num_nodes=DIST_MAT.shape[0]
    label=np.inf*np.ones(num_nodes)
    label_num=0
    remain_index=np.arange(num_nodes)
    dist_mat=DIST_MAT.copy()
    exemplar_list=[]
    print' pack clustring '
    while (dist_mat.shape[0]>2):
        #import pdb;pdb.set_trace();
        print 'dist mat size: ', dist_mat.shape
        if udiag_min(dist_mat)>max_dist:
            print 'all samples are seperated further than max_dist'
            print 'remaining samples will be individual clusters' 
            # Assign different labels to all raminig samples
            inf_idx=np.nonzero(label==np.inf)[0]
            for r in inf_idx:
                exemplar_list.append(int(r))
            #label[inf_idx]=label_num+np.arange(len(inf_idx))
            label[inf_idx]=np.int_(label_num+np.arange(len(inf_idx)))
            #import pdb;pdb.set_trace()
            break
            
        elif udiag_max(dist_mat)<min_dist:
            # Assign the same label to all raminig samples
            print 'all samples are seperated within min_dist'
            print 'remaining samples will be the same' 
            inf_idx=np.nonzero(label==np.inf)[0]
            exemplar_list.append(int(inf_idx[0]))
            label[inf_idx]=int(label_num)
            #import pdb;pdb.set_trace()
            break
        else:
            exemplar_idx,max_cluster_idx=max_diff_dist_idx(dist_mat,min_dist,max_dist)
            dcluster_idx=remain_index[max_cluster_idx]
            exemplar_list.append(np.int_(remain_index[exemplar_idx]))
            #import pdb;pdb.set_trace()
            # Update dist_mat and remain_idx
            dist_mat=np.delete(dist_mat, max_cluster_idx, axis=0)
            dist_mat=np.delete(dist_mat, max_cluster_idx, axis=1)    
            remain_index=np.delete(remain_index,max_cluster_idx, axis=0)
            # Adding label info
            label[dcluster_idx]=label_num;label_num+=1
            print 'dist_mat.max()=', dist_mat.max()

    unassigned_idx=np.nonzero(label==np.inf)[0]
    if len(unassigned_idx)>0:
        label[unassigned_idx]=label_num+np.arange(len(unassigned_idx))
        exemplar_list=exemplar_list+list(unassigned_idx)
        
        #raise NameError('There exist the unassigned: '+str(unassigned_idx))
    intra_err_cnt, inter_err_cnt=check_bounded_distance_constraint_condition(DIST_MAT,label,min_dist,max_dist)        
    return np.int_(exemplar_list),np.int_(label)

def compute_cluster_err(DIST_MAT,m_labels):
    num_clusters=int(m_labels.max())+1
    # Compute Intra-Cluster Distance
    c_wgt_set=np.zeros(num_clusters)
    c_dist_w_min=np.zeros(num_clusters)
    c_dist_w_max=np.zeros(num_clusters) 
    c_dist_w_avg=np.zeros(num_clusters)
    for i in range(num_clusters):
        c_idx=np.nonzero(m_labels==i)[0]
        c_wgt=c_idx.shape[0]/DIST_MAT.shape[0]
        c_wgt_set[i]=c_wgt
        if c_idx.shape[0]>1:
            # sample weight of the cluster
            c_dist_w_min[i]=udiag_min(DIST_MAT[c_idx,:][:,c_idx])
            c_dist_w_max[i]=udiag_max(DIST_MAT[c_idx,:][:,c_idx])
            c_dist_w_avg[i]=udiag_avg(DIST_MAT[c_idx,:][:,c_idx])
        else:
            c_dist_w_min[i]=0
            c_dist_w_max[i]=0
            c_dist_w_avg[i]=0
    intra_dist_min=sum(c_dist_w_min*c_wgt_set)
    intra_dist_avg=sum(c_dist_w_avg*c_wgt_set)
    intra_dist_max=sum(c_dist_w_max*c_wgt_set)
    intra_dist_bnd=np.array([intra_dist_min, intra_dist_avg,intra_dist_max])
    
    inter_dist=[]
    # Compute Inter-Cluster Distance
    if num_clusters>1:
        for i in range(num_clusters-1):
            for j in range(i+1,num_clusters):
                i_idx=np.nonzero(m_labels==i)[0]
                j_idx=np.nonzero(m_labels==j)[0]
                temp_mat=DIST_MAT[i_idx,:][:,j_idx]
                inter_dist.append(temp_mat.min())
    
        inter_dist=np.array(inter_dist)
        inter_dist_bnd=np.array([inter_dist.min(), inter_dist.mean(),inter_dist.max()])
        validity=intra_dist_avg/inter_dist.min()
    else:
        validity=0
        inter_dist_bnd=0
        
    return validity,intra_dist_bnd,inter_dist_bnd
    
    
def show_clusters(exemplars,labels,input_names):
    n_labels = labels.max()
    for i in range(n_labels + 1):
        print('Cluster %i: %s' % ((i + 1), ', '.join(input_names[labels == i])))
    

def plot_label(X_val,X_name,labels,exemplar,label_idx_set):
    num_label=len(label_idx_set)
    if num_label>15:
        fsize=6
    elif num_label>10:
        fsize=8
    elif num_label>5:
        fsize=10
    else:
        fsize=12
        
    for k,label_idx in enumerate(label_idx_set):
        fig = plt.figure('Label '+str(label_idx)+' Measurements')
        fig.suptitle('Label '+str(label_idx)+' Measurements',fontsize=fsize)
        idx=np.nonzero(labels==label_idx)[0]
        exemplar_idx=exemplar[label_idx]
        num_col=int(np.ceil(np.sqrt(len(idx))))
        num_row=num_col
        for k,i in enumerate(idx):    
            ax=plt.subplot(num_col,num_row,k+1)
            plt.plot(X_val[:,i])
            if exemplar_idx==i:
                plt.title('**'+X_name[i]+'**',fontsize=fsize)
            else:
                plt.title(X_name[i],fontsize=fsize)
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(fsize) 
            if (k<num_col*(num_row-1)):
                for tick in ax.xaxis.get_major_ticks():
                    ax.set_xticklabels( () )
        plt.get_current_fig_manager().window.showMaximized()


def check_bounded_distance_constraint_condition(dist_mat,labels,min_dist,max_dist):
    intra_err_cnt=0
    num_clusters=int(labels.max()+1)
    print '------------------------------------------------------------------------------------------'
    print 'Intra-Cluster distance check.....'        
    print 'Condition: inter-cluster distance is upper-bounded by',round(max_dist,2)        
    print '------------------------------------------------------------------------------------------'
    for i in range(num_clusters):
        idx_set=np.nonzero(labels==(i))[0]
        #print '----------------------------------------------------------'
        #print i,'th cluster: ',idx_set
        for idx_pair in pair_in_idx(idx_set):
            #print idx_pair, 'dist-',round(dist_mat[idx_pair[0],idx_pair[1]],2)
            dist_val_=dist_mat[idx_pair[0],idx_pair[1]]
            # Rule violation
            if dist_val_>max_dist:
                print '*** the distance of pairs :',idx_pair,'in ',i,'th cluster ~',np.round(dist_val_,2),' > max_dist=', np.round(max_dist,2),'***'          
                intra_err_cnt=intra_err_cnt+1
    print '------------------------------------------------------------------------------------------'
    print 'Inter-Cluster distance check.....'       
    print 'Condition: intra-cluster distance is lower-bounded by',round(min_dist,2)
    print '------------------------------------------------------------------------------------------'
    cluster_pairs=pair_in_idx(range(num_clusters))
    inter_err_cnt=0
    for c_pair in cluster_pairs:
        idx_set_0=np.nonzero(labels==(c_pair[0]))[0]
        idx_set_1=np.nonzero(labels==(c_pair[1]))[0]
        #print '----------------------------------------------------------'
        #print 'The pairwise distance between ',c_pair[0],'th cluster and',c_pair[1],'th cluster'
        for idx_pair in pair_in_idx(idx_set_0,idx_set_1):
            #print idx_pair, 'dist-',round(dist_mat[idx_pair[0],idx_pair[1]],2)
            dist_val_=dist_mat[idx_pair[0],idx_pair[1]]
            # Rule violation
            if dist_val_<min_dist:
                print '*** the distance of pairs :',idx_pair[0] ,'in', c_pair[0] ,' and ', idx_pair[1] ,'in',c_pair[1],'~',round(dist_val_,2),' < min_dist=', round(min_dist,2),'***'          
                inter_err_cnt=inter_err_cnt+1
    return intra_err_cnt, inter_err_cnt
