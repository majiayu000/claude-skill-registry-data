---
name: event-driven-architecture
description: Event-driven architecture patterns including event sourcing, CQRS, message brokers, and event schema design. Use when designing asynchronous systems.
---

# Event-Driven Architecture

Comprehensive guidance on building event-driven systems, covering event sourcing, CQRS, message broker selection (Kafka, RabbitMQ, NATS), event schema design with CloudEvents, saga patterns, idempotency, and strategies for event versioning and evolution.

## When to Use This Skill

Use this skill for:

- Designing publish/subscribe or event streaming systems
- Implementing event sourcing with an event store
- Applying CQRS to separate read and write models
- Choosing between Kafka, RabbitMQ, AWS SNS/SQS, and NATS
- Implementing the saga pattern (orchestration or choreography)
- Designing event schemas with CloudEvents, Avro, or Protobuf
- Handling idempotency and exactly-once semantics
- Managing dead letter queues and event replay
- Versioning events without breaking consumers

**Trigger phrases**: "event-driven", "event sourcing", "CQRS", "message broker", "Kafka", "RabbitMQ", "pub/sub", "saga pattern", "event store", "dead letter queue", "event schema", "CloudEvents", "eventual consistency"

## What This Skill Does

Provides production-ready event-driven patterns including:

- **Core Patterns**: Pub/sub, event streaming, event sourcing, CQRS
- **Broker Selection**: Feature comparison and trade-offs for Kafka, RabbitMQ, NATS, SNS/SQS
- **Schema Design**: CloudEvents format, Avro schemas, schema registry, event versioning
- **Reliability**: Idempotency, outbox pattern, dead letter queues, exactly-once semantics
- **Orchestration**: Saga pattern (orchestrator-based and choreography-based)
- **Operations**: Consumer groups, partitioning, replay, monitoring

## Instructions

### Step 1: Understand Event-Driven Patterns

```
┌────────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN PATTERNS                          │
├──────────────────┬──────────────────┬──────────────────────────────┤
│    PUB/SUB       │ EVENT STREAMING  │    EVENT SOURCING            │
│                  │                  │                              │
│  Fire-and-forget │  Ordered log of  │  Persist all state changes   │
│  message         │  events with     │  as events; derive current   │
│  broadcasting    │  consumer replay │  state by replaying          │
│                  │                  │                              │
│  Use: notifs,    │  Use: data       │  Use: audit, undo, temporal  │
│  webhooks,       │  pipelines,      │  queries, complex domains    │
│  decoupling      │  CDC, analytics  │                              │
│                  │                  │                              │
│  Tools:          │  Tools:          │  Tools:                      │
│  RabbitMQ, SNS,  │  Kafka, Pulsar,  │  EventStoreDB, Kafka +      │
│  Redis Pub/Sub   │  Kinesis, NATS   │  custom store, Axon          │
│                  │  JetStream       │                              │
└──────────────────┴──────────────────┴──────────────────────────────┘
```

**Pattern Selection Guide**:

```
Q: Do I need to replay past events?
├── No  -> Simple pub/sub (RabbitMQ, SNS/SQS)
└── Yes
    Q: Do I need to reconstruct state from events?
    ├── No  -> Event streaming (Kafka, NATS JetStream)
    └── Yes -> Event sourcing (EventStoreDB, custom event store)

Q: Are reads and writes significantly different in shape or scale?
├── No  -> Single model is fine
└── Yes -> CQRS (separate read/write models, eventually consistent)
```

### Step 2: Choose a Message Broker

**Broker Comparison**:

