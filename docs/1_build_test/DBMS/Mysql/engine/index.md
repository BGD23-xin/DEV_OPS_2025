# INDEX

## 存储引擎

#### mysql 体系结构

- 1.客户端
- 2.mysql
  - 1.连接层(授权，认证)
  - 2.服务层(sql接口，解析器，查询优化器，缓存)
  - 3.引擎层(Memory,index,Storage management)
  - 4.存储层(系统文件，文件和日志)

#### 存储引擎

存储数据，建立索引，更新/查询数据等技术的实现方式，`表的类型`  

```SQL
SHOW CREATE TABLE 表名
--查看支持的引擎
SHOW ENGINES;

--指定引擎

CREATE TABLE 表名(
...
)ENGINE = 引擎；
```

`InnoDb`: 
- 事务，外键，行级锁；文件.ibd;每张表都有一个表空间，用于存储表结构，数据和索引；有个参数叫 innodb_file_per_table 默认开，表示每个表对应一个表空间`idb2sdi 文件`来查看结构
- 存储结构
  - 表空间 tableplace
  - 段 segment 
  - 区 extent 固定 1 M
  - 页 page 磁盘操作  固定 16 K
  - 行 row(trx id, roll pointer，col1 ...)
- 存储限制 64 T

`MySAM`
- 不支持 事务 ，外键 ，行锁，支持表锁， 访问快速
`Memory`
- 存放于内存，如果硬件问题或者断电，会导致文件丢失，只能用于临时表，支持哈希索引，

#### 引擎选择

`innodb`：默认  

`MyISAM`:以读取和插入操作为主，只有很少的更新操作和删除操作 , 对数据的完整性要求不高.

`Memory`:数据存在内存中，访问速度快，常用于临时表及缓存  


## 索引 ！！！ 重点

```bash
systemctl start mysqld

mysql -u root -p
# cat /var/log/mysqld.log 中会有初始密码记录

ALTER USER 'USER'@'主机' INDENTIFIED BY '新密码';

# 调密码校验等级 (不推荐)
# set global validate_password.policy = 0
# set global validate_password.length = 4

# 创建能远程登录的用户
# CREATE USER "'用户名'@'%' IDENTIFIED BY '密码'

```

#### 概述

定义：帮助mysql`高效`获取数据的`有序`的`数据结构`  

无索引会全表扫描

优点:  
- 提高查询效率，降低I/O成本
- 提高排序效率，降低排序成本，cpu的消耗

缺点(一般忽略):  
- 占用空间
- 降低增删改的效率

#### 索引的数据结构

- B+Tree 常见
- Hash 只有memory引擎支持，底层数据结构是哈希实现的，只有精确匹配索引列才有效，不支持范围查询 
- R-tree 只有MyISAM支持, 是MyISAM的特殊索引类型，用于地理空间数据类型
- full-text memory不支持，innodb是5.6之后支持，MyISAM支持 ,通过建立倒排索引来快速匹配文档，类似 ES

#### 索引结构

`B+tree 索引`

- 二叉树 
  - 如果顺序插入就会变成一个单向列表，查询性能大大降低
- B-tree 多路平衡查找树
  - 最大度数 max-degree，5阶，最多有5个指针和4个key
- B+ tree
  - 分叶子节点起到索引数据的作用
  - 叶子节点结构能构成一个单向列表,储存所有元素

Mysql的B+tree 索引  
增加了相邻叶子节点的链表指针，形成带有顺序的B+tree

`哈希索引`: 采用哈希算法，将键值换成hash值，映射到槽位上，但是数据一多，槽位就复用，也就是哈希冲突，可通过链表解决

只支持 等值比配（=,in）不支持范围查询(between,>,<...)   

Innodb 中有个自适应 hash功能，是在 B+tree中指定条件下自动构建的hash索引

为什么innodb选用 b+tree  
- 比二叉树 层级少，搜索效率高
- 比 b-tree好是因为，非叶子节点只存索引指针，增加查询效率
- hash只支持等值匹配

#### 索引分类

- 主键索引 primary, 默认自动创建，只能有一个
- 唯一索引 unique，可以有多个，避免表中有重复值
- 常规索引，可以多个，快速定位数据
- 全文索引，fulltext，多个，快速查找文中的关键字，不是比较索引中的值，用的少

