---
name: open-commerce
description: Open Commerce MCP and AI operations context
---

# Open Commerce Domain Context

## What Is Open Commerce?

Open Commerce enables **AI-powered commerce operations** through the Model Context Protocol (MCP). It allows AI agents to interact with Violet's commerce capabilities using natural language.

## Core Capabilities

### MCP Server
- Natural language product search
- Order creation and management
- Cart operations
- Customer lookup

### AI Operations
- Conversational commerce
- Automated order processing
- Intelligent product recommendations
- Customer service automation

## MCP Tools

| Tool | Purpose |
|------|---------|
| `search_products` | Find products by natural language query |
| `get_product` | Get detailed product information |
| `create_cart` | Start a new shopping cart |
| `add_to_cart` | Add products to cart |
| `checkout` | Complete purchase |
| `get_order` | Retrieve order details |
| `track_order` | Get fulfillment status |

## Example Usage

```python
from mcp import Server

server = Server("violet-commerce")

@server.tool()
async def search_products(query: str, limit: int = 10) -> list:
    """Search for products in the Violet catalog."""
    # Implementation
    pass

@server.tool()
async def create_order(
    customer_email: str,
    items: list[dict],
    shipping_address: dict
) -> dict:
    """Create a new order with the specified items."""
    # Implementation
    pass
```

## Integration Points

- **Violet API**: Core commerce operations
- **AI Agents**: Claude, GPT, custom agents
- **Chat Platforms**: Slack, Discord, custom
- **Voice Assistants**: Natural language interfaces

## Key Patterns

### Stateless Operations
Each MCP call is independent - no session state between calls.

### Authentication
- API key authentication
- Scoped permissions per tool
- Rate limiting per key

### Error Handling
- Clear error messages for AI agents
- Retry guidance in responses
- Graceful degradation
