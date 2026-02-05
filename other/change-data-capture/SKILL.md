---
name: Change Data Capture (CDC)
description: Capturing and streaming database changes in real-time using Debezium, Kafka, and event-driven patterns for data synchronization.
---

# Change Data Capture (CDC)

## Overview

Change Data Capture (CDC) คือเทคนิคการ capture changes จาก database และ stream ไปยัง downstream systems แบบ real-time ใช้สำหรับ data replication, event sourcing, cache invalidation, และ building real-time analytics

## Why This Matters

- **Real-time Sync**: Data available in seconds, not hours
- **Low Impact**: Reads from transaction log, minimal database load
- **Reliable**: Captures all changes including deletes
- **Event-Driven**: Enable reactive architectures

---

## Core Concepts

### 1. Debezium with Kafka Connect

```yaml
# docker-compose.yml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    ports: ['9092:9092']
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  connect:
    image: debezium/connect:2.4
    depends_on: [kafka]
    ports: ['8083:8083']
    environment:
      BOOTSTRAP_SERVERS: kafka:29092
      GROUP_ID: connect-cluster
      CONFIG_STORAGE_TOPIC: connect-configs
      OFFSET_STORAGE_TOPIC: connect-offsets
      STATUS_STORAGE_TOPIC: connect-status
```

### 2. PostgreSQL Connector Configuration

```json
{
  "name": "orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${secrets:postgres-password}",
    "database.dbname": "orders_db",
    "database.server.name": "orders",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "publication.name": "dbz_publication",
    "topic.prefix": "cdc",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.unwrap.delete.handling.mode": "rewrite",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter.schemas.enable": "false"
  }
}
```

### 3. CDC Event Structure

```typescript
// Raw Debezium event
interface DebeziumEvent<T> {
  schema: object;
  payload: {
    before: T | null;      // Previous state (null for INSERT)
    after: T | null;       // New state (null for DELETE)
    source: {
      version: string;
      connector: string;
      name: string;
      ts_ms: number;
      snapshot: boolean;
      db: string;
      table: string;
      txId: number;
      lsn: number;
    };
    op: 'c' | 'u' | 'd' | 'r';  // create, update, delete, read (snapshot)
    ts_ms: number;
  };
}

// After ExtractNewRecordState transform
interface TransformedEvent<T> {
  ...T;                    // All fields from the record
  __op: 'c' | 'u' | 'd';   // Operation type
  __deleted: boolean;      // True for deletes
  __source_ts_ms: number;  // Source timestamp
}
```

### 4. Consuming CDC Events (Node.js)

```typescript
import { Kafka, EachMessagePayload } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'order-processor',
  brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({ groupId: 'order-sync-group' });

async function startConsumer() {
  await consumer.connect();
  await consumer.subscribe({ 
    topics: ['cdc.public.orders', 'cdc.public.order_items'],
    fromBeginning: false,
  });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
      const event = JSON.parse(message.value?.toString() || '{}');
      const key = JSON.parse(message.key?.toString() || '{}');
      
      console.log(`[${topic}] Operation: ${event.__op}, ID: ${key.id}`);
      
      switch (event.__op) {
        case 'c': // Create
          await handleInsert(topic, event);
          break;
        case 'u': // Update
          await handleUpdate(topic, event);
          break;
        case 'd': // Delete
          await handleDelete(topic, key);
          break;
      }
    },
  });
}

async function handleInsert(topic: string, data: any) {
  if (topic.includes('orders')) {
    await elasticsearchClient.index({
      index: 'orders',
      id: data.id,
      body: data,
    });
    await redisClient.del(`order:${data.id}`); // Invalidate cache
  }
}

async function handleUpdate(topic: string, data: any) {
  if (topic.includes('orders')) {
    await elasticsearchClient.update({
      index: 'orders',
      id: data.id,
      body: { doc: data },
    });
    await redisClient.del(`order:${data.id}`);
  }
}

async function handleDelete(topic: string, key: any) {
  if (topic.includes('orders')) {
    await elasticsearchClient.delete({
      index: 'orders',
      id: key.id,
    });
    await redisClient.del(`order:${key.id}`);
  }
}
```

### 5. Outbox Pattern

```typescript
// Instead of direct CDC, use transactional outbox
interface OutboxEvent {
  id: string;
  aggregate_type: string;
  aggregate_id: string;
  event_type: string;
  payload: object;
  created_at: Date;
}

// In your service
async function createOrder(orderData: CreateOrderDto) {
  await prisma.$transaction(async (tx) => {
    // Create order
    const order = await tx.order.create({ data: orderData });
    
    // Create outbox event (same transaction)
    await tx.outboxEvent.create({
      data: {
        id: uuid(),
        aggregate_type: 'Order',
        aggregate_id: order.id,
        event_type: 'OrderCreated',
        payload: order,
      },
    });
    
    return order;
  });
}

// Debezium captures from outbox table
// Then delete processed events periodically
```

## Quick Start

1. **Start infrastructure:**
   ```bash
   docker-compose up -d
   ```

2. **Enable logical replication (PostgreSQL):**
   ```sql
   ALTER SYSTEM SET wal_level = logical;
   -- Restart PostgreSQL
   ```

3. **Create publication:**
   ```sql
   CREATE PUBLICATION dbz_publication FOR TABLE orders, order_items;
   ```

4. **Register connector:**
   ```bash
   curl -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d @postgres-connector.json
   ```

5. **Verify topics:**
   ```bash
   kafka-topics --list --bootstrap-server localhost:9092
   ```

6. **Start consuming events**

## Production Checklist

- [ ] Dedicated replication slot with monitoring
- [ ] Schema registry for event evolution
- [ ] Dead letter queue for failed events
- [ ] Exactly-once semantics configured
- [ ] Connector monitoring and alerting
- [ ] Slot lag monitoring (prevent WAL bloat)
- [ ] Idempotent consumers
- [ ] Snapshot strategy defined
- [ ] Data masking for sensitive fields

## Anti-patterns

1. **Ignoring Schema Evolution**: Use Schema Registry and compatible changes
2. **No Idempotency**: Consumers must handle duplicate events
3. **Unbounded Replication Slots**: Monitor and clean up stale slots
4. **Large Payloads**: Consider references instead of full documents

## Integration Points

- **Elasticsearch**: Real-time search indexing
- **Redis**: Cache invalidation
- **Data Warehouse**: Real-time ETL to Snowflake/BigQuery
- **Event Sourcing**: Build event stores
- **Microservices**: Cross-service data sync

## Further Reading

- [Debezium Documentation](https://debezium.io/documentation/)
- [CDC Patterns](https://debezium.io/documentation/reference/stable/architecture.html)
- [Outbox Pattern](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
