---
name: consumer-driven-contracts
description: Design consumer-driven contracts using Pact framework
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Consumer-Driven Contracts Skill

## When to Use This Skill

Use this skill when:

- **Consumer Driven Contracts tasks** - Working on design consumer-driven contracts using pact framework
- **Planning or design** - Need guidance on Consumer Driven Contracts approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design and implement consumer-driven contracts using the Pact framework.

## MANDATORY: Documentation-First Approach

Before designing consumer contracts:

1. **Invoke `docs-management` skill** for contract testing patterns
2. **Verify Pact patterns** via MCP servers (context7, perplexity)
3. **Base guidance on Pact documentation and CDC best practices**

## What Are Consumer-Driven Contracts?

```text
CONSUMER-DRIVEN CONTRACTS (CDC):

Traditional Approach:
┌──────────────────────────────────────────────────────────┐
│ Provider defines API → Consumers adapt → Integration test│
│                                                          │
│ Problems:                                                │
│ • Provider doesn't know consumer needs                   │
│ • Breaking changes discovered late                       │
│ • Heavy integration test burden                          │
└──────────────────────────────────────────────────────────┘

Consumer-Driven Approach:
┌──────────────────────────────────────────────────────────┐
│ Consumer defines expectations → Provider verifies        │
│                                                          │
│ Benefits:                                                │
│ • Consumer needs drive API evolution                     │
│ • Breaking changes caught early                          │
│ • Lightweight, fast tests                                │
│ • Independent deployment                                 │
└──────────────────────────────────────────────────────────┘
```

## Pact Workflow

```text
PACT WORKFLOW:

                    CONSUMER SIDE                      PROVIDER SIDE
                    ─────────────                      ─────────────
┌────────────────────────────────────┐    ┌────────────────────────────────────┐
│                                    │    │                                    │
│  1. Consumer writes tests          │    │  4. Provider fetches contract     │
│     ┌─────────────────────────┐    │    │     ┌─────────────────────────┐    │
│     │ "When I request GET     │    │    │     │ Download contract from  │    │
│     │  /orders/123            │    │    │     │ Pact Broker             │    │
│     │                         │    │    │     └─────────────────────────┘    │
│     │  I expect status 200    │    │    │                                    │
│     │  and body { id: 123 }   │    │    │  5. Provider verifies contract    │
│     └─────────────────────────┘    │    │     ┌─────────────────────────┐    │
│                                    │    │     │ Run real API against    │    │
│  2. Pact mock returns expected     │    │     │ expected interactions   │    │
│     response                       │    │     │                         │    │
│                                    │    │     │ Setup provider state    │    │
│  3. Contract generated             │    │     │ for each scenario       │    │
│     ┌─────────────────────────┐    │    │     └─────────────────────────┘    │
│     │ {                       │    │    │                                    │
│     │   "consumer": "Orders", │    │    │  6. Results published to broker   │
│     │   "provider": "API",    │    │    │     ┌─────────────────────────┐    │
│     │   "interactions": [...]│    │    │     │ ✓ All interactions pass │    │
│     │ }                       │    │    │     │ ✓ Contract verified     │    │
│     └─────────────────────────┘    │    │     └─────────────────────────┘    │
│              │                     │    │                                    │
│              └───────────────────────────────────────────────────────────────┤
│                    Publish to Pact Broker                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Consumer Test Example (C#)

```csharp
// Consumer: OrdersClient tests
// File: OrdersClient.Consumer.Tests/OrdersApiConsumerTests.cs

using PactNet;
using PactNet.Matchers;
using System.Net.Http.Json;

public class OrdersApiConsumerTests : IDisposable
{
    private readonly IPactBuilderV4 _pactBuilder;

    public OrdersApiConsumerTests()
    {
        var config = new PactConfig
        {
            PactDir = "../../../pacts/",
            LogLevel = PactLogLevel.Debug
        };

        var pact = Pact.V4("OrdersClient", "OrdersApi", config);
        _pactBuilder = pact.WithHttpInteractions();
    }

