# EC2

全称是`Elastic Compute Cloud`，即在vpc上创建一个虚拟机，来部署运行项目。

这块主要涉及3个部分：
- 实例
- 网络与安全
- 负载

## 实例
实例部分就是按需创建虚拟机，设置放置的vpc环境，如果是公有子网上，可以绑定弹性IP，来让外部访问。

下面将会介绍几种使用代码创建的实例：

### 使用aws cli创建实例
可以访问 `https://docs.aws.amazon.com/cli/v1/reference/ec2/run-instances.html` 来查看所有参数

```bash
aws ec2 run-instances --profile <fire.name>  --cli-input-json file://<path of json>
```

`file://<path of json>` 这部份可以是json字段或者是json文件，一般推荐json文件，防止出错。

json文件，由aws 生成一个基本模版。

在自己编写时，主要需要改如下:

```json

"ImageId":环境和架构组成
"InstanceType":实例类型
"KeyName":密钥名称
"NetworkInterfaces/SubnetId":子网id
"NetworkInterfaces/Groups": 安全组
"TagSpecifications/tags/name":实例名称

```

### 使用cloud formation创建
`注`:如果创建单个资源推荐直接使用aws cli创建，如果创建多个资源推荐使用cloud formation创建


可以访问：`https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-instance.html`
查看所有参数定义.


以下是使用cloudformation创建的指令，一个是在yml中申明参数，一个是将参数放在json中(也可以在自己定义json字段，不推荐)
```bash
aws cloudformation create-stack \
  --stack-name ec2-test-stack \
  --template-body file://ec2.yml \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --parameters \
    ParameterKey=instance_name,ParameterValue=test \
    ParameterKey=image_id,ParameterValue=ami-01785c07ce58610d6 \
    ParameterKey=instance_type,ParameterValue=t2.micro \


#或者
aws cloudformation create-stack \
  --stack-name ec2-test-stack \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --template-body file://ec2.yml \
  --parameters file://params.json \

```

### 排查问题

最直观的问题显示就是创建不成功。
使用代码查看：
```bash
#对于 cli 命令
# 查看所有实例信息
aws ec2 describe-instances \
  --region cn-northwest-1 \
  --profile xin_xu_test

#查看某个实例状态
aws ec2 describe-instance-status \
  --instance-ids i-0123456789abcdef0 \
  --region cn-northwest-1 \
  --profile xin_xu_test

# 筛选实例
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=test" \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --query "Reservations[*].Instances[*].[InstanceId,State.Name,PrivateIpAddress,PublicIpAddress]"





# 对于cloudformation 命令
#查看所有
aws cloudformation list-stacks \
  --region cn-northwest-1 \
  --profile xin_xu_test


#查看特定的
aws cloudformation describe-stacks \
  --stack-name ec2-test-stack \
  --region cn-northwest-1 \
  --profile xin_xu_test \
  --query "Stacks[0].StackStatus" #这个是查看状态

# 查看实时
aws cloudformation describe-stack-events \
  --stack-name ec2-test-stack \
  --region cn-northwest-1 \
  --profile xin_xu_test

```


## 网络与安全

有指令可以直接查看，但是还是推荐在终端查看，更直接

```bash
#基本指令是
aws ec2 describe-security-groups \
  --profile xin_xu_test \
  --region cn-northwest-1 \
  --output json

#查看特定信息
aws ec2 describe-security-groups \
  --profile xin_xu_test \
  --region cn-northwest-1 \
  --query "SecurityGroups[*].[GroupId, GroupName]" \
  --output table

```


## 负载均衡

其主要职责是流量分发来保证服务高可用。

有以下几个种类：
- Application
- Network
- Classic

其主要配置是需要配置目标组