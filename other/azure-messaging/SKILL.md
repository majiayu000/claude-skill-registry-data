---
name: azure-messaging
description: >
  Design asynchronous messaging patterns in Azure using Service Bus, Event Hubs, Event Grid, and Storage Queues.
  Use this skill when users ask for queueing, pub-sub, event streaming, retries, or decoupled system design.
  Covers delivery semantics, dead-lettering, idempotency, and monitoring.
compatibility:
  models: [any-llm]
  cloud: azure
  patterns: [pub-sub, queue, event-streaming, saga]
---

# Azure Messaging

Choose the right Azure messaging service and delivery semantics for reliable, decoupled, event-driven systems.
Handle retries, failures, and exactly-once processing.

## Use This Skill When

- The user needs asynchronous processing design (commands, events, streams)
- The user asks about retries, dead-lettering, idempotency, or ordering
- The user needs to decouple systems via events or messaging
- The user needs high-throughput streaming or reactive patterns

## Context: Messaging Maturity

**Immature**: Synchronous API calls, no retries, tightly coupled  
**Developing**: Simple queues created, basic retry logic  
**Managed**: Service Bus/Event Hub with DLQ, idempotency, monitoring → **Target**  
**Optimized**: Saga pattern for distributed transactions, stream processing, real-time analytics

## Required Inputs

- **Message pattern**: Command (request-response), Event (pub-sub), Stream (high-volume telemetry)
- **Throughput**: 100 msg/sec? 1M msg/sec?
- **Latency**: <1sec? Batch processing acceptable?
- **Delivery guarantee**: At most once? At least once? Exactly once?
- **Ordering requirement**: FIFO per partition? Or unordered?
- **Consumer pattern**: Single consumer? Multiple competing consumers? Fan-out?
- **Scale**: Number of producers, consumers, message size?

## Decision Tree

```
What is the main use case?
├─ Simple queue (deferred processing) → Storage Queues (cheapest, simple)
├─ Enterprise queue (retries, DLQ, partitioning) → Service Bus Queue
├─ Publish-Subscribe (fan-out) → Service Bus Topic or Event Grid
├─ High-volume streaming (1000+ msg/sec) → Event Hubs
└─ Reactive events (webhooks, triggers) → Event Grid

What's the throughput target?
├─ <1000 msg/sec → Storage Queues or Service Bus
├─ 1000-10,000 msg/sec → Service Bus with partitions
├─ > 10,000 msg/sec → Event Hubs
└─ Needs low latency (<100ms) → Event Hubs or Service Bus Premium

Do you need ordering or exactly-once semantics?
├─ Yes, FIFO per partition → Event Hubs or Service Bus with sessions
├─ Yes, exactly-once → Service Bus with deduplication ID
└─ No, at-least-once acceptable → Any service + idempotency in handler

How many consumers need this message?
├─ One → Queue (Service Bus or Storage)
├─ Multiple (fan-out) → Service Bus Topic or Event Grid
└─ Streams (continuous analytics) → Event Hubs
```

## Workflow

### Phase 1: Service Selection

| Service | Use Case | Throughput | Ordering | Features |
|---------|----------|-----------|----------|----------|
| **Storage Queues** | Simple, cheap | <2K msg/sec | No | TTL, visibility timeout |
| **Service Bus Queue** | Enterprise, retries | Up to 2K msg/sec | FIFO (sessions) | DLQ, dedup, TTL, auth |
| **Service Bus Topic** | Pub-Sub, fan-out | Up to 2K msg/sec | No | Subscriptions, filters |
| **Event Hubs** | Streaming, telemetry | 1M+ msg/sec | Per partition | Consumer groups, retention |
| **Event Grid** | Reactive, webhooks | Millions/sec | No | Built-in integrations |

### Phase 2: Create Messaging Infrastructure

1. **Service Bus Queue** (for command processing):
   ```bash
   az servicebus queue create \
     --namespace-name "sb-${app}-${env}" \
     --resource-group $RG \
     --name "order-processing" \
     --max-delivery-count 10 \
     --duplicate-detection-history-time-window "PT5M" \
     --dead-letter-on-filter-evaluation-error \
     --dead-letter-on-message-expiration
   
   # Max retries: 10, then DLQ
   # Dedup window: 5 minutes (for idempotency)
   # Auto DLQ on TTL expiration
   ```

2. **Service Bus Topic** (for event distribution):
   ```bash
   az servicebus topic create \
     --namespace-name "sb-${app}-${env}" \
     --resource-group $RG \
     --name "order-events" \
     --enable-subscriptions true
   
   # Create subscription (consumer group)
   az servicebus topic subscription create \
     --namespace-name "sb-${app}-${env}" \
     --resource-group $RG \
     --topic-name "order-events" \
     --name "email-service" \
     --max-delivery-count 3 \
     --dead-letter-on-filter-evaluation-error
   
   # Different consumers listen on same topic via subscriptions
   ```

3. **Event Hubs** (for streaming):
   ```bash
   az eventhubs eventhub create \
     --namespace-name "eh-${app}-${env}" \
     --resource-group $RG \
     --name "telemetry" \
     --partition-count 4 \
     --message-retention 1 \
     --enable-capture true \
     --capture-interval-in-seconds 300 \
     --capture-size-limit-in-bytes 314572800
   
   # 4 partitions for 4 concurrent consumers
   # Capture to storage every 5 minutes or 300MB
   ```

### Phase 3: Send Messages

