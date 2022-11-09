
class Node:
    def __init__(self, posicao: tuple[int, int], velocidade: tuple[int, int] = (0, 0)):
        self.posicao = posicao
        self.velocidade = velocidade 

    def get_posicao(self) -> tuple[int, int]:
        return self.posicao

    def get_velocidade(self) -> tuple[int, int]:
        return self.velocidade

    def __str__(self):
        return f"Node(posicao = {self.posicao}, {self.velocidade})"

    def __eq__(self, node) -> bool:
        if isinstance(node, Node):
            return self.posicao == node.posicao and self.velocidade == node.velocidade
        return False

    def __hash__(self) -> int:
        return hash((self.posicao, self.velocidade))

class VectorRacer:
    def __init__(self, file_map: str):
        self.load_map_from_file(file_map)
        self.calcula_posicao_inicial()

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

    def check_bounds(self, posicao: tuple[int, int]) -> bool:
        return posicao[0] < 0 and posicao[0] >= len(self.map) and posicao[1] < 0 and posicao[1] >= len(self.map[0])

    def check_position(self, posicao: tuple[int, int]) -> bool:
        return self.map[posicao[0]][posicao[1]] != '#' and self.check_position(posicao)
            
    def prox_posicao(self, estado: Node, aceleracao: tuple[int, int]) -> Node:
        posicao_atual = estado.get_posicao()
        velocidade_atual = estado.get_velocidade()
        velocidade_nova = (velocidade_atual[0] + aceleracao[0], velocidade_atual[1] + aceleracao[1])
        posicao_nova = (posicao_atual[0] + velocidade_nova[0], posicao_atual[1] + velocidade_nova[1])
        if not self.check_position(posicao_nova):
            posicao_nova = posicao_atual
            velocidade_nova = (0, 0)
        estado_novo = Node(posicao_nova, velocidade_nova)
        return estado_novo
        
    def load_map_from_file(self, file: str):
        self.map: list[str] = []
        with open(file) as f:
            content = f.read().splitlines()
            for line in content:
                self.map.append(line)

    def __str__(self):
        value = f"VectorRacer(posicao_inicial = {self.posicao_inicial}, \nmap = \n"
        for line in self.map:
            value += line + '\n'

        value += ");"
        return value

