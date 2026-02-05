---
name: create-extension
description: Creates a new Starlark MCP extension with tools, handlers, and proper structure. Use when the user wants to add a new extension to the starlark-mcp server.
---

# Create Extension

Creates a new Starlark-based MCP extension for the starlark-mcp server.

## Instructions

When the user requests a new extension:

1. **Gather Requirements**
   - Ask the user for the extension name (lowercase with underscores)
   - Ask what tools/capabilities the extension should provide
   - Determine if the extension needs:
     - External API access (HTTP calls)
     - Database access (SQLite, PostgreSQL)
     - File system operations
     - System commands (via `exec.run()`)

2. **Choose Implementation Approach**
   - **IMPORTANT: Default to using existing Starlark modules first**
   - Use `exec.run()` for CLI tools (docker, git, kubectl, etc.) - this is almost always the right choice
   - Use `http` module for REST APIs
   - Use existing `sqlite` or `postgres` modules for databases
   - **Only create new Rust modules if:**
     - The CLI tool doesn't exist or lacks JSON output
     - You need direct library access for performance
     - The existing modules don't provide required functionality
   - Remember: `exec.run()` is simple, fast to implement, and what users already have installed

3. **Create Extension File**
   - Create `extensions/{name}.star` file
   - Follow the standard Starlark MCP extension structure

4. **Extension Structure**

   ```python
   # Tool handler functions
   def tool_name(params):
       """Tool description"""
       # Extract parameters
       param = params.get("param_name", "default")

       # Validate inputs
       if not param:
           return error_response("param_name is required")

       # Implement logic
       result = do_something(param)

       # Return MCP response
       return {
           "content": [{"type": "text", "text": result}],
       }

   # Helper functions
   def error_response(message):
       """Create an error response"""
       return {
           "content": [{"type": "text", "text": "Error: " + message}],
           "isError": True,
       }

   # Extension definition
   def describe_extension():
       """Define the extension"""
       return Extension(
           name = "extension_name",
           version = "1.0.0",
           description = "Extension description",
           tools = [
               Tool(
                   name = "tool_name",
                   description = "Tool description",
                   parameters = [
                       ToolParameter(
                           name = "param_name",
                           param_type = "string",
                           required = True,
                           description = "Parameter description",
                       ),
                   ],
                   handler = tool_name,
               ),
           ],
       )
   ```

5. **Available Starlark Modules**
   The following modules are available in extension code:

   - `exec` - **Start here for most CLI tools!** Run system commands (`exec.run("command", ["arg1", "arg2"])`)
     - Returns: `{"success": bool, "stdout": string, "stderr": string, "exit_code": int}`
     - Perfect for: docker, git, kubectl, aws cli, etc.
     - Most CLIs support `--format json` or similar for easy parsing
   - `http` - Make HTTP requests (`http.get()`, `http.post()`, etc.)
   - `sqlite` - SQLite database operations (`sqlite.query()`, `sqlite.list_tables()`, `sqlite.describe_table()`)
   - `postgres` - PostgreSQL operations (`postgres.query()`, `postgres.execute()`, `postgres.list_tables()`, `postgres.describe_table()`)
   - `env` - Access environment variables (`env.get("VAR_NAME", "default")`)
   - `time` - Time utilities (`time.now()` for Unix timestamp)
   - `json` - JSON encoding/decoding (`json.encode()`, `json.decode()`)

6. **Parameter Types**
   Supported `param_type` values:
   - `"string"` - Text values
   - `"integer"` - Whole numbers
   - `"number"` - Decimal numbers
   - `"boolean"` - true/false
   - `"array"` - Lists
   - `"object"` - Dictionaries

7. **Security Considerations**
   - Validate all user inputs
   - Sanitize parameters used in SQL queries or system commands
   - Use parameterized queries for database operations
   - Restrict file system access when possible
   - Declare `allowed_exec` in Extension() for system commands

8. **Test the Extension**
   - Build the project: `cargo build --release`
   - Test with a simple MCP call:

     ```bash
     echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"tool_name","arguments":{}}}' | ./target/release/starlark-mcp
     ```

9. **Create Test Script** (optional)
   - Create `scripts/test_{extension_name}.sh` for testing the extension
   - Make it executable: `chmod +x scripts/test_{extension_name}.sh`

## Examples

### Extension Using CLI Tool (Docker Example)

