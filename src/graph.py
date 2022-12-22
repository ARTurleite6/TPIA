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
        self.heuristica = 1000

        """
        Funcao que coloca o valor da heuristica no ponto
        """
    def set_heuristica(self, heuristica):
        self.heuristica = heuristica

        """
        Funcao que retorna o valor da heuristica do ponto, que será 1000 por defeito
        """
    def get_heuristica(self) -> int:
        return self.heuristica

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
    Funcao que transforma os nodos numa lista de strings
    """
    def print_nodes(self) -> list[str]:
        keys = self.graph.keys()
        keys = list(map(lambda node : str(node), keys))
        return keys

    def ja_tem_adjacencia(self, nodo: Node, nodo_2: Node, peso: int):
        if nodo not in self.graph or nodo_2 not in self.graph:
            return False
        return (nodo_2, peso) in self.graph[nodo]

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

    """
    Funcao que retorna uma string, para representar as adjacencias do grafo
    """
    def adjc_str(self, key) -> str:
        out = "{"
        adj = self.graph[key] 
        tam = len(adj)
        for (index, a) in enumerate(adj):
            out += f"({a[0]}, {a[1]})"
            if index < tam:
               out += "," 

        return out + "}"

    """
    Funcao que transforma o grafo em string
    """
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
        # Ponto adicionado ao caminho
        path.append(posicao_inicial)
        # ponto adicionado à colecao de pontos já visitados
        visited.add(posicao_inicial)

        # Caso em que o carro já chegou ao fim
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
    Funcao que calcula o valor minimo de heuristicas presentes em heurist, que possui um dicionario de Node para heuristica
    """
    def calcula_est(self, heurist: dict[Node, int]) -> Node:
        values = list(heurist)
        min = heurist[values[0]]
        node = values[0]
        for value in values:
            atual = heurist[value]
            if atual < min:
                min = atual 
                node = value
        return  node

    """
    Funcao que calcula um caminho através do algoritmo do a*
    O Codigo segue uma heurística em que considera a distancia em linha reta até à meta
    """
    def a_star(self, start: Node, end: list[tuple[int, int]], _: list[Node] = [], ignorados: set[Node] = set()) -> tuple[list[Node], int] | None:
        open_list = {start}
        closed_list = set([])

        g = {}
        g[start] = 0
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            calc_heurist = {} 
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1  
                    calc_heurist[v] = g[v] + v.get_heuristica()
                if flag == 1:
                    min_estima = self.calcula_est(calc_heurist)
                    n = min_estima
                if n == None:
                    print("Path does not exist!")
                    return None
            if n is not None and n.get_posicao() in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
    
                reconst_path.append(start)
    
                reconst_path.reverse()

                    #print('Path found: {}'.format(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))
            

            if n is not None:
                # for all neighbors of the current node do
                for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                    # if the current node isn't in both open_list and closed_list
                    # add it to open_list and note n as it's parent
                    if m not in ignorados and m not in open_list and m not in closed_list:
                        open_list.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                    # otherwise, check if it's quicker to first visit n, then m
                    # and if it is, update parent data and g data
                    # and if the node was in the closed_list, move it to open_list
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n
                            if m in closed_list:
                                closed_list.remove(m)
                                open_list.add(m)

                    # remove n from the open_list, and add it to closed_list
                    # because all of his neighbors were inspected
                open_list.remove(n)
                closed_list.add(n)

        print('Path does not exist!')
        return None

    """
    Funcao que retorna a lista de adjacencias acompanhadas pelo seu custo de um determinado nodo
    """
    def getNeighbours(self, node: Node) -> list[tuple[Node, int]]:
        lista = []
        if node in self.graph:
            for adjacencia in self.graph[node]:
                lista.append(adjacencia)
        return lista


    """
    Funcao que calcula um caminho com bfs
    """
    def bfs(self, posicao_inicial: Node, posicoes_finais: list[tuple[int, int]], path: list[Node] = [], visited: set[Node] = set()) -> tuple[list[Node], int] | None:
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

    """
    Funcao que calcula o custo de um caminho
    """
    def calcula_custo(self, path: list[Node]):
        custo = 0
        for i in range(len(path) - 1):
            current_node = path[i]
            prox_node = path[i + 1]
            for (adj, custo_adj) in self.graph[current_node]:
                if adj == prox_node:
                    custo += custo_adj 
                    break

        return custo

    ##########################################
    #   Greedy
    ##########################################

    def greedy(self, start: Node, end: list[tuple[int, int]], path: list[Node] = [], ignorados: set[Node] = set()) -> tuple[list[Node], int] | None:
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for v in open_list:
                if n == None or v.get_heuristica() < n.get_heuristica():
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n.get_posicao() in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in ignorados and m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        return None
