import os.path
from collections import defaultdict
from faker import Faker

DATA_PATH = "C:\\Users\\matak\\Desktop\\Dataset"
fake = Faker()

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

def antonis_function():
    triples=open(os.path.join(DATA_PATH, "MillionSongSubset", "AdditionalFiles", 'user_song_frequency.txt'), 'r')
    doubles=open(os.path.join(DATA_PATH, "MillionSongSubset", "AdditionalFiles", 'subset_unique_tracks.txt'), 'r')
    han_file=open(os.path.join(DATA_PATH,'Han_file.txt'), 'w')

    song_to_artist_dict={}
    user_to_artists=defaultdict(list)
    for line in doubles:
        tuple=line.strip().split("<SEP>")
        song_to_artist_dict[tuple[1]]=tuple[2]

    for line in triples:
        tuple=line.split("\t")
        user=tuple[0]
        try :
            artist=song_to_artist_dict[tuple[1]]
            if artist not in user_to_artists[user]:
                user_to_artists[user].append(artist)
        except:
            print("song not found: "+str(tuple[1]))

    for item in user_to_artists.keys():
        han_file.write(str(fake.name())+"\t"+str(user_to_artists[item])+"\n")



def main():
#    triplets = load_unique_artist_list()
    antonis_function()


if __name__ == "__main__":
    main()