import sqlite3
import os

os.remove('music.db')

try:
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('music.db')
    cursor = sqliteConnection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS Song''')
    cursor.execute('''DROP TABLE IF EXISTS Album''')

    # create album table
    cursor.execute(
        '''CREATE TABLE Album (
                    id INT PRIMARY KEY,
                    name TEXT NOT NULL
                   );'''
    )

    # create song table
    cursor.execute(
        '''CREATE TABLE Song (
                   id INT PRIMARY KEY,
                   title TEXT NOT NULL,
                   album_id INT NOT NULL,
                   length INT NOT NULL,
                   url TEXT NOT NULL,
                   source TEXT,
                   description TEXT,
                   lyrics TEXT,
                   lyrics_source TEXT,
                   language TEXT,
                   release_year INT,
                   thumb_url TEXT,
                   thumb_size TEXT,
                   FOREIGN KEY (album_id) REFERENCES Album(id)
                   );'''
    )

    # create artist table
    cursor.execute(
        '''CREATE TABLE Artist (
                   id INT PRIMARY KEY,
                   artist_name TEXT NOT NULL);'''
    )

    # create playlist table
    cursor.execute(
        '''CREATE TABLE Playlist (
                   id INT PRIMARY KEY,
                   playlist_name TEXT NOT NULL);'''
    )

    # create genre table
    cursor.execute(
        '''CREATE TABLE Genre (
                   id INT PRIMARY KEY,
                   genre TEXT NOT NULL);'''
    )

    # create mood table
    cursor.execute(
        '''CREATE TABLE Mood (
                   id INT PRIMARY KEY,
                   mood TEXT NOT NULL);'''
    )

    # playlist-song table
    cursor.execute(
        '''CREATE TABLE Playlist_Song (
                   playlist_id INT NOT NULL,
                   song_id INT NOT NULL,
                   FOREIGN KEY (playlist_id) REFERENCES Playlist(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (song_id) REFERENCES Song(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # genre-song table

    cursor.execute(
        '''CREATE TABLE Genre_Song (
                   genre_id INT NOT NULL,
                   song_id INT NOT NULL,
                   FOREIGN KEY (genre_id) REFERENCES Genre(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (song_id) REFERENCES Song(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # mood-song table

    cursor.execute(
        '''CREATE TABLE Mood_Song (
                   mood_id INT NOT NULL,
                   song_id INT NOT NULL,
                   FOREIGN KEY (mood_id) REFERENCES Mood(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (song_id) REFERENCES Song(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # artist-song table

    cursor.execute(
        '''CREATE TABLE Artist_Song (
                   artist_id INT NOT NULL,
                   song_id INT NOT NULL,
                   FOREIGN KEY (artist_id) REFERENCES Artist(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (song_id) REFERENCES Song(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # artist-album table

    cursor.execute(
        '''CREATE TABLE Artist_Album (
                   artist_id INT NOT NULL,
                   album_id INT NOT NULL,
                   FOREIGN KEY (artist_id) REFERENCES Artist(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (album_id) REFERENCES Album(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # genre-artist table

    cursor.execute(
        '''CREATE TABLE Genre_Artist (
                   genre_id INT NOT NULL,
                   artist_id INT NOT NULL,
                   FOREIGN KEY (genre_id) REFERENCES Genre(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (artist_id) REFERENCES Artist(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    # genre-album table

    cursor.execute(
        '''CREATE TABLE Genre_Album (
                   genre_id INT NOT NULL,
                   album_id INT NOT NULL,
                   FOREIGN KEY (genre_id) REFERENCES Genre(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   FOREIGN KEY (album_id) REFERENCES Album(id) ON UPDATE CASCADE ON DELETE CASCADE
                   );'''
    )

    test = 'Test Album'
    TEST2 = 'Test Album 2'

    # add test entry
    cursor.execute(
        '''INSERT INTO Album (id, name) 
        VALUES ((SELECT IFNULL(MAX(id)+1, 1) FROM Album), ?)'''
        , (test,)
    )

    cursor.execute(
        '''INSERT INTO Album (id, name) 
        VALUES ((SELECT IFNULL(MAX(id)+1, 1) FROM Album), ?)'''
        , (TEST2,)
    )

    #commit changes
    sqliteConnection.commit()

    # Close the cursor
    cursor.close()

# Handle errors
# except sqlite3.Error as error:
#     print('Error occurred - ', error)

# Close DB Connection irrespective of success
# or failure
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')