    [Fact]
    public async Task GetOrder_WhenOrderExists_ReturnsOrder()
    {
        // Arrange
        var orderId = "123";
        var expectedOrder = new
        {
            id = orderId,
            customerId = Match.Type("customer-456"),
            items = Match.MinType(new { productId = "prod-1", quantity = 1 }, 1),
            status = Match.Regex("Pending|Processing|Shipped", "Pending"),
            total = Match.Decimal(99.99m),
            createdAt = Match.Type(DateTime.UtcNow)
        };

        _pactBuilder
            .UponReceiving("a request for an existing order")
            .Given("an order with id 123 exists")
            .WithRequest(HttpMethod.Get, $"/orders/{orderId}")
            .WithHeader("Accept", "application/json")
            .WillRespond()
            .WithStatus(HttpStatusCode.OK)
            .WithHeader("Content-Type", "application/json")
            .WithJsonBody(expectedOrder);

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            // Act
            var client = new OrdersApiClient(ctx.MockServerUri);
            var result = await client.GetOrderAsync(orderId);

            // Assert
            Assert.NotNull(result);
            Assert.Equal(orderId, result.Id);
        });
    }

    [Fact]
    public async Task GetOrder_WhenOrderNotFound_Returns404()
    {
        // Arrange
        var orderId = "non-existent";

        _pactBuilder
            .UponReceiving("a request for a non-existent order")
            .Given("no order with id non-existent exists")
            .WithRequest(HttpMethod.Get, $"/orders/{orderId}")
            .WithHeader("Accept", "application/json")
            .WillRespond()
            .WithStatus(HttpStatusCode.NotFound)
            .WithJsonBody(new { error = "Order not found" });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrdersApiClient(ctx.MockServerUri);

            var exception = await Assert.ThrowsAsync<OrderNotFoundException>(
                () => client.GetOrderAsync(orderId));

            Assert.Equal(orderId, exception.OrderId);
        });
    }

    [Fact]
    public async Task CreateOrder_WithValidData_ReturnsCreatedOrder()
    {
        // Arrange
        var newOrder = new CreateOrderRequest
        {
            CustomerId = "customer-789",
            Items = new[] { new OrderItem("prod-1", 2) }
        };

        _pactBuilder
            .UponReceiving("a request to create a new order")
            .Given("customer customer-789 exists")
            .WithRequest(HttpMethod.Post, "/orders")
            .WithHeader("Content-Type", "application/json")
            .WithJsonBody(new
            {
                customerId = newOrder.CustomerId,
                items = Match.MinType(new { productId = "prod-1", quantity = 2 }, 1)
            })
            .WillRespond()
            .WithStatus(HttpStatusCode.Created)
            .WithHeader("Location", Match.Regex("/orders/.*", "/orders/new-order-id"))
            .WithJsonBody(new
            {
                id = Match.Type("new-order-id"),
                customerId = newOrder.CustomerId,
                status = "Pending"
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrdersApiClient(ctx.MockServerUri);
            var result = await client.CreateOrderAsync(newOrder);

            Assert.NotNull(result);
            Assert.Equal(newOrder.CustomerId, result.CustomerId);
            Assert.Equal("Pending", result.Status);
        });
    }

    public void Dispose()
    {
        // Contract file automatically generated on dispose
    }
}
```

## Pact Matchers

```text
PACT MATCHERS (use instead of exact values):

┌─────────────────────────────────────────────────────────────────┐
│ Matcher          │ Purpose                    │ Example          │
├─────────────────────────────────────────────────────────────────┤
│ Match.Type       │ Match type, not value      │ Match.Type(123)  │
│ Match.Regex      │ Match against regex        │ Match.Regex(...) │
│ Match.MinType    │ Array with min elements    │ Match.MinType    │
│ Match.Include    │ String contains            │ Match.Include(x) │
│ Match.Decimal    │ Decimal number type        │ Match.Decimal(x) │
│ Match.Integer    │ Integer number type        │ Match.Integer(1) │
│ Match.Date       │ ISO date format            │ Match.Date(x)    │
│ Match.DateTime   │ ISO datetime format        │ Match.DateTime   │
│ Match.Null       │ Null value                 │ Match.Null()     │
│ Match.Equality   │ Exact value match          │ Match.Equality   │
└─────────────────────────────────────────────────────────────────┘

GUIDELINES:
• Use matchers liberally - they make contracts more flexible
• Type matchers prevent brittle tests on specific values
• Regex for enums and constrained strings
• MinType for arrays where count varies
```

## Provider States

```text
PROVIDER STATES:

States describe the provider's condition BEFORE the interaction:

"Given an order with id 123 exists"
"Given no order with id non-existent exists"
"Given customer customer-789 exists"
"Given the user is authenticated as admin"

PURPOSE:
• Tell provider what data to set up
• Enable testing different scenarios
• Provider implements state handlers

