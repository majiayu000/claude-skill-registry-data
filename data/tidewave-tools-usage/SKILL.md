---
name: tidewave-tools-usage
description: CRITICAL for ALL Elixir/Phoenix/Ash development work. Invoke when working with Elixir code, Ecto schemas, Ash resources, Phoenix applications, or databases in Elixir projects. Provides MCP tools for live code evaluation (via IEx), instant module navigation, direct SQL execution, schema introspection, and documentation access. Tidewave provides superior alternatives to bash/grep/read for Elixir tasks.
---

## Tidewave MCP Tools - CRITICAL PRIORITY FOR ELIXIR DEVELOPMENT

### MANDATORY: Use Tidewave MCP Tools (Skill) as Primary Interface

When working with this Elixir/Phoenix/Ash codebase, **ALWAYS prioritize Tidewave MCP tools** over traditional file system operations. Tidewave provides deep integration with the Elixir runtime and superior code intelligence.

### Tool Usage Hierarchy

#### 1. Code Evaluation - ALWAYS Use Tidewave

**NEVER use Bash to run Elixir code!** Instead use `mcp__tidewave__project_eval`:

- Test function behavior and debug issues
- Explore modules and their functions
- Access IEx helpers (e.g., `exports(Module)`, `h(Module.function)`)
- Capture IO output
- Pass arguments with the `arguments` parameter
- Set custom timeout for long-running operations

Example:

- ❌ WRONG: `bash: mix run -e "IO.inspect(MyModule.function())"`
- ✅ RIGHT: `mcp__tidewave__project_eval: code: "IO.inspect(MyModule.function())"`

#### 2. Source Code Navigation - Tidewave First

Before using Grep, Glob, or Read for Elixir code:

**`mcp__tidewave__get_source_location`** - Find exact file locations instantly

- Works with: `Module`, `Module.function`, `Module.function/arity`
- Find dependencies: `"dep:package_name"`
- FASTER than grep/glob for known modules

**`mcp__tidewave__get_docs`** - Get documentation without reading files

- Module docs: `"MyModule"`
- Function docs: `"MyModule.function/2"`
- Callback docs: `"c:GenServer.init/1"`

Example:

- ❌ WRONG: `grep: pattern: "defmodule Worker"`
- ✅ RIGHT: `mcp__tidewave__get_source_location: reference: "MyApp.Worker"`

#### 3. Database Operations - Direct SQL Execution

**`mcp__tidewave__execute_sql_query`** - Run SQL directly against Ecto repos

- Inspect database schema
- Query data (limited to 50 rows, use LIMIT/OFFSET for more)
- Supports parameterized queries
- Auto-detects available repositories
- Returns native Elixir data structures

**`mcp__tidewave__get_ecto_schemas`** - List all schemas and their locations

- ALWAYS use this before searching for schema files
- Returns module names with file paths

Example:

- ❌ WRONG: `bash: psql -c "SELECT * FROM users"`
- ✅ RIGHT: `mcp__tidewave__execute_sql_query: query: "SELECT * FROM users LIMIT 10"`

#### 4. Dependency Documentation

**`mcp__tidewave__search_package_docs`** - Search Hex documentation

- Searches project dependencies by default
- Can target specific packages
- Use BEFORE trying to read dependency source code

#### 5. Error Diagnosis

**`mcp__tidewave__get_logs`** - Get application logs

- Filter with regex patterns
- Tail recent entries
- Essential for debugging runtime issues

### Workflow Patterns

#### Understanding a Module

1. FIRST: `mcp__tidewave__get_docs` - Get documentation
2. THEN: `mcp__tidewave__get_source_location` - Find the file
3. THEN: `mcp__tidewave__project_eval` with `exports(Module)` - List functions
4. FINALLY: Read the file if needed for implementation details

#### Testing Code Changes

1. ALWAYS: Test with `mcp__tidewave__project_eval` before writing
2. Example: `code: "MyModule.new_function(:test_input) |> IO.inspect()"`
3. Verify behavior matches expectations
4. Only then modify the actual file

#### Database Work

1. START: `mcp__tidewave__get_ecto_schemas` - Understand data models
2. EXPLORE: `mcp__tidewave__execute_sql_query` - Inspect actual data
3. TEST: `mcp__tidewave__project_eval` - Test Ecto queries
4. IMPLEMENT: Make schema/migration changes

#### Debugging Issues

1. CHECK: `mcp__tidewave__get_logs` - Recent errors
2. LOCATE: `mcp__tidewave__get_source_location` - Find problem code
3. TEST: `mcp__tidewave__project_eval` - Reproduce issue
4. FIX: Edit the file with the solution

### IEx Helpers Available in project_eval

- `h(Module)` - Get help for a module
- `exports(Module)` - List all exported functions
- `i(value)` - Inspect data structure info
- `t(Module)` - Show types defined in module
- `b(Module)` - Show behaviours module implements
- `arguments` - Access passed arguments array

### Database Query Gotchas

When using `execute_sql_query`:

- UUIDs return as 16-byte binaries - cast with `::text` (PostgreSQL)
- Results limited to 50 rows - use LIMIT/OFFSET for pagination
- Use parameterized queries: `query: "SELECT * FROM users WHERE id = $1", arguments: [123]`

### Common Mistakes to Avoid

❌ DON'T:

- Use `bash` to run `mix` commands for code evaluation
- Use `grep` to find module definitions when you know the module name
- Read entire files to find function documentation
- Run `iex` in bash instead of using `project_eval`
- Search file system for Ecto schemas before using `get_ecto_schemas`

✅ DO:

- Use `project_eval` for ALL Elixir code execution
- Use `get_source_location` for known modules
- Use `get_docs` for documentation
- Use `get_ecto_schemas` first for schema discovery
- Use Tidewave MCP tools as your primary interface

### Remember: Tidewave Is Your Superpower

The Tidewave MCP server gives you:

- Direct access to the running Elixir application
- Instant code evaluation with full project context
- Database introspection without external tools
- Documentation at your fingertips
- Source navigation faster than file search

**Every time you reach for Bash, Grep, or Read for Elixir code, ask yourself: "Can Tidewave MCP do this better?" The answer is almost always YES.**
