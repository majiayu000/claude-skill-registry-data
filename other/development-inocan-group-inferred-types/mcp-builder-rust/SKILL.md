---
name: mcp-builder-rust
description: Guide for creating high-quality MCP (Model Context Protocol) servers in Rust using rmcp SDK. Use when building production-grade MCP servers with type safety, performance, and async support.
license: MIT
---

# Rust MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers in Rust that enable LLMs to interact with external services through well-designed tools. Rust provides type safety, memory safety, and high performance for production-grade MCP servers.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality Rust MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps. Use Rust's type system and Result types to ensure comprehensive error handling.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: Rust (type safety, memory safety, high performance, async/await support)
- **SDK**: rmcp (official Rust MCP SDK with tokio async runtime)
- **Transport**: **stdio (standard input/output) - DEFAULT**
  - Use stdio for local development, testing, and simple integrations
  - Only use HTTP (Streamable HTTP) when remote access or multi-client support is required
  - See [Transport Options](./reference/rust_mcp_server.md#transport-options) for detailed comparison

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines
- **rmcp SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/rust-sdk/main/README.md`
- [⚡ Rust Implementation Guide](./reference/rust_mcp_server.md) - Rust patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search and WebFetch as needed.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

**Important: Unless specifically required, implement your server with stdio transport** (standard input/output). This is the default and recommended approach for:
- Local development and testing
- IDE integrations
- Desktop application integrations
- Command-line tools

Only use HTTP transport when you need remote access or multi-client support. See [Advanced Features - HTTP Transport](./reference/rust_mcp_server.md#http-transport-streamable-http) if needed.

#### 2.1 Set Up Project Structure

See Rust-specific guide for project setup:
- [⚡ Rust Implementation Guide](./reference/rust_mcp_server.md) - Project structure, Cargo.toml, dependencies

Basic project structure:
```
my-mcp-server/
├── Cargo.toml
├── src/
│   ├── main.rs          # Server entry point
│   ├── lib.rs           # Library root
│   ├── server.rs        # Server implementation
│   ├── tools/           # Tool implementations
│   │   └── mod.rs
│   └── error.rs         # Error handling
└── README.md
```

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication (using `reqwest` or `hyper`)
- Error handling with `thiserror` or `anyhow`
- Response formatting (JSON/Markdown)
- Pagination support
- Async/await with tokio runtime

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use `serde` for serialization/deserialization
- Use `schemars` for JSON Schema generation
- Include constraints and clear descriptions in doc comments
- Add examples in field documentation

**Output Schema:**
- Define output types with `serde::Serialize`
- Use structured data types for tool results
- Leverage Rust's type system for compile-time guarantees

**Tool Description:**
- Concise summary of functionality (use Rust doc comments)
- Parameter descriptions with doc attributes
- Return type schema

**Implementation:**
- Use `async fn` for I/O operations
- Proper error handling with `Result<T, E>`
- Support pagination where applicable
- Return structured data with type safety

**Tool Macros:**
Use rmcp's `#[tool]` macro for automatic tool registration:
```rust
#[tool(description = "Create a new issue")]
async fn create_issue(
    &self,
    Parameters(params): Parameters<CreateIssueParams>
) -> Result<CallToolResult, McpError> {
    // Implementation
}
```

**Annotations:**
- `readOnlyHint`: true/false (for read-only operations)
- `destructiveHint`: true/false (for destructive operations)
- `idempotentHint`: true/false (for idempotent operations)
- `openWorldHint`: true/false (for open-world assumptions)

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling with Result types
- Full type coverage (no `any` equivalent)
- Clear tool descriptions with doc comments
- Proper async/await usage
- Memory safety (leverage Rust's ownership system)

#### 3.2 Build and Test

**Rust:**
- Run `cargo build` to verify compilation
- Run `cargo test` for unit tests
- Run `cargo clippy` for lints
- Run `cargo fmt` for formatting
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

See Rust-specific guide for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Evaluation guidelines apply the same way as for other MCP implementations.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

Follow the same evaluation process as documented in the main MCP builder guide.

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines

### SDK Documentation (Load During Phase 1/2)
- **rmcp SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/rust-sdk/main/README.md`
- **rmcp crates documentation**: https://docs.rs/rmcp/latest/rmcp/

### Language-Specific Implementation Guide (Load During Phase 2)
- [⚡ Rust Implementation Guide](./reference/rust_mcp_server.md) - Complete Rust/rmcp guide with:
  - Server initialization patterns
  - Serde model examples
  - Tool registration with `#[tool]` macro
  - Complete working examples
  - Quality checklist
  - Async/await patterns
  - Error handling strategies

- [🔧 rmcp-macros Guide](./reference/rmcp_macros.md) - Comprehensive macro reference:
  - Tool macros (#[tool], #[tool_router], #[tool_handler])
  - Prompt macros (#[prompt], #[prompt_router], #[prompt_handler])
  - Advanced patterns (combining routers, state management)
  - Complete macro examples
  - Best practices for macro usage

- [🔌 Rust MCP Client Guide](./reference/rust_mcp_client.md) - Complete MCP client implementation:
  - Client architecture and basic structure
  - Transport options (stdio and HTTP)
  - Basic operations (listing tools, calling tools, reading resources, getting prompts)
  - Advanced features (sampling handlers, progress notifications, multiple client management)
  - Error handling patterns
  - Complete working examples

### Example Code (Load as Reference)
- Server examples: [examples/basic_server/](./examples/basic_server/), [examples/macros_demo_server/](./examples/macros_demo_server/), etc.
- Client examples: [examples/client_demo/](./examples/client_demo/)
- Reference: `reference/rust-sdk/examples/` in your workspace

---

## Key Differences from TypeScript/Python

### Type Safety
- Rust's type system catches errors at compile time
- No runtime type errors for properly typed code
- Use `Result<T, E>` for error handling (no exceptions)

### Memory Safety
- Ownership and borrowing prevent memory bugs
- No garbage collection overhead
- Zero-cost abstractions

### Performance
- Native compilation for optimal performance
- Async/await with tokio for high concurrency
- Minimal runtime overhead

### Tooling
- `cargo` for dependency management and builds
- `rustfmt` for automatic code formatting
- `clippy` for lints and best practices
- Strong LSP support in editors

---

## Getting Started

1. Load the [Rust Implementation Guide](./reference/rust_mcp_server.md)
2. Review the server examples:
   - **[Basic Server (stdio)](./examples/basic_server/)** - Start here! Default stdio transport
   - **[Macros Demo Server](./examples/macros_demo_server/)** - Complete rmcp-macros showcase (tools + prompts)
   - **[HTTP Server](./examples/http_server/)** - For production/remote access (advanced)
   - **[Elicitation Server](./examples/elicitation_server/)** - Interactive user input collection (advanced)
   - **[Progress Server](./examples/progress_server/)** - Real-time progress updates (advanced)
   - **[Sampling Server](./examples/sampling_server/)** - LLM sampling capabilities (advanced)
3. Review the client examples in **[Client Demo](./examples/client_demo/)**:
   - **Tool Client** - Connecting to servers and calling tools
   - **Resource Reader** - Reading server resources via HTTP
   - **Prompt Consumer** - Retrieving and using prompts
4. Study rmcp SDK documentation, [rmcp-macros Guide](./reference/rmcp_macros.md), and [Rust MCP Client Guide](./reference/rust_mcp_client.md)
5. Follow the four-phase workflow above
6. Test your server with MCP Inspector

**Remember: Start with stdio transport** unless you have a specific need for HTTP (remote access, multi-client support).

---

## Additional Resources

- rmcp GitHub: https://github.com/modelcontextprotocol/rust-sdk
- rmcp crates.io: https://crates.io/crates/rmcp
- MCP Specification: https://modelcontextprotocol.io/
- Rust Book: https://doc.rust-lang.org/book/
- Tokio Guide: https://tokio.rs/tokio/tutorial
