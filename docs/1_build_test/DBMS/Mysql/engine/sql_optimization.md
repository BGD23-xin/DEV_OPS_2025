
### SQL 优化

#### 插入数据优化

`INSERT INTO`
- 批量插入(500-1000)
- 手动事务提交
- 主键顺序插入

`LAOD`大批量插入，主键顺序插入要高于乱序插入
```bash

mysql --local-infile -u root -p
set global local_infile=1
### ",""\n"为列和行分隔符
load data local infile 'path' into table "table_name" fields terminated by "," terminated by "\n"

```

#### 主键优化

`数据的组织方式`：innodb中表数据是根据主键进行顺序存放的，这种方式叫索引组织表  
`页分裂`，页可以为空，也可以填充一半，也可以是100%，乱序插入时发生的  
`页合并`，删除一行时，记录并没有被物理删除，记录的标记(flaged)被删除，有个参数叫`MERGE_THREADHOLD`默认50% 合并

##### 设计原则

- 尽量降低主键的长度
- 尽量顺序插入，选取 auto_increment
- 尽量不要使用uuid或其他自然主键
- 尽量避免对主键的修改 

#### order by 优化

`USING FIRESORT` 所有不是通过索引直接返回排序结果的排序，若不可避免，可以上调 `sort_buffer_size`(默认256k)，查看`SHOW variables like'sort_buffer_size'`
`USING INDEX` 通过有序索引顺序扫描直接返回有序数据，不需要额外排序

#### LIMIT by 优化

在大数量时， 分页操作越往后越低
通过覆盖索引加子查询 来优化


#### count 优化
`count(*)`在innodb是一行一行读出来
优化思路：自己计数
`count(*)`：不取值，mysql做了优化，直接累加，  
`count(主键)`：取值再计数  
`count(字段)`：统计的是不为null的行，有not null就直接统计不判断是否为null  
`count(1)`：每条记录放1再累加  

#### update 优化

行锁是针对索引字段，如果非索引字段或者索引失效时，会有表锁
