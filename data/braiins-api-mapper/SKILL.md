---
name: braiins-api-mapper
version: 1.0.0
category: api-integration
complexity: moderate
status: active
created: 2025-12-18
author: braiins-pool-mcp-server

description: |
  Maps Braiins Pool API endpoints to MCP tool implementations with proper
  authentication, rate limiting, retry logic, and error handling patterns.

triggers:
  - "map API endpoint"
  - "integrate Braiins API"
  - "connect to pool endpoint"
  - "implement API call"
  - "API client method"

dependencies:
  - braiins-cache-strategist
---

# Braiins API Mapper Skill

## Description

Map Braiins Pool API endpoints from API.md to MCP tool implementations. This skill guides the creation of API client methods with proper authentication, retry logic, rate limiting, and error handling following the patterns defined in ARCHITECTURE.md.

## When to Use This Skill

- When implementing API client methods for new endpoints
- When adding authentication to API calls
- When designing retry and error handling logic
- When mapping response data to MCP tool format
- When implementing rate limiting compliance

## When NOT to Use This Skill

- When designing input schemas (use mcp-schema-designer)
- When designing caching strategy (use braiins-cache-strategist)
- When implementing the full tool handler (use mcp-tool-builder)

## Prerequisites

- API.md contains the endpoint specification
- ARCHITECTURE.md defines client patterns
- HTTP client library available (axios/httpx)
- Environment variables configured for API authentication

---

## API Reference

### Base Configuration

From API.md Section 2 & 3:

```typescript
// Environment variables
const BRAIINS_API_BASE_URL = process.env.BRAIINS_API_BASE_URL || 'https://pool.braiins.com/api/v1';
const BRAIINS_API_TOKEN = process.env.BRAIINS_POOL_API_TOKEN;

// Headers for all requests
const headers = {
  'Authorization': `Bearer ${BRAIINS_API_TOKEN}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};
```

### Endpoint Mapping Table

From API.md Sections 5-7:

| Endpoint | Method | MCP Tool | Auth | Rate Limit |
|----------|--------|----------|------|------------|
| `/user/overview` | GET | getUserOverview | Token | 1/30s |
| `/user/rewards` | GET | getUserRewards | Token | 1/30s |
| `/workers` | GET | listWorkers | Token | 1/30s |
| `/workers/{workerId}` | GET | getWorkerDetails | Token | 1/60s |
| `/workers/{workerId}/hashrate` | GET | getWorkerHashrate | Token | 1/60s |
| `/pool/stats` | GET | getPoolStats | Token | 1/60s |
| `/network/stats` | GET | getNetworkStats | Optional | 1/60s |

---

## Workflow

### Step 1: Analyze Endpoint

Extract from API.md:
- HTTP method
- Path with parameters
- Query parameters
- Authentication requirements
- Rate limit
- Response schema

**Template**:
```markdown
## Endpoint Analysis: {path}

- **Method**: GET
- **Path**: /workers/{workerId}
- **Path Params**: workerId (string, required)
- **Query Params**: none
- **Auth**: Bearer token required
- **Rate Limit**: 1 request per 60 seconds
- **Response**: WorkerDetails object (see Section 6.2)
```

### Step 2: Design Method Signature

```typescript
// src/api/braiinsClient.ts

interface BraiinsClient {
  // User endpoints
  getUserOverview(): Promise<UserOverviewResponse>;
  getUserRewards(params?: GetUserRewardsParams): Promise<UserRewardsResponse>;

  // Worker endpoints
  listWorkers(params?: ListWorkersParams): Promise<WorkerListResponse>;
  getWorkerDetails(workerId: string): Promise<WorkerDetailsResponse>;
  getWorkerHashrate(workerId: string, params?: TimeRangeParams): Promise<WorkerHashrateResponse>;

