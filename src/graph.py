from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    """
    Classe Nodo que representa um estado com uma posicao e velocidade
    """
    def __init__(self, posicao: tuple[int, int], velocidade: tuple[int, int] = (0, 0)):
        #Posicao do carro num ponto
        self.posicao = posicao
        #Velocidade do carro
        self.velocidade = velocidade 

    def get_posicao(self) -> tuple[int, int]:
        return self.posicao

    def get_velocidade(self) -> tuple[int, int]:
        return self.velocidade

    def __str__(self):
        return f"(p{self.posicao}, v{self.velocidade})"

    def __eq__(self, node) -> bool:
        if isinstance(node, Node):
            return self.posicao == node.posicao and self.velocidade == node.velocidade
        return False

    def __hash__(self) -> int:
        return hash((self.posicao, self.velocidade))

class Graph:
    """
    """
    def __init__(self, directed=False):
        self.directed: bool = directed
        self.graph: dict[Node, set[tuple[Node, int]]] = {}
        self.heuristics = {} # ainda nao sei se vai ficar

    def clear(self):
        self.graph.clear()

    """
    Funcao que transforma os nodos numa lista de stirngs
    """
    def print_nodes(self) -> list[str]:
        keys = self.graph.keys()
        keys = list(map(lambda node : str(node), keys))
        return keys

    """
    funcao que adiciona uma adjacencia ao grafo
    """
    def add_edge(self, node_1: Node, node_2: Node, weight):
        if node_1 not in self.graph:
            self.graph[node_1] = set()

        if node_2 not in self.graph:
            self.graph[node_2] = set()

        self.graph[node_1].add((node_2, weight))

        if not self.directed:
            self.graph[node_2].add((node_1, weight))

    def adjc_str(self, key) -> str:
        out = "{"
        adj = self.graph[key] 
        tam = len(adj)
        for (index, a) in enumerate(adj):
            out += f"({a[0]}, {a[1]})"
            if index < tam:
               out += "," 

        return out + "}"

    def __str__(self):
        out = ""
        for key in self.graph.keys():
            if len(self.graph[key]) != 0:
                out += "Node" + str(key) + ": " + self.adjc_str(key) + "\n"
        return out


    """
    Funcao que calcula um caminho com dfs
    """
    def dfs(self, posicao_inicial: Node, posicoes_finais: list[tuple[int, int]], path: list[Node] = [], visited: set[Node] = set()) -> tuple[list[Node], int] | None:
        path.append(posicao_inicial)
        visited.add(posicao_inicial)

        if posicao_inicial.get_posicao() in posicoes_finais:
            return (path, 0)

        for (adjacent, custo) in self.graph[posicao_inicial]:
            if adjacent not in visited:
                resultado = self.dfs(adjacent, posicoes_finais, path, visited)
                if resultado is not None:
                    return (resultado[0], resultado[1] + custo)

        path.pop()
        return None

    """
    Funcao que calcula um caminho com bfs
    """
    def bfs(self, posicao_inicial: Node, posicoes_finais: list[tuple[int, int]]):
        visited = set()
        queue = Queue()

        queue.put(posicao_inicial)
        visited.add(posicao_inicial)

        parent = dict()
        parent[posicao_inicial] = None
        custos = dict()
        custos[posicao_inicial] = None

        path_found = False

        end = None

        while not queue.empty() and path_found == False:
            nodo_atual = queue.get()
            if nodo_atual.get_posicao() in posicoes_finais:
                end = Node(nodo_atual.get_posicao(), nodo_atual.get_velocidade())
                path_found = True
            else:
                for(adjacent, peso) in self.graph[nodo_atual]:
                    if adjacent not in visited:
                        queue.put(adjacent)
                        parent[adjacent] = nodo_atual
                        custos[adjacent] = peso
                        visited.add(adjacent)

        path = []
        custo = 0

        if path_found:
            path.append(end)
            custo += custos[end]
            while parent[end] is not None:
                path.append(parent[end])
                if custos[parent[end]] is not None:
                    custo += custos[parent[end]]
                end = parent[end]
            path.reverse()

        return (path, custo)

    def desenha(self):
        g = nx.Graph()
        for (nodo, adjacentes) in self.graph.items():
            g.add_node(nodo)
            for (adjacente, peso) in adjacentes:
                g.add_edge(nodo, adjacente, weight=peso) 
        
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()
