import sqlite3
import datetime
from helpers import event_fields, artist_fields

con = sqlite3.connect("store.db")
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))

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

def add_artists(artists):
    with con:
        con.executemany(f"INSERT OR IGNORE INTO artists ({', '.join(artist_fields)}) VALUES (:{', :'.join(artist_fields)})", artists)
        con.commit()

def add_events(events):
    with con:
        con.executemany(f"INSERT OR IGNORE INTO events ({', '.join(event_fields)}) VALUES (:{', :'.join(event_fields)})", events)
        con.commit()

def dismiss_event(event_id):
    with con:
        con.execute("UPDATE events SET dismissed = 1 WHERE id = ?", (event_id,))
        con.commit()

def ignore_artist(artist_id):
    with con:
        con.execute("UPDATE artists SET ignore = 1 WHERE id = ?", (artist_id,))
        con.commit()

def get_all_artists():
    with con:
        return con.execute(f"SELECT {', '.join(artist_fields)} FROM artists")

def get_relevant_artists():
    with con:
        return con.execute(f"SELECT {', '.join(artist_fields)} FROM artists WHERE active = 1 AND ignore = 0")

def get_all_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events")

def get_new_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events WHERE dismissed = 0")

def get_new_relevant_events():
    with con:
        return con.execute(f"SELECT {', '.join(event_fields)} FROM events WHERE dismissed = 0 AND artist_id IN (SELECT id FROM artists WHERE active = 1 AND ignore = 0)")

def get_artist_name(artist_id):
    with con:
        return con.execute("SELECT name FROM artists WHERE id = ?", (artist_id,)).fetchone()
    
if __name__ == "__main__":
    add_artists([{'spotify_id': '1', 'name': 'A', 'active': 1, 'ignored': 0}, {'spotify_id': '2', 'name': 'B', 'active': 0, 'ignored': 0}])
    add_artists([{'spotify_id': '1', 'name': 'A', 'active': 1, 'ignored': 0}, {'spotify_id': '2', 'name': 'B', 'active': 0, 'ignored': 0}])
    add_artists([{'spotify_id': '1', 'name': 'A', 'active': 1, 'ignored': 0}, {'spotify_id': '2', 'name': 'B', 'active': 0, 'ignored': 0}])
    add_artists([{'spotify_id': '1', 'name': 'A', 'active': 1, 'ignored': 1}, {'spotify_id': '2', 'name': 'B', 'active': 0, 'ignored': 1}])
    add_events([{'artist_id': 1, 'name': 'A', 'date': datetime.date.today(), 'location': 'Berlin (DE)', 'url': 'https://example.com', 'dismissed': False}],)
    add_events([{'artist_id': 1, 'name': 'A', 'date': datetime.date.today(), 'location': 'Berlin (DE)', 'url': 'https://example.com', 'dismissed': False}],)
    add_events([{'artist_id': 1, 'name': 'A', 'date': datetime.date.today(), 'location': 'Berlin (DE)', 'url': 'https://example.com', 'dismissed': False}],)
    add_events([{'artist_id': 1, 'name': 'A', 'date': datetime.date.today(), 'location': 'Berlini2 (DE)', 'url': 'https://example.com', 'dismissed': False}],)
    print(get_all_artists().fetchall())
    print(get_all_events().fetchall())