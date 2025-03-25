#!/bin/bash

# Set PostgreSQL credentials
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=IMDb
export PGUSER=postgres
export PGPASSWORD=123

# Create a temporary directory for downloads in the current directory
TMP_DIR=$(mktemp -d)
if [ ! -d "$TMP_DIR" ]; then
    echo "Failed to create temporary directory. Exiting."
    exit 1
fi
echo "Temporary download folder created at: $TMP_DIR"

# Change into the temporary directory so that files are downloaded here
cd "$TMP_DIR" || { echo "Could not change into temporary directory. Exiting."; exit 1; }

# Define URLs for each file
URL_TITLE_AKAS="https://datasets.imdbws.com/title.akas.tsv.gz"
URL_TITLE_BASICS="https://datasets.imdbws.com/title.basics.tsv.gz"
URL_TITLE_CREW="https://datasets.imdbws.com/title.crew.tsv.gz"
URL_TITLE_EPISODE="https://datasets.imdbws.com/title.episode.tsv.gz"
URL_TITLE_PRINCIPALS="https://datasets.imdbws.com/title.principals.tsv.gz"
URL_TITLE_RATINGS="https://datasets.imdbws.com/title.ratings.tsv.gz"
URL_NAME_BASICS="https://datasets.imdbws.com/name.basics.tsv.gz"

# Define a download function that prefers wget, falling back to curl if wget is not found.
download_file() {
    local url="$1"
    local file
    file=$(basename "$url")
    echo "Downloading/updating ${file} into ${TMP_DIR}..."
    
    if command -v wget > /dev/null 2>&1; then
        # Use wget with timestamping (-N)
        wget -N "$url"
    else
        # If wget is not available, use curl.
        # --remote-time: sets the remote file's timestamp on local file.
        # -O: writes output to a file named as the remote.
        curl --remote-time -O "$url"
    fi

    if [ ! -f "$file" ]; then
        echo "Error: ${file} was not downloaded successfully."
        exit 1
    fi
}

# Download each file
download_file "$URL_TITLE_AKAS"
download_file "$URL_TITLE_BASICS"
download_file "$URL_TITLE_CREW"
download_file "$URL_TITLE_EPISODE"
download_file "$URL_TITLE_PRINCIPALS"
download_file "$URL_TITLE_RATINGS"
download_file "$URL_NAME_BASICS"

echo "All files downloaded. Proceeding with PostgreSQL operations..."

# Drop existing tables and create new ones in PostgreSQL
psql -d "$PGDATABASE" <<EOF
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
EOF

echo "Database schema refreshed."

# Function to load a file from the temporary folder into PostgreSQL
copy_file() {
    local filename="$1"
    local tablename="$2"
    echo "Loading ${filename} into table ${tablename}..."
    gunzip -c "${filename}" | psql -d "$PGDATABASE" -c "\copy ${tablename} FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', NULL '\\N', HEADER, QUOTE E'\x01')"
}

# Load each file into its respective table
copy_file "title.akas.tsv.gz"     title_akas
copy_file "title.basics.tsv.gz"    title_basics
copy_file "title.crew.tsv.gz"      title_crew
copy_file "title.episode.tsv.gz"   title_episode
copy_file "title.principals.tsv.gz" title_principals
copy_file "title.ratings.tsv.gz"   title_ratings
copy_file "name.basics.tsv.gz"     name_basics

echo "Data load complete."

# Change to the parent directory then remove the temporary directory and its contents
cd .. || exit 1
rm -rf "$TMP_DIR"
echo "Temporary folder removed. Process complete."