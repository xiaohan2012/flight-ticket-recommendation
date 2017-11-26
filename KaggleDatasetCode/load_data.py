import os.path
from collections import defaultdict
from faker import Faker
import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
import pickle

DATA_PATH = "data"
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
    triples=open(os.path.join(DATA_PATH, 'kaggle_visible_evaluation_triplets.txt'), 'r')
    doubles=open(os.path.join(DATA_PATH, "MillionSongSubset", "AdditionalFiles", 'subset_unique_tracks.txt'), 'r')

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
            continue
            # print("song not found: "+str(tuple[1]))


    return song_to_artist_dict, user_to_artists


def write_han_file(user_to_artists):
    han_file=open(os.path.join(DATA_PATH,'Han_file.txt'), 'w')

    for item in user_to_artists.keys():
        han_file.write(str(fake.name()) + "\t" + str(user_to_artists[item]) + "\n")


def aggregate_artist_plays_for_users(song_to_artists, user_to_artists):
    triples=open(os.path.join(DATA_PATH, 'kaggle_visible_evaluation_triplets.txt'), 'r')

    unique_artists = set()
    play_data = {}

    for line in triples:
        [user, song, num_plays] = line.split("\t")

        if song not in song_to_artists:
            continue

        artist = song_to_artists[song]

        unique_artists.add(artist)

        if user not in play_data:
            play_data[user] = {}

        if artist not in play_data[user]:
            play_data[user][artist] = 0

        play_data[user][artist] += int(num_plays)


    num_users = len(user_to_artists)
    num_artists = len(unique_artists)

    users = list(user_to_artists.keys())
    artists = list(unique_artists)

    #user_artist_matrix = sparse.lil_matrix((num_users, num_artists))
    user_artist_matrix = np.zeros((num_users, num_artists))

    # Horrible - emre
    for user in users:
        for artist in play_data[user]:
            row_index = users.index(user)
            col_index = artists.index(artist)

            user_artist_matrix[row_index, col_index] = play_data[user][artist]

    return users, artists, user_artist_matrix



def main():
    #song_to_artists, user_to_artists = antonis_function()
    #users, artists, user_artist_matrix = aggregate_artist_plays_for_users(song_to_artists, user_to_artists)

    #with open("uam.matrix", "wb") as f:
    #    pickle.dump(user_artist_matrix, f)
    return



if __name__ == "__main__":
    main()