# Mysql

## 基本概念

- 数据库: 数据存储的仓库，数据是有组织的进行存储
- 数据库管理系统(软件):操纵和管理数据库的大型软件
- SQL: 操作关系型数据库的编程语言，定义了一套操作关系型数据库统一标准

`mysql` 本质上是数据库管理系统.  

数据库类型模型:  
    - 关系型数据库(RDBMS): 建立在关系模型基础上，由多张相互连接的二维表(类excel)组成的数据库  
    - 非关系型数据库  

  
关系型数据库，优点:  
- 1.使用表存储数据，格式统一，便于维护  
- 2.使用 SQL 操作，标准统一，使用方便  

数据模型:  
    1.客户端连接 mysql的DBMS  
    2.mysql的DBMS 创建数据库(SQL 操作)  
    3.数据库创建表(SQL 操作)  

启动:  

`net start mysql80`,`net stop mysql80`  

客户端连接
`mysql [-h 172.0.0.1] [-p 3306] -u root -p`


### SQL 

通用语法  
1.单行，多行书写，以';'结尾  
2.使用空格和缩进来增强语句的可读  
3.不区分大小写，关键字建议用大写  
4.注释， 单行用'--',多行用'/*'  

分类：  
1.DDL：数据库定义语言，定义 数据库，表，字段  
2.DML：数据操作语言，对标进行增删改操作  
3.DQL: 数据查询语言，查询记录  
4.DCL: 数据控制语言，创建用户，控制数据表的权限  

`DDL`:  

`数据库`： 
- 查询: 所有 `SHOW DATABASES;` ,当前 `SELECT DATABASE();`
- 创建: `CREATE DATABASE [IF NOT EXIST] 数据库名 [DEFAULT CHARSET 字符集] [COLLATE 排序规则];`  
- 删除: `DROP DATABASE [IF EXISTS] 数据库名;`  
- 使用: `USE 数据库名;`  

`表`:  

- 创建 

```sql
CREATE TABLE 表名 (
    字段1 字段类型 [COMMENT 注释]
)[COMMENT 注释]；
--[..] 为可选参数
```
- 修改
    - 添加字段 `ALTER TABLE 表名 ADD 字段名 类型 [COMMENT] [约束]`
    - 修改数据类型 `ALTER TABLE 表名 MODIFY 字段名 新数据类型`
    - 修改字段名和类型 `ALTER TABLE 表名 CHANGE 旧字段名 新名字 类型 [COMMENT] [约束]`
    - 删除 `ALTER TABLE 表名 DROP 字段名`
    - 修改表名 `ALTER TABLE 表名 RENAME TO 新表名`
    - 删除表 `DROP TABLE [IF EXITS] 表名`
    - 删除后重新创建 `TRUNCATE TABLE 表名`

`DML`:  
- 查询: 所有 `SHOW TABLES`， 结构 `DESC 表名`，指定建表的语句 `SHOW CREATE TABLE 表名`  
- 添加数据
  - 给指定字段添加数据 `INSERT INTO 表名 （字段1，字段2...）VALUES(值1，值2)`
  - 给全部字段添加 `INSERT INTO 表名 VALUES(值1，值2)`
  - 批量添加 `INSERT INTO 表名 （字段1，字段2...）VALUES(值1，值2...)(值1，值2...)...` , `INSERT INTO 表名 VALUES(值1，值2...)(值1，值2...)...`
- 修改数据 `UPDATE 表名 SET 字段1 = 新字段2，字段2 = 新字段2 [where 条件]`
- 删除数据
  - `DELETE FROM 表名 [WHERE]`
  - `UPDATE 表名 SET 字段1 = None`

`DQL`:
```SQL

SELECT DISTINCT 字段 as 新名字  --顺序 5
FROM 表名 --1
WHERE 条件 -- 2
GROUP BY 分组字段列表 --3
HAVING 分组字段列表（分组后过滤，可以使用聚合函数）--4
ORDER BY 字段 --(ASC DESC) --6
LIMIT --起始索引（页码-1）* 每页展示数，记录查询数 --7

--聚合函数：COUNT,MAX, MIN,AVG,SUM ,列为整体进行纵向计算
```
`DCL`

- 用户管理
  - 查询用户 `USE MYSQL; SELECT * FORM USER` --需要主机名和用户才能定位
  - 创建用户 `CREATE USER "'用户名'@'主机名'" IDENTIFIED BY '密码'` --若任意主机 将 '主机名' 改成 '%'
  - 修改用户密码 `ALTER USER "'用户名'@'主机名'" IDENTIFIED WITH mysql_native_password by '密码' `
  - 删除用户 `DROP USER '用户名'@'主机名'`
- 权限控制
  - 查询权限 `SHOW GRANTS FOR '用户名'@'主机名'`
  - 授予权限 `GRANT 权限列表 ON 数据库.表名 TO '用户名'@'主机名'` 多个权限需要用逗号分开
  - 撤销权限 `REVOKE 权限列表 ON 数据库.表名 FROM '用户名'@'主机名'`


