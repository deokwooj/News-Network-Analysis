sim_thresh=0.2
labels_=np.inf*ones(Dq.shape[0])
labels_id=0
exemplars_=[]
used_idx_set=set([])
for k,rows in enumerate(Dq):
    idx=np.where(rows>sim_thresh)[0]
    print update_idx, list(used_idx_set)    
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
