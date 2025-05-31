# Big-Data-Project
This project leverages Hadoop and Apache Spark to perform large-scale data analysis on the purchasestxt dataset. It demonstrates the use of distributed computing tools to process, clean, and analyze purchase data efficiently
## Part 1 - Installing a Hadoop cluster using Docker
**Before starting make sure that docker and docker-compose are installed in your system**
```bash
docker version
docker-compose version
```
**In this section, we set up a 4-node Hadoop cluster consisting of 1 master node and 3 slave nodes. This setup enables distributed storage and processing of large datasets using HDFS and MapReduce. Each node is configured manually to ensure clear understanding of the underlying components and processes.**  
1- Below is the content of the "docker-compose.yml" file, which defines and manages the services required to deploy the Hadoop cluster using Docker containers:
```
version: "3"

services:
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    restart: always
    ports:
      - 9870:9870
      - 9000:9000
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
      - ./config/workers:/hadoop/etc/hadoop/workers
    environment:
      - CLUSTER_NAME=test
    env_file:
      - ./hadoop.env

  submit:
    build:
      context: ./submit
    container_name: submit
    restart: unless-stopped
    volumes:
      - ./submit:/app
    depends_on:
      - namenode
      - resourcemanager
    working_dir: /app
    command: tail -f /dev/null
    env_file:
      - ./hadoop.env

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode
    restart: always
    volumes:
      - hadoop_datanode:/hadoop/dfs/data
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
    env_file:
      - ./hadoop.env

  datanode2:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode2
    restart: always
    volumes:
      - hadoop_datanode2:/hadoop/dfs/data
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
    env_file:
      - ./hadoop.env

  datanode3:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode3
    restart: always
    volumes:
      - hadoop_datanode3:/hadoop/dfs/data
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
    env_file:
      - ./hadoop.env

  resourcemanager:
    image: bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8
    container_name: resourcemanager
    restart: always
    environment:
      SERVICE_PRECONDITION: "namenode:9000 datanode:9864"
    env_file:
      - ./hadoop.env

  nodemanager:
    image: bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8
    container_name: nodemanager
    restart: always
    environment:
      SERVICE_PRECONDITION: "namenode:9000 datanode:9864 resourcemanager:8088"
    env_file:
      - ./hadoop.env

  historyserver:
    image: bde2020/hadoop-historyserver:2.0.0-hadoop3.2.1-java8
    container_name: historyserver
    restart: always
    environment:
      SERVICE_PRECONDITION: "namenode:9000 datanode:9864 resourcemanager:8088"
    volumes:
      - hadoop_historyserver:/hadoop/yarn/timeline
    env_file:
      - ./hadoop.env

volumes:
  hadoop_namenode:
  hadoop_datanode:
  hadoop_datanode2:
  hadoop_datanode3:
  hadoop_historyserver:

```
2-Below is the configuration for the "core-site.xml" file, which defines essential settings for Hadoop's core components, including the default filesystem and NameNode address:  
```
<configuration>
    <!-- NameNode URI -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://namenode:9000</value>
    </property>
    
    <!-- HTTP static user -->
    <property>
        <name>hadoop.http.staticuser.user</name>
        <value>root</value>
    </property>
    
    <!-- Compression codecs -->
    <property>
        <name>io.compression.codecs</name>
        <value>org.apache.hadoop.io.compress.SnappyCodec</value>
    </property>
    
    <!-- Temporary directory -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/tmp/hadoop-${user.name}</value>
    </property>
</configuration>
```
3-Below is the configuration for the hdfs-site.xml file, which specifies settings related to the Hadoop Distributed File System (HDFS), such as replication and storage directories:
```
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- Where NameNode stores metadata -->
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/hadoop/hdfs/namenode</value>
    </property>

    <!-- Where DataNodes store blocks -->
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/hadoop/hdfs/datanode</value>
    </property>

    <!-- Replication factor (3 for your 3 DataNodes) -->
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>

    <!-- Disable permissions for development -->
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
    </property>
</configuration>
```


 

