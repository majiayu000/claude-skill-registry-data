---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
description: 'Build production-grade AI agents with Pydantic AI framework. Covers
  agent

  architecture, dependency injection, tool design, structured outputs, streaming,

  multi-agent patterns, graphs, testing with TestModel/FunctionModel, and cloud-native

  observability with structured logging. Supports Azure Monitor, AWS CloudWatch, GCP

  Cloud Logging, and OpenTelemetry. Use when creating AI agents, implementing tool

  functions, designing multi-agent systems, or configuring production observability.


  IMPORTANT: Before implementing, gather context about the target environment including

  cloud platform (Azure/AWS/GCP/on-prem), logging infrastructure, and observability

  requirements. Do not assume Logfire or any specific observability stack.'
name: pydantic-ai
---

# Pydantic AI Agent Development

Build production-grade AI agents with Pydantic AI. This guide covers agent architecture, dependency injection, tools, structured outputs, streaming, multi-agent patterns, testing, and cloud-native observability.

## Before You Start: Gather Context

**CRITICAL**: Before implementing a Pydantic AI agent, gather the following information from the user if not already known. Do not assume defaults for any of these—ask explicitly.

### Required Context Questions

1. **Cloud Platform**: Which cloud platform is the target deployment?
   - Azure (Azure Monitor, Application Insights)
   - AWS (CloudWatch, X-Ray)
   - GCP (Cloud Logging, Cloud Trace)
   - On-premises / Self-hosted
   - Hybrid / Multi-cloud

2. **Observability Stack**: What logging and monitoring infrastructure is in use?
   - OpenTelemetry (OTLP) → preferred for cloud-agnostic
   - Logfire (Pydantic's native solution)
   - Azure Application Insights
   - AWS CloudWatch / X-Ray
   - GCP Cloud Logging / Cloud Trace
   - Datadog, Splunk, Elastic, Grafana, or other third-party
   - Custom / None yet

3. **Logging Requirements**:
   - Log format preference: JSON structured, text, or platform-specific
   - Log levels needed: DEBUG, INFO, WARNING, ERROR, CRITICAL
   - Sensitive data handling: redaction requirements, PII considerations
   - Correlation ID / trace propagation requirements

4. **LLM Provider**: Which model provider(s) will be used?
   - OpenAI / Azure OpenAI
   - Anthropic Claude
   - Google Gemini / Vertex AI
   - AWS Bedrock
   - Mistral, Groq, Ollama, or other

5. **State Management**: How should agent state be persisted?
   - In-memory only (stateless)
   - Redis / Valkey
   - Database (PostgreSQL, etc.)
   - Cloud-native (Azure Redis Cache, ElastiCache, Memorystore)

6. **Deployment Target**:
   - Container (Docker, Kubernetes, Azure Container Apps, ECS, Cloud Run)
   - Serverless (Azure Functions, Lambda, Cloud Functions)
   - Traditional server

### Example Context Prompt

When context is unclear, ask:

> "Before I implement the Pydantic AI agent, I need to understand your environment:
> 1. What cloud platform are you deploying to (Azure, AWS, GCP, or on-prem)?
> 2. What observability stack do you use (OpenTelemetry, Azure Monitor, CloudWatch, etc.)?
> 3. Do you have specific structured logging requirements?
> 4. Which LLM provider will you use?"

## Core Concepts

### Agent Architecture

An Agent is a generic container with two type parameters: `deps_type` (dependencies) and `output_type` (structured response).

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    db: DatabaseConnection
    api_key: str

class MyOutput(BaseModel):
    result: str = Field(description='The computed result')
    confidence: float = Field(ge=0, le=1)

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
    output_type=MyOutput,
    instructions='You are a helpful assistant.',
)
```

### Model Support

Pydantic AI supports multiple model providers:

| Provider | Model String | Notes |
|----------|--------------|-------|
| OpenAI | `openai:gpt-4o` | GPT-4o, GPT-4, etc. |
| Anthropic | `anthropic:claude-sonnet-4-0` | Claude 3.5/4 models |
| Google | `google-gla:gemini-2.5-flash` | Gemini models |
| Groq | `groq:llama-3.3-70b-versatile` | Fast inference |
| Mistral | `mistral:mistral-large-latest` | Mistral models |

## Dependency Injection

Dependencies flow through `RunContext[DepsType]` to all agent components.

### Defining Dependencies

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class AppDeps:
    customer_id: int
    http_client: httpx.AsyncClient
    api_key: str

agent = Agent('openai:gpt-4o', deps_type=AppDeps)

# Async system prompt with dependency access
@agent.system_prompt
async def dynamic_prompt(ctx: RunContext[AppDeps]) -> str:
    response = await ctx.deps.http_client.get(
        'https://api.example.com/context',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    return f'Context: {response.text}'

# Tool with dependency access
@agent.tool
async def get_customer_data(ctx: RunContext[AppDeps]) -> dict:
    """Fetch customer information."""
    return await fetch_customer(ctx.deps.customer_id)

# Running the agent
async def main():
    async with httpx.AsyncClient() as client:
        deps = AppDeps(customer_id=123, http_client=client, api_key='secret')
        result = await agent.run('Get my account info', deps=deps)
        print(result.output)
```

