---
name: mcp-server-dev
description: Braiins OS MCP Server Development - Building MCP tools, resources, and prompts for Bitcoin mining operations management
version: 1.0.0
category: mcp-development
complexity: complex
author: braiins-os-mcp-server project
created: 2025-12-28
status: active
---

# Braiins OS MCP Server Development

## Description

Comprehensive skill for building high-quality MCP (Model Context Protocol) tools, resources, and prompts specifically for Braiins OS miner management. This skill extends the generic mcp-builder patterns with mining-specific workflows, gRPC integration, and fleet operations optimization.

**Target Audience:** Developers building the braiins-os-mcp-server

---

## When to Use This Skill

**Use this skill when:**
- Designing new MCP tools for miner management (status queries, firmware updates, pool configuration)
- Creating MCP resources for fleet monitoring (aggregated metrics, miner status feeds)
- Building MCP prompts for guided mining operations (troubleshooting, batch updates)
- Implementing gRPC client patterns for miner communication
- Designing Redis caching strategies for fleet-scale operations
- Optimizing MCP responses for AI agent consumption

**Don't use this skill for:**
- General MCP server development (use mcp-builder skill instead)
- Braiins OS API reference (use braiins-os skill for documentation)
- Infrastructure deployment (use devops-related skills)
- Non-MCP related TypeScript development

---

## Prerequisites

### Knowledge Requirements
- MCP protocol fundamentals (tools, resources, prompts, transport)
- TypeScript/Node.js development
- gRPC concepts (clients, streams, error handling)
- Redis caching patterns
- Bitcoin mining operations basics

### Project Context
- **Codebase:** braiins-os-mcp-server (TypeScript, Node.js 20.x)
- **MCP SDK:** @modelcontextprotocol/sdk
- **gRPC:** @grpc/grpc-js
- **Cache:** Redis 7.x
- **Testing:** Jest + Supertest

### Related Skills
- **braiins-os** (.claude/skills/braiins-os/) - Braiins OS API documentation reference
- **mcp-builder** (docs/claude/skills-templates/mcp-builder/) - Generic MCP development guide
- **CLAUDE.md** (./CLAUDE.md) - Project-specific development patterns

---

## Workflow

### Phase 1: Tool Design (Mining Operations Focus)

#### Step 1.1: Identify Mining Workflow

**Common Mining Operations:**
1. **Miner Status** - Get current status of one or multiple miners
2. **Firmware Update** - Update firmware with progress tracking
3. **Pool Configuration** - Manage mining pool settings
4. **Fleet Metrics** - Aggregated statistics across all miners
5. **Troubleshooting** - Guided diagnostics for offline miners

**Design Principle:** Consolidate workflows, not just API endpoints.

**Example: Firmware Update Tool Design**
```typescript
/**
 * ❌ BAD: Granular tools forcing agent orchestration
 */
@tool({ name: "check_firmware_version" })
async checkFirmwareVersion(minerId: string) { /* ... */ }

@tool({ name: "download_firmware" })
async downloadFirmware(url: string) { /* ... */ }

@tool({ name: "flash_firmware" })
async flashFirmware(minerId: string) { /* ... */ }

/**
 * ✅ GOOD: Consolidated workflow tool
 */
@tool({
  name: "update_miner_firmware",
  description: "Update firmware on one or more miners with automatic download, flashing, and progress tracking"
})
async updateMinerFirmware(params: {
  minerIds: string[];       // Batch operation support
  version: string;          // Target firmware version
  force?: boolean;          // Skip version checks
  progressCallback?: boolean; // Enable progress updates
}): Promise<{
  jobId: string;            // Background job ID
  status: "pending" | "running" | "completed" | "failed";
  progress: {
    total: number;
    completed: number;
    failed: number;
  };
}> {
  // Handles: version check → download → flash → verify
  // Returns job ID for async status polling
}
```

#### Step 1.2: Design Input Schema (Zod Validation)

