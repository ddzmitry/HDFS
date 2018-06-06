#### putty login
+ _ssh user@127.0.0.1 -p 2222_
#### see HDFS file system
+ _hadoop fs -ls_
#### make a directory
+ _hadoop fs -mkdir <name>_
#### Lookup Files
+ _hadoop fs -ls_
#### add to hadoop from Linux server
+ _hadoop fs -copyFromLocal <name>_
+ _hadoop fs -copyFromLocal <name> <locationFolder>/<name>_
#### remove data from hadoop cluster
+ _hadoop fs -rm <folder>/<file>_
#### remove directory 
+ _hadoop fs -rmdir  <dir>_
#### run python script
+ __python <name>.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar <dataset>__

#### PigScript (Examples)
+ __/PigScripts__

#### PySpark
+ __Installation__
#### RunScript
+ __spark-submit <name>.py__
#### Shell Access
+ Start with sbin/start-thriftserver.sh
+ >_Listens on port 10000 by default_
+ Connect using bin/beeline -u jdbc:hive2://localhost:10000
+ __Query existing Tables hiveCtx.cacheTable("tablename");__
#### SET SPARK 2 as enviroment
+ export SPARK_MAJOR_VERSION=2
#### Hive 
__/HiveQueries__
##### To save query
+ hive -f /somepath/queries.hql

#### Sqoop
_sqoop import --connect jdbc:mysql://localhost/movielends --driver
com.mysql.jdbc.Driver --table movies_
##### Import data from MySQL directly 
_sqoop import --connect jdbc:mysql://localhost/movielens --driver
com.mysql.jdbc.Driver --table movies_
##### Incremental Import
_--check-column and --last-value_
##### Export from HIVE to MySQL
_sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver
com.mysql.jdbc.Driver --table exported_movies --export-dir
/apps/hive/warehouse/movies --input-fields-terminated-by '\0001'_

+ **__Target table must already exist in MySQL,with columns and expected order__**

### Work with Mysql
**Hortonworks for mySQL**
+ mysql -u root -p 
+ pw hadoop
+ SET names 'utf8';`
+ SET CHARACTER SET utf8;
### ADD Permisiions to DB
__GRANT ALL PRIVILEGES ON movielens.* to ''@'localhost';__
#### sending data to HDFS
+ sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1
#### sending data to HIVE
+ sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1 --hive-import
#### scoop -> Hive ->  to MySQL
+ __sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver com.mysql.jdbc.Driver --table exported_movies 
--export-dir /aps/hive/warehouse/movies --input-fields-te rminated-by '\0001'__
### HBASE
+ __login as root__
+ __/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8000 --infoport 8001__
+ __/usr/hdp/current/hbase-master/bin/hbase-daemon.sh stop rest__
+ __importtsv__ -> to import big scale data
##### HBASE shell with Pig
+ hbase shell
+ create userstable with userinfo family in it
+ create 'users' ,'userinfo'
+ __pig PigScripts/hbase.pig'__
+ It creates table userId : {'userinfo:age,userinfo:gender,userinfo:occupation,userinfo:zip'}
+ __scan users -> displays table__

###### To drop table in HBASE firs you have to disable it
disable 'users'
drop 'users'

 #### Cassandra
 To install have to update Yum
 + yum update
 + yum install scl-utils (to run dif versions of python)
 + yum install centos-release-SCL (allows to switch between versions of python)
 + yum install python27
 + scl enable python27 bash
 
 `add directory in /etc/yum.repos.d/
  vim datastacks.repo`
  
  >name = DataStax Repo for Apache Cassandra
  >baseurl = http://rpm.datastax.com/community
  >enable = 1
  >gpgcheck = 0
 `
 + yum install dsc30
 + pip install cqlsh
 + __service cassandra start__
 + cqlsh --cqlversion="3.4.0"
 >`Uses Gossip Protocol every node does the same function and talking to each other and replecate itself`
 >__!NO JOINS!USES CQL!__
 Create keyspace 
 + _CREATE KEYSPACE movielens WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':'1'} AND durable_writes = true;_
 + USE movielens
 + _CREATE TABLE users (user_id int , age int , gender text , occupation text, zip text, PRIMARY KEY (user_id))_
 > To run actuall spark with cassandra we need to set up version spark to version 2 
 > as well we have to rout script to use cassandra --driver to execute spark script
 + **spark-submit --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 CassandraSpark.py**
#### Mongo DB and HDFS 
 _Installing on Ambari (connector is already exists)_
 + cd /var/lib/ambari-server/resources/stacks/HDP/2.5/services
 + Get connector FOR MONGO git clone https://github.com/nikunjness/mongo-ambari.git
 + sudo service ambari restart
 + login in ambari as admin add mongo as a service
 + install pymongo
 + export SPARK_MAJOR_VERSION=2
 + __When running script make sure ro specify versions scala(2.11)/spark(2.0.0)__
 + spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 MongoSpark.py
 * Setting index in mongo_db will make it faster 
 + *Example of aggregation:* _db.users.aggregate([{ $group: { _id: { occupation: "$occupation"}, avgAge: { $avg: "$age"}}}])_
#### Apache Drill (queringg HDFS using SQL )
 > Installation 
 + Download from mirror
 + wget it
 + tar -xvf 
 + bin/drillbit.sh start -Ddrill.exec.http.port=8765 (specified port)
 + Check Settings in apacheDrill
 + bin/drillbit.sh stop
#### Apache Phoenix (only for HBASE)
**Better optimization then ( Drill or MySQL) on HBASE**
   >Installation 
+ yum install phoenix
    > Use
+ cd /usr/hdp/current/phoenix-client/
+ cd bin
+ python sqline.py
+ !tables -> NO inserts USE upsert;
#### Presto 
 >Installation
 + web site docs get latest tarball
 + tar -xvf cd presto/bin/
 + CREATE YOUR OWN CONFIGS
 + go to bin abd get command line interface (from website) rename it to presto
 + chmod +x presto (add executable option)
 + bin/launcher start
 + connect to *CLI bin/presto --server 127.0.0.1:8090 --catalog hive,cassandra*
 + _to run Presto with cassandra we need thrift server_ !run cassandra! then nodetool enablethrift 
#### YARN Yet Another Resource Negotiator
 + Sits on top of HDFS
 + Split computation around cluster 
 + Maintains Data locality 
 + Allows SPARK, MR to be executed  on it 
 + HDFS -> Client Node -> YARN -> Node Manager(MR app master)
 + Monolithic Scheduler
#### MESOS Another resource negotiator
 + Came from Twitter (Takes intere pull of hardware)
 + Meant to solve a more general problem than YARN
 + Two Teared System (Google, Tweeter)
 + Uses Kuberentes / Docker
 + But YARN still better on HDFS because YARN negotiate bigger process betrween small ones 
 + MESOS can be working together with YARN 
 _"Hadoop on Mesos" package for Cloudera_
 #### ZooKeeper
 + Keeps track of information that must be synchronized across your luster
    **-Which Node is master?**
    **-What tasks are assigned to which workers?**
    **-Which workers are currently avaliable?**
 + ZooKeeper API Create,Delete,Existss,setData, getChildren
 + has to be at least 3-5 Zookeeper servers in ensemble 
     */
    |
    |_____/master (z Node ) "master1.foobar:2223"
    |
    |___/ worker
                |
                |
                |_worker1
                |
                |_worker2*
                
    + _cd /usr/hdp/current/zookeeper-client/bin/zkCli.sh_

  
 
 