### Synchronous Dependencies

Non-async functions run in a thread pool automatically:

```python
@agent.system_prompt
def sync_prompt(ctx: RunContext[AppDeps]) -> str:
    # Runs in thread pool, safe for blocking I/O
    response = ctx.deps.http_client.get('https://api.example.com')
    return response.text
```

## Tool Design Patterns

### Tool Decorators

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o', deps_type=str)

# Plain tool - no context needed
@agent.tool_plain
def calculate(a: float, b: float, operation: str) -> float:
    """Perform a math operation."""
    if operation == 'add':
        return a + b
    elif operation == 'multiply':
        return a * b
    raise ValueError(f'Unknown operation: {operation}')

# Context-aware tool - has access to deps
@agent.tool
def get_user_name(ctx: RunContext[str]) -> str:
    """Get the current user's name."""
    return ctx.deps
```

### Tool Registration via Constructor

```python
from pydantic_ai import Agent, Tool
import random

def roll_dice() -> int:
    """Roll a six-sided die."""
    return random.randint(1, 6)

def get_player(ctx: RunContext[str]) -> str:
    """Get current player name."""
    return ctx.deps

agent = Agent(
    'openai:gpt-4o',
    deps_type=str,
    tools=[
        roll_dice,  # Inferred as plain
        Tool(get_player, takes_ctx=True),  # Explicit context
    ],
)
```

### Dynamic Tool Preparation

Conditionally include or modify tools at runtime:

```python
from pydantic_ai import Agent, RunContext, ToolDefinition

agent = Agent('openai:gpt-4o', deps_type=dict)

async def only_for_admins(
    ctx: RunContext[dict], tool_def: ToolDefinition
) -> ToolDefinition | None:
    if ctx.deps.get('is_admin'):
        return tool_def
    return None  # Tool not available

@agent.tool(prepare=only_for_admins)
def delete_user(ctx: RunContext[dict], user_id: int) -> str:
    """Delete a user (admin only)."""
    return f'User {user_id} deleted'
```

### Tool Timeout Configuration

```python
# Agent-level default
agent = Agent('openai:gpt-4o', tool_timeout=30)

# Per-tool override
@agent.tool_plain(timeout=5)
async def fast_operation() -> str:
    """Must complete in 5 seconds."""
    return 'done'
```

## Structured Output

### Pydantic Models

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class Analysis(BaseModel):
    sentiment: str = Field(description='positive, negative, or neutral')
    confidence: float = Field(ge=0, le=1)
    key_points: list[str]

agent = Agent('openai:gpt-4o', output_type=Analysis)
result = agent.run_sync('Analyze: Great product, fast shipping!')
print(result.output)  # Analysis(sentiment='positive', ...)
```

### Union Types for Multiple Outputs

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class Success(BaseModel):
    data: dict

class Failure(BaseModel):
    error: str
    code: int

agent = Agent('openai:gpt-4o', output_type=[Success, Failure])
result = agent.run_sync('Process the request')
# result.output is either Success or Failure
```

### Output Functions (Hand-off Pattern)

```python
from pydantic_ai import Agent, RunContext

async def execute_sql(ctx: RunContext, query: str) -> list[dict]:
    """Execute SQL and return results."""
    return await ctx.deps.db.execute(query)

agent = Agent(
    'openai:gpt-4o',
    output_type=execute_sql,  # Model calls this as final output
    instructions='Convert natural language to SQL queries.',
)
```

### Native vs Tool Output

```python
from pydantic_ai import Agent, NativeOutput, ToolOutput

