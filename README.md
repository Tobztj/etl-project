## Introduction

This project is focused on developing an ETL (Extract, Transform, Load) pipeline that processes JSON data, applies a series of data transformations, and outputs a structured data model. The solution includes documentation covering the design approach and execution instructions. It also outlines the project scope and discusses potential enhancements for scaling the solution and integrating it into a production-grade data architecture.

## Prerequisites

- Python >= 3.11.0 ([Download Python](https://www.python.org/downloads/))
- Poetry >= 2.0.1 ([Poetry Installation Guide](https://python-poetry.org/docs/#installation))
- SQL Server (for database operations)

## Setup

1. **Clone the repository** (if you haven't already):
    ```bash
    git clone <repo-url>
    cd esure_project
    ```

2. **Open terminal at the root of this project (`esure_project`) and set up your virtual environment:**
    ```bash
    # To make Poetry create a .venv/ folder in the project folder
    poetry config virtualenvs.in-project true

    # To install all dependencies
    poetry install

    # To activate virtual environment (Windows)
    .venv\Scripts\activate

    # Or on Mac/Linux
    source .venv/bin/activate
    ```

    This will install all project dependencies in a virtual environment.

3. **Managing dependencies**

    Installing, updating or removing dependencies using Poetry:
    ```bash
    poetry add <package-name>
    poetry update <package-name>
    poetry remove <package-name>
    ```

    Always keep the lock file updated with:
    ```bash
    poetry lock
    ```

## Configuration

Before running the ETL pipeline, you need to fill out the required variables in the configuration file.

1. **Locate the config file:**  
   The configuration file is typically found at `esure_project/app/config/config.py` or `config.yaml` (update this path if your config is elsewhere).

2. **Edit the following variables as needed:**
    - `DRIVER`: ODBC driver for SQL Server (e.g., `{ODBC Driver 17 for SQL Server}`)
    - `SERVER`: Your SQL Server instance name or address
    - `DATABASE`: Target database name
    - `USERNAME` and `PASSWORD`: Your database credentials
    - Any other paths or settings required for your environment (such as input/output directories)

    Example (Python config):
    ```python
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVER = 'localhost\\SQLEXPRESS'
    DATABASE = 'EsureDB'
    USERNAME = 'your_username'
    PASSWORD = 'your_password'
    ```

    > **Note:** Never commit sensitive credentials to version control.

## How to Execute the ETL Pipeline

1. **Activate your virtual environment** (if not already active):
    ```bash
    .venv\Scripts\activate
    # or
    source .venv/bin/activate
    ```

2. **Run the main ETL script:**
    ```bash
    python main.py
    ```

    This will:
    - Extract data from JSON files in the specified input directory
    - Validate and clean the data
    - Load data into the staging tables
    - Transform and load data into the target data model (star schema)
    - Log progress and errors to the `All_Logs` directory

3. **Check logs:**
   All logs are written to the `All_Logs` folder at the root of the project for troubleshooting and audit purposes.

## Project Structure

```
esure_project/
│
├── app/
│   ├── Extraction/
│   ├── load/
│   ├── logging/
│   ├── transformations/
│   └── config/
├── All_Logs/
├── main.py
└── README.md
```

## Troubleshooting

- Ensure your database connection details are correct in the config file.
- Check the `All_Logs` folder for detailed error and info logs.
- Make sure your SQL Server is running and accessible.
- If you encounter missing dependencies, run `poetry install` again.

## Enhancements

- Add environment variable support for sensitive configs.
- Implement automated tests for data validation and transformation.
- Containerize the solution for easier deployment.

---