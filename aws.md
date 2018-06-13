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
