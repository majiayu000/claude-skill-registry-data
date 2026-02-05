---
name: message-queues
description: Message queue systems for game servers including Kafka, RabbitMQ, and actor models
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-game-server-architect
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - queue_system
  optional:
    - batch_size
    - ack_mode
  validation:
    queue_system:
      type: string
      enum: [kafka, rabbitmq, redis_pubsub, nats, sqs]
    batch_size:
      type: integer
      min: 1
      max: 1000
      default: 100
    ack_mode:
      type: string
      enum: [auto, manual, batch]
      default: manual

# Retry Configuration
retry_config:
  max_attempts: 5
  backoff: exponential
  initial_delay_ms: 100
  max_delay_ms: 30000
  retryable_errors:
    - CONNECTION_LOST
    - BROKER_UNAVAILABLE

# Observability
observability:
  logging:
    level: info
    fields: [queue, topic, partition, offset]
  metrics:
    - name: messages_published_total
      type: counter
    - name: messages_consumed_total
      type: counter
    - name: consumer_lag
      type: gauge
    - name: processing_duration_ms
      type: histogram
---

# Message Queues for Game Servers

Implement **asynchronous messaging** for scalable game server architecture.

## Queue Systems Comparison

| System | Throughput | Latency | Ordering | Use Case |
|--------|------------|---------|----------|----------|
| **Kafka** | Very High | Medium | Partition | Analytics, events |
| **RabbitMQ** | High | Low | Queue | Game events |
| **Redis Pub/Sub** | Very High | Very Low | None | Real-time updates |
| **NATS** | Very High | Ultra Low | Stream | Game state sync |
| **SQS** | High | Medium | FIFO option | Cloud native |

## Apache Kafka for Game Analytics

```java
// Producer configuration
Properties producerProps = new Properties();
producerProps.put("bootstrap.servers", "kafka:9092");
producerProps.put("key.serializer", StringSerializer.class.getName());
producerProps.put("value.serializer", JsonSerializer.class.getName());
producerProps.put("acks", "all");  // Durability
producerProps.put("retries", 3);
producerProps.put("linger.ms", 5);  // Batch for throughput
producerProps.put("batch.size", 16384);

KafkaProducer<String, GameEvent> producer = new KafkaProducer<>(producerProps);

// Publish game events
public void publishEvent(GameEvent event) {
    ProducerRecord<String, GameEvent> record = new ProducerRecord<>(
        "game-events",           // topic
        event.getPlayerId(),     // key (for partition affinity)
        event                    // value
    );

    producer.send(record, (metadata, exception) -> {
        if (exception != null) {
            log.error("Failed to publish event", exception);
            // Retry or dead-letter queue
        }
    });
}

// Consumer for analytics
Properties consumerProps = new Properties();
consumerProps.put("bootstrap.servers", "kafka:9092");
consumerProps.put("group.id", "analytics-consumer");
consumerProps.put("auto.offset.reset", "earliest");
consumerProps.put("enable.auto.commit", false);  // Manual commits

KafkaConsumer<String, GameEvent> consumer = new KafkaConsumer<>(consumerProps);
consumer.subscribe(List.of("game-events"));

while (running) {
    ConsumerRecords<String, GameEvent> records = consumer.poll(Duration.ofMillis(100));

    for (ConsumerRecord<String, GameEvent> record : records) {
        processEvent(record.value());
    }

    consumer.commitSync();  // Commit after processing
}
```

## RabbitMQ for Game Commands

