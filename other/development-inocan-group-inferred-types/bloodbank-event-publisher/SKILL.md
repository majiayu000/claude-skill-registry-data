---
name: bloodbank-event-publisher
description: Complete guide for creating, publishing, and consuming events in the DeLoNET home network's 33GOD agentic developer pipeline. Built on RabbitMQ with strict type safety via Pydantic, async Python (aio-pika), FastAPI, and Redis-backed correlation tracking. Features modular event architecture with domain-based organization and auto-discovery registry. This skill is REQUIRED for any work involving the home network event bus.
version: 2.1.0
---

# Bloodbank Event Publishing Guide

## When to Use This Skill

**ALWAYS use this skill when:**


- Working with any component in the DeLoNET home network
- Building or modifying agentic workflows in 33GOD
- Integrating external services (webhooks, APIs) with the home network
- Creating tools that need to communicate across services
- Debugging event flows or troubleshooting message routing

**This skill is NOT needed for:**


- Standalone scripts with no home network integration
- Work outside the DeLoNET ecosystem

## What is Bloodbank?

**Bloodbank** is the event bus infrastructure that powers 33GOD (the agentic developer pipeline). It provides:

- **Type-safe event publishing/consuming** via Pydantic models
- **RabbitMQ topic-based routing** for flexible message distribution
- **Multiple access patterns**: HTTP API, CLI, Python SDK, MCP server
- **Rich context capture**: Agent state, git context, file references
- **Causation tracking**: Correlation IDs link related events
- **Durable messaging**: Events survive broker restarts

### Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Event Producers                          │
├─────────────┬──────────────┬────────────┬──────────────────┤
│   CLI       │  HTTP API    │  MCP       │  File Watcher    │
│  (Typer)    │  (FastAPI)   │  Server    │  (watchdog)      │
└──────┬──────┴──────┬───────┴─────┬──────┴────────┬─────────┘
       │             │             │               │
       └─────────────┴─────────────┴───────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   RabbitMQ Broker     │
              │  (Topic Exchange)     │
              │  amq.topic            │
              └───────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │  n8n    │    │   RAG    │    │  Agents  │
    │Workflows│    │ Ingester │    │(Consumers)│
    └─────────┘    └──────────┘    └──────────┘
```

## Core Concepts

### 1. Event Structure

All events follow this structure:

```python
EventEnvelope[T](
    event_id: UUID,              # Unique identifier for THIS event
    event_type: str,             # Routing key (e.g., "fireflies.transcript.ready")
    timestamp: datetime,         # When event was created
    version: str,                # Envelope schema version
    source: Source,              # WHO/WHAT triggered this event
    correlation_id: UUID | None, # Links to previous related event
    agent_context: AgentContext | None,  # Rich agent metadata (if applicable)
    payload: T                   # Your typed event data
)
```

### 2. Source Metadata

**Source** identifies WHO or WHAT triggered the event:

```python
class TriggerType(str, Enum):
    MANUAL = "manual"           # Human-initiated
    AGENT = "agent"             # AI agent triggered
    SCHEDULED = "scheduled"     # Cron/timer triggered
    FILE_WATCH = "file_watch"   # File system event
    HOOK = "hook"               # External webhook

class Source(BaseModel):
    host: str                   # Machine that generated event (e.g., "big-chungus")
    type: TriggerType           # How was this triggered?
    app: Optional[str]          # Application name (e.g., "n8n", "claude-code")
    meta: Optional[Dict[str, Any]]  # Additional context
```

**Examples:**

```python
# Manual CLI invocation
Source(host="workstation", type=TriggerType.MANUAL, app="bb-cli")

# Claude Code agent
Source(host="workstation", type=TriggerType.AGENT, app="claude-code")

# n8n workflow responding to file change
Source(host="big-chungus", type=TriggerType.FILE_WATCH, app="n8n")

# Fireflies webhook
Source(host="fireflies.ai", type=TriggerType.HOOK, app="fireflies")
```

### 3. Agent Context (Optional)

**When to include:** Only when `source.type == TriggerType.AGENT`

**AgentContext** provides rich metadata about the AI agent:

```python
class AgentType(str, Enum):
    CLAUDE_CODE = "claude-code"
    CLAUDE_CHAT = "claude-chat"
    GEMINI_CLI = "gemini-cli"
    LETTA = "letta"
    AGNO = "agno"
    SMOLAGENT = "smolagent"
    ATOMIC_AGENT = "atomic-agent"
    # ... others

class CodeState(BaseModel):
    """Git context for agent's working environment"""
    repo_url: Optional[str]
    branch: Optional[str]
    working_diff: Optional[str]      # Unstaged changes
    branch_diff: Optional[str]       # Diff vs main
    last_commit_hash: Optional[str]

