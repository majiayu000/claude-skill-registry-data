---
name: grpc-client-dev
version: 1.0.0
category: technical
description: gRPC client development patterns for Braiins OS miners - connection pooling, retry logic, stream handling, and error recovery
triggers:
  - "gRPC client"
  - "connection pool"
  - "retry logic"
  - "gRPC stream"
  - "miner connection"
  - "gRPC error handling"
dependencies:
  - mcp-server-dev
author: Engineering Standards Committee
last_updated: 2025-12-29
---

# gRPC Client Development Skill

## Description

This skill provides comprehensive patterns for building robust gRPC clients that communicate with Braiins OS miners. It covers connection pooling, intelligent retry strategies, stream handling for real-time updates, and error recovery specific to mining hardware.

**Core Capabilities:**
- Connection pool management for fleet-scale operations
- Exponential backoff retry logic for transient failures
- Bidirectional stream handling for real-time miner data
- Circuit breaker patterns for unreachable miners
- TLS/mTLS configuration for secure communication
- Health checking and connection lifecycle management

---

## When to Use This Skill

**Use this skill when you need to:**
- Implement gRPC communication with Braiins OS miners
- Create connection pools for efficient fleet management
- Handle transient network failures with retry logic
- Stream real-time data from miners (hashrate, temperature, status)
- Recover gracefully from miner downtime or network issues
- Integrate gRPC clients with MCP server architecture

**Trigger Phrases:**
- "Create gRPC client for miner communication"
- "Implement connection pooling for fleet operations"
- "Add retry logic for miner API calls"
- "Stream miner status updates via gRPC"
- "Handle gRPC connection failures"

**Don't use this skill for:**
- REST API clients (use standard HTTP patterns)
- WebSocket connections (different protocol)
- Database connections (use database-specific pooling)
- Redis pub/sub (covered in redis-caching-patterns skill)

---

## Prerequisites

### Knowledge Requirements
1. **gRPC Fundamentals**
   - Understanding of Protocol Buffers (protobuf)
   - Client-server RPC concepts
   - Unary vs streaming RPCs
   - Metadata and headers in gRPC

2. **TypeScript/Node.js**
   - Async/await patterns
   - Promise handling and error propagation
   - Event emitters and streams
   - TypeScript interfaces and generics

3. **Braiins OS Context**
   - Miner API structure (see braiins-os skill)
   - Common miner operations (status, configuration, firmware)
   - Network characteristics (miners on local networks, VPNs, edge devices)

### Environment Setup
```typescript
// Required dependencies in package.json
{
  "@grpc/grpc-js": "^1.9.0",
  "@grpc/proto-loader": "^0.7.10",
  "google-protobuf": "^3.21.0"
}
```

### Project Context
- MCP server architecture understanding (see mcp-server-dev skill)
- Existing miner repository patterns
- Cache integration points (Redis for connection state)

---

## Workflow

### Phase 1: Connection Pool Architecture

#### 1.1 Define Pool Configuration

**Pattern: Configuration-Based Pool Management**

```typescript
// src/api/grpc/pool-config.ts
export interface GrpcPoolConfig {
  // Pool sizing
  maxConnections: number;           // Max concurrent connections
  minConnections: number;           // Min connections to maintain
  connectionTTL: number;            // Time-to-live in milliseconds

  // Connection behavior
  keepaliveTime: number;            // Keepalive ping interval
  keepaliveTimeout: number;         // Keepalive timeout
  enableKeepalive: boolean;         // Enable keepalive pings

  // Retry configuration
  maxRetries: number;               // Max retry attempts
  initialRetryDelay: number;        // Initial delay in ms
  maxRetryDelay: number;            // Max delay cap in ms
  retryBackoffFactor: number;       // Exponential backoff multiplier

  // TLS configuration
  useTls: boolean;                  // Enable TLS
  tlsCert?: Buffer;                 // Client certificate
  tlsKey?: Buffer;                  // Client private key
  tlsCa?: Buffer;                   // CA certificate

  // Health checking
  healthCheckInterval: number;      // Health check interval in ms
  unhealthyThreshold: number;       // Failures before marking unhealthy
  healthyThreshold: number;         // Successes before marking healthy
}

export const DEFAULT_GRPC_POOL_CONFIG: GrpcPoolConfig = {
  maxConnections: 100,
  minConnections: 5,
  connectionTTL: 300000,            // 5 minutes
  keepaliveTime: 30000,             // 30 seconds
  keepaliveTimeout: 10000,          // 10 seconds
  enableKeepalive: true,
  maxRetries: 3,
  initialRetryDelay: 1000,          // 1 second
  maxRetryDelay: 30000,             // 30 seconds
  retryBackoffFactor: 2,
  useTls: false,
  healthCheckInterval: 60000,       // 1 minute
  unhealthyThreshold: 3,
  healthyThreshold: 2
};
```

