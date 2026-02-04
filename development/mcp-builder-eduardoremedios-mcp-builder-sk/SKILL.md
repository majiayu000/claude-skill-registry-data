---
name: MCP Builder
description: Comprehensive guide for building production-ready MCP (Model Context Protocol) servers. Covers both FastMCP (Python) and MCP SDK (Node/TypeScript) implementations with practical examples, best practices, error handling, testing strategies, security guidelines, and real-world integration patterns.
version: 1.0.0
author: MCP Builder Skill
tags: [mcp, fastmcp, typescript, python, server-development, api-integration, best-practices]
---

# MCP Builder: Production-Ready Server Development Guide

## Table of Contents
1. [MCP Fundamentals](#mcp-fundamentals)
2. [Tool Design Principles](#tool-design-principles)
3. [Implementation Patterns](#implementation-patterns)
4. [Error Handling](#error-handling)
5. [Testing Strategy](#testing-strategy)
6. [Security Best Practices](#security-best-practices)
7. [Documentation Standards](#documentation-standards)
8. [Production Readiness](#production-readiness)
9. [Common Pitfalls](#common-pitfalls)
10. [Real-World Examples](#real-world-examples)

---

## MCP Fundamentals

### Protocol Architecture

MCP (Model Context Protocol) is a standardized protocol for connecting AI assistants to external data sources and tools. It uses JSON-RPC 2.0 over stdio, HTTP, or SSE transports.

**Key Components:**
- **Server**: Exposes tools, resources, and prompts
- **Client**: Claude Desktop or other MCP clients
- **Transport Layer**: Communication mechanism (stdio, HTTP, SSE)
- **Protocol**: JSON-RPC 2.0 messages

### Transport Layers

**Stdio (Standard Input/Output)**
- Best for: Local development, CLI tools
- Pros: Simple, no network setup
- Cons: Single client, no concurrent connections

**HTTP**
- Best for: Web services, remote servers
- Pros: Scalable, standard protocol
- Cons: Requires HTTP server setup

**SSE (Server-Sent Events)**
- Best for: Real-time updates, streaming
- Pros: Push updates, efficient
- Cons: One-way from server to client

### When to Use MCP vs Alternatives

**Use MCP when:**
- Building tools for Claude Desktop
- Need standardized tool interface
- Want protocol-level compatibility
- Require resource discovery

**Consider alternatives when:**
- Building custom integrations
- Need proprietary protocols
- Performance is critical (direct API calls)
- Legacy system integration

### Client-Server Communication Patterns

**Request-Response Pattern**
```python
# FastMCP - Tool execution
@mcp.tool()
async def get_user_info(user_id: str) -> dict:
    """Fetch user information"""
    return {"id": user_id, "name": "John"}
```

```typescript
// MCP SDK - Tool execution
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_user_info",
    description: "Fetch user information",
    inputSchema: {
      type: "object",
      properties: {
        user_id: { type: "string" }
      }
    }
  }]
}));
```

---

## Tool Design Principles

### Atomic Operations

**✅ GOOD: Atomic, Single Responsibility**
```python
# FastMCP
@mcp.tool()
async def create_issue(title: str, body: str, repo: str) -> dict:
    """Create a single GitHub issue"""
    # One clear action
    pass

@mcp.tool()
async def update_issue(issue_id: int, title: str = None, body: str = None) -> dict:
    """Update an existing GitHub issue"""
    # Separate update operation
    pass
```

```typescript
// MCP SDK
const createIssue = {
  name: "create_issue",
  description: "Create a single GitHub issue in a repository",
  inputSchema: {
    type: "object",
    required: ["title", "body", "repo"],
    properties: {
      title: { type: "string", description: "Issue title" },
      body: { type: "string", description: "Issue body" },
      repo: { type: "string", description: "Repository name" }
    }
  }
};
```

**❌ BAD: Multi-purpose, Complex**
```python
# BAD: Too many responsibilities
@mcp.tool()
async def manage_issue(action: str, **kwargs) -> dict:
    """Create, update, delete, or list issues"""
    # Too many operations in one tool
    pass
```

### Clear Input/Output Contracts

**✅ GOOD: Explicit Types and Validation**
```python
# FastMCP with Pydantic
from pydantic import BaseModel, Field, validator

class CreateIssueInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    repo: str = Field(..., pattern=r"^[\w\-\.]+/[\w\-\.]+$")
    labels: list[str] = Field(default_factory=list, max_items=10)

@mcp.tool()
async def create_issue(input: CreateIssueInput) -> dict:
    """Create a GitHub issue with validated inputs"""
    return {
        "id": 123,
        "title": input.title,
        "url": f"https://github.com/{input.repo}/issues/123"
    }
```

```typescript
// MCP SDK with Zod validation
import { z } from "zod";

const CreateIssueSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(1),
  repo: z.string().regex(/^[\w\-\.]+\/[\w\-\.]+$/),
  labels: z.array(z.string()).max(10).default([])
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "create_issue") {
    const input = CreateIssueSchema.parse(request.params.arguments);
    // Process validated input
    return {
      content: [{
        type: "text",
        text: JSON.stringify({ id: 123, title: input.title })
      }]
    };
  }
});
```

### Parameter Validation

**✅ GOOD: Comprehensive Validation**
```python
# FastMCP
from typing import Literal
from pydantic import BaseModel, validator, HttpUrl

class SearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)
    sort: Literal["relevance", "date", "stars"] = "relevance"
    
    @validator("query")
    def validate_query(cls, v):
        if any(char in v for char in ["<", ">", "&"]):
            raise ValueError("Query contains invalid characters")
        return v.strip()
```

```typescript
// MCP SDK
const SearchSchema = z.object({
  query: z.string().min(1).max(500).refine(
    (val) => !/[<>&]/.test(val),
    "Query contains invalid characters"
  ),
  limit: z.number().int().min(1).max(100).default(10),
  sort: z.enum(["relevance", "date", "stars"]).default("relevance")
});
```

### Descriptive Naming Conventions

**✅ GOOD: Clear, Action-Oriented Names**
```python
# FastMCP
@mcp.tool()
async def fetch_repository_details(owner: str, repo_name: str) -> dict:
    """Fetch detailed information about a GitHub repository"""
    pass

@mcp.tool()
async def list_open_pull_requests(owner: str, repo_name: str) -> list[dict]:
    """List all open pull requests in a repository"""
    pass
```

**❌ BAD: Vague Names**
```python
# BAD: Unclear purpose
@mcp.tool()
async def get_data(owner: str, repo: str) -> dict:
    """Get data"""
    pass
```

### When to Split vs Combine Tools

**Decision Tree:**
1. **Different operations?** → Split (create vs update vs delete)
2. **Different data sources?** → Split (GitHub vs GitLab)
3. **Different authentication?** → Split
4. **Same operation, different filters?** → Combine with parameters
5. **Related operations in same transaction?** → Consider combining

**✅ GOOD: Appropriate Splitting**
```python
# FastMCP - Separate tools for different operations
@mcp.tool()
async def create_document(title: str, content: str) -> dict:
    """Create a new Notion page"""
    pass

@mcp.tool()
async def update_document(page_id: str, title: str = None, content: str = None) -> dict:
    """Update an existing Notion page"""
    pass

@mcp.tool()
async def delete_document(page_id: str) -> dict:
    """Delete a Notion page"""
    pass
```

---

## Implementation Patterns

### REST API Integration

**FastMCP Example:**
```python
import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, HttpUrl

mcp = FastMCP("GitHub MCP Server")

class GitHubIssue(BaseModel):
    title: str
    body: str
    labels: list[str] = []

@mcp.tool()
async def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    token: str
) -> dict:
    """Create a GitHub issue"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            json={"title": title, "body": body},
            headers={"Authorization": f"token {token}"},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run()
```

**MCP SDK Example:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import fetch from "node-fetch";

const server = new Server({
  name: "github-mcp-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "create_github_issue") {
    const { owner, repo, title, body, token } = request.params.arguments as any;
    
    const response = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/issues`,
      {
        method: "POST",
        headers: {
          "Authorization": `token ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, body }),
        signal: AbortSignal.timeout(30000)
      }
    );
    
    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data) }]
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

### Database Connections

**FastMCP Example:**
```python
import asyncpg
from fastmcp import FastMCP
from contextlib import asynccontextmanager

mcp = FastMCP("Database MCP Server")
pool: asyncpg.Pool = None

@asynccontextmanager
async def lifespan(app):
    global pool
    pool = await asyncpg.create_pool(
        "postgresql://user:pass@localhost/db",
        min_size=2,
        max_size=10
    )
    yield
    await pool.close()

mcp.lifespan = lifespan

@mcp.tool()
async def query_users(limit: int = 10) -> list[dict]:
    """Query users from database"""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, email FROM users LIMIT $1",
            limit
        )
        return [dict(row) for row in rows]
```

**MCP SDK Example:**
```typescript
import { Pool } from "pg";
import { promisify } from "util";

const pool = new Pool({
  connectionString: "postgresql://user:pass@localhost/db",
  min: 2,
  max: 10
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_users") {
    const { limit = 10 } = request.params.arguments as any;
    const client = await pool.connect();
    try {
      const result = await client.query(
        "SELECT id, name, email FROM users LIMIT $1",
        [limit]
      );
      return {
        content: [{
          type: "text",
          text: JSON.stringify(result.rows)
        }]
      };
    } finally {
      client.release();
    }
  }
});
```

### File System Operations

**FastMCP Example:**
```python
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("File System MCP Server")

@mcp.tool()
async def read_file(file_path: str) -> dict:
    """Read file contents safely"""
    path = Path(file_path).resolve()
    
    # Security: Prevent directory traversal
    if not str(path).startswith(str(Path.cwd())):
        raise ValueError("Access denied: path outside workspace")
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    return {
        "content": path.read_text(),
        "size": path.stat().st_size
    }
```

**MCP SDK Example:**
```typescript
import * as fs from "fs/promises";
import * as path from "path";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "read_file") {
    const { file_path } = request.params.arguments as any;
    const resolved = path.resolve(file_path);
    const cwd = process.cwd();
    
    // Security: Prevent directory traversal
    if (!resolved.startsWith(cwd)) {
      throw new Error("Access denied: path outside workspace");
    }
    
    const stats = await fs.stat(resolved);
    if (!stats.isFile()) {
      throw new Error("Path is not a file");
    }
    
    const content = await fs.readFile(resolved, "utf-8");
    return {
      content: [{
        type: "text",
        text: JSON.stringify({ content, size: stats.size })
      }]
    };
  }
});
```

### Authentication Flows

**FastMCP Example:**
```python
import os
from fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("Authenticated API Server")

class AuthManager:
    def __init__(self):
        self._token: Optional[str] = None
    
    def get_token(self) -> str:
        if not self._token:
            self._token = os.getenv("API_TOKEN")
            if not self._token:
                raise ValueError("API_TOKEN environment variable not set")
        return self._token
    
    def refresh_token(self):
        self._token = None

auth = AuthManager()

@mcp.tool()
async def make_authenticated_request(endpoint: str) -> dict:
    """Make authenticated API request"""
    token = auth.get_token()
    # Use token in request
    pass
```

**MCP SDK Example:**
```typescript
class AuthManager {
  private token: string | null = null;
  
  getToken(): string {
    if (!this.token) {
      this.token = process.env.API_TOKEN || null;
      if (!this.token) {
        throw new Error("API_TOKEN environment variable not set");
      }
    }
    return this.token;
  }
  
  refreshToken(): void {
    this.token = null;
  }
}

const auth = new AuthManager();
```

### Proper Async/Await Handling

**✅ GOOD: Proper Async Patterns**
```python
# FastMCP
import asyncio
import httpx

@mcp.tool()
async def fetch_multiple_resources(urls: list[str]) -> list[dict]:
    """Fetch multiple resources concurrently"""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url, timeout=10.0) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        results = []
        for response in responses:
            if isinstance(response, Exception):
                results.append({"error": str(response)})
            else:
                response.raise_for_status()
                results.append(response.json())
        return results
```

```typescript
// MCP SDK
async function fetchMultipleResources(urls: string[]): Promise<any[]> {
  const promises = urls.map(url => 
    fetch(url, { signal: AbortSignal.timeout(10000) })
      .then(r => r.ok ? r.json() : { error: r.statusText })
      .catch(err => ({ error: err.message }))
  );
  return Promise.all(promises);
}
```

---

## Error Handling

### Explicit Error Types

**FastMCP Example:**
```python
class MCPError(Exception):
    """Base MCP error"""
    pass

class ValidationError(MCPError):
    """Input validation error"""
    pass

class APIError(MCPError):
    """External API error"""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class RateLimitError(APIError):
    """Rate limit exceeded"""
    pass

@mcp.tool()
async def api_call(endpoint: str) -> dict:
    """Make API call with proper error handling"""
    try:
        # API call logic
        pass
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", 429)
        raise APIError(f"API error: {e.response.status_code}", e.response.status_code)
    except httpx.RequestError as e:
        raise APIError(f"Request failed: {str(e)}")
```

**MCP SDK Example:**
```typescript
class MCPError extends Error {
  constructor(message: string, public statusCode?: number) {
    super(message);
    this.name = "MCPError";
  }
}

class ValidationError extends MCPError {}
class APIError extends MCPError {}
class RateLimitError extends APIError {}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool logic
  } catch (error: any) {
    if (error.response?.status === 429) {
      throw new RateLimitError("Rate limit exceeded", 429);
    }
    if (error.response) {
      throw new APIError(`API error: ${error.response.status}`, error.response.status);
    }
    throw new MCPError(`Request failed: ${error.message}`);
  }
});
```

### User-Facing Error Messages

**✅ GOOD: Clear, Actionable Messages**
```python
@mcp.tool()
async def create_issue(title: str, repo: str) -> dict:
    """Create GitHub issue"""
    if not title.strip():
        raise ValueError(
            "Issue title cannot be empty. Please provide a descriptive title."
        )
    
    if "/" not in repo:
        raise ValueError(
            f"Invalid repository format: '{repo}'. Expected format: 'owner/repo-name'"
        )
```

**❌ BAD: Technical, Unhelpful**
```python
# BAD
raise ValueError("Invalid input")
raise Exception("Error occurred")
```

### Retry Logic

**FastMCP Example:**
```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, RateLimitError))
)
async def api_call_with_retry(url: str) -> dict:
    """API call with exponential backoff retry"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        if response.status_code == 429:
            raise RateLimitError("Rate limited")
        response.raise_for_status()
        return response.json()
```

**MCP SDK Example:**
```typescript
async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxAttempts - 1) throw error;
      if (error instanceof RateLimitError) {
        await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
      } else {
        throw error;
      }
    }
  }
  throw new Error("Retry failed");
}
```

### Timeout Handling

**FastMCP Example:**
```python
import asyncio

@mcp.tool()
async def long_running_operation(timeout_seconds: int = 30) -> dict:
    """Operation with timeout"""
    try:
        return await asyncio.wait_for(
            perform_operation(),
            timeout=timeout_seconds
        )
    except asyncio.TimeoutError:
        raise TimeoutError(
            f"Operation timed out after {timeout_seconds} seconds. "
            "Please try again or reduce the scope of the operation."
        )
```

**MCP SDK Example:**
```typescript
async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error(`Timeout after ${timeoutMs}ms`)), timeoutMs)
    )
  ]);
}
```

### Graceful Degradation

**FastMCP Example:**
```python
@mcp.tool()
async def fetch_with_fallback(primary_url: str, fallback_url: str) -> dict:
    """Fetch with fallback on failure"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(primary_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.warning(f"Primary source failed: {e}, trying fallback")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(fallback_url, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except Exception as fallback_error:
            raise APIError(
                f"Both primary and fallback sources failed. "
                f"Primary: {str(e)}, Fallback: {str(fallback_error)}"
            )
```

### Logging Strategies

**FastMCP Example:**
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mcp-server.log"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("mcp_server")

@mcp.tool()
async def tool_with_logging(param: str) -> dict:
    """Tool with structured logging"""
    logger.info(f"Tool called with param: {param[:50]}")  # Truncate for security
    try:
        result = await perform_operation(param)
        logger.info(f"Tool completed successfully")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {str(e)}", exc_info=True)
        raise
```

**MCP SDK Example:**
```typescript
import * as winston from "winston";

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: "mcp-server.log" }),
    new winston.transports.Console()
  ]
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  logger.info("Tool called", { tool: request.params.name });
  try {
    // Tool logic
    logger.info("Tool completed");
  } catch (error) {
    logger.error("Tool failed", { error: error.message, stack: error.stack });
    throw error;
  }
});
```

---

## Testing Strategy

### Unit Tests for Individual Tools

**FastMCP Example:**
```python
import pytest
from unittest.mock import AsyncMock, patch
from mcp_server import create_issue

