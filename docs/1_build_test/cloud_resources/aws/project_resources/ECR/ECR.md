## ECR

官方定义是安全、可扩展且可靠的托管容器镜像注册服务. 因而 其主要作用是托管项目所需的镜像. 

[AWS cli](https://docs.aws.amazon.com/cli/latest/reference/ecr/create-repository.html)

```bash
aws ecr create-repository \
  --repository-name <name> \
  --encryption-configuration encryptionType=KMS,kmsKey="keys_arn" \
  --region <region>

```

[AWS CFN](https://docs.aws.amazon.com/zh_cn/AWSCloudFormation/latest/TemplateReference/aws-resource-ecr-repository.html)

```bash
AWSTemplateFormatVersion: "2010-09-09"
Description: Create an ECR repository encrypted with a customer-managed KMS key.

Parameters:
  RepositoryName:
    Type: String
    Description: ECR repository name (e.g., my-private-repo)
  KmsKeyId:
    Type: String
    Description: KMS key ARN or alias (e.g., arn:aws:kms:ap-southeast-1:111122223333:key/xxxx or alias/my-ecr-key)

Resources:
  EcrRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: !Ref RepositoryName
      EncryptionConfiguration:
        EncryptionType: KMS
        KmsKey: !Ref KmsKeyId

Outputs:
  RepositoryArn:
    Value: !GetAtt EcrRepository.Arn
    Export:
      Name: !Sub "${AWS::StackName}-RepositoryArn"
  RepositoryUri:
    Value: !GetAtt EcrRepository.RepositoryUri
    Export:
      Name: !Sub "${AWS::StackName}-RepositoryUri"

```