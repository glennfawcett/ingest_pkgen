# Import the driver.
import psycopg2
import psycopg2.errorcodes
import threading
from threading import Thread
import time
import datetime
import random
import numpy
import uuid
import math 

usleep = lambda x: time.sleep(x/1000000.0)
msleep = lambda x: time.sleep(x/1000.0)

class dbstr:
  def __init__(self, database, user, host, port):
    self.database = database
    self.user = user
    # self.sslmode = sslmode
    self.host = host
    self.port = port

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def onestmt(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)

def boolDistro(dval):
    if dval >= random.random():
        return True
    else:
        return False


def create_ddl(connStr):
    
    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)
    onestmt(mycon, "DROP TABLE IF EXISTS id_uuid;")
    cr_id_uuid = """
    CREATE TABLE id_uuid
    (
        id UUID DEFAULT gen_random_uuid(),
        thread_number int, 
        host STRING,
        port int,
        ts TIMESTAMP DEFAULT current_timestamp(),
        archive boolean DEFAULT false,
        PRIMARY KEY (id)
    );
    """
    onestmt(mycon, cr_id_uuid)
        
    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)
    onestmt(mycon, "DROP TABLE IF EXISTS id_unordered;")
    cr_id_unordered = """
    CREATE TABLE id_unordered
    (
        id INT DEFAULT unordered_unique_rowid(),
        thread_number int,  
        host STRING,
        port int,
        ts TIMESTAMP DEFAULT current_timestamp(),
        archive boolean DEFAULT false,
        PRIMARY KEY (id)
    );
    """
    onestmt(mycon, cr_id_unordered)
    
    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)
    onestmt(mycon, "DROP TABLE IF EXISTS id_unordered;")
    cr_id_ordered = """
    CREATE TABLE id_ordered
    (
        id INT DEFAULT unique_rowid(),
        thread_number int,  
        host STRING,
        port int,
        ts TIMESTAMP DEFAULT current_timestamp(),
        archive boolean DEFAULT false,
        PRIMARY KEY (id)
    );
    """
    onestmt(mycon, cr_id_ordered)

def worker_steady(num, tpsPerThread, runtime, tablename):
    """ingest worker:: Lookup valid session and then account"""
    print("Worker Steady State")

    mycon = psycopg2.connect(connStr)
    mycon.set_session(autocommit=True)

    # Configure Rate Limiter
    if tpsPerThread == 0:
        Limit=False
        arrivaleRateSec = 0
    else:
        Limit=True
        arrivaleRateSec = 1.0/tpsPerThread
    
    threadBeginTime = time.time()
    etime=threadBeginTime
    
    # Insert into Table with AutoPK
    #
    iTemplate = """
    INSERT INTO {}(host, port, thread_number)
    VALUES ('{}',{},{})
    """

    execute_count = 0
    resp = []

    with mycon:
        with mycon.cursor() as cur:
            while etime < (threadBeginTime + runtime):
                # begin time
                btime = time.time()

                # Run the query from qFunc
                cur.execute(iTemplate.format(tablename, "localhost", 26257, num))
                execute_count += 1

                etime = time.time()
                resp.append(etime-btime)

                sleepTime = arrivaleRateSec - (etime - btime)

                if Limit and sleepTime > 0:
                    time.sleep(sleepTime)

            # print("Worker_{}:  Queries={}, QPS={}, P90={}!!!".format(num, execute_count, (execute_count/(time.time()-threadBeginTime)), numpy.percentile(resp,90)))

    return (execute_count, resp)


## Main
##

# TODO make command-line options
#
# s = q1()
# print("{}".format(s))


connStr = "postgres://root@127.0.0.1:26257/defaultdb?sslmode=disable"
create_ddl(connStr)

# Runtime Settings
runtime = 900
numThreads = 64

QPS = 0  # no throttle if 0
qpsPerThread = QPS/numThreads

tables = []
tables.append('id_ordered')
tables.append('id_unordered')
tables.append('id_uuid')

# results array for QPS and p99
results = []

for tab in tables:
    
    # Threads
    threads1 = []
    
    # Query Counters
    tq1 = 0
    tq1resp = []
 
    for i in range(numThreads):
        t1 = ThreadWithReturnValue(target=worker_steady, args=((i+1), qpsPerThread, runtime, tab))
        threads1.append(t1)
        t1.start()

    # Wait for all of them to finish
    for x in threads1:
        qc, ra = x.join()
        tq1 = tq1 + qc
        tq1resp.extend(ra)


    print("{} Rows Inserted : {}".format(tab, tq1))
    print("{} QPS : {}".format(tab, tq1/runtime))
    print("{} respP99 : {}".format(tab, numpy.percentile(tq1resp,99)))
    
    ## Append Results summary
    lastrun = []
    lastrun.append(tab)
    lastrun.append(tq1/runtime)
    lastrun.append(numpy.percentile(tq1resp,99))

    results.append(lastrun)

    time.sleep(1)

print ("{:>30}  {:>10}  {:>10}".format('Table','QPS','respP99'))
print ("{}".format("-"*70))
for a in results:
    print("{:>30}  {:>10.1f}  {:>10.6f}".format(a[0], a[1], a[2]))

exit()

