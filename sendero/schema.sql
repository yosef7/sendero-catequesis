CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY);
INSERT OR IGNORE INTO schema_version VALUES (1);
CREATE TABLE IF NOT EXISTS levels (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, position INTEGER NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS requirements (
 id INTEGER PRIMARY KEY, level_id INTEGER NOT NULL REFERENCES levels(id), title TEXT NOT NULL,
 UNIQUE(level_id,title)
);
CREATE TABLE IF NOT EXISTS children (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, guardian TEXT NOT NULL DEFAULT '',
 contact TEXT NOT NULL DEFAULT '', joined TEXT NOT NULL, level_id INTEGER NOT NULL REFERENCES levels(id),
 archived INTEGER NOT NULL DEFAULT 0 CHECK(archived IN (0,1))
);
CREATE INDEX IF NOT EXISTS children_level ON children(level_id,archived);
CREATE TABLE IF NOT EXISTS completions (
 child_id INTEGER NOT NULL REFERENCES children(id), requirement_id INTEGER NOT NULL REFERENCES requirements(id),
 completed_at TEXT NOT NULL, PRIMARY KEY(child_id,requirement_id)
);
CREATE TABLE IF NOT EXISTS events (
 id INTEGER PRIMARY KEY, child_id INTEGER NOT NULL REFERENCES children(id),
 kind TEXT NOT NULL, happened TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS events_child ON events(child_id,happened DESC,id DESC);
CREATE TABLE IF NOT EXISTS attendance (
 child_id INTEGER NOT NULL REFERENCES children(id), day TEXT NOT NULL, topic TEXT NOT NULL,
 present INTEGER NOT NULL CHECK(present IN (0,1)), PRIMARY KEY(child_id,day)
);
