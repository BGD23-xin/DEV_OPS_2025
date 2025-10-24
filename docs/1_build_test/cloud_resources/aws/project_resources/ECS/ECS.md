# ECS(Amazon Elastic Container Service)

这是一个全托管的容器编排服务，本质可以视作是托管的docker.
这个底层逻辑是，用户在ecs console创建ecs 之后，ecs console会生成 cloudformation 的模版文件，来创建项目所需的资源。 逻辑链是 ： `ECS console -> cloudformation -> creation resources`

创建一个ECS包含以下几个步骤：
 -  创建集合(cluster)
 -  创建任务定义(task definition)
 -  创建服务(service)

## cluster

在其创建时 有两个选择（可多选）：
 - Fargate
 - EC2
 
 Fargate是容器化的部署, EC2是实例上的应用部署. 前者只需配置 `CPU`和`memory` , 后者需要管理EC2实例.
 如果对`计算资源(GPU)`没有特别的要求的话，`推荐使用 Fargate 模式`

```yml

```
[`aws cli`](https://docs.aws.amazon.com/cli/latest/reference/ecs/create-cluster.html)

```bash
aws ecs create-cluster \
  --cluster-name <cluster-name> \
  --capacity-providers FARGATE FARGATE_SPOT \
  --settings name=containerInsights,value=disabled \
  --configuration 'executeCommandConfiguration={logging=DEFAULT}' \
  --service-connect-defaults namespace=<connect_space_name>
```

[`aws CFN`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-cluster.html)

```bash
# 这是使用ecs cluster手动创建时等效的配置。
aws cloudformation create-stack \
  --stack-name <ecs_cluster> \
  --template-body file://<cluster_template> \
  --region cn-northwest-1 \
  --profile xin_xu_test \
```

## task

之间创建的cluster是一个空的框架，需要先创建task之后，将其部署到服务中才算完整

这里task可以理解为一个docker-compose,里面的容器有单独的日志路由，如果都设置firelens来做日志路由，需要给每个容器设置一个`tag`，方便后续firelens进行过滤。

['aws cli'](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_AWSCLI_EC2.html)


```bash
#这里的json文件的可以使用手动创建之后生成的json作为模版文件
aws ecs register-task-definition --cli-input-json file://<json_path>
```

['aws CFN'](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-taskdefinition.html)


```bash
aws cloudformation create-stack \
  --stack-name <ecs_cluster> \
  --template-body file://<cluster_template> \
  --region cn-northwest-1 \
  --profile xin_xu_test \
```


## service

有如下参数需要配置：
- 任务选择
- 计算配置(一般选启动类型，fargate，最新版)
- 排查选项(ecs exec，需要权限，本地排查容器)
- 部署配置
    - 调度策略(fargate 默认时副本模式)
    - 预期任务数(默认1，运行多少个task副本)
    - 运行状况检查宽限期(默认0s开始健康检查)
- 网络配置(VPC, subnet, security group) 注:其中有个公有IP选项如果发在私有子网下，是分不到公有IP
- 负载均衡器(ALB, NLB)
- ASG（）

查看任务信息
```bash
aws ecs list-tasks \
  --cluster <cluster_name> \
  --service-name <service_name>

aws ecs describe-tasks \
  --cluster <cluster_name> \
  --tasks <task_arn>
```

## 排查问题

常见问题有创建失败，一般需要检查task。
如果创建并运行成功，后遇到的问题一般可以归纳为2类，输入和输出

### 输入

需要查看
- service的参数是否有问题(查看运行状况,task运行状况 以及 事件)
- 检查VPC，安全组
- 如果有设置ALB，可以查看映射资源中，查看目标运行状况

常见的查看指令是

```bash
#查看指标：状态，期望有几个容器，实际运行几个，有几个启动中，服务状态
aws ecs describe-services \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --cluster <cluster_name> \
  --services <service_name> \
  --query 'services[0].[status,desiredCount,runningCount,pendingCount,deployments[*].status]'

#正常情况是 desiredCount = runningCount，pendingCount = 0,deployments[*].status 返回 "PRIMARY"，如果有"PRIMARY ACTIVE" 说明服务重新部署了


# 查看 事件
aws ecs describe-services \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --cluster <cluster_name> \
  --services <service_name> \
  --query 'services[0].events[0:10]'

```

### 输出

这个一般是容器出现问题
需要在服务下查看容器日志，从而找出原因

在开启ecs exec配置之后，可以远程查看容器

```bash
aws ecs execute-command \
  --region <region> \
  --cluster <cluster_name> \
  --task <task_id> \
  --container <container_name> \
  --interactive \
  --command "/bin/sh"
```