---
name: aws
description: AWS services including Lambda, S3, DynamoDB, CloudFormation, CDK, IAM, and serverless architecture patterns
layer: domain
category: devops
triggers:
  - "aws"
  - "lambda"
  - "s3"
  - "dynamodb"
  - "cloudformation"
  - "cdk"
  - "api gateway"
  - "ecs"
  - "fargate"
  - "sqs"
  - "sns"
inputs: [architecture requirements, scaling needs, cost constraints, compliance requirements]
outputs: [CDK stacks, CloudFormation templates, Lambda functions, IAM policies, architecture diagrams]
linksTo: [terraform, kubernetes, monitoring, docker, cicd]
linkedFrom: [ship, plan, infrastructure]
preferredNextSkills: [monitoring, terraform, cicd]
fallbackSkills: [cloudflare, vercel]
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: [resource provisioning, IAM changes, deployments]
---

# AWS Specialist

## Purpose

Design and implement scalable, cost-effective, and secure AWS architectures. This skill covers Lambda, S3, DynamoDB, ECS/Fargate, API Gateway, IAM, CDK, CloudFormation, and serverless-first design patterns.

## Key Patterns

### CDK Stack: Serverless API

```typescript
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { Construct } from "constructs";

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table
    const table = new dynamodb.Table(this, "ItemsTable", {
      tableName: `${id}-items`,
      partitionKey: { name: "pk", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "sk", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      timeToLiveAttribute: "ttl",
    });

    table.addGlobalSecondaryIndex({
      indexName: "GSI1",
      partitionKey: { name: "gsi1pk", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "gsi1sk", type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // Lambda function
    const handler = new NodejsFunction(this, "ApiHandler", {
      entry: "lambda/api/index.ts",
      handler: "handler",
      runtime: lambda.Runtime.NODEJS_20_X,
      architecture: lambda.Architecture.ARM_64,
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: {
        TABLE_NAME: table.tableName,
        NODE_OPTIONS: "--enable-source-maps",
      },
      bundling: {
        minify: true,
        sourceMap: true,
        treeshaking: true,
      },
      tracing: lambda.Tracing.ACTIVE,
    });

    table.grantReadWriteData(handler);

    // API Gateway
    const api = new apigateway.RestApi(this, "Api", {
      restApiName: `${id}-api`,
      deployOptions: {
        stageName: "v1",
        throttlingRateLimit: 1000,
        throttlingBurstLimit: 500,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    const items = api.root.addResource("items");
    items.addMethod("GET", new apigateway.LambdaIntegration(handler));
    items.addMethod("POST", new apigateway.LambdaIntegration(handler));

    const item = items.addResource("{id}");
    item.addMethod("GET", new apigateway.LambdaIntegration(handler));
    item.addMethod("PUT", new apigateway.LambdaIntegration(handler));
    item.addMethod("DELETE", new apigateway.LambdaIntegration(handler));

    new cdk.CfnOutput(this, "ApiUrl", { value: api.url });
  }
}
```

### DynamoDB Single-Table Design

```typescript
// Key schema for single-table design
interface DynamoItem {
  pk: string;    // Partition key
  sk: string;    // Sort key
  gsi1pk?: string;
  gsi1sk?: string;
  type: string;
  ttl?: number;
  [key: string]: unknown;
}

// User: pk=USER#<id>, sk=PROFILE
// Order: pk=USER#<id>, sk=ORDER#<orderId>
// Product: pk=PRODUCT#<id>, sk=METADATA
// GSI1: gsi1pk=ORDER#<status>, gsi1sk=<createdAt>

import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, QueryCommand, PutCommand } from "@aws-sdk/lib-dynamodb";

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}));

async function getUserWithOrders(userId: string) {
  const result = await client.send(new QueryCommand({
    TableName: process.env.TABLE_NAME,
    KeyConditionExpression: "pk = :pk AND sk BETWEEN :profile AND :orders",
    ExpressionAttributeValues: {
      ":pk": `USER#${userId}`,
      ":profile": "ORDER#",
      ":orders": "ORDER#~",
    },
  }));
  return result.Items;
}
```

### Lambda Handler Pattern

```typescript
import { APIGatewayProxyHandlerV2 } from "aws-lambda";

// Cold start optimization: initialize outside handler
const db = DynamoDBDocumentClient.from(new DynamoDBClient({}));

export const handler: APIGatewayProxyHandlerV2 = async (event) => {
  try {
    const { httpMethod, pathParameters, body } = event;

    switch (httpMethod) {
      case "GET":
        return await getItem(pathParameters?.id);
      case "POST":
        return await createItem(JSON.parse(body || "{}"));
      default:
        return { statusCode: 405, body: "Method Not Allowed" };
    }
  } catch (error) {
    console.error("Lambda error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};
```

### IAM Least Privilege Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:123456789012:table/my-table",
        "arn:aws:dynamodb:us-east-1:123456789012:table/my-table/index/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/uploads/*"
    }
  ]
}
```

## Best Practices

### Lambda
- Use ARM64 architecture (cheaper, often faster)
- Set memory based on profiling (more memory = more CPU)
- Initialize clients outside the handler (reuse across invocations)
- Enable X-Ray tracing for observability
- Use Powertools for structured logging, tracing, and metrics
- Bundle with esbuild for smaller packages and faster cold starts

### DynamoDB
- Use single-table design for related entities
- Design access patterns FIRST, then the table schema
- Use PAY_PER_REQUEST for unpredictable workloads
- Enable point-in-time recovery on all tables
- Use TTL for automatic cleanup of temporary data
- Use batch operations for bulk reads/writes

### S3
- Enable versioning on important buckets
- Use lifecycle rules to transition to cheaper tiers
- Enable server-side encryption (SSE-S3 or SSE-KMS)
- Use presigned URLs for direct client uploads
- Block public access by default

### Cost Optimization
- Use Graviton (ARM) for Lambda, ECS, EC2
- Use Savings Plans for steady-state workloads
- Enable S3 Intelligent-Tiering for unpredictable access
- Use DynamoDB on-demand for spiky workloads
- Set up AWS Budgets alerts

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Overly broad IAM policies | Use least privilege; specify resource ARNs |
| Lambda cold starts | Use provisioned concurrency for latency-sensitive paths |
| DynamoDB hot partitions | Distribute keys evenly; avoid sequential IDs |
| S3 public buckets | Block public access at account level |
| Missing CloudWatch alarms | Set alarms on errors, latency, throttling |
| Hardcoded region/account | Use `Aws.REGION` and `Aws.ACCOUNT_ID` in CDK |

## Examples

### S3 Presigned Upload URL

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({});

async function getUploadUrl(key: string, contentType: string) {
  const command = new PutObjectCommand({
    Bucket: process.env.UPLOAD_BUCKET,
    Key: key,
    ContentType: contentType,
  });

  return getSignedUrl(s3, command, { expiresIn: 3600 });
}
```

### SQS Event Processing

```typescript
import { SQSHandler } from "aws-lambda";

export const handler: SQSHandler = async (event) => {
  const failedIds: string[] = [];

  for (const record of event.Records) {
    try {
      const body = JSON.parse(record.body);
      await processMessage(body);
    } catch (error) {
      console.error(`Failed to process ${record.messageId}:`, error);
      failedIds.push(record.messageId);
    }
  }

  // Partial batch failure reporting
  if (failedIds.length > 0) {
    return {
      batchItemFailures: failedIds.map((id) => ({ itemIdentifier: id })),
    };
  }
};
```
