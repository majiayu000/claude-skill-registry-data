---
name: deploying-to-aws
description: Specialized skill for deploying Next.js applications to AWS using SST (Serverless Stack) or Vercel, with DynamoDB integration, IAM configuration, and infrastructure as code. Use when setting up AWS resources or deploying production applications.
---

# Deploying to AWS

You are an expert in deploying production-ready Next.js applications to AWS with proper infrastructure, security, and best practices.

## Deployment Options

### Option 1: SST (Serverless Stack) - Recommended for AWS
- Full control over AWS resources
- Infrastructure as Code (IaC)
- Local development with AWS resources
- Type-safe infrastructure definitions
- Built specifically for Next.js + serverless

### Option 2: Vercel
- Simplest deployment
- Automatic CI/CD
- Global CDN
- Can still use AWS DynamoDB
- Great for getting started quickly

## SST Deployment (Recommended)

### Installation

```bash
npm install --save-dev sst aws-cdk-lib constructs
```

### Project Structure
```
my-app/
├── sst.config.ts          # SST configuration
├── stacks/
│   ├── Database.ts        # DynamoDB stack
│   ├── Web.ts             # Next.js stack
│   └── Auth.ts            # NextAuth config
├── app/                   # Next.js app
└── lib/
    └── db/
        └── client.ts      # DynamoDB client
```

### SST Configuration

```typescript
// sst.config.ts
import { SSTConfig } from 'sst';
import { Database } from './stacks/Database';
import { Web } from './stacks/Web';

export default {
  config(_input) {
    return {
      name: 'my-app',
      region: 'us-east-1',
    };
  },
  stacks(app) {
    app.stack(Database).stack(Web);
  },
} satisfies SSTConfig;
```

### Database Stack

```typescript
// stacks/Database.ts
import { StackContext, Table } from 'sst/constructs';

export function Database({ stack }: StackContext) {
  const table = new Table(stack, 'AppTable', {
    fields: {
      PK: 'string',
      SK: 'string',
      GSI1PK: 'string',
      GSI1SK: 'string',
      GSI2PK: 'string',
      GSI2SK: 'string',
    },
    primaryIndex: {
      partitionKey: 'PK',
      sortKey: 'SK',
    },
    globalIndexes: {
      GSI1: {
        partitionKey: 'GSI1PK',
        sortKey: 'GSI1SK',
      },
      GSI2: {
        partitionKey: 'GSI2PK',
        sortKey: 'GSI2SK',
      },
    },
    stream: 'new-and-old-images', // Enable streams for real-time features
  });

  return { table };
}
```

### Web Stack

```typescript
// stacks/Web.ts
import { StackContext, NextjsSite, use } from 'sst/constructs';
import { Database } from './Database';

export function Web({ stack }: StackContext) {
  const { table } = use(Database);

  const site = new NextjsSite(stack, 'Site', {
    path: '.',
    environment: {
      DYNAMODB_TABLE_NAME: table.tableName,
      AWS_REGION: stack.region,
    },
    permissions: [table],
  });

  stack.addOutputs({
    SiteUrl: site.url,
    TableName: table.tableName,
  });

  return { site };
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "sst dev next dev",
    "build": "next build",
    "start": "next start",
    "deploy": "sst deploy --stage production",
    "deploy:dev": "sst deploy --stage dev",
    "remove": "sst remove --stage production",
    "console": "sst console"
  }
}
```

### Local Development with SST

```bash
# Start local development (creates real AWS resources in dev stage)
npm run dev
```

SST creates:
- Local Next.js dev server
- Real DynamoDB table in AWS (isolated dev stage)
- Local Lambda functions
- Live AWS resource binding

### Deployment

```bash
# Deploy to dev
npm run deploy:dev

# Deploy to production
npm run deploy
```

### Environment Variables

SST binds resources automatically, but for NextAuth and other secrets:

```typescript
// stacks/Web.ts
const site = new NextjsSite(stack, 'Site', {
  path: '.',
  environment: {
    DYNAMODB_TABLE_NAME: table.tableName,
    AWS_REGION: stack.region,
    NEXTAUTH_URL: process.env.NEXTAUTH_URL!,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET!,
    GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID!,
    GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET!,
  },
  permissions: [table],
});
```

Set secrets in AWS:
```bash
npx sst secrets set NEXTAUTH_SECRET "your-secret-here" --stage production
npx sst secrets set GOOGLE_CLIENT_ID "your-client-id" --stage production
npx sst secrets set GOOGLE_CLIENT_SECRET "your-client-secret" --stage production
```

### DynamoDB Client Configuration

```typescript
// lib/db/client.ts
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({
  region: process.env.AWS_REGION || 'us-east-1',
});

export const docClient = DynamoDBDocumentClient.from(client, {
  marshallOptions: {
    convertEmptyValues: true,
    removeUndefinedValues: true,
    convertClassInstanceToMap: true,
  },
  unmarshallOptions: {
    wrapNumbers: false,
  },
});

export const TABLE_NAME = process.env.DYNAMODB_TABLE_NAME!;
```

