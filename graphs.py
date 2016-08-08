from collections import deque
import time as t

class Graph(object):
	"""
	weights: a dict whose keys will be the keys
			 of 2 nodes concatenated together and
			 the values will be the edge weights
	Parameters:
		graph:
		  -a dict of 2 dicts: incidence dict and weight dict
		  or
		  -an adjacency matrix
		directed: boolean
	"""
	def __init__(self, graph, directed=True):
		A = set()

		self.V = {}

		#just add everything to V: O(V+E)
		for x in graph["Adj"].keys():
			for i in graph["Adj"][x]:
				A.add(i)
			A.add(x)

		for node in A:
			self.V[node] = Node(node)

		for key, val in self.V.iteritems():	
			if key in graph["Adj"].keys():
				for i in graph["Adj"][key]:
					val.neighbors.add(self.V[i])

		# self.V = dict.fromkeys([z.key for z in self.V)
		# self.Adj = dict(self.Adj, **self.V)
		self.E = graph["E"]
		self.directed = directed


	def print_adj(self):
		for i in self.V.values():
			print i.key + ": "
			for j in i.neighbors:
				print "\t"+j.key


	def weight(self, u, v):
		return self.E[u + v]


	def recursive_dfs(self):
		for node in self.V.values():
			node.distance = float('inf')
			node.color = "white"
			node.predecessor = None
		self.time = 0

		for node in self.V.values():
			if node.color == "white":
				self.recursive_dfs_visit(node)
				

		for i in self.V.values():
			print "%s: distance: %d, finish time: %d" %(i, i.distance, i.finish_time)
		

	def recursive_dfs_visit(self, u):
		self.time = self.time + 1
		u.distance = self.time
		u.color = "gray"
		for v in u.neighbors:
			if v.color == "white":
				v.predecessor = u
				self.recursive_dfs_visit(v)
		u.color = "black"
		self.time = self.time + 1
		u.finish_time = self.time



	def bfs(self, s):
		#initialize
		for node in self.V.values():
			node.distance = float('inf')
			node.color = "white"
			node.predecessor = None

		self.V[s].distance = 0
		self.V[s].color = "black"
		self.V[s].predecessor = None

		Q = deque()
		Q.append(self.V[s])
		while len(Q) != 0:
			u = Q.popleft()
			for v in u.neighbors:
				if v.color == "white":
					v.distance = u.distance + 1
					v.predecessor = u
					Q.append(v)
			u.color = "black"



class Node(object):
	def __init__(self, key, data=None):
		self.neighbors = set()
		self.key = key
		self.data = data
		

	# def __hash__(self):
	# 	return hash(self.key)

	# def __eq__(self, obj):
	# 	if not isinstance(obj, Node):
	# 		return false
	# 	return self.__hash__() == obj.__hash__()

	def __repr__(self):
		return self.key