class AgentContext(BaseModel):
    type: AgentType
    name: Optional[str]              # Agent's persona/name (e.g., "Tonny")
    system_prompt: Optional[str]     # Initial system prompt
    instance_id: Optional[str]       # Unique session identifier
    mcp_servers: Optional[List[str]] # Connected MCP servers
    file_references: Optional[List[str]]  # Files in context
    url_references: Optional[List[str]]   # URLs in context
    code_state: Optional[CodeState]  # Git state snapshot
    checkpoint_id: Optional[str]     # For checkpoint-based agents
    meta: Optional[Dict[str, Any]]   # Extensibility
```

**Example:**

```python
AgentContext(
    type=AgentType.CLAUDE_CODE,
    name="Tonny",
    system_prompt="You are Tonny, a helpful code assistant...",
    instance_id="session_abc123",
    mcp_servers=["filesystem", "git", "web-search"],
    file_references=[
        "/home/jarad/code/bloodbank/event_producers/events.py",
        "/home/jarad/code/bloodbank/rabbit.py"
    ],
    code_state=CodeState(
        repo_url="https://github.com/delorenj/bloodbank",
        branch="feature/fireflies-integration",
        working_diff="+ Added FirefliesTranscriptReadyPayload\n- ...",
        last_commit_hash="a7b3c9d"
    )
)
```

### 4. Correlation Tracking with Redis

**NEW in v2.0:** Bloodbank now automatically tracks event causation chains using Redis!

**Features:**


- **Deterministic Event IDs:** Generate the same UUID for identical events (idempotency)
- **Automatic Correlation Tracking:** Redis stores parent→child relationships
- **Multiple Parents:** Events can be caused by multiple parent events
- **Queryable Chains:** Trace full ancestry or descendancy of any event
- **30-day TTL:** Correlation data expires automatically

**How it works:**

```python
from rabbit import Publisher

publisher = Publisher(enable_correlation_tracking=True)
await publisher.start()

# 1. Generate deterministic event ID
upload_event_id = publisher.generate_event_id(
    "fireflies.transcript.upload",
    meeting_id="abc123",
    user_id="jarad"
)
# ☝️ Same inputs ALWAYS generate the same UUID (idempotency!)

# 2. Publish upload event
await publisher.publish(
    routing_key="fireflies.transcript.upload",
    body=envelope.model_dump(mode="json"),
    event_id=upload_event_id
)

# 3. Later, when Fireflies webhook fires...
ready_event_id = uuid4()
await publisher.publish(
    routing_key="fireflies.transcript.ready",
    body=envelope.model_dump(mode="json"),
    event_id=ready_event_id,
    parent_event_ids=[upload_event_id]  # ← Links back automatically!
)

# 4. Query the correlation chain
chain = publisher.get_correlation_chain(ready_event_id, "ancestors")
# Returns: [upload_event_id, ready_event_id]
```

**Why Deterministic IDs?**

Consumers can dedupe based on `event_id`. If an event is published twice (e.g., webhook retry), consumers see the same UUID and can skip reprocessing.

**Redis Schema:**

```
# Forward mapping: child → parents
bloodbank:correlation:forward:{child_uuid}
  → {"parent_event_ids": ["uuid1", "uuid2"], "created_at": "...", "metadata": {...}}

# Reverse mapping: parent → children (for querying)
bloodbank:correlation:reverse:{parent_uuid}
  → Set{"child1_uuid", "child2_uuid", ...}
```

**Configuration:**

```bash
# .env or environment variables
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=optional
CORRELATION_TTL_DAYS=30
```

### 5. Multiple Correlation IDs

**NEW in v2.0:** `correlation_ids` is now a **List[UUID]** (not Optional[UUID])!

Events can be caused by multiple parent events:

```python
# Example: Transcript combines audio from two recordings
processed_envelope = EventEnvelope(
    event_type="transcript.processed",
    correlation_ids=[
        recording1_event_id,
        recording2_event_id
    ],  # ← Multiple parents!
    payload=...
)
```

**Use cases:**
- Merging multiple recordings into one transcript
- Aggregating data from multiple sources
- Fan-in patterns (multiple events → one result)

### 6. Correlation ID Pattern (Legacy Note)

**In v1.0:** We used `correlation_id` (singular) and manually set it.

**In v2.0:** Use `correlation_ids` (plural, list) + automatic Redis tracking via `parent_event_ids` parameter in `publish()`.

**Example Flow:**

```python
# Event 1: Upload request
upload_event_id = publisher.generate_event_id(
    "fireflies.transcript.upload",
    meeting_id="abc123"
)

upload_envelope = EventEnvelope[FirefliesTranscriptUploadPayload](
    event_id=upload_event_id,  # ← Deterministic!
    event_type="fireflies.transcript.upload",
    correlation_ids=[],  # First in chain
    payload=FirefliesTranscriptUploadPayload(...)
)

await publisher.publish(
    routing_key="fireflies.transcript.upload",
    body=upload_envelope.model_dump(mode="json"),
    event_id=upload_event_id
)