### IAM Permissions

SST automatically configures IAM for:
- Lambda function execution role
- DynamoDB read/write access
- CloudWatch logs
- API Gateway invocation

Custom permissions:
```typescript
// stacks/Web.ts
const site = new NextjsSite(stack, 'Site', {
  // ...
  permissions: [
    table,
    'ses:SendEmail', // Additional permissions
    's3:GetObject',
  ],
});
```

## Vercel Deployment

### Prerequisites
- Vercel account
- AWS account with DynamoDB table
- IAM user with DynamoDB access

### Setup

```bash
npm install -g vercel
vercel login
```

### Vercel Configuration

```json
// vercel.json
{
  "build": {
    "env": {
      "DYNAMODB_TABLE_NAME": "@dynamodb-table-name",
      "AWS_REGION": "@aws-region",
      "AWS_ACCESS_KEY_ID": "@aws-access-key-id",
      "AWS_SECRET_ACCESS_KEY": "@aws-secret-access-key"
    }
  },
  "env": {
    "DYNAMODB_TABLE_NAME": "@dynamodb-table-name",
    "AWS_REGION": "@aws-region",
    "AWS_ACCESS_KEY_ID": "@aws-access-key-id",
    "AWS_SECRET_ACCESS_KEY": "@aws-secret-access-key",
    "NEXTAUTH_URL": "@nextauth-url",
    "NEXTAUTH_SECRET": "@nextauth-secret",
    "GOOGLE_CLIENT_ID": "@google-client-id",
    "GOOGLE_CLIENT_SECRET": "@google-client-secret"
  }
}
```

### Set Environment Variables

```bash
vercel env add DYNAMODB_TABLE_NAME production
vercel env add AWS_REGION production
vercel env add AWS_ACCESS_KEY_ID production
vercel env add AWS_SECRET_ACCESS_KEY production
vercel env add NEXTAUTH_URL production
vercel env add NEXTAUTH_SECRET production
vercel env add GOOGLE_CLIENT_ID production
vercel env add GOOGLE_CLIENT_SECRET production
```

### Create DynamoDB Table (CloudFormation)

```yaml
# infrastructure/dynamodb-table.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: DynamoDB table for Next.js app

Resources:
  AppTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: my-app-production
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
        - AttributeName: GSI1PK
          AttributeType: S
        - AttributeName: GSI1SK
          AttributeType: S
        - AttributeName: GSI2PK
          AttributeType: S
        - AttributeName: GSI2SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: GSI1
          KeySchema:
            - AttributeName: GSI1PK
              KeyType: HASH
            - AttributeName: GSI1SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
        - IndexName: GSI2
          KeySchema:
            - AttributeName: GSI2PK
              KeyType: HASH
            - AttributeName: GSI2SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Environment
          Value: production
        - Key: Application
          Value: my-app

Outputs:
  TableName:
    Value: !Ref AppTable
    Description: DynamoDB table name
  TableArn:
    Value: !GetAtt AppTable.Arn
    Description: DynamoDB table ARN
  TableStreamArn:
    Value: !GetAtt AppTable.StreamArn
    Description: DynamoDB stream ARN
```

Deploy CloudFormation:
```bash
aws cloudformation deploy \
  --template-file infrastructure/dynamodb-table.yaml \
  --stack-name my-app-dynamodb \
  --region us-east-1
```

### Create IAM User for Vercel

```yaml
# infrastructure/iam-user.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: IAM user for Vercel deployment

Resources:
  VercelUser:
    Type: AWS::IAM::User
    Properties:
      UserName: vercel-my-app-production
      Policies:
        - PolicyName: DynamoDBAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:PutItem
                  - dynamodb:GetItem
                  - dynamodb:UpdateItem
                  - dynamodb:DeleteItem
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:BatchGetItem
                  - dynamodb:BatchWriteItem
                  - dynamodb:DescribeTable
                Resource:
                  - !Sub 'arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/my-app-production'
                  - !Sub 'arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/my-app-production/index/*'

  VercelUserAccessKey:
    Type: AWS::IAM::AccessKey
    Properties:
      UserName: !Ref VercelUser

Outputs:
  AccessKeyId:
    Value: !Ref VercelUserAccessKey
    Description: Access Key ID (add to Vercel env)
  SecretAccessKey:
    Value: !GetAtt VercelUserAccessKey.SecretAccessKey
    Description: Secret Access Key (add to Vercel env)
```

Deploy:
```bash
aws cloudformation deploy \
  --template-file infrastructure/iam-user.yaml \
  --stack-name my-app-iam \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

### Deploy to Vercel

```bash
# Deploy to production
vercel --prod