```
┌──────────────┬────────────────┬─────────────────┬───────────────┬──────────────┐
│ Feature      │ Apache Kafka   │ RabbitMQ        │ AWS SNS/SQS   │ NATS         │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Model        │ Log-based      │ Queue/exchange  │ Queue + topic │ Pub/sub +    │
│              │ streaming      │ broker          │ cloud managed │ JetStream    │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Ordering     │ Per-partition  │ Per-queue       │ FIFO optional │ Per-subject  │
│              │ guaranteed     │ guaranteed      │ (SQS FIFO)    │ (JetStream)  │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Retention    │ Configurable   │ Until consumed  │ Up to 14 days │ Configurable │
│              │ (days/size)    │                 │ (SQS)         │ (JetStream)  │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Replay       │ Yes (offset)   │ No (dead letter │ No (DLQ only) │ Yes          │
│              │                │ only)           │               │ (JetStream)  │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Throughput   │ Very high      │ Moderate        │ High          │ Very high    │
│              │ (millions/sec) │ (tens of k/sec) │ (managed)     │ (millions/s) │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Complexity   │ High           │ Moderate        │ Low           │ Low-Moderate │
├──────────────┼────────────────┼─────────────────┼───────────────┼──────────────┤
│ Best For     │ Event streams, │ Task queues,    │ Serverless,   │ Microservice │
│              │ CDC, analytics │ RPC, routing    │ AWS-native    │ messaging    │
└──────────────┴────────────────┴─────────────────┴───────────────┴──────────────┘
```

### Step 3: Design Event Schemas

**CloudEvents Format (JSON)**:

```json
{
  "specversion": "1.0",
  "id": "evt-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "source": "urn:example:order-service",
  "type": "com.example.order.created",
  "datacontenttype": "application/json",
  "time": "2026-03-03T10:30:00Z",
  "subject": "order-12345",
  "data": {
    "orderId": "order-12345",
    "customerId": "cust-67890",
    "items": [
      {
        "productId": "prod-111",
        "quantity": 2,
        "unitPrice": 29.99
      }
    ],
    "total": 59.98,
    "currency": "USD"
  }
}
```

**Event Naming Convention**:

```
Format:  <domain>.<aggregate>.<past-tense-verb>
Examples:
  com.example.order.created
  com.example.order.cancelled
  com.example.payment.processed
  com.example.inventory.reserved
  com.example.shipment.dispatched
  com.example.user.email_verified

Rules:
  1. Always past tense (something that HAS happened)
  2. Domain-qualified to avoid collisions
  3. Specific enough to convey meaning without reading the payload
```

**Avro Schema (for schema registry)**:

```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.order.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "items", "type": {
      "type": "array",
      "items": {
        "type": "record",
        "name": "OrderItem",
        "fields": [
          {"name": "productId", "type": "string"},
          {"name": "quantity", "type": "int"},
          {"name": "unitPrice", "type": {"type": "bytes", "logicalType": "decimal", "precision": 10, "scale": 2}}
        ]
      }
    }},
    {"name": "total", "type": {"type": "bytes", "logicalType": "decimal", "precision": 10, "scale": 2}},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "occurredAt", "type": {"type": "long", "logicalType": "timestamp-millis"}}
  ]
}
```

### Step 4: Implement Kafka Producer and Consumer

**Python Producer (confluent-kafka)**:

```python
import json
import uuid
from datetime import datetime, timezone
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

def create_producer(bootstrap_servers: str) -> Producer:
    config = {
        "bootstrap.servers": bootstrap_servers,
        "acks": "all",                    # Wait for all replicas
        "enable.idempotence": True,       # Exactly-once producer semantics
        "max.in.flight.requests.per.connection": 5,
        "retries": 2147483647,            # Infinite retries with idempotence
        "linger.ms": 5,                   # Batch for 5ms for throughput
        "compression.type": "lz4",        # Compress batches
    }
    return Producer(config)

def publish_order_created(producer: Producer, order: dict):
    """Publish an OrderCreated event with CloudEvents envelope."""
    event = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:example:order-service",
        "type": "com.example.order.created",
        "datacontenttype": "application/json",
        "time": datetime.now(timezone.utc).isoformat(),
        "subject": order["id"],
        "data": order,
    }

    producer.produce(
        topic="orders",
        key=order["id"].encode("utf-8"),    # Partition by order ID
        value=json.dumps(event).encode("utf-8"),
        headers={
            "ce-type": "com.example.order.created",
            "ce-source": "urn:example:order-service",
        },
        callback=delivery_callback,
    )
    producer.flush()

def delivery_callback(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")
```

**Python Consumer with Idempotency**:

