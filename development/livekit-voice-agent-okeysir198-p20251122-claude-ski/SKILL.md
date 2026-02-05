---
name: livekit-voice-agent
description: Guide for building production-ready LiveKit voice AI agents with multi-agent workflows and intelligent handoffs. Use when creating real-time voice agents that need to transfer control between specialized agents, implement supervisor escalation, or build complex conversational systems.
license: MIT
---

# LiveKit Voice Agent with Multi-Agent Handoffs

Build production-ready voice AI agents using LiveKit Agents framework with support for multi-agent workflows, intelligent handoffs, and specialized agent capabilities.

---

## Overview

LiveKit Agents enables building real-time multimodal AI agents with voice capabilities. This skill helps you create sophisticated voice systems where multiple specialized agents can seamlessly hand off conversations based on context, user needs, or business logic.

### Key Capabilities

- **Multi-Agent Workflows**: Chain multiple specialized agents with different instructions, tools, and models
- **Intelligent Handoffs**: Transfer control between agents using function tools
- **Context Preservation**: Maintain conversation state and user data across agent transitions
- **Flexible Architecture**: Support for lateral handoffs (peer agents), escalations (human operators), and returns
- **Production Ready**: Built-in testing, Docker deployment, and monitoring support

---

## Architecture Patterns

### Core Components

1. **AgentSession**: Orchestrates the overall interaction, manages shared services (VAD, STT, LLM, TTS), and holds shared userdata
2. **Agent Classes**: Individual agents with specific instructions, function tools, and optional model overrides
3. **Handoff Mechanism**: Function tools that return new agent instances to transfer control
4. **Shared Context**: UserData dataclass that persists information across agent handoffs

### Workflow Structure

```
┌─────────────────────────────────────────────────┐
│           AgentSession (Orchestrator)           │
│  ├─ Shared VAD, STT, TTS, LLM services         │
│  ├─ Shared UserData context                    │
│  └─ Agent lifecycle management                  │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Agent A │  │ Agent B │  │ Agent C │
   │ ├─Instructions │ ├─Instructions │ ├─Instructions
   │ ├─Tools    │ ├─Tools    │ ├─Tools
   │ └─Handoff  │ └─Handoff  │ └─Handoff
   └─────────┘  └─────────┘  └─────────┘
```

---

## Implementation Process

### Phase 1: Research and Planning

#### 1.1 Study LiveKit Documentation

**Load core documentation:**
- LiveKit Agents Overview: Use WebFetch to load `https://docs.livekit.io/agents/`
- Building Voice Agents: `https://docs.livekit.io/agents/build/`
- Workflows Guide: `https://docs.livekit.io/agents/build/workflows/`
- Testing Framework: `https://docs.livekit.io/agents/build/testing/`

**Study example implementations:**
- Agent Starter Template: `https://github.com/livekit-examples/agent-starter-python`
- Multi-Agent Example: `https://github.com/livekit-examples/multi-agent-python`
- Voice Agent Examples: `https://github.com/livekit/agents/tree/main/examples/voice_agents`

**Load reference documentation:**
- [📋 Agent Best Practices](./reference/agent_best_practices.md)
- [🏗️ Multi-Agent Patterns](./reference/multi_agent_patterns.md)
- [🧪 Testing Guide](./reference/testing_guide.md)

#### 1.2 Define Your Use Case

Determine your agent workflow:

**Customer Support Pattern:**
```
Greeting Agent → Triage Agent → Technical Support → Escalation Agent
```

**Sales Pipeline Pattern:**
```
Intro Agent → Qualification Agent → Demo Agent → Account Executive Handoff
```

**Service Workflow Pattern:**
```
Reception Agent → Information Gathering → Specialist Agent → Confirmation Agent
```

**Plan your agents:**
- List each agent needed
- Define the role and instructions for each
- Identify handoff triggers and conditions
- Specify tools needed per agent
- Determine if agents need different models (STT/LLM/TTS)

#### 1.3 Design Shared Context

Create a dataclass to store information that persists across agents:

