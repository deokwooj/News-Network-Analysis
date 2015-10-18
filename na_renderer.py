# -*- coding: utf-8 -*-
# na_renderer.py  

import os
import uuid
import numpy as np 
import networkx as nx 
import matplotlib
import matplotlib.pyplot
from openpyxl import load_workbook
from openpyxl.workbook import Workbook 
from openpyxl.drawing import Image


__author__ = "Jung-uk Choi"
__copyright__ = "Copyright 2015, Deokwoo Jung, All rights reserved."
__credits__ = ["Jung-uk Choi"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jung-uk Choi"
__email__ = "choijunguk@gmail.com"
__status__ = "Prototype"


TMP_DIR = os.path.join('/tmp', 'NLP')
os.system('mkdir ' + TMP_DIR)

def temporaryImagePath():
	return os.path.join(TMP_DIR, str(uuid.uuid4()) + '.png')


class Context(object):
	def __init__(self):
		super(Context, self).__init__()
		self.__quotations = {}
		self.__labels = {}
		self.__connectivity = None

	@property
	def quotations(self):
		return sorted(self.__quotations.keys())

	@property 
	def labels(self):
		return sorted(self.__labels.keys())

	def isExamplar(self, quotationID):
		return self.__quotations[quotationID]['is_examplar']

	def labelExamplar(self, labelID):
		return self.__labels[labelID]['examplar']

	def labelQuotations(self, labelID):
		return self.__labels[labelID]['quotations']

	def setQuotationText(self, quotationID, text):
		assert isinstance(quotationID, (int, long))
		assert isinstance(text, (str, unicode))

		try:
			obj = self.__quotations[quotationID]
		except KeyError:
			obj = self.__quotations[quotationID] = {'text':None, 'label':None, 'is_examplar':False}

		obj['text'] = text

	def setQuotationLabel(self, quotationID, labelID):
		assert isinstance(quotationID, (int, long))
		assert isinstance(labelID, (int, long))

		try:
			obj = self.__labels[labelID]
		except KeyError:
			obj = self.__labels[labelID] = {'examplar': None, 'quotations': []}

		self.__quotations[quotationID]['label'] = labelID
		obj['quotations'].append(quotationID)

	def setLabelExamplar(self, labelID, quotationID):
		assert isinstance(labelID, (int, long))
		assert isinstance(quotationID, (int, long))

		try:
			obj = self.__labels[labelID]
		except KeyError:
			obj = self.__labels[labelID] = {'examplar': None, 'quotations': []}

		obj['examplar'] = quotationID
		self.__quotations[quotationID]['is_examplar'] = True

	def setConnectivityMatrix(self, m):
		assert isinstance(m, np.matrix)
		assert m.shape[0] == m.shape[1]

		self.__connectivity = m

	def connectivityMatrixForStepN(self, N):
		assert isinstance(N, int)
		assert N > 0

		if self.__connectivity is not None:
			m = self.__connectivity ** N 
			for r in range(m.shape[0]):
				for c in range(m.shape[1]):
					if m[r, c]:
						m[r, c] = 1
					else:
						m[r, c] = 0

			return m

	def labelIdForQuotationID(self, quotationID):
		assert isinstance(quotationID, (int, long))	
		return self.__quotations[quotationID]['label']


class ConnectedDots(object):
	def __init__(self, context):
		assert isinstance(context, Context)
		super(ConnectedDots, self).__init__()
		self.__context = context

	def render(self, N, outputPath=None):
		assert isinstance(N, int)
		assert N > 0
		assert outputPath is None or isinstance(outputPath, (str, unicode))

		matplotlib.pyplot.clf()

		G = nx.Graph()
		labels = {}
		degrees = {}

		quotationIDs = sorted(self.__context.quotations)

		# add all quotations
		for qid in quotationIDs:
			G.add_node(qid)
			labels[qid] = qid
			degrees[qid] = 0

		# add label - quotations relationship
		for l in self.__context.labels:
			for q in self.__context.labelQuotations(l):
				G.add_edge(self.__context.labelExamplar(l), q, weight=1.0)

		# add connectivity
		m = self.__context.connectivityMatrixForStepN(N)
		for i in range(len(quotationIDs)):
			q1 = quotationIDs[i]
			l1 = self.__context.labelIdForQuotationID(q1)

			for j in range(len(quotationIDs)):
				q2 = quotationIDs[j]
				l2 = self.__context.labelIdForQuotationID(q2)
				if l1 != l2:
					if m[l1, l2]:
						if self.__context.isExamplar(q1) and self.__context.isExamplar(q2):
							G.add_edge(q1, q2, weight=0.1)
							degrees[q1] += 1
							degrees[q2] += 1

		#
		sizes = []
		for qid in quotationIDs:
			d = degrees[qid]
			sizes.append(500 + d * 100)

		#
		colors = []
		max_depth = float(max(degrees.values()))
		for qid in quotationIDs:
			k = degrees[qid] / max_depth
			if self.__context.isExamplar(qid):
				colors.append('red')
			else:
				colors.append('orange')

		#
		try:
			pos=nx.graphviz_layout(G)

		except:
			pos=nx.spring_layout(G, iterations=20)

		# nodes
		nx.draw_networkx_nodes(G, pos, nodelist=quotationIDs, node_size=sizes, font_size=5, node_color=colors)

		# edges
		elarge=[(u,v) for (u,v,d) in G.edges(data=True) if 'weight' in d and d['weight'] > 0.5]
		esmall=[(u,v) for (u,v,d) in G.edges(data=True) if 'weight' in d and d['weight'] <=0.5]
		nx.draw_networkx_edges(G, pos, edgelist=elarge, width=0.5, edge_color='gray')
		nx.draw_networkx_edges(G, pos, edgelist=esmall, width=0.5, edge_color='gray', style='dashed')

		nx.draw_networkx_labels(G, pos, labels)

		if outputPath:
			matplotlib.pyplot.savefig(outputPath)
		
		else:
			matplotlib.pyplot.show()


class ExcelRenderer(object):
	def __init__(self, context):
		assert isinstance(context, Context)
		super(ExcelRenderer, self).__init__()
		self.__context = context
		self.__connectedDotsRenderer = ConnectedDots(context)

	def render(self, outputPath, maxN):
		assert isinstance(outputPath, (str, unicode))
		assert isinstance(maxN, int)
		
		wb=Workbook()
		wb.remove_sheet(wb.worksheets[0])
		self.renderInfoSheet(wb)
		for i in range(maxN):
			self.renderConnectivitySheet(wb, i+1)

		wb.save(outputPath)

	def renderInfoSheet(self, wb):
		ws = wb.create_sheet()
		ws.title = 'Info'
		return ws

	def renderConnectivitySheet(self, wb, N):
		ws = wb.create_sheet()
		ws.title = 'N = %d' % N

		path = temporaryImagePath()
		self.__connectedDotsRenderer.render(N, path)
		
		img = Image(path)
		img.anchor(ws['A1'])
		ws.add_image(img)
		return ws



if __name__ == '__main__':
	# q_id={0:23, 1:10, 2:39, 3:44, 4:14, 5:33, 6:21, 7:66, 8:88, 9:11}
	# q_label={0:0, 1:4, 2:1, 3:2, 4:3, 5:4, 6:1, 7:2, 8:2, 9:1}
	# q_exemplar={0:23, 1:39, 2:44, 3:14, 4:33}

	G_q = np.matrix([[1, 0, 1, 0, 0],
		             [0, 1, 1, 0, 1],
	                 [1, 1, 1, 1, 0],
	                 [0, 0, 1, 1, 0],
	                 [0, 1, 0, 0, 1]])

	obj = Context()
	obj.setQuotationText(23, 'text23')
	obj.setQuotationText(10, 'text10')
	obj.setQuotationText(39, 'text39')
	obj.setQuotationText(44, 'text44')
	obj.setQuotationText(14, 'text14')
	obj.setQuotationText(33, 'text33')
	obj.setQuotationText(21, 'text21')
	obj.setQuotationText(66, 'text66')
	obj.setQuotationText(88, 'text88')
	obj.setQuotationText(11, 'text11')

	obj.setQuotationLabel(23, 0)
	obj.setQuotationLabel(10, 4)
	obj.setQuotationLabel(39, 1)
	obj.setQuotationLabel(44, 2)
	obj.setQuotationLabel(14, 3)
	obj.setQuotationLabel(33, 4)
	obj.setQuotationLabel(21, 1)
	obj.setQuotationLabel(66, 2)
	obj.setQuotationLabel(88, 2)
	obj.setQuotationLabel(11, 1)

	obj.setLabelExamplar(0, 23)
	obj.setLabelExamplar(1, 39)
	obj.setLabelExamplar(2, 44)
	obj.setLabelExamplar(3, 14)
	obj.setLabelExamplar(4, 33)

	obj.setConnectivityMatrix(G_q)


	# r = ConnectedDots(obj)
	# r.render(1, '/Users/emerson/Downloads/1.png')
	# r.render(2, '/Users/emerson/Downloads/2.png')
	# r.render(3, '/Users/emerson/Downloads/3.png')
	# r.render(4, '/Users/emerson/Downloads/4.png')

	r2 = ExcelRenderer(obj)
	r2.render('/Users/emerson/Downloads/out.xlsx', 4)
