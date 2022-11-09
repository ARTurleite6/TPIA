from vectorracer import VectorRacer

def main():
    racer = VectorRacer("map.txt")
    racer.load_graph()
    print(racer)

if __name__ == "__main__":
    main()