# Event 2: Transcription complete (webhook from Fireflies)
ready_event_id = uuid4()
ready_envelope = EventEnvelope[FirefliesTranscriptReadyPayload](
    event_id=ready_event_id,
    event_type="fireflies.transcript.ready",
    correlation_ids=[upload_event_id],  # ← Links back!
    payload=FirefliesTranscriptReadyPayload(...)
)

await publisher.publish(
    routing_key="fireflies.transcript.ready",
    body=ready_envelope.model_dump(mode="json"),
    event_id=ready_event_id,
    parent_event_ids=[upload_event_id]  # ← Automatic Redis tracking!
)

# Event 3: RAG ingestion complete
processed_event_id = uuid4()
processed_envelope = EventEnvelope[FirefliesTranscriptProcessedPayload](
    event_id=processed_event_id,
    event_type="fireflies.transcript.processed",
    correlation_ids=[ready_event_id],  # ← Links to ready event
    payload=FirefliesTranscriptProcessedPayload(...)
)

await publisher.publish(
    routing_key="fireflies.transcript.processed",
    body=processed_envelope.model_dump(mode="json"),
    event_id=processed_event_id,
    parent_event_ids=[ready_event_id]
)

# Query the full chain!
chain = publisher.get_correlation_chain(processed_event_id, "ancestors")
# Returns: [upload_event_id, ready_event_id, processed_event_id]
```

## Routing Key Conventions

**Format:** `<namespace>.<entity>.<action>`

**Examples:**


- `fireflies.transcript.upload` - Fireflies namespace, transcript entity, upload action
- `fireflies.transcript.ready` - Same namespace/entity, ready action
- `fireflies.transcript.processed` - Same namespace/entity, processed action
- `logjangler.thread.prompt` - Logjangler namespace, thread entity, prompt action
- `logjangler.thread.response` - Same namespace/entity, response action
- `artifact.created` - Global artifact namespace, created action
- `artifact.updated` - Same namespace, updated action

**Wildcard Subscription Patterns:**


- `fireflies.*` - All events in fireflies namespace (any entity.action)
- `*.transcript.*` - All transcript events across namespaces
- `*.*.ready` - All "ready" events across all namespaces/entities
- `#` - Everything (use for debugging only)

## Error Event Patterns

**NEW in v2.0:** Standardized error events for failure tracking!

**Convention:** Use `.failed` or `.error` suffix on the base event type.

**Examples:**
- `fireflies.transcript.failed` - Transcription failed at any stage
- `llm.error` - LLM call failed
- `artifact.ingestion.failed` - RAG ingestion failed

**Error Event Structure:**

All error events should include:


```python
class SomeErrorPayload(BaseModel):
    failed_stage: str              # Where did it fail?
    error_message: str             # Human-readable error
    error_code: Optional[str]      # Machine-readable code
    is_retryable: bool             # Can we retry?
    retry_count: int = 0           # How many times have we tried?
    metadata: Dict[str, Any]       # Additional context
```

**Publishing Error Events:**

```python
# Example: Fireflies transcription failed
error_event = EventEnvelope[FirefliesTranscriptFailedPayload](
    event_type="fireflies.transcript.failed",
    correlation_ids=[original_upload_event_id],  # ← Link to failed attempt!
    source=Source(host="fireflies.ai", type=TriggerType.HOOK, app="fireflies"),
    payload=FirefliesTranscriptFailedPayload(
        failed_stage="transcription",
        error_message="Audio quality too low",
        error_code="AUDIO_QUALITY_LOW",
        is_retryable=False,
        retry_count=0,
        metadata={"meeting_id": "abc123"}
    )
)

await publisher.publish(
    routing_key="fireflies.transcript.failed",
    body=error_event.model_dump(mode="json"),
    event_id=error_event.event_id,
    parent_event_ids=[original_upload_event_id]
)
```

**Consumer Pattern for Errors:**

```python
# Subscribe to all error events
await queue.bind(exchange, routing_key="*.failed")
await queue.bind(exchange, routing_key="*.error")

# Handle retry logic
if error_payload.is_retryable and error_payload.retry_count < 3:
    # Republish original event with incremented retry count
    await retry_logic(error_payload)
else:
    # Send to dead letter queue or alert humans
    await send_alert(error_payload)
```

## File Locations

```
bloodbank/
├── rabbit.py                    # Publisher class with correlation tracking
├── correlation_tracker.py       # Redis-backed correlation tracking
├── config.py                    # Settings via Pydantic (includes Redis config)
├── pyproject.toml               # Dependencies (includes redis)
├── kubernetes/
│   └── deploy.yaml              # K8s deployment
└── event_producers/
    ├── __init__.py
    ├── events/                  # Modular event package
    │   ├── __init__.py          # Package exports
    │   ├── base.py              # Core envelope types (EventEnvelope, Source, etc.)
    │   ├── registry.py          # Event registry with auto-discovery
    │   ├── utils.py             # Helper functions (create_envelope)
    │   └── domains/             # Domain-specific events
    │       ├── __init__.py      # Domain auto-discovery
    │       ├── fireflies.py     # Fireflies domain (4 events)
    │       ├── agent_thread.py  # AgentThread domain (3 events)
    │       └── github.py        # GitHub domain (1 event)
    ├── cli.py                   # Typer CLI for publishing
    ├── http.py                  # FastAPI HTTP endpoints (with debug endpoints)
    ├── mcp_server.py            # MCP server for agents
    ├── watch.py                 # File watcher → events
    ├── n8n/
    │   ├── workflows/           # n8n workflow JSON files
    │   └── docs/                # n8n integration guides
    └── scripts/
        ├── artifact_consumer.py # Example consumer
        └── rag_transcript_consumer.py  # RAG ingestion consumer
```