@pytest.mark.asyncio
async def test_create_issue_success():
    """Test successful issue creation"""
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"id": 123, "title": "Test"}
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        
        result = await create_issue(
            owner="test",
            repo="repo",
            title="Test Issue",
            body="Body",
            token="token"
        )
        
        assert result["id"] == 123
        assert result["title"] == "Test"

@pytest.mark.asyncio
async def test_create_issue_validation_error():
    """Test validation error handling"""
    with pytest.raises(ValueError, match="title cannot be empty"):
        await create_issue("test", "repo", "", "body", "token")
```

**MCP SDK Example:**
```typescript
import { describe, it, expect, vi } from "vitest";
import { createIssue } from "./tools";

describe("createIssue", () => {
  it("should create issue successfully", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: 123, title: "Test" })
    });
    
    const result = await createIssue({
      owner: "test",
      repo: "repo",
      title: "Test Issue",
      body: "Body",
      token: "token"
    });
    
    expect(result.id).toBe(123);
  });
  
  it("should throw validation error for empty title", async () => {
    await expect(
      createIssue({ owner: "test", repo: "repo", title: "", body: "body", token: "token" })
    ).rejects.toThrow("title cannot be empty");
  });
});
```

### Integration Tests with Mock Servers

**FastMCP Example:**
```python
import pytest
from httpx import ASGITransport, AsyncClient
from mcp_server import app

