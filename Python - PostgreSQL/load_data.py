#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import gzip
import psycopg2

# PostgreSQL connection parameters – adjust as needed
PGHOST = 'localhost'
PGPORT = 5432
PGDATABASE = 'IMDb'
PGUSER = 'postgres'
PGPASSWORD = '1234'

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
    types TEXT,        -- originally an array, stored as plain text (e.g., "original")
    attributes TEXT,   -- originally an array, stored as plain text
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
    genres TEXT         -- originally an array, stored as plain text (e.g., "Documentary,Short")
);

CREATE TABLE title_crew (
    tconst TEXT,
    directors TEXT,    -- originally an array, stored as plain text
    writers TEXT       -- originally an array, stored as plain text
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
    primaryProfession TEXT,  -- originally an array, stored as plain text
    knownForTitles TEXT       -- originally an array, stored as plain text
);
"""

def setup_database(conn):
    """Drops existing tables and creates new ones using the TABLE_SETUP_SQL."""
    with conn.cursor() as cur:
        print("Dropping existing tables (if any) and creating new ones...")
        cur.execute(TABLE_SETUP_SQL)
    conn.commit()
    print("Tables have been set up successfully.")

def load_file_to_table(conn, gz_filename, table_name):
    """
    Decompress the given .tsv.gz file and load its data into the specified table.
    Uses PostgreSQL's COPY command for efficient data load.
    """
    print(f"Loading {gz_filename} into table {table_name}...")
    # Open the gzip file in text mode; adjust encoding if necessary.
    with gzip.open(gz_filename, mode="rt", encoding="utf-8", errors="replace") as f:
        # COPY command with parameters matching the original shell script options.
        copy_sql = (
            f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', NULL '\\N', HEADER, QUOTE E'\x01')"
        )
        with conn.cursor() as cur:
            cur.copy_expert(sql=copy_sql, file=f)
        conn.commit()
    print(f"Finished loading data from {gz_filename} into table {table_name}.")

def main():
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

    # Set up tables in the database.
    setup_database(conn)

    # List of (filename, target table name) tuples.
    files = [
        ("title.akas.tsv.gz",   "title_akas"),
        ("title.basics.tsv.gz",  "title_basics"),
        ("title.crew.tsv.gz",    "title_crew"),
        ("title.episode.tsv.gz", "title_episode"),
        ("title.principals.tsv.gz", "title_principals"),
        ("title.ratings.tsv.gz", "title_ratings"),
        ("name.basics.tsv.gz",   "name_basics")
    ]

    # Process each file: check its existence and load it.
    for gz_file, table_name in files:
        if not os.path.exists(gz_file):
            print(f"Error: File '{gz_file}' not found in {os.getcwd()}. Skipping.")
            continue
        load_file_to_table(conn, gz_file, table_name)

    conn.close()
    print("Data load complete.")

if __name__ == '__main__':
    main()