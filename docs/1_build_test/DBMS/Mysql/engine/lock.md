# 锁 (LOCK)

三个方面：
- 使用方式
- 加锁范围
- 思想层面

##  使用方式

### 共享锁(读锁)
当对象被锁定时，允许其他事物 可读但不能写入

```sql
--加锁方式

select ... lock in share mode;

select ... for share;
```
### 排他锁(写锁或者独占锁)

如果锁表就是不能对整张表增删改，如果锁行就是不能对锁定行增删改


```sql
select ... for update;
```

## 加锁范围

### 全局锁
对数据库加锁,只可读

```sql
--加锁
flush tables with read lock
--解锁
unlock tables

```

### 表级锁

表锁就是对整张表加锁，包含读锁和写锁
```sql
# 给表加写锁
lock tables tablename write;

# 给表加读锁
lock tables tablename read;

# 释放锁
unlock tables;
```


### 行级锁

行锁是针对数据表中行记录的锁
在innodb中

- 1.Record Lock： 记录锁，是在索引记录上加锁；
- 2.Gap Lock：间隙锁，锁定一个范围，但不包含记录；
- 3.Next-key Lock：Gap Lock + Record Lock，锁定一个范围(Gap Lock实现)，并且锁定记录本身(Record Lock实现)；
- 4.插入意向锁：针对 insert 操作产生的意向锁；


## 思想层面看

悲观锁，可以理解成：在对任意记录进行修改前，先尝试为该记录加上排他锁(exclusive locking)，采用的是先获取锁再操作数据的策略，可能会产生死锁；
乐观锁，是相对悲观锁而言，一般不会利用数据库的锁机制，而是采用类似版本号比较之类的操作，因此乐观锁不会产生死锁的问题；

死锁和死锁检测
当并发系统中不同线程出现循环资源依赖，涉及的线程都在等待别的线程释放资源时，就会导致这几个线程都进入无限等待的状态，称为死锁。可以通过下面的指令查看死锁

`show engine innodb status\G`