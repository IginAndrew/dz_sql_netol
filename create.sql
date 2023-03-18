create table if not exists Zhanr (
	id INTEGER PRIMARY KEY,
	name varchar(40) not null
);

create table if not exists Artist (
	id INTEGER PRIMARY KEY,
	zhanr_id integer not null,
	name varchar(40) not null,
	FOREIGN KEY (zhanr_id) REFERENCES Zhanr (id)
);

create table if not exists Album (
	id INTEGER PRIMARY KEY,
	artist_id integer not null,
	name varchar(40) not null,
	years date not null,
	FOREIGN KEY (artist_id) REFERENCES Artist (id)
);

create table if not exists Sbornik (
	id INTEGER PRIMARY KEY,
	name varchar(40) not null
);

create table if not exists Singl (
	id INTEGER PRIMARY KEY,
	album_id integer,
	sbornik_id integer,
	name varchar(40) not null,
  long time not null,
	FOREIGN KEY (album_id) REFERENCES Album (id),
	FOREIGN KEY (sbornik_id) REFERENCES Sbornik (id)
);
