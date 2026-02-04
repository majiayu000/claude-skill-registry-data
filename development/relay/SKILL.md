---
name: relay
description: Relay events and notifications context
---

# Relay Domain Context

## What Is Relay?

Relay handles **events, notifications, and data feeds** across the Violet platform. It's the central nervous system for asynchronous communication.

## Core Capabilities

### Event Processing
- Kafka-based event streaming
- Event routing and transformation
- Dead letter queue handling
- Event replay capabilities

### Notifications
- Webhook delivery to external systems
- Email notifications
- In-app notifications
- Notification preferences management

### Feed Management
- Product feed generation
- Order feed updates
- Inventory feed synchronization
- Custom feed formats

## Key Kafka Topics

| Topic Pattern | Purpose |
|---------------|---------|
| `orders.order.*` | Order lifecycle events |
| `products.product.*` | Product update events |
| `merchants.merchant.*` | Merchant account events |
| `fulfillment.*` | Fulfillment tracking events |
| `inventory.*` | Stock level changes |

## Event Schema Pattern

```json
{
  "event_type": "order.created",
  "event_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0",
  "payload": {
    "order_id": 12345,
    "app_id": 67890
  },
  "metadata": {
    "source": "OrderService",
    "correlation_id": "uuid"
  }
}
```

## Key Repositories

| Repo | Purpose |
|------|---------|
| `FeedManagementService` | Feed generation and delivery |
| `NotificationService` | Notification routing |
| `EventBridge` | Event processing infrastructure |

## Integration Points

- **Beam**: Receives fulfillment events, sends order confirmations
- **Prism**: Receives order events, sends inventory updates
- **Channels**: Webhook delivery for order/fulfillment updates
- **Merchants**: Store update notifications
