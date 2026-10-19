---
name: kafka-streaming
description: >
  Architect, produce to, consume from, and operate Apache Kafka event streaming systems.
  Use when partitioning topics for ordered processing, configuring durability invariants
  (acks=all, min.insync.replicas), tuning consumer groups and cooperative rebalancing,
  designing offset commit strategies, tracking consumer lag, integrating Schema Registries
  with Avro or JSON Schema, managing poison pills with dead-letter queues (DLQs),
  or enabling Exactly-Once Semantics (EOS).
compatibility: >
  Agent Skills-compatible coding agents building event-driven systems with Apache Kafka 3.0+ or Confluent Platform. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "kafka, event-streaming, pub-sub, distributed-systems, schema-registry, avro, dlq, eos"
  topics: "software-development"
---

# Apache Kafka & Event Streaming Architecture

Apache Kafka is a distributed, partitioned, replicated commit-log platform engineered for high-throughput, fault-tolerant event streaming. Designing robust Kafka systems requires mastering partitioning keys for ordering guarantees, configuring broker/producer durability invariants, tuning consumer groups to avoid rebalance storms, integrating schema contracts, and isolating poisoned messages.

## Purpose & Overview

This skill guides the design, implementation, and operational governance of Kafka event streaming systems. It covers topic partitioning strategies, durability configurations (`acks=all`, `min.insync.replicas`), consumer group lifecycle management, synchronous vs asynchronous offset commits, consumer lag monitoring, Schema Registry evolution with Avro and JSON Schema, poison pill remediation via Dead Letter Queues (DLQ), and Exactly-Once Semantics (EOS).

---

## Core Principles & Rules

1. **Ordering is guaranteed only per partition**: Kafka guarantees total message ordering exclusively within a single partition. Messages with identical keys hash to the same partition; keys must represent the logical entity whose order must be strictly preserved (e.g. `order_id`, `account_id`).
2. **Durability requires `acks=all` with `min.insync.replicas >= 2`**: Setting `acks=all` (or `acks=-1`) guarantees that the leader and all in-sync replicas acknowledge the write. Ensure topic replication factor is at least 3 with `min.insync.replicas=2` to tolerate broker failures without data loss or write rejection.
3. **Always enable producer idempotence**: Set `enable.idempotence=true` on producers. This prevents duplicate messages caused by network retries without degrading throughput.
4. **Never commit offsets before processing completing successfully**: Committing offsets prematurely causes permanent data loss if processing crashes. Always commit offsets synchronously or asynchronously *after* records are fully processed and downstream side effects persist.
5. **Enforce schema evolution with a Schema Registry**: Never publish unversioned arbitrary JSON blobs to shared topics. Register Avro, Protobuf, or JSON Schema contracts and enforce backward or full compatibility to prevent breaking downstream consumers.
6. **Isolate poison pills immediately with Dead-Letter Queues (DLQ)**: An unparseable or unprocessable message will block an entire partition indefinitely if repeatedly retried. Route failed messages to a dedicated DLQ topic with original error metadata after bounded retries.
7. **Use Cooperative Sticky Rebalancing**: Configure `partition.assignment.strategy` to `org.apache.kafka.clients.consumer.CooperativeStickyAssignor` to avoid stop-the-world partition rebalances when consumers join or leave a group.

---

## Standard Workflows & Procedures

### Workflow 1: High-Durability Producer Configuration

1. Set `acks=all`.
2. Enable idempotence: `enable.idempotence=true`.
3. Set `retries=MAX_INT` and configure exponential backoff (`retry.backoff.ms`).
4. Configure batching: `linger.ms=10` and `batch.size=65536` (64 KB) to optimize throughput without adding noticeable latency.
5. Supply explicit partition keys for entity-bound records.

### Workflow 2: Resilient Consumer Loop with DLQ & Manual Commit

1. Poll batches of records: `consumer.poll(Duration.ofMillis(100))`.
2. Iterate through records sequentially.
3. For each record:
   - Attempt processing within a try/catch block.
   - If a transient exception occurs, retry with bounded exponential backoff.
   - If all retries fail or a poison pill format error occurs, publish the record along with exception stack trace to the `<topic>.dlq` topic.
4. Commit processed offsets synchronously (`commitSync()`) or batch asynchronously (`commitAsync()`) upon loop conclusion.

### Workflow 3: Schema Registry Contract Evolution

1. Author schema definition (`order-event.avsc`).
2. Test compatibility against the registry before publishing:
   ```bash
   mvn schema-registry:test-compatibility
   # or via REST:
   curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"schema": "..."}' \
     http://schema-registry:8081/compatibility/subjects/order-events-value/versions/latest
   ```
3. Maintain `BACKWARD` or `FULL` compatibility: only add optional fields with defaults or remove optional fields.

---

## Real-World Examples & Patterns

### 1. High-Durability Idempotent Producer (Java)

```java
package com.example.streaming;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import io.confluent.kafka.serializers.KafkaAvroSerializer;

import java.util.Properties;

public class ResilientOrderProducer {
    private final Producer<String, OrderEvent> producer;

    public ResilientOrderProducer(String bootstrapServers, String schemaRegistryUrl) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class.getName());
        props.put("schema.registry.url", schemaRegistryUrl);

        // Core Durability & Idempotence Settings
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5); // Safe with idempotence

        // High-Throughput Batching
        props.put(ProducerConfig.LINGER_MS_CONFIG, "20");
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, Integer.toString(64 * 1024));
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "zstd");

        this.producer = new KafkaProducer<>(props);
    }

    public void publishOrder(OrderEvent event) {
        // Explicit key ensures partition ordering per customer
        ProducerRecord<String, OrderEvent> record = 
            new ProducerRecord<>("commerce.orders.v1", event.getCustomerId(), event);

        producer.send(record, (metadata, exception) -> {
            if (exception != null) {
                // Handle unrecoverable send failure
                System.err.printf("Failed to produce record %s: %s%n", event.getId(), exception.getMessage());
            } else {
                System.out.printf("Produced record to partition %d at offset %d%n",
                    metadata.partition(), metadata.offset());
            }
        });
    }
}
```

