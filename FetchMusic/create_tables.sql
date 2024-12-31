-- Create the Song table if it does not exist
CREATE TABLE IF NOT EXISTS Song (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each song
    coverart TEXT,                               -- Cover art URL or path
    song_no INTEGER,                             -- Song number in the album
    name TEXT,                                   -- Name of the song
    artist TEXT,                                 -- Artist of the song
    duration INTEGER,                            -- Duration of the song in seconds
    download_link TEXT                           -- Link to download the song
);

-- Create the Album table if it does not exist
CREATE TABLE IF NOT EXISTS Album (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each album
    name TEXT,                                   -- Name of the album
    artistName TEXT,                             -- Name of the artist
    runtime INTEGER,                             -- Total runtime of the album in seconds
    song_list TEXT                               -- List of song IDs (could be a comma-separated string or a JSON array)
);

-- Create a junction table for the many-to-many relationship if it does not exist
CREATE TABLE IF NOT EXISTS AlbumSong (
    album_id INTEGER,
    song_id INTEGER,
    PRIMARY KEY (album_id, song_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);