**Rationale:**
- **Keepalive enabled**: Miners can drop idle connections; keepalive prevents this
- **Conservative TTL**: Miners are long-running; 5-minute TTL balances freshness and overhead
- **Bounded retry delays**: Prevents indefinite waiting on unresponsive miners
- **Health checking**: Proactively detect and replace unhealthy connections

#### 1.2 Implement Connection Pool

**Pattern: LRU Connection Pool with Health Checking**

```typescript
// src/api/grpc/connection-pool.ts
import * as grpc from '@grpc/grpc-js';
import type { MinerServiceClient } from './proto/miner_grpc_pb';
import type { MinerConfig } from '../../repositories/miner-repository';

interface PooledConnection {
  client: MinerServiceClient;
  minerId: string;
  host: string;
  port: number;
  createdAt: Date;
  lastUsed: Date;
  healthy: boolean;
  failureCount: number;
  successCount: number;
}

export class GrpcConnectionPool {
  private connections: Map<string, PooledConnection> = new Map();
  private config: GrpcPoolConfig;
  private healthCheckTimer?: NodeJS.Timer;

  constructor(config: Partial<GrpcPoolConfig> = {}) {
    this.config = { ...DEFAULT_GRPC_POOL_CONFIG, ...config };
    this.startHealthChecks();
  }

  /**
   * Get or create a connection for a specific miner
   */
  async getConnection(minerId: string, minerConfig: MinerConfig): Promise<MinerServiceClient> {
    const key = this.getConnectionKey(minerId);

    // Check for existing healthy connection
    const existing = this.connections.get(key);
    if (existing && this.isConnectionValid(existing)) {
      existing.lastUsed = new Date();
      return existing.client;
    }

    // Remove stale connection if exists
    if (existing) {
      await this.closeConnection(key);
    }

    // Create new connection
    return this.createConnection(minerId, minerConfig);
  }

  /**
   * Create a new gRPC connection
   */
  private async createConnection(minerId: string, minerConfig: MinerConfig): Promise<MinerServiceClient> {
    // Check pool size limit
    if (this.connections.size >= this.config.maxConnections) {
      this.evictOldest();
    }

    const address = `${minerConfig.host}:${minerConfig.port}`;
    const credentials = this.createCredentials(minerConfig);
    const options = this.createChannelOptions();

    const client = new MinerServiceClient(address, credentials, options);

    const connection: PooledConnection = {
      client,
      minerId,
      host: minerConfig.host,
      port: minerConfig.port,
      createdAt: new Date(),
      lastUsed: new Date(),
      healthy: true,
      failureCount: 0,
      successCount: 0
    };

    const key = this.getConnectionKey(minerId);
    this.connections.set(key, connection);

    return client;
  }

  /**
   * Create gRPC credentials (TLS or insecure)
   */
  private createCredentials(minerConfig: MinerConfig): grpc.ChannelCredentials {
    if (this.config.useTls && minerConfig.useTls) {
      if (this.config.tlsCa && this.config.tlsCert && this.config.tlsKey) {
        return grpc.credentials.createSsl(
          this.config.tlsCa,
          this.config.tlsKey,
          this.config.tlsCert
        );
      }
      return grpc.credentials.createSsl();
    }
    return grpc.credentials.createInsecure();
  }

  /**
   * Create channel options for gRPC client
   */
  private createChannelOptions(): grpc.ChannelOptions {
    return {
      'grpc.keepalive_time_ms': this.config.keepaliveTime,
      'grpc.keepalive_timeout_ms': this.config.keepaliveTimeout,
      'grpc.keepalive_permit_without_calls': this.config.enableKeepalive ? 1 : 0,
      'grpc.http2.max_pings_without_data': 0,
      'grpc.http2.min_time_between_pings_ms': 10000,
      'grpc.http2.min_ping_interval_without_data_ms': 5000
    };
  }

  /**
   * Check if connection is still valid
   */
  private isConnectionValid(connection: PooledConnection): boolean {
    const now = new Date();
    const age = now.getTime() - connection.createdAt.getTime();

    return (
      connection.healthy &&
      age < this.config.connectionTTL &&
      connection.failureCount < this.config.unhealthyThreshold
    );
  }

  /**
   * Evict the oldest (LRU) connection
   */
  private evictOldest(): void {
    let oldestKey: string | null = null;
    let oldestTime = Date.now();

    for (const [key, conn] of this.connections.entries()) {
      if (conn.lastUsed.getTime() < oldestTime) {
        oldestTime = conn.lastUsed.getTime();
        oldestKey = key;
      }
    }

    if (oldestKey) {
      void this.closeConnection(oldestKey);
    }
  }

  /**
   * Close a specific connection
   */
  private async closeConnection(key: string): Promise<void> {
    const connection = this.connections.get(key);
    if (!connection) return;

    connection.client.close();
    this.connections.delete(key);
  }

  /**
   * Mark connection as healthy (after successful call)
   */
  markHealthy(minerId: string): void {
    const key = this.getConnectionKey(minerId);
    const connection = this.connections.get(key);
    if (!connection) return;

    connection.successCount++;
    connection.failureCount = 0;

    if (connection.successCount >= this.config.healthyThreshold) {
      connection.healthy = true;
    }
  }

  /**
   * Mark connection as unhealthy (after failed call)
   */
  markUnhealthy(minerId: string): void {
    const key = this.getConnectionKey(minerId);
    const connection = this.connections.get(key);
    if (!connection) return;

    connection.failureCount++;
    connection.successCount = 0;

    if (connection.failureCount >= this.config.unhealthyThreshold) {
      connection.healthy = false;
    }
  }

  /**
   * Start periodic health checks
   */
  private startHealthChecks(): void {
    this.healthCheckTimer = setInterval(() => {
      void this.performHealthChecks();
    }, this.config.healthCheckInterval);
  }

  /**
   * Perform health checks on all connections
   */
  private async performHealthChecks(): Promise<void> {
    for (const [key, connection] of this.connections.entries()) {
      if (!this.isConnectionValid(connection)) {
        await this.closeConnection(key);
      }
    }
  }

  /**
   * Get connection key (composite of minerId)
   */
  private getConnectionKey(minerId: string): string {
    return `miner:${minerId}`;
  }

  /**
   * Close all connections and stop health checks
   */
  async dispose(): void {
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
    }

    for (const [key] of this.connections.entries()) {
      await this.closeConnection(key);
    }

    this.connections.clear();
  }

  /**
   * Get pool statistics
   */
  getPoolStats(): {
    totalConnections: number;
    healthyConnections: number;
    unhealthyConnections: number;
  } {
    let healthy = 0;
    let unhealthy = 0;

    for (const connection of this.connections.values()) {
      if (connection.healthy) {
        healthy++;
      } else {
        unhealthy++;
      }
    }

    return {
      totalConnections: this.connections.size,
      healthyConnections: healthy,
      unhealthyConnections: unhealthy
    };
  }
}
```

