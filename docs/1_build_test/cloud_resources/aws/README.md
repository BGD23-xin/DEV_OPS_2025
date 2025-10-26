# aws resources

涉及的资源：
- 1.IAM
- 2.VPC
- 3.Cloudwatch
- 4.EC2
- 5.S3
- 6.ECS
- 7.ECR

其中1-3是贯穿所有aws所有项目所需要的资源,之后的资源是根据项目需求来具体使用. 因而我将资源分成2类：
- base_sources
- project_sources

在使用cloud formation创建一个资源集合时，没有直接的命令如`terraform plan`来预览创建结果，需要进行如下操作

[AWS CFN Intrinsic function reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference.html)
```bash
#需要先创建一个预览集合
aws cloudformation create-change-set \
  --stack-name <stack_name> \
  --template-body file://<file_path> \
  --change-set-name <preview_name> \
  --change-set-type CREATE \
  --region <region> \
  --profile <profile>

# 查看预览结果
aws cloudformation describe-change-set \
  --change-set-name <preview_name> \
  --stack-name <stack_name> \
  --region <region> \
  --profile <profile> \

#运行文件
aws cloudformation execute-change-set \
  --change-set-name <preview_name> \
  --stack-name <stack_name> \
  --region <region>\
  --profile <profile>
```

如果创建的资源在运行时挂了，需要手动更新或者放在ASG下