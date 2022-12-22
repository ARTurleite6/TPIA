from collections.abc import Callable
from graph import Node, Graph
from queue import Queue
from time import time

import math

class VectorRacer:
    """
    Classe que representa a maior parte do jogo do VectorRacer
    """

    def __init__(self):
        #Mapa
        self.map = []
        #posicao inicial('P') do mapa
        self.posicao_inicial = []
        #posicoes finais('F') do mapa
        self.posicoes_finais = []
        #representação do grafo pelo mapa
        self.graphs: list[Graph] = []

    """
    linhas: int: numero de linhas que novo mapa deve ter
    colunas: int: numero de colunas que novo mapa deve ter

    Funcao que gera um mapa recebendo um numero de linhas e colunas, o mapa gerado será random
    """
    # def gen_map(self, linhas: int, colunas: int):
    #     self.map = []
    #     self.graph.clear()
    #     self.posicoes_finais = []
    #     self.posicao_inicial = Node((0, 0))
    #     valid = False
    #     while not valid:
    #         map = []
    #         map.append(["X" for _ in range(colunas)])
    #         
    #         pieces = "X---"
    #         for i in range(1, linhas - 1):
    #             map.append(['X'])
    #             for _ in range(1, colunas - 1):
    #                 map[i].append(pieces[randint(0, 3)]) 
    #             map[i].append('X')
    #             # for j in range(colunas - 1):
    #             # map[i] += 
    #         # for i in range(1, linhas - 1):
    #         map[1][1] = "P"
    #         map.append(["X" for _ in range(colunas)])
    #
    #         posicao_inicial = randint(1, linhas - 1 - 3)
    #
    #         map[posicao_inicial][-1] = map[posicao_inicial + 1][-1] = map[posicao_inicial + 2][-1] = "F"
    #         for i in range(linhas):
    #             map[i] = "".join(map[i])
    #
    #         self.map = map
    #         self.posicao_inicial = Node((1, 1))
    #         self.posicoes_finais = [(posicao_inicial, colunas - 1), (posicao_inicial + 1, colunas - 1), (posicao_inicial + 1, colunas - 2)]
    #         self.load_graph()
    #         if self.dfs() is not None:
    #             for line in self.map:
    #                 print(line)
    #             valid = True
    #             
    """
    Função que transforma um caracter do mapa para um inteiro(codigo de caracter)
    """
    def __from_char_to_int__(self, sec: str) -> int:
        if sec == 'X':
            return 1
        elif sec == '-':
            return 2
        elif sec == 'F':
            return 3
        elif sec == 'P':
            return 4
        else:
            return 0
             
    def __has_car__(self, sec: int) -> int:
        return sec >= 5

    """
    Funcao que gera uma matriz a partir do mapa, colocando cara caracter pelo codigo correspondente
    """
    def get_map_as_matrix(self, map_to_use: list[str] | None = None) -> list[list[int]]:
        map = self.map if map_to_use is None else map_to_use
        mat = []
        for (i, line) in enumerate(map):
            mat.append([])
            for col in line:
                elem = self.__from_char_to_int__(col)
                mat[i].append(elem)

        return mat
                    

    """
    Funcao que calcula as posicoes finais do mapa, encontrando os caracteres F no mapa
    """
    def calcula_posicoes_finais(self):
        resultados: list[tuple[int, int]] = []
        for (i, line) in enumerate(self.map):
            for (j, column) in enumerate(line):
                if column == 'F':
                    resultados.append((i, j))
        return resultados
            

    def calcula_distancia_fim(self, node: tuple[int, int]):
        distancias = []
        for ponto in self.posicoes_finais:
            distancias.append(math.sqrt(math.pow(node[0] - ponto[0], 2) + math.pow(node[1] - ponto[1], 2)))
        return min(distancias)

    """
    Funcao que gera o grafo a partir do mapa definido, explorando as opções a partir de um estado 
    """
    def load_graph(self):
        for (posicao_inicial) in self.posicao_inicial:
            graph = Graph(True)
            nodo_inicial = posicao_inicial
            queue: Queue[tuple[Node, int]] = Queue()
            estados_visitados: set[tuple[Node, int]] = set()
            queue.put((nodo_inicial, 0))
            estados_visitados.add((nodo_inicial, 0))


            tempo = time()
            while not queue.empty():
                nodo_atual = queue.get() 
                estados_possiveis = self.estados_possiveis(nodo_atual[0])
    
                for estado in estados_possiveis:
                    if estado not in estados_visitados:
                        nodo_atual[0].set_heuristica(self.calcula_distancia_fim(nodo_atual[0].get_posicao()))
                        estado[0].set_heuristica(self.calcula_distancia_fim(nodo_atual[0].get_posicao()))
                        graph.add_edge(nodo_atual[0], estado[0], estado[1]) 
                        queue.put(estado)
                        estados_visitados.add(estado)
            fim = time()

            self.graphs.append(graph)


    """
    Funcao que calcula os estados possiveis a partir de um nodo
    """
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


    """
    Funcao que encontra a posicao inicial no mapa, ou seja, o caracter P
    """
    def calcula_posicoes_inicial(self):
        posicao_inicial = []
        found = False
        for (line, list) in enumerate(self.map):
            for (column, value) in enumerate(list):
                if value == 'P':
                    posicao_inicial.append((line, column))
                    found = True

        if not found:
            raise Exception("Posicao inicial não encontrada, insira um P no mapa")

        for posicao in posicao_inicial:
            self.posicao_inicial.append(Node(posicao))

        """
        Funcao que verifica se uma posicao se encontra nos limites do mapa
        """
    def check_bounds(self, position: list[int]) -> bool:
            return position[0] >= 0 and position[0] < len(self.map) and position[1] >= 0 and position[1] < len(self.map[0])


    """
    Funcao que testa se de uma posicao até outra com uma determinada velocidade colide ou não com uma parede
    A Funcao retorna (-1, -1) se nao tiver encontrado o final do mapa, e retorna a posicao final caso tenha encontrado um 'F' pelo caminho
    """
    def check_colision(self, posicao_atual: tuple[int, int], velocidade: tuple[int, int], posicao_final: tuple[int, int]) -> tuple[list[tuple[int, int]], tuple[int, int]] | None:
        path = []
        velocidade_atual = list(velocidade)
        current_position = list(posicao_atual)

        while (current_position[0] != posicao_final[0] or current_position[1] != posicao_final[1]) and velocidade_atual != [0, 0]:
            path.append((current_position[0], current_position[1]))
            if (self.map[current_position[0]][current_position[1]] == 'F'):
                return (path, (current_position[0], current_position[1]))
            if abs(velocidade_atual[0]) == abs(velocidade_atual[1]):
                pos_x = current_position[0]
                pos_y = current_position[1]
                if velocidade_atual[0] < 0:
                    pos_y = current_position[0] - 1
                elif velocidade_atual[0] > 0:
                    pos_y = current_position[0] + 1
                if velocidade_atual[1] < 0:
                    pos_x = current_position[1] - 1
                elif velocidade_atual[1] > 0:
                    pos_x = current_position[1] + 1
                if not self.check_bounds([pos_y, pos_x]) or (self.map[current_position[0]][pos_x] == 'X' and self.map[pos_y][current_position[1]] == 'X') or self.map[pos_y][pos_x] == 'X':
                    return None

                current_position = [pos_y, pos_x]
                if velocidade_atual[0] < 0:
                    velocidade_atual[0] += 1 
                elif velocidade_atual[0] > 0:
                     velocidade_atual[0] -= 1
                if velocidade_atual[1] < 0:
                    velocidade_atual[1] += 1 
                elif velocidade_atual[1] > 0:
                     velocidade_atual[1] -= 1
            elif abs(velocidade_atual[0]) > abs(velocidade_atual[1]):
                pos_y = current_position[0]
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
                pos_x = current_position[1]
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
                
                
        # path.append((current_position[0], current_position[1]))
        return (path, (-1, -1))
            
    """
    Funcao que calcula um par de Nodo e custo a partir de um estado aplicado a uma determinada aceleracao
    """
    def prox_posicao(self, estado: Node, aceleracao: tuple[int, int]) -> tuple[Node, int]:
        posicao_atual = estado.get_posicao()
        velocidade_atual = estado.get_velocidade()
        velocidade_nova = (velocidade_atual[0] + aceleracao[0], velocidade_atual[1] + aceleracao[1])
        posicao_nova = (posicao_atual[0] + velocidade_nova[0], posicao_atual[1] + velocidade_nova[1])
        custo = 1
        #Caso a nova posicao seja exatamente igual à anterior, ou seja nao possui velocidade nenhuma
        if posicao_nova == posicao_atual:
            return (Node(posicao_nova), 0)
        resultado = self.check_colision(posicao_atual, velocidade_nova, posicao_nova)
        #Houve alguma colisao
        if resultado is None:
            posicao_nova = posicao_atual
            velocidade_nova = (0, 0)
            custo = 25
        #caso em que no check_colision encontrou uma posicao final do mapa
        elif resultado[1] != (-1, -1):
            posicao_nova = resultado[1]
            velocidade_nova = (0, 0)
        estado_novo = Node(posicao_nova, velocidade_nova)
        return (estado_novo, custo)
        
    """
    Funcao que recebe um caminho para um ficheiro de texto com a localização do mapa, dando load ao mesmo
    """
    def load_map_from_file(self, file: str):
        self.graphs.clear()
        self.posicao_inicial.clear()
        self.posicoes_finais.clear()
        self.map: list[str] = []
        with open(file) as f:
            content = f.read().splitlines()
            for line in content:
                self.map.append(line)

        self.calcula_posicoes_inicial()
        self.posicoes_finais = self.calcula_posicoes_finais()
        self.load_graph()

    """
    Funcao que retorna uma string representando o estado do VectorRacer
    """
    def __str__(self):
        value = f"VectorRacer(posicao_inicial = {self.posicao_inicial}, \nmap = \n graph = {self.graphs}"
        for line in self.map:
            value += line + '\n'

        value += ");"
        return value

    """
    Funcao que calcula se existe colisao num determinado ponto entre todos os paths dados por um algoritmo
    """
    def __caminho_colisao__(self, index: int, my_path: list[Node], other_paths: list[list[Node]]) -> tuple[Node, Node, int] | None:
        for(n_node, node) in enumerate(my_path):
            for (n_path, path) in enumerate(other_paths):
                if(n_path == index):
                    break
                if n_node < len(path) - 1:
                    fst_velocidade = node.get_velocidade()
                    snd_velocidade = path[n_node].get_velocidade()
                    # Verificar a diferenca de velocidades dos carros num determinado ponto, para dar prioridade àquele que se deslocava com maior velocidade
                    if node.get_posicao() == path[n_node].get_posicao() and fst_velocidade[0] + fst_velocidade[1] < snd_velocidade[0] + snd_velocidade[1]:
                        return node, path[n_node], n_node
        
        return None
                

    """
    Funcao que a partir de uma lista de caminhos, tenta encontrar caminhos que não tenham colisões
    """
    def get_valid_paths(self, paths: list[tuple[list[Node], int]], algoritmo: Callable[[Graph, Node, list[tuple[int, int]], list[Node], set[Node]], tuple[list[Node], int] | None]) -> list[tuple[list[Node], int]]:
        for (i, path) in enumerate(paths):
            posicoes_colisoes = set()
            # verificar se existe alguma colisao nos caminhos atuais
            colisao = self.__caminho_colisao__(i, path[0], list(map(lambda path: path[0], paths)))
            new_path = path
            while colisao is not None:
                (fst, snd, _) = colisao
                fst_velocidade = fst.get_velocidade()
                snd_velocidade = snd.get_velocidade()
                # verificar as velocidades
                if fst_velocidade[0] + fst_velocidade[1] < snd_velocidade[0] + snd_velocidade[1]:
                    #adicionar ponto como ponto proibido na travessia, para que não volte a passar por lá
                    posicoes_colisoes.add(fst) 
                    # efetuar outra travessia com o algoritmo passado, para que calcule um caminho sem colisoes
                    new_path = algoritmo(self.graphs[i], self.posicao_inicial[i], self.posicoes_finais, [], posicoes_colisoes)
                    if new_path is None:
                        break
                        
                #verificar se novo caminho é válido
                colisao = self.__caminho_colisao__(i, new_path[0], list(map(lambda path: path[0], paths)))
            if new_path is not None:
                paths[i] = new_path
        return paths

    """
    Funcao que calcula o caminho através do algoritmo DFS 
    """
    def dfs(self) -> list[tuple[list[Node], int]]:
        ans: list[tuple[list[Node], int]] = []
        for (index, graph) in enumerate(self.graphs):
            caminho = graph.dfs(self.posicao_inicial[index], self.posicoes_finais, [], set())
            if caminho is not None:
                ans.append(caminho) 

        ans = self.get_valid_paths(ans, Graph.dfs)       
            
        return ans

    """
    Funcao que calcula um caminho através do algoritmo BFS
    """
    def bfs(self):
        ans: list[tuple[list[Node], int]] = []
        for(index, graph) in enumerate(self.graphs):
            caminho = graph.bfs(self.posicao_inicial[index], self.posicoes_finais, [], set())
            if caminho is not None:
                ans.append(caminho)

        ans = self.get_valid_paths(ans, Graph.bfs)
        return ans

    """
    Funcao que calcula um caminho através do algoritmo A_Star
    """
    def a_star(self):
        ans: list[tuple[list[Node], int]] = []
        for (index, graph) in enumerate(self.graphs):
            caminho = graph.bfs(self.posicao_inicial[index], self.posicoes_finais, [], set())
            if caminho is not None:
                ans.append(caminho)
        ans = self.get_valid_paths(ans, Graph.a_star)
        return ans

    """
    Funcao que calcula um caminho através do algoritmo Greedy
    """
    def greedy(self):
        ans: list[tuple[list[Node], int]] = []
        for (index, graph) in enumerate(self.graphs):
            caminho = graph.greedy(self.posicao_inicial[index], self.posicoes_finais, [], set())
            if caminho is not None:
                ans.append(caminho)
        ans = self.get_valid_paths(ans, Graph.greedy)
        return ans
        

    def show_path_map(self, paths: list[tuple[list[Node], int]]) -> list[list[int]]:
        mat = self.get_map_as_matrix()
        number_cars = len(paths)
        for (car, path) in enumerate(paths):
            for i in range(len(path[0]) - 1):
                current_point = path[0][i]
                next_point = path[0][i + 1]
                caminho = self.check_colision(current_point.get_posicao(), next_point.get_velocidade(), next_point.get_posicao())
                caminho = [] if caminho is None else caminho[0]
    
                for point in caminho:
                    if mat[point[0]][point[1]] >= 5 and mat[point[0]][point[1]] < number_cars + 5:
                        mat[point[0]][point[1]] = number_cars + 5
                    elif mat[point[0]][point[1]] < 5:
                        mat[point[0]][point[1]] = car + 5
            

        return mat