**Mining-Specific Patterns:**
```typescript
import { z } from "zod";

// Common validations for mining operations
const MinerIdSchema = z.string().regex(/^[a-zA-Z0-9\-_]+$/);
const MinerIdsSchema = z.array(MinerIdSchema).min(1).max(100); // Batch limit

const FirmwareVersionSchema = z.string().regex(/^\d+\.\d+\.\d+$/);

const PoolUrlSchema = z.string().url().refine(
  (url) => url.startsWith("stratum+tcp://") || url.startsWith("stratum+ssl://"),
  { message: "Pool URL must use stratum protocol" }
);

// Tool input schema
const UpdateMinerFirmwareSchema = z.object({
  minerIds: MinerIdsSchema,
  version: FirmwareVersionSchema,
  force: z.boolean().optional().default(false),
  progressCallback: z.boolean().optional().default(false)
}).strict();
```

#### Step 1.3: Design Output Format (Context-Optimized)

**Principle:** Agents have limited context - provide concise by default, detailed on request.

```typescript
// Concise output (default) - ~150 tokens
{
  jobId: "update-20251228-abc123",
  status: "running",
  progress: {
    total: 10,
    completed: 7,
    failed: 1,
    current: "miner-008"
  },
  estimatedCompletion: "2025-12-28T18:30:00Z"
}

// Detailed output (detailLevel: "verbose") - ~500 tokens
{
  jobId: "update-20251228-abc123",
  status: "running",
  progress: {
    total: 10,
    completed: 7,
    failed: 1,
    current: "miner-008",
    breakdown: [
      { minerId: "miner-001", status: "completed", duration: "5m32s" },
      { minerId: "miner-002", status: "completed", duration: "5m28s" },
      // ... all 10 miners
    ]
  },
  startedAt: "2025-12-28T18:00:00Z",
  estimatedCompletion: "2025-12-28T18:30:00Z",
  errors: [
    {
      minerId: "miner-005",
      error: "Connection timeout",
      suggestion: "Check network connectivity with ping_miner tool"
    }
  ]
}
```

---

### Phase 2: Implementation (TypeScript + MCP SDK)

#### Step 2.1: Tool Registration

```typescript
// src/mcp/tools/updateMinerFirmware.ts
import { tool } from "@modelcontextprotocol/sdk";
import { z } from "zod";

const UpdateMinerFirmwareSchema = z.object({
  minerIds: z.array(z.string()).min(1).max(100),
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  force: z.boolean().optional().default(false),
  detailLevel: z.enum(["concise", "verbose"]).optional().default("concise")
}).strict();

@tool({
  name: "update_miner_firmware",
  description: "Update firmware on one or more Braiins OS miners. Handles download, flashing, and verification. Returns job ID for progress tracking.",
  inputSchema: UpdateMinerFirmwareSchema,
  annotations: {
    readOnlyHint: false,      // Modifies miner state
    destructiveHint: false,   // Can be rolled back
    idempotentHint: true,     // Safe to retry
    openWorldHint: true       // Interacts with external miners
  }
})
export async function updateMinerFirmware(
  params: z.infer<typeof UpdateMinerFirmwareSchema>
): Promise<FirmwareUpdateJobStatus> {
  // Implementation in next step
}
```

#### Step 2.2: gRPC Integration Pattern

```typescript
import { GrpcConnectionPool } from "../../api/grpc/pool";
import { withRetry } from "../../api/grpc/retry";

export async function updateMinerFirmware(
  params: z.infer<typeof UpdateMinerFirmwareSchema>
): Promise<FirmwareUpdateJobStatus> {
  const { minerIds, version, force, detailLevel } = params;

  // 1. Create background job
  const jobId = await this.jobQueue.createJob({
    type: "firmware_update",
    minerIds,
    version
  });

  // 2. Execute updates asynchronously
  this.executeInBackground(async () => {
    const results = await Promise.allSettled(
      minerIds.map(async (minerId) => {
        // Get gRPC connection from pool
        const client = await this.grpc.pool.getConnection(minerId);

        // Update with retry logic
        return await withRetry(
          () => client.updateFirmware({ version, force }),
          { maxRetries: 3, initialDelay: 5000 }
        );
      })
    );

    // 3. Update job status
    await this.jobQueue.updateJob(jobId, {
      status: "completed",
      results: results.map((r, i) => ({
        minerId: minerIds[i],
        success: r.status === "fulfilled",
        error: r.status === "rejected" ? r.reason.message : undefined
      }))
    });
  });

  // 4. Return immediate response
  return {
    jobId,
    status: "pending",
    progress: { total: minerIds.length, completed: 0, failed: 0 }
  };
}
```

