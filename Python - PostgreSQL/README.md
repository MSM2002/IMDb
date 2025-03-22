# IMDb Dataset Loader for PostgreSQL

## Overview

This Python script provides an automated solution for loading IMDb's publicly available dataset into a PostgreSQL database. It handles decompression of .tsv.gz files and efficiently loads them into corresponding database tables.

## Prerequisites

### Software Requirements
- Python 3.x
- PostgreSQL
- psycopg2 library

### Installation Steps

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
3. Install psycopg2 using pip:
   ```bash
   pip install psycopg2-binary
	```
## Configuration
### PostgreSQL Setup

1. Create a new database named 'IMDb'
2. Ensure you have a PostgreSQL user with appropriate permissions

### Script Configuration

Edit the following variables in `load_data.py`:

1. `PGHOST`: PostgreSQL host (default: 'localhost')
2. `PGPORT`: PostgreSQL port (default: 5432)
3. `PGDATABASE`: Database name (default: 'IMDb')
4. `PGUSER`: PostgreSQL username
5. `PGPASSWORD`: PostgreSQL password

## Data Source

Download the IMDb dataset from [IMDb Datasets](https://datasets.imdbws.com/)

Required files:

1. title.akas.tsv.gz
2. title.basics.tsv.gz
3. title.crew.tsv.gz
4. title.episode.tsv.gz
5. title.principals.tsv.gz
6. title.ratings.tsv.gz
7. name.basics.tsv.gz

## Usage

1. Place the downloaded .tsv.gz files in the same directory as `load_data.py`
2. Run the script:
   ```bash
   python load_data.py
   ```

## Tables Created

The script creates the following tables in the 'IMDb' database:

1. `title_akas`
1. `title_basics`
1. `title_crew`
1. `title_episode`
1. `title_principals`
1. `title_ratings`
1. `name_basics`

## Performance Notes

* Uses PostgreSQL's COPY command for efficient data loading
* Decompresses files on-the-fly without intermediate file storage
* Handles large datasets with minimal memory overhead

## Error Handling

The script includes basic error handling for:

* PostgreSQL connection issues
* Missing input files
* Encoding problems

## Customisation

You can modify the `TABLE_SETUP_SQL` variable to adjust table schemas or add additional preprocessing

## Troubleshooting

* Ensure all .tsv.gz files are present
* Check PostgreSQL credentials
* Verify Python and psycopg2 installation

## License

See the [LICENSE](../LICENSE) file for more details.

## Acknowledgements

Information courtesy of
IMDb
(https://www.imdb.com).
Used with permission.