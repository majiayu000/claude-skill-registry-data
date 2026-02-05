---
name: AgnoAGI Agents
description: Expert guidance for building AI agents with Agno framework, including multi-agent systems, reasoning agents, tools integration, memory, knowledge, and production deployment
version: 1.0.0
---

# AgnoAGI Agents Framework

Complete guide for building production-ready AI agents and multi-agent systems with Agno (formerly Phidata).

## Installation and Setup

```bash
# Install Agno
pip install agno

# With specific model providers
pip install 'agno[anthropic]'
pip install 'agno[openai]'
pip install 'agno[groq]'
pip install 'agno[ollama]'

# Install tools
pip install yfinance duckduckgo-search newspaper4k sqlalchemy

# Full installation
pip install 'agno[all]'
```

## Quick Start

### Basic Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Create simple agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are a helpful AI assistant",
    markdown=True
)

# Run agent
agent.print_response("What is quantum computing?", stream=True)
```

### Agent with Tools

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

# Agent with web search capability
web_agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest"),
    tools=[DuckDuckGoTools()],
    description="You are a research assistant that can search the web",
    instructions=[
        "Always search for current information",
        "Cite your sources",
        "Provide comprehensive answers"
    ],
    show_tool_calls=True,
    markdown=True
)

# Use the agent
web_agent.print_response("What are the latest developments in AI?", stream=True)
```

## Agent Configuration

### Complete Agent Setup

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.memory.db.postgres import PostgresMemory

agent = Agent(
    # Model configuration
    model=OpenAIChat(
        id="gpt-4o",
        temperature=0.7,
        max_tokens=2000
    ),

    # Agent identity
    name="Finance Assistant",
    role="Financial analyst and advisor",
    description="Expert in financial analysis and market research",

    # Instructions
    instructions=[
        "Use tables to display financial data",
        "Always include current date in analysis",
        "Explain your reasoning step by step",
        "Cite data sources"
    ],

    # Tools
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True
        )
    ],

    # Memory
    memory=PostgresMemory(
        table_name="agent_memory",
        db_url="postgresql://user:pass@localhost:5432/agno"
    ),

    # Storage for sessions
    storage=PostgresStorage(
        table_name="agent_sessions",
        db_url="postgresql://user:pass@localhost:5432/agno"
    ),

    # Display options
    show_tool_calls=True,
    markdown=True,
    debug_mode=False,

    # Add timestamps to responses
    add_datetime_to_instructions=True,

    # Prevent prompt injection
    prevent_prompt_injection=True,

    # Custom system prompt
    system_prompt="You are a professional financial analyst..."
)
```

## Working with Different Models

### Anthropic Claude

```python
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(
        id="claude-3-7-sonnet-latest",
        temperature=0.7,
        max_tokens=4096
    ),
    description="Helpful assistant powered by Claude"
)
```

### OpenAI

```python
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(
        id="gpt-4o",
        temperature=0.8
    )
)
```

### Groq (Fast Inference)

```python
from agno.models.groq import Groq

agent = Agent(
    model=Groq(
        id="llama-3.3-70b-versatile",
        # or "mixtral-8x7b-32768"
    ),
    description="Fast agent powered by Groq"
)
```

### Ollama (Local Models)

```python
from agno.models.ollama import Ollama

agent = Agent(
    model=Ollama(
        id="llama3.2",
        # host="http://localhost:11434"  # Custom Ollama host
    ),
    description="Local AI agent"
)
```

### Google Gemini

```python
from agno.models.gemini import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp")
)
```

## Built-in Tools

### Web Search

```python
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=["Always search for up-to-date information"]
)
```

### Finance Tools

```python
from agno.tools.yfinance import YFinanceTools

finance_agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest"),
    tools=[
        YFinanceTools(
            stock_price=True,
            stock_fundamentals=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            historical_prices=True
        )
    ],
    instructions=["Use tables to display data"]
)

finance_agent.print_response("Analyze Tesla stock performance", stream=True)
```

### File Tools

```python
from agno.tools.file import FileTools

file_agent = Agent(
    tools=[FileTools()],
    instructions=["Help users manage their files"]
)
```

### Python Tools

```python
from agno.tools.python import PythonTools

code_agent = Agent(
    tools=[PythonTools()],
    instructions=[
        "Write clean, well-documented Python code",
        "Run code to verify it works"
    ]
)
```

### Shell Tools

```python
from agno.tools.shell import ShellTools