```go
// Connection with retry
func connectRabbitMQ() (*amqp.Connection, error) {
    var conn *amqp.Connection
    var err error

    for i := 0; i < 5; i++ {
        conn, err = amqp.Dial("amqp://guest:guest@localhost:5672/")
        if err == nil {
            return conn, nil
        }
        time.Sleep(time.Second * time.Duration(1<<i))  // Exponential backoff
    }
    return nil, fmt.Errorf("failed to connect after retries: %w", err)
}

// Publisher
func publishMatchEvent(ch *amqp.Channel, event MatchEvent) error {
    body, err := json.Marshal(event)
    if err != nil {
        return err
    }

    return ch.Publish(
        "game-exchange",    // exchange
        "match.created",    // routing key
        false,              // mandatory
        false,              // immediate
        amqp.Publishing{
            ContentType:  "application/json",
            Body:         body,
            DeliveryMode: amqp.Persistent,  // Survive broker restart
            MessageId:    uuid.New().String(),
            Timestamp:    time.Now(),
        },
    )
}

// Consumer with manual ack
func consumeMatchEvents(ch *amqp.Channel) error {
    msgs, err := ch.Consume(
        "match-events",  // queue
        "",              // consumer tag
        false,           // auto-ack (false = manual)
        false,           // exclusive
        false,           // no-local
        false,           // no-wait
        nil,             // args
    )
    if err != nil {
        return err
    }

    for msg := range msgs {
        var event MatchEvent
        if err := json.Unmarshal(msg.Body, &event); err != nil {
            msg.Nack(false, false)  // Don't requeue malformed messages
            continue
        }

        if err := processMatchEvent(event); err != nil {
            msg.Nack(false, true)  // Requeue for retry
            continue
        }

        msg.Ack(false)  // Acknowledge successful processing
    }
    return nil
}
```

## Redis Pub/Sub for Real-Time

```python
import redis
import json
from concurrent.futures import ThreadPoolExecutor

# Publisher (Game Server)
class GameStatePublisher:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)

    def broadcast_state(self, game_id: str, state: dict):
        channel = f"game:{game_id}"
        self.redis.publish(channel, json.dumps(state))

    def broadcast_chat(self, game_id: str, message: dict):
        channel = f"chat:{game_id}"
        self.redis.publish(channel, json.dumps(message))

# Subscriber (Client Gateway)
class GameStateSubscriber:
    def __init__(self, game_id: str, callback):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.pubsub = self.redis.pubsub()
        self.callback = callback
        self.game_id = game_id

    def subscribe(self):
        self.pubsub.subscribe(f"game:{self.game_id}")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                self.callback(data)

    def unsubscribe(self):
        self.pubsub.unsubscribe()
        self.pubsub.close()

# Usage with connection pool
pool = redis.ConnectionPool(host='localhost', port=6379, max_connections=100)
redis_client = redis.Redis(connection_pool=pool)
```

## NATS for Low-Latency Messaging

```go
// NATS JetStream for persistent messaging
func setupNATS() (*nats.Conn, nats.JetStreamContext, error) {
    nc, err := nats.Connect("nats://localhost:4222",
        nats.RetryOnFailedConnect(true),
        nats.MaxReconnects(10),
        nats.ReconnectWait(time.Second),
    )
    if err != nil {
        return nil, nil, err
    }

    js, err := nc.JetStream()
    if err != nil {
        return nil, nil, err
    }

    // Create stream for game events
    _, err = js.AddStream(&nats.StreamConfig{
        Name:       "GAME_EVENTS",
        Subjects:   []string{"game.>"},
        Retention:  nats.LimitsPolicy,
        MaxAge:     time.Hour * 24,
        Storage:    nats.FileStorage,
        Replicas:   3,
    })

    return nc, js, err
}

// Publish with acknowledgment
func publishGameEvent(js nats.JetStreamContext, event GameEvent) error {
    data, _ := json.Marshal(event)

    ack, err := js.Publish(
        fmt.Sprintf("game.%s.%s", event.GameID, event.Type),
        data,
    )
    if err != nil {
        return err
    }

    log.Printf("Published: seq=%d", ack.Sequence)
    return nil
}

// Durable consumer
func consumeGameEvents(js nats.JetStreamContext) error {
    sub, err := js.Subscribe("game.>",
        func(msg *nats.Msg) {
            var event GameEvent
            json.Unmarshal(msg.Data, &event)
            processEvent(event)
            msg.Ack()
        },
        nats.Durable("game-processor"),
        nats.ManualAck(),
        nats.AckWait(time.Second*30),
    )
    if err != nil {
        return err
    }
    defer sub.Unsubscribe()

    <-make(chan struct{})  // Block forever
    return nil
}
```