## Modular Event Architecture

Events are organized into domain-specific modules for maintainability and clarity.

### Structure

```
event_producers/events/
├── base.py              # Core types: EventEnvelope, Source, AgentContext
├── registry.py          # Auto-discovery and validation
├── utils.py             # create_envelope() helper
└── domains/             # Domain modules
    ├── fireflies.py     # Fireflies events
    ├── agent_thread.py  # AgentThread events
    └── github.py        # GitHub events
```

### Import Patterns

```python
from event_producers.events.base import EventEnvelope, Source, TriggerType
from event_producers.events.domains.fireflies import FirefliesTranscriptReadyPayload
from event_producers.events.domains.agent_thread import AgentThreadPrompt
from event_producers.events.utils import create_envelope
```

### Event Registry

The registry provides runtime validation and introspection:

```python
from event_producers.events import get_registry

# Get registry (auto-discovers all domains)
registry = get_registry()

# Validate event type
if registry.is_valid_event_type("fireflies.transcript.ready"):
    payload_type = registry.get_payload_type("fireflies.transcript.ready")

# List domains and events
domains = registry.list_domains()  # ['agent_thread', 'fireflies', 'github']
events = registry.list_domain_events("fireflies")  # 4 events

# Get JSON schema
schema = registry.get_schema("agent.thread.prompt")
```

## How to Define New Events

### Option 1: Add to Existing Domain

Edit the appropriate domain file in `event_producers/events/domains/`:

```python
# In event_producers/events/domains/your_domain.py

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, List

class YourEventPayload(BaseModel):
    """
    Description of what this event represents.

    Published when: [describe trigger condition]
    Consumed by: [list consumers]
    Routing Key: namespace.entity.action
    """
    # Required fields
    some_id: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Optional fields
    metadata: Optional[dict] = None
    tags: List[str] = Field(default_factory=list)

# Add to routing keys mapping at bottom of file
ROUTING_KEYS = {
    "YourEventPayload": "namespace.entity.action",
    # ... other events
}
```

### Option 2: Create New Domain Module

**Step 1:** Create new domain file `event_producers/events/domains/new_domain.py`

```python
"""
NewDomain domain events.

Event Types:
- newdomain.entity.action: Description
"""

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class NewDomainEventPayload(BaseModel):
    """Event payload for new domain."""

    some_id: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Map payload classes to routing keys
ROUTING_KEYS = {
    "NewDomainEventPayload": "newdomain.entity.action",
}
```

**Step 2:** Import in `event_producers/events/domains/__init__.py`

```python
from . import new_domain

__all__ = [
    "fireflies",
    "agent_thread",
    "github",
    "new_domain",  # <-- Add here
    "list_available_domains",
    "list_domain_events",
]
```

**Step 3:** Optionally add to main `event_producers/events/__init__.py` for convenience

```python
from .domains.new_domain import NewDomainEventPayload

__all__ = [
    # ... existing exports
    "NewDomainEventPayload",  # <-- Add here
]
```

**That's it!** The registry auto-discovers and registers your events.

### Creating Event Envelopes

Use the `create_envelope()` helper from `event_producers.events.utils`:

```python
from event_producers.events import create_envelope, Source, TriggerType
from uuid import uuid4

envelope = create_envelope(
    event_type="namespace.entity.action",
    payload=your_payload,
    source=Source(
        host="workstation",
        type=TriggerType.MANUAL,
        app="your-service"
    ),
    correlation_ids=[],  # Or [parent_event_id] to link
    agent_context=None,  # Or AgentContext(...) if agent-triggered
    event_id=uuid4()     # Or use deterministic ID
)
```

## How to Publish Events

### Method 1: Python SDK with Correlation Tracking (Recommended)