#### 数据类型

- 数值类型
- 字符串类型
- 日期类型

##### 数值类型

- TINYINT ,大小 1 Byte , 范围 -128_127 ，无符号 UNSIGNED 0_255
- SMALLINT,2 bytes, 2**16
- MEDIUMINT,3 bytes, 2**24
- INT,4 bytes, 2**32
- BIGINT,8 bytes,
- FLOAT, 4 bytes
- DOUBLE,8 bytes
- DECIMAL,依赖于M精度和D标度，小数值

##### 字符串类型

- CHAR, 0-255 bytes, 定长
- VARCHR,0-65535 bytes,变长
- *BLOB,二进制数据
- *TEXT,文本数据

比较:  
CHAR(10),最大10个字节，但是少于10字节时，会补到10字节，性能高
VARCHAR(10)，最大10字节，少于10字字节时，就是储存字符串大小，性能比CHAR 会差，因为会因内容计算空间  

示例: 用户名，varchar，性别，char


##### 日期时间类型

- DATE, 3 bytes, 1000-01-01_9999-12-31, "YYYY-MM-DD"
- TIME, 3 bytes,-838.59.59_838.59.59, "HH:MM:SS"
- YERA, 1 byte,1901_2155
- DATETIME, 8 bytes,
- TIMESTAMP, 4 bytes,1970-01-01_2038-01-19

```sql
#示例

create table emp(
    id int,
    workid varchar(10),
    name varchar(10),
    gender char(1),
    age tinyint unsigned,
    id_card char(18),
    entry_date date
);
```
#### 函数

##### 字符串函数

- CONCAT(S1,S2...Sn) 字符串拼接
- LOW(str)
- UPPER(str)
- LPAD(str,n,pad) 左填充，用字符串pad 对str左边进行填充，达到n个字符串长度
- RPAD(str,n,pad)
- TRIM(str) 去除字符串左右的空格
- SUBSTRING(str,start,len) 截取字符串长度

##### 数值函数

- CEIL(x) 向上取整
- FLOOR(x) 向下取整
- MOD(X,Y) 返回 x/y的模
- RAND() 返回0-1的随机数
- ROUND(X,Y) x保留y位小数

```SQL
SELECT lpad(ROUND(RAND()*1000000,0),6,'0') --生成6位数密码
```

##### 日期函数

- CURDATE()
- CURTIME()
- NOW()
- YEAR(date)
- MONTH(date)
- DAY(date)
- DATE_ADD(date,INTERVAL N YEAR) 增加 N 年，
- DATEDIFF(date1, date2)

##### 流程函数

- IF(VALUE,T,F)
- IFNULL(value1，value2)
- CASE WHEN [val1] THEN [res1].. ELSE [default] END
- CASE [EXPER] WHEN [val1] THEN [res1].. ELSE [default] END

#### 约束

作用于字段的规则，限制该字段的数据。 用于保证数据库中的数据的正确,有效性和完整性

分类：  
- 非空 NOT NULL
- 唯一 UNIQUE
- 主键 PRIMARY KEY
- 默认 DEFAULT
- 检查 CHECK (8.0.16版本之后)
- 外键 FOREIGN KEY 用于两张表之间建立连接，保证一致性和完整性

```SQL
ID INT PRIMARY KEY  AUTO_INCREMENT,
NAME VARCHAR(10) NOT NULL UNIQUE,
AGE INT CHECK(AGE>0 && AGE<120),
STATUS CHAR(1) DEFAULT "1",
GENDER CHAR(1)

[CONSTRAINT] [外键名称] FOREIGN KEY (外键字段) REFERENCES 主表(主表列名)
```

##### 外键约束

`ALTER TABEL 表名 ADD CONSTRAINT 外键名称 foreign key (字段) references 表名(字段)`  

删除外键: `ALTER TABEL 表名 DROP foreign key 字段`  

- NO ACTION 在有外键情况下，父表不能更新或删除
- RESTRICT 在有外键情况下，父表不能更新或删除
- CASCADE 在有外键情况下，父表删除或更新，子表也删除对应的
- SET NULL  在有外键情况下，父表删除或更新，子表对应的会变成null
- SET DEFUALT 父表更新，子表对应的会变成一个默认（innodb不支持）

`ALTER TABEL 表名 ADD CONSTRAINT 外键名称 foreign key (字段) references 表名(字段) ON UNDATE CASCADE ON DELETE CASCADE`  

#### 多表查询

- 一对多 在多的地方建立外键
- 多对多 ，建立中间表，存储两表关系
- 一对一，子表字段要设置unique，父表字段是主键，经常做表的拆分

要注意笛卡尔积，会生成两个的集合所有情况


