---
name: aws-advanced-patterns
category: cloud-native
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
- serverless
- cloud-concepts
- aws-fundamentals
tags:
- aws
- step-functions
- eventbridge
- lambda-layers
- dynamodb
- observability
version: 1.0.0
description: 'Orchestration & Events:'
---


# AWS Advanced Patterns

Master advanced AWS serverless architectures, event-driven patterns, and enterprise-grade cloud solutions.

## Level 1: Quick Reference

### AWS Advanced Services Overview

**Orchestration & Events:**

- **Step Functions**: State machine orchestration for complex workflows
- **EventBridge**: Serverless event bus for event-driven architectures
- **Lambda Layers**: Shared code and dependencies across functions

**Data & Storage:**

- **DynamoDB Advanced**: Single-table design, streams, global tables
- **S3 Advanced**: Event notifications, object lifecycle, intelligent tiering

**Integration:**

- **API Gateway Advanced**: Custom authorizers, usage plans, WebSocket APIs
- **SQS/SNS Patterns**: FIFO queues, DLQ, fan-out, message filtering

**Observability:**

- **CloudWatch**: Custom metrics, composite alarms, insights
- **X-Ray**: Distributed tracing, service maps, annotations

### Common Patterns Quick Reference

```yaml
# Event-Driven Architecture
Pattern: Publisher → EventBridge → Subscribers
Use Case: Microservices decoupling, cross-account events
Key Services: EventBridge, Lambda, SQS

# Orchestrated Workflow
Pattern: API → Step Functions → Lambda/Services
Use Case: Multi-step processes, saga pattern, ETL
Key Services: Step Functions, Lambda, DynamoDB

# Fan-Out Processing
Pattern: SNS Topic → Multiple SQS Queues → Lambda
Use Case: Parallel processing, multi-tenant systems
Key Services: SNS, SQS, Lambda

# CQRS Pattern
Pattern: Write DB → DynamoDB Streams → Read DB
Use Case: Read/write separation, materialized views
Key Services: DynamoDB Streams, Lambda, ElastiCache

# Saga Pattern
Pattern: Step Functions → Compensating Transactions
Use Case: Distributed transactions, rollback logic
Key Services: Step Functions, Lambda, DynamoDB
```

### Essential Checklist

**Security:**

- [ ] IAM least privilege policies (resource-level permissions)
- [ ] Secrets Manager for credentials (automatic rotation)
- [ ] VPC endpoints for private connectivity
- [ ] Encryption at rest and in transit
- [ ] WAF rules for API Gateway

**Cost Optimization:**

- [ ] Lambda reserved concurrency for predictable workloads
- [ ] DynamoDB on-demand vs provisioned capacity
- [ ] S3 Intelligent-Tiering for variable access patterns
- [ ] CloudWatch Logs retention policies
- [ ] Cost allocation tags for all resources

**Reliability:**

- [ ] Multi-AZ deployments
- [ ] Dead-letter queues (DLQ) for failed messages
- [ ] Circuit breakers in Step Functions
- [ ] Exponential backoff with jitter
- [ ] Chaos engineering tests

**Observability:**

- [ ] X-Ray tracing enabled on all Lambda functions
- [ ] Custom CloudWatch metrics for business KPIs
- [ ] Structured logging (JSON format)
- [ ] Distributed tracing correlation IDs
- [ ] Alarms for error rates and latency

---

## Level 2: Implementation Guide

> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

### API Gateway Advanced Patterns

**Custom Authorizers** - Lambda functions that validate tokens/API keys before allowing API access.

- **JWT Authorizer** - Verify JWT tokens, return IAM policy + context
- **Request Authorizer** - Validate custom headers, IP whitelist, API keys

**Usage Plans & Rate Limiting:**

- Throttle: Burst (max concurrent), Rate (requests/second)
- Quota: Monthly/daily limits per API key
- Associate API keys with usage plans

**VTL Mapping Templates** - Transform request/response without Lambda:

- Add `$context` variables (requestId, authorizer data, sourceIP)
- Access `$input` for payload manipulation
- Use for legacy system integration

See [REFERENCE.md](./REFERENCE.md) for authorizer implementations, VTL examples, and WebSocket APIs.

---

### DynamoDB Advanced Patterns

**Single-Table Design** - Store multiple entity types in one table using composite keys.

**Key Strategy:**

- `PK` (Partition Key): Entity type + ID (e.g., `USER#123`, `ORDER#456`)
- `SK` (Sort Key): Relationship or sub-entity (e.g., `PROFILE`, `ORDER#2024-01-15`)
- GSI for alternate access patterns (e.g., query by email, status)

**Common Patterns:**

- 1:N relationships - Same PK, different SK prefixes
- N:N relationships - Inverted index with GSI
- Hierarchical data - SK with begins_with queries

**DynamoDB Streams** - Capture changes (INSERT/MODIFY/REMOVE) for:

- Materialized views
- Cross-region replication
- Analytics/auditing
- Event-driven workflows

**Transactions** - ACID operations across up to 100 items:

