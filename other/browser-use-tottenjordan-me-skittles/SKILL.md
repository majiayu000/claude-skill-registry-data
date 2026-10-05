---
name: browser-use
description: AI-powered browser automation using the browser-use Python library. Use when the user requests web automation tasks including web scraping and data extraction, form filling and submission, automated testing and validation, web navigation and interaction, or any task requiring programmatic browser control. Supports natural language task descriptions that are executed by AI agents.
---

# Browser-Use Automation

AI-powered browser automation that executes web tasks from natural language descriptions using the browser-use Python library.

## Quick Start

Browser-use enables browser automation through natural language task descriptions:

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def automate():
    browser = Browser()
    llm = ChatBrowserUse()

    agent = Agent(
        task="Go to github.com/browser-use/browser-use and find the star count",
        llm=llm,
        browser=browser,
    )

    result = await agent.run()
    await browser.close()
    return result

asyncio.run(automate())
```

## Installation

Before using browser-use, ensure it's installed. Check and install automatically:

```bash
python scripts/check_install.py
```

Or install manually:

```bash
pip install browser-use
```

## Core Workflow

### 1. Understand the Task

Identify what the user wants to accomplish:
- **Data extraction**: Scraping content, collecting information
- **Form automation**: Filling forms, submitting data
- **Testing**: Verifying functionality, checking elements
- **Navigation**: Multi-step processes, conditional flows

### 2. Write the Task Description

Translate the user's request into a clear, specific task description for the AI agent. Be explicit about:
- Target URL or starting point
- Specific actions to take
- Data to extract or input
- Expected outcome

**Good example**: "Go to example.com/products, filter by category 'Electronics', and extract the name and price of the first 10 products"

**Avoid**: "Get product data" (too vague)

### 3. Create the Automation Script

Use the basic pattern from `scripts/basic_automation.py`:

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def run_task(task_description: str):
    browser = Browser()
    llm = ChatBrowserUse()

    agent = Agent(
        task=task_description,
        llm=llm,
        browser=browser,
    )

    try:
        result = await agent.run()
        return result
    finally:
        await browser.close()

# Run it
result = asyncio.run(run_task("Your task here"))
```

### 4. Execute and Iterate

Run the script and adjust the task description if needed for better results.

## Common Task Patterns

### Web Scraping

Extract data from websites:

```python
task = "Go to news.ycombinator.com and extract the titles of the top 10 stories"
```

### Form Filling

Automate form submission:

```python
task = """
Go to example.com/contact-us
Fill out the form with:
- Name: John Doe
- Email: john@example.com
- Message: I'm interested in your services
Then click Submit
"""
```

### Multi-Step Navigation

Handle complex workflows:

```python
task = """
1. Go to example.com
2. Click on 'Products' in the navigation
3. Filter by price range $50-$100
4. Sort by 'Most Popular'
5. Click on the first product and get its description
"""
```

### Conditional Logic

Handle dynamic scenarios:

```python
task = """
Go to example.com/dashboard
If prompted to log in, use username 'user@example.com' and password 'secure123'
Once logged in, navigate to Settings and export data
"""
```

## Advanced Features

### Headless Mode

Run browser without UI for faster execution:

```python
browser = Browser(headless=True)
```

### Stealth Mode

Avoid detection for sensitive scraping:

```python
browser = Browser(stealth=True)
```

### Custom Tools

Extend agent capabilities with custom functions:

```python
from browser_use import Controller

@Controller.action("Save to file")
def save_data(content: str, filename: str):
    with open(filename, 'w') as f:
        f.write(content)
    return f"Saved to {filename}"

controller = Controller()
agent = Agent(task="...", llm=llm, browser=browser, controller=controller)
```

### Cloud Browsers

Use cloud-hosted browsers:

```python
browser = Browser(cloud=True, cloud_provider="browserbase")
```

## Detailed Patterns

For comprehensive examples including data extraction patterns, form automation, navigation strategies, and error handling, see:

**[references/common_patterns.md](references/common_patterns.md)**

Load this file when you need detailed code examples or are implementing complex automation workflows.

## Best Practices

1. **Be specific in task descriptions** - The more detailed, the better the AI performs
2. **Use headless mode by default** - Faster and more resource-efficient
3. **Always close browsers** - Use try/finally blocks to ensure cleanup
4. **Handle errors gracefully** - Wrap automation in try/except blocks
5. **Test incrementally** - Start with simple tasks and add complexity
6. **Reuse browser instances** - For multiple related tasks, keep browser open between operations

## Troubleshooting

**Task not completing correctly**:
- Make task description more specific
- Break complex tasks into smaller steps
- Check if website requires authentication

**Installation issues**:
- Run `scripts/check_install.py` to verify installation
- Ensure Python 3.8+ is installed
- Check for dependency conflicts

**Browser crashes or hangs**:
- Use headless mode to reduce resource usage
- Ensure sufficient system memory
- Check for website anti-bot measures