@pytest.mark.asyncio
async def test_integration_create_issue():
    """Integration test with mock server"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/tools/call",
            json={
                "name": "create_issue",
                "arguments": {
                    "owner": "test",
                    "repo": "repo",
                    "title": "Test",
                    "body": "Body"
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
```

**MCP SDK Example:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { TestTransport } from "./test-transport";

describe("Integration Tests", () => {
  it("should handle tool call end-to-end", async () => {
    const transport = new TestTransport();
    await server.connect(transport);
    
    const response = await transport.sendRequest({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "create_issue",
        arguments: {
          owner: "test",
          repo: "repo",
          title: "Test",
          body: "Body"
        }
      }
    });
    
    expect(response.result).toHaveProperty("content");
  });
});
```

### Validation of Tool Schemas

**FastMCP Example:**
```python
import pytest
from pydantic import ValidationError
from mcp_server import CreateIssueInput

def test_tool_schema_validation():
    """Test tool input schema validation"""
    # Valid input
    valid = CreateIssueInput(
        title="Test",
        body="Body",
        repo="owner/repo"
    )
    assert valid.title == "Test"
    
    # Invalid input
    with pytest.raises(ValidationError):
        CreateIssueInput(title="", body="Body", repo="owner/repo")
    
    # Invalid repo format
    with pytest.raises(ValidationError):
        CreateIssueInput(title="Test", body="Body", repo="invalid")
```

**MCP SDK Example:**
```typescript
import { describe, it, expect } from "vitest";
import { CreateIssueSchema } from "./schemas";

describe("Tool Schema Validation", () => {
  it("should validate correct input", () => {
    const result = CreateIssueSchema.parse({
      title: "Test",
      body: "Body",
      repo: "owner/repo"
    });
    expect(result.title).toBe("Test");
  });
  
  it("should reject invalid input", () => {
    expect(() => {
      CreateIssueSchema.parse({ title: "", body: "Body", repo: "owner/repo" });
    }).toThrow();
  });
});
```

### Testing Authentication Flows

**FastMCP Example:**
```python
@pytest.mark.asyncio
async def test_authentication_success():
    """Test successful authentication"""
    with patch.dict(os.environ, {"API_TOKEN": "test-token"}):
        auth = AuthManager()
        token = auth.get_token()
        assert token == "test-token"

@pytest.mark.asyncio
async def test_authentication_missing_token():
    """Test missing token error"""
    with patch.dict(os.environ, {}, clear=True):
        auth = AuthManager()
        with pytest.raises(ValueError, match="API_TOKEN"):
            auth.get_token()
```

### Handling Rate Limits in Tests

**FastMCP Example:**
```python
@pytest.mark.asyncio
async def test_rate_limit_handling():
    """Test rate limit retry logic"""
    call_count = 0
    
    async def mock_api_call():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RateLimitError("Rate limited", 429)
        return {"success": True}
    
    result = await api_call_with_retry("http://test.com")
    assert result["success"] is True
    assert call_count == 3
```

---

## Security Best Practices

### API Key Management

**✅ GOOD: Environment Variables**
```python
# FastMCP
import os
from fastmcp import FastMCP

mcp = FastMCP("Secure Server")

# Never hardcode keys
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")

@mcp.tool()
async def secure_api_call() -> dict:
    """Make secure API call"""
    # Use environment variable
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # ...
```

```typescript
// MCP SDK
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY environment variable must be set");
}

// Use API_KEY in requests
```

**❌ BAD: Hardcoded Secrets**
```python
# NEVER DO THIS
API_KEY = "sk-1234567890abcdef"
```

### Input Sanitization

**FastMCP Example:**
```python
import html
import re
from pydantic import validator

class SafeInput(BaseModel):
    user_input: str
    
    @validator("user_input")
    def sanitize_input(cls, v):
        # Remove potentially dangerous characters
        v = html.escape(v)
        # Remove script tags
        v = re.sub(r"<script[^>]*>.*?</script>", "", v, flags=re.IGNORECASE | re.DOTALL)
        # Limit length
        if len(v) > 10000:
            raise ValueError("Input too long")
        return v.strip()
```

**MCP SDK Example:**
```typescript
import { z } from "zod";
import DOMPurify from "isomorphic-dompurify";

const SafeInputSchema = z.object({
  userInput: z.string()
    .max(10000, "Input too long")
    .transform(val => DOMPurify.sanitize(val.trim()))
});
```

### Preventing Injection Attacks

**✅ GOOD: Parameterized Queries**
```python
# FastMCP - Database
async def safe_query(user_id: str) -> list[dict]:
    """Safe database query with parameterization"""
    async with pool.acquire() as conn:
        # Use parameterized query
        rows = await conn.fetch(
            "SELECT * FROM users WHERE id = $1",
            user_id  # Safe: parameterized
        )
        return [dict(row) for row in rows]
```

**❌ BAD: String Concatenation**
```python
# NEVER DO THIS - SQL Injection risk
query = f"SELECT * FROM users WHERE id = '{user_id}'"
```

### Rate Limiting

**FastMCP Example:**
```python
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[datetime]] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, key: str) -> bool:
        async with self.lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=self.window_seconds)
            
            # Clean old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > window_start
            ]
            
            if len(self.requests[key]) >= self.max_requests:
                return False
            
            self.requests[key].append(now)
            return True

rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

@mcp.tool()
async def rate_limited_operation() -> dict:
    """Operation with rate limiting"""
    if not await rate_limiter.check_rate_limit("default"):
        raise RateLimitError("Rate limit exceeded. Please try again later.")
    # Proceed with operation
```

**MCP SDK Example:**
```typescript
class RateLimiter {
  private requests: Map<string, number[]> = new Map();
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}
  
  check(key: string): boolean {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    const timestamps = this.requests.get(key) || [];
    const recent = timestamps.filter(ts => ts > windowStart);
    
    if (recent.length >= this.maxRequests) {
      return false;
    }
    
    recent.push(now);
    this.requests.set(key, recent);
    return true;
  }
}
```

### Scoping Permissions Appropriately

**✅ GOOD: Principle of Least Privilege**
```python
# FastMCP - Scoped permissions
@mcp.tool()
async def read_user_data(user_id: str, requester_id: str) -> dict:
    """Read user data with permission check"""
    # Check if requester has permission
    if requester_id != user_id:
        # Check if requester is admin
        if not await is_admin(requester_id):
            raise PermissionError("Insufficient permissions")
    
    return await get_user_data(user_id)
```

---

## Documentation Standards

### Tool Descriptions for LLMs

**✅ GOOD: Clear, Action-Oriented Descriptions**
```python
# FastMCP
@mcp.tool()
async def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str
) -> dict:
    """
    Create a new GitHub issue in the specified repository.
    
    Use this tool when you need to create a bug report, feature request,
    or any other type of issue in a GitHub repository. The issue will be
    created with the provided title and body text.
    
    Args:
        owner: GitHub username or organization name (e.g., "microsoft")
        repo: Repository name (e.g., "vscode")
        title: Issue title (required, 1-200 characters)
        body: Issue description/body text (required, supports Markdown)
    
    Returns:
        Dictionary containing:
        - id: Issue number
        - url: URL to the created issue
        - title: Issue title
        - state: Issue state (usually "open")
    
    Raises:
        ValueError: If title or body is empty
        APIError: If GitHub API request fails
        RateLimitError: If GitHub rate limit is exceeded
    
    Example:
        >>> create_github_issue(
        ...     owner="microsoft",
        ...     repo="vscode",
        ...     title="Bug: Editor crashes",
        ...     body="The editor crashes when..."
        ... )
        {"id": 12345, "url": "https://github.com/microsoft/vscode/issues/12345", ...}
    """
    pass
```

**❌ BAD: Vague Descriptions**
```python
# BAD
@mcp.tool()
async def do_stuff(param: str) -> dict:
    """Does stuff"""
    pass
```

### Parameter Documentation

**FastMCP Example:**
```python
from pydantic import Field

@mcp.tool()
async def search_repositories(
    query: str = Field(
        ...,
        description="Search query string. Supports GitHub search syntax.",
        examples=["language:python", "stars:>1000"]
    ),
    sort: str = Field(
        default="best-match",
        description="Sort order: 'best-match', 'stars', 'forks', 'updated'",
        examples=["stars", "updated"]
    ),
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)"
    )
) -> dict:
    """Search GitHub repositories with detailed parameter docs"""
    pass
```

**MCP SDK Example:**
```typescript
const searchRepositories = {
  name: "search_repositories",
  description: "Search GitHub repositories using GitHub's search API",
  inputSchema: {
    type: "object",
    required: ["query"],
    properties: {
      query: {
        type: "string",
        description: "Search query string. Supports GitHub search syntax. Examples: 'language:python', 'stars:>1000'"
      },
      sort: {
        type: "string",
        enum: ["best-match", "stars", "forks", "updated"],
        default: "best-match",
        description: "Sort order for results"
      },
      limit: {
        type: "number",
        minimum: 1,
        maximum: 100,
        default: 10,
        description: "Maximum number of results to return (1-100)"
      }
    }
  }
};
```

### Return Value Schemas

**FastMCP Example:**
```python
from typing import TypedDict

class IssueResult(TypedDict):
    id: int
    url: str
    title: str
    state: str
    created_at: str
    author: str

@mcp.tool()
async def get_issue(owner: str, repo: str, issue_number: int) -> IssueResult:
    """
    Get GitHub issue details.
    
    Returns:
        IssueResult with fields:
        - id: Issue number
        - url: Full URL to issue
        - title: Issue title
        - state: "open" or "closed"
        - created_at: ISO 8601 timestamp
        - author: GitHub username of issue creator
    """
    pass
```

### Usage Examples

**FastMCP Example:**
```python
@mcp.tool()
async def create_notion_page(
    database_id: str,
    title: str,
    content: str
) -> dict:
    """
    Create a new page in a Notion database.
    
    Examples:
        Basic usage:
        >>> create_notion_page(
        ...     database_id="abc123",
        ...     title="Meeting Notes",
        ...     content="# Meeting Notes\\n\\nDiscussion points..."
        ... )
        
        With rich content:
        >>> create_notion_page(
        ...     database_id="abc123",
        ...     title="Project Plan",
        ...     content="## Phase 1\\n- [ ] Task 1\\n- [ ] Task 2"
        ... )
    """
    pass
```

### Common Pitfalls Documentation

**FastMCP Example:**
```python
@mcp.tool()
async def update_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: str = None,
    body: str = None
) -> dict:
    """
    Update an existing GitHub issue.
    
    Common Pitfalls:
    1. Both title and body are optional, but at least one must be provided
    2. Issue number must exist in the repository
    3. You must have write access to the repository
    4. Rate limits: 5000 requests/hour for authenticated requests
    
    Error Handling:
    - 404: Issue not found or repository doesn't exist
    - 403: Insufficient permissions
    - 429: Rate limit exceeded (wait and retry)
    """
    if not title and not body:
        raise ValueError("At least one of 'title' or 'body' must be provided")
    pass
```

---

## Production Readiness

### Configuration Management

**FastMCP Example:**
```python
import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    api_key: str
    api_base_url: str = "https://api.example.com"
    timeout_seconds: int = 30
    max_retries: int = 3
    log_level: str = "INFO"
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

@mcp.tool()
async def configured_api_call() -> dict:
    """API call using configuration"""
    async with httpx.AsyncClient(
        base_url=settings.api_base_url,
        timeout=settings.timeout_seconds
    ) as client:
        # Use settings.api_key
        pass
```

**MCP SDK Example:**
```typescript
import { config } from "dotenv";
config();

interface Config {
  apiKey: string;
  apiBaseUrl: string;
  timeoutSeconds: number;
  maxRetries: number;
  logLevel: string;
  databaseUrl?: string;
}

const settings: Config = {
  apiKey: process.env.API_KEY!,
  apiBaseUrl: process.env.API_BASE_URL || "https://api.example.com",
  timeoutSeconds: parseInt(process.env.TIMEOUT_SECONDS || "30"),
  maxRetries: parseInt(process.env.MAX_RETRIES || "3"),
  logLevel: process.env.LOG_LEVEL || "INFO",
  databaseUrl: process.env.DATABASE_URL
};
```

### Dependency Management

**FastMCP - requirements.txt:**
```txt
fastmcp>=0.9.0
httpx>=0.25.0
pydantic>=2.0.0
python-dotenv>=1.0.0
tenacity>=8.2.0
```

**MCP SDK - package.json:**
```json
{
  "name": "mcp-server",
  "version": "1.0.0",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "zod": "^3.22.0",
    "dotenv": "^16.3.0",
    "node-fetch": "^3.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

### Deployment Considerations

**Dockerfile Example:**
```dockerfile
# FastMCP
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "mcp_server"]
```

```dockerfile
# MCP SDK
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

CMD ["node", "dist/index.js"]
```

### Monitoring and Logging

**FastMCP Example:**
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self):
        self.logger = logging.getLogger("mcp_server")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(message)s'  # JSON format
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_tool_call(self, tool_name: str, duration_ms: float, success: bool):
        self.logger.info(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "tool_call",
            "tool": tool_name,
            "duration_ms": duration_ms,
            "success": success
        }))
```

**MCP SDK Example:**
```typescript
import * as winston from "winston";

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "mcp-server.log" })
  ]
});

function logToolCall(toolName: string, durationMs: number, success: boolean) {
  logger.info("tool_call", {
    tool: toolName,
    duration_ms: durationMs,
    success
  });
}
```

### Versioning Strategy

**FastMCP Example:**
```python
from fastmcp import FastMCP

mcp = FastMCP(
    "My MCP Server",
    version="1.2.3"
)

# Semantic versioning: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features, backwards compatible
# PATCH: Bug fixes, backwards compatible
```

**MCP SDK Example:**
```typescript
const server = new Server({
  name: "my-mcp-server",
  version: "1.2.3"  // Semantic versioning
}, {
  capabilities: {
    tools: {}
  }
});
```

### Backwards Compatibility

**✅ GOOD: Additive Changes**
```python
# Version 1.0
@mcp.tool()
async def create_issue(title: str, body: str) -> dict:
    """Create issue"""
    pass

# Version 1.1 - Backwards compatible (new optional parameter)
@mcp.tool()
async def create_issue(
    title: str,
    body: str,
    labels: list[str] = None  # New optional parameter
) -> dict:
    """Create issue with optional labels"""
    pass
```

**❌ BAD: Breaking Changes**
```python
# Version 1.0
@mcp.tool()
async def create_issue(title: str, body: str) -> dict:
    pass

# Version 2.0 - BREAKING: Changed parameter name
@mcp.tool()
async def create_issue(heading: str, content: str) -> dict:  # BAD
    pass
```

---

## Common Pitfalls

### Anti-Patterns to Avoid

**1. God Tools (Too Many Responsibilities)**
```python
# ❌ BAD
@mcp.tool()
async def manage_github(action: str, **kwargs) -> dict:
    """Do everything GitHub-related"""
    if action == "create_issue":
        # ...
    elif action == "create_pr":
        # ...
    elif action == "list_repos":
        # ...
    # Too many responsibilities!
```

```python
# ✅ GOOD
@mcp.tool()
async def create_github_issue(...) -> dict:
    """Create a GitHub issue"""
    pass

@mcp.tool()
async def create_github_pr(...) -> dict:
    """Create a GitHub pull request"""
    pass

@mcp.tool()
async def list_github_repos(...) -> dict:
    """List GitHub repositories"""
    pass
```

**2. Ignoring Errors**
```python
# ❌ BAD
@mcp.tool()
async def api_call() -> dict:
    try:
        result = await make_api_call()
        return result
    except:
        return {}  # Silent failure!
```

```python
# ✅ GOOD
@mcp.tool()
async def api_call() -> dict:
    try:
        result = await make_api_call()
        return result
    except httpx.HTTPStatusError as e:
        raise APIError(f"API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

**3. No Input Validation**
```python
# ❌ BAD
@mcp.tool()
async def query_database(sql: str) -> dict:
    # No validation - SQL injection risk!
    return await db.execute(sql)
```

```python
# ✅ GOOD
@mcp.tool()
async def query_database(table: str, filters: dict) -> dict:
    # Validate and use parameterized queries
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table}' not allowed")
    # Use parameterized query
    return await db.execute_parameterized(table, filters)
```

### Performance Bottlenecks

**1. Synchronous Operations in Async Context**
```python
# ❌ BAD
@mcp.tool()
async def read_file(file_path: str) -> dict:
    content = open(file_path).read()  # Blocking!
    return {"content": content}
```

```python
# ✅ GOOD
@mcp.tool()
async def read_file(file_path: str) -> dict:
    content = await asyncio.to_thread(
        lambda: Path(file_path).read_text()
    )
    return {"content": content}
```

**2. Not Using Connection Pooling**
```python
# ❌ BAD
@mcp.tool()
async def db_query() -> dict:
    conn = await asyncpg.connect(DB_URL)  # New connection each time!
    result = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return result
```

```python
# ✅ GOOD
pool = await asyncpg.create_pool(DB_URL, min_size=2, max_size=10)

@mcp.tool()
async def db_query() -> dict:
    async with pool.acquire() as conn:  # Reuse connection
        result = await conn.fetch("SELECT * FROM users")
        return result
```

### Common Bugs

**1. Race Conditions**
```python
# ❌ BAD
counter = 0

@mcp.tool()
async def increment() -> dict:
    global counter
    counter += 1  # Race condition!
    return {"count": counter}
```

```python
# ✅ GOOD
import asyncio

counter = 0
lock = asyncio.Lock()

@mcp.tool()
async def increment() -> dict:
    global counter
    async with lock:
        counter += 1
        return {"count": counter}
```

**2. Resource Leaks**
```python
# ❌ BAD
@mcp.tool()
async def api_call() -> dict:
    client = httpx.AsyncClient()  # Never closed!
    response = await client.get("https://api.example.com")
    return response.json()
```

```python
# ✅ GOOD
@mcp.tool()
async def api_call() -> dict:
    async with httpx.AsyncClient() as client:  # Auto-closed
        response = await client.get("https://api.example.com")
        return response.json()
```

### Overly Complex Tool Designs

**❌ BAD: Over-Engineered**
```python
@mcp.tool()
async def complex_operation(
    config: dict,
    options: dict,
    callbacks: list[callable],
    middleware: list[callable]
) -> dict:
    """Too many layers of abstraction"""
    # Complex nested logic
    pass
```

**✅ GOOD: Simple and Clear**
```python
@mcp.tool()
async def create_issue(title: str, body: str, repo: str) -> dict:
    """Create issue - simple and clear"""
    # Straightforward implementation
    pass
```

### Poor Error Messages

**❌ BAD:**
```python
raise ValueError("Error")
raise Exception("Failed")
```

**✅ GOOD:**
```python
raise ValueError(
    "Issue title cannot be empty. Please provide a descriptive title "
    "that summarizes the issue (1-200 characters)."
)
```

---

## Real-World Examples

### GitHub API Integration

**Complete FastMCP Example:**
```python
import os
import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

mcp = FastMCP("GitHub MCP Server")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable required")

class CreateIssueInput(BaseModel):
    owner: str = Field(..., description="Repository owner (username or org)")
    repo: str = Field(..., description="Repository name")
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    labels: list[str] = Field(default_factory=list, max_items=20)

class IssueResult(BaseModel):
    id: int
    number: int
    title: str
    url: str
    state: str
    created_at: str

@mcp.tool()
async def create_github_issue(input: CreateIssueInput) -> IssueResult:
    """
    Create a new GitHub issue in the specified repository.
    
    Requires GITHUB_TOKEN environment variable with 'repo' scope.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{input.owner}/{input.repo}/issues",
            json={
                "title": input.title,
                "body": input.body,
                "labels": input.labels
            },
            headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=30.0
        )
        
        if response.status_code == 401:
            raise ValueError("Invalid GITHUB_TOKEN. Check your token permissions.")
        elif response.status_code == 403:
            raise ValueError("Insufficient permissions. Token needs 'repo' scope.")
        elif response.status_code == 404:
            raise ValueError(f"Repository {input.owner}/{input.repo} not found.")
        elif response.status_code == 429:
            raise ValueError("GitHub rate limit exceeded. Please wait before retrying.")
        
        response.raise_for_status()
        data = response.json()
        
        return IssueResult(
            id=data["id"],
            number=data["number"],
            title=data["title"],
            url=data["html_url"],
            state=data["state"],
            created_at=data["created_at"]
        )

