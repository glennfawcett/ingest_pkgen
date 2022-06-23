# AUTOPK Generation Tests

There were two series of tests performed.  Since the introduction of cached sequences, it made sense to re-run the tests 
to include this new functionality.

* [Ingest Tests v20.2.2](ingest_analysis.md) prio to CACHED sequences : December 2020
* [Ingest Tests v21.1.7](ingest_pk_seqcache_v21.md) with `CACHED` sequences : August 2021
* [Ingest Tests v22.1.2](ingest_unordered_analysis.md) using the `unordered_unique_rowid()` instead of sequences or `unique_rowid()`
