---
name: mcp-server-enhancement
description: Guide for safely adding new MCP tools to the AI Counsel server
when_to_use: |
  Use this skill when you need to:
  - Add a new MCP tool to server.py
  - Extend the MCP server with additional deliberation capabilities
  - Create new tool handlers with proper stdio safety
  - Ensure new tools follow MCP protocol standards
  - Add tools that interact with existing engine/storage components
tags: [mcp, protocol, server, tools, stdio]
---

# MCP Server Enhancement Skill

This skill provides a systematic approach to extending the AI Counsel MCP server (`server.py`) with new tools while maintaining protocol compliance, stdio safety, and proper error handling.

## Architecture Overview

The AI Counsel MCP server communicates via **stdio** (stdin/stdout) using the Model Context Protocol. Key architectural constraints:

- **Stdio Safety**: stdout is RESERVED for MCP protocol JSON. All logging MUST go to file (`mcp_server.log`) or stderr
- **Protocol Compliance**: Tools must follow MCP specification for request/response format
- **Type Safety**: Use Pydantic models for all request/response validation
- **Error Isolation**: Tool failures should return structured error responses, not crash the server
- **Async First**: All tool handlers are async functions using asyncio

## Current Tool Architecture

### Tool 1: `deliberate` (Primary Tool)
- **Purpose**: Multi-round AI model deliberation with consensus building
- **Handler**: `call_tool()` function (lines 242-327 in server.py)
- **Request Model**: `DeliberateRequest` (models/schema.py)
- **Response Model**: `DeliberationResult` (models/schema.py)
- **Engine**: Uses `DeliberationEngine.execute()` for orchestration

### Tool 2: `query_decisions` (Decision Graph Tool)
- **Purpose**: Search and analyze past deliberations in decision graph memory
- **Handler**: `handle_query_decisions()` function (lines 329-415 in server.py)
- **Request Schema**: Inline in `list_tools()` (lines 196-237)
- **Response**: Custom JSON structure (not a Pydantic model)
- **Conditional**: Only exposed if `config.decision_graph.enabled == True`

## Step-by-Step: Adding a New MCP Tool

### Step 1: Define Pydantic Request/Response Models

**Location**: `models/schema.py`

Create type-safe models for your tool's inputs and outputs:

```python
# In models/schema.py

class NewToolRequest(BaseModel):
    """Model for new_tool request."""

    parameter1: str = Field(
        ...,
        min_length=1,
        description="Description of parameter1"
    )
    parameter2: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Integer parameter with range validation"
    )
    optional_param: Optional[str] = Field(
        default=None,
        description="Optional parameter"
    )

class NewToolResponse(BaseModel):
    """Model for new_tool response."""

    status: Literal["success", "partial", "failed"] = Field(
        ...,
        description="Operation status"
    )
    result_data: str = Field(..., description="Main result data")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
```

**Best Practices**:
- Use `Field()` with descriptive text for all fields (helps MCP client documentation)
- Use `Literal` types for enums (status fields, modes, etc.)
- Apply validation constraints (`min_length`, `ge`, `le`) at the model level
- Provide sensible defaults for optional parameters
- Use `Optional[]` for truly optional fields

### Step 2: Add Tool Definition to `list_tools()`

**Location**: `server.py`, inside `list_tools()` function

Add your tool to the tools list returned by the MCP server:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    tools = [
        # Existing deliberate tool...
        Tool(
            name="deliberate",
            description=(...),
            inputSchema={...},
        ),

        # Your new tool
        Tool(
            name="new_tool",
            description=(
                "Clear, concise description of what this tool does. "
                "Include use cases and examples. Make it helpful for "
                "Claude Code users who will invoke this tool.\n\n"
                "Example usage:\n"
                '  {"parameter1": "example", "parameter2": 5}\n\n'
                "Expected behavior: Explain what the tool will do."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "parameter1": {
                        "type": "string",
                        "description": "Description matching your Pydantic model",
                        "minLength": 1,
                    },
                    "parameter2": {
                        "type": "integer",
                        "description": "Integer parameter",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5,
                    },
                    "optional_param": {
                        "type": "string",
                        "description": "Optional parameter",
                    },
                },
                "required": ["parameter1"],  # Only required fields
            },
        ),
    ]

    return tools
