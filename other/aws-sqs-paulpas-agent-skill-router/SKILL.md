---




name: aws-sqs
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Deploys managed message queues with SQS for asynchronous processing"
  decoupling services, and reliable message delivery with visibility timeout and dead-letter
  queues.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-cloudwatch, aws-lambda, aws-sns
  role: reference
  scope: infrastructure
  triggers: dead-letter queue, fifo queue, message deduplication, message queue, queue,
    queuing, sqs, visibility timeout
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# SQS (Simple Queue Service)

Deploy managed message queues for asynchronous processing with guaranteed delivery, visibility timeout, and built-in dead-letter queue support.

## TL;DR Checklist

- [ ] Use FIFO queue when message order is critical
- [ ] Use Standard queue for high throughput when order doesn't matter
- [ ] Configure visibility timeout appropriately (match processing time)
- [ ] Enable message deduplication for FIFO
- [ ] Set up dead-letter queue for poison pill messages
- [ ] Use short polling to reduce costs (default)
- [ ] Encrypt messages with KMS for sensitive data
- [ ] Monitor queue depth and processing time
- [ ] Set message retention appropriately (4 days default)
- [ ] Use batch operations for better performance

---

## When to Use

Use SQS when:

- Decoupling producers and consumers
- Building asynchronous processing pipelines
- Implementing reliable message delivery
- Handling traffic spikes with queuing
- Processing messages in order (FIFO)
- Retrying failed operations

---

## When NOT to Use

Avoid SQS when:

- Requiring real-time processing (< 1 second latency)
- Need pub/sub broadcast (use SNS instead)
- Strict ordering not needed but throughput critical (SNS cheaper)

---

## Purpose and Use Cases

**Primary Purpose:** Provide reliable asynchronous message delivery with automatic scaling, deduplication, and failure handling.

**Common Use Cases:**

1. **Async Job Processing** — Background tasks, image resizing, reports
2. **Service Decoupling** — Decouple order service from email service
3. **Rate Limiting** — Queue traffic to prevent downstream overload
4. **Retry Logic** — Automatic retries via visibility timeout
5. **Batch Processing** — Accumulate messages for batch processing
6. **Data Pipelines** — Multi-stage processing workflows

---

## Architecture Design Patterns

