import sqlite3
import datetime
from helpers import event_fields, artist_fields

con = sqlite3.connect("store.db")
def dict_factory(cursor, row):
    d = {}
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_bool(val):
    """Adapt boolean to integer."""
    return int(val)

def convert_bool(val):
    """Convert integer to boolean."""
    return bool(val)

con.row_factory = dict_factory
sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_converter("date", convert_date)
sqlite3.register_adapter(bool, adapt_bool)
sqlite3.register_converter("BOOL", convert_bool)

def store_artists(artists):
    with con:
        con.execute("DELETE FROM artists")
        con.executemany(f"INSERT INTO artists ({', '.join(artist_fields)}) VALUES (:{', :'.join(artist_fields)})", artists)
        con.commit()

def store_events(events):
    with con:
        con.execute("DELETE FROM events")
        con.executemany(f"INSERT INTO events ({', '.join(event_fields)}) VALUES (:{', :'.join(event_fields)})", events)
        con.commit()

def get_artists():
    with con:
        return con.execute(f"SELECT {', '.join(artist_fields)} FROM artists")

def get_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events")
