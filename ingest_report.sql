select
    'uuid_uuid' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from uuid_uuid)) as Threads,
    (e_ts - b_ts) loadSeconds, 
    cnt as rowsLoaded, 
    cnt/(e_ts - b_ts) as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from uuid_uuid
)
union all 
select 
    'uuid_bytes' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from uuid_bytes)) as Threads,
    (e_ts - b_ts) loadSeconds, 
    cnt as rowsLoaded, 
    cnt/(e_ts - b_ts) as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from uuid_bytes
)
union all
select 
    'id_serial' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from id_serial)) as Threads,
    (e_ts - b_ts) loadSeconds, 
    cnt as rowsLoaded, 
    cnt/(e_ts - b_ts) as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from id_serial
)
union all
select 
    'id_seq' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from id_seq)) as Threads,
    (e_ts - b_ts) loadSeconds, 
    cnt as rowsLoaded, 
    cnt/(e_ts - b_ts) as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from id_seq
)
order by 1;