### Pattern 1: Standard Queue with Dead-Letter Queue

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # Dead-Letter Queue
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: processing-dlq
      MessageRetentionPeriod: 1209600  # 14 days
      VisibilityTimeout: 300
      KmsMasterKeyId: alias/aws/sqs  # Encryption

  # Main Processing Queue
  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: processing-queue
      VisibilityTimeout: 300  # 5 minutes
      MessageRetentionPeriod: 345600  # 4 days
      ReceiveMessageWaitTimeSeconds: 10  # Long polling
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3  # Move to DLQ after 3 failures
      KmsMasterKeyId: alias/aws/sqs

  # Queue Policy
  QueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues:
        - !Ref ProcessingQueue
      PolicyText:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: sns.amazonaws.com
            Action: sqs:SendMessage
            Resource: !GetAtt ProcessingQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: arn:aws:sns:*:*:*
          - Effect: Allow
            Principal:
              AWS: arn:aws:iam::123456789012:role/ApplicationRole
            Action:
              - sqs:SendMessage
              - sqs:ReceiveMessage
              - sqs:DeleteMessage
              - sqs:GetQueueAttributes
            Resource: !GetAtt ProcessingQueue.Arn
          - Effect: Deny
            Principal: '*'
            Action: sqs:*
            Resource: !GetAtt ProcessingQueue.Arn
            Condition:
              Bool:
                aws:SecureTransport: 'false'

  # Lambda Processor
  ProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: queue-processor
      Runtime: python3.11
      Handler: index.handler
      Role: !GetAtt ProcessorRole.Arn
      Timeout: 300
      Code:
        ZipFile: |
          import json
          import boto3
          import logging
          
          logger = logging.getLogger()
          
          def handler(event, context):
              sqs = boto3.client('sqs')
              
              for record in event['Records']:
                  try:
                      message_body = json.loads(record['body'])
                      logger.info(f"Processing: {message_body}")
                      
                      # Business logic here
                      process_message(message_body)
                      
                      # Delete on success
                      sqs.delete_message(
                          QueueUrl=record['eventSourceARN'],
                          ReceiptHandle=record['receiptHandle']
                      )
                      
                  except Exception as e:
                      logger.error(f"Failed to process: {str(e)}")
                      # On error, message stays in queue for retry
                      raise
              
              return {'statusCode': 200}
          
          def process_message(message):
              # Business logic
              pass

  ProcessorRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: SQSAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - sqs:ReceiveMessage
                  - sqs:DeleteMessage
                  - sqs:GetQueueAttributes
                  - sqs:ChangeMessageVisibility
                Resource: !GetAtt ProcessingQueue.Arn
              - Effect: Allow
                Action:
                  - kms:Decrypt
                Resource: !Sub 'arn:aws:kms:${AWS::Region}:${AWS::AccountId}:key/*'

  # Event Source Mapping
  EventSourceMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt ProcessingQueue.Arn
      FunctionName: !Ref ProcessorFunction
      BatchSize: 10
      MaximumBatchingWindowInSeconds: 5
      FunctionResponseTypes:
        - ReportBatchItemFailures
      ScalingConfig:
        MaximumConcurrency: 10

  # CloudWatch Alarms
  QueueDepthAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: sqs-queue-depth-high
      MetricName: ApproximateNumberOfMessagesVisible
      Namespace: AWS/SQS
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 1000
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: QueueName
          Value: !GetAtt ProcessingQueue.QueueName

  DLQDepthAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: sqs-dlq-not-empty
      MetricName: ApproximateNumberOfMessagesVisible
      Namespace: AWS/SQS
      Statistic: Average
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: QueueName
          Value: !GetAtt DeadLetterQueue.QueueName

  ProcessingTimeAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: sqs-message-age-high
      MetricName: ApproximateAgeOfOldestMessage
      Namespace: AWS/SQS
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 600  # 10 minutes
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: QueueName
          Value: !GetAtt ProcessingQueue.QueueName

Outputs:
  QueueUrl:
    Value: !Ref ProcessingQueue
    Description: Queue URL
  QueueArn:
    Value: !GetAtt ProcessingQueue.Arn
    Description: Queue ARN
  DLQUrl:
    Value: !Ref DeadLetterQueue
    Description: Dead-Letter Queue URL
```

**Key Elements:**
- Standard queue for high throughput
- Dead-letter queue for failed messages
- Long polling (10s) to reduce costs
- Visibility timeout matches processing time
- Message deduplication via timestamp
- KMS encryption
- Lambda with batch processing
- Alarms for queue depth and age

### Pattern 2: FIFO Queue for Ordered Processing

```yaml
Resources:
  # FIFO Queue (message order guaranteed)
  OrderQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: order-processing.fifo
      FifoQueue: true
      ContentBasedDeduplication: false  # Explicit IDs preferred
      VisibilityTimeout: 300
      MessageRetentionPeriod: 345600
      ReceiveMessageWaitTimeSeconds: 10
      DeduplicationScope: messageGroup  # Dedup per group
      FifoThroughputLimit: perMessageGroupId

  # FIFO Dead-Letter Queue
  OrderDLQ:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: order-dlq.fifo
      FifoQueue: true
      ContentBasedDeduplication: true
      MessageRetentionPeriod: 1209600

  # Link DLQ
  OrderQueueWithDLQ:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: order-queue.fifo
      FifoQueue: true
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt OrderDLQ.Arn
        maxReceiveCount: 3
