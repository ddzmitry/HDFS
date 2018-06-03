#### putty login
_ssh user@127.0.0.1 -p 2222_
#### see HDFS file system
_hadoop fs -ls_
#### make a directory
_hadoop fs -mkdir <name>_
#### add to hadoop from Linux server
_hadoop fs -copyFromLocal <name>_
_hadoop fs -copyFromLocal <name> <locationFolder>/<name>_
#### remove data from hadoop cluster
_hadoop fs -rm <folder>/<file>_
#### remove directory 
_hadoop fs -rmdir  <dir>_
#### run python script
**python <name>.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar <dataset>**