```python
from dataclasses import dataclass, field

@dataclass
class ConversationData:
    """Shared context across all agents"""
    user_name: str = ""
    user_email: str = ""
    issue_category: str = ""
    collected_details: list[str] = field(default_factory=list)
    escalation_needed: bool = False
    # Add fields relevant to your use case
```

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

Use the provided template as a starting point:

```
your-agent-project/
├── src/
│   ├── agent.py              # Main entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── intro_agent.py    # Initial agent
│   │   ├── specialist_agent.py
│   │   └── escalation_agent.py
│   ├── models/
│   │   └── shared_data.py    # UserData dataclass
│   └── tools/
│       └── custom_tools.py   # Business-specific tools
├── tests/
│   └── test_agent.py         # pytest tests
├── pyproject.toml            # Dependencies with uv
├── .env.example              # Environment variables template
├── Dockerfile                # Container definition
└── README.md
```

**Use the quick start script or copy template files:**
- See [⚡ Quick Start Script](./scripts/quickstart.sh) for automated setup
- Or manually copy files from `./templates/` directory

#### 2.2 Initialize Project

**Install uv package manager:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Create project with dependencies:**
```bash
# Initialize project
uv init your-agent-project
cd your-agent-project

# Add dependencies
uv add "livekit-agents>=1.3.3"
uv add "livekit-plugins-openai"      # For OpenAI LLM & TTS
uv add "livekit-plugins-deepgram"    # For Deepgram STT
uv add "livekit-plugins-silero"      # For Silero VAD
uv add "python-dotenv"               # For environment variables

# Add testing dependencies
uv add --dev "pytest"
uv add --dev "pytest-asyncio"
```

**Set up environment variables:**
```bash
# Copy from template
cp .env.example .env

# Edit with your credentials
# LIVEKIT_URL=wss://your-livekit-server.com
# LIVEKIT_API_KEY=your-api-key
# LIVEKIT_API_SECRET=your-api-secret
# OPENAI_API_KEY=your-openai-key
# DEEPGRAM_API_KEY=your-deepgram-key
```

#### 2.3 Implement Core Infrastructure

**Create main entry point (src/agent.py):**

Load the complete template: [🚀 Main Entry Point Template](./templates/main_entry_point.py)

Key patterns:
- Use `prewarm()` to load static resources (VAD models) before sessions start
- Initialize `AgentSession[YourDataClass]` with shared services
- Start with your initial agent in the entrypoint
- Use `@server.rtc_session()` decorator for the main handler

**Example structure:**
```python
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, deepgram, silero
import logging
from dotenv import load_dotenv

from agents.intro_agent import IntroAgent
from models.shared_data import ConversationData

load_dotenv()
logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    """Load static resources before sessions start"""
    # Load VAD model once and reuse across sessions
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main agent entry point"""
    logger.info("Starting voice agent session")

    # Get prewarmed VAD
    vad = ctx.proc.userdata["vad"]

    # Initialize session with shared services
    session = AgentSession[ConversationData](
        vad=vad,
        stt=deepgram.STT(model="nova-2-general"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
        userdata=ConversationData(),
    )

    # Connect to room
    await ctx.connect()

    # Start with intro agent
    intro_agent = IntroAgent()

    # Run session (handles all handoffs automatically)
    await session.start(agent=intro_agent, room=ctx.room)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )
```

#### 2.4 Implement Agent Classes

**Agent structure:**

Each agent should:
1. Extend the `Agent` base class
2. Define instructions in `__init__`
3. Implement function tools for capabilities
4. Include handoff tools that return new agent instances

**Load templates:**
- [🤖 Intro Agent Template](./templates/agents/intro_agent.py)
- [🎯 Specialist Agent Template](./templates/agents/specialist_agent.py)
- [📞 Escalation Agent Template](./templates/agents/escalation_agent.py)

**Example agent with handoff:**