```

**Key Elements:**
- FIFO queue for strict ordering
- MessageGroupId for partitioning (same group = same order)
- ContentBasedDeduplication for automatic dedup
- Deduplication scope per group
- Throughput limit per message group

### Pattern 3: Batch Processing with Visibility Adjustment

```yaml
Resources:
  # Batch Processing Lambda
  BatchProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: batch-processor
      Runtime: python3.11
      Handler: index.handler
      Timeout: 600  # 10 minutes for batch
      Code:
        ZipFile: |
          import boto3
          import json
          from datetime import datetime, timedelta
          
          sqs = boto3.client('sqs')
          
          def handler(event, context):
              queue_url = event['QueueUrl']
              
              # Receive batch of messages
              response = sqs.receive_message(
                  QueueUrl=queue_url,
                  MaxNumberOfMessages=10,
                  WaitTimeSeconds=10
              )
              
              messages = response.get('Messages', [])
              
              try:
                  # Process batch
                  process_batch(messages)
                  
                  # Delete processed messages
                  for msg in messages:
                      sqs.delete_message(
                          QueueUrl=queue_url,
                          ReceiptHandle=msg['ReceiptHandle']
                      )
                  
              except Exception as e:
                  # Extend visibility for slower processing
                  for msg in messages:
                      sqs.change_message_visibility(
                          QueueUrl=queue_url,
                          ReceiptHandle=msg['ReceiptHandle'],
                          VisibilityTimeout=600  # +10 minutes
                      )
                  raise
              
              return {'processed': len(messages)}
          
          def process_batch(messages):
              # Batch processing logic
              pass
```

**Key Elements:**
- Batch receive for efficiency
- Dynamic visibility adjustment
- Graceful failure handling
- Message deletion on success

---

## Integration Approaches

### 1. Integration with Lambda

Lambda + SQS enables:
- Event-driven processing
- Batch message handling
- Automatic scaling

### 2. Integration with SNS

SNS + SQS enables:
- Fan-out pattern
- Persistence layer
- Multiple consumers

### 3. Integration with Application Load Balancer

ALB + SQS enables:
- HTTP request queueing
- Backend decoupling
- Request buffering

---

## Common Pitfalls

### ❌ Pitfall 1: Visibility Timeout Too Short

**Problem:** Messages re-delivered before processing completes; duplicates.

**Solution:**
- Set to match longest processing time
- Use change_message_visibility if processing slower

### ❌ Pitfall 2: No Dead-Letter Queue

**Problem:** Poison pill messages cause infinite retries.

**Solution:**
- Configure DLQ with maxReceiveCount
- Monitor DLQ for failures

### ❌ Pitfall 3: Long Polling Disabled

**Problem:** Empty responses waste API calls; high costs.

**Solution:**
- Enable long polling (WaitTimeSeconds = 10s)
- Reduces API call costs by 80%+

### ❌ Pitfall 4: Not Deleting Processed Messages

**Problem:** Messages re-delivered indefinitely.

**Solution:**
- Always delete on successful processing
- Only delete after message handle no longer valid

### ❌ Pitfall 5: FIFO for Non-Ordered Workloads

**Problem:** FIFO throughput limited (300 msg/s per group).

**Solution:**
- Use Standard queue for high throughput
- FIFO only when order matters

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Queue Type** | Standard for throughput; FIFO for order |
| **Visibility** | Match to processing time; adjust dynamically |
| **Reliability** | Dead-letter queue; batch failure reporting |
| **Performance** | Long polling; batch receives; 10+ messages |
| **Monitoring** | Queue depth; message age; DLQ depth |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-sns` | Fan-out to multiple queues |
| `cncf-aws-lambda` | Event source for queue processing |
| `cncf-aws-cloudwatch` | Queue monitoring and alarms |
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests

---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- [Configuration Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-timing.html)
- [Best Practices](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-scheduled-concurrency-for-lambda-functions.html)