### 2. Resilient Consumer with DLQ & Cooperative Rebalancing (Python)

```python
import json
import logging
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

logger = logging.getLogger(__name__)

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-fulfillment-service',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual offset control
    'partition.assignment.strategy': 'cooperative-sticky',
    'max.poll.interval.ms': 300000,
}

consumer = Consumer(conf)
dlq_producer = Producer({'bootstrap.servers': 'localhost:9092', 'acks': 'all'})

def send_to_dlq(topic: str, original_msg, error: Exception):
    dlq_topic = f"{topic}.dlq"
    headers = [
        ('original_topic', topic.encode('utf-8')),
        ('original_partition', str(original_msg.partition()).encode('utf-8')),
        ('original_offset', str(original_msg.offset()).encode('utf-8')),
        ('error_message', str(error).encode('utf-8')),
    ]
    dlq_producer.produce(
        dlq_topic,
        key=original_msg.key(),
        value=original_msg.value(),
        headers=headers
    )
    dlq_producer.flush(timeout=5)

def run_consumer_loop():
    consumer.subscribe(['commerce.orders.v1'])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaException(msg.error())

            # Process record
            try:
                payload = json.loads(msg.value().decode('utf-8'))
                process_order(payload)
                # Commit offset synchronously after successful business logic
                consumer.commit(message=msg, asynchronous=False)
            except json.JSONDecodeError as err:
                logger.error(f"Poison pill detected at offset {msg.offset()}: {err}")
                send_to_dlq('commerce.orders.v1', msg, err)
                consumer.commit(message=msg, asynchronous=False)
            except Exception as err:
                logger.exception(f"Transient error processing order: {err}")
                # Backoff / retry or route to retry topic
    finally:
        consumer.close()
```

### 3. Exactly-Once Semantics (EOS) Transactional Processing

Consuming from input topic and producing to output topic within a single atomic transaction:

```python
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'order-aggregator-tx-1',
    'enable.idempotence': True,
}
tx_producer = Producer(producer_conf)
tx_producer.init_transactions()

try:
    tx_producer.begin_transaction()
    # 1. Produce transformed event
    tx_producer.produce('orders.aggregated', key=agg_key, value=agg_val)

    # 2. Commit consumer offsets inside the same producer transaction
    tx_producer.send_offsets_to_transaction(
        consumer.position(consumer.assignment()),
        consumer.consumer_group_metadata()
    )
    tx_producer.commit_transaction()
except Exception as e:
    tx_producer.abort_transaction()
    raise
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Why It Fails | Remediated Practice |
|---|---|---|
| **`enable.auto.commit=true`** | Offsets are auto-committed on timer intervals regardless of whether message processing succeeded, causing permanent data loss on crash. | Set `enable.auto.commit=false` and commit manually after processing. |
| **`acks=1` on financial/critical data** | Acknowledges write when only leader receives it. If leader dies before replicating, written data is permanently lost. | Use `acks=all` combined with broker `min.insync.replicas=2`. |
| **Random or null partition keys for entity events** | Orders or updates for the same account arrive out of order across multiple partitions. | Hash entity identifier (e.g. `user_id`, `order_id`) as the partition key. |
| **Long processing times exceeding `max.poll.interval.ms`** | Kafka broker assumes the consumer crashed, kicks it out of the group, and triggers constant rebalance storms. | Offload CPU-heavy work to worker thread pools or increase `max.poll.interval.ms`. |
| **Retrying poison pills indefinitely in the main loop** | Invalid JSON or corrupt schema blocks partition consumption forever, halting downstream pipeline progress. | Forward malformed messages to a Dead-Letter Queue (DLQ) and commit the offset. |
| **Evolving schemas with incompatible modifications** | Removing required fields or changing types causes consumers to crash during deserialization. | Enforce backward compatibility via Schema Registry and run validation in CI. |

---

## Verification Checklist

- [ ] Producers configured with `acks=all` and `enable.idempotence=true`.
- [ ] Topic configuration has `replication.factor >= 3` and `min.insync.replicas >= 2`.
- [ ] Partition keys are explicitly set on events where ordering matters.
- [ ] Consumers set `enable.auto.commit=false` and commit offsets post-processing.
- [ ] Cooperative sticky assignor is configured to prevent stop-the-world rebalances.
- [ ] Dead-Letter Queue (DLQ) topic is configured with error context headers for poison pills.
- [ ] Schema Registry compatibility checks are integrated into CI test pipelines.
- [ ] Consumer lag metrics (`records-lag-max`) are alerted upon in Prometheus/Datadog.

---

## Tooling & Reference Guides

- **Client Libraries**: `librdkafka`, `confluent-kafka` (Python/Go/C#), `kafka-clients` (Java).
- **Cluster Diagnostics**: `kcat` (formerly `kafkacat`) for CLI inspection, `kafka-consumer-groups.sh` for lag inspection.
- **Monitoring & UI**: AKHQ, Kafka UI, Confluent Control Center, Prometheus JMX Exporter for broker metrics.
- **Specifications & RFCs**: [Apache Kafka Documentation](https://kafka.apache.org/documentation/), [Confluent Schema Registry Guide](https://docs.confluent.io/platform/current/schema-registry/index.html).
