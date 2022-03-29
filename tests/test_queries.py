#!/usr/bin/env python3

import os
import asyncio
import asyncpg
from unittest import IsolatedAsyncioTestCase


class TestQueryResults(IsolatedAsyncioTestCase):
    """Unittests to verify query produces the same results in each database.

    """
    def setUp(self):
        self.queries = [
            'SELECT COUNT(*) FROM wallaby.run;',
            'SELECT * FROM wallaby.run;',
            'SELECT COUNT(*) FROM wallaby.detection;',
            'SELECT COUNT(*) FROM wallaby.source;'
        ]
        self.sites = [
            ('AusSRC', 'admin', os.environ['AUSSRC_PASSWORD'], '146.118.67.204', 5432, 'wallabydb'),
            ('SpSRC', 'admin', os.environ['SPSRC_PASSWORD'], '161.111.167.192', 18020, 'wallabydb')
        ] 

    async def test_query_results(self):
        """Connect to databases, run PostgreSQL queries. Assert output is the same.

        """
        for query in self.queries:
            query_response = {'query': query}
            results = []
            for site in self.sites:
                (name, user, password, host, port, dbname) = site
                conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
                res = await conn.fetch(query)
                results.append(res)
                query_response[name] = res
                await conn.close()
            passing = all(res == results[0] for res in results)
            self.assertTrue(passing)
