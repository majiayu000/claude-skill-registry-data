---
name: queue-monitoring
category: observability
description: Use when an "enable observability" card asks for queues, or a worker's queue.backlog / consumer lag signals are unbound - which exporter or direct broker data source reads Kafka, RabbitMQ, NATS and Redis queues, the metric names the recipes expect, and the consumer-side metrics the developer adds
source: danielqsj/kafka_exporter, redpanda-data/kminion, rabbitmq/rabbitmq-server, nats-io/prometheus-nats-exporter, oliver006/redis_exporter docs (Apache-2.0/MIT), adapted
---

# Queue monitoring

A worker's golden signals are its backlog (messages waiting), its consume rate and its errors. The backlog is read at the broker; the rate and the errors are best emitted by the consumer itself. Decide per broker which path exists before you open a task.

## Read the broker first: no code change at all

TaskTrooper reads three brokers directly as data sources of their own kind — `kafka`, `rabbitmq`, `nats` — and their direct recipes (`kafka-direct`, `rabbitmq-direct`, `nats-direct`) bind a worker's backlog to a consumer group, queue or JetStream consumer. When a person can add that data source (broker address and credentials), nothing has to be built: say so on the card and propose the binding once the source exists.

## Or a Prometheus exporter next to the broker

| Broker | Exporter | What the recipes read |
|---|---|---|
| Kafka | `danielqsj/kafka_exporter` (recipe `kafka-exporter`) | `kafka_consumergroup_lag{consumergroup,topic,partition}`, `kafka_topic_partition_current_offset` |
| Kafka | `redpanda-data/kminion` (recipe `kminion`) | `kminion_kafka_consumer_group_topic_lag{group_id,topic_name}` |
| RabbitMQ | the built-in `rabbitmq_prometheus` plugin, port 15692 (recipe `rabbitmq-prometheus`) | `rabbitmq_queue_messages_ready`, `rabbitmq_queue_messages_unacked` per queue — scrape `/metrics/detailed?family=queue_coarse_metrics` (or `/metrics/per-object`), since the default `/metrics` aggregates queues away |
| NATS JetStream | `nats-io/prometheus-nats-exporter` with `-jsz=all` (recipe `nats-exporter`) | the consumer's `num_pending` and ack-pending gauges |
| Redis lists (Sidekiq, Bull, RQ, custom) | `oliver006/redis_exporter` with `-check-keys` / `-check-single-keys` naming the queue keys (recipe `redis-exporter-lists`) | `redis_key_size{key="queue:default"}` |
| AWS SQS / GCP Pub/Sub | none needed: CloudWatch `ApproximateNumberOfMessagesVisible` and Cloud Monitoring `subscription/num_undelivered_messages` (recipes `aws-sqs`, `gcp-pubsub`) | read through the cloud's own data source |

Running an exporter is infrastructure: if its deployment lives in this repository (a Helm chart, a docker-compose file, Terraform), it can be the developer's task; otherwise it is a `before_deploy` step for a person, and the exporter's address becomes a Prometheus scrape target.

## In the consumer: what the developer adds

- Counters for messages processed and failed, labelled by queue or topic (OpenTelemetry semantic conventions: `messaging.client.consumed.messages`, and `messaging.process.duration` as a histogram), plus `error.type` on failures.
- A consumer span per message, continuing the producer's trace context from the message headers (the OpenTelemetry Kafka/AMQP/NATS instrumentations do this) — so a slow job shows the request that enqueued it.
- Where the broker cannot be read (a managed service without metrics access), the consumer's own lag gauge: the client library's lag metric (Kafka consumers expose `records-lag-max`) exported as a gauge.

Acceptance criteria: "Given messages wait on queue `orders`, then the backlog series for `orders` is readable from <data source> and grows while the worker is stopped"; "Given a message fails, then the failed counter for `orders` increases by one."

## Then

Bind `queue.backlog` (and the worker's other golden signals) with `propose_signal_binding` scoped to this worker's queue or group — never a query summing every queue on the broker — and propose a `rising` alert rule above its normal peak.