```python
from livekit.agents import Agent, RunContext
from livekit.agents.llm import function_tool
from typing import Annotated

from models.shared_data import ConversationData
from agents.specialist_agent import SpecialistAgent


class IntroAgent(Agent):
    """Initial agent that greets users and routes to specialists"""

    def __init__(self):
        super().__init__(
            instructions="""You are a friendly voice assistant that helps customers.

Your role:
1. Greet the user warmly
2. Ask for their name and what they need help with
3. Gather basic information about their request
4. Transfer to a specialist agent when you have enough information

Be conversational, friendly, and efficient. Once you understand their
need and have their name, immediately transfer to the specialist."""
        )

    @function_tool
    async def transfer_to_specialist(
        self,
        context: RunContext[ConversationData],
        user_name: Annotated[str, "The user's name"],
        issue_category: Annotated[str, "Category: technical, billing, or general"],
        issue_description: Annotated[str, "Brief description of the user's issue"],
    ):
        """Transfer the conversation to a specialist agent.

        Call this when you have gathered the user's name and understand
        their issue well enough to categorize it.
        """
        # Store data in shared context
        context.userdata.user_name = user_name
        context.userdata.issue_category = issue_category
        context.userdata.collected_details.append(issue_description)

        # Create and return specialist agent
        specialist = SpecialistAgent(
            category=issue_category,
            chat_ctx=self.chat_ctx,  # Preserve conversation history
        )

        return specialist, f"Let me connect you with our {issue_category} specialist."
```

**Key handoff patterns:**

1. **Store context**: Update `context.userdata` with collected information
2. **Create new agent**: Instantiate the next agent with relevant parameters
3. **Preserve history**: Pass `chat_ctx=self.chat_ctx` to maintain conversation
4. **Return tuple**: `(new_agent, transition_message)`

#### 2.5 Implement Custom Tools

Add business-specific tools to your agents using `@function_tool`:

```python
from livekit.agents.llm import function_tool
from livekit.agents import RunContext
from typing import Annotated

@function_tool
async def lookup_order_status(
    context: RunContext,
    order_id: Annotated[str, "The order ID to look up"],
) -> str:
    """Look up the status of an order by order ID.

    Returns the current status, shipping info, and estimated delivery.
    """
    # Your API call here
    try:
        # result = await your_api.get_order(order_id)
        return f"Order {order_id} is currently being processed..."
    except Exception as e:
        raise ToolError(f"Could not find order {order_id}. Please verify the order ID.")


@function_tool
async def schedule_callback(
    context: RunContext,
    phone_number: Annotated[str, "Customer's phone number"],
    preferred_time: Annotated[str, "Preferred callback time"],
) -> str:
    """Schedule a callback for the customer."""
    # Your scheduling logic here
    return f"Callback scheduled for {preferred_time}"
```

**Best practices for tools:**
- Use clear, descriptive names
- Provide detailed docstrings (LLM sees these)
- Use `Annotated` to add parameter descriptions
- Return actionable error messages using `ToolError`
- Keep tools focused on single responsibilities

#### 2.6 Configure Model Services

**Override services per agent:**

Different agents can use different models:

```python
from livekit.plugins import openai, elevenlabs

class EscalationAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You help escalate issues to human operators...",
            # Use a different TTS for this agent
            tts=elevenlabs.TTS(
                voice="professional_voice_id",
            ),
            # Use a more capable LLM
            llm=openai.LLM(model="gpt-4o"),
        )
```

**Available plugins:**

**LLM Providers:**
- `livekit-plugins-openai`: GPT-4o, GPT-4o-mini
- `livekit-plugins-anthropic`: Claude Sonnet, Opus
- `livekit-plugins-groq`: Fast Llama inference

**STT Providers:**
- `livekit-plugins-deepgram`: Nova-2 models
- `livekit-plugins-assemblyai`: Universal streaming
- `livekit-plugins-google`: Google Speech-to-Text

**TTS Providers:**
- `livekit-plugins-openai`: Natural voices
- `livekit-plugins-elevenlabs`: High-quality voices
- `livekit-plugins-cartesia`: Low-latency Sonic models

**VAD:**
- `livekit-plugins-silero`: Multilingual voice detection

---

### Phase 3: Testing and Quality

#### 3.1 Write Behavioral Tests

LiveKit provides a testing framework with pytest integration.

**Load testing guide:** [🧪 Complete Testing Guide](./reference/testing_guide.md)

**Example test structure:**