#### Step 2.3: Redis Caching Integration

**Pattern: Invalidate cached data when miners update**
```typescript
async function updateMinerFirmware(params: /* ... */): Promise</* ... */> {
  // ... perform update ...

  // Invalidate all caches related to updated miners
  await Promise.all(
    params.minerIds.map(async (minerId) => {
      await this.redis.del(`cache:miner:${minerId}:status`);
      await this.redis.del(`cache:miner:${minerId}:config`);
    })
  );

  // Invalidate fleet-level caches
  await this.redis.del("cache:fleet:summary");

  // Publish update event for real-time subscribers
  await this.redis.publish("events:firmware-update", JSON.stringify({
    minerIds: params.minerIds,
    version: params.version,
    timestamp: new Date().toISOString()
  }));

  return { /* ... */ };
}
```

---

### Phase 3: Resource Development (Fleet Monitoring)

#### Step 3.1: Design Resource URI Scheme

**URI Pattern:** `braiins:///<category>/<resource>[/<identifier>]`

```
braiins:///fleet/summary             # Aggregated fleet metrics
braiins:///fleet/miners              # List of all miners
braiins:///miner/miner-123/status    # Single miner status
braiins:///miner/miner-123/logs      # Miner logs
braiins:///jobs/update-abc123        # Job status
```

#### Step 3.2: Implement Cached Resource

```typescript
import { resource } from "@modelcontextprotocol/sdk";

@resource({
  uri: "braiins:///fleet/summary",
  name: "Fleet Summary",
  description: "Aggregated metrics for all managed miners (cached for 30s)",
  mimeType: "application/json"
})
export async function getFleetSummary(): Promise<FleetSummary> {
  const cacheKey = "cache:fleet:summary";
  const ttl = 30; // 30 seconds - fleet data changes slowly

  // Check cache
  const cached = await this.redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Compute fresh data (expensive operation)
  const [total, online, hashrate, temp, alerts] = await Promise.all([
    this.db.countMiners(),
    this.db.countMinersOnline(),
    this.aggregateHashrate(),       // Sum across all miners
    this.averageTemperature(),      // Average temp
    this.getActiveAlerts()          // Count critical alerts
  ]);

  const summary: FleetSummary = {
    totalMiners: total,
    onlineMiners: online,
    offlineMiners: total - online,
    totalHashrate: `${hashrate} TH/s`,
    averageTemp: `${temp}°C`,
    activeAlerts: alerts.length,
    lastUpdated: new Date().toISOString()
  };

  // Cache for 30 seconds
  await this.redis.setex(cacheKey, ttl, JSON.stringify(summary));

  return summary;
}
```

---

### Phase 4: Prompt Development (Guided Workflows)

#### Step 4.1: Troubleshooting Prompt

```typescript
import { prompt } from "@modelcontextprotocol/sdk";

@prompt({
  name: "troubleshoot_miner_offline",
  description: "Step-by-step guide to diagnose and fix offline miners",
  arguments: [
    { name: "minerId", description: "Miner ID to troubleshoot", required: true }
  ]
})
export async function troubleshootMinerOffline(
  minerId: string
): Promise<PromptMessage[]> {
  // Get miner details
  const miner = await this.db.getMiner(minerId);

  return [
    {
      role: "user",
      content: {
        type: "text",
        text: `My miner ${minerId} is offline. Can you help me fix it?`
      }
    },
    {
      role: "assistant",
      content: {
        type: "text",
        text: `I'll help troubleshoot miner ${minerId}. Let me run through diagnostics:

**Step 1: Check Last Known Status**
Last seen: ${miner.lastSeen || "Never"}
Last status: ${miner.lastStatus || "Unknown"}
Last IP: ${miner.lastIp || "Unknown"}

