#-*- coding:utf-8 -*-
from konlpy.tag import Kkma
from konlpy.utils import pprint

 
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.cell import get_column_letter

from openpyxl import load_workbook

import xlsxwriter


wb=load_workbook('reference.xlsx')
sheetList = wb.get_sheet_names()
sheet = wb.get_sheet_by_name(sheetList[0])

cellValue = sheet.cell('B2').value

#count = cellValue.count('\u201c')
count = cellValue.count(u'\u201c')   # count of quatation mark

if count == 1:

	START_QUA = cellValue.find(u"\u201c") + 1 # position of first quatation mark
	CELL_VALUE_LEN = len(cellValue)

	cellValue_re = cellValue[START_QUA:CELL_VALUE_LEN]
	END_QUA = cellValue_re.find(u"\u201d") # position of last quatation mark

	cellValue_final = cellValue_re[0:END_QUA]

	kkma = Kkma()
	pprint (kkma.nouns(cellValue_final))

else :
	print "no one sentence"
