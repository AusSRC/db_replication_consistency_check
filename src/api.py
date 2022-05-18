#!/usr/bin/env python3

from query import table_query_consistency_check
from flask import Flask, make_response


app = Flask(__name__)


@app.route("/")
def hello():
    return "OK"


@app.route("/api/consistency")
async def check_consistency():
    passed = await table_query_consistency_check()
    if passed:
        return make_response("Passed", 200)
    return make_response("Failed", 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
