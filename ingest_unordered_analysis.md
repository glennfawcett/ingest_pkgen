# Ingest Tests with unordered_unique_rowid() function

With distributed SQL datatabases, it is important that data gets distributed well across the nodes of the cluster.  This series of tests show how then new `unordered_unique_rowid()` function in v22.1 is able to compare to `unique_rowid()` as well as `gen_random_uuid()`.  For details on these built-in functions a [link](https://github.com/cockroachdb/cockroach/blob/6eb3bf0a6fba3554aaf6c74f60c06cf1a4316a67/pkg/sql/sem/builtins/builtins.go#L2155) to the code is provided.

##  Results


### Round 1

```bash
                         Table         QPS     respP99
----------------------------------------------------------------------
                       id_uuid     16349.8    0.016455
                  id_unordered     16995.4    0.014020
```

### Round 2

```bash

```