#-*- coding:utf-8 -*-
from konlpy.tag import Kkma
from konlpy.utils import pprint

 
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.cell import get_column_letter

from openpyxl import load_workbook

import xlsxwriter

#kkma = Kkma()
#pprint (kkma.nouns(u"아버지가 방에 들어가신다. 그 방에는 내 동생이 있다."))

wb=load_workbook('reference.xlsx')
sheetList = wb.get_sheet_names()
sheet = wb.get_sheet_by_name(sheetList[0])
cellValue = sheet.cell('B2').value

print cellValue