**Step 2: Test Network Connectivity**
I'll ping the miner to check if it's reachable.
→ Using tool: ping_miner({ minerId: "${minerId}" })

Please wait while I test connectivity...

**Next Steps Based on Results:**
✅ If ping succeeds:
   - Use tool: get_miner_logs({ minerId: "${minerId}", lines: 50 })
   - Check for error patterns in logs
   - May need to restart miner services

❌ If ping fails:
   - Check physical power connection
   - Verify network cable connected
   - Check router/switch port status
   - Verify IP address hasn't changed

Would you like me to proceed with the ping test?`
      }
    }
  ];
}
```

---

### Phase 5: Testing (MCP-Specific)

#### Step 5.1: Unit Test for MCP Tool

```typescript
// tests/unit/mcp/tools/updateMinerFirmware.test.ts
import { MCPServer } from "../../../../src/server";
import { createMockGrpcClient } from "../../../mocks/grpc";
import { createMockRedis } from "../../../mocks/redis";

describe("update_miner_firmware tool", () => {
  let mcpServer: MCPServer;
  let mockGrpc: jest.Mocked<GrpcClient>;
  let mockRedis: jest.Mocked<Redis>;

  beforeEach(() => {
    mockGrpc = createMockGrpcClient();
    mockRedis = createMockRedis();
    mcpServer = new MCPServer({ grpc: mockGrpc, redis: mockRedis });
  });

  it("should accept valid firmware update request", async () => {
    const result = await mcpServer.callTool("update_miner_firmware", {
      minerIds: ["miner-1", "miner-2"],
      version: "2.0.1"
    });

    expect(result.jobId).toBeDefined();
    expect(result.status).toBe("pending");
    expect(result.progress.total).toBe(2);
  });

  it("should reject invalid version format", async () => {
    await expect(
      mcpServer.callTool("update_miner_firmware", {
        minerIds: ["miner-1"],
        version: "invalid-version"
      })
    ).rejects.toThrow("version must match format");
  });

  it("should enforce batch size limit", async () => {
    const tooManyMiners = Array.from({ length: 101 }, (_, i) => `miner-${i}`);

    await expect(
      mcpServer.callTool("update_miner_firmware", {
        minerIds: tooManyMiners,
        version: "2.0.1"
      })
    ).rejects.toThrow("maximum 100 miners");
  });
});
```

#### Step 5.2: Integration Test for Resource

```typescript
// tests/integration/mcp/resources/fleetSummary.test.ts
describe("Fleet Summary Resource", () => {
  let mcpServer: MCPServer;
  let redis: Redis;

  beforeAll(async () => {
    redis = new Redis(process.env.REDIS_URL);
    mcpServer = new MCPServer({ redis });
  });

  it("should return cached fleet summary on second request", async () => {
    const result1 = await mcpServer.readResource("braiins:///fleet/summary");
    const result2 = await mcpServer.readResource("braiins:///fleet/summary");

    expect(result1).toEqual(result2);

    // Verify cache was used (mock/spy on Redis get method)
    expect(redis.get).toHaveBeenCalledWith("cache:fleet:summary");
  });

  it("should refresh cache after TTL expiry", async () => {
    await mcpServer.readResource("braiins:///fleet/summary");

    // Wait for cache to expire (30s TTL)
    await sleep(31000);

    const result = await mcpServer.readResource("braiins:///fleet/summary");

    expect(result.lastUpdated).not.toBe(/* previous timestamp */);
  });
});
```

---

## Mining-Specific Patterns

### Pattern 1: Batch Operations with Progress Tracking

**Use Case:** Update firmware on 50 miners simultaneously