```

**Best Practices**:
- **inputSchema MUST match your Pydantic model** (field names, types, constraints)
- Use JSON Schema types: `string`, `integer`, `number`, `boolean`, `array`, `object`
- Constraints: `minLength`, `maxLength`, `minimum`, `maximum`, `minItems`, `maxItems`
- Provide examples in the description (helps Claude Code understand usage)
- Multi-line descriptions are encouraged for clarity

**Conditional Tools** (like `query_decisions`):
```python
# Add tool only if config enables it
if hasattr(config, "feature_name") and config.feature_name and config.feature_name.enabled:
    tools.append(
        Tool(name="conditional_tool", description=(...), inputSchema={...})
    )
```

### Step 3: Create Tool Handler Function

**Location**: `server.py`, typically before `main()` function

Create an async handler function for your tool's logic:

```python
async def handle_new_tool(arguments: dict) -> list[TextContent]:
    """
    Handle new_tool MCP tool call.

    Args:
        arguments: Tool arguments as dict (validated by MCP client)

    Returns:
        List of TextContent with JSON response

    Raises:
        Exception: Caught and converted to error response
    """
    try:
        # Step 1: Validate request with Pydantic
        logger.info(f"Validating new_tool request: {arguments}")
        request = NewToolRequest(**arguments)

        # Step 2: Execute your tool's logic
        logger.info(f"Processing new_tool: {request.parameter1}")

        # Example: Call engine or storage components
        # result_data = await some_engine.process(request.parameter1)
        result_data = f"Processed: {request.parameter1}"

        # Step 3: Build response model
        response_model = NewToolResponse(
            status="success",
            result_data=result_data,
            metadata={"parameter2_used": request.parameter2}
        )

        # Step 4: Serialize to JSON
        result_json = json.dumps(response_model.model_dump(), indent=2)
        logger.info(f"new_tool complete: {len(result_json)} chars")

        # Step 5: Return as TextContent
        return [TextContent(type="text", text=result_json)]

    except ValidationError as e:
        # Pydantic validation failure
        logger.error(f"Validation error in new_tool: {e}", exc_info=True)
        error_response = {
            "error": f"Invalid parameters: {str(e)}",
            "error_type": "ValidationError",
            "status": "failed",
        }
        return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    except Exception as e:
        # General error handling
        logger.error(f"Error in new_tool: {type(e).__name__}: {e}", exc_info=True)
        error_response = {
            "error": str(e),
            "error_type": type(e).__name__,
            "status": "failed",
        }
        return [TextContent(type="text", text=json.dumps(error_response, indent=2))]
```

**Best Practices**:
- Always use try-except to catch errors gracefully
- Log liberally to `mcp_server.log` (helps debugging)
- Return structured error responses (don't raise exceptions to MCP layer)
- Use Pydantic's `model_dump()` for serialization (ensures consistency)
- Separate validation errors from general errors for better diagnostics

### Step 4: Route Tool Calls in `call_tool()`

**Location**: `server.py`, inside `call_tool()` function (around line 242)

Add routing logic to dispatch your new tool:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from MCP client.

    Args:
        name: Tool name
        arguments: Tool arguments as dict

    Returns:
        List of TextContent with JSON response
    """
    logger.info(f"Tool call received: {name} with arguments: {arguments}")

    # Route to appropriate handler
    if name == "new_tool":
        return await handle_new_tool(arguments)
    elif name == "query_decisions":
        return await handle_query_decisions(arguments)
    elif name == "deliberate":
        # Inline handler for deliberate (existing code)
        try:
            request = DeliberateRequest(**arguments)
            result = await engine.execute(request)
            # ... rest of deliberate logic
        except Exception as e:
            # ... error handling
    else:
        # Unknown tool error
        error_msg = f"Unknown tool: {name}"
        logger.error(error_msg)
        raise ValueError(error_msg)
```

