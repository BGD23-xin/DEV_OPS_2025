

## 视图/存储过程/触发器

### 视图
虚拟存在的表，只保存sql的逻辑
- 创建 `CREATE [OR REPLACE] VIEW 视图名称 AS SELECT 语句`
- 查询 `SHOW CREATE VIEW 视图名称` ; ` SELECT ...FROM 视图名称`
- 修改 `CREATE [OR REPLACE] VIEW 视图名称 AS SELECT 语句`；`ALTER VIEW 视图名称 AS SELECT 语句`
- 删除 `DROP VIEW  [IF EXISTS] 视图名称 `

对视图进行 `insert`操作时，是对基表操作，如果视图有限定条件，有时添加的值是看不到的，需要在视图创建后添加 `WITH CASCADED/LOCAL CHECK OPTION`,做添加检查

#### 视图检查

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

### 存储过程

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

#### 变量

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


### 触发器