```typescript
@tool({ name: "update_multiple_miners" })
async updateMultipleMiners(params: {
  minerIds: string[];
  operation: "firmware_update" | "pool_change" | "reboot";
  config: any;
}) {
  // Create job for background execution
  const jobId = uuid();

  // Process in parallel with concurrency limit
  const concurrency = 10; // Max 10 simultaneous updates
  const queue = new PQueue({ concurrency });

  const promises = params.minerIds.map((minerId) =>
    queue.add(async () => {
      try {
        await this.performOperation(minerId, params.operation, params.config);
        await this.updateJobProgress(jobId, { completed: minerId });
      } catch (error) {
        await this.updateJobProgress(jobId, { failed: minerId, error });
      }
    })
  );

  // Don't wait - return job ID immediately
  Promise.all(promises).then(() => {
    this.updateJobStatus(jobId, "completed");
  });

  return {
    jobId,
    status: "running",
    total: params.minerIds.length,
    pollUrl: `braiins:///jobs/${jobId}`
  };
}
```

### Pattern 2: Real-Time Status Streaming

**Use Case:** Subscribe to miner status updates via Redis pub/sub

```typescript
@tool({ name: "subscribe_miner_status" })
async subscribeMinerStatus(params: { minerId: string }) {
  // Start gRPC stream
  const stream = await this.grpc.streamMinerStatus(params.minerId);

  // Publish to Redis for agent consumption
  for await (const status of stream) {
    await this.redis.publish(
      `miner:${params.minerId}:status`,
      JSON.stringify(status)
    );
  }

  return {
    subscribed: true,
    channel: `miner:${params.minerId}:status`,
    message: "Status updates will be published to Redis pub/sub channel"
  };
}

// Agent can then read from resource:
@resource({ uri: "braiins:///miner/{minerId}/status/stream" })
async getMinerStatusStream(minerId: string) {
  // Subscribe to Redis channel and return latest status
  const status = await this.redis.get(`miner:${minerId}:status:latest`);
  return JSON.parse(status);
}
```

### Pattern 3: Actionable Error Guidance

**Use Case:** Miner unreachable - guide agent to next steps

```typescript
async function pingMiner(minerId: string) {
  try {
    const client = await this.grpc.pool.getConnection(minerId);
    await client.ping({ timeout: 5000 });

    return { reachable: true, latency: "45ms" };
  } catch (error) {
    // Return actionable error with next steps
    return {
      reachable: false,
      error: {
        code: "MINER_UNREACHABLE",
        message: `Cannot connect to miner ${minerId}`,
        suggestions: [
          "Check if miner is powered on",
          "Verify network connectivity with: list_miners",
          "Check miner IP address in configuration",
          "Try rebooting miner with: reboot_miner"
        ],
        possibleCauses: [
          "Miner offline or powered off",
          "Network firewall blocking gRPC port (50051)",
          "Incorrect IP address in database",
          "Miner experiencing hardware failure"
        ]
      }
    };
  }
}
```

---

## Quality Standards

### MCP Tool Checklist

- [ ] **Input Validation**: Zod schema with proper constraints
- [ ] **Batch Support**: Handles multiple miners when applicable
- [ ] **Concise Output**: Default response < 300 tokens
- [ ] **Detailed Option**: Verbose mode available via `detailLevel` param
- [ ] **Error Guidance**: Errors include suggestions for next steps
- [ ] **Caching**: Reads use cached data when appropriate
- [ ] **Cache Invalidation**: Writes invalidate related caches
- [ ] **Background Jobs**: Long operations return job ID immediately
- [ ] **Progress Tracking**: Job progress available via separate tool/resource
- [ ] **Annotations**: readOnlyHint, destructiveHint, idempotentHint, openWorldHint set correctly
- [ ] **Documentation**: Clear description with examples
- [ ] **Tests**: Unit tests cover happy path + error cases

### MCP Resource Checklist

- [ ] **URI Format**: Follows `braiins:///<category>/<resource>` pattern
- [ ] **Caching**: Appropriate TTL for data type
- [ ] **Freshness**: lastUpdated timestamp included
- [ ] **Mime Type**: Correct content type (application/json, text/plain, etc.)
- [ ] **Performance**: Queries optimized for large fleets
- [ ] **Tests**: Integration tests verify caching behavior

### MCP Prompt Checklist

