CREATE TABLE IF NOT EXISTS cells (
    uid    INTEGER PRIMARY KEY,
    type   INTEGER NOT NULL,
    hash   TEXT    NOT NULL UNIQUE,
    ext    TEXT    NOT NULL,
    width  INTEGER,
    height INTEGER,
    size   INTEGER NOT NULL,
    added  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    extra  TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    uid  INTEGER PRIMARY KEY,
    name TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS cell_tags (
    cell_uid INTEGER NOT NULL REFERENCES cells(uid) on DELETE CASCADE,
    tag_uid  INTEGER NOT NULL REFERENCES tags(uid)  on DELETE CASCADE,
    PRIMARY KEY (cell_uid, tag_uid)
);

CREATE INDEX IF NOT EXISTS cell_tags_index_tag ON cell_tags(tag_uid);
