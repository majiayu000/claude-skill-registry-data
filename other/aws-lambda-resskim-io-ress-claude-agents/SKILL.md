---
name: aws-lambda
description: "AWS Lambda 서버리스 — 콜드 스타트 최적화, 이벤트 소스 통합, VPC 연결, 비용 최적화. Use when Lambda 함수를 설계하거나 지연·비용 문제를 줄일 때."
---

# AWS Lambda & Serverless Patterns

AWS Lambda 기반 서버리스 아키텍처 설계, 콜드 스타트 최적화, 이벤트 소스 통합

## Quick Reference (결정 트리)

```
서버리스 적합성 판단
    │
    ├─ 짧은 실행 (<15분) + 간헐적 트래픽 ──> Lambda 적합
    │
    ├─ 상시 트래픽 + 긴 실행 ──────────────> ECS/EKS
    │
    ├─ 실시간 응답 필수 (p99 < 100ms) ────> 컨테이너 또는 Provisioned
    │
    └─ 배치 처리 + 비용 민감 ──────────────> Lambda + SQS

콜드 스타트 최소화
    │
    ├─ Java/Spring ──> Provisioned Concurrency + SnapStart
    │
    ├─ Node.js/Python ──> 번들 최소화, 지연 로딩
    │
    └─ Go/Rust ──> 거의 무시 가능
```

---

## Lambda 기본 구조

### Node.js Handler

```javascript
// handler.js
export const handler = async (event, context) => {
  // 콜드 스타트 시에만 실행 (핸들러 밖에서 초기화)
  // DB 연결 등은 여기서

  try {
    const result = await processEvent(event);
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};

// DB 연결은 핸들러 밖에서 (재사용)
let dbConnection;
const getDb = async () => {
  if (!dbConnection) {
    dbConnection = await createConnection();
  }
  return dbConnection;
};
```

### Python Handler

```python
# handler.py
import json
import boto3

# 핸들러 밖: 콜드 스타트 시 1회 실행
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def handler(event, context):
    try:
        user_id = event['pathParameters']['id']
        response = table.get_item(Key={'id': user_id})

        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Item', {}))
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Go Handler

```go
package main

import (
    "context"
    "encoding/json"
    "github.com/aws/aws-lambda-go/events"
    "github.com/aws/aws-lambda-go/lambda"
)

func handler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
    response := map[string]string{"message": "Hello"}
    body, _ := json.Marshal(response)

    return events.APIGatewayProxyResponse{
        StatusCode: 200,
        Body:       string(body),
        Headers:    map[string]string{"Content-Type": "application/json"},
    }, nil
}

func main() {
    lambda.Start(handler)
}
```

---

## Cold Start 최적화

### 런타임별 콜드 스타트

| 런타임 | 콜드 스타트 | 최적화 방법 |
|--------|-----------|------------|
| Go, Rust | ~100ms | 거의 불필요 |
| Node.js | ~200-500ms | 번들 최소화, Tree Shaking |
| Python | ~300-700ms | 지연 import, Layer 활용 |
| Java | ~3-10초 | **SnapStart** (필수), Provisioned |

### Java SnapStart (필수)

```yaml
# serverless.yml
functions:
  api:
    handler: com.example.Handler
    runtime: java21
    snapStart:
      applyOn: PublishedVersions
    timeout: 30
    memorySize: 1024
```

```java
// CRaC 초기화 훅
public class Handler implements RequestHandler<Event, Response>, CracResource {
    private final Service service;

    public Handler() {
        this.service = new Service();
        Core.getGlobalContext().register(this);
    }

    @Override
    public void beforeCheckpoint(Context<? extends Resource> context) {
        // 스냅샷 전 정리 (DB 연결 닫기)
    }

    @Override
    public void afterRestore(Context<? extends Resource> context) {
        // 복원 후 재초기화 (DB 재연결)
    }
}
```

### Provisioned Concurrency

```yaml
# serverless.yml
functions:
  api:
    handler: handler.main
    provisionedConcurrency: 5  # 항상 5개 웜 인스턴스 유지