# NativeOutput: Model uses native structured output (faster)
native_agent = Agent('openai:gpt-4o', output_type=NativeOutput(MyModel))

# ToolOutput: Model calls a tool to return structured data
tool_agent = Agent('openai:gpt-4o', output_type=ToolOutput(MyModel))
```

## Streaming

### Text Streaming

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def stream_response():
    async with agent.run_stream('Tell me a story') as result:
        # Stream complete text (accumulated)
        async for text in result.stream_text():
            print(text)

        # Or stream deltas only
        async for delta in result.stream_text(delta=True):
            print(delta, end='')
```

### Structured Output Streaming

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class Profile(BaseModel):
    name: str
    bio: str | None = None

agent = Agent('openai:gpt-4o', output_type=Profile)

async def stream_profile():
    async with agent.run_stream('Create a profile for Alice') as result:
        async for partial in result.stream_output():
            print(partial)  # Partial Profile objects
```

### Event Streaming

```python
from pydantic_ai import (
    Agent,
    PartStartEvent,
    PartDeltaEvent,
    FunctionToolCallEvent,
    FinalResultEvent,
)

agent = Agent('openai:gpt-4o')

async def stream_events():
    async for event in agent.run_stream_events('Use the search tool'):
        if isinstance(event, PartStartEvent):
            print(f'Started: {event.part}')
        elif isinstance(event, FunctionToolCallEvent):
            print(f'Tool call: {event.part.tool_name}')
        elif isinstance(event, FinalResultEvent):
            print('Final result starting')
```

## Multi-Agent Patterns

### Agent Delegation

```python
from pydantic_ai import Agent, RunContext

# Specialized agent
researcher = Agent(
    'openai:gpt-4o',
    output_type=list[str],
    instructions='Research and return key facts.',
)

# Coordinator agent
coordinator = Agent('openai:gpt-4o')

@coordinator.tool
async def research_topic(ctx: RunContext, topic: str) -> list[str]:
    """Research a topic using specialized agent."""
    result = await researcher.run(
        f'Research: {topic}',
        usage=ctx.usage,  # Share usage tracking
    )
    return result.output

# Usage tracks across all agents
result = coordinator.run_sync('Write about AI safety')
print(result.usage())  # Combined usage from both agents
```

### Shared Dependencies

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class SharedDeps:
    http_client: httpx.AsyncClient
    api_key: str

# Both agents share the same dependency type
analyzer = Agent('openai:gpt-4o', deps_type=SharedDeps)
summarizer = Agent('anthropic:claude-sonnet-4-0', deps_type=SharedDeps)

@analyzer.tool
async def analyze_and_summarize(ctx: RunContext[SharedDeps], data: str) -> str:
    # Delegate to summarizer with same deps
    result = await summarizer.run(
        f'Summarize: {data}',
        deps=ctx.deps,  # Pass dependencies through
    )
    return result.output
```

## Graphs (Complex Workflows)

### Basic Graph Structure

```python
from dataclasses import dataclass
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class MyState:
    counter: int = 0

@dataclass
class Increment(BaseNode[MyState]):
    async def run(self, ctx: GraphRunContext[MyState]) -> 'Check':
        ctx.state.counter += 1
        return Check()

@dataclass
class Check(BaseNode[MyState, None, int]):
    async def run(self, ctx: GraphRunContext[MyState]) -> Increment | End[int]:
        if ctx.state.counter >= 5:
            return End(ctx.state.counter)
        return Increment()

graph = Graph(nodes=(Increment, Check), state_type=MyState)

async def main():
    result = await graph.run(Increment(), state=MyState())
    print(result.output)  # 5
```

### Graph with AI Agents

```python
from dataclasses import dataclass, field
from pydantic_ai import Agent, ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class ConversationState:
    messages: list[ModelMessage] = field(default_factory=list)

draft_agent = Agent('openai:gpt-4o', output_type=str)
review_agent = Agent('anthropic:claude-sonnet-4-0', output_type=bool)

@dataclass
class Draft(BaseNode[ConversationState]):
    topic: str

    async def run(self, ctx: GraphRunContext[ConversationState]) -> 'Review':
        result = await draft_agent.run(
            f'Write about: {self.topic}',
            message_history=ctx.state.messages,
        )
        ctx.state.messages.extend(result.new_messages())
        return Review(draft=result.output)

@dataclass
class Review(BaseNode[ConversationState, None, str]):
    draft: str

    async def run(self, ctx: GraphRunContext[ConversationState]) -> Draft | End[str]:
        result = await review_agent.run(f'Is this good? {self.draft}')
        if result.output:
            return End(self.draft)
        return Draft(topic='Improve the draft')

workflow = Graph(nodes=(Draft, Review), state_type=ConversationState)
```

