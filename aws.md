#### Install mySQL on cloud
+ yum -y update _(update all packages)_
+ yum -y install mysql-server mysql-connector-java _(install connector and install server)_
+ *to check status of mySql instance* _service mysqld status_
+ *to start service of mySQL* _service mysql start_
+ *to start service every time when starting up the system* chkconfig mysqld on 
+ `/usr/bin/mysql_secure_installation` run secure installation
+ *login from localhost* mysql -u root -h localhost -p
+ create user 'temp'@'%' identified by 'password123';
+ grant all privileges on *.* to 'temp'@'%' with option;
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
+ vim /etc/selinux/config
+ _SET_ SELINUX=disabled
+ echo never > /sys/kernel/mm/transparent_hugepage/enabled
+ `echo "echo never > /sys/kernel/mm/transparent_hugepage/enabled" >> /etc/rc.local`
+  /sbin/shutdown -r now `restart`
+ Open Ports for current IP address
+ http://ipaddress:7180/
+ Spin up 3 more server boxes from AMIs and add them to hosts in Cloudera management
+ Make sure to set properly Inbound and Outbound traffic
+ use .pem file to provide all root access to nodes 