@mcp.tool()
async def list_github_issues(
    owner: str,
    repo: str,
    state: str = "open",
    limit: int = 10
) -> list[IssueResult]:
    """List GitHub issues in a repository"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            params={"state": state, "per_page": min(limit, 100)},
            headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=30.0
        )
        response.raise_for_status()
        return [IssueResult(**issue) for issue in response.json()]

if __name__ == "__main__":
    mcp.run()
```

**Complete MCP SDK Example:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from "@modelcontextprotocol/sdk/types.js";
import fetch from "node-fetch";
import { z } from "zod";

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
if (!GITHUB_TOKEN) {
  throw new Error("GITHUB_TOKEN environment variable required");
}

const CreateIssueSchema = z.object({
  owner: z.string().describe("Repository owner (username or org)"),
  repo: z.string().describe("Repository name"),
  title: z.string().min(1).max(200),
  body: z.string().min(1),
  labels: z.array(z.string()).max(20).default([])
});

const server = new Server({
  name: "github-mcp-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "create_github_issue",
      description: "Create a new GitHub issue in the specified repository. Requires GITHUB_TOKEN with 'repo' scope.",
      inputSchema: {
        type: "object",
        required: ["owner", "repo", "title", "body"],
        properties: {
          owner: { type: "string", description: "Repository owner" },
          repo: { type: "string", description: "Repository name" },
          title: { type: "string", minLength: 1, maxLength: 200 },
          body: { type: "string", minLength: 1 },
          labels: {
            type: "array",
            items: { type: "string" },
            maxItems: 20,
            default: []
          }
        }
      }
    },
    {
      name: "list_github_issues",
      description: "List GitHub issues in a repository",
      inputSchema: {
        type: "object",
        required: ["owner", "repo"],
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          state: { type: "string", enum: ["open", "closed", "all"], default: "open" },
          limit: { type: "number", minimum: 1, maximum: 100, default: 10 }
        }
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "create_github_issue") {
    const input = CreateIssueSchema.parse(request.params.arguments);
    
    const response = await fetch(
      `https://api.github.com/repos/${input.owner}/${input.repo}/issues`,
      {
        method: "POST",
        headers: {
          "Authorization": `token ${GITHUB_TOKEN}`,
          "Accept": "application/vnd.github.v3+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: input.title,
          body: input.body,
          labels: input.labels
        }),
        signal: AbortSignal.timeout(30000)
      }
    );
    
    if (response.status === 401) {
      throw new Error("Invalid GITHUB_TOKEN. Check your token permissions.");
    } else if (response.status === 403) {
      throw new Error("Insufficient permissions. Token needs 'repo' scope.");
    } else if (response.status === 404) {
      throw new Error(`Repository ${input.owner}/${input.repo} not found.`);
    } else if (response.status === 429) {
      throw new Error("GitHub rate limit exceeded. Please wait before retrying.");
    }
    
    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          id: data.id,
          number: data.number,
          title: data.title,
          url: data.html_url,
          state: data.state,
          created_at: data.created_at
        })
      }]
    };
  }
  
  if (request.params.name === "list_github_issues") {
    const { owner, repo, state = "open", limit = 10 } = request.params.arguments as any;
    
    const response = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/issues?state=${state}&per_page=${Math.min(limit, 100)}`,
      {
        headers: {
          "Authorization": `token ${GITHUB_TOKEN}`,
          "Accept": "application/vnd.github.v3+json"
        },
        signal: AbortSignal.timeout(30000)
      }
    );
    
    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.statusText}`);
    }
    
    const issues = await response.json();
    return {
      content: [{
        type: "text",
        text: JSON.stringify(issues.map((issue: any) => ({
          id: issue.id,
          number: issue.number,
          title: issue.title,
          url: issue.html_url,
          state: issue.state,
          created_at: issue.created_at
        })))
      }]
    };
  }
  
  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("GitHub MCP server running on stdio");
}

main().catch(console.error);
```

### Notion API Integration

**FastMCP Example:**
```python
import os
import httpx
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional

mcp = FastMCP("Notion MCP Server")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN environment variable required")

class CreatePageInput(BaseModel):
    database_id: str
    title: str
    content: Optional[str] = None

@mcp.tool()
async def create_notion_page(input: CreatePageInput) -> dict:
    """Create a new page in a Notion database"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/pages",
            json={
                "parent": {"database_id": input.database_id},
                "properties": {
                    "Title": {
                        "title": [{"text": {"content": input.title}}]
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": input.content or ""}}]
                        }
                    }
                ] if input.content else []
            },
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
        if response.status_code == 401:
            raise ValueError("Invalid NOTION_TOKEN")
        elif response.status_code == 404:
            raise ValueError(f"Database {input.database_id} not found")
        
        response.raise_for_status()
        return response.json()