  // Pool/Network endpoints
  getPoolStats(): Promise<PoolStatsResponse>;
  getNetworkStats(): Promise<NetworkStatsResponse>;
}
```

### Step 3: Implement Request Method

**Base Request Pattern**:

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';
import { BraiinsApiError } from '../utils/errors';
import { logger } from '../utils/logger';

class BraiinsClient {
  private client: AxiosInstance;
  private rateLimiter: RateLimiter;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.BRAIINS_API_BASE_URL,
      timeout: 30000, // 30 second timeout
      headers: {
        'Authorization': `Bearer ${process.env.BRAIINS_POOL_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
    });

    this.rateLimiter = new RateLimiter({
      requestsPerSecond: 1,
      burstSize: 5,
    });

    // Add response interceptor for logging
    this.client.interceptors.response.use(
      (response) => {
        logger.debug('API response', {
          path: response.config.url,
          status: response.status,
          duration: response.headers['x-response-time'],
        });
        return response;
      },
      (error) => {
        logger.error('API error', {
          path: error.config?.url,
          status: error.response?.status,
          message: error.message,
        });
        throw error;
      }
    );
  }

  /**
   * Make authenticated request with retry logic
   */
  private async request<T>(
    method: 'GET' | 'POST',
    path: string,
    options?: {
      params?: Record<string, unknown>;
      body?: unknown;
    }
  ): Promise<T> {
    // Wait for rate limiter
    await this.rateLimiter.acquire();

    try {
      const response = await this.retryWithBackoff(async () => {
        return this.client.request<T>({
          method,
          url: path,
          params: options?.params,
          data: options?.body,
        });
      });

      return response.data;
    } catch (error) {
      throw this.transformError(error);
    }
  }

  /**
   * Retry with exponential backoff
   */
  private async retryWithBackoff<T>(
    fn: () => Promise<T>,
    maxRetries = 3,
    baseDelay = 1000
  ): Promise<T> {
    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;

        // Don't retry client errors (4xx)
        if (error instanceof AxiosError && error.response) {
          const status = error.response.status;
          if (status >= 400 && status < 500) {
            throw error;
          }
        }

        // Wait before retry (exponential backoff)
        if (attempt < maxRetries) {
          const delay = baseDelay * Math.pow(2, attempt);
          logger.warn('Retrying request', { attempt: attempt + 1, delay });
          await this.sleep(delay);
        }
      }
    }

    throw lastError;
  }

  /**
   * Transform axios errors to custom errors
   */
  private transformError(error: unknown): BraiinsApiError {
    if (error instanceof AxiosError && error.response) {
      const status = error.response.status;
      const data = error.response.data;

      // Map HTTP status to error code
      const errorMap: Record<number, string> = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        429: 'RATE_LIMITED',
        500: 'SERVER_ERROR',
      };

      return new BraiinsApiError(
        data?.message || error.message,
        errorMap[status] || 'UNKNOWN_ERROR',
        status
      );
    }

    return new BraiinsApiError(
      'Network error',
      'NETWORK_ERROR',
      0
    );
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### Step 4: Implement Endpoint Methods

**Example: getUserOverview**

```typescript
/**
 * Get user overview statistics
 *
 * @see API.md Section 5.1
 * @returns User hashrate, rewards, and worker counts
 */
async getUserOverview(): Promise<UserOverviewResponse> {
  return this.request<UserOverviewResponse>('GET', '/user/overview');
}
```

**Example: listWorkers with pagination/filters**

```typescript
interface ListWorkersParams {
  page?: number;
  pageSize?: number;
  status?: 'active' | 'inactive' | 'all';
  search?: string;
  sortBy?: string;
}

/**
 * List workers with pagination and filtering
 *
 * @see API.md Section 6.1
 * @param params - Pagination and filter options
 * @returns Paginated list of workers
 */
async listWorkers(params?: ListWorkersParams): Promise<WorkerListResponse> {
  return this.request<WorkerListResponse>('GET', '/workers', {
    params: {
      page: params?.page ?? 1,
      page_size: params?.pageSize ?? 50,
      status: params?.status ?? 'all',
      search: params?.search,
      sort_by: params?.sortBy,
    },
  });
}
```

