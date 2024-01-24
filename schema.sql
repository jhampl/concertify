CREATE TABLE artists (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	spotify_id VARCHAR,
	name VARCHAR,
	relevant BOOL DEFAULT TRUE,
	);
CREATE UNIQUE INDEX ux_artists_name_relevant ON artists (name, relevant);

CREATE TABLE events (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR,
	location VARCHAR,
	artist_id INTEGER,
	date DATETIME,
	calendar_notified BOOL DEFAULT FALSE,
	FOREIGN KEY (artist_id) REFERENCES artists(id)
	);
CREATE UNIQUE INDEX ux_events_artist_id_date_location ON events (artist_id, date, location);