import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.idMap = {}
        self._bestPath = []
        self._bestLenght = 0


    def buildGraph(self, anno):
        self._graph.clear()
        numAvvistamenti = DAO.getAvvistamenti(anno)
        nodi = DAO.getNodes(anno)
        self._graph.add_nodes_from(nodi)

        for nodo in nodi:
            self.idMap[nodo.id] = nodo

        edges = DAO.getEdges(anno, self.idMap.keys())
        for edge in edges:
            v0 = self.idMap[edge[0]]
            v1 = self.idMap[edge[1]]
            self._graph.add_edge(v0, v1)

        return self._graph

    def getNodes(self):
        return self._graph.nodes

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getPrecedenti(self, nodo):
        precedenti = self._graph.predecessors(nodo)
        return precedenti

    def getSuccessori(self, nodo):
        successori = self._graph.successors(nodo)
        return successori

    def getRaggiungibili(self, nodo):
        raggiungibili = nx.descendants(self._graph, nodo)
        return raggiungibili

    def getRaggiungibiliDFS(self, stato):
        tree = nx.dfs_tree(self._graph, stato)
        raggiungibili = list(tree.nodes)
        raggiungibili.remove(stato)
        return raggiungibili

    def getRaggiungibiliBFS(self, stato):
        tree = nx.bfs_tree(self._graph, stato)
        raggiungibili = list(tree.nodes)
        raggiungibili.remove(stato)
        return raggiungibili


    def getAnni(self):
        return list(DAO.getYears())

    def getAvvistamenti(self, anno):
        return DAO.getAvvistamenti(anno)

    def sequenzaAvvistamenti(self, nodo):
        self._bestPath = []
        self._bestLenght = 0

        parziale = [nodo]

        self._ricorsione(parziale)

        return self._bestPath, self._bestLenght

    def _ricorsione(self, parziale):
        #condizione di terminazione:
        if len(parziale) > self._bestLenght:
            self._bestLenght = len(parziale)
            self._bestPath = parziale[:]
            print(self._bestPath, self._bestLenght)

        for nodo in self._graph.successors(parziale[-1]):
            if nodo not in parziale:
                parziale.append(nodo)
                self._ricorsione(parziale)
                parziale.pop()


