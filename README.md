# 5DHUB-test
initial task for 5DHUB internship 

Table of contents:
-
- [Application running instructions](#running-application)
  - [With Docker](#with-docker-compose)
  - [Manually](#manually)
- [Testing](#testing)
- [Documentation](#documentation)
  - [Environment variables](#environment-variables)


## Running application

### With Docker Compose
In order to launch an application in this manner, running machine should support Docker CLI tools.

1. Create .env file in root directory and fill it with required environment variables 
(full list see [lower](#environment-variables))
2. Execute from the root directory:
```bash
docker compose up --build -d 
```

By default, application is run on port 8080; it may be customized: for that you should set 
[APPLICATION_PORT](#environment-variables) environment variable in your in .env file to 
the value of port you want to see


    APPLICATION_PORT=<your_port>

To stop an application, you should run
```bash
docker compose down 
```

### Manually
1. Run PostgreSQL database server and create a project database
2. Specify project's environment variables in .env file

In the root directory of the project create .env file, containing all 
required environment variables (complete list see [lower](#environment-variables)) in following 
syntax:

    VARNAME1=VAL1
    VARNAME2=VAL2
    ...

3. Create virtual environment, activate it and install project dependencies<br>

From  the root directory execute (on Linux)
```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

4. Run FastAPI application
```bash
cd src
fastapi run main.py --port 8080
```
(or any other PORT value of your choice)


## Testing
In order to test an application, it must be configured for **_test mode_**
### What is test mode?
Test mode implies specific application configuration via env variables, specifying that it is
launched for testing exclusively. It assumes setting up special _TEST DATABASE_ isolated 
from production one<br>
Application is considered to be run in test mode when:
1. TESTING env variable is set to True
2. TEST_POSTGRES_DB is provided and is different from POSTGRES_DB

If these two requirements aren't met, tests will be aborted. 

To launch testing from the root directory run in CLI:
```bash
pytest
```

## Documentation

Actual shortening is made via [pyshorteners](https://pyshorteners.readthedocs.io/en/latest/) 
python library

Implemented endpoints:
1. shorten_link
- URL: "/"
- method: POST
- description: expects JSON request data with "link" key containing link to shorten <br>
RETURNS json object with shortened link data and response status 201 (CREATED) if succeeded; <br>
On fail returns JSON {"error": "<error message>"} with corresponding code <br><br>
Example of valid response:
```json lines
{
  "id": <link_id>,
  "shortened_link": <link_shortened>
}
```

2. redirect
- URL: "/<shorten-url-id>"
- method: GET
- description: gets link's ID in database, returns 307 code and full link address in "Location" header

3. request_service
- URL: "/make_request/<shorten-url-id>"
- methods: GET, POST
- description: accepts request to given server and sends request to it in asynchronous mode; 
when response is returned, gives it to user. Redirect payload (if provided) and all 
provided headers as well
> [!NOTE]
> Any data provided will be sent as a JSON payload 

> [!WARNING]
> file redirection is not supported yet - if user sends files to this endpoint they will be ignored

### Environment variables

| Variable | Value |
| -------- | ----- |
| POSTGRES_USER | declares USER for accessing PostgreSQL DB |
| POSTGRES_PASSWORD | defines password for accessing PostgreSQL DB |
| POSTGRES_DB | declares name of the production/development database used (opposing to test database) |
| DB_HOST | host database listens on, defaults to localhost |
| DB_PORT | port database listens on, defaults to 5432 (default for PostgreSQL) |
|||
| TESTING | defines whether application is in testing mode; about testing mode see [higher](#what-is-test-mode?) |
| TEST_POSTGRES_DB | defines name of test database for testing mode |
|||
| APPLICATION_PORT | defines port for an application to run on; defaults to 8080 (in docker-compose.yaml) |