```python
import pytest
from livekit.agents import AgentSession
from livekit.plugins import openai
from agents.intro_agent import IntroAgent
from models.shared_data import ConversationData


@pytest.mark.asyncio
async def test_intro_agent_greeting():
    """Test that intro agent greets user properly"""
    async with AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        userdata=ConversationData(),
    ) as sess:
        agent = IntroAgent()
        await sess.start(agent)

        result = await sess.run(user_input="Hello")

        # Assert greeting behavior
        result.expect.next_event().is_message(role="assistant")
        result.expect.contains_message("help")


@pytest.mark.asyncio
async def test_handoff_to_specialist():
    """Test that agent hands off correctly with context"""
    async with AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        userdata=ConversationData(),
    ) as sess:
        agent = IntroAgent()
        await sess.start(agent)

        result = await sess.run(
            user_input="Hi, I'm John and I need help with my billing"
        )

        # Expect function call for handoff
        result.expect.next_event().is_function_call(name="transfer_to_specialist")

        # Verify userdata was updated
        assert sess.userdata.user_name == "John"
        assert "billing" in sess.userdata.issue_category.lower()


@pytest.mark.asyncio
async def test_tool_usage():
    """Test that agent correctly uses custom tools"""
    async with AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        userdata=ConversationData(),
    ) as sess:
        agent = SpecialistAgent(category="technical")
        await sess.start(agent)

        result = await sess.run(
            user_input="What's the status of order #12345?"
        )

        # Expect tool call
        result.expect.next_event().is_function_call(name="lookup_order_status")
        result.expect.next_event().is_function_call_output()
```

**Testing areas:**
- ✅ Expected behavior (greetings, responses, tone)
- ✅ Tool usage (correct arguments, error handling)
- ✅ Handoff logic (context preservation, timing)
- ✅ Error handling (invalid inputs, failures)
- ✅ Grounding (factual responses, no hallucinations)

**Run tests:**
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_agent.py::test_handoff_to_specialist
```

#### 3.2 Quality Checklist

Before deployment, verify:

**Code Quality:**
- [ ] No duplicated code
- [ ] Consistent error handling
- [ ] Clear agent instructions
- [ ] All tools have descriptions
- [ ] Type hints throughout

**Functionality:**
- [ ] All agents initialize correctly
- [ ] Handoffs preserve context
- [ ] Tools execute successfully
- [ ] Error cases handled gracefully
- [ ] Conversation flows naturally

**Performance:**
- [ ] VAD prewarmed in prewarm()
- [ ] No blocking operations in entrypoint before ctx.connect()
- [ ] Appropriate models selected (balance quality/latency)
- [ ] Timeout handling implemented

**Testing:**
- [ ] Unit tests for each agent
- [ ] Integration tests for handoffs
- [ ] Tool tests with mocked APIs
- [ ] Error scenario tests

---

### Phase 4: Deployment

#### 4.1 Docker Deployment

**Load Dockerfile template:** [🐳 Dockerfile Template](./templates/Dockerfile)

**Example Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen

# Run agent
CMD ["uv", "run", "python", "src/agent.py", "start"]
```

**Build and run:**
```bash
# Build image
docker build -t your-voice-agent .

# Run container
docker run -d \
  --env-file .env \
  --name voice-agent \
  your-voice-agent
```

#### 4.2 Environment Configuration

**Production environment variables:**

```bash
# LiveKit Connection
LIVEKIT_URL=wss://your-production-server.com
LIVEKIT_API_KEY=your-production-key
LIVEKIT_API_SECRET=your-production-secret

# AI Services
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...

# Agent Configuration
LOG_LEVEL=INFO
NUM_IDLE_PROCESSES=3  # Number of warmed processes to keep ready
```

#### 4.3 Monitoring and Observability

**Add logging:**

```python
import logging

logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

# In your agents
logger.info(f"Starting session with user: {context.userdata.user_name}")
logger.info(f"Handoff from {self.__class__.__name__} to SpecialistAgent")
logger.error(f"Tool execution failed: {error}")
```

**Track metrics:**