```python
from rabbit import Publisher
from event_producers.events import YourEventPayload, EventEnvelope, Source, TriggerType
from uuid import uuid4
import asyncio

async def publish_example():
    # Create publisher with correlation tracking enabled
    publisher = Publisher(enable_correlation_tracking=True)
    await publisher.start()

    try:
        # Option A: Generate deterministic event ID (idempotency)
        event_id = publisher.generate_event_id(
            "namespace.entity.action",
            unique_field="abc123",
            timestamp="2025-10-18"
        )
        # ☝️ Same inputs = same UUID every time!

        # Option B: Generate random UUID
        event_id = uuid4()

        # Create payload
        payload = YourEventPayload(
            some_id="abc123",
            content="Hello, Bloodbank!"
        )

        # Create envelope
        envelope = EventEnvelope[YourEventPayload](
            event_id=event_id,
            event_type="namespace.entity.action",
            timestamp=datetime.now(timezone.utc),
            version="1.0.0",
            source=Source(
                host="workstation",
                type=TriggerType.MANUAL,
                app="my-service"
            ),
            correlation_ids=[],  # Or [parent1_id, parent2_id] if this is a follow-up
            payload=payload
        )

        # Publish with automatic correlation tracking
        await publisher.publish(
            routing_key=envelope.event_type,
            body=envelope.model_dump(mode="json"),
            event_id=envelope.event_id,
            parent_event_ids=[]  # Or [parent1_id, parent2_id] for auto-tracking
        )

        print(f"✓ Published event {envelope.event_id}")

        # Query correlation chain (if needed)
        if parent_event_ids:
            chain = publisher.get_correlation_chain(envelope.event_id, "ancestors")
            print(f"Correlation chain: {chain}")

    finally:
        await publisher.close()

if __name__ == "__main__":
    asyncio.run(publish_example())
```

### Method 2: HTTP API (Webhooks, External Services)

Add endpoint to `event_producers/http.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .events import YourEventPayload, EventEnvelope, Source, TriggerType

@app.post("/events/your-namespace/your-entity")
async def publish_your_event(payload: YourEventPayload, request: Request):
    """Publish your custom event"""
    envelope = EventEnvelope[YourEventPayload](
        event_id=uuid4(),
        event_type="namespace.entity.action",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        source=Source(
            host=request.client.host,
            type=TriggerType.HOOK,
            app="http-api"
        ),
        payload=payload
    )

    await publisher.publish(
        routing_key=envelope.event_type,
        body=envelope.model_dump(mode="json"),
        message_id=str(envelope.event_id)
    )

    return JSONResponse({"event_id": str(envelope.event_id)})
```

**Usage:**

```bash
curl -X POST http://localhost:8682/events/your-namespace/your-entity \
  -H "Content-Type: application/json" \
  -d '{
    "some_id": "abc123",
    "content": "Hello from curl!"
  }'
```

### Method 3: CLI (Manual/Scripting)

Using the `bb` CLI (from `event_producers/cli.py`):

```bash
# Publish LLM prompt
bb publish-prompt --provider claude --model sonnet-4 "Write me a haiku"

# Wrap an LLM tool to auto-publish events
bb wrap claude-code -- "Fix the bug in app.py"
```

**Extend the CLI** for your events:

```python
# In event_producers/cli.py
@app.command()
def publish_custom(some_id: str, content: str):
    """Publish a custom event"""
    payload = YourEventPayload(some_id=some_id, content=content)
    envelope = create_your_event(
        payload=payload,
        source_host=socket.gethostname(),
        source_app="bb-cli"
    )

    # Sync wrapper around async publish
    asyncio.run(_publish(envelope))
    typer.echo(f"✓ Published {envelope.event_id}")
```

### Method 4: MCP Server (For AI Agents)

The MCP server (`event_producers/mcp_server.py`) exposes tools to agents:

```python
# Example MCP tool definition
@mcp.tool()
async def publish_event(
    event_type: str,
    payload: dict,
    correlation_id: Optional[str] = None
) -> str:
    """Publish an event to Bloodbank event bus"""
    # Agent can call this tool with structured data
    # Implementation handles envelope creation and publishing
    ...
```

**Usage from Claude:**


```
I need to publish a transcript.ready event. Let me use the MCP tool...
```

## How to Consume Events

### Pattern 1: Python Consumer (Long-Running Service)