**Key Design Decisions:**
- **LRU Eviction**: Least recently used connections are evicted when pool is full
- **Health Tracking**: Failures increment counter; successes decrement it
- **Automatic Cleanup**: Periodic health checks remove stale connections
- **Connection Reuse**: Same miner reuses connection until TTL expires

---

### Phase 2: Retry Logic Implementation

#### 2.1 Exponential Backoff Retry

**Pattern: Configurable Retry with Backoff**

```typescript
// src/api/grpc/retry.ts
export interface RetryOptions {
  maxRetries?: number;
  initialDelay?: number;
  maxDelay?: number;
  backoffFactor?: number;
  retryableErrors?: grpc.status[];
  onRetry?: (attempt: number, error: Error) => void;
}

const DEFAULT_RETRY_OPTIONS: Required<RetryOptions> = {
  maxRetries: 3,
  initialDelay: 1000,
  maxDelay: 30000,
  backoffFactor: 2,
  retryableErrors: [
    grpc.status.UNAVAILABLE,
    grpc.status.DEADLINE_EXCEEDED,
    grpc.status.RESOURCE_EXHAUSTED,
    grpc.status.ABORTED
  ],
  onRetry: () => { /* noop */ }
};

/**
 * Execute a gRPC call with exponential backoff retry logic
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const config = { ...DEFAULT_RETRY_OPTIONS, ...options };
  let lastError: Error;
  let delay = config.initialDelay;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if error is retryable
      if (!isRetryableError(error as grpc.ServiceError, config.retryableErrors)) {
        throw error;
      }

      // Don't wait after last attempt
      if (attempt < config.maxRetries) {
        config.onRetry(attempt + 1, lastError);
        await sleep(delay);
        delay = Math.min(delay * config.backoffFactor, config.maxDelay);
      }
    }
  }

  throw new Error(
    `gRPC call failed after ${config.maxRetries} retries: ${lastError!.message}`
  );
}

/**
 * Check if a gRPC error is retryable
 */
function isRetryableError(error: grpc.ServiceError, retryableStatuses: grpc.status[]): boolean {
  return retryableStatuses.includes(error.code);
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

**Usage Example:**
```typescript
// Example: Get miner status with retry
const status = await withRetry(
  () => grpcClient.getStatus(minerId),
  {
    maxRetries: 3,
    initialDelay: 1000,
    backoffFactor: 2,
    onRetry: (attempt, error) => {
      logger.warn(`Retry attempt ${attempt} for miner ${minerId}:`, error);
    }
  }
);
```

#### 2.2 Circuit Breaker Pattern

**Pattern: Prevent Cascading Failures**

```typescript
// src/api/grpc/circuit-breaker.ts
export enum CircuitState {
  CLOSED = 'CLOSED',     // Normal operation
  OPEN = 'OPEN',         // Failing, rejecting requests
  HALF_OPEN = 'HALF_OPEN' // Testing if service recovered
}

