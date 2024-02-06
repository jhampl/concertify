CREATE TABLE artists (
	spotify_id VARCHAR PRIMARY KEY,
	name VARCHAR,
	active BOOL DEFAULT TRUE,
	ignored BOOL DEFAULT FALSE
);
CREATE UNIQUE INDEX ux_artists ON artists (name, spotify_id, active);
CREATE TABLE events (
	id INTEGER PRIMARY KEY,
	name VARCHAR,
	location VARCHAR,
	artist_id INTEGER,
	date DATETIME,
	url VARCHAR,
	dismissed BOOL DEFAULT FALSE,
	FOREIGN KEY (artist_id) REFERENCES artists(spotify_id)
);
CREATE UNIQUE INDEX ux_events ON events (artist_id, date, location);