### GraphBuilder (Beta API)

```python
from dataclasses import dataclass
from pydantic_graph.beta import GraphBuilder, StepContext
from pydantic_graph.beta.join import reduce_list_append

@dataclass
class State:
    items_processed: int = 0

g = GraphBuilder(state_type=State, input_type=list[int], output_type=list[int])

@g.step
async def square(ctx: StepContext[State, None, int]) -> int:
    ctx.state.items_processed += 1
    return ctx.inputs * ctx.inputs

collect = g.join(reduce_list_append, initial_factory=list[int])

g.add(
    g.edge_from(g.start_node).map().to(square),
    g.edge_from(square).to(collect),
    g.edge_from(collect).to(g.end_node),
)

graph = g.build()

async def main():
    state = State()
    result = await graph.run(state=state, inputs=[1, 2, 3, 4, 5])
    print(sorted(result))  # [1, 4, 9, 16, 25]
```

## Human-in-the-Loop

### Tool Approval

```python
from pydantic_ai import Agent, ApprovalRequired, RunContext, DeferredToolRequests

agent = Agent('openai:gpt-4o', output_type=[str, DeferredToolRequests])

@agent.tool(requires_approval=True)
def delete_file(path: str) -> str:
    """Delete a file (requires approval)."""
    return f'Deleted {path}'

@agent.tool
def update_file(ctx: RunContext, path: str, content: str) -> str:
    """Update a file (conditional approval)."""
    if path.startswith('.env') and not ctx.tool_call_approved:
        raise ApprovalRequired(metadata={'reason': 'sensitive file'})
    return f'Updated {path}'

# First run - may return deferred requests
result = agent.run_sync('Delete config.yaml')
if isinstance(result.output, DeferredToolRequests):
    # Present to user for approval
    for call in result.output.approvals:
        print(f'Approve {call.tool_name}({call.args})?')
```

## Testing

### TestModel for Unit Tests

```python
import pytest
from pydantic_ai import Agent, models, capture_run_messages
from pydantic_ai.models.test import TestModel

# Block real API calls in tests
models.ALLOW_MODEL_REQUESTS = False

my_agent = Agent('openai:gpt-4o', instructions='Be helpful')

@pytest.mark.asyncio
async def test_agent_behavior():
    with capture_run_messages() as messages:
        with my_agent.override(model=TestModel()):
            result = await my_agent.run('Hello')
            assert result.output == 'success (no tool calls)'

    # Assert on message exchange
    assert len(messages) == 2  # Request + Response
```

### FunctionModel for Custom Responses

```python
from pydantic_ai import Agent, ModelMessage, ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

agent = Agent('openai:gpt-4o')

@agent.tool_plain
def get_weather(location: str) -> str:
    return f'Sunny in {location}'

def mock_model(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    # First call: trigger tool
    if len(messages) == 1:
        return ModelResponse(parts=[
            ToolCallPart('get_weather', {'location': 'London'})
        ])
    # Second call: return final response
    return ModelResponse(parts=[TextPart('Weather retrieved successfully')])

async def test_with_tool_call():
    with agent.override(model=FunctionModel(mock_model)):
        result = await agent.run('What is the weather?')
        assert 'Weather' in result.output
```

### Override Dependencies

```python
from pydantic_ai import Agent

class MockDB:
    async def query(self, sql: str) -> list:
        return [{'id': 1, 'name': 'Test'}]

async def test_with_mock_deps():
    with agent.override(deps=MockDB()):
        result = await agent.run('Get all users')
        # Agent uses MockDB instead of real database
```

### Pytest Fixtures

```python
import pytest
from pydantic_ai.models.test import TestModel

@pytest.fixture
def test_agent():
    with my_agent.override(model=TestModel()):
        yield my_agent

async def test_feature(test_agent):
    result = await test_agent.run('Do something')
    assert result.output
```

## Observability and Structured Logging

Choose the observability approach based on the target environment. This section covers cloud-agnostic OpenTelemetry, cloud-specific integrations, and Logfire.