```python
import asyncio
import aio_pika
import json
from typing import Callable
from event_producers.events import EventEnvelope, YourEventPayload

class YourConsumer:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def start(self):
        """Connect to RabbitMQ and start consuming"""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

        # Declare exchange (idempotent)
        exchange = await self.channel.declare_exchange(
            "amq.topic",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Create queue
        queue = await self.channel.declare_queue(
            "your-service-queue",
            durable=True
        )

        # Bind to routing keys you care about
        await queue.bind(exchange, routing_key="namespace.entity.*")

        # Start consuming
        await queue.consume(self._handle_message)
        print("✓ Consumer started, waiting for messages...")

    async def _handle_message(self, message: aio_pika.IncomingMessage):
        """Process incoming message"""
        async with message.process():
            try:
                # Parse envelope
                data = json.loads(message.body.decode())
                envelope = EventEnvelope[YourEventPayload](**data)

                # Handle event
                await self._process_event(envelope)

                # Message auto-acked via context manager

            except Exception as e:
                print(f"✗ Error processing message: {e}")
                # Message will be requeued or sent to DLQ

    async def _process_event(self, envelope: EventEnvelope[YourEventPayload]):
        """Your business logic here"""
        print(f"Processing event {envelope.event_id}")
        print(f"  Type: {envelope.event_type}")
        print(f"  Payload: {envelope.payload}")

        # Do something with the event
        # ...

    async def stop(self):
        """Clean shutdown"""
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

# Run the consumer
async def main():
    consumer = YourConsumer("amqp://user:pass@localhost:5673/")
    await consumer.start()

    # Keep running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 2: n8n Workflow (No Code)

1. **Add RabbitMQ Trigger node**
   - Mode: `receiver`
   - Exchange: `amq.topic`
   - Routing Key: `namespace.entity.*` (your pattern)
   - Queue: `n8n-your-workflow`

2. **Process the message**


   ```javascript
   // n8n Function node
   const envelope = JSON.parse($json.content);
   return {
       event_id: envelope.event_id,
       event_type: envelope.event_type,
       payload: envelope.payload
   };
   ```

3. **Route by event type**
   - IF node: `{{ $json.event_type == "namespace.entity.action" }}`
   - Different branches for different event types

See `event_producers/n8n/README.md` for complete n8n integration guide.

## Debug & Monitoring

### Correlation Debug Endpoints

**NEW in v2.0:** HTTP API includes correlation debugging!

```bash
# Get full correlation debug info for an event
curl http://localhost:8682/debug/correlation/{event_id}

# Response:
{
  "event_id": "abc-123",
  "parents": ["xyz-789"],
  "children": ["def-456", "ghi-789"],
  "ancestors": ["root-000", "xyz-789", "abc-123"],
  "descendants": ["abc-123", "def-456", "ghi-789"],
  "metadata": {"reason": "transcription completed"}
}

# Get correlation chain
curl http://localhost:8682/debug/correlation/{event_id}/chain?direction=ancestors

# Response:
{
  "event_id": "abc-123",
  "direction": "ancestors",
  "chain": ["root-000", "xyz-789", "abc-123"]
}
```

### Query from Python

```python
# Debug correlation from your code
debug_data = publisher.debug_correlation(event_id)
print(f"Parents: {debug_data['parents']}")
print(f"Ancestors: {debug_data['ancestors']}")

# Get just the chain
ancestors = publisher.get_correlation_chain(event_id, "ancestors")
descendants = publisher.get_correlation_chain(event_id, "descendants")
```

### Redis Direct Access

```bash
# View forward mapping (child → parents)
redis-cli GET "bloodbank:correlation:forward:abc-123"

# View reverse mapping (parent → children)
redis-cli SMEMBERS "bloodbank:correlation:reverse:xyz-789"
```

## Complete Example: Fireflies Integration

### Event Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. File Watch detects new recording in ~/Recordings         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Publish: fireflies.transcript.upload                     │
│    - event_id: abc-123                                       │
│    - media_file: /path/to/recording.mp3                     │
│    - correlation_id: None (first in chain)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. n8n workflow uploads to Fireflies API                    │
│    - Consumes: fireflies.transcript.upload                  │
│    - Uploads media file                                      │
│    - Fireflies processes asynchronously                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Fireflies webhook fires (transcription complete)         │
│    - POST to /webhooks/fireflies                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Publish: fireflies.transcript.ready                      │
│    - event_id: def-456                                       │
│    - correlation_id: abc-123 (links back!)                  │
│    - payload: Full transcript with sentences, speakers, etc │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. RAG consumer ingests transcript                          │
│    - Consumes: fireflies.transcript.ready                   │
│    - Chunks sentences into documents                         │
│    - Generates embeddings                                    │
│    - Stores in vector database                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Publish: fireflies.transcript.processed                  │
│    - event_id: ghi-789                                       │
│    - correlation_id: def-456 (links back!)                  │
│    - rag_document_id: Internal ID for queries               │
└─────────────────────────────────────────────────────────────┘

Result: Complete audit trail
abc-123 → def-456 → ghi-789
```

### Implementation

See `/home/claude/fireflies_events_proposal.py` for complete schemas.

**Step 1:** Define events in `events.py` (already done in proposal)

**Step 2:** Add webhook endpoint in `http.py`

```python
@app.post("/webhooks/fireflies")
async def fireflies_webhook(req: Request):
    """Receive Fireflies completion webhook"""
    body = await req.json()

    # Parse webhook into our schema
    payload = FirefliesTranscriptReadyPayload(
        id=body["data"]["id"],
        title=body["data"]["title"],
        date=datetime.fromtimestamp(body["data"]["date"] / 1000),
        duration=body["data"]["duration"],
        transcript_url=body["data"]["transcript_url"],
        sentences=[
            TranscriptSentence(**s) for s in body["data"]["sentences"]
        ],
        # ... map other fields
    )

    # Look up original upload event to get correlation_id
    # (In practice, you'd query a state store)
    original_event_id = await get_upload_event_id(payload.id)

    # Create envelope
    envelope = EventEnvelope[FirefliesTranscriptReadyPayload](
        event_id=uuid4(),
        event_type="fireflies.transcript.ready",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        source=Source(
            host="fireflies.ai",
            type=TriggerType.HOOK,
            app="fireflies"
        ),
        correlation_id=original_event_id,  # Links back!
        payload=payload
    )

    # Publish
    await publisher.publish(
        routing_key=envelope.event_type,
        body=envelope.model_dump(mode="json"),
        message_id=str(envelope.event_id)
    )

    return {"status": "ok", "event_id": str(envelope.event_id)}
```