```python
import json
from confluent_kafka import Consumer, KafkaError
from typing import Callable

def create_consumer(
    bootstrap_servers: str,
    group_id: str,
    topics: list[str],
) -> Consumer:
    config = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,       # Manual commit for reliability
        "max.poll.interval.ms": 300000,    # 5 min processing budget
        "session.timeout.ms": 45000,
    }
    consumer = Consumer(config)
    consumer.subscribe(topics)
    return consumer

class IdempotentConsumer:
    """Consumer that tracks processed event IDs to ensure exactly-once handling."""

    def __init__(self, consumer: Consumer, db, handler: Callable):
        self.consumer = consumer
        self.db = db
        self.handler = handler

    async def run(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    raise Exception(f"Consumer error: {msg.error()}")

                event = json.loads(msg.value().decode("utf-8"))
                event_id = event["id"]

                # Idempotency check: skip if already processed
                if await self.db.execute(
                    "SELECT 1 FROM processed_events WHERE event_id = :id",
                    {"id": event_id},
                ):
                    self.consumer.commit(msg)
                    continue

                # Process event within a transaction
                async with self.db.transaction():
                    await self.handler(event)
                    await self.db.execute(
                        "INSERT INTO processed_events (event_id, processed_at) "
                        "VALUES (:id, NOW())",
                        {"id": event_id},
                    )

                self.consumer.commit(msg)

        finally:
            self.consumer.close()
```

### Step 5: Implement Event Sourcing

**Event Store Schema (PostgreSQL)**:

```sql
-- Event store table
CREATE TABLE event_store (
    id              BIGSERIAL PRIMARY KEY,
    aggregate_type  TEXT NOT NULL,
    aggregate_id    UUID NOT NULL,
    event_type      TEXT NOT NULL,
    event_version   INTEGER NOT NULL,
    data            JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Optimistic concurrency: no two events for the same aggregate
    -- can have the same version
    UNIQUE (aggregate_id, event_version)
);

CREATE INDEX idx_event_store_aggregate
    ON event_store (aggregate_type, aggregate_id, event_version);

CREATE INDEX idx_event_store_type
    ON event_store (event_type, created_at);

-- Processed events table (for idempotent consumers)
CREATE TABLE processed_events (
    event_id        TEXT PRIMARY KEY,
    processed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Snapshots table (for performance optimization)
CREATE TABLE snapshots (
    aggregate_type  TEXT NOT NULL,
    aggregate_id    UUID NOT NULL,
    version         INTEGER NOT NULL,
    state           JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (aggregate_type, aggregate_id)
);
```

**Event Store Implementation (Python)**:

```python
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import list, Optional

@dataclass
class DomainEvent:
    event_type: str
    aggregate_id: str
    data: dict
    version: int = 0
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = field(default_factory=dict)

class EventStore:
    def __init__(self, db):
        self.db = db

    async def append(
        self,
        aggregate_type: str,
        aggregate_id: str,
        events: list[DomainEvent],
        expected_version: int,
    ):
        """Append events with optimistic concurrency control."""
        async with self.db.transaction():
            # Check current version
            row = await self.db.fetchone(
                "SELECT COALESCE(MAX(event_version), 0) AS version "
                "FROM event_store WHERE aggregate_id = :id",
                {"id": aggregate_id},
            )
            current_version = row["version"]

            if current_version != expected_version:
                raise ConcurrencyError(
                    f"Expected version {expected_version}, "
                    f"but current version is {current_version}"
                )

            for i, event in enumerate(events):
                version = expected_version + i + 1
                await self.db.execute(
                    """INSERT INTO event_store
                       (aggregate_type, aggregate_id, event_type,
                        event_version, data, metadata)
                       VALUES (:agg_type, :agg_id, :evt_type,
                               :version, :data, :metadata)""",
                    {
                        "agg_type": aggregate_type,
                        "agg_id": aggregate_id,
                        "evt_type": event.event_type,
                        "version": version,
                        "data": json.dumps(event.data),
                        "metadata": json.dumps(event.metadata),
                    },
                )

    async def load(
        self,
        aggregate_id: str,
        after_version: int = 0,
    ) -> list[DomainEvent]:
        """Load events for an aggregate, optionally after a snapshot version."""
        rows = await self.db.fetchall(
            """SELECT event_type, aggregate_id, event_version, data, metadata, created_at
               FROM event_store
               WHERE aggregate_id = :id AND event_version > :after
               ORDER BY event_version""",
            {"id": aggregate_id, "after": after_version},
        )
        return [
            DomainEvent(
                event_type=r["event_type"],
                aggregate_id=r["aggregate_id"],
                data=json.loads(r["data"]),
                version=r["event_version"],
                timestamp=r["created_at"],
                metadata=json.loads(r["metadata"]),
            )
            for r in rows
        ]

class ConcurrencyError(Exception):
    pass
```

