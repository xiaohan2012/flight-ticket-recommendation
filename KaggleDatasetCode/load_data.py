import os.path

DATA_PATH = "data"

def load_triplets():
    file_path = os.path.join(DATA_PATH, 'kaggle_visible_evaluation_triplets.txt')
    f = open(file_path, 'r')

    triplets = []

    for line in f:
        triplets.append(line.strip().split('\t'))

    return triplets


def load_unique_artist_list():
    file_path =os.path.join(DATA_PATH, "MillionSongSubset", "AdditionalFiles", "subset_unique_artists.txt")

    artists = set()

    with open(file_path, "r") as f:
        for line in f:
            artist_name = line.strip().split('<SEP>')[3]
            artists.add(artist_name)

    return artists


def main():
    triplets = load_unique_artist_list()

    print(triplets)


if __name__ == "__main__":
    main()