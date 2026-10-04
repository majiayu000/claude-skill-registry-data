---
name: serverless
description: Serverless - Cloud Functions & Event-Driven Architecture. Build APIs, event processing, scheduled tasks with AWS Lambda, API Gateway, DynamoDB. Use when building auto-scaling backend without managing servers.
---

# Serverless - Cloud Functions & Event-Driven Architecture

**Purpose**: Build scalable, cost-effective applications using serverless architecture with AWS Lambda, API Gateway, and managed services

**Agent**: Amazon Cloud Architect
**Use When**: Building APIs, event processing, scheduled tasks, or auto-scaling backend services without managing servers

---

## Overview

Serverless lets you run code without provisioning or managing servers. Pay only for compute time consumed.

**Core Benefits**:
- No server management
- Automatic scaling (0 to millions of requests)
- Pay-per-use (no idle costs)
- High availability built-in
- Focus on code, not infrastructure

**AWS Serverless Stack**:
- **Lambda**: Function as a Service
- **API Gateway**: HTTP APIs
- **DynamoDB**: NoSQL database
- **S3**: Object storage
- **EventBridge**: Event bus
- **SQS/SNS**: Messaging

---

## Quick Start: Lambda + API Gateway

### Basic Lambda Handler
```typescript
export const handler = async (event: any) => {
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello from Lambda!' })
  }
}
```

### API Gateway Handler
```typescript
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda'

export const handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  const { httpMethod, pathParameters, body } = event

  switch (httpMethod) {
    case 'GET':
      return respond(200, await getUsers())
    case 'POST':
      return respond(201, await createUser(JSON.parse(body || '{}')))
    default:
      return respond(405, { error: 'Method not allowed' })
  }
}

function respond(statusCode: number, data: any) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    body: JSON.stringify(data)
  }
}
```

---

## Infrastructure as Code

### AWS SAM (Quick Start)
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: nodejs20.x
      Handler: index.handler
      Events:
        Api:
          Type: Api
          Properties:
            Path: /users
            Method: GET
```

```bash
sam build && sam deploy --guided
```

### AWS CDK (Production)
```typescript
const table = new dynamodb.Table(this, 'Table', {
  partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
})

const handler = new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.NODEJS_20_X,
  code: lambda.Code.fromAsset('dist'),
  handler: 'index.handler',
  environment: { TABLE_NAME: table.tableName }
})

table.grantReadWriteData(handler)
```

---

## Common Patterns

### 1. Event-Driven Processing
- **S3 triggers**: Process uploaded files (resize images, extract text)
- **SQS triggers**: Async job processing with retry/DLQ
- **EventBridge**: Event routing and filtering

### 2. Scheduled Tasks (Cron)
```typescript
// CDK
new events.Rule(this, 'DailyReport', {
  schedule: events.Schedule.cron({ hour: '9', minute: '0' }),
  targets: [new targets.LambdaFunction(reportFunction)]
})
```

### 3. API with Authentication
- Cognito User Pools
- Custom Lambda Authorizer
- API Key for external clients

**For detailed code examples**: Read `references/code-examples.md`

---

## Best Practices

### Cold Start Optimization
```typescript
// ❌ Bad: Initialize inside handler
export const handler = async () => {
  const db = new DynamoDBClient({})  // Cold start every time!
}

// ✅ Good: Initialize outside handler
const db = new DynamoDBClient({})  // Reused across invocations

export const handler = async () => {
  // Use db
}
```

### Error Handling
```typescript
export const handler = async (event: any) => {
  try {
    const result = await processEvent(event)
    return { statusCode: 200, body: JSON.stringify(result) }
  } catch (error) {
    console.error('Error:', error)
    if (error instanceof ValidationError) {
      return { statusCode: 400, body: JSON.stringify({ error: error.message }) }
    }
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal error' }) }
  }
}
```

### Logging
```typescript
export const handler = async (event: any, context: any) => {
  console.log('Request ID:', context.requestId)
  console.log('Event:', JSON.stringify(event))
  // ...
}
```

---

## Cost Optimization

| Strategy | Description |
|----------|-------------|
| **Right-size memory** | Test 128MB-10GB, find cost/speed sweet spot |
| **Minimize package** | Use esbuild, tree-shaking, production deps only |
| **Use Provisioned Concurrency** | Only for critical, consistent-load functions |
| **Avoid polling** | Use EventBridge/SQS instead of scheduled polling |

### Package Optimization
```bash
# Bundle with esbuild
esbuild src/index.ts --bundle --platform=node --target=node20 --outfile=dist/index.js

# Production only
npm install --production
```

---

## DynamoDB Quick Reference

```typescript
import { DynamoDBDocumentClient, GetCommand, PutCommand } from '@aws-sdk/lib-dynamodb'

const docClient = DynamoDBDocumentClient.from(new DynamoDBClient({}))

// Get
const { Item } = await docClient.send(new GetCommand({
  TableName: 'users',
  Key: { id: '123' }
}))

// Put
await docClient.send(new PutCommand({
  TableName: 'users',
  Item: { id: '123', name: 'John', createdAt: new Date().toISOString() }
}))
```

---

## Reference Files

For detailed code examples including:
- Lambda function patterns
- API Gateway integration
- DynamoDB operations
- AWS SAM templates
- AWS CDK stacks
- Event-driven patterns (S3, SQS, EventBridge)
- Authentication with Cognito
- Best practices and cost optimization

**Read**: `references/code-examples.md`

---

**Remember**: Serverless is not "no ops" - it's "different ops". Monitor costs, optimize cold starts, and design for statelessness.

**Created**: 2026-02-04
**Maintained By**: Amazon Cloud Architect
**Version**: AWS Lambda (Node.js 20)