**Aggregate Reconstruction**:

```python
class OrderAggregate:
    """Reconstruct order state by replaying events."""

    def __init__(self):
        self.id: Optional[str] = None
        self.status: str = "unknown"
        self.items: list = []
        self.total: float = 0.0
        self.version: int = 0

    def apply(self, event: DomainEvent):
        handler = getattr(self, f"_on_{event.event_type}", None)
        if handler:
            handler(event.data)
        self.version = event.version

    def _on_order_created(self, data):
        self.id = data["orderId"]
        self.status = "pending"
        self.items = data["items"]
        self.total = data["total"]

    def _on_order_confirmed(self, data):
        self.status = "confirmed"

    def _on_order_cancelled(self, data):
        self.status = "cancelled"

    @classmethod
    async def load(cls, event_store: EventStore, aggregate_id: str) -> "OrderAggregate":
        order = cls()
        events = await event_store.load(aggregate_id)
        for event in events:
            order.apply(event)
        return order
```

### Step 6: Implement the Saga Pattern

**Choreography-Based Saga (event-driven)**:

```
Order Service          Payment Service        Inventory Service       Shipping Service
     │                       │                       │                       │
     │  OrderCreated         │                       │                       │
     ├──────────────────────►│                       │                       │
     │                       │  PaymentProcessed     │                       │
     │                       ├──────────────────────►│                       │
     │                       │                       │  InventoryReserved    │
     │                       │                       ├──────────────────────►│
     │                       │                       │                       │
     │                       │   If PaymentFailed    │                       │
     │  OrderCancelled  ◄────┤                       │                       │
     │                       │                       │                       │
     │                       │   If InsufficientStock│                       │
     │                       │  PaymentRefunded ◄────┤                       │
     │  OrderCancelled  ◄────┤                       │                       │
```

**Orchestrator-Based Saga (Python)**:

```python
from enum import Enum
from dataclasses import dataclass
from typing import list, Optional

class SagaStepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: str          # Command to execute
    compensation: str    # Command to undo the action
    status: SagaStepStatus = SagaStepStatus.PENDING

class OrderSagaOrchestrator:
    """Orchestrates order creation across multiple services."""

    def __init__(self, command_bus, event_store):
        self.command_bus = command_bus
        self.event_store = event_store

    def define_steps(self, order_data: dict) -> list[SagaStep]:
        return [
            SagaStep(
                name="reserve_inventory",
                action="ReserveInventory",
                compensation="ReleaseInventory",
            ),
            SagaStep(
                name="process_payment",
                action="ProcessPayment",
                compensation="RefundPayment",
            ),
            SagaStep(
                name="create_shipment",
                action="CreateShipment",
                compensation="CancelShipment",
            ),
        ]

    async def execute(self, saga_id: str, order_data: dict):
        steps = self.define_steps(order_data)
        completed_steps = []

        for step in steps:
            try:
                step.status = SagaStepStatus.COMPLETED
                await self.command_bus.send(step.action, {
                    "saga_id": saga_id,
                    "order": order_data,
                })
                completed_steps.append(step)
            except Exception as e:
                # Compensate in reverse order
                step.status = SagaStepStatus.FAILED
                await self._compensate(saga_id, completed_steps, order_data)
                raise SagaFailedError(
                    f"Saga {saga_id} failed at step '{step.name}': {e}"
                )

    async def _compensate(
        self,
        saga_id: str,
        completed_steps: list[SagaStep],
        order_data: dict,
    ):
        for step in reversed(completed_steps):
            try:
                step.status = SagaStepStatus.COMPENSATING
                await self.command_bus.send(step.compensation, {
                    "saga_id": saga_id,
                    "order": order_data,
                })
                step.status = SagaStepStatus.COMPENSATED
            except Exception as comp_error:
                # Compensation failure requires manual intervention
                step.status = SagaStepStatus.FAILED
                await self._alert_manual_intervention(saga_id, step, comp_error)

class SagaFailedError(Exception):
    pass
```

### Step 7: Handle Event Versioning and Evolution

