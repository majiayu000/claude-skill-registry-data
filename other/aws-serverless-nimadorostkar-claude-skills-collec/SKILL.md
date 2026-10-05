---
name: aws-serverless
description: Use when building serverless systems on AWS. Covers Lambda design, cold starts, event-driven patterns with EventBridge and SQS, idempotency, step functions, and the limits that shape the architecture.
metadata:
  category: devops
  version: 1.0.0
  tags: [serverless, lambda, eventbridge, sqs, step-functions]
---

# AWS Serverless

## Purpose

Build serverless systems that handle retries and partial failure correctly. The platform will retry your function; whether that is harmless is entirely your design decision.

## When to Use

- Building event-driven or API workloads on Lambda.
- Designing an event flow with EventBridge, SQS, or Step Functions.
- Diagnosing duplicate processing, throttling, or cold-start latency.
- Deciding whether serverless is the right model at all.

## Capabilities

- Lambda design: handler structure, concurrency, memory tuning, cold starts.
- Event sources: API Gateway, EventBridge, SQS, S3, DynamoDB Streams.
- Idempotency and partial-batch failure handling.
- Orchestration with Step Functions.
- Cost and limit awareness.

## Inputs

- The workload shape: request/response, event-driven, or batch.
- Volume, burstiness, and latency requirements.
- Whether the operation is naturally idempotent.

## Outputs

- Handlers that are safe under at-least-once delivery.
- Explicit DLQs and retry configuration on every asynchronous source.
- A concurrency and memory configuration chosen by measurement.

## Workflow

1. **Assume the function will run twice** — SQS is at-least-once. EventBridge is at-least-once. Asynchronous Lambda invocations retry twice by default. Idempotency is not optional.
2. **Report partial batch failures** — With SQS batches, a single failed message re-delivers the *entire* batch unless you return `batchItemFailures`. That is how one poison message causes ten thousand duplicate side effects.
3. **Keep the handler thin** — Parse the event, call a plain function, map the result. The business logic should be testable without a Lambda context.
4. **Initialize outside the handler** — Database clients, SDK clients, and config are reused across warm invocations. Creating them per invocation is a per-request cost you pay forever.
5. **Tune memory by measurement** — Memory determines CPU. A function at 1024 MB often finishes in a third of the time of one at 256 MB, for the same or lower total cost.
6. **Set the DLQ and the alarm** — An asynchronous function without a DLQ silently discards events after its retries. You will not know.

## Best Practices

- `reportBatchItemFailures` on every SQS event-source mapping. Without it, one bad message in a batch of ten reprocesses the nine good ones on every retry.
- Set `maximumConcurrency` on the SQS event source, or a busy queue will scale Lambda until it exhausts your database connections.
- Reserved concurrency protects the rest of the account from one function's burst. Provisioned concurrency eliminates cold starts and costs money continuously — use it only on latency-critical paths.
- A Lambda in a VPC that needs internet access requires a NAT gateway. That is an hourly charge and a bandwidth charge for what looked like a free architecture.
- Step Functions is the right tool when a workflow has retries, branches, waits, or human approval. Orchestrating that in Lambda code means reimplementing a state machine, badly.
- Do not use Lambda for long-running or steady high-throughput work. At sustained load, a container on Fargate or ECS is usually both cheaper and faster.

## Examples

**SQS handler: partial batch failure plus idempotency:**

```typescript
export const handler = async (event: SQSEvent): Promise<SQSBatchResponse> => {
  const batchItemFailures: SQSBatchItemFailure[] = [];

  for (const record of event.Records) {
    try {
      const order = JSON.parse(record.body) as OrderPlaced;

      // Conditional write: the second delivery of the same event is a no-op.
      await ddb.send(new PutItemCommand({
        TableName: PROCESSED_TABLE,
        Item: { pk: { S: `event#${order.eventId}` }, ttl: { N: String(ttl(14)) } },
        ConditionExpression: "attribute_not_exists(pk)",
      }));

      await fulfil(order);
    } catch (err) {
      if (err instanceof ConditionalCheckFailedException) {
        continue;                                    // already processed: succeed silently
      }
      // Fail only this message. The rest of the batch is acknowledged.
      batchItemFailures.push({ itemIdentifier: record.messageId });
      console.error("processing failed", { messageId: record.messageId, err });
    }
  }

  return { batchItemFailures };
};
```

**Retries and DLQ declared, not assumed:**

```yaml
Resources:
  OrdersQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180              # >= 6x the function timeout
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt OrdersDlq.Arn
        maxReceiveCount: 5                # then it stops retrying and lands in the DLQ
```

## Notes

- SQS visibility timeout must be at least six times the Lambda timeout, or a slow invocation will cause the message to be re-delivered while it is still being processed — producing exactly the duplicate you were trying to avoid.
- Lambda's default asynchronous retry is two attempts with no DLQ configured by default. Events that fail three times simply vanish.
- The AWS Lambda Powertools libraries provide idempotency, batch processing, tracing, and structured logging as tested primitives. Reimplementing them by hand is a common and unnecessary source of bugs.
