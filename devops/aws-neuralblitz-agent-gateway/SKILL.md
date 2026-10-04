---
name: aws
description: Amazon Web Services best practices and patterns
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: cloud
---
## What I do
- Design and implement AWS architectures
- Use IAM for secure access control
- Leverage EC2, ECS, and Lambda for compute
- Use S3, RDS, and DynamoDB for storage
- Implement serverless with API Gateway and Lambda
- Use CloudFormation or CDK for infrastructure
- Set up monitoring with CloudWatch
- Implement security best practices

## When to use me
When working with AWS services or designing cloud architectures.

## IAM Best Practices
```python
import boto3
from iam_roles import create_role_with_policy


# Create IAM role with least privilege
iam = boto3.client('iam')


def create_lambda_role(function_name: str) -> str:
    assume_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    role = iam.create_role(
        RoleName=f'{function_name}-role',
        AssumeRolePolicyDocument=json.dumps(assume_policy),
        Description=f'IAM role for {function_name}',
    )

    # Attach only necessary policies
    policies = [
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
    ]

    for policy in policies:
        iam.attach_role_policy(
            RoleName=role['Role']['RoleName'],
            PolicyArn=policy,
        )

    return role['Role']['Arn']
```

## S3 Best Practices
```python
import boto3


s3 = boto3.client('s3')


def upload_with_encryption(
    bucket: str,
    key: str,
    body: bytes,
    metadata: dict = None
) -> str:
    """Upload file with server-side encryption."""
    params = {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
        'ServerSideEncryption': 'AES256',
        'ACL': 'private',
    }

    if metadata:
        params['Metadata'] = metadata

    response = s3.put_object(**params)
    return response['VersionId']


def generate_presigned_url(
    bucket: str,
    key: str,
    expiration: int = 3600
) -> str:
    """Generate pre-signed URL for temporary access."""
    return s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': key,
        },
        ExpiresIn=expiration,
    )


# S3 lifecycle policy for cost optimization
def create_lifecycle_policy():
    lifecycle = {
        'Rules': [
            {
                'ID': 'DeleteOldLogs',
                'Status': 'Enabled',
                'Prefix': 'logs/',
                'Expiration': {'Days': 90},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 60, 'StorageClass': 'GLACIER'},
                ],
            }
        ]
    }
    s3.put_bucket_lifecycle_configuration(
        Bucket='my-bucket',
        LifecycleConfiguration=lifecycle,
    )
```

## Lambda Best Practices
```python
import json
import boto3
from typing import Dict, Any


lambda_client = boto3.client('lambda')


def invoke_lambda_async(
    function_name: str,
    payload: Dict[str, Any]
) -> str:
    """Invoke Lambda asynchronously with Event invocation."""
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(payload),
    )
    return response['StatusCode']


def invoke_lambda_sync(
    function_name: str,
    payload: Dict[str, Any],
    timeout: int = 900
) -> Dict[str, Any]:
    """Invoke Lambda synchronously and wait for response."""
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
        Qualifier='$LATEST',
    )

    if response['StatusCode'] != 200:
        raise Exception(f'Lambda invocation failed: {response}')

    return json.loads(response['Payload'].read())
```

## DynamoDB Best Practices
```python
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')


def create_table_with_gsi():
    table = dynamodb.create_table(
        TableName='Orders',
        KeySchema=[
            {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
            {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'customer_id', 'AttributeType': 'S'},
            {'AttributeName': 'order_date', 'AttributeType': 'S'},
            {'AttributeName': 'status', 'AttributeType': 'S'},
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'StatusIndex',
                'KeySchema': [
                    {'AttributeName': 'status', 'KeyType': 'HASH'},
                    {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10,
                },
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        },
    )
    return table


def query_with_pagination(
    table_name: str,
    key_condition: dict,
    filter_expression: dict = None,
    limit: int = 100
) -> list:
    """Query with automatic pagination."""
    table = dynamodb.Table(table_name)
    items = []

    response = table.query(
        KeyConditionExpression=Key('pk').eq(key_condition['pk']),
        FilterExpression=Attr('status').eq('active') if filter_expression else None,
        Limit=limit,
    )

    items.extend(response.get('Items', []))

    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq(key_condition['pk']),
            ExclusiveStartKey=response['LastEvaluatedKey'],
        )
        items.extend(response.get('Items', []))

    return items
```

## Serverless Architecture
```yaml
# serverless.yml
service: my-serverless-app

provider:
  name: aws
  runtime: python3.11
  stage: ${opt:stage, 'dev'}
  region: ${opt:region, 'us-east-1'}
  lambdaHashingVersion: 20201221
  environment:
    STAGE: ${self:provider.stage}
    DYNAMODB_TABLE: ${self:service}-${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
          Resource:
            - !GetAtt DynamoDBTable.Arn
            - !Join ['/', [!GetAtt DynamoDBTable.Arn, 'index/*']]
        - Effect: Allow
          Action:
            - sqs:*
          Resource: !GetAtt SQSQueue.Arn

functions:
  processOrder:
    handler: handlers/process_order.handler
    timeout: 30
    memorySize: 256
    events:
      - http:
          path: orders
          method: post
          cors: true
      - sqs:
          - arn: !GetAtt SQSQueue.Arn

  getOrder:
    handler: handlers/get_order.handler
    timeout: 10
    events:
      - http:
          path: orders/{orderId}
          method: get

resources:
  Resources:
    DynamoDBTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: pk
            AttributeType: S
          - AttributeName: sk
            AttributeType: S
        KeySchema:
          - AttributeName: pk
            KeyType: HASH
          - AttributeName: sk
            KeyType: RANGE
        GlobalSecondaryIndexes:
          - IndexName: GSI1
            KeySchema:
              - AttributeName: pk
                KeyType: HASH
              - AttributeName: sk
                KeyType: RANGE
            Projection:
              ProjectionType: ALL

    SQSQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-queue-${self:provider.stage}
        VisibilityTimeout: 360
        MessageRetentionPeriod: 86400
```