**Versioning Strategies**:

```python
# Strategy 1: Upcasting (transform old events to new format on read)
class EventUpcaster:
    """Transform events from older versions to the current schema."""

    upcasters = {}

    @classmethod
    def register(cls, event_type: str, from_version: int, to_version: int):
        def decorator(fn):
            cls.upcasters[(event_type, from_version, to_version)] = fn
            return fn
        return decorator

    @classmethod
    def upcast(cls, event: DomainEvent) -> DomainEvent:
        key = (event.event_type, event.metadata.get("schema_version", 1), 2)
        upcaster = cls.upcasters.get(key)
        if upcaster:
            return upcaster(event)
        return event

@EventUpcaster.register("order_created", from_version=1, to_version=2)
def upcast_order_created_v1_to_v2(event: DomainEvent) -> DomainEvent:
    """V1 had 'amount'; V2 renamed to 'total' and added 'currency'."""
    data = dict(event.data)
    data["total"] = data.pop("amount", 0)
    data.setdefault("currency", "USD")
    event.data = data
    event.metadata["schema_version"] = 2
    return event
```

**Backward-Compatible Evolution Rules**:

```
SAFE changes (backward compatible):
  - Add a new optional field with a default value
  - Add a new event type
  - Add a new optional header

UNSAFE changes (breaking):
  - Remove or rename a field
  - Change a field's type
  - Change the meaning of a field
  - Remove an event type

MIGRATION strategy for breaking changes:
  1. Publish both old and new event versions simultaneously
  2. Migrate all consumers to read the new version
  3. Stop publishing the old version
  4. (Optional) Upcast old events on read
```

### Step 8: Implement the Outbox Pattern

```python
# The outbox pattern ensures atomicity between database writes and event publishing.
# Events are written to an outbox table in the same transaction as the business data.
# A separate process reads the outbox and publishes to the message broker.

async def create_order_with_outbox(db, order_data: dict):
    """Atomically persist order and queue event for publishing."""
    async with db.transaction():
        # 1. Write business data
        order = await db.execute(
            "INSERT INTO orders (customer_id, total, status) "
            "VALUES (:cid, :total, 'pending') RETURNING *",
            {"cid": order_data["customer_id"], "total": order_data["total"]},
        )

        # 2. Write event to outbox (same transaction)
        await db.execute(
            """INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
               VALUES ('order', :id, 'order.created', :payload)""",
            {
                "id": order["id"],
                "payload": json.dumps({
                    "orderId": order["id"],
                    "customerId": order["customer_id"],
                    "total": order["total"],
                }),
            },
        )

    return order

# Outbox publisher (runs as a background process)
async def outbox_publisher(db, producer, poll_interval: float = 1.0):
    """Poll outbox table and publish to Kafka."""
    while True:
        rows = await db.fetchall(
            "SELECT * FROM outbox WHERE published_at IS NULL "
            "ORDER BY created_at LIMIT 100",
        )
        for row in rows:
            producer.produce(
                topic=row["aggregate_type"] + "s",
                key=row["aggregate_id"].encode(),
                value=row["payload"].encode(),
            )
            await db.execute(
                "UPDATE outbox SET published_at = NOW() WHERE id = :id",
                {"id": row["id"]},
            )
        producer.flush()
        await asyncio.sleep(poll_interval)
```

**RabbitMQ Setup (Docker Compose + Python)**:

```yaml
# docker-compose.yaml
services:
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    ports:
      - "5672:5672"     # AMQP
      - "15672:15672"   # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: secret
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  rabbitmq-data:
```

```python
# RabbitMQ publisher with exchange and routing
import pika
import json

def setup_rabbitmq(host: str = "localhost"):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials("admin", "secret"))
    )
    channel = connection.channel()

    # Topic exchange for flexible routing
    channel.exchange_declare(exchange="events", exchange_type="topic", durable=True)

    # Dead letter exchange
    channel.exchange_declare(exchange="events.dlx", exchange_type="topic", durable=True)

    # Queues with dead letter routing
    channel.queue_declare(
        queue="order-processing",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "events.dlx",
            "x-dead-letter-routing-key": "order.failed",
            "x-message-ttl": 300000,  # 5 min TTL
        },
    )
    channel.queue_bind(queue="order-processing", exchange="events", routing_key="order.*")

    # Dead letter queue
    channel.queue_declare(queue="order-failed-dlq", durable=True)
    channel.queue_bind(queue="order-failed-dlq", exchange="events.dlx", routing_key="order.failed")

    return connection, channel

def publish_event(channel, routing_key: str, event: dict):
    channel.basic_publish(
        exchange="events",
        routing_key=routing_key,
        body=json.dumps(event),
        properties=pika.BasicProperties(
            delivery_mode=2,         # Persistent
            content_type="application/json",
            message_id=event.get("id", ""),
        ),
    )
```

