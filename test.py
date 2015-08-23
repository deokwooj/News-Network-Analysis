# -*- coding: utf-8 -*-



all_ns = pickle.load(open("./file/dict_informer.p","rb"))
U=np.matrix(np.ones((len(all_ns),6)))

for i in range(0, len(all_ns)):
    #print all_ns[i].id, all_ns[i].org, all_ns[i].pos
    a=i
    b=i+1

    U[a:b,0]=all_ns[i].id
    U[a:b,1]=all_ns[i].org
    U[a:b,2]=all_ns[i].type
    U[a:b,3]=all_ns[i].pos
    U[a:b,4]=all_ns[i].code
    U[a:b,5]=all_ns[i].classified

print U

