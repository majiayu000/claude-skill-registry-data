---
name: realtime-dashboard
model: reasoning
description: Complete guide to building real-time dashboards with streaming data, WebSocket/SSE, and live updates. Orchestrates dual-stream architecture, React hooks, and data visualization. Use when building trading dashboards, monitoring UIs, or live analytics. Triggers on realtime dashboard, live data, streaming dashboard, trading UI, monitoring.
---

# Real-Time Dashboard (Meta-Skill)

Complete guide to building real-time dashboards with streaming data.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install realtime-dashboard
```


---

## When to Use

- Building trading or financial dashboards
- Monitoring and analytics UIs
- Any dashboard needing live data updates
- Systems with server-to-client push requirements

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  APIs, Databases, Message Queues                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Services                          │
├─────────────────────────────────────────────────────────────┤
│  Kafka (durable)     │     Redis Pub/Sub (real-time)       │
│  See: dual-stream-architecture                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket/SSE Gateway                     │
│  See: websocket-hub-patterns                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Application                         │
├─────────────────────────────────────────────────────────────┤
│  Real-time Hooks          │  Data Visualization             │
│  See: realtime-react-hooks│  See: financial-data-visualization
├─────────────────────────────────────────────────────────────┤
│  Animated Displays        │  Connection Handling            │
│  See: animated-financial  │  See: resilient-connections     │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Event Publishing

Set up dual-stream publishing for durability + real-time.

**Read:** `ai/skills/realtime/dual-stream-architecture`

```go
func (p *DualPublisher) Publish(ctx context.Context, event Event) error {
    // 1. Kafka: Must succeed (durable)
    err := p.kafka.WriteMessages(ctx, kafka.Message{...})
    if err != nil {
        return err
    }

    // 2. Redis: Best-effort (real-time)
    p.publishToRedis(ctx, event)
    return nil
}
```

### Step 2: WebSocket Gateway

Create horizontally-scalable WebSocket connections.

**Read:** `ai/skills/realtime/websocket-hub-patterns`

```go
type Hub struct {
    connections   map[*Connection]bool
    subscriptions map[string]map[*Connection]bool
    redisClient   *redis.Client
}

// Lazy Redis subscriptions
func (h *Hub) subscribeToChannel(conn *Connection, channel string) {
    // Only subscribe to Redis on first local subscriber
}
```

### Step 3: React Hooks

Connect React to real-time data.

**Read:** `ai/skills/realtime/realtime-react-hooks`

```tsx
const { data, isConnected } = useSSE({ 
  url: '/api/events',
  onMessage: (data) => updateState(data),
});

// Or with SWR integration
const { data } = useRealtimeData('metrics', fetchMetrics);
```

### Step 4: Resilient Connections

Handle connection failures gracefully.

**Read:** `ai/skills/realtime/resilient-connections`

```typescript
const { isConnected, send } = useWebSocket({
  url: 'wss://api/ws',
  reconnect: true,
  maxRetries: 5,
  onMessage: handleMessage,
});
```

### Step 5: Data Visualization

Build dark-themed financial charts.

**Read:** `ai/skills/design-systems/financial-data-visualization`

```tsx
<PriceChart 
  data={priceHistory} 
  isPositive={change >= 0} 
/>
```

### Step 6: Animated Displays

Add smooth number animations.

**Read:** `ai/skills/design-systems/animated-financial-display`

```tsx
<AnimatedNumber value={price} prefix="$" decimals={2} />
<FlashingValue value={value} formatter={formatCurrency} />
```

---

## Component Skills Reference

| Skill | Purpose |
|-------|---------|
| `dual-stream-architecture` | Kafka + Redis publishing |
| `websocket-hub-patterns` | Scalable WebSocket server |
| `realtime-react-hooks` | SSE/WebSocket React hooks |
| `resilient-connections` | Retry, circuit breaker |
| `financial-data-visualization` | Chart theming |
| `animated-financial-display` | Number animations |

---

## Key Patterns

### Streaming Over Blocking

Never wait for all data. Show immediately, improve progressively:

```
Phase 1: Initial data + hints      → Immediate display
Phase 2: Background refinement     → Prices update in place
Phase 3: Historical data           → Charts populate
```

### Additive-Only Updates

Never zero out data when refinement fails. Only update when you have *better* data.

### Connection Status

Always show users their connection state:

```tsx
<ConnectionStatus isConnected={isConnected} />
```

---

## NEVER Do

- **Never block on data fetching** — Show immediately, refine progressively
- **Never skip connection status indicators** — Users need to know they're live
- **Never use polling when SSE/WebSocket available** — Real-time means push, not pull
- **Never forget graceful degradation** — System should work (degraded) when connection lost
- **Never zero out data on refinement failure** — Only update when you have *better* data
- **Never reconnect without exponential backoff** — Prevents thundering herd
- **Never skip Redis Pub/Sub failure handling** — Redis is best-effort; log and continue
- **Never send full payloads over Redis** — Send IDs only, clients fetch from API
- **Never share WebSocket pubsub across channels** — Each channel needs own subscription
- **Never forget ping/pong on WebSocket** — Load balancers close "idle" connections

---

## Checklist

- [ ] Set up dual-stream publishing (Kafka + Redis)
- [ ] Create WebSocket/SSE gateway
- [ ] Implement React hooks for real-time data
- [ ] Add reconnection with exponential backoff
- [ ] Build dark-themed chart components
- [ ] Add animated number displays
- [ ] Show connection status to users
- [ ] Handle errors gracefully
