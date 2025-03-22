# IMDb Dataset Loader

## Overview

This project provides multiple methods for loading IMDb's publicly available datasets into a PostgreSQL database. The goal is to offer flexible, efficient data ingestion solutions for researchers, data analysts, and developers working with IMDb's comprehensive movie and TV show datasets.


## Methods of Data Loading

This project provides two primary approaches to loading IMDb datasets:

1. **Python Method** (`/python`)
   - Uses Python's `psycopg2` library
   - Efficient on-the-fly decompression
   - Cross-platform compatibility
   - Detailed error handling

2. **Bash Method** (`/bash`)
   - Uses native shell commands
   - Leverages PostgreSQL's COPY command
   - Ideal for Unix-like systems
   - Minimal dependencies

## Prerequisites

- PostgreSQL
- Python 3.x (for Python method)
- Bash shell (for Bash method)

## Data Source

Datasets are sourced from [IMDb Interfaces](https://datasets.imdbws.com/)

## Required Files

- title.akas.tsv.gz
- title.basics.tsv.gz
- title.crew.tsv.gz
- title.episode.tsv.gz
- title.principals.tsv.gz
- title.ratings.tsv.gz
- name.basics.tsv.gz

## Performance Comparison

| Aspect           | Python Method | Bash Method |
|-----------------|--------------|-------------|
| Portability     | Cross-platform | Unix-like systems |
| Dependency      | psycopg2     | Shell utilities |
| Error Handling  | Comprehensive | Basic |
| Memory Usage    | Low          | Moderate |

## Getting Started

1. Clone the repository
2. Choose your preferred method (Python or Bash)
3. Follow the README in the respective subdirectory

## License

See the [LICENSE](/LICENSE) file for more details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Contact

For issues or questions, please open a GitHub issue.