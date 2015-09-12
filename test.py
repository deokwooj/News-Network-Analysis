
NewsQuoObjs=[]
########################################################
# Print all news dictionary information    
########################################################
fld_name=('Name','Quatation', 'Nouns','Code')
print '********************************************************************'
print 'all news dictionary'    
for k,(key, val) in enumerate(dict_news_info.iteritems()):
    print '==================================================='
    print 'key val: ', key        
    print '==================================================='
    #for val_a ,val_b in (('name','quatation', 'nouns','code'), list(val)[0]):
    #    print val_a, val_b
    quo_temp=NewsQuotation()
    quo_temp.quotation_key=str(key)
    for i,(fld_, val_) in enumerate(zip(fld_name,list(val)[0])):
        print fld_
        if fld_=='Name':
            quo_temp.news_src.name=val_
        elif fld_=='Quatation':
            val_temp=val_
            quo_temp.quotation=val_
        elif fld_=='Nouns':
            quo_temp.nounvec=val_
        elif fld_=='Code':
            val_temp=str(val_)[1:]
            quo_temp.media_id=val_temp[:8]
            quo_temp.date=\
            dt.datetime(int(val_temp[9:13]),int(val_temp[13:15]),int(val_temp[15:17]),23)
            quo_temp.article_id=val_temp[17:]
        else:
            warnings.warn("fld name not found")
        print i+1,'.', fld_, ':', val_
        print '-----------------'
    NewsQuoObjs.append((k,quo_temp))
print '********************************************************************'


"""
wb=load_workbook(WHOLETABLE_EXCEL)
ws = wb.get_sheet_by_name('wholetable')
[ b for a in ws.iter_rows() for b in a] 
"""
"""
NewsSrcObjs=[]
src_fld_name=\
['src_id','src_date','src_name','src_org','src_type','src_pos','src_code','src_clfd']
for k,row in enumerate(ws.iter_rows(row_offset=1)):
src_temp=NewsSource()
print  '==========================================='
print k
for (fld_, row_) in zip(src_fld_name,row):
    if row_.value=='null':
        row_.value=None
    elif row_.value=='\N':
        row_.value='N'
    print  '----------------'
    print fld_, row_.value
    val_temp=row_.value
    if val_temp!=None:
        if fld_=='src_id':
            src_temp.id =val_temp
        elif fld_=='src_date':
            val_temp=str(val_temp)[:10]
            src_temp.date =dt.datetime(int(val_temp[:4]),int(val_temp[5:7]),int(val_temp[8:10]))
        elif fld_=='src_name':
            src_temp.name =val_temp
        elif fld_=='src_org':
            src_temp.org =val_temp
        elif fld_=='src_type':
            src_temp.srctype =val_temp
        elif fld_=='src_pos':
            src_temp.pos =val_temp
        elif fld_=='src_code':
            src_temp.code =val_temp
        elif fld_=='src_clfd':                            
            src_temp.classified =val_temp
        else:
            warnings.warn("fld name not found")

print  '==========================================='
if src_temp.name!=None:
    NewsSrcObjs.append((k,src_temp))


for temp_obj in NewsSrcObjs:
print temp_obj[1].name
"""


"""
for (fld_name, rowlet) in zip(src_fld_name,row):
print fld_name
print rowlet.value

"""

"""
########################################################
# Print all news dictionary information    
########################################################
fld_name=('Name','Quatation', 'Nouns','Code')
print '********************************************************************'
print 'all news dictionary'    
for k,(key, val) in enumerate(dict_news_info.iteritems()):
    print '==================================================='
    print 'key val: ', key        
    print '==================================================='
    #for val_a ,val_b in (('name','quatation', 'nouns','code'), list(val)[0]):
    #    print val_a, val_b
    quo_temp=NewsQuotation()
    quo_temp.quotation_key=str(key)
    for i,val_a in enumerate(zip(fld_name,list(val)[0])):
        print val_a[0]
        if val_a[0]=='Name':
            quo_temp.news_src.name=val_a[1]
        elif val_a[0]=='Quatation':
            val_temp=val_a[1]
            quo_temp.quotation=val_a[1]
        elif val_a[0]=='Nouns':
            quo_temp.nounvec=val_a[1]
        elif val_a[0]=='Code':
            val_temp=str(val_a[1])[1:]
            quo_temp.media_id=val_temp[:8]
            quo_temp.date=\
            dt.datetime(int(val_temp[9:13]),int(val_temp[13:15]),int(val_temp[15:17]),23)
            quo_temp.article_id=val_temp[17:]
        else:
            warnings.warn("fld name not found")
        quo_temp.news_src.code= []
        quo_temp.news_src.name=[]
        quo_temp.news_src.classified= []
        quo_temp.news_src.pos= []
        quo_temp.news_src.srctype= []
        quo_temp.news_src.org= []
        quo_temp.news_src.id= []        
        
        print i+1,'.', val_a[0], ':', val_a[1]
        print '-----------------'
    NewsQuoObjs.append((k,quo_temp))
print '********************************************************************'


for i in range(2,row_count):
id = sheet.cell(row=i, column=1).value   # id
name = sheet.cell(row=i, column=3).value   # name
org = sheet.cell(row=i, column=4).value   # organization
i_type = sheet.cell(row=i, column=5).value   # organization
pos = sheet.cell(row=i, column=6).value   # position
code = sheet.cell(row=i, column=7).value   # organization
classified = sheet.cell(row=i, column=8).value   # organization
print code
dict_id_name[id] = name   # dictionary id : name
dict_type[id] = get_excel_type(i_type)   # dictionary   id : type
dict_code[id] = code   # dictionary   id : code
dict_classified[id] = get_excel_classified(classified)   # dictionary   id : classified
try:
    idx_org = inv_src_org_set.keys().index(org)
    dict_org[id] = idx_org
except ValueError:
    idx_org = -1

try:
    idx_pos = inv_src_pos_set.keys().index(pos)
    dict_pos[id] = idx_pos
except ValueError:
    idx_pos = -1

"""