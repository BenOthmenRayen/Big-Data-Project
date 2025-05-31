# Big-Data-Project
This project leverages Hadoop and Apache Spark to perform large-scale data analysis on the purchasestxt dataset. It demonstrates the use of distributed computing tools to process, clean, and analyze purchase data efficiently
## Part 1 - Installing a Hadoop cluster using Docker
**Before starting make sure that docker and docker-compose are installed in your system**
```bash
docker version
docker-compose version
```
**In this section, we set up a 4-node Hadoop cluster consisting of 1 master node and 3 slave nodes. This setup enables distributed storage and processing of large datasets using HDFS and MapReduce. Each node is configured manually to ensure clear understanding of the underlying components and processes.**
```
version: "X"

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
    environment:
      - CLUSTER_NAME=test
    env_file:
      - ./hadoop.env

```