```

**MCP SDK Example:**
```typescript
const NOTION_TOKEN = process.env.NOTION_TOKEN;
if (!NOTION_TOKEN) {
  throw new Error("NOTION_TOKEN environment variable required");
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "create_notion_page") {
    const { database_id, title, content } = request.params.arguments as any;
    
    const response = await fetch("https://api.notion.com/v1/pages", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${NOTION_TOKEN}`,
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        parent: { database_id },
        properties: {
          Title: {
            title: [{ text: { content: title } }]
          }
        },
        children: content ? [{
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [{ text: { content } }]
          }
        }] : []
      }),
      signal: AbortSignal.timeout(30000)
    });
    
    if (!response.ok) {
      throw new Error(`Notion API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data) }]
    };
  }
});
```

### Database Connection Example

**FastMCP Example:**
```python
import asyncpg
from fastmcp import FastMCP
from contextlib import asynccontextmanager
import os

mcp = FastMCP("Database MCP Server")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable required")

pool: asyncpg.Pool = None

@asynccontextmanager
async def lifespan(app):
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=2,
        max_size=10,
        command_timeout=30
    )
    yield
    await pool.close()

mcp.lifespan = lifespan

@mcp.tool()
async def query_users(limit: int = 10, offset: int = 0) -> list[dict]:
    """Query users from database with pagination"""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2",
            limit,
            offset
        )
        return [dict(row) for row in rows]