### Structured Logging Foundation

Always use structured logging for AI agents. This enables filtering, alerting, and analysis across any observability platform.

```python
import logging
import json
from datetime import datetime, timezone
from typing import Any
from dataclasses import dataclass, field

@dataclass
class AgentLogContext:
    """Structured context for agent logging."""
    session_id: str
    agent_name: str
    correlation_id: str | None = None
    user_id: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

class StructuredLogger:
    """Cloud-agnostic structured logger for Pydantic AI agents."""

    def __init__(self, name: str, context: AgentLogContext):
        self.logger = logging.getLogger(name)
        self.context = context

    def _build_record(self, level: str, message: str, **kwargs) -> dict:
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': level,
            'message': message,
            'session_id': self.context.session_id,
            'agent_name': self.context.agent_name,
            'correlation_id': self.context.correlation_id,
            'user_id': self.context.user_id,
            **self.context.extra,
            **kwargs,
        }

    def info(self, message: str, **kwargs):
        record = self._build_record('INFO', message, **kwargs)
        self.logger.info(json.dumps(record))

    def error(self, message: str, **kwargs):
        record = self._build_record('ERROR', message, **kwargs)
        self.logger.error(json.dumps(record))

    def agent_run_started(self, prompt: str, model: str):
        self.info('Agent run started', event='agent_run_started', model=model, prompt_length=len(prompt))

    def agent_run_completed(self, duration_ms: float, tokens_used: int):
        self.info('Agent run completed', event='agent_run_completed', duration_ms=duration_ms, tokens_used=tokens_used)

    def tool_called(self, tool_name: str, duration_ms: float):
        self.info('Tool called', event='tool_called', tool_name=tool_name, duration_ms=duration_ms)

    def llm_error(self, error: str, retry_count: int = 0):
        self.error('LLM error', event='llm_error', error_message=error, retry_count=retry_count)
```

### OpenTelemetry (Cloud-Agnostic)

OpenTelemetry provides vendor-neutral instrumentation that exports to any backend.

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentation
from pydantic_ai import Agent, RunContext
import time

# Configure OTLP export (works with any OTLP-compatible backend)
def configure_opentelemetry(service_name: str, otlp_endpoint: str):
    # Tracing
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics
    meter_provider = MeterProvider()
    metrics.set_meter_provider(meter_provider)

    # Instrument HTTP clients (captures LLM API calls)
    HTTPXClientInstrumentation().instrument()

    return trace.get_tracer(service_name)

tracer = configure_opentelemetry('my-agent', 'http://localhost:4317')

# Instrumented agent wrapper
class InstrumentedAgent:
    def __init__(self, agent: Agent, tracer: trace.Tracer):
        self.agent = agent
        self.tracer = tracer
        self.meter = metrics.get_meter('pydantic-ai-agent')
        self.run_counter = self.meter.create_counter('agent_runs_total')
        self.run_duration = self.meter.create_histogram('agent_run_duration_ms')
        self.token_counter = self.meter.create_counter('agent_tokens_total')

    async def run(self, prompt: str, deps=None):
        with self.tracer.start_as_current_span('agent_run') as span:
            span.set_attribute('agent.prompt_length', len(prompt))
            span.set_attribute('agent.model', str(self.agent.model))

            start = time.perf_counter()
            try:
                result = await self.agent.run(prompt, deps=deps)
                duration = (time.perf_counter() - start) * 1000

                usage = result.usage()
                span.set_attribute('agent.total_tokens', usage.total_tokens)
                span.set_attribute('agent.duration_ms', duration)

                self.run_counter.add(1, {'status': 'success'})
                self.run_duration.record(duration)
                self.token_counter.add(usage.total_tokens)

                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(trace.StatusCode.ERROR, str(e))
                self.run_counter.add(1, {'status': 'error'})
                raise
```

### Azure Monitor / Application Insights

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from pydantic_ai import Agent
import os

# Configure Azure Monitor with connection string
configure_azure_monitor(
    connection_string=os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING'],
    enable_live_metrics=True,
)

tracer = trace.get_tracer('pydantic-ai-agent')

agent = Agent('openai:gpt-4o')

async def run_with_azure_tracing(prompt: str):
    with tracer.start_as_current_span('agent_run') as span:
        span.set_attribute('ai.prompt', prompt[:100])  # Truncate for safety
        result = await agent.run(prompt)
        span.set_attribute('ai.tokens', result.usage().total_tokens)
        return result
```

