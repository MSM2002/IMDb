#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip
import psycopg2
import urllib.request
import tempfile

# PostgreSQL connection parameters – adjust as needed
PGHOST = 'localhost'
PGPORT = 5432
PGDATABASE = 'IMDb'
PGUSER = 'postgres'
PGPASSWORD = '123'

# List of tuples: (local filename, URL, target table name)
FILES = [
    ("title.akas.tsv.gz",      "https://datasets.imdbws.com/title.akas.tsv.gz",      "title_akas"),
    ("title.basics.tsv.gz",     "https://datasets.imdbws.com/title.basics.tsv.gz",     "title_basics"),
    ("title.crew.tsv.gz",       "https://datasets.imdbws.com/title.crew.tsv.gz",       "title_crew"),
    ("title.episode.tsv.gz",    "https://datasets.imdbws.com/title.episode.tsv.gz",    "title_episode"),
    ("title.principals.tsv.gz", "https://datasets.imdbws.com/title.principals.tsv.gz", "title_principals"),
    ("title.ratings.tsv.gz",    "https://datasets.imdbws.com/title.ratings.tsv.gz",    "title_ratings"),
    ("name.basics.tsv.gz",      "https://datasets.imdbws.com/name.basics.tsv.gz",      "name_basics")
]

# SQL commands to drop existing tables and create the new ones
TABLE_SETUP_SQL = """
DROP TABLE IF EXISTS title_akas;
DROP TABLE IF EXISTS title_basics;
DROP TABLE IF EXISTS title_crew;
DROP TABLE IF EXISTS title_episode;
DROP TABLE IF EXISTS title_principals;
DROP TABLE IF EXISTS title_ratings;
DROP TABLE IF EXISTS name_basics;

CREATE TABLE title_akas (
    titleId TEXT,
    ordering INTEGER,
    title TEXT,
    region TEXT,
    language TEXT,
    types TEXT,
    attributes TEXT,
    isOriginalTitle BOOLEAN
);

CREATE TABLE title_basics (
    tconst TEXT,
    titleType TEXT,
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult BOOLEAN,
    startYear INTEGER,
    endYear INTEGER,
    runtimeMinutes INTEGER,
    genres TEXT
);

CREATE TABLE title_crew (
    tconst TEXT,
    directors TEXT,
    writers TEXT
);

CREATE TABLE title_episode (
    tconst TEXT,
    parentTconst TEXT,
    seasonNumber INTEGER,
    episodeNumber INTEGER
);

CREATE TABLE title_principals (
    tconst TEXT,
    ordering INTEGER,
    nconst TEXT,
    category TEXT,
    job TEXT,
    characters TEXT
);

CREATE TABLE title_ratings (
    tconst TEXT,
    averageRating FLOAT,
    numVotes INTEGER
);

CREATE TABLE name_basics (
    nconst TEXT,
    primaryName TEXT,
    birthYear INTEGER,
    deathYear INTEGER,
    primaryProfession TEXT,
    knownForTitles TEXT
);
"""

def setup_database(conn):
    """Drops existing tables and creates new ones using TABLE_SETUP_SQL."""
    with conn.cursor() as cur:
        print("Dropping existing tables (if any) and creating new ones...")
        cur.execute(TABLE_SETUP_SQL)
    conn.commit()
    print("Tables have been set up successfully.")

def load_file_to_table(conn, gz_filepath, table_name):
    """
    Decompress the given .tsv.gz file and load its data into the specified table.
    Uses PostgreSQL's COPY command for efficient data load.
    """
    print(f"Loading {gz_filepath} into table {table_name}...")
    with gzip.open(gz_filepath, mode="rt", encoding="utf-8", errors="replace") as f:
        copy_sql = (
            f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', NULL '\\N', HEADER, QUOTE E'\x01')"
        )
        with conn.cursor() as cur:
            cur.copy_expert(sql=copy_sql, file=f)
        conn.commit()
    print(f"Finished loading data from {gz_filepath} into table {table_name}.")

def download_file(url, destination):
    """Download a file from the given URL to the destination path."""
    print(f"Downloading {url} to {destination} ...")
    try:
        urllib.request.urlretrieve(url, destination)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    # Create a temporary directory for downloads.
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"Temporary directory created at {tmpdirname}")
        
        # Download each file into the temporary directory.
        for filename, url, _ in FILES:
            dest_path = os.path.join(tmpdirname, filename)
            download_file(url, dest_path)
        
        # Connect to the PostgreSQL database using provided credentials.
        try:
            conn = psycopg2.connect(
                host=PGHOST,
                port=PGPORT,
                dbname=PGDATABASE,
                user=PGUSER,
                password=PGPASSWORD
            )
        except Exception as e:
            print("Error connecting to PostgreSQL:", e)
            return

        # Set up database tables.
        setup_database(conn)

        # Load each downloaded file into its corresponding table.
        for filename, _, table_name in FILES:
            filepath = os.path.join(tmpdirname, filename)
            if not os.path.exists(filepath):
                print(f"Error: File '{filepath}' not found. Skipping table {table_name}.")
                continue
            load_file_to_table(conn, filepath, table_name)

        conn.close()
        print("Data load complete.")

if __name__ == '__main__':
    main()