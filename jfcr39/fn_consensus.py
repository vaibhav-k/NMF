import numpy as np
import pandas as pd
import numpy.matlib
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform

class JConsensus():
	def __init__(self, X, Y, Z):
		self.cmW = pd.DataFrame(np.zeros((X.shape[0], X.shape[0])), index = X.index, columns = X.index)
		self.cmHx = pd.DataFrame(np.zeros((X.shape[1], X.shape[1])), index = X.columns, columns = X.columns)
		self.cmHy = pd.DataFrame(np.zeros((Y.shape[1], Y.shape[1])), index = Y.columns, columns = Y.columns)
		self.cmHz = pd.DataFrame(np.zeros((Z.shape[1], Z.shape[1])), index = Z.columns, columns = Z.columns)
		self.cmNum = 0

	def calcConnectivityW(self, W):
		maxW = W.values.max(axis=1)
		maxW[maxW == 0] = 1
		maxMatW = (np.tile(maxW, (W.shape[1], 1))).transpose()
		binaryW = W == maxMatW
		connMatW = np.dot(binaryW, binaryW.transpose())
		return connMatW
	
	def calcConnectivityH(self, H):
		maxH = H.values.max(axis=0)
		maxH[maxH == 0] = 1
		maxMatH = np.tile(maxH, (H.shape[0], 1))
		binaryH = H == maxMatH
		connMatH = np.dot(binaryH.transpose(), binaryH)
		return connMatH
		
	def addConnectivityMatrixtoConsensusMatrix(self, connW, connHx, connHy, connHz):
		self.cmW += connW
		self.cmHx += connHx
		self.cmHy += connHy
		self.cmHz += connHz
		self.cmNum += 1
		
	def finalizeConsensusMatrix(self):
		self.cmW /= self.cmNum
		self.cmHx /= self.cmNum
		self.cmHy /= self.cmNum
		self.cmHz /= self.cmNum

	def reorderConsensusMatrix(self, M):
		Y = 1 - M
		Z = linkage(squareform(Y), method='average')
		ivl = leaves_list(Z)
		ivl = ivl[::-1]
		reorderM = pd.DataFrame(M.values[:, ivl][ivl, :], index = M.columns[ivl], columns = M.columns[ivl])
		return reorderM