**Azure-specific structured logging:**

```python
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Configure Azure Log Analytics export
logger = logging.getLogger('pydantic-ai')
logger.addHandler(AzureLogHandler(
    connection_string=os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING']
))

# Custom dimensions for Azure queries
logger.info('Agent run completed', extra={
    'custom_dimensions': {
        'session_id': session_id,
        'agent_name': 'deviation-assistant',
        'tokens_used': usage.total_tokens,
        'model': 'gpt-4o',
    }
})
```

### AWS CloudWatch / X-Ray

```python
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.util import get_trace_id
import watchtower
import logging
import json

# Patch HTTP libraries for X-Ray tracing
patch_all()

# Configure CloudWatch Logs with structured JSON
logger = logging.getLogger('pydantic-ai')
logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='pydantic-ai-agents',
    log_stream_name='agent-{}'.format(os.environ.get('HOSTNAME', 'local')),
))

class CloudWatchAgentLogger:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger('pydantic-ai')

    def log_run(self, session_id: str, duration_ms: float, tokens: int):
        # Structured log for CloudWatch Insights queries
        self.logger.info(json.dumps({
            'event': 'agent_run_completed',
            'agent_name': self.agent_name,
            'session_id': session_id,
            'duration_ms': duration_ms,
            'tokens_used': tokens,
            'trace_id': get_trace_id(),
        }))

# X-Ray instrumented agent
@xray_recorder.capture('agent_run')
async def run_agent(agent: Agent, prompt: str):
    segment = xray_recorder.current_segment()
    segment.put_metadata('prompt_length', len(prompt))

    result = await agent.run(prompt)

    segment.put_metadata('tokens', result.usage().total_tokens)
    segment.put_annotation('model', str(agent.model))

    return result
```

### GCP Cloud Logging / Cloud Trace

```python
from google.cloud import logging as cloud_logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
import logging

# Configure Cloud Trace
trace_provider = TracerProvider()
trace_provider.add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer('pydantic-ai-agent')

# Configure Cloud Logging with structured logs
client = cloud_logging.Client()
handler = CloudLoggingHandler(client, name='pydantic-ai-agent')

logger = logging.getLogger('pydantic-ai')
logger.addHandler(handler)

class GCPAgentLogger:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger('pydantic-ai')

    def log_run(self, session_id: str, **kwargs):
        # jsonPayload format for Cloud Logging queries
        self.logger.info('Agent run', extra={
            'json_fields': {
                'agent_name': self.agent_name,
                'session_id': session_id,
                **kwargs,
            }
        })
```

### Logfire (Pydantic Native)

For teams using Pydantic's hosted observability platform:

```python
import logfire
from pydantic_ai import Agent, InstrumentationSettings

logfire.configure()
logfire.instrument_pydantic_ai()

# Agent-level instrumentation settings
settings = InstrumentationSettings(
    include_content=True,  # Include prompts/completions
    include_binary_content=False,  # Exclude images
)

agent = Agent('openai:gpt-4o', instrument=settings)

# Trace HTTP requests to LLM APIs
logfire.instrument_httpx(capture_all=True)
```

### Exclude Sensitive Content

For compliance (HIPAA, GDPR, PCI-DSS), redact PII from logs:

```python
import re
from pydantic_ai import Agent, InstrumentationSettings

# Disable content logging entirely
settings = InstrumentationSettings(include_content=False)
agent = Agent('openai:gpt-4o', instrument=settings)

# Or implement custom redaction
def redact_pii(text: str) -> str:
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }
    for name, pattern in patterns.items():
        text = re.sub(pattern, f'[REDACTED_{name.upper()}]', text)
    return text

class RedactedLogger(StructuredLogger):
    def agent_run_started(self, prompt: str, model: str):
        # Log only redacted prompts
        self.info('Agent run started',
                  event='agent_run_started',
                  model=model,
                  prompt_preview=redact_pii(prompt[:100]))
```

### Correlation and Trace Propagation

Propagate trace context across service boundaries:

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

propagator = TraceContextTextMapPropagator()

# Inject trace context into outgoing request headers
def inject_trace_context(headers: dict) -> dict:
    inject(headers)
    return headers

# Extract trace context from incoming request
def extract_trace_context(headers: dict):
    ctx = extract(headers)
    return trace.set_span_in_context(trace.get_current_span(), ctx)