**Example: getWorkerDetails with path parameter**

```typescript
/**
 * Get detailed information for a specific worker
 *
 * @see API.md Section 6.2
 * @param workerId - Unique worker identifier
 * @returns Worker details including hashrate, status, hardware info
 */
async getWorkerDetails(workerId: string): Promise<WorkerDetailsResponse> {
  // Validate workerId to prevent path traversal
  if (!workerId.match(/^[a-zA-Z0-9\-_]+$/)) {
    throw new BraiinsApiError('Invalid worker ID format', 'VALIDATION_ERROR', 400);
  }

  return this.request<WorkerDetailsResponse>('GET', `/workers/${workerId}`);
}
```

**Example: getWorkerHashrate with time range**

```typescript
interface TimeRangeParams {
  from?: string; // ISO 8601
  to?: string;   // ISO 8601
  granularity?: 'minute' | 'hour' | 'day';
}

/**
 * Get hashrate timeseries for a worker
 *
 * @see API.md Section 6.3
 * @param workerId - Unique worker identifier
 * @param params - Time range and granularity options
 * @returns Array of timestamped hashrate values
 */
async getWorkerHashrate(
  workerId: string,
  params?: TimeRangeParams
): Promise<WorkerHashrateResponse> {
  if (!workerId.match(/^[a-zA-Z0-9\-_]+$/)) {
    throw new BraiinsApiError('Invalid worker ID format', 'VALIDATION_ERROR', 400);
  }

  return this.request<WorkerHashrateResponse>('GET', `/workers/${workerId}/hashrate`, {
    params: {
      from: params?.from,
      to: params?.to,
      granularity: params?.granularity ?? 'hour',
    },
  });
}
```

### Step 5: Write Tests

```typescript
// tests/unit/api/braiinsClient.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BraiinsClient } from '../../../src/api/braiinsClient';
import nock from 'nock';

describe('BraiinsClient', () => {
  let client: BraiinsClient;

  beforeEach(() => {
    client = new BraiinsClient();
    nock.cleanAll();
  });

  describe('getUserOverview', () => {
    it('should return user overview on success', async () => {
      const mockResponse = {
        username: 'test_user',
        hashrate: { current: 100000000000000 },
      };

      nock(process.env.BRAIINS_API_BASE_URL!)
        .get('/user/overview')
        .reply(200, mockResponse);

      const result = await client.getUserOverview();
      expect(result).toEqual(mockResponse);
    });

    it('should throw on 401 unauthorized', async () => {
      nock(process.env.BRAIINS_API_BASE_URL!)
        .get('/user/overview')
        .reply(401, { message: 'Invalid token' });

      await expect(client.getUserOverview()).rejects.toThrow('UNAUTHORIZED');
    });
  });

  describe('retry logic', () => {
    it('should retry on 500 errors', async () => {
      let attempts = 0;
      nock(process.env.BRAIINS_API_BASE_URL!)
        .get('/user/overview')
        .times(2)
        .reply(() => {
          attempts++;
          return [500, { message: 'Server error' }];
        })
        .get('/user/overview')
        .reply(200, { username: 'test' });

      const result = await client.getUserOverview();
      expect(attempts).toBe(2);
      expect(result.username).toBe('test');
    });

    it('should not retry on 400 errors', async () => {
      let attempts = 0;
      nock(process.env.BRAIINS_API_BASE_URL!)
        .get('/user/overview')
        .reply(() => {
          attempts++;
          return [400, { message: 'Bad request' }];
        });

      await expect(client.getUserOverview()).rejects.toThrow('BAD_REQUEST');
      expect(attempts).toBe(1);
    });
  });

  describe('path parameter validation', () => {
    it('should reject invalid worker ID', async () => {
      await expect(client.getWorkerDetails('../../../etc/passwd')).rejects.toThrow('VALIDATION_ERROR');
    });

    it('should accept valid worker ID', async () => {
      nock(process.env.BRAIINS_API_BASE_URL!)
        .get('/workers/valid-worker-123')
        .reply(200, { id: 'valid-worker-123' });

      const result = await client.getWorkerDetails('valid-worker-123');
      expect(result.id).toBe('valid-worker-123');
    });
  });
});
```