export interface CircuitBreakerOptions {
  failureThreshold: number;       // Failures before opening circuit
  successThreshold: number;       // Successes to close circuit from half-open
  timeout: number;                // Time to wait before moving to half-open
  monitoringPeriod: number;       // Window for failure counting
}

export class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failures: number = 0;
  private successes: number = 0;
  private lastFailureTime: Date | null = null;
  private config: CircuitBreakerOptions;

  constructor(config: Partial<CircuitBreakerOptions> = {}) {
    this.config = {
      failureThreshold: 5,
      successThreshold: 2,
      timeout: 60000, // 1 minute
      monitoringPeriod: 120000, // 2 minutes
      ...config
    };
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (this.shouldAttemptReset()) {
        this.state = CircuitState.HALF_OPEN;
      } else {
        throw new Error('Circuit breaker is OPEN - service unavailable');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failures = 0;

    if (this.state === CircuitState.HALF_OPEN) {
      this.successes++;
      if (this.successes >= this.config.successThreshold) {
        this.state = CircuitState.CLOSED;
        this.successes = 0;
      }
    }
  }

  private onFailure(): void {
    this.failures++;
    this.lastFailureTime = new Date();
    this.successes = 0;

    if (this.failures >= this.config.failureThreshold) {
      this.state = CircuitState.OPEN;
    }
  }

  private shouldAttemptReset(): boolean {
    if (!this.lastFailureTime) return false;

    const timeSinceLastFailure = Date.now() - this.lastFailureTime.getTime();
    return timeSinceLastFailure >= this.config.timeout;
  }

  getState(): CircuitState {
    return this.state;
  }

  reset(): void {
    this.state = CircuitState.CLOSED;
    this.failures = 0;
    this.successes = 0;
    this.lastFailureTime = null;
  }
}
```

**Integration with Connection Pool:**
```typescript
// Add circuit breaker per miner
private circuitBreakers: Map<string, CircuitBreaker> = new Map();