**Step 3:** Create RAG consumer

```python
# See event_producers/scripts/rag_transcript_consumer.py for complete example

class RAGTranscriptConsumer:
    async def start(self):
        # ... connection setup ...
        await queue.bind(exchange, routing_key="fireflies.transcript.ready")
        await queue.consume(self._handle_transcript)

    async def _handle_transcript(self, message):
        async with message.process():
            envelope = EventEnvelope[FirefliesTranscriptReadyPayload](
                **json.loads(message.body.decode())
            )

            # Ingest into RAG
            doc_id = await self._ingest_to_rag(envelope.payload)

            # Publish processed event
            await self._publish_processed(
                transcript_id=envelope.payload.id,
                rag_doc_id=doc_id,
                correlation_id=envelope.event_id  # Links back!
            )
```

## Best Practices

### 1. Event Naming

✅ **DO:**


- Use lowercase with dots: `fireflies.transcript.ready`
- Follow namespace.entity.action pattern
- Be specific: `llm.thread.response` not `llm.response`

❌ **DON'T:**


- Use camelCase: `fireflies.transcriptReady`
- Mix concerns: `fireflies.transcript.ready.and.processed`
- Be too generic: `event` or `message`

### 2. Payload Design

✅ **DO:**


- Include enough data to avoid additional API calls
- Use ISO 8601 for timestamps
- Provide example values in docstrings
- Version your payload schemas

❌ **DON'T:**


- Include sensitive credentials or tokens
- Make payloads enormous (>1MB) - use URLs/references
- Change existing fields - add new ones instead

### 3. Idempotency & Deduplication

✅ **DO:**


- Use deterministic event IDs when possible:
  ```python
  event_id = publisher.generate_event_id(
      "fireflies.transcript.upload",
      meeting_id="abc123"
  )
  ```
- Consumers should dedupe based on `event_id`
- Store processed event IDs in Redis with TTL
- Handle duplicate events gracefully (idempotent operations)

❌ **DON'T:**


- Assume events arrive only once
- Process the same event multiple times
- Use random UUIDs for events that should be idempotent

**Consumer Deduplication Pattern:**

```python
import redis

class IdempotentConsumer:
    def __init__(self):
        self.redis = redis.Redis()
        self.processed_ttl = 86400  # 24 hours

    async def _handle_message(self, message):
        envelope = json.loads(message.body)
        event_id = envelope["event_id"]

        # Check if already processed
        cache_key = f"processed:{event_id}"
        if self.redis.exists(cache_key):
            print(f"Skipping duplicate event {event_id}")
            await message.ack()
            return

        # Process event
        await self._process(envelope)

        # Mark as processed
        self.redis.setex(cache_key, self.processed_ttl, "1")
        await message.ack()
```

### 4. Correlation IDs

✅ **DO:**


- Always set correlation_ids when event is caused by another event
- Use parent_event_ids parameter for automatic tracking
- Document correlation patterns in payload docstrings
- Query chains for debugging: `publisher.get_correlation_chain()`

❌ **DON'T:**


- Create circular references (A → B → A)
- Lose the correlation chain (always link to immediate parent)
- Forget that correlation_ids is now a list (can have multiple parents)

### 5. Error Handling

✅ **DO:**


- Publish error events (e.g., `namespace.entity.failed`)
- Include error details in payload (failed_stage, error_message, error_code)
- Set correlation_ids to the failed event's ID
- Use `is_retryable` flag for retry logic
- Implement exponential backoff for retries
- Use DLQ (Dead Letter Queue) for persistent failures
- Track retry_count to prevent infinite loops

❌ **DON'T:**


- Silently swallow errors
- Retry indefinitely (set max retry count = 3)
- Log errors without publishing events
- Lose context when publishing error events

**Error Event Publishing Pattern:**

```python
try:
    # Attempt operation
    result = await process_transcript(transcript_id)
except Exception as e:
    # Publish error event
    error_payload = FirefliesTranscriptFailedPayload(
        failed_stage="processing",
        error_message=str(e),
        error_code=getattr(e, 'code', None),
        transcript_id=transcript_id,
        is_retryable=isinstance(e, RetryableError),
        retry_count=current_retry_count,
        metadata={
            "original_event_id": str(original_event_id),
            "stack_trace": traceback.format_exc()
        }
    )

    error_envelope = create_envelope(
        event_type="fireflies.transcript.failed",
        payload=error_payload,
        source=Source(host=socket.gethostname(), type=TriggerType.AGENT, app="rag-consumer"),
        correlation_ids=[original_event_id]  # Link to failed attempt!
    )

    await publisher.publish(
        routing_key="fireflies.transcript.failed",
        body=error_envelope.model_dump(mode="json"),
        event_id=error_envelope.event_id,
        parent_event_ids=[original_event_id]
    )

    # Re-raise or handle based on retry logic
    if error_payload.is_retryable and error_payload.retry_count < 3:
        # Schedule retry
        await schedule_retry(original_event_id, delay=2 ** retry_count)
    else:
        # Send to DLQ
        await send_to_dlq(original_event_id)
```