@mcp.tool()
async def create_user(name: str, email: str) -> dict:
    """Create a new user in the database"""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email, created_at",
            name,
            email
        )
        return dict(row)
```

**MCP SDK Example:**
```typescript
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  min: 2,
  max: 10,
  connectionTimeoutMillis: 30000
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_users") {
    const { limit = 10, offset = 0 } = request.params.arguments as any;
    const client = await pool.connect();
    try {
      const result = await client.query(
        "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2",
        [limit, offset]
      );
      return {
        content: [{ type: "text", text: JSON.stringify(result.rows) }]
      };
    } finally {
      client.release();
    }
  }
  
  if (request.params.name === "create_user") {
    const { name, email } = request.params.arguments as any;
    const client = await pool.connect();
    try {
      const result = await client.query(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email, created_at",
        [name, email]
      );
      return {
        content: [{ type: "text", text: JSON.stringify(result.rows[0]) }]
      };
    } finally {
      client.release();
    }
  }
});
```

### File Operations Example

**FastMCP Example:**
```python
from pathlib import Path
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import os

mcp = FastMCP("File System MCP Server")

WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", ".")).resolve()

class ReadFileInput(BaseModel):
    file_path: str = Field(..., description="Relative path from workspace root")

def validate_path(file_path: str) -> Path:
    """Validate and resolve file path safely"""
    resolved = (WORKSPACE_ROOT / file_path).resolve()
    
    # Security: Prevent directory traversal
    if not str(resolved).startswith(str(WORKSPACE_ROOT)):
        raise ValueError(f"Access denied: path outside workspace")
    
    if not resolved.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not resolved.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    return resolved