async callWithCircuitBreaker<T>(
  minerId: string,
  fn: (client: MinerServiceClient) => Promise<T>
): Promise<T> {
  const circuitBreaker = this.getOrCreateCircuitBreaker(minerId);

  return circuitBreaker.execute(async () => {
    const client = await this.getConnection(minerId, minerConfig);
    try {
      const result = await withRetry(() => fn(client));
      this.markHealthy(minerId);
      return result;
    } catch (error) {
      this.markUnhealthy(minerId);
      throw error;
    }
  });
}
```

---

### Phase 3: Stream Handling

#### 3.1 Server Streaming (Real-Time Miner Updates)

**Pattern: Server Stream with Backpressure**

```typescript
// src/api/grpc/stream-handler.ts
import { EventEmitter } from 'events';

export class MinerStatusStream extends EventEmitter {
  private stream: grpc.ClientReadableStream<MinerStatus> | null = null;
  private reconnectTimer?: NodeJS.Timer;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  constructor(
    private pool: GrpcConnectionPool,
    private minerId: string,
    private minerConfig: MinerConfig
  ) {
    super();
  }

  async start(): Promise<void> {
    try {
      const client = await this.pool.getConnection(this.minerId, this.minerConfig);

      this.stream = client.streamStatus({ minerId: this.minerId });

      this.stream.on('data', (status: MinerStatus) => {
        this.reconnectAttempts = 0; // Reset on successful data
        this.emit('status', status);
      });

      this.stream.on('end', () => {
        this.emit('end');
        this.attemptReconnect();
      });

      this.stream.on('error', (error: grpc.ServiceError) => {
        this.emit('error', error);
        if (this.isRetryableStreamError(error)) {
          this.attemptReconnect();
        }
      });

    } catch (error) {
      this.emit('error', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.emit('maxReconnectAttemptsReached');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

    this.reconnectTimer = setTimeout(() => {
      void this.start();
    }, delay);
  }

  private isRetryableStreamError(error: grpc.ServiceError): boolean {
    return [
      grpc.status.UNAVAILABLE,
      grpc.status.DEADLINE_EXCEEDED,
      grpc.status.INTERNAL
    ].includes(error.code);
  }

  stop(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    if (this.stream) {
      this.stream.cancel();
      this.stream = null;
    }

    this.removeAllListeners();
  }
}
```

**Usage in MCP Resource:**
```typescript
// Example: MCP resource for streaming miner status
@resource({
  uri: "braiins:///miner/{minerId}/status/stream",
  name: "Miner Status Stream",
  mimeType: "application/json"
})
async getMinerStatusStream(minerId: string): Promise<AsyncIterable<MinerStatus>> {
  const stream = new MinerStatusStream(this.pool, minerId, minerConfig);

  await stream.start();

  return {
    [Symbol.asyncIterator]() {
      return {
        next: () => new Promise((resolve, reject) => {
          stream.once('status', (status) => {
            resolve({ value: status, done: false });
          });
          stream.once('end', () => {
            resolve({ value: undefined, done: true });
          });
          stream.once('error', reject);
        })
      };
    }
  };
}
```

---

### Phase 4: Error Handling

#### 4.1 gRPC Error Classification

**Pattern: Actionable Error Messages for Agents**

```typescript
// src/api/grpc/errors.ts
import { MCPError } from '../../utils/errors';

export class GrpcMinerError extends MCPError {
  constructor(
    public readonly minerId: string,
    public readonly grpcCode: grpc.status,
    message: string,
    details?: Record<string, unknown>
  ) {
    super({
      code: grpcCodeToMCPErrorCode(grpcCode),
      message: `Miner ${minerId}: ${message}`,
      details: {
        grpcCode: grpc.status[grpcCode],
        ...details,
        suggestion: getSuggestionForError(grpcCode)
      }
    });
  }
}

function grpcCodeToMCPErrorCode(code: grpc.status): string {
  const mapping: Record<number, string> = {
    [grpc.status.UNAVAILABLE]: 'MINER_UNREACHABLE',
    [grpc.status.DEADLINE_EXCEEDED]: 'MINER_TIMEOUT',
    [grpc.status.UNAUTHENTICATED]: 'MINER_AUTH_FAILED',
    [grpc.status.PERMISSION_DENIED]: 'MINER_PERMISSION_DENIED',
    [grpc.status.NOT_FOUND]: 'MINER_NOT_FOUND',
    [grpc.status.INVALID_ARGUMENT]: 'INVALID_MINER_REQUEST',
    [grpc.status.RESOURCE_EXHAUSTED]: 'MINER_OVERLOADED'
  };

  return mapping[code] || 'MINER_GRPC_ERROR';
}

function getSuggestionForError(code: grpc.status): string {
  const suggestions: Record<number, string> = {
    [grpc.status.UNAVAILABLE]:
      "Check miner network connectivity. Try 'ping_miner' or 'list_miners' to see reachable miners.",
    [grpc.status.DEADLINE_EXCEEDED]:
      "Miner is slow to respond. Check if miner is under heavy load or increase timeout.",
    [grpc.status.UNAUTHENTICATED]:
      "Authentication failed. Verify miner credentials in configuration.",
    [grpc.status.PERMISSION_DENIED]:
      "Permission denied. Check miner user has required permissions.",
    [grpc.status.NOT_FOUND]:
      "Miner resource not found. Verify miner ID and that miner is registered.",
    [grpc.status.RESOURCE_EXHAUSTED]:
      "Miner is overloaded. Reduce request rate or check miner health."
  };

  return suggestions[code] || "Retry the operation or check miner logs for details.";
}

/**
 * Wrap gRPC calls with error transformation
 */
export async function wrapGrpcCall<T>(
  minerId: string,
  fn: () => Promise<T>,
  operation: string
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (isGrpcError(error)) {
      throw new GrpcMinerError(
        minerId,
        error.code,
        `${operation} failed: ${error.message}`,
        { operation }
      );
    }
    throw error;
  }
}

function isGrpcError(error: unknown): error is grpc.ServiceError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'details' in error
  );
}
```

---

## Examples

### Example 1: Basic gRPC Client with Pool

```typescript
// src/api/grpc/miner-client.ts
import { GrpcConnectionPool } from './connection-pool';
import { withRetry } from './retry';
import { wrapGrpcCall } from './errors';

