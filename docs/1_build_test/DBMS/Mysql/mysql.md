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

