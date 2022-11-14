from vectorracer import VectorRacer

def main():
    racer = VectorRacer("map.txt")
    racer.load_graph()
    print(racer.graph)
    resultado_dfs = racer.dfs()
    if resultado_dfs is not None:
        resultado_dfs = list(map(lambda node: str(node), resultado_dfs[0]))
            
    resultado_bfs = list(map(lambda node: str(node), racer.bfs()[0]))

    print(resultado_dfs)
    print(resultado_bfs)
    # print(racer.check_colision((3, 1), (-1, 3), (2, 4)))

if __name__ == "__main__":
    main()
