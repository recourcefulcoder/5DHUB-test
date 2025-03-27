# 5DHUB-test
initial task for 5DHUB internship 

Table of contents:
-
- Application running instructions
  - With Docker
  - Manually
- Documentation
  - Environment variables


## Running application

### With Docker Compose
In order to launch an application in this manner, running machine should support Docker CLI tools.

1. Create .env file in root directory and fill it with required environment variables 
(full list see [lower](#environment-variables))
2. Execute from the root directory:
```bash
docker-compose build 
docker compose up -d
```

By default, application is run on port 8080; it may be customized: for that you should:
1. call docker-compose build command with --build-arg, setting needed port
```bash
docker-compose --build --build-arg port="<your_number_here>"
```
2. set APPLICATION_PORT environment variable in your in .env file to this value


    APPLICATION_PORT=<your_port>

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

## Documentation
### Environment variables

| Variable | Value |
| -------- | ----- |
| POSTGRES_USER | declares USER for accessing PostgreSQL DB |
| POSTGRES_PASSWORD | defines password for accessing PostgreSQL DB |
| POSTGRES_DB | declares name of the database used |
| DB_HOST | host database listens on, defaults to localhost |
| DB_PORT | port database listens on, defaults to 5432 (default for PostgreSQL) |
|||
| APPLICATION_PORT | defines port for an application to run on; defaults to 8080 (in docker-compose.yaml) |

