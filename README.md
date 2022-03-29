# Replication check

Check the results of certain PostgreSQL queries are the same across regional centres. Makes use of Python `unittest` module. 

## Running

Set environment variables

```
export AUSSRC_PASSWORD=...
export SPSRC_PASSWORD=...
```

Install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run unittest module

```
./main.py
```