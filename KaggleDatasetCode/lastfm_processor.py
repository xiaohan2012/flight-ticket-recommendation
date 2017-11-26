import sqlite3
import os.path
import json
from tqdm import tqdm

DATA_PATH = "data"


def process_file(cursor, file_path):
    path = os.path.join("..", "..", "data", file_path)

    data = None

    with open(path, "r") as f:
        for line in f:
            data = json.loads(line)

    if not data["similars"]:
        return

    try:
        sql_str = '''INSERT OR REPLACE INTO track_data VALUES ("{artist}", "{title}", "{track_id}","{timestamp}","{tags}")'''.format(
            artist=data["artist"].replace("\"", "'"),
            title=data["title"].replace("\"", "'"),
            track_id=data["track_id"],
            timestamp=data["timestamp"].replace("\"", "'"),
            tags=str(data["tags"]).replace("\"", "'"),
        )

        cursor.execute(sql_str)

        for similarity_rec in data["similars"]:
            target_track_id = similarity_rec[0]
            similarity = float(similarity_rec[1])

            cursor.execute('''INSERT OR REPLACE INTO track_similarity_data VALUES ("{}", "{}", {})'''.format(
                data["track_id"].replace("\"", "'"),
                target_track_id, similarity))
    except Exception as e:
        print(e)
        print(data)
        exit(0)


# exit(0)


def init_db(cursor):
    cursor.execute('''CREATE TABLE track_data
                 (artist TEXT, title TEXT, track_id TEXT PRIMARY KEY, timestamp TEXT, tags TEXT)''')


def main():
    path = os.path.join("..", "..", "data", "lastfm_train_files.txt")
    conn = sqlite3.connect('lastfm.db')
    c = conn.cursor()

    with open(path, "r") as f:
        for file_path in tqdm(f, mininterval=5, maxinterval=15):
            try:
                process_file(c, file_path.strip())
            except:
                print(file_path)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
