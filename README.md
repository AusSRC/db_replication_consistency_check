# Database replication consistency check

The consistency of the database tables is determined by the comparison of results for a set of queries. If each database returns the same result, we say that they are consistent. Otherwise, this API will state which databases are consistent with the main.

## Configuration

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