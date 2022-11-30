from graph import Node, Graph
from queue import Queue
from random import randint

class VectorRacer:
    def __init__(self):
        self.map = []
        self.posicao_inicial = Node((0, 0))
        self.posicoes_finais = []
        self.graph = Graph(True)

    def gen_map(self, linhas: int, colunas: int):
        valid = False
        while not valid:
            map = []
            map.append(["X" for _ in range(colunas)])
            
            pieces = "X-----"
            for i in range(1, linhas - 1):
                map.append(['X'])
                for _ in range(1, colunas - 1):
                    map[i].append(pieces[randint(0, 5)]) 
                map[i].append('X')
                # for j in range(colunas - 1):
                # map[i] += 
            # for i in range(1, linhas - 1):
            map[1][1] = "P"
            map.append(["X" for _ in range(colunas)])

            posicao_inicial = randint(1, linhas - 1 - 3)

            map[posicao_inicial][-1] = map[posicao_inicial + 1][-1] = map[posicao_inicial + 2][-1] = "F"
            for i in range(linhas):
                map[i] = "".join(map[i])

            self.map = map
            self.posicao_inicial = Node((1, 1))
            self.posicoes_finais = [(posicao_inicial, colunas - 1), (posicao_inicial + 1, colunas - 1), (posicao_inicial + 1, colunas - 2)]
            self.load_graph()
            if self.dfs() is not None:
                for line in self.map:
                    print(line)
                valid = True
                
                

    def __from_char_to_int__(self, sec: str) -> int:
        if sec == 'X':
            return 0
        elif sec == '-':
            return 1
        elif sec == 'F':
            return 2
        elif sec == 'P':
            return 3
        else:
            return 0
             

    def get_map_as_matrix(self) -> list[list[int]]:
        mat = []
        for (i, line) in enumerate(self.map):
            mat.append([])
            for col in line:
                elem = self.__from_char_to_int__(col)
                mat[i].append(elem)

        return mat
                    

    def calcula_posicoes_finais(self):
        resultados: list[tuple[int, int]] = []
        for (i, line) in enumerate(self.map):
            for (j, column) in enumerate(line):
                if column == 'F':
                    resultados.append((i, j))
        return resultados
            

    def load_graph(self):
        nodo_inicial = self.posicao_inicial
        queue: Queue[tuple[Node, int]] = Queue()
        queue.put((nodo_inicial, 0))
        estados_visitados: set[tuple[Node, int]] = set()

        i = 0;
        while not queue.empty():
            i += 1
            nodo_atual = queue.get() 
            estados_visitados.add(nodo_atual)
            estados_possiveis = self.estados_possiveis(nodo_atual[0])

            for estado in estados_possiveis:
                if estado not in estados_visitados:
                    self.graph.add_edge(nodo_atual[0], estado[0], estado[1]) 
                    queue.put(estado)


    def estados_possiveis(self, estado: Node) -> set[tuple[Node, int]]:
        if not self.check_bounds(list(estado.get_posicao())):
            return set()

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

        self.posicao_inicial: Node = Node(posicao_inicial)

    def check_bounds(self, position: list[int]) -> bool:
            return position[0] >= 0 and position[0] < len(self.map) and position[1] >= 0 and position[1] < len(self.map[0])

    def check_colision(self, posicao_atual: tuple[int, int], velocidade: tuple[int, int], posicao_final: tuple[int, int]) -> tuple[int, int] | None:
        velocidade_atual = list(velocidade)
        current_position = list(posicao_atual)

        index = 0
        while current_position[0] != posicao_final[0] or current_position[1] != posicao_final[1]:
            if (self.map[current_position[0]][current_position[1]] == 'F'):
                return (current_position[0], current_position[1])
            if abs(velocidade_atual[0]) == abs(velocidade_atual[1]):
                if velocidade_atual[0] < 0:
                    pos_y = current_position[0] - 1
                else:
                    pos_y = current_position[0] + 1
                if velocidade_atual[1] < 0:
                    pos_x = current_position[1] - 1
                else:
                    pos_x = current_position[1] + 1
                if not self.check_bounds([pos_y, pos_x]) or (self.map[current_position[0]][pos_x] == 'X' and self.map[pos_y][current_position[1]] == 'X') or self.map[pos_y][pos_x] == 'X':
                    return None

                current_position = [pos_y, pos_x]
                if velocidade_atual[0] < 0:
                    velocidade_atual[0] += 1 
                else:
                     velocidade_atual[0] -= 1
                if velocidade_atual[1] < 0:
                    velocidade_atual[1] += 1 
                else:
                     velocidade_atual[1] -= 1
            elif abs(velocidade_atual[0]) > abs(velocidade_atual[1]):
                if velocidade_atual[0] < 0:
                    pos_y = current_position[0] - 1
                else:
                    pos_y = current_position[0] + 1
                if not self.check_bounds([pos_y, current_position[1]]) or(self.map[pos_y][current_position[1]] == 'X'):
                    return None
                
                current_position = [pos_y, current_position[1]]
                if velocidade_atual[0] < 0:
                    velocidade_atual[0] += 1 
                else:
                    velocidade_atual[0] -= 1
            elif abs(velocidade_atual[0]) < abs(velocidade_atual[1]):
                if velocidade_atual[1] < 0:
                    pos_x = current_position[1] - 1
                else:
                    pos_x = current_position[1] + 1

                if not self.check_bounds([current_position[0], pos_x]) or(self.map[current_position[0]][pos_x] == 'X'):
                    return None
                
                current_position = [current_position[0], pos_x]
                if velocidade_atual[1] < 0:
                    velocidade_atual[1] += 1 
                else:
                    velocidade_atual[1] -= 1
                
                
        return (-1, -1)
            
    def prox_posicao(self, estado: Node, aceleracao: tuple[int, int]) -> tuple[Node, int]:
        posicao_atual = estado.get_posicao()
        velocidade_atual = estado.get_velocidade()
        velocidade_nova = (velocidade_atual[0] + aceleracao[0], velocidade_atual[1] + aceleracao[1])
        posicao_nova = (posicao_atual[0] + velocidade_nova[0], posicao_atual[1] + velocidade_nova[1])
        custo = 1
        if posicao_nova == posicao_atual:
            return (Node(posicao_nova), 0)
        resultado = self.check_colision(posicao_atual, velocidade_nova, posicao_nova)
        if resultado is None:
            posicao_nova = posicao_atual
            velocidade_nova = (0, 0)
            custo = 25
        elif resultado != (-1, -1):
            posicao_nova = resultado
            velocidade_nova = (0, 0)
        estado_novo = Node(posicao_nova, velocidade_nova)
        return (estado_novo, custo)
        
    def load_map_from_file(self, file: str):
        self.map: list[str] = []
        with open(file) as f:
            content = f.read().splitlines()
            for line in content:
                self.map.append(line)

        self.calcula_posicao_inicial()
        self.posicoes_finais = self.calcula_posicoes_finais()
        self.load_graph()

    def __str__(self):
        value = f"VectorRacer(posicao_inicial = {self.posicao_inicial}, \nmap = \n graph = {self.graph}"
        for line in self.map:
            value += line + '\n'

        value += ");"
        return value

    def dfs(self):
        return self.graph.dfs(self.posicao_inicial, self.posicoes_finais)

    def bfs(self):
        return self.graph.bfs(self.posicao_inicial, self.posicoes_finais)
