# algorithm

## [10 大排序算法](https://www.cnblogs.com/upstudy/p/16171897.html)

### 1.冒泡排序

如有n个数，需有n轮比较，每轮比较出最大或最小的数，比如，第一轮比较出所有数中的最小的或者最大数，第二轮比出剩下的最小的或者最大的

```python
# 这里是从小到大排序
def selectionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        minIndex = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[minIndex]:  # 更新最小值索引
                minIndex = j  
        nums[i], nums[minIndex] = nums[minIndex], nums[i] # 把最小数交换到前面
    return nums
```


### 2.选择排序

代码逻辑是比较 len(nums) 轮，索引依次往后挪一位,每轮是该索引对应的位置数，和索引之后的数进行比较，如果当前数比之后的数小，则记录索引位置,在本轮结束之后交换

```python

def selectionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        minIndex = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[minIndex]:  # 更新最小值索引
                minIndex = j  
        nums[i], nums[minIndex] = nums[minIndex], nums[i] # 把最小数交换到前面
    return nums
```

### 3.插入排序

运行 len(nums) 轮, 每轮有i+1个数参与,第一轮决出顺序，之后的数根据顺序插入,时间复杂度是O(n^2)
```python 
def insertionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        curNum, preIndex = nums[i+1], i  # curNum 保存当前待插入的数
        while preIndex >= 0 and curNum < nums[preIndex]: # 将比 curNum 大的元素向后移动
            nums[preIndex + 1] = nums[preIndex]
            preIndex -= 1
        nums[preIndex + 1] = curNum  # 待插入的数的正确位置   
    return nums
```

### 4.希尔排序

这个是先设置一个gap, 就i 和 i+gap 两个数进行比较交换，这一轮之后gap变为 gap //3 ,再以新的gap比较排序，直到gap = 1，就变为等效的插入排序进行排序，所以gap的设置 和 计算很重要,这个数不能比 `初始值` 比 `除数`(这里是3)，要保证最后一次gap为1或者初始就为1。。 


```python
def shellSort(nums):
    lens = len(nums)
    gap = 1  
    while gap < lens // 3:
        gap = gap * 3 + 1  # 动态定义间隔序列
    while gap > 0:
        for i in range(gap, lens):
            curNum, preIndex = nums[i], i - gap  # curNum 保存当前待插入的数
            while preIndex >= 0 and curNum < nums[preIndex]:
                nums[preIndex + gap] = nums[preIndex] # 将比 curNum 大的元素向后移动
                preIndex -= gap
            nums[preIndex + gap] = curNum  # 待插入的数的正确位置
        gap //= 3  # 下一个动态间隔
    return nums
```


### 5.归并排序 merge sort


这个代码的原理是通过递归，将集合分成最小的1个元素，在一层一层的合并排序
```python
#这个合并函数可以独立开来或者放到函数中都可以
def merge(left, right):
    result = []  # 保存归并后的结果
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result = result + left[i:] + right[j:] # 剩余的元素直接添加到末尾
    return result


def mergeSort(nums):
    # 归并过程

    # 递归过程
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = mergeSort(nums[:mid])
    right = mergeSort(nums[mid:])
    return merge(left, right)
```

### 6.快速排序

代码逻辑是 每一次递归先找一个基准数，然后比这个数小的放在左边，比这个数大的放在右边，然后对左右两边的数组进行递归处理。
```python 
def quick_sort(nums:list):
    if len(nums) <= 1:
        return nums
    pivot = nums[0]
    letf =[nums[i] for i in range(1,len(nums)) if nums[i] < pivot ]
    right = [nums[i] for i in range(1,len(nums)) if nums[i] > pivot]
    return quick_sort(letf) + [pivot] + quick_sort(right)


# 第二种写法

#先创建一个分区函数
def partition(nums, left, right):
    pivot = nums[left]  # 基准值
    while left < right:
        while left < right and nums[right] >= pivot:
            right -= 1
        nums[left] = nums[right]  # 比基准小的交换到前面
        while left < right and nums[left] <= pivot:
            left += 1
        nums[right] = nums[left]  # 比基准大交换到后面
    nums[left] = pivot # 基准值的正确位置，也可以为 nums[right] = pivot
    return left  # 返回基准值的索引，也可以为 return right


# 这里的输入left和right是数组的左右闭区间，即0 
def quickSort2(nums, left, right):  # 这种写法的平均空间复杂度为 O(logn) 
    # 分区操作

    # 递归操作
    if left < right:
        pivotIndex = partition(nums, left, right)
        quickSort2(nums, left, pivotIndex - 1)  # 左序列
        quickSort2(nums, pivotIndex + 1, right) # 右序列
    return nums

```

### 7.堆排序

逻辑代码是，先建立一个原始堆，先调整，选出一个最大值，在剩下的堆中删除这个最大值，在堆中重新调整，重复这个过程，直到堆中元素个数为1

