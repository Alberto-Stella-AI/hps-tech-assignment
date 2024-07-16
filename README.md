<div align="center">

# how-people-shop

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)]()

[![Linting, formatting, imports sorting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)
</div>


# Table of Contents

- [how-people-shop](#how-people-shop)
  - [Repository Structure](#repository-structure)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Assignment and Documentation](#assignment-and-documentation)

# Repository Structure

```
.
├── .github                       <- GitHub PR template
├── Makefile
├── README.md
├── bin                           <- Bash files
├── config                        <- Configuration files
├── db                            <- sample databases
├── docs                          <- Documentation files
├── lib
│   ├── databases                 <- sample database creation modules
│   ├── service_catalog           <- Service Catalog modules
│   └── user                      <- User service moduls
├── pytest.ini                    <- config for pytest
├── requirements-developer.txt    <- conda requirements for development
├── requirements.txt              <- conda requirements
├── secrets                       <- Secret files (ignored by git)
└── tests                         <- tests folder
    └── unit_tests                <- unit tests for the services
```

# Installation

Install the required packages in a conda environment running the following command:
```bash
make install
```

Then activate the environment:
```bash
conda activate hps
```

Add the repository path:
```bash
export PYTHONPATH=.
```

# Usage
This section allows to:
1. create a sample database with some users' details
2. run the Service Catalog RESTful API endpoint
3. run the User RESTful API endpoint

Create a sample user database running in the terminal:
```bash
python lib/databases/create_sample_user_db.py
```
A new folder __db__ and a sample database __users.db__ are created.

Run the Service Catalog microservice:
```bash
python lib/service_catalog/main.py
```

Run the User microservice:
```bash
python lib/user/main.py
```

The endpoints can investigated through the web browser at the hosts and ports indicated in the [Config File](config/config.py).
Moreover, the endpoint documentation can be found at http://{HOST}:{PORT}/docs", and from there some custom tests can be executed.

To test the endpoints automatically, run the unit tests with:
```bash
pytest tests
```


# Assignment and Documentation
This section provides a mapping between the assignment points and the resources that constitute the solution for each of those.

1. Sketch out an architecture diagram, showing the main components of the digital web-based HPS product. Indicate how the components communicate with each other and what architectural style are being used/followed. Create a basic RESTful API endpoint (including some unit tests) for at least one of the components.
    - architecture -> [Architecture Docs](docs/architecture.md)
    - RESTful API endpoints -> [Service Catalog](lib/service_catalog/), [User](lib/user/)
    - unit tests -> [Unit Tests](tests/unit_tests/)

2. Design and diagram an underlying unified data model / database(s) to be used to store, analyze and modify the primary data. Write sample SQL queries to retrieve specific data from this database.
    - Database diagram -> [Entity Relationship Diagram](docs/data.md)
    - Sample queries -> [Queries]((docs/data.md#sample-sql-queries))
3. Define the relevant technical specifications and set of technologies that would be used to address the following operational aspects -> [Docs](docs/etl.md)
    - Extract data from different data sources, Transform it to the underlying data model, then Load it to the desired storage location -> [ETL](docs/etl.md#extract-transform-load-etl)
    - Dealing with structured and unstructured data sources -> [Structured and Unstructured data](docs/etl.md#dealing-with-structured-and-unstructured-data)
    - Scalability in order to process & serve behavioral data of billions of customers worldwide -> [Scalability](docs/etl.md#scalability)
    - Support of various trigger mechanisms that would invoke data extraction and ingestion -> [Triggers](docs/etl.md#support-of-various-trigger-mechanisms)

4. Define what kind of technologies/platforms/tools should be used with or integrated into the application. Consider here also peripheral aspects such as observability and data quality -> [Platform](docs/platform.md)
5. List challenges/concerns that you see and indicate how you think they should be approached and resolved -> [Challenges](docs/challenges.md)
6. Calculate the total number of cups of coffee that the HPS product team consumes each sprint. Explain how you arrived at your answer -> [Coffee Cups Estimate](docs/coffee.md)
