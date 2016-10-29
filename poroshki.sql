DROP TABLE IF EXISTS poroshki;
CREATE TABLE poroshki(
    id integer PRIMARY KEY,
    text varchar(1024) NOT NULL,
    posted timestamp,
    like_count integer,
    repost_count integer
);