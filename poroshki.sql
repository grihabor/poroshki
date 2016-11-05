DROP TABLE IF EXISTS poroshki;
CREATE TABLE poroshki(
    id integer PRIMARY KEY,
    text varchar(512) NOT NULL,
    text_length integer,
    posted timestamp,
    like_count integer,
    repost_count integer
);