```python
from livekit.agents import metrics

# Create usage collector
collector = metrics.UsageCollector()

# In entrypoint
session = AgentSession[ConversationData](
    # ... other params
    usage_collector=collector,
)

# Log usage on completion
@ctx.on("agent_completed")
async def log_metrics():
    logger.info(f"Session usage: {collector.get_summary()}")
```

**Monitor:**
- Time to first word (< 500ms target)
- Handoff success rates
- Tool execution times
- Error rates and types
- Audio quality metrics

#### 4.4 Scaling Considerations

**Worker Options:**

```python
cli.run_app(
    WorkerOptions(
        entrypoint_fnc=entrypoint,
        prewarm_fnc=prewarm,
        num_idle_processes=3,  # Processes to keep warm
    )
)
```

**Production settings:**
- **Development**: `num_idle_processes=0` (no warming)
- **Production**: `num_idle_processes=3+` (keep processes ready)

**Kubernetes deployment:**
- Use horizontal pod autoscaling
- Set resource limits appropriately
- Use liveness/readiness probes
- Configure rolling updates

---

## Common Patterns

### Pattern 1: Customer Support Workflow

```python
# Entry flow
GreetingAgent → TriageAgent → SupportAgent → EscalationAgent
                                    ↓
                            (Resolves issue or escalates)
```

**Use when:**
- Building customer service agents
- Need issue categorization
- Require human escalation path

### Pattern 2: Sales Pipeline

```python
IntroAgent → QualificationAgent → DemoAgent → HandoffAgent
                ↓
        (Disqualified → FollowUpAgent)
```

**Use when:**
- Lead qualification needed
- Multi-step sales process
- Different agents for stages

### Pattern 3: Information Collection

```python
WelcomeAgent → DataCollectionAgent → VerificationAgent → ConfirmationAgent
```

**Use when:**
- Form filling via voice
- Multi-step data gathering
- Verification required

### Pattern 4: Dynamic Routing

```python
RouterAgent ─┬→ TechnicalAgent
             ├→ BillingAgent
             ├→ SalesAgent
             └→ GeneralAgent
```

**Use when:**
- Intent-based routing
- Multiple specialist agents
- Dynamic capability selection

---

## Best Practices

### Agent Design

✅ **DO:**
- Keep agent instructions clear and focused
- Define specific roles per agent
- Use handoffs for distinct capability changes
- Preserve relevant context across handoffs
- Announce handoffs to users clearly

❌ **DON'T:**
- Create agents for trivial differences
- Duplicate tools across agents unnecessarily
- Handoff too frequently (confuses users)
- Lose important context in transitions

### Handoff Timing

**Good handoff triggers:**
- User requests a specialist
- Agent completes its specific task
- Different tools/permissions needed
- Escalation conditions met

**Poor handoff triggers:**
- Minor topic changes
- After every user message
- Without clear purpose

### Context Management

**Always preserve:**
- User identification (name, ID)
- Request/issue details
- Conversation history (via `chat_ctx`)
- Critical decisions made

**Consider resetting:**
- Temporary working data
- Search results
- Non-critical metadata

### Tool Design

**Effective tools:**
- Single, clear purpose
- Descriptive names (action-oriented)
- Detailed docstrings
- Graceful error handling
- Appropriate scope per agent

**Tool organization:**
- Common tools: Available to all agents
- Specialist tools: Only for relevant agents
- Handoff tools: Control transfer capabilities

---

## Troubleshooting

### Issue: Handoff Not Triggering

**Symptoms:** Agent doesn't call transfer function

**Solutions:**
- Verify function tool is registered (use `@function_tool`)
- Check instructions clearly mention when to transfer
- Ensure LLM has enough context to decide
- Test with explicit user requests

### Issue: Context Lost After Handoff

**Symptoms:** New agent doesn't know previous information

**Solutions:**
- Ensure `context.userdata` is updated before handoff
- Pass `chat_ctx=self.chat_ctx` to preserve history
- Verify shared data class is properly typed
- Check new agent instructions reference available context

### Issue: Poor Voice Quality

**Symptoms:** Audio cutting out, robotic voice

**Solutions:**
- Check network connectivity
- Verify STT/TTS API keys are valid
- Consider lower-latency models
- Adjust VAD sensitivity
- Monitor latency metrics