## Best Practices

- **Use the outbox pattern** to guarantee atomicity between state changes and event publication
- **Design events as facts** (past tense, immutable); never update a published event
- **Include enough context** in events so consumers do not need to call back to the producer
- **Implement idempotent consumers** using a processed-events table or deduplication key
- **Use a schema registry** (Confluent, Apicurio) to enforce schema compatibility
- **Version events from day one**; include a schema_version field in metadata
- **Set up dead letter queues** for every consumer to capture unprocessable messages
- **Partition by aggregate ID** so all events for one entity go to the same partition (ordering)
- **Monitor consumer lag** as a key health metric; alert when lag exceeds a threshold
- **Prefer choreography for simple flows** (2-3 services); use orchestration for complex sagas (4+)
- **Replay events to rebuild read models** rather than writing complex migration scripts

## Common Patterns

### Pattern 1: CQRS with Separate Read Model

```python
# Write side: event-sourced aggregate
async def place_order(command, event_store):
    order = await OrderAggregate.load(event_store, command.order_id)
    events = order.place(command)
    await event_store.append("order", command.order_id, events, order.version)

# Read side: projector updates a denormalized read model
async def on_order_created(event, read_db):
    await read_db.execute(
        """INSERT INTO order_view
           (id, customer_name, total, status, item_count, created_at)
           VALUES (:id, :name, :total, 'pending', :count, :ts)""",
        {
            "id": event.data["orderId"],
            "name": event.data["customerName"],
            "total": event.data["total"],
            "count": len(event.data["items"]),
            "ts": event.timestamp,
        },
    )
```

### Pattern 2: Dead Letter Queue Handler

```python
async def process_dlq(consumer, alert_service):
    """Process dead letter queue: log, alert, and store for manual review."""
    for message in consumer:
        await alert_service.notify(
            channel="ops",
            message=f"DLQ message: {message.topic} | "
                    f"Key: {message.key} | "
                    f"Error: {message.headers.get('x-error')}",
        )
        await store_for_review(message)
        consumer.commit(message)
```

### Pattern 3: Event Replay for Read Model Rebuild

```python
async def rebuild_read_model(event_store, projector, aggregate_type: str):
    """Replay all events to rebuild a read model from scratch."""
    await projector.truncate()  # Clear the read model

    offset = 0
    batch_size = 1000
    while True:
        events = await event_store.load_all(
            aggregate_type=aggregate_type,
            after_id=offset,
            limit=batch_size,
        )
        if not events:
            break
        for event in events:
            await projector.project(event)
            offset = event.id
    print(f"Rebuilt read model from {offset} events")
```

## Quality Checklist

- [ ] Events use past tense and follow a consistent naming convention
- [ ] Event schemas include specversion, id, source, type, and timestamp (CloudEvents)
- [ ] Outbox pattern ensures atomicity between data writes and event publication
- [ ] Consumers are idempotent (duplicate event processing is safe)
- [ ] Dead letter queues configured for every consumer
- [ ] Schema versioning strategy documented (upcasting or dual-publish)
- [ ] Consumer group lag is monitored and alerted
- [ ] Partitioning strategy ensures ordering where needed
- [ ] Saga compensations handle failure of compensating actions
- [ ] Event retention and compaction policies defined
- [ ] Read model rebuild procedure documented and tested
- [ ] Schema registry enforces backward compatibility

## Related Skills

- `async-patterns` - Concurrency patterns for event processing
- `observability-setup` - Monitoring event-driven systems
- `graphql-development` - GraphQL subscriptions as an event delivery mechanism
- `cloud-architect` - Managed messaging services (SNS/SQS, EventBridge, Pub/Sub)

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
