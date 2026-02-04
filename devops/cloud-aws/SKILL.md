---
name: cloud-aws
description: AWS cloud infrastructure and services expert. Use when working with AWS CLI, Terraform for AWS, Lambda, S3, EC2, DynamoDB, IAM, API Gateway, or any AWS service configuration, deployment, troubleshooting, or best practices.
---

# Cloud AWS

Expert guidance for Amazon Web Services infrastructure, development, and operations.

## Instructions

When helping with AWS tasks:

1. **Identify the AWS service(s)** involved in the request
2. **Check authentication**: Ensure AWS CLI is configured (`aws sts get-caller-identity`)
3. **Use appropriate tools**: AWS CLI or Terraform as needed
   - **Avoid SAM, CloudFormation, and CDK** - Always prefer Terraform for Infrastructure as Code
4. **Follow security best practices**: Least privilege IAM, encryption, no hardcoded credentials
5. **Consider cost implications**: Suggest cost-effective alternatives when relevant

## AWS CLI Essentials

### Authentication Check
```bash
aws sts get-caller-identity
aws configure list
```

### Common Service Commands

**S3:**
```bash
aws s3 ls
aws s3 cp file.txt s3://bucket-name/
aws s3 sync ./local-dir s3://bucket-name/prefix/
aws s3 rm s3://bucket-name/prefix/ --recursive
```

**EC2:**
```bash
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}'
aws ec2 start-instances --instance-ids i-xxxxx
aws ec2 stop-instances --instance-ids i-xxxxx
```

**Lambda:**
```bash
aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime}'
aws lambda invoke --function-name my-function output.json
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
aws logs tail /aws/lambda/my-function --follow
```

**DynamoDB:**
```bash
aws dynamodb list-tables
aws dynamodb scan --table-name my-table
aws dynamodb get-item --table-name my-table --key '{"PK":{"S":"USER#123"},"SK":{"S":"PROFILE"}}'
aws dynamodb put-item --table-name my-table --item '{"PK":{"S":"USER#123"},"SK":{"S":"PROFILE"},"name":{"S":"John"}}'
```

**API Gateway (HTTP API v2):**
```bash
aws apigatewayv2 get-apis
aws apigatewayv2 get-routes --api-id API_ID
aws apigatewayv2 get-stages --api-id API_ID
```

**CloudFront:**
```bash
aws cloudfront list-distributions --query 'DistributionList.Items[].{Id:Id,Domain:DomainName,Status:Status}'
aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*"
```

**CloudWatch:**
```bash
aws logs describe-log-groups
aws logs tail /aws/lambda/my-function --follow --since 1h
aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=my-function --start-time 2025-01-01T00:00:00Z --end-time 2025-01-02T00:00:00Z --period 3600 --statistics Sum
```

## Cost Management

### Get Current Costs
```bash
# Current month costs by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE

# Cost forecast
aws ce get-cost-forecast \
  --time-period Start=$(date -u +%Y-%m-%d),End=$(date -u +%Y-%m-31) \
  --granularity MONTHLY \
  --metric UNBLENDED_COST

# Filter by specific service
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-12-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Amazon CloudFront"]}}'
```

### Set Budget Alert
```bash
aws budgets create-budget \
  --account-id ACCOUNT_ID \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Infrastructure as Code (Terraform)
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "my_function" {
  filename         = "function.zip"
  function_name    = "my-function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "python3.12"
  source_code_hash = filebase64sha256("function.zip")
}
```

Deploy:
```bash
terraform init
terraform plan
terraform apply -auto-approve
terraform destroy
```

## Security Best Practices

### IAM Policies
- Use least privilege principle
- Prefer managed policies for common use cases
- Use conditions to restrict access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"],
      "Resource": "arn:aws:dynamodb:*:*:table/my-table",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:userid}"]
        }
      }
    }
  ]
}
```

### Secrets Management
```bash
# AWS Secrets Manager
aws secretsmanager create-secret --name my-secret --secret-string '{"key":"value"}'
aws secretsmanager get-secret-value --secret-id my-secret --query SecretString --output text

# SSM Parameter Store (cheaper for simple values)
aws ssm put-parameter --name /app/db-password --value "secret" --type SecureString
aws ssm get-parameter --name /app/db-password --with-decryption --query Parameter.Value --output text
```

### Encryption
- Enable encryption at rest for all data stores
- Use AWS KMS for key management
- Enable encryption in transit (TLS/HTTPS)

## Troubleshooting

### Check Permissions
```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT:role/my-role \
  --action-names dynamodb:PutItem \
  --resource-arns arn:aws:dynamodb:us-east-1:ACCOUNT:table/my-table
```

### Debug Lambda
```bash
aws logs tail /aws/lambda/my-function --since 1h
aws lambda get-function-configuration --function-name my-function
aws lambda get-function --function-name my-function
```

### Network Issues
```bash
aws ec2 describe-flow-logs
aws ec2 describe-security-groups --group-ids sg-xxxxx
aws ec2 describe-network-acls --network-acl-ids acl-xxxxx
```

### API Gateway Issues
```bash
aws apigatewayv2 get-api --api-id API_ID
aws logs tail /aws/api-gateway/API_ID --since 1h
```

## Cost Optimization Tips

- **Lambda**: Use ARM64 (Graviton2) for ~34% cost savings
- **DynamoDB**: Use on-demand for variable workloads, provisioned for steady-state
- **S3**: Enable Intelligent-Tiering for variable access patterns
- **CloudFront**: Use caching to reduce origin requests
- **API Gateway**: Use HTTP APIs (v2) instead of REST APIs for ~70% cost savings
- Set up billing alerts and budgets
- Use AWS Cost Explorer to identify optimization opportunities