# Example: FastAPI middleware for trace propagation
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ctx = extract(dict(request.headers))
        tracer = trace.get_tracer('pydantic-ai-api')

        with tracer.start_as_current_span('http_request', context=ctx) as span:
            span.set_attribute('http.method', request.method)
            span.set_attribute('http.url', str(request.url))

            response = await call_next(request)

            span.set_attribute('http.status_code', response.status_code)
            return response
```

### Observability Configuration Table

| Platform | Tracing | Logging | Metrics |
|----------|---------|---------|---------|
| **OpenTelemetry** | `OTLPSpanExporter` | N/A (use structured JSON) | `OTLPMetricExporter` |
| **Azure** | `azure-monitor-opentelemetry` | `AzureLogHandler` | Azure Monitor Metrics |
| **AWS** | `aws-xray-sdk` | `watchtower` | CloudWatch Metrics |
| **GCP** | `cloud-trace` | `google-cloud-logging` | Cloud Monitoring |
| **Logfire** | `logfire.instrument_pydantic_ai()` | Built-in | Built-in |

## Pydantic Evals

### Basic Evaluation

```python
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected, LLMJudge

dataset = Dataset(
    cases=[
        Case(
            name='capital_question',
            inputs='What is the capital of France?',
            expected_output='Paris',
        ),
    ],
    evaluators=[
        EqualsExpected(),
        LLMJudge(rubric='Response is factually accurate'),
    ],
)

async def my_agent(question: str) -> str:
    result = await agent.run(question)
    return result.output

report = dataset.evaluate_sync(my_agent)
report.print()
```

### Custom Evaluator

```python
from dataclasses import dataclass
from pydantic_evals.evaluators import Evaluator, EvaluatorContext

@dataclass
class ContainsKeyword(Evaluator):
    keyword: str

    def evaluate(self, ctx: EvaluatorContext) -> bool:
        return self.keyword.lower() in str(ctx.output).lower()
```

## MCP Integration

```python
from pydantic_ai import Agent, MCPServerTool
from pydantic_ai.mcp import MCPServerStdio

# Connect to MCP server
mcp_server = MCPServerStdio(
    'filesystem',
    command='uvx',
    args=['mcp-server-filesystem', '/data']
)

mcp_tool = MCPServerTool(mcp_server)

agent = Agent(
    'anthropic:claude-sonnet-4-0',
    builtin_tools=[mcp_tool],
)

result = agent.run_sync('List files in the data directory')
```

## Built-in Tools

```python
from pydantic_ai import Agent, WebSearchTool, CodeExecutionTool

agent = Agent(
    'openai:gpt-4o',
    builtin_tools=[
        WebSearchTool(max_uses=5),
        CodeExecutionTool(),
    ],
)
```

## Best Practices

### Dependency Design

1. Use `@dataclass` for dependencies (immutable, typed)
2. Include connection pools, not individual connections
3. Keep dependencies stateless when possible
4. Use `async with` for cleanup

### Tool Design

1. Write clear docstrings (used as tool descriptions)
2. Use type hints (converted to JSON schema)
3. Return simple types (str, dict, list)
4. Handle errors gracefully with `ModelRetry`

### Output Design

1. Use Pydantic models for structured output
2. Add Field descriptions for the LLM
3. Use union types for multiple possible outputs
4. Consider `NativeOutput` for speed

### Testing

1. Set `models.ALLOW_MODEL_REQUESTS = False` globally
2. Use `TestModel` for basic behavior tests
3. Use `FunctionModel` for complex scenarios
4. Test tool logic independently
5. Use `capture_run_messages()` to assert on conversations

### Production

1. Enable Logfire instrumentation
2. Set appropriate timeouts
3. Implement retry logic
4. Monitor costs via usage tracking
5. Consider durable execution with Temporal/Prefect

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Global state in tools | Race conditions | Use dependencies |
| Blocking I/O in async | Blocks event loop | Use sync function (runs in thread) |
| Large tool responses | Token waste | Return focused data |
| Missing docstrings | Poor tool descriptions | Document all tools |
| Hardcoded models | Inflexible | Use configuration |
| No output validation | Unreliable responses | Use Pydantic models |
| Testing with real API | Slow, costly, flaky | Use TestModel |
| Ignoring usage() | Cost overruns | Track and limit usage |
