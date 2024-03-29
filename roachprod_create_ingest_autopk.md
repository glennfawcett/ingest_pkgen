# Ingest Auto PK Project

The ingest autoPK project shows how the Cluster and Driver machines were created.  The [ingest-pk-concurrent.py](ingest-pk-concurrent.py) python script was created to test all of the table types.  The runtime and code can easily be adjusted should you want to reuse it test your own table types.

## Create Cluster and Driver Machine

```bash
## Configure CockroachDB Cluster SUT
# roachprod create `whoami`-ingestpk --gce-machine-type 'n1-standard-16' --nodes 9 --lifetime 24h
roachprod create `whoami`-ingestpk --gce-machine-type 'n1-standard-4' --nodes 9 --lifetime 24h
# roachprod stage `whoami`-ingestpk release v20.2.2
# roachprod stage `whoami`-ingestpk release v21.1.7
roachprod stage `whoami`-ingestpk release v22.1.2
roachprod start `whoami`-ingestpk
roachprod pgurl `whoami`-ingestpk
roachprod adminurl `whoami`-ingestpk:1
        http://glenn-ingestpk-0001.roachprod.crdb.io:26258/

## Configure driver machine
roachprod create `whoami`-drive2 -n 1 --gce-machine-type 'n1-standard-16' --lifetime 24h
roachprod stage `whoami`-drive2 release v22.1.2
roachprod ssh `whoami`-drive2:1
sudo mv ./cockroach /usr/local/bin
sudo apt-get update -y
sudo apt install htop

## Download workload binary if needed
wget https://edge-binaries.cockroachdb.com/cockroach/workload.LATEST
chmod 755 workload.LATEST
sudo cp -i workload.LATEST /usr/local/bin/workload
sudo chmod u+x /usr/local/bin/workload

## Setup HA proxy
sudo apt-get update -y
sudo apt-get install haproxy -y
cockroach gen haproxy --insecure   --host=10.142.0.82   --port=26257 
nohup haproxy -f haproxy.cfg &

## Setup Python if needed
sudo apt-get update -y
# sudo apt install python3-pip -y
# sudo pip3 install --upgrade pip
sudo apt-get install libpq-dev python-dev python3-psycopg2 python3-numpy -y


## Put Python Script on Driver
# roachprod put glenn-drive:1 ./ingest-pk-concurrent.py
roachprod put glenn-drive2:1 ./ingest-pk-concurrent-v22.py 
```