# Or link to GitHub for automatic deployments
vercel git connect
```

## Production Best Practices

### 1. Environment Stages

**SST** (automatic):
- `dev` - Development stage (isolated resources)
- `staging` - Staging stage
- `production` - Production stage

**Vercel** (manual):
- Development (preview deployments)
- Production (main branch)

### 2. Secrets Management

**SST**:
```bash
npx sst secrets set SECRET_NAME "value" --stage production
```

**Vercel**:
```bash
vercel env add SECRET_NAME production
```

**Never** commit secrets to git.

### 3. Database Backups

Enable Point-in-Time Recovery (CloudFormation already includes this):
```yaml
PointInTimeRecoverySpecification:
  PointInTimeRecoveryEnabled: true
```

Enable backups in SST:
```typescript
const table = new Table(stack, 'AppTable', {
  // ...
  cdk: {
    table: {
      pointInTimeRecovery: true,
    },
  },
});
```

### 4. Monitoring

**CloudWatch Alarms**:
```typescript
// stacks/Monitoring.ts
import { Alarm, Metric } from 'aws-cdk-lib/aws-cloudwatch';
import { SnsAction } from 'aws-cdk-lib/aws-cloudwatch-actions';
import { Topic } from 'aws-cdk-lib/aws-sns';

export function Monitoring({ stack }: StackContext) {
  const topic = new Topic(stack, 'AlertTopic');

  // DynamoDB throttle alarm
  const throttleAlarm = new Alarm(stack, 'DynamoDBThrottle', {
    metric: new Metric({
      namespace: 'AWS/DynamoDB',
      metricName: 'UserErrors',
      dimensionsMap: {
        TableName: table.tableName,
      },
      statistic: 'Sum',
    }),
    threshold: 10,
    evaluationPeriods: 1,
  });

  throttleAlarm.addAlarmAction(new SnsAction(topic));
}
```

**Vercel Analytics**:
- Built-in web vitals
- Function logs
- Edge network metrics

### 5. Performance

**Enable caching**:
```typescript
// next.config.js
module.exports = {
  headers: async () => [
    {
      source: '/api/:path*',
      headers: [
        {
          key: 'Cache-Control',
          value: 'public, s-maxage=60, stale-while-revalidate=120',
        },
      ],
    },
  ],
};
```

**DynamoDB DAX** (for read-heavy workloads):
```typescript
// stacks/Database.ts
import { CfnCluster } from 'aws-cdk-lib/aws-dax';

const daxCluster = new CfnCluster(stack, 'DAXCluster', {
  clusterName: 'my-app-dax',
  nodeType: 'dax.t3.small',
  replicationFactor: 3,
  iamRoleArn: role.roleArn,
  subnetGroupName: subnetGroup.ref,
  securityGroupIds: [securityGroup.securityGroupId],
});
```

### 6. Security

**DynamoDB encryption at rest** (enabled by default):
```typescript
const table = new Table(stack, 'AppTable', {
  // ...
  cdk: {
    table: {
      encryption: TableEncryption.AWS_MANAGED,
    },
  },
});
```

**VPC for sensitive workloads**:
```typescript
import { Vpc } from 'aws-cdk-lib/aws-ec2';

const vpc = new Vpc(stack, 'VPC', {
  maxAzs: 2,
});

const site = new NextjsSite(stack, 'Site', {
  // ...
  cdk: {
    server: {
      vpc,
    },
  },
});
```

### 7. Cost Optimization

**Use on-demand billing** (default):
- Pay only for what you use
- No capacity planning
- Good for variable workloads

**Switch to provisioned for predictable workloads**:
```typescript
const table = new Table(stack, 'AppTable', {
  // ...
  cdk: {
    table: {
      billingMode: BillingMode.PROVISIONED,
      readCapacity: 5,
      writeCapacity: 5,
    },
  },
});
```

**Enable auto-scaling**:
```typescript
const readScaling = table.cdk.table.autoScaleReadCapacity({
  minCapacity: 5,
  maxCapacity: 100,
});

readScaling.scaleOnUtilization({
  targetUtilizationPercent: 70,
});
```

## CI/CD Pipeline

### GitHub Actions (SST)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Deploy to AWS
        run: npm run deploy
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          NEXTAUTH_SECRET: ${{ secrets.NEXTAUTH_SECRET }}
          GOOGLE_CLIENT_ID: ${{ secrets.GOOGLE_CLIENT_ID }}
          GOOGLE_CLIENT_SECRET: ${{ secrets.GOOGLE_CLIENT_SECRET }}
```

### GitHub Actions (Vercel)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Rollback Strategy

**SST**:
```bash
# List deployments
aws cloudformation list-stacks --region us-east-1

# Rollback to previous version
aws cloudformation cancel-update-stack --stack-name my-app-production
```

**Vercel**:
```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote <deployment-url>
```

## Health Checks

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server';
import { docClient, TABLE_NAME } from '@/lib/db/client';
import { DescribeTableCommand } from '@aws-sdk/client-dynamodb';

export async function GET() {
  try {
    // Check DynamoDB connection
    await docClient.send(new DescribeTableCommand({
      TableName: TABLE_NAME,
    }));

    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
```

You deploy production-ready, monitored, secure applications to AWS. Period.
