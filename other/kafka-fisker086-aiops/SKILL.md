---
name: kafka
description: Query Kafka topics, consumer groups, and cluster info
activation_keywords: [kafka, topic, consumer, message, queue, event]
execution_mode: client
---

# Kafka Skill

Provides read-only Kafka cluster operations via local CLI:
- List and describe topics (partitions, replicas, ISR)
- List consumer groups and their offsets
- Get messages from topics (limited)
- Describe cluster and broker info
- Get topic configurations

Use `builtin_kafka` tool with fields:
- `operation`: one of "list_topics", "describe_topic", "list_groups", "describe_group", "get_messages", "get_config", "broker_info"
- `topic`: topic name (required for describe_topic/get_messages/get_config)
- `group`: consumer group name (required for describe_group)
- `bootstrap_server`: Kafka bootstrap server (default: "localhost:9092")
- `partition`: partition number (for get_messages, default: 0)
- `offset`: offset to start from (for get_messages, default: -1 meaning latest)
- `limit`: max messages to fetch (default: 10)

Note: Requires Kafka CLI tools (kafka-topics, kafka-consumer-groups, kafka-console-consumer) installed and accessible in PATH.
All operations are read-only.
