# Ingest Auto PK Project


## Create Cluster and Driver Machine

```bash
## Configure CockroachDB Cluster SUT
# roachprod create `whoami`-ingestpk --gce-machine-type 'n1-standard-16' --nodes 9 --lifetime 24h
roachprod create `whoami`-ingestpk --gce-machine-type 'n1-standard-4' --nodes 9 --lifetime 24h
roachprod stage `whoami`-ingestpk release v21.1.7
roachprod start `whoami`-ingestpk
roachprod pgurl `whoami`-ingestpk
roachprod adminurl `whoami`-ingestpk:1
        http://glenn-ingestpk-0001.roachprod.crdb.io:26258/

## Configure driver machine
roachprod create `whoami`-drive -n 1 --lifetime 24h
roachprod stage `whoami`-drive release v21.1.7
roachprod ssh `whoami`-drive:1
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
cockroach gen haproxy --insecure   --host=10.142.0.27   --port=26257 
nohup haproxy -f haproxy.cfg &

## Setup Python if needed
sudo apt-get update
sudo apt install python3-pip -y
sudo pip3 install --upgrade pip
sudo apt-get install libpq-dev python-dev python3-psycopg2 python3-numpy -y


## Put Python Script on Driver
roachprod put glenn-drive:1 ./ingest-pk-concurrent.py 
```
