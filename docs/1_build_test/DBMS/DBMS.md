# 数据库管理系统
## ranking
https://db-engines.com/en/ranking
https://www.cnblogs.com/xrq730/p/11039384.html
https://www.ibm.com/cn-zh/think/topics/nosql-databases


数据库管理系统的本质是对数据的存储和查询，管理和控制

宏观分类是

关系型数据库
常见的有
1.oracle
2.mysql
3.pgsql




非关系型数据库(Not only sql)

键值数据库：redis

列簇数据库 Hbase, cassandra

(https://blog.csdn.net/gengzhikui1992/article/details/104920742)
解决海量数据下分析慢的问题
在关系型数据库中，一行可以看作是一个整体，所以增删改很方便

但是对于查询需要

文档数据库：mongodb
图形数据库：neo4j


结构化数据

非结构化数据

半结构化数据


根据互联网不同时期的需求，得到两种结构
区别是
数据的存储和组织方式

关系型数据库
数据的存储形式以二维表存储，查询语言是结构化查询语言(sql)

非关系型数据库 Nosql(not only sql)



键值存储 redis

速度快，存储数据量大，支持高并发和方便扩展

sql 

为企业级应用设计的，核心需求是：数据一致性、不重复、不出错，ACID


nosql，海量数据，高并发，高可用与可扩展性

键值 redis
列式存储 cassandra，hbase
文档 MongoDB
图形 Neo4J
搜索引擎数据库 Elasticsearch
时序数据库 InfluxDB
向量数据库 Pinecone

架构/系分-数据库系统-NoSQL
