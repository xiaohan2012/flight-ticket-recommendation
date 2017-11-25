import os.path

DATA_PATH = "data"

def load_triplets():
    file_path = os.path.join(DATA_PATH, 'kaggle_visible_evaluation_triplets.txt')
    f = open(file_path, 'r')

    triplets = []

    for line in f:
        triplets.append(line.strip().split('\t'))

    return triplets


def main():
    triplets = load_triplets()

    print(triplets)


if __name__ == "__main__":
    main()