# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 18:15:38 2015

@author: deokwooj
"""

id_name_load = pickle.load(open("./file/dict_id_name.p","rb"))
org_load = pickle.load(open("./file/dict_org.p","rb"))
type_load = pickle.load(open("./file/dict_type.p","rb"))
pos_load = pickle.load(open("./file/dict_pos.p","rb"))
code_load = pickle.load(open("./file/dict_code.p","rb"))
classified_load = pickle.load(open("./file/dict_classified.p","rb"))

sheet = excel_open()
row_count = sheet.get_highest_row()
all_ns = []
#id = sheet.cell(row=i, column=1).value   # id
count = 0


for i in range(2, row_count):
    ns_ins = NewsSource() # create an instance of news sources
    id = sheet.cell(row=i, column=1).value   # id 
    org = sheet.cell(row=i, column=4).value   # org
    pos = sheet.cell(row=i, column=6).value   # pos
    code = sheet.cell(row=i, column=7).value   # organization type
    ns_ins.id = id
    ns_ins.code = code_load[str(count)]
    ns_ins.type = type_load[str(count)]
    ns_ins.classified = classified_load[str(count)]
    if org == 'null':
        org = None
        if pos == 'null':
            pos = None  
        for j in range(0, len(org_load)):
            if org == org_load[j]:
                ns_ins.org = org_load.keys()[j]
        for k in range(0, len(pos_load)):
            if pos == pos_load[k]:
                ns_ins.pos = pos_load.keys()[k]
        count = count + 1
        all_ns.append(ns_ins)




sheetList = wb.get_sheet_names()
sheet = wb.get_sheet_by_name('wholetable')

wb=load_workbook('./file/wholetable.xlsx')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    items = []
    rows = []