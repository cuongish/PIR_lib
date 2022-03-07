import json
from typing import TYPE_CHECKING, List
import sqlalchemy.orm
from sqlalchemy import insert

import app.database as _database
import app.models as _models
import app.schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from psycopg2.extras import Json
from psycopg2.extras import json as psycop_json
from psycopg2 import connect, Error

import sys

# accept command line arguments for the Postgres table name
if len(sys.argv) > 1:
    table_name = '_'.join(sys.argv[1:])
else:
    # ..otherwise revert to a default table name
    table_name = "contacts"

print("\ntable name for JSON data:", table_name)

# use Python's open() function to load the JSON data
with open('data.json') as json_data:
    # use load() rather than loads() for JSON files
    record_list = json.load(json_data)

print("\nrecords:", record_list)
print("\nJSON records object type:", type(record_list))
# should return "<class 'list'>"

# concatenate an SQL string
sql_string = 'INSERT INTO {}'.format(table_name)

# if record list then get column names from first key
if type(record_list) == list:
    first_record = record_list[0]

    columns = list(first_record.keys())
    print("\ncolumn names:", columns)

# if just one dict obj or nested JSON dict
else:
    print("Needs to be an array of JSON objects")
    sys.exit()

# enclose the column names within parenthesis
sql_string += "(" + ', '.join(columns) + ")\nVALUES "

# enumerate over the record
for i, record_dict in enumerate(record_list):

    # iterate over the values of each record dict object
    values = []
    for col_names, val in record_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophies with two single quotations
            val = val.replace("'", "''")
            val = "'" + val + "'"

        values += [str(val)]

    # join the list of values and enclose record in parenthesis
    sql_string += "(" + ', '.join(values) + "),\n"

# remove the last comma and end statement with a semicolon
sql_string = sql_string[:-2] + ";"

print("\nSQL string:")
print(sql_string)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_csv(sql_query: str, db: sqlalchemy.orm.Session) -> List[_schemas.Contact]:
    # TODO FIXME
    db.query(sql_query)
    db.commit()
    db.refresh()

    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.from_orm, contacts))


load_csv(sql_query=sql_string, db=get_db())
