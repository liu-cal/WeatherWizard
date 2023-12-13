CREATE TABLE IF NOT EXISTS timetemphumid (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP UNIQUE,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imageName TEXT NOT NULL UNIQUE,
    imageData BLOB NOT NULL,
    capturedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS image_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imageId INTEGER UNIQUE,
    timetemphumidId INTEGER,
    avgColor TEXT,
    FOREIGN KEY (imageId) REFERENCES images(id),
    FOREIGN KEY (timetemphumidId) REFERENCES timetemphumid(id)
);
