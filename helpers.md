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


