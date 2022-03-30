#!/usr/bin/env python3

import os
import random
import asyncio
import asyncpg
from unittest import IsolatedAsyncioTestCase


class TestSourceFindingQueryResults(IsolatedAsyncioTestCase):
    """Unittests to verify queries for source finding tables produces the same results in each replicated database.

    """
    def setUp(self):
        self.host = ('AusSRC', 'admin', os.environ['AUSSRC_PASSWORD'], '146.118.67.204', 5432, 'wallabydb')
        self.sites = [
            ('SpSRC', 'admin', os.environ['SPSRC_PASSWORD'], '161.111.167.192', 18020, 'wallabydb')
        ]

    async def test_table_source_query_results(self):
        """Check that the number of rows in important database tables is the same between regional centres.

        """
        count_queries = [
            'SELECT COUNT(*) FROM wallaby.run;',
            'SELECT COUNT(*) FROM wallaby.product;',
            'SELECT COUNT(*) FROM wallaby.detection;',
            'SELECT COUNT(*) FROM wallaby.source;',
            'SELECT COUNT(*) FROM wallaby.source_detection;',
            'SELECT COUNT(*) FROM wallaby.tag;',
        ]

        # Assert table counts are the same
        counts = []
        for query in count_queries:
            results = []
            # host results
            (name, user, password, host, port, dbname) = self.host
            conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
            res = await conn.fetch(query)
            await conn.close()
            counts.append(int(dict(res[0])['count']) - 1)
            results.append(res)

            # compare with sites
            for site in self.sites:
                (name, user, password, host, port, dbname) = site
                conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
                res = await conn.fetch(query)
                results.append(res)
                await conn.close()
            passing = all(res == results[0] for res in results)
            self.assertTrue(passing)

        # Assert table content is the same
        random_entry_queries = [
            f'SELECT * FROM wallaby.run WHERE id={random.randint(0, counts[0])};',
            f'SELECT * FROM wallaby.product WHERE id={random.randint(0, counts[1])};',
            f'SELECT * FROM wallaby.detection WHERE id={random.randint(0, counts[2])};',
            f'SELECT * FROM wallaby.source WHERE id={random.randint(0, counts[3])};',
            f'SELECT * FROM wallaby.source_detection WHERE id={random.randint(0, counts[4])};',
            f'SELECT * FROM wallaby.tag WHERE id={random.randint(0, counts[5])};',
        ]
        self.assertEqual(len(random_entry_queries), len(counts))
        for query in random_entry_queries:
            results = []
            # host results
            (name, user, password, host, port, dbname) = self.host
            conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
            res = await conn.fetch(query)
            await conn.close()
            results.append(res)

            # compare with sites
            for site in self.sites:
                (name, user, password, host, port, dbname) = site
                conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
                res = await conn.fetch(query)
                results.append(res)
                await conn.close()
            passing = all(res == results[0] for res in results)
            self.assertTrue(passing)
