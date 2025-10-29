# python 

https://developer.aliyun.com/article/1003286

## 基础知识点补缺

### 变量

`构成`：标识，类型，值 , id(var),type(var),var . 注： 值改了，类型和标识也会变化

对于 list，dict，set 通过代买来修改值是不改变标识的

主要用途：
    测试引用对象是否改变
    内存优化分析：对象是否复用或者缓存 (数字大时不会缓存)
    性能优化：避免对象复用
    实现对象池，用id区分唯一实例

一般检测是 用  `is/is not`

`进制`
```python

# 二进制  0b前缀
# 八进制  0o前缀
#十六进制 0x前缀
```


`转义字符`
```python
print("\'") # output: '

print("\\") # output: \

print('\"') # output: "

print('hello\rhelloworld')   # 将hello覆盖

print('hello\nworld') # 换行

print('helloo\bworld') # =>hello world

print('hello\tworld\t你好\t好') # => hello	world	你好	好

print(r'hello \n word') # => hello \n word

```

### 运算

```python
abs(x)  # => |x|
divmod(x, y) # => (x // y, x % y)
pow(x, y) ,pow(x, y, z) # => x ** y, x ** y % z


'''
位运算符:

位与 & 对应位数都是1，结果才为1，否则为0

位或 | 对应位数都是0，结果才为0

# 下面是在二进制下整体移动位置 a << n  = a * 2 ** n
a >> n  = a / 2 ** n
左移运算符   <<  高位溢出，低位补0
右移运算符   >>  低位溢出，高位补0 
'''

# 运算符的优先级

# 指数运算运算（最高优先级）      **
# 算数运算       *       /       //     %       +     -
# 位运算         <<      >>      &     |
# 比较运算符      >     <       >=      <=
# 等于运算符       ==      !=
# 身份运算符       is      is not
# 成员运算符       in      not in
# 逻辑运算符       and     or     not

```

`位图运算`
```python
# 这个算法主要是用于判断是否出现，重复次数,重复值有哪些

"""
对于一个大的数据集，比如 1e10,如果全部扫描，占用的内存会很大，但是我们把这些出现的数字转化成 位置标记 就能快速计算
"""
#例子
import numpy as np
# 如果遍历，占用内存是 64 * 1e10 大约 80 GB ,将数字变成对应的位置编号，就是/64的大小
N = int(1e10)
bitmap_per_block  = 64  #cpu能力，64位还是32位

# 这样就会分成多少个标记位置的数,这里是向上取整，保证所有的数都有区间
n_interval = (N + bitmap_per_block - 1) // bitmap_per_block

# 有n_interval区间，每个区间的位数代表 0-63，64-127
bitmap = np.zeros(n_interval, dtype=np.uint64)
# bitmap = [0] * int(n_interval)

# 返回输入数的位置
def _loc(num:int):
    return num // bitmap_per_block, num % bitmap_per_block

# 1.标记

def mark(num:int):
    if 0< num < N:
        
        i, j = _loc(num)
        # | 作用是保留其他位置，不然其它位置会清零
        bitmap[i] |= 1 << j

# 2.是否重复

def set_seen(num:int):
    
    i,j = _loc(num)

    return bool(bitmap[i] >> j & 1) == 1

# 清除

def unmark(num:int):
    if 0< num < N:
        i, j = _loc(num)
        bitmap[i] &= ~(1 << j)

```