innodb中的索引
- 聚集索引 必须有，且有一个；将数据和索引放到一块，索引结构的叶子节点保存数据
- 二级索引 可以有多个；数据和索引分开，索引结构的叶子结点关联对应的主键  

无论如何，聚集索引是存在的，若有主键，主键是聚集索引，若没有主键，unique 索引就会变为聚集索引  
若两者都没有，会自动生成一个rowid作为隐藏的聚集索引  

`回表查询`即二级索引找到对应的主键，之后再走一次聚集索引

#### 索引语法

- 创建 `CREATE [UNIQUE | FULLTEXT] INDEX 索引名 ON 表名(字段)`
- 查看 `SHOW INDEX FROM 表名`
- 删除 `DROP INDEX 索引名 ON 表`

#### SQL性能分析

- SQL的执行频率 `SHOW GLOBAL STATUS LIKE 'Com_______'` 7个下划线
- 慢查询日志 查看超过所有指定时间(默认10s)的查询
  - 查看是否开启`SHOW VARIABLES LIKE 'show_query_log';`
  - 在(/etc/my.cnf)中将 `slow_query_log = 1` 和 `long_query_time = 2`，开启和设置为2s
- profile 详情
  - 查看 `SELECT @@HAVE_PROFILING`, `SELEECT @@PROFILING`,开启 `SET PROFILING = 1`
  - 查看耗时 `SHOW PROFILES`, 具体耗时`SHOW PROFILES [cpu] FOR QUERY 查询id`
- explain 执行计划
  - `EXPLAIN/DESC SELECT ... `
  - 字段含义
    - id，操作表的顺序，相同 时，从上到下，id不同时(子查询)，值越大，越先执行
    - selct_type 表示select类型，常见是simple
    - `type` 性能高到低 null,system, CONST(主键或唯一索引), ER_REF, REF(非唯一index查询), RANGE,INDEX(用了索引),ALL(全表扫描)
    - `POSSIBLE_KEY` 可能用到的索引
    - `KEY` 实际用到的索引
    - `KEY_LEN` 跟字段中的长度有关
    - rows 预估的执行行数
    - filtered 返回的行数和读取的行数的百分比，越大表示性能越好
  

#### 索引使用

创建索引，避免全表扫描

- 最左前缀法则(联合索引时，即一个索引包含多个字段，查询顺序是从左到右，如果查询时没有最左列，索引就失效，如果跳过中间的列，那么部分失效，查询时位置变化没关系)
- 范围查询(右侧的列失效，尽量使用'>='避免使用 '>'这种)
- 索引列算操作（对索引列进行函数操作会导致索引失效）
- 字符串不加引号 (where 索引列 = "值"，这里的值需要加引号，不然索引失效)
- 模糊查询（尾部模糊匹配时，索引不会失效，但是头部模糊时，索引会失效）
- or连接条件 (or只有两侧都有索引时，索引才有效)
- 数据分布影响(如果全表扫描效率高于索引时，mysql会自动切全表扫描)

##### sql 提示

如果一个字段有多个索引时，告诉数据库用哪个索引
```SQL
USE INDEX --给建议
EXPLAIN SELECT * FORM 表名 USE INDEX(索引名) where ...
IGNORE INDEX -- 不要用索引
FORCE INDEX --必须用我的索引
```

##### 索引用途

- `覆盖索引`：尽量使用覆盖索引(查询使用了索引，返回的列已满足需求)，减少使用 select *,`USING INDEX CONDITION` 表示使用了索引但是要回表
- `前缀索引`：在字段为字符串时，作为索引时，若字符串很长，会使得索引很大，所以需要前缀索引
  - `CREATE INDEX 索引名 ON 表名(字段(前几个字))`
  - 先看选择性 COUNT(DISTINCT 字段)/COUNT(*)计算出可以前几个字符
- `单列索引`和`联合索引`的选择，多个字段查询时，建议使用联合索引

#### 索引的设计原则

- 数据量大(1E10以上)，查询频繁
- 对where, order by , group by 操作的字段建立索引
- 尽量选择区分度高的字段建立索引
- 对字符串字段建立索引时，建议使用前缀索引
- 尽量使用联合索引
- 要控制索引的数量，会影响增删改的效率
- 如果列不能存null，建议使用not null约束

