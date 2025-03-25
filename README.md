# IMDb Dataset Loader

## Overview

This project contains two versions of an automated data import solution for IMDb data files into a PostgreSQL database: one written in **Bash** and one in **Python**.

Both versions perform the following steps:

- **Download Files**: Retrieve gzipped TSV files from specified URLs.
- **Database Setup**: Connect to PostgreSQL, drop existing tables, and recreate them with a defined schema.
- **Data Load**: Decompress the downloaded files and load their contents into PostgreSQL using an efficient bulk copy operation.
- **Cleanup**: Remove temporary files/folders once the update is complete.

The complete refresh approach is used – each time the script runs, it downloads the full dataset, drops any pre-existing tables, and reloads all the data.

## PostgreSQL Database Schema

Both versions create the following tables:

- **title_akas**
- **title_basics**
- **title_crew**
- **title_episode**
- **title_principals**
- **title_ratings**
- **name_basics**

Each table uses plain text columns for fields that IMDb originally stores as arrays.

## License

See the [LICENSE](LICENSE.txt) file for more details.

## Summary

This project provides two complete solutions (Bash and Python) for automating a full refresh of IMDb data in a PostgreSQL database. For environments where a complete download and reload is more efficient, both scripts drop existing tables and load the full dataset. Daily updates can be enabled through Windows Task Scheduler, ensuring your database remains up-to-date.

Feel free to modify the scripts according to your specific requirements.

Code and README files for Bash and Python are in their respective directories.

## Acknowledgements

Information courtesy of
IMDb
(https://www.imdb.com).
Used with permission.