shell_agent = Agent(
    tools=[ShellTools()],
    instructions=["Execute shell commands safely"]
)
```

## Custom Tools

### Creating Custom Tools

```python
from agno.agent import Agent
from agno.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city.

    Args:
        city: The city name

    Returns:
        Weather information as a string
    """
    # Your weather API logic here
    return f"Weather in {city}: Sunny, 72°F"

@tool
def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int
) -> dict:
    """Calculate monthly mortgage payment.

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (e.g., 0.05 for 5%)
        years: Loan term in years

    Returns:
        Dictionary with payment details
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12

    monthly_payment = principal * (
        monthly_rate * (1 + monthly_rate) ** num_payments
    ) / ((1 + monthly_rate) ** num_payments - 1)

    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_paid': round(monthly_payment * num_payments, 2),
        'total_interest': round(monthly_payment * num_payments - principal, 2)
    }

# Use custom tools
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[get_weather, calculate_mortgage],
    instructions=["Use the tools to help users"]
)

agent.print_response("What's the weather in Paris?")
agent.print_response("Calculate mortgage for $500,000 at 6.5% for 30 years")
```

### Tool Class

```python
from agno.tools import Toolkit
from typing import Optional

class DatabaseTools(Toolkit):
    """Custom database toolkit"""

    def __init__(self, connection_string: str):
        super().__init__(name="database_tools")
        self.connection_string = connection_string

    @tool
    def query_users(self, limit: int = 10) -> list:
        """Query users from database.

        Args:
            limit: Maximum number of users to return

        Returns:
            List of user dictionaries
        """
        # Database query logic
        return [{"id": 1, "name": "John"}]

    @tool
    def insert_user(self, name: str, email: str) -> dict:
        """Insert new user.

        Args:
            name: User name
            email: User email

        Returns:
            Created user dictionary
        """
        # Insert logic
        return {"id": 2, "name": name, "email": email}

# Use toolkit
agent = Agent(
    tools=[DatabaseTools("postgresql://localhost/mydb")]
)
```

## Multi-Agent Systems

### Agent Teams

```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# Create specialized agents
web_researcher = Agent(
    name="Web Researcher",
    role="Search the web for information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Search for current and accurate information",
        "Always cite sources"
    ],
    markdown=True
)

finance_analyst = Agent(
    name="Finance Analyst",
    role="Analyze financial data and stocks",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True
        )
    ],
    instructions=[
        "Use tables to display data",
        "Provide detailed analysis"
    ],
    markdown=True
)

writer_agent = Agent(
    name="Writer",
    role="Create well-written reports",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Write clear, professional reports",
        "Use markdown formatting",
        "Include all information from other agents"
    ],
    markdown=True
)

# Create team
research_team = Agent(
    name="Research Team",
    team=[web_researcher, finance_analyst, writer_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Coordinate team members effectively",
        "Ensure comprehensive research",
        "Produce high-quality final report"
    ],
    markdown=True
)

# Use team
research_team.print_response(
    "Research NVIDIA: current stock price, recent news, and market analysis. Provide a comprehensive report.",
    stream=True
)
```

## Reasoning Agents

### Basic Reasoning

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools

reasoning_agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest"),
    tools=[ReasoningTools(add_instructions=True)],
    reasoning=True,  # Enable reasoning
    markdown=True
)

reasoning_agent.print_response(
    "If I have 3 boxes, each containing 4 bags, and each bag has 5 apples, how many apples do I have?",
    stream=True,
    show_full_reasoning=True
)
```

### Reasoning with Tools

```python
from agno.tools.yfinance import YFinanceTools

reasoning_finance_agent = Agent(
    model=Claude(id="claude-3-7-sonnet-latest"),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(stock_price=True, analyst_recommendations=True)
    ],
    reasoning=True,
    instructions=[
        "Think step by step",
        "Use reasoning before making conclusions",
        "Show your work"
    ],
    markdown=True
)

reasoning_finance_agent.print_response(
    "Should I invest in Tesla or Apple? Analyze both stocks and provide a reasoned recommendation.",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True
)
```

## Memory and Knowledge

### Database Memory

```python
from agno.memory.db.postgres import PostgresMemory
from agno.storage.postgres import PostgresStorage

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    memory=PostgresMemory(
        table_name="agent_memory",
        db_url="postgresql://user:pass@localhost:5432/agno"
    ),
    storage=PostgresStorage(
        table_name="agent_sessions",
        db_url="postgresql://user:pass@localhost:5432/agno"
    ),
    # Create tables automatically
    create_storage=True,
    create_memory=True
)
```

### Session Management

```python
# Start new session
session_id = agent.session_id

# Continue existing session
agent = Agent(
    session_id="previous-session-id",
    memory=PostgresMemory(...),
    model=OpenAIChat(id="gpt-4o")
)

# Agent remembers previous conversations
agent.print_response("What did we discuss earlier?")
```

