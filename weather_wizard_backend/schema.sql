CREATE TABLE timetemphumid (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL UNIQUE,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imageName TEXT NOT NULL,
    imageData BLOB NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE image_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imageId INTEGER,
    timetemphumidId INTEGER,
    FOREIGN KEY (imageId) REFERENCES images(id),
    FOREIGN KEY (timetemphumidId) REFERENCES timetemphumid(id)
);
