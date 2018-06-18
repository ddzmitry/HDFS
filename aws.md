
##### Create Pem File
+ openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
#### Install mySQL on cloud
+ yum -y update _(update all packages)_
+ yum -y install mysql-server mysql-connector-java _(install connector and install server)_
+ *to check status of mySql instance* _service mysqld status_
+ *to start service of mySQL* _service mysqld start_
+ *to start service every time when starting up the system* chkconfig mysqld on 
+ `/usr/bin/mysql_secure_installation` run secure installation
+ *login from localhost* mysql -u root -h localhost -p
+ `create user 'temp'@'%' identified by 'password123'`;
+ `grant all privileges on *.* to 'temp'@'%' with grant option;`;
+ __then you can log in as temp__
+ mysql -u temp -h localhost -p
+ _To see firewall_ *service iptables status*
+ _To stop firewall_ *service iptables stop*
+ _To make sure that firewall off every time when restart server_ chkconfig iptables off
+ iptables --flush
#### Installing Cloudera 
+ wget http://archive.cloudera.com/cm5/installer/latest/cloudera-manager-installer.bin
+ chmod u+x cloudera-manager-installer.bin
+ make sure SeLinux is disabled `getenforce`
+ *IMPORTANT*
+ echo 10 > /proc/sys/vm/swappiness
+ vim /etc/selinux/config
+ _SET_ SELINUX=disabled
+ Or you can do it `sed -i 's/SELINUX=enforcing/SELINUX=disabled' /etc/sysconfig/selinux`
+ echo never > /sys/kernel/mm/transparent_hugepage/enabled
+ `echo "echo never > /sys/kernel/mm/transparent_hugepage/enabled" >> /etc/rc.local`
+  /sbin/shutdown -r now `restart`
+ Open Ports for current IP address
+ http://ipaddress:7180/
+ Spin up 3 more server boxes from AMIs and add them to hosts in Cloudera management
+ Make sure to set properly Inbound and Outbound traffic
+ use .pem file to provide all root access to nodes 
+`sudo -u hdfs hdfs dfsadmin -safemode leave`
+ `Cloudera recommends setting /proc/sys/vm/swappiness to a maximum of 10. Current setting is 60. Use the sysctl command to change this setting at run time and edit /etc/sysctl.conf for this setting to be saved after a reboot. You can continue with installation, but Cloudera Manager might report that your hosts are unhealthy because they are swapping. The following hosts are affected:`
+ `Transparent Huge Page Compaction is enabled and can cause significant performance problems. Run "echo never > /sys/kernel/mm/transparent_hugepage/defrag" and "echo never > /sys/kernel/mm/transparent_hugepage/enabled" to disable this, and then add the same command to an init script such as /etc/rc.local so it will be set on system reboot. The following hosts are affected:`
#### Manually installing cloudera with apache

+ > Important Steps For Centos 6.5
+ image ami-8997afe0 30gb (CentOS 6.5)
+ Open Ports
+ Disable selinux `vim /etc/selinux/config SELINUX=disabled`
+ Turn off IP tables `service iptables stop`  _and_ `chkconfig iptables off` to make sure service will be off once system is rebooted
+ Resize hard disc so it can recalcuilate actuall space (df -h) `resize2fs /dev/xvde`
+ Change (swappiness) `cat /proc/sys/vm/swappiness` `=>` `echo "vm.swappiness=1" >> /etc/sysctl.conf`
 
