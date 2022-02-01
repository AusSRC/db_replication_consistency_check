#!/usr/bin/env python3

import os
import asyncio
import asyncpg
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def check_sync():
    """Periodically check the different databases and compare to check the state of the database replication

    """
    queries = [
        'SELECT COUNT(*) FROM wallaby.run;',
        'SELECT * FROM wallaby.run;',
        'SELECT COUNT(*) FROM wallaby.detection;',
        'SELECT COUNT(*) FROM wallaby.source;'
    ]

    sites = [
        ('AusSRC', 'admin', os.getenv('AUSSRC_PASSWORD'), 'localhost', 5432, 'wallabydb'),
        ('SpSRC', 'admin', os.getenv('SPSRC_PASSWORD'), '161.111.167.192', 18020, 'wallabydb')
    ]

    response = []

    for query in queries:
        query_response = {'query': query}
        results = []
        for site in sites:
            (name, user, password, host, port, dbname) = site
            conn = await asyncpg.connect(f'postgres://{user}:{password}@{host}:{port}/{dbname}')
            res = await conn.fetch(query)
            results.append(res)
            query_response[name] = res
        passing = all(res == results[0] for res in results)
        query_response['passing'] = passing
        logging.info(f'Query: {query} Passing: {passing}')
        if not passing:
            logging.error(f'Query results did not match: {results}')

        response.append(query_response)

    return response


@app.get('/')
async def root():
    return await check_sync()