export class BraiinsMinerClient {
  private pool: GrpcConnectionPool;

  constructor(config?: Partial<GrpcPoolConfig>) {
    this.pool = new GrpcConnectionPool(config);
  }

  async getMinerStatus(minerId: string, minerConfig: MinerConfig): Promise<MinerStatus> {
    return wrapGrpcCall(minerId, async () => {
      const client = await this.pool.getConnection(minerId, minerConfig);

      const status = await withRetry(
        () => new Promise<MinerStatus>((resolve, reject) => {
          client.getStatus({ minerId }, (error, response) => {
            if (error) reject(error);
            else resolve(response);
          });
        }),
        { maxRetries: 3, onRetry: (attempt) => {
          logger.debug(`Retry ${attempt} for getMinerStatus(${minerId})`);
        }}
      );

      this.pool.markHealthy(minerId);
      return status;
    }, 'getMinerStatus');
  }

  async updateMinerConfig(
    minerId: string,
    minerConfig: MinerConfig,
    newConfig: MinerConfiguration
  ): Promise<void> {
    return wrapGrpcCall(minerId, async () => {
      const client = await this.pool.getConnection(minerId, minerConfig);

      await withRetry(
        () => new Promise<void>((resolve, reject) => {
          client.updateConfiguration({ minerId, config: newConfig }, (error) => {
            if (error) reject(error);
            else resolve();
          });
        }),
        { maxRetries: 2 } // Fewer retries for mutations
      );

      this.pool.markHealthy(minerId);
    }, 'updateMinerConfig');
  }

