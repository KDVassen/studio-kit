-- Enquiry storage.
--   kept = 1    the enquiry became work; it is exempt from the retention purge
--   suspect = 1 sent faster than a person plausibly could; kept, but check before replying
CREATE TABLE IF NOT EXISTS enquiries (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at INTEGER NOT NULL,
  name       TEXT    NOT NULL,
  email      TEXT    NOT NULL,
  business   TEXT,
  message    TEXT    NOT NULL,
  kept       INTEGER NOT NULL DEFAULT 0,
  suspect    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS enquiries_created ON enquiries (created_at);

-- Abuse limiting only. `hash` is a salted, daily-rotating hash of the sender's IP address (per /64 for IPv6),
-- never the address itself. Rows are deleted after 24 hours by the Worker's daily scheduled job.
CREATE TABLE IF NOT EXISTS rate_events (
  hash TEXT    NOT NULL,
  ts   INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS rate_events_hash_ts ON rate_events (hash, ts);
