---
name: cosmosdb-sdk
description: >
  Azure Cosmos DB SDK best practices for .NET, Java, Python, Spring Boot, and
  LangChain: singleton client, async APIs, connection modes, retry handling,
  diagnostics, serialization, emulator configuration, ETags,
  and framework-specific patterns.
  USE FOR: CosmosClient singleton, async API, Direct vs Gateway mode, retry 429,
  preferred regions, excluded regions, availability strategy, circuit breaker,
  SDK diagnostics, serialization enums, emulator SSL, ETag concurrency,
  conditional create, patch increment, continuation token, content response,
  Spring Data Cosmos, Spring Boot versions, Newtonsoft dependency, namespace collision,
  Python async deps, local dev config, LangChain Cosmos DB saver, LangGraph checkpointer,
  MCP persistent session, tool content format, tool filtering,
  LangChain JS vectorstore, chat history, semantic cache.
  DO NOT USE FOR: data modeling (use cosmosdb-data-modeling), queries (use cosmosdb-query-optimization),
  partition keys (use cosmosdb-partition-key).
---

# Azure Cosmos DB SDK Best Practices

SDK usage patterns and framework-specific guidance for Azure Cosmos DB across .NET, Java, Python, Spring Boot, and LangChain.

## When to Apply

Reference these guidelines when:
- Configuring CosmosClient instances
- Choosing connection modes (Direct vs Gateway)
- Handling retries and throttling
- Setting up the Cosmos DB Emulator
- Using ETags for optimistic concurrency
- Integrating with Spring Boot or LangChain
- Configuring availability and resilience features

## Rules

- [sdk-singleton-client](references/sdk-singleton-client.md) - Reuse CosmosClient as singleton
- [sdk-async-api](references/sdk-async-api.md) - Use async APIs for throughput
- [sdk-retry-429](references/sdk-retry-429.md) - Handle 429s with retry-after
- [sdk-connection-mode](references/sdk-connection-mode.md) - Use Direct mode for production
- [sdk-preferred-regions](references/sdk-preferred-regions.md) - Configure preferred regions
- [sdk-excluded-regions](references/sdk-excluded-regions.md) - Exclude regions experiencing issues
- [sdk-availability-strategy](references/sdk-availability-strategy.md) - Configure availability strategy
- [sdk-circuit-breaker](references/sdk-circuit-breaker.md) - Use circuit breaker for fault tolerance
- [sdk-diagnostics](references/sdk-diagnostics.md) - Log diagnostics for troubleshooting
- [sdk-serialization-enums](references/sdk-serialization-enums.md) - Serialize enums as strings
- [sdk-emulator-ssl](references/sdk-emulator-ssl.md) - Configure SSL for Cosmos DB Emulator
- [sdk-etag-concurrency](references/sdk-etag-concurrency.md) - Use ETags for optimistic concurrency
- [sdk-conditional-create-etag](references/sdk-conditional-create-etag.md) - Reject duplicates atomically
- [sdk-request-options-per-call](references/sdk-request-options-per-call.md) - Never reuse request options
- [sdk-patch-counter-increment](references/sdk-patch-counter-increment.md) - Use patch incr for atomic counters
- [sdk-continuation-token-null-guard](references/sdk-continuation-token-null-guard.md) - Guard empty continuation tokens
- [sdk-java-content-response](references/sdk-java-content-response.md) - Enable content response on writes (Java)
- [sdk-java-cosmos-config](references/sdk-java-cosmos-config.md) - Configure Cosmos DB in Spring Boot
- [sdk-java-spring-boot-versions](references/sdk-java-spring-boot-versions.md) - Match Java to Spring Boot versions
- [sdk-local-dev-config](references/sdk-local-dev-config.md) - Configure local development
- [sdk-dotnet-cosmos-package-id](references/sdk-dotnet-cosmos-package-id.md) - Use correct NuGet package
- [sdk-newtonsoft-dependency](references/sdk-newtonsoft-dependency.md) - Reference Newtonsoft.Json explicitly
- [sdk-python-async-deps](references/sdk-python-async-deps.md) - Include aiohttp for Python async
- [sdk-go-partition-key-metadata](references/sdk-go-partition-key-metadata.md) - Use current Go SDK with explicit partition-key metadata
- [sdk-spring-data-annotations](references/sdk-spring-data-annotations.md) - Annotate entities for Spring Data
- [sdk-spring-data-repository](references/sdk-spring-data-repository.md) - Use CosmosRepository correctly
- [sdk-dotnet-namespace-collision](references/sdk-dotnet-namespace-collision.md) - Avoid namespace collisions
- [sdk-langchain-cosmosdb-saver](references/sdk-langchain-cosmosdb-saver.md) - CosmosDBSaver for LangGraph
- [sdk-langchain-async-checkpointer](references/sdk-langchain-async-checkpointer.md) - Async container init
- [sdk-langchain-mcp-persistent-session](references/sdk-langchain-mcp-persistent-session.md) - Persistent MCP sessions
- [sdk-langchain-mcp-tool-content-format](references/sdk-langchain-mcp-tool-content-format.md) - MCP tool content format
- [sdk-langgraph-mcp-tool-filtering](references/sdk-langgraph-mcp-tool-filtering.md) - Filter MCP tools by prefix
- [sdk-langchain-js-vectorstore-init](references/sdk-langchain-js-vectorstore-init.md) - LangChain JS vectorstore init
- [sdk-langchain-js-chat-history](references/sdk-langchain-js-chat-history.md) - LangChain JS chat history
- [sdk-langchain-js-embedding-model](references/sdk-langchain-js-embedding-model.md) - LangChain JS embedding model
- [sdk-langchain-js-filter-injection](references/sdk-langchain-js-filter-injection.md) - LangChain JS filter injection
- [sdk-langchain-js-fulltext-prerequisites](references/sdk-langchain-js-fulltext-prerequisites.md) - LangChain JS FTS prerequisites
- [sdk-langchain-js-managed-identity](references/sdk-langchain-js-managed-identity.md) - LangChain JS managed identity
- [sdk-langchain-js-search-types](references/sdk-langchain-js-search-types.md) - LangChain JS search types
- [sdk-langchain-js-semantic-cache](references/sdk-langchain-js-semantic-cache.md) - LangChain JS semantic cache
