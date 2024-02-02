CREATE TABLE artists (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	spotify_id VARCHAR,
	name VARCHAR,
	active BOOL DEFAULT TRUE,
	ignored BOOL DEFAULT FALSE
	);
CREATE UNIQUE INDEX ux_artists ON artists (name, spotify_id);

CREATE TABLE events (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR,
	location VARCHAR,
	artist_id INTEGER,
	date DATETIME,
	url VARCHAR,
	dismissed BOOL DEFAULT FALSE,
	FOREIGN KEY (artist_id) REFERENCES artists(id)
	);
CREATE UNIQUE INDEX ux_events ON events (artist_id, date, location);