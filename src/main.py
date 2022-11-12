from vectorracer import VectorRacer

def main():
    racer = VectorRacer("map.txt")
    racer.load_graph()
    print(racer.graph)
    # print(racer.check_colision((3, 1), (-1, 3), (2, 4)))

if __name__ == "__main__":
    main()
