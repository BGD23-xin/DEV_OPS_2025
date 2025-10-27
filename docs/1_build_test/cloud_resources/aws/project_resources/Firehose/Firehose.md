# Firehose

官方定义是全托管的实时数据流处理服务。 通俗理解是调节数据流的`输入`和`输出`，放置数据流因传输速率而出发写入问题。

Firehose也有数据转化的选项，其使用的是`Lambda function`工具来实现，但不做推荐。

## 配置

firehose 涉及的参数不多：
- 数据源：（如果选择Direct PUT时，需要考虑配额）
- 目标
    - 目标缓冲区（大小和等待时间）
    - 文档类型
- 备份设置(建议开启失败备份，方便排查)
- 高级配置
    - 服务访问权限（选择现有的角色）

[AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/firehose/)

```bash

aws firehose create-delivery-stream \
  --region <REGION> \
  --profile <YOUR_PROFILE> \
  --cli-input-json file://opensearch-ds.json

# 下面是json代码
"{
  "DeliveryStreamName": "my-opensearch-stream",
  "DeliveryStreamType": "DirectPut",
  "AmazonOpenSearchServiceDestinationConfiguration": {
    "RoleARN": "<arn:firehose-role>",
    "DomainARN": "<arn_opensearch_domain>",
    "IndexName": "<index_name>",
    "IndexRotationPeriod": "<frequency_of_update_index>",
    "BufferingHints": {
      "IntervalInSeconds": 60,
      "SizeInMBs": 5
    },
    "S3BackupMode": "FailedDocumentsOnly",
    "S3Configuration": {
      "RoleARN": "<arn:firehose-role>",
      "BucketARN": "<arn_s3_bucket>"
    },
    "DocumentIdOptions": {
      "DefaultDocumentIdFormat": "FIREHOSE_DEFAULT"
    }
  }
} "

```

[AWS CFN](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kinesisfirehose-deliverystream.html)


```bash
aws cloudformation create-stack \
  --stack-name <ecs_cluster> \
  --template-body file://<cluster_template> \
  --region cn-northwest-1 \
  --profile xin_xu_test \
```


## 排查问题

根据firehose的功能，可以从`输入`和`输出`2方面着手排查问题。



### 输入

查看是否由写入问题引起的可以在firehose的监控中查看：

- 传入的字节数
- 传入的put请求数
- 传入的记录数

这个方面主要看写入速度是否超过[配额](https://docs.aws.amazon.com/firehose/latest/dev/limits.html)上限。在中国的默认配额是 1 M/s 的写入。需要查看具体查看所在区域的配额，可以在`Service Quotas`中查看。


### 输出

查看是否由写入问题引起的可以在firehose的监控中查看：
- 成功传入S3(错误日志)
- 成功传入目标(如Opensearch)
- 传输给目标的记录数
- 传输给目标的字节数

如果这块有问题，需要firehose的目标缓冲区设置