- [ ] **Guided Workflow**: Clear step-by-step instructions
- [ ] **Tool References**: Suggests specific tools for each step
- [ ] **Resource References**: Links to relevant resources
- [ ] **Conditional Logic**: Different paths based on outcomes
- [ ] **Next Steps**: Always provides clear next actions
- [ ] **Context-Aware**: Uses miner-specific data in guidance

---

## Common Pitfalls

### ❌ Pitfall 1: Not Supporting Batch Operations

**Problem:** Tool only accepts single miner ID
```typescript
// BAD
@tool({ name: "get_miner_status" })
async getMinerStatus(minerId: string) { /* ... */ }

// Agent must call 50 times for 50 miners
```

**Solution:** Accept array of IDs
```typescript
// GOOD
@tool({ name: "get_miner_status" })
async getMinerStatus(minerIds: string[]) {
  return Promise.all(minerIds.map(id => this.fetchStatus(id)));
}

// Agent calls once for all 50 miners
```

---

### ❌ Pitfall 2: Returning Too Much Data

**Problem:** Tool returns 5000+ token response overwhelming context
```typescript
// BAD - Returns full miner details
{
  minerId: "miner-123",
  status: "running",
  hashrate: { /* 20 fields */ },
  temperature: { /* 15 fields */ },
  fans: [ /* 6 fans × 10 fields each */ ],
  pools: [ /* 3 pools × 30 fields each */ ],
  // ... 4500 more tokens
}
```

**Solution:** Concise by default, detailed on request
```typescript
// GOOD - Concise default
{
  minerId: "miner-123",
  status: "running",
  hashrate: "95 TH/s",
  temp: "65°C",
  issues: []  // Only show if problems exist
}

// Detailed available via detailLevel: "verbose"
```

---

### ❌ Pitfall 3: Blocking on Long Operations

**Problem:** Firmware update takes 10 minutes, blocking agent context
```typescript
// BAD
@tool({ name: "update_firmware" })
async updateFirmware(params: {/* ... */}) {
  // Wait for 10 minute update to complete
  await this.performUpdate(params);

  return { status: "completed" };
}
// Agent stuck for 10 minutes
```

**Solution:** Return job ID immediately, poll separately
```typescript
// GOOD
@tool({ name: "update_firmware" })
async updateFirmware(params: {/* ... */}) {
  const jobId = await this.startBackgroundUpdate(params);

  return {
    jobId,
    status: "pending",
    pollWith: "check_job_status"
  };
}

// Separate tool for polling
@tool({ name: "check_job_status" })
async checkJobStatus(jobId: string) {
  return await this.jobQueue.getStatus(jobId);
}
```

---

## Integration Notes

### Related Skills

- **braiins-os** - Braiins OS API documentation and reference
- **mcp-builder** - Generic MCP server development patterns
- **grpc-client-dev** (planned) - gRPC client implementation patterns
- **redis-caching-patterns** (planned) - Advanced Redis caching strategies

### Related Commands

- `/start-session` - Initialize development session with project context
- `/close-session` - End session with documentation updates
- `/test-all` - Run comprehensive test suite
- `/test-mcp-tools` (planned) - Test MCP tools in isolation

### Related Agents

- **Architect** - System design and API design review
- **Builder** - Feature implementation
- **Validator** - Testing and code review
- **Scribe** - Documentation updates

---

## Version History

- **1.0.0** (2025-12-28): Initial skill creation
  - Mining-specific MCP development patterns
  - Tool/Resource/Prompt workflows
  - gRPC integration patterns
  - Redis caching strategies
  - Batch operations and progress tracking
  - Quality checklists and common pitfalls

---

## Metadata

```json
{
  "name": "mcp-server-dev",
  "version": "1.0.0",
  "description": "Braiins OS MCP Server Development Skill",
  "author": "braiins-os-mcp-server project",
  "created": "2025-12-28",
  "status": "active",
  "complexity": "complex",
  "category": "mcp-development",
  "tags": ["mcp", "braiins-os", "mining", "grpc", "redis", "typescript"],
  "extends": "mcp-builder",
  "related_skills": ["braiins-os", "mcp-builder"],
  "target_project": "braiins-os-mcp-server"
}
```