```python
# 调整堆
def adjustHeap(nums, i, size):
    # 非叶子结点的左右两个孩子
    lchild = 2 * i + 1
    rchild = 2 * i + 2
    # 在当前结点、左孩子、右孩子中找到最大元素的索引
    largest = i 
    largest =lchild if lchild < size and nums[lchild] > nums[largest] else largest
    largest =rchild if rchild < size and nums[rchild] > nums[largest] else largest

    # 如果最大元素的索引不是当前结点，把大的结点交换到上面，继续调整堆
    if largest != i: 
        nums[largest], nums[i] = nums[i], nums[largest] 
        # 第 2 个参数传入 largest 的索引是交换前大数字对应的索引
        # 交换后该索引对应的是小数字，应该把该小数字向下调整
        # print(nums)
        adjustHeap(nums, largest, size)
# 大根堆（从小打大排列）


# 建立堆
def builtHeap(nums, size):
    for i in range(len(nums)//2)[::-1]: # 从倒数第一个非叶子结点开始建立大根堆
        # print(i)
        adjustHeap(nums, i, size)

def heapSort(nums):

    # 堆排序 
    size = len(nums)
    builtHeap(nums, size) 
    for i in range(len(nums))[::-1]: 
        # 每次根结点都是最大的数，最大数放到后面
        nums[0], nums[i] = nums[i], nums[0] 
        # print(nums)
        # 交换完后还需要继续调整堆，只需调整根节点，此时数组的 size 不包括已经排序好的数
        adjustHeap(nums, 0, i) 
    return nums  # 由于每次大的都会放到后面，因此最后的 nums 是从小到大排列
```

### 8.计数排序


 
代码逻辑是 先根据最大值建立一个桶，包含 集合中最大值个数的 0, 在通过将数值转化成index来计数，之后排序可以直接提取索引就可以了。


```python 
def countingSort(nums):
    # 找到最值
    max_num = nums[0]
    for num in nums:
        if num > max_num:
            max_num = num
    #创建桶
    bucket = [0] * (max_num + 1)
    # bucket = [0] * (max(nums) + 1) # 桶的个数
    for num in nums:  # 将元素值作为键值存储在桶中，记录其出现的次数
        bucket[num] += 1
    i = 0  # nums 的索引
    for j in range(len(bucket)):
        while bucket[j] > 0:
            nums[i] = j
            bucket[j] -= 1
            i += 1
    return nums
```


### 9.桶排序


```python

def insertionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        curNum, preIndex = nums[i+1], i  # curNum 保存当前待插入的数
        while preIndex >= 0 and curNum < nums[preIndex]: # 将比 curNum 大的元素向后移动
            nums[preIndex + 1] = nums[preIndex]
            preIndex -= 1
        nums[preIndex + 1] = curNum  # 待插入的数的正确位置   
    return nums

def bucketSort(nums, defaultBucketSize = 5):
    maxVal, minVal = max(nums), min(nums)
    bucketSize = defaultBucketSize  # 如果没有指定桶的大小，则默认为5
    bucketCount = (maxVal - minVal) // bucketSize + 1  # 数据分为 bucketCount 组
    buckets = []  # 二维桶
    for i in range(bucketCount):
        buckets.append([])
    # 利用函数映射将各个数据放入对应的桶中
    for num in nums:
        buckets[(num - minVal) // bucketSize].append(num)
    nums.clear()  # 清空 nums
    # 对每一个二维桶中的元素进行排序
    for bucket in buckets:
        insertionSort(bucket)  # 假设使用插入排序
        nums.extend(bucket)    # 将排序好的桶依次放入到 nums 中
    return nums
```

### 10.基数排序


这个代码逻辑是 先创建 0-9 的 空桶， 先排个位，将集合中的数一次放到对用个位数的空桶中，之后在依次倒回到集合中，执行次数由 集合中最大的数决定

```python 
# LSD Radix Sort

def radixSort(nums):
    mod = 10
    div = 1
    mostBit = len(str(max(nums)))  # 最大数的位数决定了外循环多少次
    buckets = [[] for row in range(mod)] # 构造 mod 个空桶
    while mostBit:
        for num in nums:  # 将数据放入对应的桶中
            buckets[num // div % mod].append(num)
        i = 0  # nums 的索引
        for bucket in buckets:  # 将数据收集起来
            while bucket:
                nums[i] = bucket.pop(0) # 依次取出
                i += 1
        div *= 10
        mostBit -= 1
    return nums
```


### 尝试编写

```python

# 位图排序
# 算法会去重返回

def _loc(num:int,bitmap_per_block):
    return num // bitmap_per_block, num % bitmap_per_block


def bitmap_sort(nums,bitmap_per_block=32):

    max_num = max(nums)
    bitmap = [0] * ((max_num + bitmap_per_block - 1) // bitmap_per_block)
    
    # 标记出现的位置
    for num in nums:
        i,j = _loc(num,bitmap_per_block)
        bitmap[i] |= 1 << j

    sort_result =[]
    
    # 提取出位置
    for i in range(len(bitmap)):
        bits = bitmap[i]
        for j in range(bitmap_per_block):

            if bits & (1 << j):
                sort_result.append(i * bitmap_per_block + j)
    
    return sort_result

```

## 广度优先和深度优先搜索

### [图的概念](https://zhuanlan.zhihu.com/p/35864291)

`图` 是 一种数据结构

图结构 数据元素的关系，包含 数据节点, 边 , 权重 以及 方向。


`图的搜索算法`：就是通过数据节点的连接，从起始节点到目标节点的过程

### 广度优先搜索算法

从起始节点，一层一层遍历所有的相连的节点，直至到目标节点的最短过程为止。
用途：
- 网络爬虫： 查找目标网页关联的资源
- 最短路径查找
- 图搜索

```python

from collections import deque

def bfs(graph, start):
    visited = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])
    return visited
    
```

### 深度优先搜索算法

从起始节点，沿着一条路径深入，直到不能再深入为止，然后回溯到上一层节点，之后再走，再回溯。
这是用于遍历所有的路径

```python
# 递归算法
def dfs(graph, node, visited):

    if node not in visited:
        visited.append(node)
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited)
    return visited

# 判断是否可达
def dfs(graph,start,target, visited):
    if start == target:
        return True

    if start not in visited:
        visited.append(start)
        for neighbor in graph[start]:
            dfs(graph, neighbor,target, visited)
            # 这里是为了一层一层返回
            return True
    return False


```