+ > Creating Server Box that will host files
+ Spin UP CentOS box
+ yum -y install httpd
+ chkconfig httpd on *have it running at all the time*
+ service httpd restart
+ service iptables stop
+ /var/www/html/ is a directory where files are stored
+ Cloudera hostes tarballs on http://archive.cloudera.com/cm5/repo-as-tarball/5.14.1/
+ *tar zxvf cm5.14.1-centos7.tar.gz  -C /var/www/html/cm/*
+ and it is avaliable online 
+ _Parcels_ http://archive.cloudera.com/cdh5/parcels/5.14/

+ > For CentOS7 AMI
+ you can create script that will be runned when user logges into machine
+ /etc/systemd/system/disable-thp.service
+ look `/Transparent_huge_pages.sh`
+ https://blacksaildivision.com/how-to-disable-transparent-huge-pages-on-centos
+ sudo systemctl daemon-reload
+ sudo systemctl start disable-thp
+ sudo systemctl enable disable-thp
+ *To Change Swappiness*`echo "vm.swappiness = 1" >> /etc/sysctl.conf`
+ yum -y update
+ yum -y install ntp
+ chkconfig ntpd on
+ service ntpd start
+ yum -y install yum-utils

+ _FINAL CHECK_
+   cat /etc/sysconfig/selinux ("MUST BE DISABLED")
+   cat /etc/selinux/config ("MUST BE DISABLED")
+   cat /sys/kernel/mm/transparent_hugepage/enabled ([never])
+   cat /sys/kernel/mm/transparent_hugepage/defrag ([never])
+   cat /proc/sys/vm/swappiness (1)

##### Addig repository to box
+ cd cd /etc/yum.repos.d/
+ vim cloudera-manager.repo
+ check `cloudera-manager.repo`
+ yum clean all (to clean cache)
+ yum makecache
+ yum list all | grep cloudera (To ensure that repo is avaliable)
+ _NOW WE CAN CREATWE AN IMAGE!!!!_

#### Cloudera Manager installation from box with repo
+ yum -y install mysql-connector-java (To Connect to DB service)
+ yum -y install mariadb-server mariadb (MySQL server)
+ Make sure you have another box with mySQL installed
+ mysql -u 'temp' -h 'ip-address' -p (To check connection)
+ `yum -y install cloudera-manager-agent.x86_64 cloudera-manager-daemons.x86_64 cloudera-manager-server.x86_64 oracle-j2sdk1.7.x86_64`
+ add config in `/etc/default/cloudera-scm-server`
+ export JAVA_HOME=/usr/java/jdk1.7.0_67-cloudera/
+ cd /usr/share/cmf/schema/
+ `make sure that there is scm user created in databases befor running next step`
+ /usr/share/cmf/schema/scm_prepare_database.sh mysql -hMY_SQL_SERVER.com -utemp -ppassword123 --scm-host CLOUDERA_MANAGER_HOST.com scm scm scm (user,database,password)
+ /etc/cloudera-scm-agent 'Change server_host on appropriate one *the server where agent is running*'
+ `service cloudera-scm-server start`
+ chkconfig cloudera-scm-server on
+ `service cloudera-scm-agent start`
+ chkconfig cloudera-scm-agent on
+ port 7180 
#### Adding agents to current cloudera manager
+ spin up 3 more AMIs with all prerequisites done `For CentOS7 AMI`
+ Login into Workers
+ sudo su
+ yum -y install cloudera-manager-agent.x86_64 cloudera-manager-daemons.x86_64 oracle-j2sdk1.7.x86_64
+ cd /etc/default/
+ vim cloudera-scm-agent 'set $JAVA_HOME=/usr/java/jdk1.7.0_67-cloudera/'
+ export JAVA_HOME=/usr/java/jdk1.7.0_67-cloudera/
+ vim /etc/cloudera-scm-agent/config.ini
+ _Change Host on which one cloudera manager is running_
+ `service cloudera-scm-agent start`
+ chkconfig cloudera-scm-agent on
+ go to :7180/cmf/express-wizard/hosts (select 3 except the manager one)
+ for parcels  link add the one we created on httd server
#### Creating Databases (for reportmanager,hue,hive,oozie)
+ create database hue;
+ create user 'hue'@'%' identified by 'password123';
+ grant all privileges on hue.* to 'hue'@'%';

+ create database hive;
+ create user 'hive'@'%' identified by 'password123';
+ grant all privileges on hive.* to 'hive'@'%';

+ create database oozie;
+ create user 'oozie'@'%' identified by 'password123';
+ grant all privileges on oozie.* to 'oozie'@'%';

+ Go back to console and finish install as well as provide host for database
+ IF ERROR `JDBC driver cannot be found. Unable to find the JDBC database jar on host : ip-172-31-44-90.ec2.internal.
`
+ Go to that server and `yum -y install mysql-connector-java`

#### HDFS Commands
+ Make sure JAVA_HOME is set and JAVA_HOME/bin is in the $PATH
+ Can run from any box you are currently on
+ su hdfs (*will make you as a users of hdfs*)
+ hdfs dfs 
+ `hdfs dfs -put test.txt /test.txt` - To put Files
+ `hdfs dfs -ls /` - To List Files 
+ `hdfs dfs -setrep 2 /test.txt` - To set replecations on file
+ `hdfs fsck / -files -blocks` - Will show blocks of HDFS
+ `hdfs dfs -cat /test.txt` - Will give content on File
+ `hdfs dfs -tail /test.txt` - Will show end of the file
+ `hdfs dfs -count /` - Will count directories
+ `hdfs dfs -count -q /` - Will give quota
+ `hdfs dfs -count -du /` - Will give detailed report
+ `hdfs dfs -get /test.txt ./fromhdfs.txt` - Will get a file on local system
+ `hdfs dfs -get /test.txt ./fromhdfs.txt ` - Will get a file on local system
+ `mkdir -p /var/lib/hadoop-hdfs/mydir && hdfs dfs -get /test.txt /var/lib/hadoop-hdfs/mydir/hadoopget.txt` - `-p` Will create folder
+ `hdfs dfs -mkdirectory /dzmitry` - Will create directiory
+ `hdfs dfs -touchz /dzmitry/dzmitrycoolfile.txt` - Will create file
+ `hdfs dfs -test -e /filename.txt  ` - Will check if file exists
+ `hdfs dfs -test -z /filename.txt  ` - Will check if file zero length
+ `hdfs dfs -test -d /filename.txt  ` - Will check if file is directory
+ `echo ?q` - returns the last command result
+ `hdfs dfs -chmod 775 /test.txt` - will set permissons on file

#### HDFS Trash
+ `hdfs dfs -rm /trash.txt` -will remove into trash 
+ `hdfs dfs -rm -skipTrash  /skiptrash.txt` - will remove without trashing it first
+ `hdfs dfs -mv /user/centos/.Trash/Current/test.txt /recovery_text.txt` - Remove file from trash
+ ` hdfs dfs -expunge` - will expunge all trash and create a checkpoint `/timestamp` folder 
#### HDFS High Availability
#### Enable High Availability for HDFS
+ _Avaliable via one click_ in HDFS Action settings
> Will force zookeeper  to be installed on all of these nodes 
+ Enable High Availability Command
+ If NameNode will shut down > Fallover Controle will put the job on another nameNode(Standby)
+ `Zookeeper takes care of it` 
#### HDFS Balancer
+ Can be set on any node
+ In Scope of balancer 
+ Can be Rablanced
#### HDFS Maintains Mode
+ Taking HDFS into blocks will go under replication mode
+Maintenance State Minimal Block Replication set replica to 1 
#### HDFS Quota Manager
+ File quota can be set on folders top store certaine amount of files
+ `hdfs dfs -count -q -h -v /folder` - File Count and quota of it 
+ `hdfs fsck /folder/file` - Will show the blocks that file takes per block
+ `find .blockname` - Will show directory where folder stored at
+ `hdfs dfsadmin -setQuota 6 /testfolder` - set Quota
+ `hdfs dfsadmin -clrQuota 6 /testfolder` - clear Quota
+ `hdfs dfsadmin -setSpaceQuota 6 /testfolder` - Set Space  Quota `Allowed prefixes are k, m, g, t, p`
+ `hdfs dfsadmin -clrSpaceQuota 6 /testfolder` - Remove Space  Quota
##### HDFS Canary Test
+ HDFS -> Canary - Specify location for long time files 
#### HDFS Racks 
+ Make Cluster Highly avaliable
+ Defines based of the zones 
+ Increase a probability that server will still work
+ `var/run/cloudera-scm-agent/process` - Will describe all process that are going on cluster
+ `dfs/nn/current`  - Will have current logs and fsimages (passed/inProgress)
+ You can use fsimages for backing up 
+ `hdfs oiv -i fs_imagefile` - To be able to see fsImage content (Have to be on nameNode server)
+ This will open ofline session on which one you can see what files are avaliable
+ `hdfs dfs -ls webhdfs://127.0.0.1:5978/` - Will show what files were avalialble at that time _AMAZING_
+ `hdfs oiv -i fs_imagefile -p XML -o /var/lib/hadoop-hdfs/prev_files.xml` - Will dump fsimage into xml file
+ You can also see what edit logs were happening on cluster `dfs/nn/current` 
+ `hdfs oev -i edits_file -p xml -o /var/lib/hadoop-hdfs/filename_.xml`
+ Checkpoints work like backup version logs you can roll back to if something happens 
#### Roll Testing
+ hdfs dfs -mkdir /filename
+ edit_in_progress will be updated (so you can see what is going as transaction on folder)
+ `hdfs oev -i edits_file -p xml -o /var/lib/hadoop-hdfs/filename_.xml` - to see what is there
+ Once you roll edits "Cloudera UI" will create new edits_inprogress file
+ If the edits were destroyed Cloudera can use fsimage to recover 
####  HDFS Save Namespace
+ Create couple files 
+ HDFS `->` Action `->` Roll Edits
+ Ypu can see ofline what files were on fsimage `hdfs oiv -i fs_imagefile`
+ To do Save Namespace you have to put NameMode into Enter `Savemode`
+ in `hdfs-site` you can maintain how many checkpoints (fsimages,editlogs) will be saved
+ Save namespace will create new `fs_image`
+ from command line `hdfs dfsadmin -rollEdits` _New segment starts at txid 50879_
#### To do Save Namespace from CMD
+ `hdfs dfsadmin -safemode enter`
+ _Cant add any files on NameNode_
+ `hdfs dfsadmin -saveNamespace`
+ `hdfs dfsadmin -safemode leave`
+ `hdfs dfsadmin -rollEdits`
#### HDFS Snapshots 
+ Go to HDFS point to folder and Enable Snapshot
+ You can also restore from snapshot as well 
+ *with cmd*
+ `hdfs dfs -mkdir /snapshotshelltest`
+ `hdfs dfsadmin -allowSnapshot /snapshotshelltest`
+ `hdfs dfs -createSnapshot /snapshotshelltest filePath`
+ `hdfs snapshotDiff /snapshotshelltest with0files with2files` - To see differents between snapshots
+ `hdfs lsSnapshottableDir` - Will show all directories where snapshots are stored
+ Before disallowing snapshots you have to remove all previous once
+ hdfs dfs -deleteSnapshot /snapshotshelltest with2files
+ `hdfs dfsadmin -disallowSnapshot /snapshotshelltest`
#### HDFS Snapshots Policy
+ Can be set as cron job in Baclup settings on Cloudera
+ Create snapshots for backup
#### HDFS Edge Node
+ Usually the one node that USER uses
+ Spinup centos 7 add all configs for agent
+ Add it to Cluster
+ Go To HDFS and  assign Gateway service to it 
+ Deploy Change Configs
+ We can allow acces only to the Edge Node (That Point we protect all other nodes from running on them)
+ We use That machie for accessing HDFS
+ Create Security Configurations where all ports will be closed exept the one that is EdgeNode
#### Web HDFS
+ To access Hadoop through  RESTApi
+ HDFS Configs `->` webhdfs
+ *Example*  `curl -i -X PUT "http://hostaddress:50070/webhdfs/v1/webhdfstest?user.name=hdfs&op=MKDIRS"`
+ *Example*  `curl -i -X PUT "http://hostaddress:50070/webhdfs/v1/test.txt?user.name=hdfs&op=CREATE"`
+ _DOCS_ https://hadoop.apache.org/docs/r1.0.4/webhdfs.html
#### HDFS httpFS
+ Complete control on security
+ Can be added as a service on one of the hosts
+ Redeploy New settings /Restart Services
+ API will be avaliable on that host at port 14000
+ `curl "http://host:14000/webhdfs/v1/?op=LISTSTATUS&user.name=hdfs"` *get list status*
+ `curl -X PUT "http://host:14000/webhdfs/v1/httpFSTest?user.name=hdfs&op=MKDIRS" `
+ `curl -X PUT "http://host:14000/webhdfs/v1/file.txt?user.name=hdfs&op=CREATE" `
+ Creation will return cookie that will authenticate user to talk back to server
+ Also Works Great With Postman
+ Uses Proxy
#### HDFS FSCK Utility
+ `hdfs fsck /` - To check health of the system
+ `hdfs fsck /file.txt -files -blocks -locations` - Show where and how blocks of file are stored
+ `hdfs getconf -confKey dfs.replication` - Show Replicas
+  Check Blocks Where Data is avaliable using block id `blk_1073748012`
+ `hdfs fsck / -blockId blk_1073748012` - Check Where block is located
+ `find . -name " blk_1073748012" ` - find block by name
+ if fileBlocks werte corrupted we will have to remove the file
+ `hdfs dfsadmin -triggerBlockReport ip:50020` - To trigger BlockReport
#### HDFS Recovery
+ `hdfs namenode recovery` - will fire up recovery if any data was missing will recover from `fs_images,edits_file`
#### HDFS Federation
+ Horizontal Scalability of NameNode
+ HDFS `->` Configurations `->` nameservice
+ adding nameservice will provide High Availability and Federations
+ Will Peovide BlockPools assigned to NameServices 
+ Each NameService will have its own NameNode and SecondaryNode
+ NameSpace will have different BlockPullID and different DataNodes but Will have same cluster ID
#### HDFS Home Directory
+ sing up as HDFS `id username` - check if user exists
+ `hdfs dfs -mkdir /user/username` - Create Folder for user
+ `hdfs dfs -chown username:hdfs /user/username` - Give/Assign Permissions on userfolder
+ `hdfs dfs -chmod -R 700 /user/username` - Give Restrictions for folder to user *Only this user*
+ once you login as that user you can do all jobs on that user folder
+ so if you run `hdfs dfs -put file.txt` -> will put it into `user/username/file.txt`
#### Cluster Commission and Decommission
+ Begin Maitance First
+ Decomission DataNote (will reduce replication)
+ End Maitaince (will take back to comissioned)
+ You can also remove from cluster (it will delete agent as well)
#### Cluster Client Configuration
+ HDFS `->` Configurations
#### Cloudera Host Templates
+ Define what roles will be running with particular mission
#### Open LDAP UBUNTU
+ Lightweight Directory Access Protocol
+ Spinup ububntu 16.04
+ sudo apt-get update
+ sudo apt install slapd ldap-utils
+ systemctl status slapd *Check LDAP service status*
+ _We need to reconfigure settings_
+ sudo dpkg-reconfigure slapd
+ Change settings on appropriate
+ _Create Small App_ sudo vim /etc/ldap/ldap.conf
+ _Then You can search particular client_ `ldapsearch -x`
+ sudo apt install phpldapadmin *LDAP Interface*
+ `host/phpldapadmin`
+ `/etc/phpldapadmin/config.php`
+ check `config.php` - This settings will allow to create usergroups
#### Open LDAP CentOS
+ Loggin in one of the workers 
+ yum -y install nss-pam-ldapd
+ authconfig-tui (GUI Interface for UI)
+ authconfig --enableldap --enablemkhomedir --ldapserver=ip-172-31-86-60.ec2.internal:389 --ldapbasedn="dc=ddzmitry,dc=com" --update
+ authconfig-tui  (check ldap auth)
+ then we can look for user `id fln1` 
+ `su username` -> `cd` -> `pwd` -> "Will Take to home directory of user"
+ Now you can create any files and add them to HDFS
+ Repeat steps of `HDFS Home Directory` for new user 
+ _AND THIS WILL WORK_ `hdfs dfs -put test.txt /user/username/test.txt`
#### YARN 
+ OS That mages resources of all systems 
+ YARN gateway submits the job
+ `hadoop jar`
+ *EXAMPLES* `cd /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce`
+ ` hadoop jar hadoop-mapreduce-examples.jar pi 50 100`
+ `nohup hadoop jar hadoop-mapreduce-examples.jar pi 50 100` - will allow to run application in background
+ `sudo -u ddubarau hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar pi 10 100` submit job as user
+ in Cluster -> Static Service Pools -> You can assign how much memory will be allocated to Services
+ in YARN - > Configurations ->  Scheduler we can define scheduler class
+ Cluster -> Dynamic Resource Pool Configurations -> `User Limits`
+ If Changes were made you can revert them in YARN configuration -> `Revert changes` 
##### YARN SCHEDULER
+ FIFO Scheduler (Apache Hadoop)
+ Capacity Schedule (Hortonworks)
+ *Fair Share Schedulers (Cloudera Default)* -> Based off how much capacity in the cluster
+ YARN -> Configurations -> Scheduler
##### YARN Capacity Scheduler
+ YARN->Configurations->SCHEDULER
+ You can specify ResourceManager Default Group based of the group of users
+ Yarn-site.xml – For every container request
+ `Yarn.scheduler.minimum-allocation-mb - 1024`
+ `Yarn.scheduler.maximum-allocation-mb - 8192`
+ `Yarn.scheduler.minimum-allocation-vcores - 1`
+ `Yarn.scheduler.maximum-allocation-vcores – 32`
+ `yarn.scheduler.capacity.<queue-path>.maximum-capacity`
+ `yarn.scheduler.capacity.<queue-path>.capacity`
##### Dynamic Resource Pool Configuration
+ Cluster -> Dynamic Resource Pool Configuration -> Placement Rules
+ Create Percentage resources based of groups 
+ Can Allocate amount the jobs that be run by user within time
+ Can change Preemption (to facilitate ability of resources )
#### YARN Resource Manager High Availability 
+ Assign another host for process
+ Will add another Resource manager
+ Prvodide RM submit a job at the any point of the time
#### Zookeeper 
+ Coordinator Service Within a clustr
+ Has to be at least 3 systems on 
#### Hive 
+ Works with structured data only
+ Processes onto MR platform on top of the YARN
+ Shared by other components Like Impala
#### Work with files 
+ `sed 's/::/#/g' movies.dat > movies.t` *Replace :: with #*
#### Hive Shell and Beeline 
+ describe formated tablename
+ `LOAD DATA LOCAL INPATH 'occupations.t' OVERWRITE INTO TABLE occupations;`
+ `LOAD DATA INPATH 'ratings.t' OVERWRITE INTO TABLE ratings;` - Load data 
+ `hdfs dfs -put movies.t /user/hive/warehouse/movielens.db/movies/movie.t`  You can also load text data straight in table 
+ Then You can fire MR jobs
+ beeline uses connection to server where HIVE is running
+ `beeline` -> `!connect jdbc:hive2://host:10000`
#### Hive Point of Failure
+ RDBMS holding the metastore
+ Hivr Metaserver
+ HiveServer 2 
+ Zookeeper to coorinate high availability
#### Hive HA HiveServer 2 
+ Beeline > Login _Make sure all working_
+ Cloudera > Go To Hive and add more MetastoreServices (Which will increas High Avaliability by adding thrigt servers)
+ When Adding New Hosts Make sure that Driver is here 
+ Go to that server and `yum -y install mysql-connector-java`
+ Hive Metastore Default Group can be changed (Cluster>Hive>Configuration>Search Delegation)
+ Make Hive Metastore Higlu Avaliable by adding HMS to other hosts
+ To make Hive HA you have to have Zookeeper running on each one of them
+ *TO FIND SERVICES WITHIN ZOOKEEPER*
+ `beeline -u "jdbc:hive2://ip:2181, ip2:2181, ip3:2181; serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2"`
+ So if any of hiveservers will be down you can still support connection because of zookeeper will find another one
#### Hive WebHCat and HCatalog
+ Can be added to the host from Cluster>Hive>Instances
+ `curl -i http://host:50111/templeton/v1/status` - To check status of WebHCat Service
+ `hcat -e "create table groups123(name string,placeholder string, id int) row format delimited fields terminated by ':' stored as textfile"`
+ _hcat can also be used to describe the table and etc._ `hcat -e "desc groups123"`
+ Then you can simply can use hive or beeline to see data
#### Apache OOzie
+ Scheduler for Hadoop
+ Runs Tomcat server to schedule jobs 
+ Workflow -> Schedule -> Bundle
#### HUE  Hadoop USer Experience 
+ Comes in as Parcel from Cloudera
+ Need Horizontal Scalability
#### HUE Open LDAP
+ HUE > Configurations > authentication
+ Authentication Backend -> desktop.auth.backend.LdapBackend 
+ ldap_url -> ldap://<<hostname>>:389 
+ ldap_username_pattern -> uid=<username>,ou=users,dc=username,dc=com
+ search_bind_authentication-> Select ( True ) 
+ use_start_tls -> True
+ create_users_on_logon -> True 
+ base_dn -> dc=username,dc=com 
+ bind_dn -> cn=admin,dc=username,dc=com 
+ bind_password -> Provide as per LDAP configuration 
+ user_filter -> objectClass=* 
+ user_name_attr -> uid 
+ group_filter -> objectClass=posixGroup
+ _Once All of it is done_ User WILL Login with OPEN LDAP server
+ The firstr user who logged in is going to be an administrator
#### Extendend Controll HDFS
+ *Linux Permissions* Owner Group Other
+ Read -4 Write - 2 Execute - 1
+ `___________________` `r w x` `r - x` `r - x`
+ `___________________` `4+2+1` `4+0+1` `4+0+1`
+ `___________________`   `7`     `5`     `5`
+ `___________________`-chmod -R
#### Properties - ACL
+ dfs.permissions.enabled = true 
+ dfs.permissions.superusergroup = supergroup 
+ dfs.namenode.acls.enabled = true
+ *Scenario!* User creates a folder and  want to have one user have permission
+ hdfs dfs -chown user:productionGroup /folder
+ _LOGIN AS OWNER OF FOLDER_
+ *!!IMPORTANT!!*
+ hdfs dfs -setfacl -m user:username:rwx /folder
+ `That mean we allow only ONE USER from group to have read,weite and execute access to the folder`
+ `hdfs dfs -getfacl /folder` - to be able to see permissions on folder
#### ACL Options
+ -R: List ACLs recursively. 
+ -b: Revoke all permissions except the base ACLs for user, groups and others. 
+ -k: Remove the default ACL. 
+ -m: Add new permissions to the ACL. 
+ -x: Remove only the ACL specified. 
+ <acl_spec>: Comma-separated list of ACL permissions. 
+ --set: Completely replace the existing ACL. Previous ACL entries will no longer apply.
#### Order of evaluation of ACL Entries
+ User is file owner – Owner permission bits are enforced 
+ Named user ACL entry. 
+ Member of file’s group 
+ Named group in ACL entry (Union of previous entry) 
+ If none then other permission bits are enforced
#### Apache Sentry 
+ Enforces find grained authorization 
+ Role based authorization to data and metadata 
+ Integrates with Hive and HDFS 
+ Supports Impala and many more components 
+ Developed by Cloudera • Collection level, document level authorization could be provided