### Knowledge Base

```python
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.pgvector import PgVector

# Create knowledge base
knowledge = TextKnowledgeBase(
    path="docs/",  # Directory with documents
    vector_db=PgVector(
        table_name="agent_knowledge",
        db_url="postgresql://user:pass@localhost:5432/agno"
    )
)

# Load knowledge
knowledge.load(recreate=False)

# Agent with knowledge
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True,  # Enable RAG
    instructions=[
        "Use knowledge base to answer questions",
        "Cite sources when using knowledge"
    ]
)

agent.print_response("What does our documentation say about API authentication?")
```

## Production Deployment

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

app = FastAPI(title="Agno Agent API")

# Initialize agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with agent"""
    try:
        # Set session if provided
        if request.session_id:
            agent.session_id = request.session_id

        # Get response
        response = agent.run(request.message)

        return ChatResponse(
            response=response.content,
            session_id=agent.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM agnohq/python:3.12

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://agno:agno@db:5432/agno
    depends_on:
      - db

  db:
    image: pgvector/pgvector:pg17
    environment:
      - POSTGRES_DB=agno
      - POSTGRES_USER=agno
      - POSTGRES_PASSWORD=agno
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Production Configuration

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.db.postgres import PostgresMemory
from agno.storage.postgres import PostgresStorage
import os

def create_production_agent():
    """Create production-ready agent"""
    return Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=30,
            max_retries=3
        ),
        memory=PostgresMemory(
            table_name="agent_memory",
            db_url=os.getenv("DATABASE_URL")
        ),
        storage=PostgresStorage(
            table_name="agent_sessions",
            db_url=os.getenv("DATABASE_URL")
        ),
        # Production settings
        debug_mode=False,
        monitoring=True,
        prevent_prompt_injection=True,
        markdown=True
    )
```

## Advanced Patterns

### Agentic RAG

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.pgvector import PgVector

# Create knowledge base
kb = TextKnowledgeBase(
    path="documentation/",
    vector_db=PgVector(
        table_name="docs_knowledge",
        db_url="postgresql://localhost/agno"
    )
)

# Load documents
kb.load()

# Create agent
rag_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=kb,
    search_knowledge=True,
    instructions=[
        "Search knowledge base for relevant information",
        "Always cite sources",
        "If information is not in knowledge base, say so"
    ]
)
```

### Streaming Responses

```python
agent = Agent(model=OpenAIChat(id="gpt-4o"))

# Stream response
response = agent.run("Explain machine learning", stream=True)

for chunk in response:
    print(chunk.content, end="", flush=True)
```

### Error Handling

```python
from agno.agent import Agent, RunResponse

def safe_agent_run(agent: Agent, message: str) -> RunResponse | None:
    """Run agent with error handling"""
    try:
        response = agent.run(message)
        return response
    except Exception as e:
        print(f"Agent error: {e}")
        return None
```

## MCP (Model Context Protocol) Integration

```python
from agno.tools.mcp import MCPTools

# Use MCP server
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        MCPTools(
            server_name="notion",
            config={
                "command": "npx",
                "args": ["-y", "@notionhq/mcp-server-notion"],
                "env": {"NOTION_API_KEY": os.getenv("NOTION_API_KEY")}
            }
        )
    ]
)
```

## Best Practices

1. **Use appropriate models** - Balance cost, speed, and quality
2. **Enable memory for context** - Better conversations
3. **Add knowledge bases** - Domain-specific expertise
4. **Use reasoning for complex tasks** - Better decision making
5. **Create specialized agents** - Single responsibility
6. **Coordinate with teams** - Complex workflows
7. **Stream responses** - Better UX
8. **Handle errors gracefully** - Retry logic
9. **Monitor in production** - Track performance
10. **Secure API keys** - Use environment variables

## Performance Tips

- Use Groq for fast inference
- Use Ollama for privacy/cost savings
- Cache knowledge embeddings
- Implement connection pooling for databases
- Use async operations where possible
- Batch process requests
- Set reasonable timeouts
- Monitor token usage

## Key Principles

- **Agents are 529× faster than Langgraph**
- **Built for production from day one**
- **Supports all major model providers**
- **Easy to extend with custom tools**
- **Memory and knowledge out of the box**
- **Team coordination built-in**
- **Reasoning capabilities included**
- **MCP support for integrations**

## Resources

- Documentation: https://docs.agno.com/
- GitHub: https://github.com/agno-agi/agno
- Examples: https://github.com/agno-agi/agno/tree/main/cookbook
- PyPI: https://pypi.org/project/agno/
- Discord: Join Agno community
- Blog: https://www.agno.com/blog