**Best Practices**:
- Use early returns for clarity (avoid deep nesting)
- Keep routing logic simple (just dispatch, don't implement logic here)
- Log the tool name and arguments on entry (debugging aid)
- Raise `ValueError` for unknown tools (MCP client will handle gracefully)

### Step 5: Write Tests

**Location**: Create `tests/unit/test_new_tool.py` and `tests/integration/test_new_tool_integration.py`

#### Unit Tests (Fast, No Dependencies)

```python
# tests/unit/test_new_tool.py
import pytest
from models.schema import NewToolRequest, NewToolResponse
from pydantic import ValidationError

def test_new_tool_request_validation():
    """Test NewToolRequest validates correctly."""
    # Valid request
    req = NewToolRequest(parameter1="test", parameter2=7)
    assert req.parameter1 == "test"
    assert req.parameter2 == 7

    # Invalid: parameter2 out of range
    with pytest.raises(ValidationError):
        NewToolRequest(parameter1="test", parameter2=11)

    # Invalid: missing required parameter
    with pytest.raises(ValidationError):
        NewToolRequest(parameter2=5)

def test_new_tool_response_serialization():
    """Test NewToolResponse serializes correctly."""
    resp = NewToolResponse(
        status="success",
        result_data="test result",
        metadata={"key": "value"}
    )
    data = resp.model_dump()
    assert data["status"] == "success"
    assert data["result_data"] == "test result"
    assert data["metadata"]["key"] == "value"
```

#### Integration Tests (Real Server Invocation)

```python
# tests/integration/test_new_tool_integration.py
import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from mcp.types import TextContent

# Import your handler
from server import handle_new_tool

@pytest.mark.asyncio
async def test_handle_new_tool_success():
    """Test handle_new_tool with valid input."""
    arguments = {"parameter1": "test", "parameter2": 5}

    result = await handle_new_tool(arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)

    response_data = json.loads(result[0].text)
    assert response_data["status"] == "success"
    assert "test" in response_data["result_data"]

@pytest.mark.asyncio
async def test_handle_new_tool_validation_error():
    """Test handle_new_tool with invalid input."""
    arguments = {"parameter2": 5}  # Missing required parameter1

    result = await handle_new_tool(arguments)

    assert len(result) == 1
    response_data = json.loads(result[0].text)
    assert response_data["status"] == "failed"
    assert response_data["error_type"] == "ValidationError"
```

**Testing Best Practices**:
- Test validation (valid inputs, invalid inputs, edge cases)
- Test error handling (validation errors, runtime errors)
- Test serialization (model_dump() produces correct JSON)
- Mock external dependencies (engines, storage, API calls)
- Use `pytest.mark.asyncio` for async tests

### Step 6: Update Documentation

**Location**: `CLAUDE.md`

Add your new tool to the architecture documentation:

```markdown
## Architecture

### Core Components

**MCP Server Layer** (`server.py`)
- Entry point for MCP protocol communication via stdio
- Exposes tools: `deliberate`, `query_decisions`, `new_tool` (NEW)
- Tool: `new_tool` - [Brief description of what it does]
```

Update the data flow section if your tool has unique flow characteristics.

## Critical Rules: Stdio Safety

**WHY THIS MATTERS**: The MCP server uses stdout for protocol communication. Any writes to stdout that aren't MCP protocol JSON will corrupt the communication channel and crash the server.

### Rules

1. **NEVER print() to stdout**
   - Bad: `print("Debug message")`
   - Good: `logger.info("Debug message")`

2. **NEVER write to sys.stdout**
   - Bad: `sys.stdout.write("output")`
   - Good: `sys.stderr.write("output")` or use logger

3. **Configure logging to file/stderr ONLY**
   ```python
   logging.basicConfig(
       handlers=[
           logging.FileHandler("mcp_server.log"),
           logging.StreamHandler(sys.stderr),  # NOT sys.stdout!
       ]
   )
   ```

4. **Return MCP responses via TextContent**
   - Good: `return [TextContent(type="text", text=json.dumps(response))]`
   - This is the ONLY correct way to send data to MCP client

5. **Suppress subprocess stdout if not needed**
   ```python
   # If invoking external processes in your tool
   result = subprocess.run(
       ["command"],
       stdout=subprocess.PIPE,  # Capture, don't print
       stderr=subprocess.PIPE
   )
   ```

### Testing Stdio Safety

Run your tool through the MCP client and verify:
- No garbled output in Claude Code
- Server log shows clean execution
- No "protocol error" messages from MCP client

## Error Handling Patterns

### Pattern 1: Pydantic Validation Errors

```python
try:
    request = NewToolRequest(**arguments)
except ValidationError as e:
    logger.error(f"Validation error: {e}", exc_info=True)
    return [TextContent(type="text", text=json.dumps({
        "error": f"Invalid parameters: {str(e)}",
        "error_type": "ValidationError",
        "status": "failed",
    }, indent=2))]
```

### Pattern 2: Runtime Errors

```python
try:
    result = await some_operation()
except SomeSpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    return [TextContent(type="text", text=json.dumps({
        "error": str(e),
        "error_type": type(e).__name__,
        "status": "failed",
    }, indent=2))]
```

### Pattern 3: Graceful Degradation

```python
# If optional feature unavailable, return partial result
try:
    enhanced_data = await optional_enhancement()
except Exception as e:
    logger.warning(f"Enhancement failed, using base data: {e}")
    enhanced_data = None

return [TextContent(type="text", text=json.dumps({
    "status": "success" if enhanced_data else "partial",
    "result": base_data,
    "enhanced": enhanced_data,
}, indent=2))]
```

### Pattern 4: Conditional Tool Availability

```python
# In handle_new_tool()
if not hasattr(config, "feature") or not config.feature.enabled:
    return [TextContent(type="text", text=json.dumps({
        "error": "Feature not enabled in config.yaml",
        "error_type": "ConfigurationError",
        "status": "failed",
    }, indent=2))]
```

## Integration with Existing Components

### Using DeliberationEngine

If your tool needs to trigger deliberations:

```python
from deliberation.engine import DeliberationEngine

async def handle_new_tool(arguments: dict) -> list[TextContent]:
    # Access global engine (initialized in server.py)
    request = DeliberateRequest(
        question="Generated question",
        participants=[...],
        rounds=2
    )
    result = await engine.execute(request)
    # Process result...
```

### Using DecisionGraphStorage

If your tool needs to query decision graph:

```python
from decision_graph.storage import DecisionGraphStorage
from pathlib import Path

async def handle_new_tool(arguments: dict) -> list[TextContent]:
    db_path = Path(config.decision_graph.db_path)
    if not db_path.is_absolute():
        db_path = PROJECT_DIR / db_path

    storage = DecisionGraphStorage(str(db_path))
    decisions = storage.get_all_decisions(limit=10)
    # Process decisions...
```

### Using QueryEngine

If your tool needs advanced decision graph queries:

```python
from deliberation.query_engine import QueryEngine

async def handle_new_tool(arguments: dict) -> list[TextContent]:
    engine = QueryEngine(storage)
    results = await engine.search_similar(query_text, limit=5)
    # Process results...
```

## Configuration for New Tools

If your tool needs configuration, add to `models/config.py` and `config.yaml`:

### In `models/config.py`:

```python
class NewToolConfig(BaseModel):
    """Configuration for new_tool."""
    enabled: bool = Field(default=False, description="Enable new_tool feature")
    parameter: str = Field(default="default", description="Tool-specific parameter")
    timeout: int = Field(default=60, description="Timeout in seconds")

class Config(BaseModel):
    # ... existing config ...
    new_tool: Optional[NewToolConfig] = None
```

### In `config.yaml`:

```yaml
new_tool:
  enabled: true
  parameter: "custom_value"
  timeout: 120
```

### Accessing config in handler:

```python
async def handle_new_tool(arguments: dict) -> list[TextContent]:
    if not hasattr(config, "new_tool") or not config.new_tool.enabled:
        return error_response("new_tool not enabled")

    timeout = config.new_tool.timeout
    # Use config...
```

## Testing Your New Tool End-to-End

### 1. Manual Testing via MCP Inspector

Use the MCP Inspector tool to test your tool directly:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
mcp-inspector python /path/to/server.py
```

Invoke your tool with test inputs and verify responses.

### 2. Integration with Claude Code

Add your server to `~/.claude/config/mcp.json`:

```json
{
  "mcpServers": {
    "ai-counsel": {
      "command": "python",
      "args": ["/path/to/ai-counsel/server.py"],
      "env": {}
    }
  }
}
```

Test in Claude Code:
1. Start a conversation
2. Claude Code should auto-discover your tool
3. Trigger your tool with a query that would use it
4. Verify the response is correct

### 3. Check Logs

Always check `mcp_server.log` after testing:

```bash
tail -f /path/to/ai-counsel/mcp_server.log
```

Look for:
- Tool invocation logs
- Validation successes/failures
- Error stack traces (if any)
- Performance timings

## Common Pitfalls

### Pitfall 1: inputSchema Mismatch with Pydantic Model

**Problem**: JSON Schema in `list_tools()` doesn't match Pydantic model fields.

**Symptom**: MCP client accepts invalid inputs, or rejects valid inputs.

**Solution**: Keep schemas in sync. Consider generating JSON Schema from Pydantic:

```python
from pydantic.json_schema import JsonSchemaValue

schema = NewToolRequest.model_json_schema()
# Use this schema in inputSchema (but manually clean up for MCP if needed)
```

### Pitfall 2: Forgetting to Route in `call_tool()`

**Problem**: Tool defined in `list_tools()` but not handled in `call_tool()`.

**Symptom**: MCP client can invoke tool, but server returns "Unknown tool" error.

**Solution**: Always add routing in `call_tool()` after defining tool.

### Pitfall 3: Blocking Operations in Handler

**Problem**: Tool handler does CPU-intensive or I/O-blocking work synchronously.

**Symptom**: Server becomes unresponsive, other tools timeout.

**Solution**: Use async operations or run blocking work in executor:

```python
import asyncio

async def handle_new_tool(arguments: dict) -> list[TextContent]:
    # For CPU-bound work
    result = await asyncio.to_thread(blocking_function, arg1, arg2)

    # For I/O-bound work
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")

    # Process result...
```

### Pitfall 4: Not Testing Error Cases

**Problem**: Only testing happy path, not validation failures or edge cases.

**Symptom**: Tool crashes or returns unclear errors when given bad input.

**Solution**: Write tests for every error scenario:

```python
@pytest.mark.asyncio
async def test_handle_new_tool_errors():
    # Missing required field
    result = await handle_new_tool({})
    assert "ValidationError" in result[0].text

    # Invalid value range
    result = await handle_new_tool({"parameter1": "test", "parameter2": 999})
    assert "failed" in result[0].text
```

## Checklist for Adding a New Tool

Use this checklist to ensure you've completed all steps:

- [ ] Define Pydantic request model in `models/schema.py`
- [ ] Define Pydantic response model in `models/schema.py`
- [ ] Add tool definition to `list_tools()` in `server.py`
- [ ] Ensure inputSchema matches Pydantic model exactly
- [ ] Create async handler function in `server.py`
- [ ] Add error handling (ValidationError + general exceptions)
- [ ] Add routing logic in `call_tool()`
- [ ] Write unit tests for models and validation
- [ ] Write integration tests for handler function
- [ ] Test stdio safety (no stdout contamination)
- [ ] Update `CLAUDE.md` architecture section
- [ ] Add configuration to `models/config.py` if needed
- [ ] Update `config.yaml` with default config if needed
- [ ] Test end-to-end with MCP Inspector
- [ ] Test integration with Claude Code
- [ ] Review logs for errors and performance
- [ ] Document any new dependencies in `requirements.txt`

## References

- **MCP Protocol Specification**: https://spec.modelcontextprotocol.io/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **AI Counsel Architecture**: `CLAUDE.md` in repository root
- **Existing Tool Implementations**: `server.py` lines 104-416

## Examples in Codebase

Study these existing implementations as reference:

1. **Simple tool with inline handler**: `deliberate` tool (lines 242-327 in server.py)
   - Shows: Pydantic validation, engine invocation, response truncation, error handling

2. **Separate handler function**: `query_decisions` tool (lines 329-415 in server.py)
   - Shows: Handler separation, conditional tool availability, storage integration

3. **Conditional tool**: Decision graph tools (lines 196-237 in server.py)
   - Shows: How to conditionally expose tools based on config

## Getting Help

If you encounter issues:

1. Check `mcp_server.log` for detailed error traces
2. Verify stdio safety (no stdout writes)
3. Test Pydantic models in isolation first
4. Use MCP Inspector for manual testing before integration
5. Review existing tool implementations for patterns
6. Ensure all dependencies are installed (`requirements.txt`)

---

**Remember**: Stdio safety is paramount. When in doubt, log to file/stderr, NEVER stdout.
