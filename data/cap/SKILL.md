---
name: cap
description: Comprehensive guidance for implementing distributed transactions and event bus patterns using DotNetCore.CAP library. Use when working with CAP for microservices event-driven architecture, message publishing/subscribing, outbox pattern implementation, and integration with message queues like RabbitMQ, Kafka, Azure Service Bus, and databases like SQL Server, PostgreSQL, MongoDB.
version: 1.0.0
---

# CAP (DotNetCore.CAP) Skill

This skill provides comprehensive guidance for using the DotNetCore.CAP library to implement distributed transactions and event bus patterns in .NET microservices.
Home page: `https://cap.dotnetcore.xyz/`

## Overview

CAP is a .NET library that provides a lightweight solution for distributed transactions and event bus integration in microservices. It uses the Outbox Pattern to ensure message reliability and consistency.

## What is EventBus?

An EventBus is a mechanism that allows different components to communicate with each other without knowing each other. A component can send an Event to the EventBus without knowing who will pick it up or how many others will. Components can also listen to Events on an EventBus without knowing who sent them. This way, components can communicate without depending on each other. Also, it's very easy to substitute a component – as long as the new component understands the events being sent and received, other components will never know about the substitution.

## Key Capabilities

### Setup and Configuration
- Installing CAP packages for different transports and storage providers
- Configuring CAP in ASP.NET Core applications
- Setting up message queues (RabbitMQ, Kafka, Azure Service Bus, etc.)
- Configuring databases (SQL Server, PostgreSQL, MySQL, MongoDB)

### Publishing Messages
- Publishing events within transactions
- Delayed message publishing
- Message headers and metadata

### Subscribing to Messages
- Controller-based subscriptions
- Service-based subscriptions with ICapSubscribe
- Consumer groups and load balancing
- Asynchronous message processing

### Advanced Features
- Partial topic subscriptions
- Custom serialization
- Monitoring with dashboard
- Service discovery integration

## Quick Start

### 1. Installation

Install the main CAP package:
```bash
dotnet add package DotNetCore.CAP
```

Choose your transport (message queue):
```bash
# RabbitMQ
dotnet add package DotNetCore.CAP.RabbitMQ

# Kafka
dotnet add package DotNetCore.CAP.Kafka

# Azure Service Bus
dotnet add package DotNetCore.CAP.AzureServiceBus
```

Choose your storage provider:
```bash
# SQL Server
dotnet add package DotNetCore.CAP.SqlServer

# PostgreSQL
dotnet add package DotNetCore.CAP.PostgreSql

# MongoDB
dotnet add package DotNetCore.CAP.MongoDB
```

### 2. Basic Configuration

In `Program.cs`:

```csharp
builder.Services.AddCap(x =>
{
    // Configure storage
    x.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"));
    
    // Configure transport
    x.UseRabbitMQ("localhost");
    
    // Optional: Configure dashboard
    x.UseDashboard();
});
```

### 3. Publishing Messages

```csharp
public class OrderService
{
    private readonly ICapPublisher _capPublisher;

    public OrderService(ICapPublisher capPublisher)
    {
        _capPublisher = capPublisher;
    }

    public async Task CreateOrder(Order order)
    {
        // Publish event
        await _capPublisher.PublishAsync("order.created", order);
    }
}
```

### 4. Subscribing to Messages

```csharp
public class OrderEventHandler : ICapSubscribe
{
    [CapSubscribe("order.created")]
    public async Task HandleOrderCreated(Order order)
    {
        // Process the order created event
        await ProcessOrderAsync(order);
    }
}
```

## Common Patterns

### Transactional Publishing

```csharp
using (var transaction = dbContext.Database.BeginTransaction(_capPublisher, autoCommit: true))
{
    // Business logic
    await dbContext.Orders.AddAsync(order);
    await dbContext.SaveChangesAsync();
    
    // Publish event within transaction
    await _capPublisher.PublishAsync("order.created", order);
}
```

### Consumer Groups

```csharp
[CapSubscribe("order.created", Group = "order-processing-group")]
public async Task ProcessOrder(Order order)
{
    // Only one instance in the group will process this message
}
```

### Delayed Messages

```csharp
await _capPublisher.PublishDelayAsync(
    TimeSpan.FromMinutes(5), 
    "order.reminder", 
    orderId
);
```

## Troubleshooting

### Common Issues

1. **Messages not being processed**: Check consumer group configuration and ensure subscribers are registered
2. **Duplicate messages**: Verify idempotency handling in subscribers
3. **Connection issues**: Validate message queue and database connection strings
4. **Performance problems**: Consider consumer group sizing and parallel processing settings

### Monitoring

Use the CAP dashboard to monitor message status:
- Access at `/cap` by default
- View published and received messages
- Manually retry failed messages
- Monitor system health

## References

See [references/](references/) for detailed documentation on:
- [Configuration options](references/configuration.md)
- [Message patterns](references/patterns.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [API reference](references/api.md)