  dispose(): void {
    void this.pool.dispose();
  }
}
```

### Example 2: Fleet Operation with Parallel Calls

```typescript
// Example: Get status for all miners in fleet
async getFleetStatus(minerIds: string[]): Promise<Map<string, MinerStatus>> {
  const results = new Map<string, MinerStatus>();

  // Execute in parallel with Promise.allSettled
  const promises = minerIds.map(async (minerId) => {
    try {
      const minerConfig = await this.minerRepo.findById(minerId);
      if (!minerConfig) {
        throw new Error(`Miner ${minerId} not found`);
      }

      const status = await this.getMinerStatus(minerId, minerConfig);
      results.set(minerId, status);
    } catch (error) {
      logger.error(`Failed to get status for ${minerId}:`, error);
      // Continue with other miners
    }
  });

  await Promise.allSettled(promises);

  return results;
}
```

### Example 3: Real-Time Stream Integration

```typescript
// Example: Subscribe to miner updates via Redis pub/sub
async subscribeToMinerUpdates(minerId: string): Promise<void> {
  const stream = new MinerStatusStream(this.pool, minerId, minerConfig);

  stream.on('status', async (status: MinerStatus) => {
    // Publish to Redis for MCP resource subscribers
    await this.redis.publish(
      `miner:${minerId}:status`,
      JSON.stringify(status)
    );

    // Update cache
    await this.redis.setex(
      `cache:miner:${minerId}:status`,
      30, // 30 second TTL
      JSON.stringify(status)
    );
  });

  stream.on('error', (error) => {
    logger.error(`Stream error for miner ${minerId}:`, error);
  });

  stream.on('maxReconnectAttemptsReached', () => {
    logger.warn(`Max reconnect attempts reached for miner ${minerId}`);
    // Mark miner as offline in database
  });

  await stream.start();
}
```

---

## Quality Standards

### Code Quality Checklist

- [ ] **Connection Pooling**
  - [ ] Pool size is configurable and enforced
  - [ ] LRU eviction implemented for max connections
  - [ ] Connections have TTL and are automatically refreshed
  - [ ] Health checks run periodically

- [ ] **Retry Logic**
  - [ ] Exponential backoff implemented
  - [ ] Max retry delay is capped
  - [ ] Only retryable errors trigger retries
  - [ ] Circuit breaker prevents cascading failures

- [ ] **Error Handling**
  - [ ] All gRPC errors are caught and transformed to MCPError
  - [ ] Error messages include actionable suggestions for agents
  - [ ] Non-retryable errors fail fast
  - [ ] Errors include context (minerId, operation, grpcCode)

- [ ] **Streaming**
  - [ ] Stream reconnection logic implemented
  - [ ] Backpressure handled appropriately
  - [ ] Stream resources cleaned up on close
  - [ ] Max reconnect attempts enforced

- [ ] **TLS Security**
  - [ ] TLS credentials properly configured
  - [ ] Certificate validation enabled
  - [ ] Credentials not hardcoded

- [ ] **Performance**
  - [ ] Keepalive prevents idle connection drops
  - [ ] Parallel fleet operations use Promise.allSettled
  - [ ] Connection reuse minimizes handshake overhead

### Testing Requirements

```typescript
// Example test structure
describe('GrpcConnectionPool', () => {
  it('should reuse connections for same miner', async () => {
    const client1 = await pool.getConnection('miner-1', config);
    const client2 = await pool.getConnection('miner-1', config);
    expect(client1).toBe(client2);
  });

  it('should evict oldest connection when pool is full', async () => {
    // Create max connections
    // Create one more
    // Verify oldest was evicted
  });

  it('should mark connection unhealthy after threshold failures', async () => {
    // Simulate failures
    // Verify connection marked unhealthy
  });
});

