DROP TABLE IF EXISTS music;

CREATE TABLE music
(
    song_id CHAR(9) NOT NULL,
    name VARCHAR(35) NOT NULL,
    artist VARCHAR(40),
    genre VARCHAR(30),
    location VARCHAR(60) NOT NULL,
    date_of_release DATE,
    PRIMARY KEY (song_id)
);

INSERT INTO music (song_id, name, artist, genre, location, date_of_release) VALUES

    ('000000001', 'Actionable', 'Bensound', 'Rock', 'music/bensound-actionable.mp3', null),
    ('000000002', 'Creep', 'Bensound', 'Freaky', 'music/bensound-creepy.mp3', null),
    ('000000003', 'Dubstep', 'Bensound', 'Hiphop', 'music/bensound-dubstep.mp3', null),
    ('000000004', 'Energy', 'Bensound', 'Electric', 'music/bensound-energy.mp3', null),
    ('000000005', 'Epic', 'Bensound', 'Electric', 'music/bensound-epic.mp3', null),
    ('000000006', 'Funky Element', 'Bensound', 'Punk', 'music/bensound-funkyelement.mp3', null),
    ('000000007', 'Going Higher', 'Bensound', 'rock', 'music/bensound-goinghigher.mp3', null),
    ('000000008', 'Groovy Hiphop', 'Bensound', 'Hiphop', 'music/bensound-groovyhiphop.mp3', null),
    ('000000009', 'Highoctane', 'Bensound', 'rock', 'music/bensound-highoctane.mp3', null),
    ('000000010', 'House', 'Bensound', 'rock', 'music/bensound-house.mp3', null),
    ('000000011', 'Love', 'Bensound', 'rock', 'music/bensound-love.mp3', null),
    ('000000012', 'Moose', 'Bensound', 'rock', 'music/bensound-moose.mp3', null),
    ('000000013', 'Psychedelic', 'Bensound', 'rock', 'music/bensound-psychedelic.mp3', null),
    ('000000014', 'Retro Soul', 'Bensound', 'rock', 'music/bensound-retrosoul.mp3', null),
    ('000000015', 'Rumble', 'Bensound', 'rock', 'music/bensound-rumble.mp3', null),
    ('000000016', 'Sexy', 'Bensound', 'rock', 'music/bensound-sexy.mp3', null),
    ('000000017', 'Happyrock', 'Bensound', 'rock', 'music/happyrock.mp3', null);


