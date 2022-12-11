from vectorracer import VectorRacer
import matplotlib.pyplot as pl
from os import listdir

MAPS_DIR = "./maps"

def print_map(path_map: str) -> str:
    with open(path_map) as file:
        content = file.read()
        return content

def main():
    racer = VectorRacer()
    maps = listdir(MAPS_DIR)
    for i in range(len(maps)):
        maps[i] = MAPS_DIR + "/" + maps[i]

    mudar = True

    saida = -1
    while saida != 0:
        if mudar:
            print("1-Gerar mapa")
            print("2-Escolher mapa")
            map_choice = int(input()) 
            if map_choice == 2:
                for i in range(len(maps)):
                    print(f"{i + 1}-Mapa {i + 1}") 
                    print(print_map(maps[i]))
                print("Escolhe um mapa...")
                map_choice = int(input())
                if map_choice >= 1 and map_choice <= len(maps):
                    racer.load_map_from_file(maps[map_choice - 1])
                    mudar = False
                else:
                    print("Opção inválida")
            elif map_choice == 1:
                print("Insira o numero de linhas")
                linhas = int(input())
                print("Insira o numero de colunas")
                colunas = int(input())
                racer.gen_map(linhas, colunas)
                mudar = False
            # elif map_choice >= 2 and map_choice <= len(maps) + 1:
            else:
                print("Opção inválida")
        if not mudar:
            print("1-Imprimir grafo ")
            print("2-Desenhar Grafo")
            print("3-Imprimir  nodos de Grafo")
            print("4-Imprimir arestas de Grafo")
            print("5-DFS")
            print("6-BFS")
            print("7-Representa mapa")
            print("8-Mudar de Mapa")
            print("0-Sair")

            saida = int(input("introduza a sua opcao-> "))
            if saida == 0:
                print("saindo.......")
            elif saida == 1:
                print(racer.graphs[0])
                input("prima enter para continuar")
            elif saida == 2:
                racer.graphs[0].desenha()
            elif saida == 3:
                print(racer.graphs[0].print_nodes())
                input("prima enter para continuar")
            elif saida == 4:
                print(racer.graphs[0])
                input("prima enter para continuar")
            elif saida == 5:
                caminho = racer.dfs()
                if caminho is not None:
                    caminho_str = list(map(lambda nodo: str(nodo), caminho[0]))
                    print("caminho =", caminho_str, ", custo=", caminho[1])
            elif saida == 6:
                resultado_dfs = racer.bfs()
                if resultado_dfs is not None:
                    resultado_dfs_str = list(map(lambda node: str(node), resultado_dfs[0]))
                    print("caminho=",resultado_dfs_str, "custo=",resultado_dfs[1])
            elif saida == 7:
                mat = racer.get_map_as_matrix()
                print(mat)
                pl.imshow(racer.get_map_as_matrix())
                pl.show()
            elif saida == 8:
                print("Mudando de mapa")
                mudar = True
            else:
                print("you didn't add anything")
                input("prima enter para continuar")

if __name__ == "__main__":
    main()