```SQL
--内连接
SELECT * FROM 表1 [inner]join 表2 on 

--外连接
SELECT * FROM 表1 LEFT[OUTER]join 表2 on 
SELECT * FROM 表1 RIGHT[OUTER]join 表2 on 

--自连接

SELECT * FROM 表1 as a left join 表1 as b  on where 


-- 联合查询
--需要保证列数和字段类型一致

SELECT * FROM 表1

UNION [ALL] --不加all是去重 

SELECT * FROM 表2

--子查询，嵌套查询


```
### 事务

```SQL
--查看、设置事务提交
-- SELECT @@AUTOCOMMIT 自动提交 ;
SET @@AUTOCOMMIT = 0 --手动提交;

--提交

COMMIT;

-- 回滚，业务失败，没提交之前
rollback；

/*
开启事务

START TRANSACTION / BEGIN;

COMMIT;

rollback；
*/
```

#### 特性  
- A(atomicity) 原子性， 不可分割的最小操作单元
- C(consistency) 一致性，完成后，数据一致状态
- I(isolation) 隔离性，隔离机制
- D(Durability) 持久性,提交或回滚，数据的改变是永久的

#### 并发事务导致的问题

事务A,B同时操作引发的问题：
- 脏读 A读到B没交的数据
- 不可重复读 A先后读取一条记录但是返回的值不一样，中间B的操作将值给改了
- 幻读 读的时候没有数据，但是插入时有数据,B的插入操作将插入的操作给顶了

#### 隔离级别

- 读未提交 有三个并发问题
- 读已提交 有不可重复读和幻读的问题
- 可重复读(默认) 有幻读的问题 
- 串行化(serializable) 都解决但是 并发性能腰斩

```SQL
--查看
SELECT @@TRANSACTION_ISOLATION;

--设置
SET [SESSION | GLOBAL] TRANSACTION ISOLATION LEVEL{ READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ |SERIALIZABLE}

```

## 进阶

### 存储引擎

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


### 索引 ！！！ 重点

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


### 视图/存储过程/触发器

#### 视图
虚拟存在的表，只保存sql的逻辑
- 创建 `CREATE [OR REPLACE] VIEW 视图名称 AS SELECT 语句`
- 查询 `SHOW CREATE VIEW 视图名称` ; ` SELECT ...FROM 视图名称`
- 修改 `CREATE [OR REPLACE] VIEW 视图名称 AS SELECT 语句`；`ALTER VIEW 视图名称 AS SELECT 语句`
- 删除 `DROP VIEW  [IF EXISTS] 视图名称 `

对视图进行 `insert`操作时，是对基表操作，如果视图有限定条件，有时添加的值是看不到的，需要在视图创建后添加 `WITH CASCADED/LOCAL CHECK OPTION`,做添加检查

##### 视图检查

`WITH CASCADED/LOCAL CHECK OPTION`在增删改的时候会检查where的条件  
`LOCAL` 会去递归的去找 有没有 CHECK OPTION

视图的行和基表的行需一一对应。

- 1.select 中使用了聚合函数
- 2.distinct
- 3.group by
- 4.having
- 5.union / union all

作用

- 操作简单，将复杂操作丢给视图
- 安全，敏感数据不可见
- 数据独立 帮用户屏蔽真实表带来的影响

#### 存储过程

将sql语句进行封装进数据库

特点
- 封装，复用
- 可接收参数
- 减少网络交互，提升效率
```SQL
CREATE PRECEDURE 名称([参数])

BEGIN

--sql语句
END；

--调用
call 名称();

-- 查看
SELECT * FROM INFORMATION_SECHEMA.ROUTINES WHERE ROUTINE_SCHEMA = "表名"；

-- SHOW CREATE PROCEDURE 名称;

--删除

DROP PROCEDURE IF EXISTS 名称

delimiter 可定义结束符号
```

##### 变量

- session 在当前回话内有效
- global 全局有效

```SQL

--查看
SHOW [SEESION|GLOBAL] VARIABLES;
SHOW [SEESION|GLOBAL] VARIABLES LIKE "";
SHOW @@[SEESION|GLOBAL] 系统变量名;

--设置

SET [SEESION|GLOBAL] 系统变量名 = 值;

-- SET @@[SEESION|GLOBAL] 系统变量名 = 值;
```

`用户自定义变量` "@变量名"

```SQL
--赋值

SET @VAR_NAME = VALUE [,@VAR_NAME = VALUE]
SET @VAR_NAME := VALUE [,@VAR_NAME := VALUE]

SELECT @VAR_NAME := VALUE [,@VAR_NAME := VALUE]
SELECT 字段名 INTO @VAR_NAME FROM 表名


-- 使用
SELECT @VAR_NAME

```
`局部变量` 需要`DECLARE 变量名 变量类型 [DEFAULT ...]`,在begin 和 end 内生效

`IF`

```SQL
IF 条件1 THEN

ELSEIF 条件2 THEN

ELSE

END IF;
```
`参数`:
- IN 
- OUT
- INOUT

### 锁

### InnoDB 引擎

### Mysql 管理

