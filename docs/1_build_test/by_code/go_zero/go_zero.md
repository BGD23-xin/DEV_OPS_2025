# Go_zero 
[参考网站](https://go-zero.dev/docs/concepts/overview)

https://go-zero.dev/docs/reference

一个项目的主要逻辑是：先确定服务架构，

每一层可以看作是一个独立的服务模块，需要goctl 在逻辑的基础上生成配置文件。
主要结构是：
- api 网关层
- rpc 服务层
- model 层（数据库）

创建model层
```go

goctl model mysql datasource \
  -url="root:12345678@tcp(localhost:5650)/testdb" \
  -table="tenant_info" \
  -dir="/Users/xin/Project/study_go_zero/workplace/model" \
  -style gozero
```




https://juejin.cn/post/7138960256054345741#heading-6
https://github.com/qingconglaixueit/my_test_Demo


https://github.com/zhoushuguang/lebron/blob/main/apps/order/rpc/order.proto
