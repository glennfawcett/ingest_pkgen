# Ingest Auto PK Project

*FIRST DRAFT OF JUST ENVIRONMENT CREATION*

# Roachprod Create Prometheus Monitoring

## Create Cluster and Driver Machine
```bash

## Create workload driver
##
roachprod create glenn-driver -n 1 --lifetime 36h

## Create System Under Test (SUT)
##
roachprod create glenn-sut -n 3 --lifetime 36h
roachprod stage glenn-sut release v20.1.1
roachprod start glenn-sut

## Setup workload driver
##
roachprod create glenn-driver -n1 --lifetime 120h
roachprod stage glenn-driver release v20.1.1
roachprod ssh glenn-driver
sudo mv cockroach /usr/local/bin

## Download CRDB  (Other than Roachprod)
##
#wget -qO- https://binaries.cockroachdb.com/cockroach-v19.2.4.linux-amd64.tgz | tar  xvz
#cp -i cockroach-v19.2.4.linux-amd64/cockroach /usr/local/bin/
#chmod 755 /usr/local/bin/cockroach

##**Get IP address for host / haproxy**
roachprod pgurl glenn-sut:1   ##--- get IPaddress for host below

##**Setup HAproxy on Driver Machine**
sudo apt-get update -y
sudo apt-get install haproxy -y
cockroach gen haproxy --insecure   --host=(SUT internal IP)   --port=26257 
nohup haproxy -f haproxy.cfg &

## Download workload binary if needed
##
wget https://edge-binaries.cockroachdb.com/cockroach/workload.LATEST
chmod 755 workload.LATEST
cp -i workload.LATEST /usr/local/bin/workload  
chmod u+x /usr/local/bin/workload
yum install libncurses*

## SETUP JMETER on Driver if needed
sudo apt-get update
sudo apt install default-jre -y
wget https://apache.cs.utah.edu//jmeter/binaries/apache-jmeter-5.2.1.tgz
tar xvf apache-jmeter-5.2.1.tgz
cd apache-jmeter-5.2.1/lib
wget -O postgresql-42.2.11.jar https://jdbc.postgresql.org/download/postgresql-42.2.11.jar

## Setup Python if needed
sudo apt-get update
sudo apt install python3-pip
sudo pip3 install --upgrade pip
sudo apt-get install libpq-dev python-dev
sudo pip3 install psycopg2
```