### 6. Testing

✅ **DO:**


- Test with real RabbitMQ instance (use docker-compose)
- Verify routing keys match event_type
- Check correlation IDs propagate correctly
- Monitor queue depths in production

❌ **DON'T:**


- Test only with mocks (routing is complex!)
- Assume events arrive in order
- Forget to test failure scenarios

## Troubleshooting

### Messages not being consumed

1. **Check queue bindings:**


   ```bash
   kubectl -n messaging exec statefulset/bloodbank-server -- \
     rabbitmqctl list_bindings
   ```

2. **Verify routing key matches pattern:**
   - Published: `fireflies.transcript.ready`
   - Binding: `fireflies.transcript.*` ✅
   - Binding: `fireflies.*` ✅
   - Binding: `llm.*` ❌ (won't match)

3. **Check consumer is running:**
   ```bash
   kubectl -n messaging exec statefulset/bloodbank-server -- \
     rabbitmqctl list_consumers
   ```

### Published events disappear

1. **Queue might not exist:**
   - Consumers create queues on startup
   - If no consumer, no queue = messages dropped
   - Solution: Declare durable queue before publishing

2. **Wrong exchange:**
   - Must publish to `amq.topic`
   - Check Publisher configuration

3. **Message not persistent:**
   - Set `delivery_mode=2` in BasicProperties
   - Check Publisher code uses `persistent=True`

### Correlation IDs not linking

1. **Check event_id → correlation_id mapping:**


   ```python
   # When handling event A
   event_a_id = envelope.event_id  # abc-123

   # When publishing event B
   envelope_b.correlation_id = event_a_id  # Must match!
   ```

2. **Verify UUIDs are valid:**
   - Use `uuid4()` to generate
   - Convert to string for JSON: `str(uuid_obj)`

## Environment Configuration

### Local Development (with port-forward)

```bash
# Port-forward RabbitMQ
kubectl -n messaging port-forward svc/bloodbank 15672:15672 5673:5672

# Set environment variables
export RABBIT_URL="amqp://user:pass@localhost:5673/"
export EXCHANGE_NAME="amq.topic"

# Get credentials
kubectl -n messaging get secret bloodbank-default-user \
  -o jsonpath='{.data.username}' | base64 -d; echo
kubectl -n messaging get secret bloodbank-default-user \
  -o jsonpath='{.data.password}' | base64 -d; echo
```

### In-Cluster Deployment

```yaml
# kubernetes/your-service.yaml
env:
  - name: RABBIT_URL
    valueFrom:
      secretKeyRef:
        name: bloodbank-credentials
        key: amqp-url
  - name: EXCHANGE_NAME
    value: "amq.topic"
```

## Quick Reference

### Common Commands

```bash
# View RabbitMQ UI
kubectl -n messaging port-forward svc/bloodbank 15672:15672
# Visit: http://localhost:15672

# Check queue depth
kubectl -n messaging exec statefulset/bloodbank-server -- \
  rabbitmqctl list_queues name messages

# List connections
kubectl -n messaging exec statefulset/bloodbank-server -- \
  rabbitmqctl list_connections name state

# Purge a queue (DANGER!)
kubectl -n messaging exec statefulset/bloodbank-server -- \
  rabbitmqctl purge_queue "your-queue-name"
```

### Example Routing Keys

```
llm.prompt                  → LLM interaction started
llm.response                → LLM responded
fireflies.transcript.upload → Request transcription
fireflies.transcript.ready  → Transcription complete
artifact.created            → New artifact generated
artifact.updated            → Artifact modified
logjangler.thread.prompt    → LogJangler thread prompt
logjangler.thread.response  → LogJangler thread response
```

### Subscription Patterns

```
fireflies.*                 → All Fireflies events
*.transcript.*              → All transcript events
llm.#                       → All LLM events (any depth)
#                           → Everything (debug only)
```

## Additional Resources

- **n8n Integration:** `event_producers/n8n/README.md`
- **Example Consumer:** `event_producers/scripts/artifact_consumer.py`
- **RabbitMQ Docs:** https://www.rabbitmq.com/
- **aio-pika Docs:** https://aio-pika.readthedocs.io/

---

**Remember:** Always include rich context (source, agent_context if applicable), use correlation IDs to link events, and publish complete data to avoid additional API calls by consumers.

Happy eventing! 🩸
