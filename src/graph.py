
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