```python
def list_containers(params):
    """List Docker containers"""
    all_containers = params.get("all", False)

    # Build docker command
    args = ["ps", "--format", "json", "--no-trunc"]
    if all_containers:
        args.append("--all")

    # Run docker CLI
    result = exec.run("docker", args)

    if not result["success"]:
        return error_response("Docker command failed: {}".format(result["stderr"]))

    # Parse JSON output (docker outputs one JSON object per line)
    containers = []
    for line in result["stdout"].strip().split("\n"):
        if line:
            container = json.decode(line)
            containers.append(container)

    output = "Found {} container(s):\n\n".format(len(containers))
    for c in containers:
        output += "- {} ({}): {}\n".format(
            c.get("Names", ""),
            c.get("ID", "")[:12],
            c.get("State", ""),
        )

    return {"content": [{"type": "text", "text": output}]}

def error_response(message):
    return {
        "content": [{"type": "text", "text": "Error: " + message}],
        "isError": True,
    }

def describe_extension():
    return Extension(
        name = "docker",
        version = "1.0.0",
        description = "Docker container management",
        allowed_exec = ["docker"],  # Must declare allowed commands
        tools = [
            Tool(
                name = "docker_list_containers",
                description = "List Docker containers",
                parameters = [
                    ToolParameter(
                        name = "all",
                        param_type = "boolean",
                        required = False,
                        default = "false",
                        description = "Include stopped containers",
                    ),
                ],
                handler = list_containers,
            ),
        ],
    )
```

### Simple Extension (No External Dependencies)

```python
def greet(params):
    """Greet a user"""
    name = params.get("name", "World")
    return {
        "content": [{"type": "text", "text": "Hello, {}!".format(name)}],
    }

def describe_extension():
    return Extension(
        name = "greeter",
        version = "1.0.0",
        description = "Simple greeting extension",
        tools = [
            Tool(
                name = "greet",
                description = "Greet a user by name",
                parameters = [
                    ToolParameter(
                        name = "name",
                        param_type = "string",
                        required = False,
                        default = "World",
                        description = "Name to greet",
                    ),
                ],
                handler = greet,
            ),
        ],
    )
```

### Extension with HTTP Access

```python
def fetch_data(params):
    """Fetch data from an API"""
    url = params.get("url", "")

    if not url:
        return error_response("url parameter is required")

    response = http.get(url, {})

    if response["status_code"] != 200:
        return error_response("HTTP request failed: {}".format(response["status_code"]))

    return {
        "content": [{"type": "text", "text": response["body"]}],
    }

def error_response(message):
    return {
        "content": [{"type": "text", "text": "Error: " + message}],
        "isError": True,
    }

def describe_extension():
    return Extension(
        name = "http_fetcher",
        version = "1.0.0",
        description = "Fetch data from HTTP endpoints",
        tools = [
            Tool(
                name = "fetch_data",
                description = "Fetch data from a URL",
                parameters = [
                    ToolParameter(
                        name = "url",
                        param_type = "string",
                        required = True,
                        description = "URL to fetch",
                    ),
                ],
                handler = fetch_data,
            ),
        ],
    )
```

### Extension with Database Access

```python
def query_db(params):
    """Query a SQLite database"""
    db_path = params.get("db_path", "")
    query = params.get("query", "")

    if not db_path or not query:
        return error_response("db_path and query are required")

    # Security: Only allow SELECT
    if not query.strip().upper().startswith("SELECT"):
        return error_response("Only SELECT queries allowed")

    rows = sqlite.query(db_path, query, [])

    output = "Found {} row(s):\n\n{}".format(len(rows), json.encode(rows))

    return {
        "content": [{"type": "text", "text": output}],
    }

def error_response(message):
    return {
        "content": [{"type": "text", "text": "Error: " + message}],
        "isError": True,
    }

def describe_extension():
    return Extension(
        name = "db_query",
        version = "1.0.0",
        description = "Query SQLite databases",
        tools = [
            Tool(
                name = "query_db",
                description = "Execute a SELECT query on a SQLite database",
                parameters = [
                    ToolParameter(
                        name = "db_path",
                        param_type = "string",
                        required = True,
                        description = "Path to SQLite database",
                    ),
                    ToolParameter(
                        name = "query",
                        param_type = "string",
                        required = True,
                        description = "SELECT query to execute",
                    ),
                ],
                handler = query_db,
            ),
        ],
    )
```

## Reference Files

See existing extensions for more examples:

- `extensions/cat_facts.star` - Simple extension with no dependencies
- `extensions/sqlite.star` - Database access with multiple tools
- `extensions/postgres.star` - PostgreSQL with environment configuration
- `extensions/plane.star` - API integration with authentication
- `extensions/github.star` - GitHub API integration

## Notes

- Extension names should be lowercase with underscores
- Tool names are prefixed with extension name (e.g., `sqlite_query`)
- All handlers must return a dict with `content` array
- Use `error_response()` helper for consistent error handling
- Test thoroughly before committing