---

## Error Handling Matrix

| HTTP Status | Error Code | Retry? | User Message |
|-------------|------------|--------|--------------|
| 400 | BAD_REQUEST | No | Invalid request parameters |
| 401 | UNAUTHORIZED | No | Authentication failed - check API token |
| 403 | FORBIDDEN | No | Permission denied for this operation |
| 404 | NOT_FOUND | No | Resource not found |
| 429 | RATE_LIMITED | Yes (with delay) | Too many requests - please wait |
| 500 | SERVER_ERROR | Yes | Server error - please try again |
| Network | NETWORK_ERROR | Yes | Network connection failed |

---

## Quality Checklist

Every API client method must:

- [ ] Have JSDoc with @see reference to API.md
- [ ] Validate path parameters (prevent injection)
- [ ] Use TypeScript types for params and response
- [ ] Handle all documented error codes
- [ ] Include in rate limiter
- [ ] Have unit tests with mocked responses

---

## Examples

### Example 1: Simple GET endpoint (getUserOverview)

**API.md Section 5.1**:
```
GET /user/overview
Auth: Bearer token
Response: UserOverviewResponse
```

**Implementation**:
```typescript
async getUserOverview(): Promise<UserOverviewResponse> {
  return this.request<UserOverviewResponse>('GET', '/user/overview');
}
```

---

### Example 2: GET with query params (listWorkers)

**API.md Section 6.1**:
```
GET /workers
Auth: Bearer token
Query: page, page_size, status, search, sort_by
Response: WorkerListResponse
```

**Implementation**:
```typescript
async listWorkers(params?: ListWorkersParams): Promise<WorkerListResponse> {
  return this.request<WorkerListResponse>('GET', '/workers', {
    params: {
      page: params?.page ?? 1,
      page_size: params?.pageSize ?? 50,
      status: params?.status,
      search: params?.search,
      sort_by: params?.sortBy,
    },
  });
}
```

---

### Example 3: GET with path param (getWorkerDetails)

**API.md Section 6.2**:
```
GET /workers/{workerId}
Auth: Bearer token
Path: workerId (string)
Response: WorkerDetailsResponse
```

**Implementation**:
```typescript
async getWorkerDetails(workerId: string): Promise<WorkerDetailsResponse> {
  // Validate to prevent path traversal
  if (!workerId.match(/^[a-zA-Z0-9\-_]+$/)) {
    throw new BraiinsApiError('Invalid worker ID', 'VALIDATION_ERROR', 400);
  }

  return this.request<WorkerDetailsResponse>('GET', `/workers/${workerId}`);
}
```

---

## Common Pitfalls

**Pitfall 1: Not validating path parameters**
```typescript
// BAD: Path traversal vulnerability
async getWorker(id: string) {
  return this.request('GET', `/workers/${id}`);
}

// GOOD: Validate input
async getWorker(id: string) {
  if (!id.match(/^[a-zA-Z0-9\-_]+$/)) throw new Error('Invalid ID');
  return this.request('GET', `/workers/${id}`);
}
```

**Pitfall 2: Retrying client errors**
```typescript
// BAD: Retrying 400/401 errors wastes requests
if (error.status >= 400) retry();

// GOOD: Only retry server errors
if (error.status >= 500) retry();
```

**Pitfall 3: Hardcoding base URL**
```typescript
// BAD: Can't change between environments
const url = 'https://pool.braiins.com/api/v1/users';

// GOOD: Use environment variable
const url = `${process.env.BRAIINS_API_BASE_URL}/users`;
```

---

## Version History

- **1.0.0** (2025-12-18): Initial skill definition

---

## References

- [API.md](../../../API.md) - Braiins API specification
- [ARCHITECTURE.md](../../../ARCHITECTURE.md) - API client design
- [Axios Documentation](https://axios-http.com/docs/intro)