1. **Produce to Service Bus Queue**:
   ```csharp
   // .NET
   var client = new ServiceBusClient(connectionString);
   var sender = client.CreateSender("order-processing");
   
   var message = new ServiceBusMessage("Order 123");
   message.MessageId = "order-123";  // For deduplication
   message.TimeToLive = TimeSpan.FromMinutes(5);  // Auto-DLQ if not processed
   message.ApplicationProperties["OrderId"] = "123";
   
   await sender.SendMessageAsync(message);
   ```

2. **Publish to Event Hub**:
   ```csharp
   // .NET
   var producer = new EventHubProducerClient(connectionString, "telemetry");
   
   var batch = await producer.CreateBatchAsync();
   batch.TryAdd(new EventData(new BinaryData("temperature=72.5")));
   batch.TryAdd(new EventData(new BinaryData("humidity=45%")));
   
   await producer.SendAsync(batch);
   ```

### Phase 4: Consume & Handle Failures

1. **Consume with retry and DLQ**:
   ```csharp
   // .NET
   var client = new ServiceBusClient(connectionString);
   var processor = client.CreateProcessor("order-processing");
   
   processor.ProcessMessageAsync += async args => {
     try {
       var message = args.Message;
       var orderId = message.ApplicationProperties["OrderId"];
       
       // Idempotency check
       if (await database.OrderProcessed(orderId)) {
         await args.CompleteMessageAsync(message);
         return;
       }
       
       // Process order
       await ProcessOrder(orderId);
       await args.CompleteMessageAsync(message);
     } catch (Exception ex) {
       // Retry automatically (up to max-delivery-count)
       // After max retries, goes to DLQ
       throw;  // Nack, retry
     }
   };
   
   processor.ProcessErrorAsync += args => {
     Console.WriteLine($"Error: {args.Exception}");
     return Task.CompletedTask;
   };
   
   await processor.StartProcessingAsync();
   ```

2. **Monitor DLQ** (failed messages):
   ```bash
   # Peek at DLQ
   az servicebus queue peek \
     --namespace-name "sb-${app}-${env}" \
     --resource-group $RG \
     --name "order-processing/$DeadLetterQueue"
   ```

### Phase 5: Ensure Exactly-Once Processing (Idempotency)

1. **Deduplication ID** (Service Bus):
   ```
   Message A sent with MessageId="order-123"
   ├─ First delivery: Processed ✓
   ├─ Retry (within 5-min window): Not reprocessed (dedup)
   └─ After 5 min: Can send again (different transaction)
   ```

2. **Idempotency key in handler** (Event Hub, Storage Queue):
   ```python
   # Python
   def process_order(event):
       order_id = event['OrderId']
       
       # Check if already processed
       if db.query(f"SELECT * FROM processed_orders WHERE order_id = {order_id}"):
           return  # Already done, idempotent
       
       # Process
       db.insert("orders", {"id": order_id, "status": "processing"})
       # ... fulfill order ...
       db.insert("processed_orders", {"order_id": order_id, "timestamp": now()})
   ```

### Phase 6: Scaling & Partitioning

1. **Service Bus (sharding via topics/queues)**:
   ```
   Instead of: Single queue "orders" (bottleneck at scale)
   Use: 10 queues: "orders-0", "orders-1", ..., "orders-9"
   
   Producer hashes order_id % 10 → routes to specific queue
   Consumers: One per queue for parallelism
   ```

2. **Event Hubs (partitions)**:
   ```bash
   # 4 partitions = 4 independent streams
   # Each consumer group member gets 1 partition
   # Max throughput: ~1M events/sec with 32 partitions
   
   # Each partition maintains ordering FIFO per session_id
   ```

### Phase 7: Monitoring & Alerting

1. **Setup monitoring**:
   ```bash
   az monitor metrics list \
     --resource-group $RG \
     --resource-type "Microsoft.ServiceBus/namespaces" \
     --resource-id "sb-${app}-${env}" \
     --metric "ActiveMessageCount,DeadletteredMessageCount"
   ```

2. **Alerts**:
   - Active message count > 10,000 (backlog building)
   - Dead-lettered message count > 0 (failures happening)
   - Consumer lag > 1 hour (consumer slow/stopped)
   - Message age > TTL (about to expire)

## Output Contract

1. **Messaging Architecture**
   - Service chosen (Queue, Topic, Event Hub)
   - Number of queues/topics, partitions
   - Consumer count and groups

2. **Delivery & Ordering Design**
   - Delivery guarantee: At most once, at least once, exactly once
   - Ordering requirements (FIFO per partition? Global?)
   - Idempotency strategy (dedup ID, business key check)

3. **Failure Handling**
   - Max retries before DLQ
   - DLQ monitoring and remediation process
   - Message TTL (time to live)

4. **Configuration & Access**
   - Connection strings or managed identity scopes
   - Queue/topic names and subscription details
   - Retention policy (1-30 days)

5. **Operations Checklist**
   - Alerts configured for backlog, lag, DLQ
   - DLQ monitoring and replay procedure
   - Capacity planning (throughput targets)

## Guardrails

- **Always define a DLQ**: Dead-lettered messages need handling (manual replay or archive).
- **Implement idempotency**: Assume messages arrive >1 time; handle gracefully.
- **Use TTL (time-to-live)**: Prevent stale messages; auto-expire to DLQ.
- **Monitor backlog**: If active message count grows, consumer is slow.
- **Partition for scale**: Don't use single queue for >2K msg/sec.
- **Log message content (redacted)**: Include order ID, not full message body (size/privacy).
- **Test failure scenarios**: What if consumer crashes mid-processing? Does DLQ work?
- **Avoid coupling**: Producers and consumers should not know each other.
