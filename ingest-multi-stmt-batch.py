# Import the driver.
import psycopg2
import psycopg2.errorcodes
import threading
import time
import random

usleep = lambda x: time.sleep(x/1000000.0)
msleep = lambda x: time.sleep(x/1000.0)

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
threadsPerHost = round(numThreads/3)
threads = []

# Define Host:Port / Injection endpoints
#
dbcons = []
dbcons.append(dbstr("ingestpkgen", "root", "localhost", 26257))
dbcons.append(dbstr("ingestpkgen", "root", "localhost", 26259))
dbcons.append(dbstr("ingestpkgen", "root", "localhost", 26261))

# Define Tables to Test
#
tables = []
tables.append('uuid_uuid')
tables.append('uuid_bytes')
tables.append('id_serial')
tables.append('id_seq')

# Runtime Per Table
runtime = 120

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
    
    time.sleep(10)

exit()
