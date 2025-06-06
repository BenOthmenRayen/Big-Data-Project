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
3-Below is the configuration for the "hdfs-site.xml" file, which specifies settings related to the Hadoop Distributed File System (HDFS), such as replication and storage directories:
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
4-Below is the configuration for the "mapred-site.xml" file, which defines the MapReduce framework settings, including the execution engine used by Hadoop for job processing:
```
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>

  <property>
    <name>mapreduce.jobhistory.address</name>
    <value>historyserver:10020</value>
  </property>

  <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>historyserver:19888</value>
  </property>
</configuration>
```
5-Below is the configuration for the "yarn-site.xml" file, which sets parameters for the YARN resource manager and node managers, enabling cluster resource management and job scheduling:  
```
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>

  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>resourcemanager</value>
  </property>

  <property>
    <name>yarn.scheduler.minimum-allocation-mb</name>
    <value>256</value>
  </property>

  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>4096</value>
  </property>

  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>4096</value>
  </property>

 
  <property>
    <name>yarn.app.mapreduce.am.resource.mb</name>
    <value>1024</value>
  </property>

  <property>
    <name>mapreduce.map.memory.mb</name>
    <value>1024</value>
  </property>

  <property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>1024</value>
  </property>

  <property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
  </property>
</configuration>
```
6-Below is the content of the "workers.txt" file, which lists all the worker (slave) nodes that will participate in the Hadoop cluster for distributed data processing:  
```
datanode
datanode2
datanode3
```
7-Change directory where the docker-compose file exists and you can now start your container:
```
docker-compose up -d
```
8-Browse your http://localhost:9870 and check your cluster :
<img src="screenshots/3 datanodes.png" width="100%" />
9-We can also test the MapReduce functionality using a sample data file named purchases.txt, along with two Python scripts: mapper.py and reducer.py:
  9.1-The mapper.py file is responsible for reading each line of the dataset and emitting key- 
   value pairs:
   ```
    import sys

    for line in sys.stdin:
       words = line.strip().split()
       for word in words:
         print(f"{word}\t1")
   ```
  9.2-The reducer.py file receives the sorted output from the mapper and counts the total 
    number of occurrences for each unique word:  
  ```
import sys

      current_word = None
      current_count = 0

      for line in sys.stdin:
          word, count = line.strip().split("\t")
          count = int(count)

          if word == current_word:
              current_count += count
          else:
              if current_word:
                   print(f"{current_word}\t{current_count}")
              current_word = word
              current_count = count

      if current_word:
          print(f"{current_word}\t{current_count}")
  ```
10-we create a directory named /input in the Hadoop Distributed File System (HDFS), where we will store the input files for processing:   
<img src="screenshots/creation de fichier input .png" width="100%" />   
11-Copy the purchases.txt file from the local file system to HDFS:  
<img src="screenshots/coping the data in the folder input inthe hdfs.png" width="100%" />    
12-To do this, access the NameNode container or machine, then run the following commands:
<img src="screenshots/commande to run mapreduce job.png" width="100%" />
13-output:
<p>  
<img src="screenshots/output1.png" width="30%" height="460" /> 
<img src="screenshots/output2.png" width="30%" height="460" /> 
<img src="screenshots/output3.png" width="30%" height="460" /> 
</p>   

## Part 2 - Apache Spark using Docker : PySpark
**We will setup a 3-node spark cluster**
1- We use docker-compose.yml to deploy the Spark cluster services via Docker, enabling an easy-to-manage and scalable Spark environment:   
 ```
version: '3.3'

services:
  spark-master:
    image: bitnami/spark:latest
    container_name: spark-master
    command: bin/spark-class org.apache.spark.deploy.master.Master
    ports:
    - 9090:8080
    - 7077:7077 
  spark-worker-1:
    image: bitnami/spark:latest
    container_name: spark-worker1
    command: bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    depends_on:
      - spark-master
    environment:
      SPARK_MODE: worker
      SPARK_WORKER_CORES: 2
      SPARK_WORKER_MEMORY: 2g
      SPARK_MASTER_URL: spark://spark-master:7077
  spark-worker-2:
    image: bitnami/spark:latest
    container_name: spark-worker2
    command: bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    depends_on:
      - spark-master
    environment:
      SPARK_MODE: worker
      SPARK_WORKER_CORES: 2
      SPARK_WORKER_MEMORY: 2g
      SPARK_MASTER_URL: spark://spark-master:7077
 ```
2-The wordcount.py file contains a Spark application script that reads a text file, processes it using Spark's RDD transformations, and computes the frequency of each word in the dataset:
 ```
from pyspark import SparkContext

sc = SparkContext(appName="WordCount")
rdd = sc.textFile("file:///opt/bitnami/spark/purchases.txt")
word_counts = rdd.flatMap(lambda line: line.split()) \
                 .map(lambda word: (word, 1)) \
                 .reduceByKey(lambda a, b: a + b)

for word, count in word_counts.collect():
    print(f"{word}: {count}")

sc.stop()
 ```
3-Type this command to copy the python script containinng pyspark code :
```bash
docker cp sample_pyspark.py spark-master:/opt/bitnami/spark/sample_pyspark.py
```
4-run the pyspark job :

<img src="screenshots/excecuttin wordcount.py.png" width="100%" /> 

5-output:
<p>  
<img src="screenshots/output1.png" width="30%" height="460" /> 
<img src="screenshots/output2.png" width="30%" height="460" /> 
<img src="screenshots/output3.png" width="30%" height="460" /> 
</p>   









 

