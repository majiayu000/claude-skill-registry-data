---
name: stagehand
description: Stagehand Python AI-powered browser automation. Use for web scraping, form filling, clicking elements, extracting structured data, and autonomous multi-step browser workflows. Covers act(), extract(), observe() methods and Computer Use Agent patterns.
version: 1.0.0
---

# Stagehand Python Browser Automation Skill

AI-powered browser automation using Stagehand Python with `act`, `extract`, `observe`, and `agent` methods.

## Overview

[Stagehand Python](https://github.com/browserbase/stagehand-python) provides AI-powered browser automation built on Playwright with:
- **act()**: Perform actions using natural language
- **extract()**: Extract structured data using Pydantic schemas
- **observe()**: Plan actions and get selectors before executing
- **agent()**: Create autonomous agents for complex multi-step workflows

**Key Mental Model**: Use natural language instructions for browser interactions. Keep actions atomic. Always use Pydantic schemas for data extraction.

---

## Quick Reference

| What You Need | Method |
|---------------|--------|
| Click/type/interact | `page.act("Click the submit button")` |
| Extract data | `page.extract("Get all product prices", schema=PriceList)` |
| Plan before acting | `page.observe("Find the login form")` |
| Complex workflows | `agent.execute("Fill out the form and submit")` |

---

## Configuration

```python
from stagehand import Stagehand, StagehandConfig
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    config = StagehandConfig(
        env="BROWSERBASE",  # or "LOCAL" for local browser
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("MODEL_API_KEY"),
        verbose=1,  # 0=minimal, 1=medium, 2=detailed
        dom_settle_timeout_ms=30000,
        self_heal=True,
    )
    
    # Recommended: Use as async context manager
    async with Stagehand(config) as stagehand:
        page = stagehand.page
        # Your automation code here
        
if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `env` | `"BROWSERBASE"` or `"LOCAL"` | `"BROWSERBASE"` |
| `api_key` | Browserbase API key | Required for BROWSERBASE |
| `project_id` | Browserbase project ID | Required for BROWSERBASE |
| `model_name` | AI model for instructions | Required |
| `model_api_key` | API key for the AI model | Required |
| `verbose` | Logging level (0-2) | 1 |
| `dom_settle_timeout_ms` | DOM settle timeout | 30000 |
| `self_heal` | Enable self-healing | True |

---

## Core Methods

### 1. act() - Perform Actions

Execute actions using natural language. **Keep actions atomic and specific.**

```python
# Simple actions
await page.act("Click the sign in button")
await page.act("Type 'hello world' into the search input")
await page.act("Select 'United States' from the country dropdown")

# Form filling with variables
await page.act("Enter name 'John Doe' and email 'john@example.com'")
```

**CRITICAL**: Actions should be atomic (single step).

```python
# GOOD: Atomic actions
await page.act("Click the submit button")
await page.act("Type 'password123' into the password field")

# BAD: Multi-step actions (AVOID)
await page.act("Order me a pizza")
await page.act("Sign in and navigate to settings")
```

### 2. observe() - Plan Before Acting

Plan actions and get selectors before executing. Results can be passed directly to `act()`.

```python
# Get action plan
results = await page.observe("Click the sign in button")

# Use result directly in act()
await page.act(results[0])

# With visual overlay for debugging
results = await page.observe(
    instruction="Find all navigation links",
    draw_overlay=True
)
```

**Use observe() when:**
- Page has multiple similar elements
- DOM is dynamic/changing
- You need to cache selectors for repeated use

### 3. extract() - Extract Structured Data

Extract data using Pydantic schemas. **Always use schemas for structured data.**

#### Simple String Extraction

```python
button_text = await page.extract("Get the sign in button text")
```

#### Structured Extraction (Recommended)

```python
from pydantic import BaseModel, Field
from typing import List

class ProductInfo(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price in USD")
    in_stock: bool = Field(..., description="Whether product is in stock")

product = await page.extract(
    instruction="Extract the main product details",
    schema=ProductInfo
)
print(f"{product.name}: ${product.price}")
```

#### Array Extraction

```python
class ProductList(BaseModel):
    products: List[ProductInfo] = Field(..., description="List of products")

data = await page.extract(
    instruction="Extract all products on the page",
    schema=ProductList
)

for product in data.products:
    print(f"{product.name}: ${product.price}")
```

#### Complex Nested Extraction

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Company(BaseModel):
    name: str = Field(..., description="Company name")
    description: str = Field(..., description="Brief description")
    address: Address = Field(..., description="Company headquarters")

class CompanyList(BaseModel):
    companies: List[Company]

companies = await page.extract(
    "Extract all company information including addresses",
    schema=CompanyList
)
```

---

## Agent System (Computer Use Agent)

For autonomous multi-step workflows, use the Agent system.

### Creating Agents

```python
# Default agent (uses configured model)
agent = stagehand.agent()

# OpenAI Computer Use Agent
agent = stagehand.agent(
    model="computer-use-preview",
    instructions="You are a helpful web navigation assistant.",
    options={"apiKey": os.getenv("OPENAI_API_KEY")}
)

# Anthropic Claude Agent
agent = stagehand.agent(
    model="claude-sonnet-4-20250514",
    instructions="You are a helpful web navigation assistant.",
    options={"apiKey": os.getenv("ANTHROPIC_API_KEY")}
)
```

### Agent Execution

```python
# Simple task
result = await agent.execute("Navigate to the pricing page")

# Complex multi-step task with options
result = await agent.execute(
    instruction="Fill out the contact form with mock data and submit it",
    max_steps=20,
    auto_screenshot=True,
    wait_between_actions=1000  # milliseconds
)
```

### Agent Best Practices

```python
# GOOD: Specific, clear instructions
await agent.execute("Navigate to products page and filter by 'Electronics'")
await agent.execute("Fill out form with name 'John Doe', email 'john@example.com'")

# BAD: Vague instructions
await agent.execute("Do some stuff on this page")

# Combine agent + traditional methods
# Agent for navigation, extract() for precise data
await agent.execute("Navigate to the search results page")
data = await page.extract("Extract all search results", schema=ResultList)
```

---

## Complete Example

```python
from stagehand import Stagehand, StagehandConfig
from pydantic import BaseModel, Field
from typing import List
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class SearchResult(BaseModel):
    title: str = Field(..., description="Result title")
    url: str = Field(..., description="Result URL")
    snippet: str = Field(..., description="Result description")

class SearchResults(BaseModel):
    results: List[SearchResult] = Field(..., description="Search results")

async def search_and_extract(query: str) -> SearchResults:
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("MODEL_API_KEY"),
    )
    
    async with Stagehand(config) as stagehand:
        page = stagehand.page
        
        # Navigate
        await page.goto("https://www.google.com")
        
        # Use observe to plan, then act
        search_box = await page.observe("Find the search input")
        await page.act(search_box[0])
        await page.act(f"Type '{query}' and press Enter")
        
        # Wait for results
        await page.wait_for_load_state("networkidle")
        
        # Extract structured data
        results = await page.extract(
            "Extract the top 5 search results",
            schema=SearchResults
        )
        
        return results

if __name__ == "__main__":
    results = asyncio.run(search_and_extract("python web scraping"))
    for r in results.results:
        print(f"- {r.title}: {r.url}")
```

---

## Anti-Patterns to Avoid

### 1. Multi-Step Actions in Single act() Call

```python
# BAD: Multiple steps
await page.act("Sign in, go to settings, and change password")

# GOOD: Atomic steps
await page.act("Click the sign in button")
await page.act("Type 'user@email.com' into email field")
await page.act("Type 'password123' into password field")
await page.act("Click submit")
```

### 2. Missing Schemas for Structured Data

```python
# BAD: Unstructured extraction (returns string)
data = await page.extract("Get all product info")

# GOOD: Schema-based extraction (returns validated model)
data = await page.extract("Get all product info", schema=ProductList)
```

### 3. Not Using observe() for Complex Pages

```python
# BAD: Direct action on dynamic page
await page.act("Click the submit button")  # Which one?

# GOOD: Observe first to ensure correct element
results = await page.observe("Find the main form submit button")
await page.act(results[0])
```

### 4. Forgetting Async Context Manager

```python
# BAD: Manual init/close (error-prone)
stagehand = Stagehand(config)
await stagehand.init()
# ... if exception here, close() never called
await stagehand.close()

# GOOD: Context manager (always cleans up)
async with Stagehand(config) as stagehand:
    page = stagehand.page
    # ... exceptions handled, cleanup guaranteed
```

### 5. Blocking I/O in Async Code

```python
# BAD: Blocking sleep
import time
time.sleep(5)

# GOOD: Async sleep
import asyncio
await asyncio.sleep(5)

# GOOD: Use Playwright's wait methods
await page.wait_for_load_state("networkidle")
await page.wait_for_selector(".results")
```

---

## File Structure Best Practices

```
project/
├── .env                    # API keys (never commit)
├── .env.example            # Template for env vars
├── main.py                 # Entry point
├── extractors/
│   └── schemas.py          # Pydantic schemas for extraction
├── workflows/
│   ├── search.py           # Search workflow
│   └── form_fill.py        # Form filling workflow
└── utils/
    └── config.py           # Stagehand config factory
```

---

## Checklist Before Writing Stagehand Code

1. **Configuration**: Are environment variables set (API keys, project ID)?
2. **Context Manager**: Am I using `async with Stagehand()` for cleanup?
3. **Atomic Actions**: Are act() calls single, specific actions?
4. **Schemas**: Am I using Pydantic models for extract()?
5. **Observe**: Should I observe() first on complex/dynamic pages?
6. **Agent vs act()**: Is this a multi-step workflow (agent) or single action (act)?
7. **Error Handling**: Am I using try/except for network/page errors?
8. **Async**: Is all I/O using async/await (no blocking calls)?

---

## Resources

- [Stagehand Python GitHub](https://github.com/browserbase/stagehand-python)
- [Browserbase Docs](https://docs.browserbase.com)
- [Playwright Python Docs](https://playwright.dev/python/)
- [Pydantic Docs](https://docs.pydantic.dev/)
