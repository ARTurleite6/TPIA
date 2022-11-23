from vectorracer import VectorRacer
import matplotlib.pyplot as pl

def main():
    racer = VectorRacer("Circuito50X30.txt")
    racer.load_graph()

    saida = -1

    while saida != 0:
        print("1-Imprimir grafo ")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7-Representa mapa")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            print(racer.graph)
            input("prima enter para continuar")
        elif saida == 2:
            racer.graph.desenha()
        elif saida == 3:
            print(racer.graph.print_nodes())
            input("prima enter para continuar")
        elif saida == 4:
            print(racer.graph)
            input("prima enter para continuar")
        elif saida == 5:
            caminho = racer.dfs()
            if caminho is not None:
                caminho_str = list(map(lambda nodo: str(nodo), caminho[0]))
                print("caminho =", caminho_str)
        elif saida == 6:
            resultado_dfs = racer.bfs()
            if resultado_dfs is not None:
                resultado_dfs = list(map(lambda node: str(node), resultado_dfs[0]))
                print(resultado_dfs)
        elif saida == 7:
            mat = racer.get_map_as_matrix()
            print(mat)
            pl.imshow(racer.get_map_as_matrix())
            pl.show()
        else:
            print("you didn't add anything")
            input("prima enter para continuar")

if __name__ == "__main__":
    main()
