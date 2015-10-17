# -*- coding: utf-8 -*-
# na_exporter.py  

import numpy as np 
import networkx as nx 
import matplotlib
import matplotlib.pyplot

from openpyxl import load_workbook
from openpyxl.workbook import Workbook 


__author__ = "Jung-uk Choi"
__copyright__ = "Copyright 2015, Deokwoo Jung, All rights reserved."
__credits__ = ["Jung-uk Choi"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jung-uk Choi"
__email__ = "choijunguk@gmail.com"
__status__ = "Prototype"


class Exporter(object):
	def __init__(self):
		super(Exporter, self).__init__()
		self.__quotations = {}
		self.__labels = {}
		self.__connectivity = None

	def quotationText(self, quotationID, text):
		assert isinstance(quotationID, (int, long))
		assert isinstance(text, (str, unicode))

		try:
			obj = self.__quotations[quotationID]
		except KeyError:
			obj = self.__quotations[quotationID] = {'text':None, 'label':None, 'is_examplar':False}

		obj['text'] = text

	def quotationLabel(self, quotationID, labelID):
		assert isinstance(quotationID, (int, long))
		assert isinstance(labelID, (int, long))

		try:
			obj = self.__labels[labelID]
		except KeyError:
			obj = self.__labels[labelID] = {'examplar': None, 'quotations': []}

		self.__quotations[quotationID]['label'] = labelID
		obj['quotations'].append(quotationID)

	def labelExamplar(self, labelID, quotationID):
		assert isinstance(labelID, (int, long))
		assert isinstance(quotationID, (int, long))

		try:
			obj = self.__labels[labelID]
		except KeyError:
			obj = self.__labels[labelID] = {'examplar': None, 'quotations': []}

		obj['examplar'] = quotationID
		self.__quotations[quotationID]['is_examplar'] = True

	def connectivityMatrix(self, m):
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

	def showGraphForStepN(self, N):
		assert isinstance(N, int)
		assert N > 0

		G = nx.Graph()
		labels = {}
		examplar_nodes = []
		other_nodes = []
		degrees = {}

		quotationIDs = sorted(self.__quotations.keys())

		# add all quotations
		for qid in quotationIDs:
			G.add_node(qid)
			obj = self.__quotations[qid]

			labels[qid] = qid
			degrees[qid] = 0

			if obj['is_examplar']:
				examplar_nodes.append(qid)
			else:
				other_nodes.append(qid)

		# add label - quotations relationship
		for l in self.__labels.values():
			for q in l['quotations']:
				G.add_edge(l['examplar'], q, weight=1.0)

		# add connectivity
		m = self.connectivityMatrixForStepN(N)
		for i in range(len(quotationIDs)):
			q1 = quotationIDs[i]
			l1 = self.labelIdForQuotationID(q1)

			for j in range(len(quotationIDs)):
				q2 = quotationIDs[j]
				l2 = self.labelIdForQuotationID(q2)
				if l1 != l2:
					if m[l1, l2]:
						if self.__labels[l1]['examplar'] == q1 and self.__labels[l2]['examplar'] == q2:
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
			if self.__quotations[qid]['is_examplar']:
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
		matplotlib.pyplot.show()


if __name__ == '__main__':
	# q_id={0:23, 1:10, 2:39, 3:44, 4:14, 5:33, 6:21, 7:66, 8:88, 9:11}
	# q_label={0:0, 1:4, 2:1, 3:2, 4:3, 5:4, 6:1, 7:2, 8:2, 9:1}
	# q_exemplar={0:23, 1:39, 2:44, 3:14, 4:33}

	# G_q = np.matrix([[1, 0, 1, 0, 0],
	# 	             [0, 1, 1, 0, 1],
	#                  [1, 1, 1, 1, 0],
	#                  [0, 0, 1, 1, 0],
	#                  [0, 1, 0, 0, 1]])

	obj = Exporter()
	obj.quotationText(23, 'text23')
	obj.quotationText(10, 'text10')
	obj.quotationText(39, 'text39')
	obj.quotationText(44, 'text44')
	obj.quotationText(14, 'text14')
	obj.quotationText(33, 'text33')
	obj.quotationText(21, 'text21')
	obj.quotationText(66, 'text66')
	obj.quotationText(88, 'text88')
	obj.quotationText(11, 'text11')

	obj.quotationLabel(23, 0)
	obj.quotationLabel(10, 4)
	obj.quotationLabel(39, 1)
	obj.quotationLabel(44, 2)
	obj.quotationLabel(14, 3)
	obj.quotationLabel(33, 4)
	obj.quotationLabel(21, 1)
	obj.quotationLabel(66, 2)
	obj.quotationLabel(88, 2)
	obj.quotationLabel(11, 1)

	obj.labelExamplar(0, 23)
	obj.labelExamplar(1, 39)
	obj.labelExamplar(2, 44)
	obj.labelExamplar(3, 14)
	obj.labelExamplar(4, 33)

	obj.connectivityMatrix(G_q)


	obj.showGraphForStepN(1)
	obj.showGraphForStepN(2)
	obj.showGraphForStepN(3)
	obj.showGraphForStepN(4)
