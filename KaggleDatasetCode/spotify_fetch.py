import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from load_data import load_unique_artist_list
from graphviz import Graph
from collections import defaultdict
import pickle

CREDENTIALS_PATH = "credentials.json"
SIMILAR_ARTISTS_URL = "https://api.spotify.com/v1/artists/{id}/related-artists"


def fetch_artist_id(sp, artist_name):
    try:
        search_results = sp.search(artist_name, limit=3, type="artist")
        artist_id = search_results["artists"]["items"][0]["id"]

        return artist_id
    except:
        return None


def fetch_similar_artists(sp, artist_id):
    try:
        relevant_artists_json = sp.artist_related_artists(artist_id)

        return [(artist["name"], artist["id"]) for artist in relevant_artists_json["artists"]]
    except IndexError as e:
        return None


def construct_artist_graph(edge_tuples):
    edges = defaultdict(lambda: [])

    for (a1, a2) in edge_tuples:
        edges[a1].append(a2)
        edges[a2].append(a1)

    return edges


def render_graph(edges):
    dot = Graph(comment='Artists', strict=True)

    for node in edges.keys():
        dot.node(node)

        for n in edges[node]:
            dot.node(n)
            dot.edge(node, n)

    dot.render('test-output/artists', view=True)


def phase1(sp):
    unique_artists = load_unique_artist_list()

    tuple_list = []
    i = 0

    with open("similar.txt", "w") as f:
        for artist in unique_artists:
            try:
                artist_id = fetch_artist_id(sp, artist)

                if not artist_id: continue

                similar_artists = fetch_similar_artists(sp, artist_id)

                if not similar_artists: continue

                for similar_artist in similar_artists:
                    tuple_list.append((artist, similar_artist))
                    print("{}<SEP>{}<SEP>{}<SEP>{}".format(artist_id, similar_artist[1], artist, similar_artist[0]), file=f, flush=True)

                i += 1
                if i % 250 == 0: print("At {}".format(i))
            except:
                print("Failed for artist: {}".format(artist))
                continue


def phase2(tuple_list):
    graph = construct_artist_graph(tuple_list)

    graph = dict(graph)

    with open("graph", 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

    render_graph(graph)


def main():
    with open(CREDENTIALS_PATH) as f:
        credentials_json = json.load(f)

    client_credentials_manager = SpotifyClientCredentials(client_id=credentials_json["CLIENT_ID"], client_secret=credentials_json["CLIENT_SECRET"])

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    phase1(sp)


if __name__ == "__main__":
    main()