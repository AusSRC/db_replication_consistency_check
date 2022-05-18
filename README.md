# Consistency check

The consistency of the database tables is determined by the comparison of results for a set of queries. If each database returns the same result, we say that they are consistent. Otherwise, this API will state which databases are consistent with the main.

## Add databases

We get database credentials from a `config.ini` file. Each entry is a database that will be checked against each other for consistency

```
[database]
host = 
port = 5432
user = 
password = 
database = 

[replica]
host = 
port = 5432
user = 
password = 
database = 

...
```

Place this database file inside `src` so that it is accessible to the `query.py` script.

## Run locally

Install dependencies from `requirements.txt` and from inside `src` run

```
./query.py
```

## Deployment

In production the consistency check result can be retrieved from outside of the database instance through the API. We expose `/api/consistency` which returns 

| Response | Description |
| --- | --- | 
| `200 OK` | Consistency check passed |
| `400 BAD REQUEST` | Consistency check failed |

We use Docker to deploy this to your database environment. Create the credentials file in `src` (as required to run the check locally) and run the following

```
docker-compose up --build -d
```
