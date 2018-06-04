#### putty login
_ssh user@127.0.0.1 -p 2222_
#### see HDFS file system
_hadoop fs -ls_
#### make a directory
_hadoop fs -mkdir <name>_
#### Lookup Files
_hadoop fs -ls_
#### add to hadoop from Linux server
_hadoop fs -copyFromLocal <name>_
_hadoop fs -copyFromLocal <name> <locationFolder>/<name>_
#### remove data from hadoop cluster
_hadoop fs -rm <folder>/<file>_
#### remove directory 
_hadoop fs -rmdir  <dir>_
#### run python script
__python <name>.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar <dataset>__

#### PigScript (Examples)
__/PigScripts__

#### PySpark
__Installation__
#### RunScript
__spark-submit <name>.py__
#### Shell Access
Start with sbin/start-thriftserver.sh
Listens on port 10000 by default
Connect using bin/beeline -u jdbc:hive2://localhost:10000
__Query existing Tables hiveCtx.cacheTable("tablename");__
#### SET SPARK 2 as enviroment
export SPARK_MAJOR_VERSION=2
#### Hive 
__/HiveQueries__
##### To save query
hive -f /somepath/queries.hql

#### Sqoop
sqoop import --connect jdbc:mysql://localhost/movielends --driver
com.mysql.jdbc.Driver --table movies
##### Import data from MySQL directly 
sqoop import --connect jdbc:mysql://localhost/movielens --driver
com.mysql.jdbc.Driver --table movies
##### Incremental Import
--check-column and --last-value
##### Export from HIVE to MySQL
sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver
com.mysql.jdbc.Driver --table exported_movies --export-dir
/apps/hive/warehouse/movies --input-fields-terminated-by '\0001'
__Target table must already exist in MySQL,with columns and expected order__

### Work with Mysql
Hortonworks for mySQL
mysql -u root -p 
pw hadoop
SET names 'utf8';
SET CHARACTER SET utf8;
### ADD Permisiions to DB
__GRANT ALL PRIVILEGES ON movielens.* to ''@'localhost';__
#### sending data to HDFS
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1
#### sending data to HIVE
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1 --hive-import
#### scoop -> Hive ->  to MySQL
__sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver com.mysql.jdbc.Driver --table exported_movies 
--export-dir /aps/hive/warehouse/movies --input-fields-te rminated-by '\0001'__
### HBASE
 

 