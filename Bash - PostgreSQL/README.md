# IMDb PostgreSQL Data Loader

This repository contains a Bash script to set up and populate a PostgreSQL database with IMDb data. The script performs the following tasks:

1. Drops any existing tables related to IMDb data.
2. Creates new tables with appropriate schema definitions.
3. Loads the IMDb TSV data files (compressed with gzip) into the newly created tables.

## Prerequisites

Before running the script, ensure you have the following installed on your system:

- [PostgreSQL](https://www.postgresql.org/) (with the `psql` command-line utility)
- [Gunzip](https://www.gnu.org/software/gzip/) (or a similar utility to decompress gzip files)
- Bash

You also need the IMDb TSV data files (compressed as `.gz`), which should be located in the same directory (download from: https://datasets.imdbws.com/) as the script:
- `title.akas.tsv.gz`
- `title.basics.tsv.gz`
- `title.crew.tsv.gz`
- `title.episode.tsv.gz`
- `title.principals.tsv.gz`
- `title.ratings.tsv.gz`
- `name.basics.tsv.gz`

## Configuration

The script sets the following environment variables to establish the PostgreSQL connection:

- `PGHOST`: Hostname of the PostgreSQL server (default: `localhost`)
- `PGPORT`: Port on which PostgreSQL is running (default: `5432`)
- `PGDATABASE`: Name of the database (default: `IMDb`)
- `PGUSER`: PostgreSQL user (default: `postgres`)
- `PGPASSWORD`: Password for the PostgreSQL user (default: `123`)

**Note:** Adjust these variables in the script if your PostgreSQL configuration is different or set them in your shell environment beforehand.

## How It Works

- The script starts by dropping any existing tables with the names:
  - title_akas, title_basics, title_crew, title_episode, title_principals, title_ratings, name_basics.
- It then creates fresh tables using SQL commands. Some fields that are originally arrays in the IMDb dataset are stored as plain text.
- A helper function (`copy_file`) uses `gunzip` and PostgreSQL's `\copy` command to load each TSV file into its corresponding table.

## Running the Script

1. Open a terminal in the directory containing the script and the IMDb TSV files.
2. Make the script executable (if it isn't already):
```bash
chmod +x load_data.sh
```

3. Run the script:
```bash
./load_data.sh
```

The script will output log messages to the console as it drops, creates tables, and loads each file. When the process is complete, you will see the message "Data load complete."

## Troubleshooting

- Ensure that the PostgreSQL server is up and running.
- Check that the connection parameters (host, port, database, user, password) match your local PostgreSQL installation.
- Verify that the IMDb TSV files are present in the working directory and are not corrupted.

## License

See the [LICENSE](../LICENSE) file for more details.

## Acknowledgements

Information courtesy of
IMDb
(https://www.imdb.com).
Used with permission.