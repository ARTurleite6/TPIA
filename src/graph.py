from queue import Queue

class Node:
    def __init__(self, posicao: tuple[int, int], velocidade: tuple[int, int] = (0, 0)):
        self.posicao = posicao
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
    def __init__(self, directed=False):
        self.directed: bool = directed
        self.graph: dict[Node, set[tuple[Node, int]]] = {}
        self.heuristics = {} # ainda nao sei se vai ficar


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
            out = out + "node" + str(key) + ": " + self.adjc_str(key) + "\n"
        return out


    def dfs(self, posicao_inicial: Node, posicoes_finais: list[tuple[int, int]], path: list[Node] = [], visited: set[Node] = set()) -> tuple[list[Node], int] | None:
        path.append(posicao_inicial)
        visited.add(posicao_inicial)

        print(posicao_inicial.get_posicao())

        if posicao_inicial.get_posicao() in posicoes_finais:
            return (path, 0)

        for (adjacent, custo) in self.graph[posicao_inicial]:
            if adjacent not in visited:
                resultado = self.dfs(adjacent, posicoes_finais, path, visited)
                if resultado is not None:
                    return resultado

        path.pop()
        return None
    
    def bfs(self, posicao_inicial: Node, posicoes_finais: list[tuple[int, int]]):
        visited = set()
        queue = Queue()

        queue.put(posicao_inicial)
        visited.add(posicao_inicial)

        parent = dict()
        parent[posicao_inicial] = None

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
                        visited.add(adjacent)

        path = []
        custo = 0

        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()

            custo = 0
        return (path, custo)






