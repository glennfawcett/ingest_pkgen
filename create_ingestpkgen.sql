USE DEFAULTDB;
DROP DATABASE ingestpkgen CASCADE;

CREATE DATABASE ingestpkgen;
USE ingestpkgen;

-- UUID using UUID data type
--
CREATE TABLE uuid_uuid
(
    id UUID DEFAULT gen_random_uuid(),
    thread_number int, 
    host STRING,
    port int,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false,
    PRIMARY KEY (id)
);

-- UUID using BYTES data type and uuid_v4()
--
CREATE TABLE uuid_bytes (
    id BYTES DEFAULT uuid_v4(),
    thread_number int, 
    host STRING,
    port int,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false,
    PRIMARY KEY (id)
);

-- Serial using INT
--
CREATE TABLE id_serial
(
    id SERIAL,
    thread_number int,  
    host STRING,
    port int,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false,
    PRIMARY KEY (id)
);

-- Sequence using INT
--
CREATE SEQUENCE seqid INCREMENT BY 1;
CREATE TABLE id_seq (
    id INT DEFAULT nextval('seqid'),
    thread_number int,
    host STRING,
    port int,
    ts TIMESTAMP DEFAULT current_timestamp(),
    archive boolean DEFAULT false,
    PRIMARY KEY (id)
);

ALTER DATABASE ingestpkgen CONFIGURE ZONE USING num_replicas = 3, gc.ttlseconds = 600;


select count(*), 'id_seq' as test_table from id_seq;
select count(*), 'id_serial' as test_table from id_serial;
select count(*), 'uuid_bytes' as test_table from uuid_bytes;
select count(*), 'uuid_uuid' as test_table from uuid_uuid;

-- Test Insert... be sure to truncate before test run
--
insert into id_seq (host, port, thread_number)
select 'host1', 26257, 1 from generate_series (1,1);
insert into id_seq (host, port, thread_number)
select 'host1', 26258, 2 from generate_series (1,1);
insert into id_seq (host, port, thread_number)
select 'host2', 26257, 1 from generate_series (1,1);
insert into id_seq (host, port, thread_number)
select 'host3', 26257, 1 from generate_series (1,1);

