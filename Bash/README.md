# IMDb Data Import (Bash Version)

This is the Bash script version of the IMDb data import project. This script:

- Downloads multiple gzipped TSV files from specified URLs.
- Drops any existing PostgreSQL tables and recreates them using a defined schema.
- Loads the data from the downloaded files into PostgreSQL.
- Cleans up any temporary files by removing the download folder after processing.
- Can be scheduled for daily updates using Windows Task Scheduler.

> **Note:** This script is designed to run in a Bash-compatible environment on Windows (e.g., Git Bash, WSL, or Cygwin).

---

## Prerequisites

Ensure the following are installed and accessible in your environment:

- **Git Bash (or other Bash shell):** [Download Git for Windows](https://gitforwindows.org/)
- **PostgreSQL:** Database must be installed and running.
- **Utilities:**  
  - `wget` (or fall back to `curl` if wget is not available)
  - `gunzip`
  - `psql` (PostgreSQL client)

Download URLs for IMDb data files are defined in the script. Update these URLs as needed.

---

## Script Overview

The Bash script performs the following steps:

1. **Create a Temporary Directory:**  
   It creates a temporary folder in the current directory to store downloads only for the duration of the process.

2. **Download Data Files:**  
   It downloads each data file (gzipped TSV) using either `wget` (preferred) or `curl` if `wget` is not installed.

3. **Database Setup:**  
   It connects to PostgreSQL and drops existing tables then creates new tables based on the predefined schema.

4. **Data Load:**  
   The script decompresses each gzipped file and loads the content into PostgreSQL using the `\copy` command.

5. **Cleanup:**  
   Finally, it removes the temporary download folder so no files remain on disk.

---

## Configuration

1. **PostgreSQL Credentials:**  
   At the top of the script, update the following environment variables if necessary:

   ```bash
   export PGHOST=your_host (default: localhost)
   export PGPORT=your_port (defaul: 5432)
   export PGDATABASE=your_database (default: IMDb)
   export PGUSER=your_username (default: postgres)
   export PGPASSWORD=your_password 
   ```
2. **File Paths & Environment:**
  The script creates a temporary folder (using mktemp -d) in the current directory. It downloads all files there, processes them, and then deletes the folder.

## Running the Script Manually

1. Save the script as `load_data.sh` in your preferred location.
2. Open Git Bash and navigate to the folder that contains the script.
3. Make the script executable:
  ```bash
  chmod +x update_imdb.sh
  ```
4. Execute the script:
  ```bash
  ./update_imdb.sh
  ```
Monitor the console output for messages indicating progress through downloads, database setup, data load, and cleanup.

## Enabling Daily Updates with Windows Task Scheduler

1. **Prepare the Script:** Ensure `load_data.sh` is saved at a fixed location (e.g., `C:\IMDb\Bash\load_data.sh`).
2. **Open Task Scheduler:** Press the Windows key and type "Task Scheduler" to open it.
3. **Create Basic Task:**
    - In Task Scheduler’s right-hand panel, click Create **Basic Task…**.
    - Enter a Name (e.g., "Daily IMDb Update") and a Description.
    - Set the Trigger to **Daily** and choose your preferred start time.
4. **Set the Action:**
    - Choose the Action Start a program.
    - In the **Program/script** field, enter the full path to Git Bash. For example:
    ```bash
    C:\Program Files\Git\bin\bash.exe
    ```
    - In the **Add arguments (optional)** field, include:
    ```bash
    --login -i "C:\Tools\IMDb_Data_Import\bash\update_imdb.sh"
    ```
    This tells Git Bash to run your script in an interactive login shell.
    - Set **Start in** to the folder containing your script (e.g., `C:\IMDb\Bash\load_data.sh`).
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
- The Bash script downloads IMDb files, sets up the PostgreSQL database, loads data, and cleans up temporary files.
- It is designed to run on a Bash shell (Git Bash/WSL/Cygwin on Windows).
- Daily updates can be enabled using Windows Task Scheduler by configuring Git Bash to run the script automatically.

This setup ensures your IMDb database is updated automatically each day without any manual intervention.

