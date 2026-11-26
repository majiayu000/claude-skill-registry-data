---
name: messaging-streaming-lord
always: true
description: Authority on Kafka, RabbitMQ, NATS, and Redis Streams.
triggers:
  - messaging streaming lord
  - messaging
  - kafka
  - rabbitmq

---
[SKILL] messaging-streaming-lord
[OBJ] Design event-driven systems from pub/sub to stream processing.
[RULES]
1. [CMD] IDs: Kafka `/apache/kafka`, RabbitMQ `/websites/rabbitmq`, NATS `/nats-io/nats.docs`, Redis Streams `/redis/docs`.
2. [REQ] Pillar coverage: messaging patterns, protocols/APIs, delivery guarantees, ordering/partitioning, scalability/availability, observability, schema/evolution, security.
3. [REQ] Query broker ID with full question + topic (producer, consumer, jetstream, streams, clustering).
4. [REQ] Compare brokers on throughput, latency, ordering, operational complexity, ecosystem.
5. [REQ] State delivery semantics and failure handling before recommending patterns.
6. [REQ] Broker selection: Kafka = high-throughput event backbone + replay (the log IS the storage); RabbitMQ = task queues + complex routing (work distribution, not event log); NATS = lightweight ops/edge/request-reply; Redis Streams = already-in-Redis simplicity. Match the tool to whether the consumer needs history.
7. [REQ] Delivery semantics are a contract: at-most-once (fast, lossy), at-least-once (default reality — dedupe required), exactly-once (Kafka EOS/transactions — expensive, scope-limited). Design consumers idempotent REGARDLESS; dedupe keys on natural ids.
8. [REQ] Ordering math: global ordering doesn't scale — order per key/partition only. Partition key = ordering boundary + parallelism unit; hot keys create hot partitions — pick keys that distribute.
9. [REQ] Consumer design: consumer groups for parallel processing; manual offset/ack after processing completes (not before); rebalancing is a stop-the-world — keep processing fast or use incremental/cooperative rebalancing.
10. [REQ] Failure taxonomy: retryable errors → retry with backoff; poison messages → DLQ after N attempts (never infinite retry); DLQ monitored + replayable; processing gaps alerted via lag metrics — consumer lag IS the health signal.
11. [REQ] Schema governance: registry (Avro/Protobuf/JSON-Schema) with compat rules; additive-evolvable schema changes; breaking changes = new topic/version, never overwrite meaning.
12. [REQ] Backpressure & flow: bounded queues/buffers everywhere; slow consumers must shed, buffer, or scale — never silently balloon; producer batching/compression for throughput, linger.ms trade-offs stated.
13. [REQ] Event design: events are facts (past tense, immutable), commands are instructions — don't blur; event payloads carry enough context to be useful without callbacks (fat vs thin is a stated decision); correlation/causation ids through every hop.
14. [REQ] Patterns catalog: outbox pattern for DB+broker atomicity (never dual-write), saga/process-manager for distributed transactions, CDC (Debezium) for change propagation, stream processing (Flink/Kafka Streams) only when real-time derivation is the requirement.
15. [PROHIBIT] Dual-writing DB + broker without outbox, assuming at-most-once (you'll get duplicates), ordering assumptions across partitions, infinite retries, or events that require synchronous callbacks to be interpretable.
