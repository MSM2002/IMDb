# IMDb Data Import (Python Version)

This Python solution automates the import of IMDb data files into a PostgreSQL database. The script downloads multiple gzipped TSV files, sets up your database (dropping and recreating tables), loads the data using PostgreSQL’s efficient COPY command, and then cleans up temporary files automatically.

> **Note:** This script is designed to run with Python 3 and uses standard libraries along with [psycopg2](https://www.psycopg.org/).

---

## Prerequisites

- **Python 3.x** installed on your system.
- **PostgreSQL** must be installed, running, and accessible.
- Required Python package:
  - **psycopg2-binary** – Install using pip:
    ```bash
    pip install psycopg2-binary
    ```
- Internet connectivity to download IMDb data files.
- Update the data file download URLs in the script as needed.

---

## Script Overview

The Python script performs the following steps:

1. **Temporary Directory Creation:**  
   It creates a temporary directory (using Python’s `tempfile.TemporaryDirectory`) to hold the downloaded files during execution.

2. **Download Data Files:**  
   For each IMDb data file, the script downloads the file from a specified URL into the temporary directory using Python’s `urllib.request`.

3. **Database Setup:**  
   It connects to PostgreSQL using the provided credentials, drops existing tables, and recreates them using a predefined SQL schema.

4. **Data Loading:**  
   The script decompresses each gzipped TSV file and loads the data into the corresponding PostgreSQL table using a bulk `COPY` operation (via `psycopg2`).

5. **Cleanup:**  
   Once completed, the temporary directory (and all downloaded files) is automatically removed.

---

## Configuration

1. **PostgreSQL Credentials:**  
   Update these variables near the top of the script if necessary:
   ```python
   PGHOST=your_host (default: localhost)
   PGPORT=your_port (defaul: 5432)
   PGDATABASE=your_database (default: IMDb)
   PGUSER=your_username (default: postgres)
   PGPASSWORD=your_password 
   ```
2. **Database Schema:**
   The script contains SQL commands (in `TABLE_SETUP_SQL`) to drop existing tables and recreate them. Ensure it meets your requirements.

## Running the Script Manually

1. Clone or download the repository.
2. Navigate to the folder containing the Python script (e.g., `load_data.py`).
3. Run the script from the command line:
   ```python
   python load_data.py
   ```
4. Monitor the output to ensure files are downloaded, the database is set up, data loads correctly, and temporary files are cleaned up.

## Enabling Daily Updates with Windows Task Scheduler

1. **Prepare the Script:** Ensure `load_data.py` is saved at a fixed location (e.g., `C:\IMDb\Python\load_data.py`).
2. **Open Task Scheduler:** Press the Windows key and type "Task Scheduler" to open it.
3. **Create Basic Task:**
    - In Task Scheduler’s right-hand panel, click Create **Basic Task…**.
    - Enter a Name (e.g., "Daily IMDb Update") and a Description.
    - Set the Trigger to **Daily** and choose your preferred start time.
4. **Set the Action:**
    - Choose the Action Start a program.
    - In the **Program/script** field, enter the full path to Git Bash. For example: `C:\Python39\python.exe`
    - In the **Add arguments (optional)** field, include:
    ```bash
    --login -i "C:\Tools\IMDb_Data_Import\bash\update_imdb.sh"
    ```
    This tells Git Bash to run your script in an interactive login shell.
    - Set **Start in** to the folder containing your script (e.g., `C:\IMDb\Python\load_data.py`).
5. **Finalise the Task:**
    - Proceed to finish the wizard.
    - Open the task’s **Properties** (right-click the task and choose Properties).
    - On the **General** tab, select **Run whether user is logged on or not.**
    - Configure any necessary conditions (e.g., ensure the machine is awake and connected to a network).
    - Save your settings.
6. **Test the Task:**
    - In Task Scheduler, right-click on your new task and select Run.
    - Verify that the script is executed and that PostgreSQL is updated accordingly.

## Summary
- The Python script downloads IMDb files, sets up the PostgreSQL database, loads data, and cleans up temporary files.
- It is designed to run on a Bash shell (Git Bash/WSL/Cygwin on Windows).
- Daily updates can be enabled using Windows Task Scheduler by configuring Git Bash to run the script automatically.

This setup ensures your IMDb database is updated automatically each day without any manual intervention.