EXAMPLE STATE HANDLER (C#):

public class OrdersProviderStateHandler : IProviderStateHandler
{
    private readonly OrdersDbContext _context;

    public Task HandleAsync(ProviderState state)
    {
        return state.State switch
        {
            "an order with id 123 exists" =>
                SeedOrder("123", state.Params),
            "no order with id non-existent exists" =>
                Task.CompletedTask, // No setup needed
            "customer customer-789 exists" =>
                SeedCustomer("customer-789"),
            _ => throw new NotSupportedException($"State: {state.State}")
        };
    }
}
```

## Contract Structure

```json
{
  "consumer": {
    "name": "OrdersClient"
  },
  "provider": {
    "name": "OrdersApi"
  },
  "interactions": [
    {
      "description": "a request for an existing order",
      "providerStates": [
        {
          "name": "an order with id 123 exists"
        }
      ],
      "request": {
        "method": "GET",
        "path": "/orders/123",
        "headers": {
          "Accept": "application/json"
        }
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "id": "123",
          "customerId": "customer-456",
          "status": "Pending"
        },
        "matchingRules": {
          "body": {
            "$.customerId": { "match": "type" },
            "$.status": { "match": "regex", "regex": "Pending|Processing|Shipped" }
          }
        }
      }
    }
  ],
  "metadata": {
    "pactSpecification": { "version": "4.0" }
  }
}
```

## Pact Broker Integration

```text
PACT BROKER WORKFLOW:

Consumer Pipeline:
┌─────────────────────────────────────────────────────────────┐
│ 1. Run consumer tests                                       │
│ 2. Generate pact contracts                                  │
│ 3. Publish to Pact Broker                                   │
│    pact-broker publish ./pacts \                           │
│      --broker-base-url https://broker.example.com \        │
│      --consumer-app-version ${GIT_SHA} \                   │
│      --branch ${GIT_BRANCH}                                │
└─────────────────────────────────────────────────────────────┘

Provider Pipeline:
┌─────────────────────────────────────────────────────────────┐
│ 1. Fetch contracts from Pact Broker                        │
│ 2. Verify provider against contracts                       │
│ 3. Publish verification results                            │
│                                                             │
│ Can-I-Deploy check:                                         │
│ pact-broker can-i-deploy \                                 │
│   --pacticipant OrdersApi \                                │
│   --version ${GIT_SHA} \                                   │
│   --to-environment production                              │
└─────────────────────────────────────────────────────────────┘
```

## Consumer Test Guidelines

```text
CONSUMER TEST BEST PRACTICES:

DO:
✓ Write consumer tests from consumer's perspective
✓ Use matchers instead of exact values
✓ Define meaningful provider states
✓ Test only what consumer actually uses
✓ Keep interactions focused and minimal
✓ Include error scenarios (404, 400, 500)

DON'T:
✗ Test provider's internal logic
✗ Duplicate provider's unit tests
✗ Over-specify response bodies
✗ Create contracts for unused fields
✗ Skip provider state descriptions
✗ Use exact values when matchers work
```

## Async/Message Contracts

```csharp
// Consumer test for async/event contracts
public class OrderEventsConsumerTests
{
    [Fact]
    public void ConsumeOrderCreatedEvent_ProcessesCorrectly()
    {
        var pact = Pact.V4("OrderProcessor", "OrdersApi");
        var messagePact = pact.WithMessageInteractions();

        messagePact
            .ExpectsToReceive("an order created event")
            .Given("an order was created")
            .WithJsonContent(new
            {
                eventType = "OrderCreated",
                data = new
                {
                    orderId = Match.Type("order-123"),
                    customerId = Match.Type("customer-456"),
                    createdAt = Match.Type(DateTime.UtcNow)
                }
            })
            .Verify<OrderCreatedEvent>(message =>
            {
                var handler = new OrderCreatedHandler();
                handler.Handle(message);
                // Assert handler processed correctly
            });
    }
}
```

## Assessment Template

```markdown
# Consumer Contract Assessment: [Consumer Name]

## Consumer Profile
- **Consumer:** [Name]
- **Provider:** [Name]
- **Contract Type:** [HTTP/Message/GraphQL]

## Interactions Covered

| Interaction | Provider State | HTTP Method | Path |
|-------------|----------------|-------------|------|
| [Description] | [State] | [Method] | [Path] |

## Matcher Usage

| Field | Matcher Type | Rationale |
|-------|--------------|-----------|
| [Field] | [Type/Regex/etc.] | [Why this matcher] |

## Provider States Required

| State | Setup Required | Notes |
|-------|----------------|-------|
| [State] | [Data needed] | [Notes] |

## Test Quality Checklist

- [ ] Uses matchers instead of exact values
- [ ] Provider states are descriptive
- [ ] Error scenarios included
- [ ] Only consumer's needs tested
- [ ] Interactions are focused
- [ ] Published to Pact Broker

## CI/CD Integration

- [ ] Consumer tests run in pipeline
- [ ] Contracts published automatically
- [ ] Version tagged with git SHA
- [ ] Branch information included
```

## Workflow

When designing consumer contracts:

1. **Identify Interactions**: What does consumer need from provider?
2. **Define Provider States**: What conditions are needed?
3. **Write Consumer Tests**: Generate contracts from expectations
4. **Use Appropriate Matchers**: Avoid brittleness
5. **Publish Contracts**: Send to Pact Broker
6. **Coordinate with Provider**: Ensure state handlers exist

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