```

**비용 계산**: Provisioned는 On-Demand보다 ~60% 비쌈. 일정 트래픽 이상에서만 사용.

### 번들 최소화 (Node.js)

```javascript
// esbuild.config.js
import { build } from 'esbuild';

await build({
  entryPoints: ['src/handler.ts'],
  bundle: true,
  minify: true,
  platform: 'node',
  target: 'node20',
  outfile: 'dist/handler.js',
  external: ['@aws-sdk/*'],  // Lambda에 내장된 SDK 제외
  treeShaking: true,
});
```

---

## Event Sources

### API Gateway (REST/HTTP API)

```yaml
# serverless.yml
functions:
  getUser:
    handler: handler.getUser
    events:
      - httpApi:
          path: /users/{id}
          method: get
```

| 타입 | 특징 | 용도 |
|------|------|------|
| **HTTP API** | 저렴, 빠름, 기본 기능 | 대부분의 API |
| **REST API** | 캐싱, WAF, 사용량 계획 | 엔터프라이즈 |

### SQS (비동기 처리)

```yaml
functions:
  processQueue:
    handler: handler.process
    events:
      - sqs:
          arn: !GetAtt MyQueue.Arn
          batchSize: 10
          maximumBatchingWindow: 5
```

```javascript
export const process = async (event) => {
  const results = await Promise.allSettled(
    event.Records.map(record => processMessage(JSON.parse(record.body)))
  );

  // 부분 실패 시 실패한 것만 DLQ로
  const failures = results
    .map((r, i) => r.status === 'rejected' ? event.Records[i].messageId : null)
    .filter(Boolean);

  return {
    batchItemFailures: failures.map(id => ({ itemIdentifier: id }))
  };
};
```

### EventBridge (이벤트 기반)

```yaml
functions:
  orderCreated:
    handler: handler.onOrderCreated
    events:
      - eventBridge:
          pattern:
            source: ['order-service']
            detail-type: ['OrderCreated']
```

### S3 Trigger

```yaml
functions:
  processImage:
    handler: handler.processImage
    events:
      - s3:
          bucket: my-bucket
          event: s3:ObjectCreated:*
          rules:
            - prefix: uploads/
            - suffix: .jpg
```

### DynamoDB Streams

```yaml
functions:
  syncToSearch:
    handler: handler.sync
    events:
      - stream:
          type: dynamodb
          arn: !GetAtt UsersTable.StreamArn
          batchSize: 100
          startingPosition: LATEST
          filterPatterns:
            - eventName: [INSERT, MODIFY]
```

---

## 아키텍처 패턴

### API + DynamoDB (단순 CRUD)

```
Client → API Gateway → Lambda → DynamoDB
```

```yaml
# serverless.yml
service: user-service

provider:
  name: aws
  runtime: nodejs20.x
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:Query
          Resource: !GetAtt UsersTable.Arn

functions:
  api:
    handler: handler.main
    events:
      - httpApi: '*'

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: users
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH
```

### 비동기 처리 (이미지 리사이징)

```
S3 Upload → Lambda → S3 (resized)
         ↓
      SQS (DLQ)
```

```javascript
export const processImage = async (event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = record.s3.object.key;

    const image = await s3.getObject({ Bucket: bucket, Key: key });
    const resized = await sharp(image.Body).resize(200, 200).toBuffer();

    await s3.putObject({
      Bucket: bucket,
      Key: `thumbnails/${key}`,
      Body: resized,
    });
  }
};
```

### Fan-Out (병렬 처리)

```
SNS Topic → Lambda 1 (Email)
         → Lambda 2 (Push)
         → Lambda 3 (Analytics)
```

### Saga Pattern (Step Functions)

```json
{
  "StartAt": "ReserveInventory",
  "States": {
    "ReserveInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:reserveInventory",
      "Next": "ProcessPayment",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "ReleaseInventory"
      }]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:processPayment",
      "Next": "CompleteOrder",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "RefundPayment"
      }]
    },
    "CompleteOrder": { "Type": "Succeed" },
    "ReleaseInventory": { "Type": "Task", "Resource": "...", "Next": "FailState" },
    "RefundPayment": { "Type": "Task", "Resource": "...", "Next": "ReleaseInventory" },
    "FailState": { "Type": "Fail" }
  }
}
```

---

## 환경 변수 & Secrets

### SSM Parameter Store

```yaml
provider:
  environment:
    DB_HOST: ${ssm:/myapp/db/host}
    DB_PASSWORD: ${ssm:/myapp/db/password~true}  # SecureString
