select
    'uuid_uuid' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from uuid_uuid)) as Threads,
    (e_ts - b_ts)::int loadSeconds, 
    cnt as rowsLoaded, 
    (cnt/(e_ts - b_ts)::int)::int as rowsPerSecond
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
    's1000000t' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from s1000000t)) as Threads,
    (e_ts - b_ts)::int loadSeconds, 
    cnt as rowsLoaded, 
    (cnt/(e_ts - b_ts)::int)::int as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from s1000000t
)
union all
select 
    's100000t' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from s100000t)) as Threads,
    (e_ts - b_ts)::int loadSeconds, 
    cnt as rowsLoaded, 
    (cnt/(e_ts - b_ts)::int)::int as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from s100000t
)
union all
select 
    's10000t' as autoPkTable,
    (select count(a) from (select distinct host, port, thread_number as a from s10000t)) as Threads,
    (e_ts - b_ts)::int loadSeconds, 
    cnt as rowsLoaded, 
    (cnt/(e_ts - b_ts)::int)::int as rowsPerSecond
from 
(
    select 
        max(extract('epoch',ts)) as e_ts, 
        min(extract('epoch',ts)) as b_ts,
        count(*) as cnt
    from s10000t
);
order by 1;
