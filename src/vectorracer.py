from graph import Node, Graph
from queue import Queue

class VectorRacer:
    def __init__(self, file_map: str):
        self.load_map_from_file(file_map)
        self.calcula_posicao_inicial()
        self.graph = Graph(True)

    def load_graph(self):
        nodo_inicial = Node(self.posicao_inicial)
        queue: Queue[tuple[Node, int]] = Queue()
        queue.put((nodo_inicial, 0))
        estados_visitados: set[tuple[Node, int]] = set()

        while not queue.empty():
            nodo_atual = queue.get() 
            # print("nodo=", nodo_atual[0], "custo=", nodo_atual[1])
            estados_visitados.add(nodo_atual)
            estados_possiveis = self.estados_possiveis(nodo_atual[0])

            for estado in estados_possiveis:
                if estado not in estados_visitados:
                    self.graph.add_edge(nodo_atual[0], estado[0], estado[1]) 
                    queue.put(estado)


    def estados_possiveis(self, estado: Node) -> set[tuple[Node, int]]:
        aceleracoes_possiveis = [
            (0, 0),
            (0, 1),
            (0, -1),
            (1, 0),
            (1, 1),
            (1, -1),
            (-1, 0),
            (-1, 1),
            (-1, -1)
        ]

        estados = set()
    
        for aceleracao in aceleracoes_possiveis:
            estados.add(self.prox_posicao(estado, aceleracao))

        return estados

    def calcula_posicao_inicial(self):
        posicao_inicial = (0, 0)
        found = False
        for (line, list) in enumerate(self.map):
            for (column, value) in enumerate(list):
                if value == 'P':
                    posicao_inicial = (line, column)
                    found = True
                    break
            if found:
                break

        if not found:
            raise Exception("Posicao inicial não encontrada, insira um P no mapa")

        self.posicao_inicial: tuple[int, int] = posicao_inicial

    def check_colision(self, posicao_atual: tuple[int, int], velocidade: tuple[int, int], posicao_final: tuple[int, int]) -> bool:

        if posicao_final[0] >= len(self.map) or posicao_final[0] < 0 or posicao_final[1] >= len(self.map[0]) or posicao_final[1] < 0 or self.map[posicao_final[0]][posicao_final[1]]:
            return False

        velocidade_list = [velocidade[0], velocidade[1]]

        current_position = [posicao_atual[0], posicao_atual[1]]
        while current_position != posicao_final:
            if abs(velocidade_list[0]) != abs(velocidade_list[1]):
                pass
            else:
                pass

        return True
            
    def prox_posicao(self, estado: Node, aceleracao: tuple[int, int]) -> tuple[Node, int]:
        posicao_atual = estado.get_posicao()
        velocidade_atual = estado.get_velocidade()
        velocidade_nova = (velocidade_atual[0] + aceleracao[0], velocidade_atual[1] + aceleracao[1])
        posicao_nova = (posicao_atual[0] + velocidade_nova[0], posicao_atual[1] + velocidade_nova[1])
        custo = 1
        if posicao_nova == posicao_atual:
            return (Node(posicao_nova), 0)
        if not self.check_colision(posicao_atual, velocidade_nova, posicao_nova):
            posicao_nova = posicao_atual
            velocidade_nova = (0, 0)
            custo = 25
        estado_novo = Node(posicao_nova, velocidade_nova)
        return (estado_novo, custo)
        
    def load_map_from_file(self, file: str):
        self.map: list[str] = []
        with open(file) as f:
            content = f.read().splitlines()
            for line in content:
                self.map.append(line)

    def __str__(self):
        value = f"VectorRacer(posicao_inicial = {self.posicao_inicial}, \nmap = \n graph = {self.graph}"
        for line in self.map:
            value += line + '\n'

        value += ");"
        return value

