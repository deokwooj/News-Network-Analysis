# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 21:18:26 2015

@author: deokwooj
"""

"""
* Description 
- This file defines global constant symbols and definitions used through in this program. 
- Should be included all python modules first. 
"""
import na_tools as nt
# Define media code dictionary
#(media name, media id)
media_code={\
'강원도민일보':01300101,\
'강원일보':01300201,\
'경기일보':	01200101,\
'경남도민일보':01500151,\
'경남신문':	01500051,\
'경상일보':	01500301,\
'경인일보':	01200201,\
'경향신문':	01100101,\
'광주일보':	01600301,\
'국민일보':	01100201,\
'국제신문':	01500401,\
}
"""
'기자협회보	07100702
'김포뉴스	05200752
'내일신문	01100301
'당진시대	05520352
'대덕넷	04400108
대전일보	01400201
매일신문	01500601
무등일보	01600501
미디어오늘	07100251
문화일보	01100501
부산일보	01500701
브레이크뉴스	04100608
새전북신문	01600601
서울신문	01100601
세계일보	01100701
한국경제	02100601
한국재경신문	04101358
시사인	06100252
MBC	08100201
KNN	08520101
머니투데이	02100201
오마이뉴스	04100908
헤럴드경제	02100701
스포츠서울	10100101
스포츠칸	10100201
영남일보	01500801
옥천신문	05410052
이데일리	04101008
인천일보	01200401
전남일보	01600801
전북도민일보	01601001
전북일보	01601101
제민일보	01700101
중도일보	01400351
중부매일	01400401
충북일보	01400551
충청투데이	01400701
파이낸셜뉴스	02100501
평택문화신문	05202702
한겨레	01101001
한라일보	01700201
홍성신문	05420702
PD저널	07100602
아시아투데이	01100751
한국일보	01101101
매일경제	02100101
서울경제	02100301
이투데이	02100351
프라임경제	02100563
투데이코리아	04101258
국방일보	04103008
KBS	08100101
SBS	08100301
동아일보	01100401
노컷뉴스	04100058
조세일보	04101208
코리아헤럴드	03100101
"""


#noun_dict={1:'대한민국', 2:'분단','3:북한',....so on}
noun_dict_temp_1=nt.loadObjectBinaryFast(DICT_SPLIT_ARR_NOUNS)
noun_dict_temp_2=nt.loadObjectBinaryFast(DICT_NOUNS)

all_nouns=[]
for key in noun_dict_temp.iteritems():
    print key[0]
    print '---------------'
    for wd in key[1]:
        all_nouns.append(wd)
noun_dict={}
for i,noun in enumerate(set(all_nouns)):
    noun_dict.update({i:noun})

# 
#for key, noun in noun_dict.iteritems():
#    print key, noun