@mcp.tool()
async def read_file(input: ReadFileInput) -> dict:
    """Read file contents safely"""
    path = validate_path(input.file_path)
    return {
        "content": path.read_text(),
        "size": path.stat().st_size,
        "path": str(path.relative_to(WORKSPACE_ROOT))
    }

@mcp.tool()
async def write_file(file_path: str, content: str) -> dict:
    """Write file contents safely"""
    path = validate_path(file_path)
    path.write_text(content)
    return {
        "success": True,
        "path": str(path.relative_to(WORKSPACE_ROOT)),
        "size": len(content)
    }

@mcp.tool()
async def list_directory(dir_path: str = ".") -> list[dict]:
    """List directory contents"""
    resolved = (WORKSPACE_ROOT / dir_path).resolve()
    
    if not str(resolved).startswith(str(WORKSPACE_ROOT)):
        raise ValueError("Access denied: path outside workspace")
    
    if not resolved.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    
    if not resolved.is_dir():
        raise ValueError(f"Path is not a directory: {dir_path}")
    
    return [
        {
            "name": item.name,
            "path": str(item.relative_to(WORKSPACE_ROOT)),
            "type": "directory" if item.is_dir() else "file",
            "size": item.stat().st_size if item.is_file() else None
        }
        for item in resolved.iterdir()
    ]
