Google Trends Data Pipeline

1. Overview

    This project implements a backend service that integrates with Google Search Trends to collect keyword interest data.

    It was built as part of the Data Engineer assessment.

    - Key Features

        Fetches Google Trends time-series data using the pytrends library.

        Validates and parses data with Pydantic models.

        Stores data in PostgreSQL running inside a Docker container.

        -   Logic:

            - Initial run → fetches last 90 days of data.

            - Subsequent runs → fetches last 7 days of data to keep it current.

        Performs upserts (insert or update) in batches for efficiency.

        Fully containerized with Dockerfile and docker-compose.yml.

2. Setup Instructions
    - Prerequisites

        Docker and Docker Compose installed.
        Git (to clone the repo)
        Python 3.11+ (only if you want to test without Docker).

    - Run with Docker Compose
        
        # Clone the repository
        git clone https://github.com/Majid-El-Ezzi/google-trends.git
        cd google-trends

        # Build and start the services
        docker-compose up --build


    - This will:

        Start a PostgreSQL 15 container.

        Start the Python application container and run main.py.

    - Database Initialization

        The database schema is created automatically at startup.

        On container launch, the script [`wait-for-db.sh`](./wait-for-db.sh) runs [`app/init_db.py`](./app/init_db.py) to ensure the `trends` table exists before the app starts.

3. How It Works

    At startup:
        - The app waits until PostgreSQL is ready.
        - The database schema (`trends` table) is created if missing.

    a. The application checks if the database is empty.

        If empty → fetch 90 days of historical data.

        If not empty → fetch 7 days of recent data.

    b. The data is converted into validated Pydantic models.

    c. Records are inserted or updated in PostgreSQL in batches using upsert logic.

4. How to Test and Extend
    Run Locally (without Docker)
        - pip install -r requirements.txt
        - python app/init_db.py
        - python app/main.py
        - For local development without Docker, you can use a Python virtual environment (python -m venv venv) to isolate dependencies and install from requirements.txt

    Extending

        Add new keywords by calling run_pipe("keyword", "geo").

        Modify timeframes in the code (e.g., "today 3-m" or "now 7-d").

        Automate the database updates (e.g., via a scheduled job)

5. Verify Database Contents

    After running the pipeline, you can directly check the database using psql inside the container:

    # Open a PostgreSQL shell inside the db container
    docker-compose exec db psql -U majid -d trends

    # Once inside, run queries such as:
    \dt                -- list all tables
    SELECT COUNT(*) FROM trends;          -- total number of rows
    SELECT * FROM trends LIMIT 10;        -- preview the first 10 rows



    Exit the PostgreSQL shell with:

        \q

6. Design and Decisions

    a. Pytrends was used because Google does not provide an official Trends API.

    b. Pydantic was chosen to validate each record before insertion.

    c. PostgreSQL was selected as a reliable relational database, running inside Docker.

    d. SQLAlchemy upsert was implemented to avoid duplicate data and keep records updated.

    e. Docker Compose was used to ensure reproducible setup and easy deployment.
    
    f. A startup script (`wait-for-db.sh`) ensures the app waits for Postgres and initializes the schema before running.


7. Data Preloading

    In practice, a container could ship with a preloaded SQL dump.
    For this project, preloading was intentionally not implemented so that the 90-day initial load versus 7-day update logic can be tested as required.

8. Challenges Faced
    
    a. 429 Error (Too Many Requests)

        Google Trends does not have an official public API.

        Pytrends works by scraping internal endpoints.

        Sending too many requests in a short period, or from the same IP, causes Google to temporarily block requests.

        Google may also change limits dynamically, so code that works one day may fail the next.

        Mitigation steps:

            - Implemented retries with exponential backoff.

            - Used smaller timeframes during development.

            - Waiting a few hours until the block was removed.

    b. Ensuring Database Readiness and Initialization

        A common issue in containerized apps is that the application tries to connect to the database 
        before Postgres is fully up and ready to accept connections, or before the required tables exist.

        This caused errors such as:
            - "relation 'trends' does not exist"
            - connection failures on startup

        Mitigation steps:

            - Added a startup script (`wait-for-db.sh`) to block app launch until Postgres is ready.
            - Integrated an initialization step (`init_db.py`) into the startup flow to create the `trends` table automatically.
            - Ensured the script uses `exec` so Docker can correctly manage the app process.
9. Next Steps

    a. Add automated testing.

    b. Support multiple keywords in one run.

    c. Improve resilience against 429 errors with proxy rotation.

10. Some sources:

    - https://youtu.be/DQdB7wFEygo?si=OWQ--6u66Toap9Uw
    - https://www.docker.com/blog/how-to-dockerize-your-python-applications/
    - https://pypi.org/project/pytrends/
    - https://docs.pydantic.dev/latest/concepts/models/#data-conversion
