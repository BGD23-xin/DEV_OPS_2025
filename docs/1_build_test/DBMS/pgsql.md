# SQL

关系型结构


mysql vs pgsql vs oracle

数据库技术 
纯粹的关系性数据库 - 对象关系数据库（关系模型（表、行、列）和面向对象模型（对象、类、继承））


数据类型 

支持数字、字符、日期和时间、空间和 JSON 数据类型   -- 支持所有 MySQL 数据类型，以及几何、枚举、网络地址、数组、范围、XML、hstore 和组合

ACID 合规性

MySQL 仅针对 InnoDB 和 NDB 集群存储引擎具有 ACID 兼容性 -- PostgreSQL 始终符合 ACID。 

NDB
https://www.cnblogs.com/xiaozengzeng/p/12111691.html


索引

MySQL 支持 B 树和 R 树索引 -- PostgreSQL 支持多种索引类型，例如表达式索引、部分索引和带有树的哈希索引

性能
MySQL 提高了高频读取操作的性能 -- PostgreSQL 提高了高频写入操作的性能。