```

### Secrets Manager

```javascript
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

let cachedSecret;
const getSecret = async () => {
  if (!cachedSecret) {
    const client = new SecretsManager();
    const { SecretString } = await client.getSecretValue({ SecretId: 'myapp/db' });
    cachedSecret = JSON.parse(SecretString);
  }
  return cachedSecret;
};
```

---

## VPC 연결

```yaml
provider:
  vpc:
    securityGroupIds:
      - sg-xxx
    subnetIds:
      - subnet-xxx  # Private Subnet

functions:
  dbAccess:
    handler: handler.main
    vpc:
      securityGroupIds:
        - sg-xxx
      subnetIds:
        - subnet-xxx
```

**주의**: VPC 연결 시 콜드 스타트 +1~2초 추가. NAT Gateway 필요 (외부 통신).

---

## 비용 최적화

### 메모리 vs 비용

| 메모리 | vCPU | 비용/ms | 실행시간 | 총 비용 |
|--------|------|---------|---------|---------|
| 128MB | 0.08 | 낮음 | 길다 | 높을 수 있음 |
| 1024MB | 0.6 | 중간 | 중간 | **최적** |
| 3008MB | 2 | 높음 | 짧다 | 빠름 필요시 |

**권장**: 1024MB로 시작, Lambda Power Tuning으로 최적화.

### AWS Lambda Power Tuning

```bash
# SAR 앱 배포 후
aws lambda invoke --function-name powerTuning \
  --payload '{"lambdaARN":"arn:aws:lambda:...","num":10,"powerValues":[128,256,512,1024]}' \
  output.json
```

### Reserved Concurrency

```yaml
functions:
  api:
    handler: handler.main
    reservedConcurrency: 100  # 최대 100개 동시 실행
```

---

## Monitoring

### CloudWatch Metrics

| 메트릭 | 알림 기준 |
|--------|----------|
| `Errors` | > 0 |
| `Duration` | > timeout의 80% |
| `Throttles` | > 0 |
| `ConcurrentExecutions` | > 80% of limit |

### X-Ray Tracing

```yaml
provider:
  tracing:
    lambda: true
    apiGateway: true
```

```javascript
import AWSXRay from 'aws-xray-sdk-core';
import AWS from 'aws-sdk';

const dynamodb = AWSXRay.captureAWSClient(new AWS.DynamoDB.DocumentClient());
```

### Structured Logging

```javascript
import { Logger } from '@aws-lambda-powertools/logger';

const logger = new Logger({ serviceName: 'user-service' });

export const handler = async (event) => {
  logger.info('Processing request', { userId: event.pathParameters.id });
  // ...
};
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| 핸들러 안에서 DB 연결 | 핸들러 밖에서 연결 재사용 |
| 동기적 순차 호출 | `Promise.all`로 병렬 처리 |
| VPC 무조건 사용 | 필요한 경우만 (RDS 접근 등) |
| 모든 SDK import | 필요한 클라이언트만 import |
| 15분 타임아웃 의존 | Step Functions 또는 분할 |

---

## 체크리스트

### 함수 설계
- [ ] 핸들러 밖에서 초기화 (연결 재사용)
- [ ] 메모리 최적화 (Power Tuning)
- [ ] 타임아웃 적절히 설정

### 콜드 스타트
- [ ] Java: SnapStart 활성화
- [ ] Node.js: 번들 최소화, Tree Shaking
- [ ] 필요시 Provisioned Concurrency

### 운영
- [ ] X-Ray 트레이싱 활성화
- [ ] 구조화된 로깅 (Powertools)
- [ ] DLQ 설정 (비동기 이벤트)
- [ ] 알람 설정 (Errors, Throttles)

---

## 관련 Skills

- `/architecture:api-design` — REST API 설계 원칙
- `/observability:observability-otel` — OpenTelemetry 트레이싱
