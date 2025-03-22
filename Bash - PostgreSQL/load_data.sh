#!/bin/bash

# Set PostgreSQL credentials
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=IMDb
export PGUSER=postgres
export PGPASSWORD=123

echo "Dropping existing tables (if any) and creating new ones..."
psql -d $PGDATABASE <<EOF
DROP TABLE IF EXISTS title_akas;
DROP TABLE IF EXISTS title_basics;
DROP TABLE IF EXISTS title_crew;
DROP TABLE IF EXISTS title_episode;
DROP TABLE IF EXISTS title_principals;
DROP TABLE IF EXISTS title_ratings;
DROP TABLE IF EXISTS name_basics;

-- Create tables with plain text columns for array fields
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
EOF

# Function to load a file into PostgreSQL using gunzip and psql's \copy
copy_file() {
    local filename=$1
    local tablename=$2
    echo "Loading ${filename} into table ${tablename}..."
    gunzip -c ${filename} | psql -d $PGDATABASE -c "\copy ${tablename} FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', NULL '\\N', HEADER, QUOTE E'\x01')"
}

copy_file title.akas.tsv.gz   title_akas
copy_file title.basics.tsv.gz  title_basics
copy_file title.crew.tsv.gz    title_crew
copy_file title.episode.tsv.gz title_episode
copy_file title.principals.tsv.gz title_principals
copy_file title.ratings.tsv.gz title_ratings
copy_file name.basics.tsv.gz   name_basics

echo "Data load complete."