```

**MCP SDK Example:**
```typescript
import * as fs from "fs/promises";
import * as path from "path";

const WORKSPACE_ROOT = path.resolve(process.env.WORKSPACE_ROOT || ".");

function validatePath(filePath: string): string {
  const resolved = path.resolve(WORKSPACE_ROOT, filePath);
  
  if (!resolved.startsWith(WORKSPACE_ROOT)) {
    throw new Error("Access denied: path outside workspace");
  }
  
  return resolved;
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "read_file") {
    const { file_path } = request.params.arguments as any;
    const resolved = validatePath(file_path);
    
    const stats = await fs.stat(resolved);
    if (!stats.isFile()) {
      throw new Error("Path is not a file");
    }
    
    const content = await fs.readFile(resolved, "utf-8");
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          content,
          size: stats.size,
          path: path.relative(WORKSPACE_ROOT, resolved)
        })
      }]
    };
  }
  
  if (request.params.name === "write_file") {
    const { file_path, content } = request.params.arguments as any;
    const resolved = validatePath(file_path);
    
    await fs.writeFile(resolved, content, "utf-8");
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          path: path.relative(WORKSPACE_ROOT, resolved),
          size: content.length
        })
      }]
    };
  }
  
  if (request.params.name === "list_directory") {
    const { dir_path = "." } = request.params.arguments as any;
    const resolved = validatePath(dir_path);
    
    const stats = await fs.stat(resolved);
    if (!stats.isDir()) {
      throw new Error("Path is not a directory");
    }
    
    const items = await fs.readdir(resolved);
    const results = await Promise.all(
      items.map(async (item) => {
        const itemPath = path.join(resolved, item);
        const itemStats = await fs.stat(itemPath);
        return {
          name: item,
          path: path.relative(WORKSPACE_ROOT, itemPath),
          type: itemStats.isDirectory() ? "directory" : "file",
          size: itemStats.isFile() ? itemStats.size : null
        };
      })
    );
    
    return {
      content: [{ type: "text", text: JSON.stringify(results) }]
    };
  }
});
```

---

## Implementation Quality Checklist

Use this checklist to validate your MCP server implementation:

### Tool Design
- [ ] Each tool has a single, clear responsibility
- [ ] Tool names are descriptive and action-oriented
- [ ] Input parameters are validated with proper types
- [ ] Output schemas are well-defined
- [ ] Tools handle edge cases appropriately

### Error Handling
- [ ] All errors are caught and handled appropriately
- [ ] Error messages are user-friendly and actionable
- [ ] Different error types are distinguished
- [ ] Retry logic is implemented where appropriate
- [ ] Timeouts are set for all external calls

### Security
- [ ] API keys are stored in environment variables
- [ ] Input is sanitized and validated
- [ ] SQL injection is prevented (parameterized queries)
- [ ] Path traversal is prevented
- [ ] Rate limiting is implemented
- [ ] Permissions are scoped appropriately

### Testing
- [ ] Unit tests cover all tools
- [ ] Integration tests validate end-to-end flows
- [ ] Error cases are tested
- [ ] Authentication flows are tested
- [ ] Rate limiting is tested

### Documentation
- [ ] Tool descriptions are clear and LLM-friendly
- [ ] Parameters are documented with examples
- [ ] Return value schemas are documented
- [ ] Common pitfalls are documented
- [ ] Usage examples are provided

### Production Readiness
- [ ] Configuration is managed via environment variables
- [ ] Dependencies are properly versioned
- [ ] Logging is implemented
- [ ] Monitoring is set up
- [ ] Versioning strategy is defined
- [ ] Backwards compatibility is maintained

---

## Decision Trees

### When to Create a New Tool vs Add Parameters

```
Is it a different operation?
├─ YES → Create new tool
└─ NO → Is it the same operation with different filters/options?
    ├─ YES → Add parameters to existing tool
    └─ NO → Consider if operations are related
        ├─ Related and often used together → Consider combining
        └─ Unrelated → Create separate tools
```

### Error Handling Strategy

```
Error occurs
├─ Is it a validation error?
│   ├─ YES → Return ValueError with clear message
│   └─ NO → Is it a transient error (network, timeout)?
│       ├─ YES → Implement retry with exponential backoff
│       └─ NO → Is it a permanent error (404, 403)?
│           ├─ YES → Return specific error type with actionable message
│           └─ NO → Log and return generic error
```

### Transport Layer Selection

```
What is your use case?
├─ Local development/CLI → Use stdio
├─ Web service/remote → Use HTTP
├─ Real-time updates needed → Use SSE
└─ Need bidirectional streaming → Consider HTTP with WebSockets
```

---

## Conclusion

This guide provides comprehensive, actionable guidance for building production-ready MCP servers. Follow these patterns and principles to create maintainable, secure, and reliable MCP servers that integrate seamlessly with Claude Desktop and other MCP clients.

Remember:
- **Start simple**: Begin with atomic, single-purpose tools
- **Validate everything**: Input validation prevents security issues
- **Handle errors gracefully**: User-friendly error messages improve UX
- **Test thoroughly**: Comprehensive tests catch issues early
- **Document clearly**: Good documentation helps LLMs use your tools effectively
- **Plan for production**: Consider monitoring, logging, and deployment from the start

For additional resources:
- FastMCP Documentation: https://github.com/jlowin/fastmcp
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Specification: https://spec.modelcontextprotocol.io

