#!/usr/bin/env python3

import os
import asyncio
import asyncpg
from unittest import IsolatedAsyncioTestCase


class TestConnection(IsolatedAsyncioTestCase):
    """Unittests to verify connection between databases.

    """
    def setUp(self):
        self.sites = [
            ('AusSRC', 'admin', os.environ['AUSSRC_PASSWORD'], '146.118.67.204', 5432, 'wallabydb'),
            ('SpSRC', 'admin', os.environ['SPSRC_PASSWORD'], '161.111.167.192', 18020, 'wallabydb')
        ] 

    async def test_all_connections(self):
        """Attempt to connect to each of the databases. Do nothing.

        """
        for site in self.sites:
            (name, user, password, host, port, dbname) = site
            conn = await asyncpg.connect(database=dbname, host=host, user=user, password=password, port=port)
            await conn.close()
