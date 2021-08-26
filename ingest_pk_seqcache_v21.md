# Sequences with CACHE

Sequences that auto-increment are an anti-pattern to scaling ingest throughput with CockroachDB.  `UUID` was introduced to better distribute load with distributed SQL.  The issue is, not all applications can easily move to using a `UUID` as the primary key.  Often there are many sub-systems that rely on integers being used as the key.  To better optimize for these use cases, [cached sequences](https://www.cockroachlabs.com/docs/v21.1/create-sequence.html) were introduced.

By allowing each session to obtain a range of values, this lowers the hot-spot for a single counter.  Below are some tests run to ingest data into tables with *uuid* and *cached sequences* of 10k, 100k, and 1million values.

## Schema for ingest tests

```sql
CREATE SEQUENCE s10000 CACHE 10000 INCREMENT BY 1;
CREATE SEQUENCE s100000 CACHE 100000 INCREMENT BY 1;
CREATE SEQUENCE s1000000 CACHE 1000000 INCREMENT BY 1;

CREATE TABLE s10000t (
    id INT DEFAULT nextval('s10000') PRIMARY KEY,
    host STRING,
    port INT,
    thread_number INT,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false
);

CREATE TABLE s100000t (
    id INT DEFAULT nextval('s100000') PRIMARY KEY,
    host STRING,
    port INT,
    thread_number INT,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false
);

CREATE TABLE s1000000t (
    id INT DEFAULT nextval('s1000000') PRIMARY KEY,
    host STRING,
    port INT,
    thread_number INT,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false
);

CREATE TABLE uuid_uuid
(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    host STRING,
    port INT,
    thread_number INT,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false
);
```

## Results