### Issue: Tools Not Being Called

**Symptoms:** Agent doesn't use available tools

**Solutions:**
- Improve tool descriptions (LLM-friendly)
- Add examples in docstrings
- Simplify parameter requirements
- Check tool registration
- Verify instructions mention tool usage

### Issue: High Latency

**Symptoms:** Slow responses, delays

**Solutions:**
- Ensure VAD loaded in `prewarm()`
- Use faster models (e.g., gpt-4o-mini)
- Avoid API calls before `ctx.connect()`
- Consider streaming responses
- Check network latency to services

---

## Example Use Cases

The templates and patterns in this skill support various use cases:

### Restaurant Ordering Agent

**Flow:** Welcome → Menu Navigation → Order Taking → Payment → Confirmation

**Implementation:** Use Linear Pipeline pattern from [Multi-Agent Patterns](./reference/multi_agent_patterns.md) with the OrderData model from [shared_data.py](./templates/models/shared_data.py).

### Technical Support Agent

**Flow:** Greeting → Triage → Troubleshooting → Resolution/Escalation

**Implementation:** Use Escalation Hierarchy pattern with the SupportTicket model. See the provided templates for intro, specialist, and escalation agents.

### Appointment Booking Agent

**Flow:** Reception → Availability Check → Booking → Confirmation

**Implementation:** Use Linear Pipeline pattern. Customize ConversationData to track appointment details, availability, and booking confirmation.

**Note:** The templates in `./templates/` provide a complete working implementation. Adapt the agents and data models to your specific use case.

---

## Reference Files

### 📚 Documentation Library

Load these resources as needed:

#### Core LiveKit Documentation
- **LiveKit Agents Docs**: Start at `https://docs.livekit.io/agents/`
- **Building Voice Agents**: `https://docs.livekit.io/agents/build/`
- **Workflows**: `https://docs.livekit.io/agents/build/workflows/`
- **Tool Definition**: `https://docs.livekit.io/agents/build/tools/`
- **Testing Framework**: `https://docs.livekit.io/agents/build/testing/`

#### Example Repositories
- **Agent Starter**: `https://github.com/livekit-examples/agent-starter-python`
- **Multi-Agent**: `https://github.com/livekit-examples/multi-agent-python`
- **Voice Examples**: `https://github.com/livekit/agents/tree/main/examples/voice_agents`

#### Local Reference Files
- [📋 Agent Best Practices](./reference/agent_best_practices.md)
- [🏗️ Multi-Agent Patterns](./reference/multi_agent_patterns.md)
- [🧪 Testing Guide](./reference/testing_guide.md)

#### Templates
- [🚀 Main Entry Point](./templates/main_entry_point.py)
- [🤖 Intro Agent](./templates/agents/intro_agent.py)
- [🎯 Specialist Agent](./templates/agents/specialist_agent.py)
- [📞 Escalation Agent](./templates/agents/escalation_agent.py)
- [📦 Shared Data Models](./templates/models/shared_data.py)
- [🔧 pyproject.toml](./templates/pyproject.toml)
- [🐳 Dockerfile](./templates/Dockerfile)
- [📝 .env.example](./templates/.env.example)

---

## Quick Start

For a fast start with a working example:

1. **Load the quick start script:** [⚡ Quick Start Script](./scripts/quickstart.sh)
2. **Run:** `./scripts/quickstart.sh my-agent-project`
3. **Follow the generated README for setup instructions**

This creates a complete project with:
- Working multi-agent setup (Intro → Specialist → Escalation)
- Example tools and handoffs
- Test suite with pytest
- Docker deployment ready
- Environment configuration

---

## Additional Resources

- **LiveKit Cloud**: Deploy without managing infrastructure at `https://cloud.livekit.io`
- **Community**: Join LiveKit Discord for support
- **Examples**: Browse `https://github.com/livekit-examples` for more patterns
- **API Reference**: Full Python API at `https://docs.livekit.io/reference/python/`

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review LiveKit documentation at docs.livekit.io
3. Search GitHub issues: `https://github.com/livekit/agents/issues`
4. Join LiveKit Discord community
