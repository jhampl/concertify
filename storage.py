import sqlite3
import datetime
from helpers import event_fields, artist_fields
import os

DBPATH = "concertify.db"

# connect to database, create it if it doesn't exist
db_exists = os.path.exists(DBPATH)
con = sqlite3.connect(DBPATH)
if not db_exists:
    with open("schema.sql") as file:
        con.executescript(file.read())
        con.commit()


def _dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


def _convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.datetime.fromisoformat(val)


def _adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def _adapt_bool(val):
    """Adapt boolean to integer."""
    return int(val)


def _convert_bool(val):
    """Convert integer to boolean."""
    return bool(val)


# set row factory to return dictionaries
con.row_factory = _dict_factory

# register adapters and converters for datetime and boolean
sqlite3.register_adapter(datetime.datetime, _adapt_date_iso)
sqlite3.register_converter("DATETIME", _convert_date)
sqlite3.register_adapter(bool, _adapt_bool)
sqlite3.register_converter("BOOL", _convert_bool)


def add_artists(artists):
    with con:
        con.executemany(
            f"INSERT OR IGNORE INTO artists ({', '.join(artist_fields)}) VALUES (:{', :'.join(artist_fields)})", artists)
        con.commit()


def add_events(events):
    with con:
        con.executemany(
            f"INSERT OR IGNORE INTO events ({', '.join(event_fields)}) VALUES (:{', :'.join(event_fields)})", events)
        con.commit()


def dismiss_event(event_id):
    with con:
        con.execute("UPDATE events SET dismissed = 1 WHERE id = ?", (event_id,))
        con.commit()


def ignore_artist(artist_id):
    with con:
        con.execute("UPDATE artists SET ignored = 1 WHERE id = ?", (artist_id,))
        con.commit()


def get_all_artists():
    with con:
        return con.execute(f"SELECT {', '.join(artist_fields)} FROM artists")


def get_relevant_artists():
    with con:
        return con.execute(f"SELECT {', '.join(artist_fields)} FROM artists WHERE active = 1 AND ignored = 0")


def get_all_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events")


def get_new_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events WHERE dismissed = 0")


def get_new_relevant_events():
    with con:
        query = f"""
            SELECT {', '.join(['events.' + s for s in event_fields])},
                   events.id as id,
                   artists.name as artist
            FROM events
            JOIN artists on events.artist_id = artists.spotify_id
            WHERE dismissed = 0
                AND artist_id IN (
                    SELECT spotify_id
                    FROM artists
                    WHERE active = 1 AND ignored = 0
                )
                AND events.date > date('now')
            ORDER BY events.date ASC
        """
        return con.execute(query).fetchall()


def get_artist_name(artist_id):
    with con:
        return con.execute("SELECT name FROM artists WHERE spotify_id = ?", (artist_id,)).fetchone()["name"]