- `TransactWriteItems` - Atomic writes with conditions
- `TransactGetItems` - Consistent reads
- Use for fund transfers, inventory management

See [REFERENCE.md](./REFERENCE.md) for complete access patterns, stream processors, and transaction examples.

---

### SQS/SNS Messaging Patterns

**FIFO Queues** - Guarantee ordering and exactly-once processing:

- `MessageGroupId` - Messages with same ID processed in order
- `MessageDeduplicationId` - Prevents duplicates (5-minute window)
- Throughput: 300 TPS (batching: 3,000 TPS)

**Fan-Out Pattern** (SNS → Multiple SQS):

- Publish once to SNS topic
- Multiple SQS queues subscribe with filter policies
- Each subscriber processes independently
- Use for microservices decoupling

**Dead-Letter Queues (DLQ):**

- Capture messages that fail after `maxReceiveCount` attempts
- Analyze failure patterns
- Replay after fixing root cause

**Best Practices:**

- Idempotent processing (track message IDs in DB)
- Exponential backoff for retries
- Monitor DLQ depth with CloudWatch alarms
- Use long polling (20s) to reduce empty receives

See [REFERENCE.md](./REFERENCE.md) for FIFO queue setup, SNS filter policies, and DLQ consumers.

---

### Cost Optimization Strategies

**Lambda:**

- Right-size memory (use AWS Lambda Power Tuning tool)
- Use ARM64 (Graviton2) for 20% cost reduction
- Reserved concurrency for predictable workloads
- Reduce cold starts with provisioned concurrency

**DynamoDB:**

- On-demand vs provisioned capacity analysis
- Auto-scaling for variable workloads
- DAX (DynamoDB Accelerator) for read-heavy apps
- Delete old data with TTL (no write cost)

**S3:**

- Intelligent-Tiering for variable access patterns
- Lifecycle policies (Standard → IA → Glacier → Deep Archive)
- Delete incomplete multipart uploads
- Request metrics to optimize access patterns

**General:**

- CloudWatch Logs retention policies (default: never expire)
- Use Cost Explorer and Budget alerts
- Tag all resources for cost allocation
- Enable Cost Anomaly Detection

See [REFERENCE.md](./REFERENCE.md) for auto-scaling configs, lifecycle policies, and cost analysis scripts.

---

### Observability and Monitoring

**X-Ray Distributed Tracing:**

- Instrument AWS SDK calls automatically
- Add subsegments for custom operations
- Annotations (indexed) for filtering traces
- Metadata (not indexed) for debugging context

**CloudWatch Custom Metrics (EMF):**

- Embedded Metric Format - log-based metrics (no PutMetricData API calls)
- Custom dimensions for business KPIs
- Composite alarms (AND/OR logic across multiple alarms)

**Structured Logging:**

```javascript
console.log(JSON.stringify({
  level: 'INFO',
  message: 'Order processed',
  orderId, customerId,
  timestamp: new Date().toISOString()
}));
```

**Best Practices:**

- Correlation IDs across service boundaries
- Log sampling for high-volume endpoints
- Use CloudWatch Insights for log analysis
- Set up dashboards for key metrics (latency, errors, throttles)

See [REFERENCE.md](./REFERENCE.md) for X-Ray instrumentation, EMF examples, and structured logger implementations.

---

## Level 3: Deep Dive Resources


### Official AWS Documentation


**Step Functions:**


- [Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)

- [State Machine Examples](https://github.com/aws-samples/aws-stepfunctions-examples)

- [Best Practices](https://docs.aws.amazon.com/step-functions/latest/dg/bp-general.html)


**EventBridge:**


- [User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)

- [Event Patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)

- [Schema Registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html)


**Lambda Layers:**


- [Working with Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)

- [Creating Layers](https://docs.aws.amazon.com/lambda/latest/dg/creating-deleting-layers.html)


**DynamoDB:**


- [Single-Table Design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html)

- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)

- [Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)


**Observability:**


- [X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)

- [CloudWatch Embedded Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html)


### Books and Courses


**Books:**


- "AWS Lambda in Action" by Danilo Poccia

- "The DynamoDB Book" by Alex DeBrie

- "Serverless Architectures on AWS" by Peter Sbarski


**Courses:**


- AWS Certified Solutions Architect Professional

- A Cloud Guru: AWS Serverless

- Linux Academy: DynamoDB Deep Dive


### Architecture Patterns


**AWS Prescriptive Guidance:**


- [Serverless Patterns Collection](https://serverlessland.com/patterns)

- [EventBridge Patterns](https://serverlessland.com/event-driven-architecture)

- [Step Functions Workflows](https://serverlessland.com/workflows)


**Reference Architectures:**


- [AWS Samples Repository](https://github.com/aws-samples)

- [Serverless Application Repository](https://serverlessrepo.aws.amazon.com/)


### Bundled Resources


See included templates and scripts:


- `templates/step-functions-state-machine.json`

- `templates/eventbridge-patterns.json`

- `templates/lambda-layer-structure/`

- `templates/dynamodb-single-table.yaml`

- `templates/custom-authorizer.js`

- `scripts/cost-optimization.py`
