import matplotlib.pyplot as plt
import networkx as nx


class autoinstance(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self.func.__get__(owner(), owner)
        else:
            return self.func.__get__(instance, owner)


class GraphWrapper(object):
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._node_labels = {}
        self._edge_labels = {}
        self._graph = nx.MultiDiGraph()

    @autoinstance
    def add_node(self, node, label=None):
        self._nodes.append(node)
        self._node_labels[node] = node if label is None else label
        return self

    @autoinstance
    def add_nodes(self, nodes: list, labels: dict = None):
        self._nodes += nodes
        if labels is not None:
            self._node_labels.update(labels)
        return self

    @autoinstance
    def add_edge(self, edge_from, edge_to, label: str = ""):
        edge = (edge_from, edge_to)
        self._edges.append(edge)
        if label != "":
            self._edge_labels[edge] = label
        return self

    @autoinstance
    def add_edges(self, edges, labels: dict = None):
        self._edges += edges
        if labels is not None:
            self._edge_labels.update(labels)
        return self

    def edges_to_node(self, node):
        return {i: self._edge_labels[i] for i in self._graph.in_edges(node)}

    def edges_from_node(self, node):
        return {i: self._edge_labels[i] for i in self._graph.out_edges(node)}

    def probability_to_node_index(self, node_index):
        return {self._nodes.index(i[0]): self._edge_labels[i] for i in self._graph.in_edges(self._nodes[node_index])}

    def probability_from_node_index(self, node_index):
        return {self._nodes.index(i[1]): self._edge_labels[i] for i in self._graph.out_edges(self._nodes[node_index])}

    def get_nodes(self):
        return self._nodes.copy()

    def get_edges(self):
        return self._edges.copy()

    @autoinstance
    def build(self, label_pos=0.3, edge_font_size=6, node_font_size=8):
        self._graph.add_nodes_from(self._nodes)
        self._graph.add_edges_from(self._edges)
        pos = nx.spring_layout(self._graph, k=0.95, iterations=150)
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=self._edge_labels, label_pos=label_pos,
                                     font_size=edge_font_size, rotate=False)
        nx.draw_networkx_labels(self._graph, pos, self._node_labels, font_size=node_font_size)
        nx.draw(self._graph, pos=pos)
        return self

    def show(self, __outpath=None):
        if __outpath is not None:
            plt.savefig(__outpath)  # save as png
        plt.show()  # display
