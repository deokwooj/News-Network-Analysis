# -*- coding: utf-8 -*-


"""
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
"""


class NewsQuotation:
    def __init__(self):
        self.article_id ='000000000' # 9 digit number 
        self.media_id = '00000000'  # 8 digit number 
        self.date=dt.datetime(1999,12,31,23) #  quotations data,1999년 12월 31일 23시.
        self.news_src=NewsSource()
        self.quo_nouns = []     # position, need utcto be initionalized by kkd_functions. 
    def whoami(self):
        for key in self.__dict__.items():
            if key[0]=='news_src':
                import pdb;pdb.set_trace()
                temp=key[1]
                print key[0],'name : ', temp.name
            else:
                print key[0],': ', key[1]


aa=NewsQuotation()
aa.whoami()