describe('withRetry', () => {
  it('should retry on UNAVAILABLE error', async () => {
    let attempts = 0;
    await withRetry(async () => {
      attempts++;
      if (attempts < 3) throw new GrpcError(grpc.status.UNAVAILABLE);
      return 'success';
    });
    expect(attempts).toBe(3);
  });

  it('should not retry on INVALID_ARGUMENT error', async () => {
    await expect(
      withRetry(() => {
        throw new GrpcError(grpc.status.INVALID_ARGUMENT);
      })
    ).rejects.toThrow();
  });
});
```

---

## Common Pitfalls

### ❌ Pitfall 1: Not Closing Connections

**Problem**: Connections left open lead to resource exhaustion

```typescript
// BAD: Connection never closed
async function badExample() {
  const client = new MinerServiceClient(address, credentials);
  const status = await client.getStatus({ minerId });
  // Connection never closed!
  return status;
}
```

**Solution**: Use connection pool with automatic cleanup

```typescript
// GOOD: Pool manages lifecycle
async function goodExample() {
  const client = await pool.getConnection(minerId, config);
  const status = await client.getStatus({ minerId });
  // Pool keeps connection open for reuse or closes on TTL
  return status;
}
```

### ❌ Pitfall 2: Unbounded Retries

**Problem**: Indefinite retries on permanently failed miners

```typescript
// BAD: Will retry forever
async function badRetry() {
  while (true) {
    try {
      return await client.getStatus({ minerId });
    } catch (error) {
      await sleep(1000);
      // Retries forever!
    }
  }
}
```

**Solution**: Use exponential backoff with max attempts and circuit breaker

```typescript
// GOOD: Bounded retries with circuit breaker
async function goodRetry() {
  return withRetry(
    () => client.getStatus({ minerId }),
    { maxRetries: 3, backoffFactor: 2 }
  );
}
```

### ❌ Pitfall 3: Ignoring Stream Errors

**Problem**: Stream errors not handled, causing silent failures

```typescript
// BAD: No error handling
const stream = client.streamStatus({ minerId });
stream.on('data', (status) => {
  console.log(status);
});
// Stream errors not handled!
```

**Solution**: Always handle stream errors and implement reconnection

```typescript
// GOOD: Complete error handling
const stream = new MinerStatusStream(pool, minerId, config);

stream.on('data', (status) => processStatus(status));
stream.on('error', (error) => logger.error('Stream error:', error));
stream.on('end', () => stream.attemptReconnect());
stream.on('maxReconnectAttemptsReached', () => markMinerOffline(minerId));

await stream.start();
```

---

## Integration with MCP Server

### Pattern: gRPC Client as MCP Tool Dependency

```typescript
// src/mcp/tools/get-miner-status.ts
import { BraiinsMinerClient } from '../../api/grpc/miner-client';

@tool({
  name: "get_miner_status",
  description: "Get current status of a Braiins OS miner",
  inputSchema: z.object({
    minerId: z.string(),
    includeDetails: z.boolean().optional()
  })
})
async getMinerStatus(params: { minerId: string; includeDetails?: boolean }) {
  // Use gRPC client with pooling and retries
  const status = await this.grpcClient.getMinerStatus(params.minerId, minerConfig);

  return {
    minerId: params.minerId,
    online: status.status === 'running',
    hashrate: `${status.hashrate} TH/s`,
    temperature: `${status.temperature}°C`,
    // Include detailed info if requested
    ...(params.includeDetails && { details: status })
  };
}
```

---

## References

- **gRPC Node.js Documentation**: https://grpc.io/docs/languages/node/
- **Braiins OS API**: See `.claude/skills/braiins-os/` skill
- **MCP Server Patterns**: See `.claude/skills/mcp-server-dev/` skill
- **Connection Pooling Best Practices**: https://grpc.io/docs/guides/performance/
- **Retry Strategies**: Exponential backoff with jitter
- **Circuit Breaker Pattern**: Release It! by Michael Nygard

---

**Version History**:
- 1.0.0 (2025-12-29): Initial release - Connection pooling, retry logic, stream handling