## Actor Model (Akka/Orleans)

```csharp
// Orleans Grain (Virtual Actor)
public interface IPlayerGrain : IGrainWithStringKey
{
    Task<PlayerState> GetState();
    Task<bool> TakeDamage(int amount, string sourceId);
    Task<bool> ApplyBuff(Buff buff);
}

public class PlayerGrain : Grain, IPlayerGrain
{
    private readonly IPersistentState<PlayerState> _state;
    private readonly ILogger<PlayerGrain> _logger;

    public PlayerGrain(
        [PersistentState("player", "gameStore")] IPersistentState<PlayerState> state,
        ILogger<PlayerGrain> logger)
    {
        _state = state;
        _logger = logger;
    }

    public Task<PlayerState> GetState() => Task.FromResult(_state.State);

    public async Task<bool> TakeDamage(int amount, string sourceId)
    {
        _state.State.Health -= amount;

        if (_state.State.Health <= 0)
        {
            // Notify game grain about death
            var gameGrain = GrainFactory.GetGrain<IGameGrain>(_state.State.GameId);
            await gameGrain.OnPlayerDeath(this.GetPrimaryKeyString(), sourceId);
        }

        await _state.WriteStateAsync();
        return _state.State.Health > 0;
    }
}

// Silo configuration
var host = new HostBuilder()
    .UseOrleans(siloBuilder =>
    {
        siloBuilder
            .UseLocalhostClustering()
            .AddRedisGrainStorage("gameStore", options =>
            {
                options.ConnectionString = "localhost:6379";
            })
            .ConfigureLogging(logging => logging.AddConsole());
    })
    .Build();
```

## Use Case Mapping

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Cross-server chat | RabbitMQ | Reliable delivery |
| Analytics pipeline | Kafka | High throughput, replay |
| Real-time state | Redis Pub/Sub | Ultra-low latency |
| Distributed game state | Orleans/Akka | Location transparency |
| Match results | Kafka | Ordered, durable |
| Notifications | NATS | Simple, fast |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Consumer lag | Slow processing | Scale consumers |
| Message loss | Auto-ack before process | Manual ack |
| Duplicate processing | At-least-once | Idempotent handlers |
| Broker unavailable | Single point | Cluster mode |

### Debug Checklist

```bash
# Kafka consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group analytics-consumer

# RabbitMQ queue status
rabbitmqctl list_queues name messages consumers

# Redis pub/sub channels
redis-cli PUBSUB CHANNELS "game:*"

# NATS stream info
nats stream info GAME_EVENTS
```

## Unit Test Template

```go
func TestMessagePublishing(t *testing.T) {
    // Setup test broker (use testcontainers)
    container := setupRabbitMQContainer(t)
    defer container.Terminate(context.Background())

    conn, _ := amqp.Dial(container.URI)
    ch, _ := conn.Channel()

    // Publish test event
    event := MatchEvent{
        MatchID:   "match-123",
        EventType: "created",
    }
    err := publishMatchEvent(ch, event)
    require.NoError(t, err)

    // Verify message received
    msgs, _ := ch.Consume("match-events", "", true, false, false, false, nil)
    select {
    case msg := <-msgs:
        var received MatchEvent
        json.Unmarshal(msg.Body, &received)
        assert.Equal(t, event.MatchID, received.MatchID)
    case <-time.After(time.Second * 5):
        t.Fatal("timeout waiting for message")
    }
}
```

## Resources

- `assets/` - Queue configurations
- `references/` - Messaging patterns
