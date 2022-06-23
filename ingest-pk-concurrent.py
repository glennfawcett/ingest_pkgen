# Import the driver.
import psycopg2
import psycopg2.errorcodes
import threading
import time
import random

usleep = lambda x: time.sleep(x/1000000.0)
msleep = lambda x: time.sleep(x/1000.0)

def create_ddl(connStr):
    
    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)
    crbigfastddl1 = """
    CREATE TABLE IF NOT EXISTS ingest_stress (
        uuid1 UUID NOT NULL,
        uuid2 UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL,
        j JSONB NOT NULL,
        id1 INT8 NULL AS ((j->>'k1':::STRING)::INT8) STORED,
        id2 INT8 NULL AS ((j->>'k2':::STRING)::INT8) STORED,
        id3 INT8 NULL AS ((j->>'k3':::STRING)::INT8) STORED,
        id4 INT8 NULL AS ((j->>'k4':::STRING)::INT8) STORED,
        INDEX idx_id1 (id1, created_at DESC),
        INDEX idx_id1_storing (id1, created_at DESC) STORING (id2),
        PRIMARY KEY (uuid1, uuid2)
    );
    """
    #     ) WITH (ttl = 'on', ttl_automatic_column = 'on', ttl_expire_after = '24:00:00':::INTERVAL, ttl_label_metrics='true');

    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)
    onestmt(mycon, "set experimental_enable_hash_sharded_indexes=true;")
    onestmt(mycon, "DROP TABLE IF EXISTS ingest_stress;")
    onestmt(mycon, crbigfastddl1)
    onestmt(mycon, "ALTER TABLE ingest_stress SPLIT AT select gen_random_uuid() from generate_series(1,16);")
    onestmt(mycon, "ALTER INDEX ingest_stress@idx_id1 SPLIT AT select  generate_series(1,100);")


class dbstr:
  def __init__(self, database, user, host, port):
    self.database = database
    self.user = user
    # self.sslmode = sslmode
    self.host = host
    self.port = port

def onestmt(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)

def getcon(dc):
    myconn = psycopg2.connect(
        database=dc.database,
        user=dc.user,
        sslmode='disable',
        port=dc.port,
        host=dc.host
    )
    return myconn

def worker_steady(num, tpsPerThread, targetTable, dbstr, runtime):
    """ingest worker:: Lookup valid session and then account"""
    print("Worker Steady State")

    mycon = getcon(dbstr)
    mycon.set_session(autocommit=True)

    # Insert into Table with AutoPK
    #
    iTemplate = """
    INSERT INTO {}(host, port, thread_number)
    VALUES ('{}',{},{})
    """

    # Configure Rate Limiter
    if tpsPerThread == 0:
        Limit=False
        arrivaleRateSec = 0
    else:
        Limit=True
        arrivaleRateSec = 1.0/tpsPerThread
    
    threadBeginTime = time.time()
    etime=threadBeginTime

    with mycon:
        with mycon.cursor() as cur:
            while etime < (threadBeginTime + runtime):
                # begin time
                btime = time.time()

                cur.execute(iTemplate.format(targetTable, dbstr.host, dbstr.port, num))
                # iRows = cur.fetchall()

                etime = time.time()

                sleepTime = arrivaleRateSec - (etime - btime)

                if Limit and sleepTime > 0:
                    time.sleep(sleepTime)

            print("Worker: {} Finished!!!".format(num))


## Main
##

# TODO make command-line options
#
QPS = 0
numThreads = 36
qpsPerThread = QPS/numThreads
threadsPerHost = round(numThreads)
threads = []

# Define Host:Port / Injection endpoints
#
dbcons = []
dbcons.append(dbstr("defaultdb", "root", "localhost", 26257))


# Define Tables to Test
#
tables = []
tables.append('uuid_uuid')
# tables.append('uuid_bytes')
tables.append('id_serial')
# tables.append('id_seq')
# tables.append('s1000000t')
# tables.append('s100000t')
# tables.append('s10000t')
# tables.append('s1000t')
# tables.append('s100t')
# tables.append('s10t')
# tables.append('s0t')


# Runtime Per Table
runtime = 900

for tab in tables:
    print ("Inserting to table: {}".format(tab))
    for c in dbcons:
        for i in range(threadsPerHost):
            t = threading.Thread(target=worker_steady, args=((i+1),qpsPerThread,tab,c,runtime))
            threads.append(t)
            t.start()

    # Wait for all of them to finish
    for x in threads:
        x.join()
    
    time.sleep(60)

exit()
