#!/usr/bin/env python3

import asyncio
import asyncpg
import logging
import random
from utils import parse_config


async def table_query_consistency_check():
        """Check that the number of rows in important database tables is the same between regional centres.

        """
        consistent = False
        cred_dict = parse_config()

        # Assert table counts are the same
        count_queries = [
            'SELECT COUNT(*) FROM wallaby.run;',
            'SELECT COUNT(*) FROM wallaby.product;',
            'SELECT COUNT(*) FROM wallaby.detection;',
            'SELECT COUNT(*) FROM wallaby.source;',
            'SELECT COUNT(*) FROM wallaby.source_detection;',
            'SELECT COUNT(*) FROM wallaby.tag;',
        ]
        counts = []
        for query in count_queries:
            count_res_list = []
            for db_name, db_cred in cred_dict.items():
                # TODO(austin): this is blocking and therefore takes ages...
                conn = await asyncpg.connect(
                    database=db_cred["database"],
                    host=db_cred["host"],
                    user=db_cred["user"],
                    password=db_cred["password"],
                    port=db_cred["port"]
                )
                res = await conn.fetch(query)
                logging.info(f"{db_name}: Result {res} for query '{query}'")
                await conn.close()
                count_res_list.append(res)

            counts.append(int(dict(res[0])['count']) - 1)
            
        count_passing = all(res == count_res_list[0] for res in count_res_list)
        if not count_passing:
            logging.error("Count queries do not produce the same result between databases.")
            return False

        # Assert random row from table content is the same
        random_entry_queries = [
            f'SELECT * FROM wallaby.run WHERE id={random.randint(0, counts[0])};',
            f'SELECT * FROM wallaby.product WHERE id={random.randint(0, counts[1])};',
            f'SELECT * FROM wallaby.detection WHERE id={random.randint(0, counts[2])};',
            f'SELECT * FROM wallaby.source WHERE id={random.randint(0, counts[3])};',
            f'SELECT * FROM wallaby.source_detection WHERE id={random.randint(0, counts[4])};',
            f'SELECT * FROM wallaby.tag WHERE id={random.randint(0, counts[5])};',
        ]
        for query in random_entry_queries:
            value_res_list = []
            for db_name, db_cred in cred_dict.items():
                # TODO(austin): this is blocking and therefore takes ages...
                conn = await asyncpg.connect(
                    database=db_cred["database"],
                    host=db_cred["host"],
                    user=db_cred["user"],
                    password=db_cred["password"],
                    port=db_cred["port"]
                )
                res = await conn.fetch(query)
                logging.info(f"{db_name}: Result {res} for query '{query}'")
                await conn.close()
                value_res_list.append(res)
            
        value_passing = all(res == value_res_list[0] for res in value_res_list)
        if not value_passing:
            logging.error("Query table entries do not produce the same result between databases.")
            return False

        logging.info("Query results are the same between databases.")
        return True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(table_query_consistency_check())
