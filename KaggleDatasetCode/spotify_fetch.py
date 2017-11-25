import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from load_data import load_unique_artist_list
from graphviz import Graph
from collections import defaultdict
import pickle

CREDENTIALS_PATH = "credentials.json"
SIMILAR_ARTISTS_URL = "https://api.spotify.com/v1/artists/{id}/related-artists"


def fetch_similar_artists(sp, artist_name):
    try:
        search_results = sp.search(artist_name, limit=3, type="artist")
        artist_id = search_results["artists"]["items"][0]["id"]

        relevant_artists_json = sp.artist_related_artists(artist_id)

        return [(artist["name"], artist["id"]) for artist in relevant_artists_json["artists"]]
    except IndexError as e:
        return None



def construct_artist_graph(sp, unique_artist_set):
    i = 0
    edges = defaultdict(lambda: [])

    for artist in unique_artist_set:
        similar_artists = fetch_similar_artists(sp, artist)

        if not similar_artists: continue

        for similar_artist in similar_artists:

            edges[similar_artist[0]].append(artist)
            edges[artist].append(similar_artist[0])

        i += 1
        if i % 100 == 0: print("At line {}".format(i))
        #if i == 3: return edges


def render_graph(edges):
    dot = Graph(comment='Artists', strict=True)

    for node in edges.keys():
        dot.node(node)

        for n in edges[node]:
            dot.node(n)
            dot.edge(node, n)

    dot.render('test-output/artists', view=True)


def main():
    with open(CREDENTIALS_PATH) as f:
        credentials_json = json.load(f)

    client_credentials_manager = SpotifyClientCredentials(client_id=credentials_json["CLIENT_ID"], client_secret=credentials_json["CLIENT_SECRET"])

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    graph = construct_artist_graph(sp, load_unique_artist_list())

    graph = dict(graph)

    with open("graph", 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

    render_graph(graph)




if __name__ == "__main__":
    main()