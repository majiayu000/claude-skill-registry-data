---
name: create-builtin-tool
description: Guide for creating builtin MCP tools in LibrAgent. Use when creating a new builtin MCP server, adding tools to existing builtin servers, refactoring tool implementations to follow best practices, or auditing tool compliance with the Tool Design Manifesto v2.1.
---

# Create Builtin MCP Tool Skill

## When to Use This Skill

Use this skill when:

- Creating a new builtin MCP server for LibrAgent
- Adding tools to existing builtin servers
- Refactoring tool implementations to follow best practices
- Auditing tool compliance with the Tool Design Manifesto v2.1

**Prerequisites:** Understanding of Rust async/await, Tauri backend architecture, and MCP protocol basics.

---

## Architecture Overview

### 3-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  React Frontend (src/lib/backend/, src/features/)       │
│  - TypeScript API wrappers (builtin-tools.ts)           │
│  - UI components (BuiltInToolsEditor.tsx)               │
└────────────────┬────────────────────────────────────────┘
                 │ Tauri Commands (invoke)
┌────────────────▼────────────────────────────────────────┐
│  Proxy Layer (src-tauri/src/mcp/service_proxy_manager/) │
│  - MCPServiceProxyManager (session routing)             │
│  - MCPServiceProxy (per-session instances)              │
└────────────────┬────────────────────────────────────────┘
                 │ BuiltinMCPServer trait
┌────────────────▼────────────────────────────────────────┐
│  Rust Backend (src-tauri/src/mcp/builtin/)              │
│  - Tool definitions (tools/*.rs)                        │
│  - Tool handlers (handlers/*.rs, mod.rs)                │
│  - Business logic (*.rs modules)                        │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation Guide

### Step 1: Create Server Module Structure

```bash
src-tauri/src/mcp/builtin/
└── your_server/
    ├── mod.rs              # Server struct + BuiltinMCPServer impl
    ├── tools.rs            # Tool schema definitions
    ├── handlers.rs         # Tool execution handlers
    └── types.rs            # Domain-specific types (optional)
```

### Step 2: Define the Server Struct

**File:** `src-tauri/src/mcp/builtin/your_server/mod.rs`

```rust
use async_trait::async_trait;
use serde_json::{json, Value};
use std::sync::Arc;

use super::BuiltinMCPServer;
use crate::mcp::types::{MCPResult, ServiceContext};
use crate::mcp::MCPTool;

pub mod handlers;
pub mod tools;

/// Your server description
/// Explain its purpose and capabilities
#[derive(Debug)]
pub struct YourServer {
    pub(crate) session_id: String,
    // Add dependencies (e.g., database, managers)
    // Example: db: Arc<DatabaseConnection>,
}

impl YourServer {
    pub fn new(session_id: String /* , dependencies */) -> Self {
        Self {
            session_id,
            // Initialize dependencies
        }
    }

    /// Static tool definitions (called during registry initialization)
    pub fn tools_static() -> Vec<MCPTool> {
        vec![
            tools::create_your_tool(),
            // Add more tools
        ]
    }

    /// Static metadata for UI
    pub fn metadata_static() -> crate::mcp::types::BuiltinServerMetadata {
        crate::mcp::types::BuiltinServerMetadata {
            display_name: "Your Server".to_string(),
            description: "Brief description for UI".to_string(),
            icon: None,
        }
    }
}
```

### Step 3: Implement BuiltinMCPServer Trait

**Critical:** declare `pub const NAME` as the single source of truth for the server name.
This constant is referenced by both `fn name()` and the regression tests in `agent/tools.rs`.
A typo in a string literal would compile silently; a typo here breaks the build immediately.

```rust
/// Canonical server name – must exactly match the entry in BUILTIN_SERVICE_REGISTRY.
pub const NAME: &str = "your_server"; // lowercase_snake_case, no spaces

#[async_trait]
impl BuiltinMCPServer for YourServer {
    fn name(&self) -> &str {
        NAME // ← reference the const, never a raw string literal
    }

    fn description(&self) -> &str {
        "Detailed description of server capabilities"
    }

    fn display_name(&self) -> String {
        "Your Server".to_string()
    }

    fn tools(&self) -> Vec<MCPTool> {
        Self::tools_static()
    }

    async fn get_service_context(&self, options: Option<&Value>) -> ServiceContext {
        // Extract session_id if provided in options
        let session_id = if let Some(opts) = options {
            opts.get("session_id")
                .and_then(|v| v.as_str())
                .unwrap_or(&self.session_id)
                .to_string()
        } else {
            self.session_id.clone()
        };

        // Build context prompt for AI (what the agent SEES)
        // ✅ RULE 7: Echo recent changes with context
        let context_prompt = format!(
            "## Your Server

**Session**: {}
**Status**: Active

**Recent Activity**:
- Resource 'A' created (ID: 123)
- Resource 'B' updated: 'Refactoring login flow' (ID: 456)

**Available Features**: Feature A, Feature B

💡 Use listYourResources() to see available items.",
            session_id
        );

        // Build structured state for UI (what the agent DOESN'T see)
        ServiceContext {
            context_prompt,
            structured_state: Some(json!({
                "session_id": session_id,
                "server_type": "your_server",
                "initialized": true
            })),
        }
    }

    async fn call_tool(
        &self,
        tool_name: &str,
        args: Value,
        session_id: Option<String>,
    ) -> Result<MCPResult, String> {
        match tool_name {
            "yourTool" => handlers::handle_your_tool(self, args, session_id).await,
            "listResources" => handlers::handle_list_resources(self, args, session_id).await,
            _ => Err(format!("Tool '{}' not found", tool_name)),
        }
    }
}
```

### Step 4: Define Tool Schemas (Following Manifesto Rules)

**Critical rule for tool docs:**

- `input_schema` property descriptions are the single source of truth for parameter semantics.
- Tool `description` should focus on purpose, prerequisites, workflow, and next actions.
- Do **not** add `PARAMETERS:` blocks in tool `description` when the same details already exist in schema.

**File:** `src-tauri/src/mcp/builtin/your_server/tools.rs`

```rust
use crate::mcp::{utils::schema_builder::*, MCPTool};
use serde_json::json;
use std::collections::HashMap;

/// ✅ CREATE TOOL: No ID parameter (Rule 1: Immutable ID Rule)
pub fn create_your_resource_tool() -> MCPTool {
    let mut props = HashMap::new();

    // ❌ NEVER include "id" field in create tools
    props.insert(
        "name".to_string(),
        string_prop(
            Some(1),
            Some(100),
            Some("Resource name (required)")
        ),
    );

    props.insert(
        "description".to_string(),
        string_prop(
            None,
            Some(500),
            Some("Resource description (optional)")
        ),
    );

    MCPTool {
        name: "createResource".to_string(),
        title: Some("Create Resource".to_string()),
        description: "Create a new resource in the system.

⚠️ WORKFLOW:
1. System generates unique ID automatically
2. Returns ID in response for future operations
3. Use listResources() to verify creation

RESPONSE:
- Created resource with system-generated ID
- Use returned ID for updateResource() or deleteResource()

💡 NEXT STEPS: Use getResource(id) to verify or updateResource(id) to modify"
            .to_string(),
        input_schema: object_schema(props, vec!["name".to_string()]),
        output_schema: None,
        annotations: None,
    }
}

/// ✅ UPDATE/DELETE TOOLS: ID is required (Rule 1)
pub fn create_update_resource_tool() -> MCPTool {
    let mut props = HashMap::new();

    // ✅ ID is REQUIRED for updates
    props.insert(
        "id".to_string(),
        string_prop(
            Some(1),
            Some(50),
            Some("Resource ID (from createResource or listResources)")
        ),
    );

    props.insert(
        "name".to_string(),
        string_prop(
            Some(1),
            Some(100),
            Some("New resource name")
        ),
    );

    // ✅ RULE 6: Memory-Augmented Mutation
    props.insert(
        "summary".to_string(),
        string_prop(
            None,
            Some(200),
            Some("Optional context: why this change is being made (e.g., 'Refactoring X', 'Fixing bug Y')")
        ),
    );

    MCPTool {
        name: "updateResource".to_string(),
        title: Some("Update Resource".to_string()),
        description: "Update an existing resource.

⚠️ PREREQUISITE: Obtain valid ID from:
- createResource() response
- listResources() output

ERROR HANDLING:
- If ID not found, returns error with suggestion to use listResources()

💡 WORKFLOW:
1. Call listResources() to find the resource
2. Extract the 'id' field from the result
3. Pass exact ID to this tool"
            .to_string(),
        input_schema: object_schema(props, vec!["id".to_string(), "name".to_string()]),
        output_schema: None,
        annotations: None,
    }
}

/// ✅ LIST TOOL: Returns IDs in BOTH text and structured content
pub fn create_list_resources_tool() -> MCPTool {
    let props = HashMap::new();  // No parameters needed

    MCPTool {
        name: "listResources".to_string(),
        title: Some("List Resources".to_string()),
        description: "List all available resources with their IDs.

RETURNS:
- Complete list of resources with IDs and details
- Use returned IDs for updateResource() or deleteResource()

OUTPUT FORMAT (text):
Each resource shows: ID | Name | Status

💡 Use getResource(id) to see full details of a specific resource"
            .to_string(),
        input_schema: object_schema(props, vec![]),
        output_schema: None,
        annotations: None,
    }
}
```

### Step 5: Implement Tool Handlers (Following Manifesto Rules)

**File:** `src-tauri/src/mcp/builtin/your_server/handlers.rs`

```rust
use super::YourServer;
use crate::mcp::builtin::error_guidance::{operation_failed_error, ToolGroup};
use crate::mcp::types::{text, MCPContent, MCPResult};
use crate::mcp::utils::success_hint::SuccessHint;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct CreateResourceArgs {
    name: String,
    description: Option<String>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct UpdateResourceArgs {
    id: String,  // ✅ Required for updates
    name: String,
    summary: Option<String>, // ✅ Rule 6
}

/// ✅ CREATE HANDLER: Generates ID, returns it in BOTH channels (Rule 3)
pub async fn handle_create_resource(
    server: &YourServer,
    args: Value,
    _session_id: Option<String>,
) -> Result<MCPResult, String> {
    let args: CreateResourceArgs = serde_json::from_value(args)
        .map_err(|e| format!("Invalid arguments: {}", e))?;

    // ✅ SYSTEM GENERATES ID (Rule 1: Immutable ID Rule)
    let resource_id = generate_id();  // Use UUID, CUID, or domain-specific format

    // TODO: Insert into database
    // db.resources.insert(Resource {
    //     id: resource_id.clone(),
    //     name: args.name.clone(),
    //     description: args.description.clone(),
    //     session_id: server.session_id.clone(),
    // }).await?;

    // ✅ DUAL-CHANNEL RESPONSE (Rule 3)
    // Channel 1: TEXT (What the AI SEES)
    let result_text = format!(
        "Resource created successfully (ID: {}).\n\n\
         Name: {}\n\
         Description: {}\n\n\
         💡 NEXT STEPS:\n\
         - Use getResource(\"{}\") to view details\n\
         - Use updateResource(\"{}\", ...) to modify\n\
         - Use listResources() to see all resources",
        resource_id,  // ✅ ID IN TEXT for AI to read
        args.name,
        args.description.as_deref().unwrap_or("None"),
        resource_id,
        resource_id
    );

    // Channel 2: STRUCTURED CONTENT (What the UI sees, AI DOESN'T)
    let structured_data = json!({
        "resource_id": resource_id,  // For UI parsing/rendering
        "name": args.name,
        "description": args.description,
        "created_at": chrono::Utc::now().to_rfc3339()
    });

    Ok(MCPResult {
        content: vec![text(result_text)],
        structured_content: Some(structured_data),
        is_error: Some(false),
    })
}

/// ✅ UPDATE HANDLER: Validates ID existence FIRST (Rule 2: Hallucination Firewall)
pub async fn handle_update_resource(
    server: &YourServer,
    args: Value,
    _session_id: Option<String>,
) -> Result<MCPResult, String> {
    let args: UpdateResourceArgs = serde_json::from_value(args)
        .map_err(|e| format!("Invalid arguments: {}", e))?;

    // ✅ HALLUCINATION FIREWALL (Rule 2)
    // Check existence BEFORE attempting database write
    // let exists = db.resources.exists(&args.id).await
    //     .map_err(|e| format!("Database error: {}", e))?;

    let exists = false;  // TODO: Replace with actual DB check

    if !exists {
        // ✅ SUCCESS HINT PATTERN (Rule 5)
        return Ok(operation_failed_error(
            "Update Resource",
            &format!("Resource '{}' not found", args.id),
            vec![
                "Use listResources() to find the correct resource ID".to_string(),
                "IDs are case-sensitive and must match exactly".to_string(),
                format!("You provided: '{}'", args.id)
            ],
            ToolGroup::YourServer  // Replace with actual group
        ));
    }

    // Proceed with update only after validation passes
    // db.resources.update(&args.id, UpdateData {
    //     name: args.name.clone(),
    // }).await?;

    // ✅ RULE 7: State Echo
    // If a summary was provided, echo it back so the agent knows it was recorded
    let summary_echo = args.summary.as_deref().unwrap_or("No summary provided");

    let result_text = format!(
        "Resource updated successfully (ID: {}).\n\n\
         New name: {}\n\
         Context: {}\n\n\
         💡 Use getResource(\"{}\") to view updated details",
        args.id,
        args.name,
        summary_echo,
        args.id
    );

    Ok(SuccessHint::new(
        result_text,
        vec![format!("Use getResource(\"{}\") to verify changes", args.id)]
    ).to_mcp_result_with_data(Some(json!({
        "resource_id": args.id,
        "updated_fields": ["name"],
        "timestamp": chrono::Utc::now().to_rfc3339()
    }))))
}

/// ✅ LIST HANDLER: Shows IDs in text for AI to read (Rule 3)
pub async fn handle_list_resources(
    server: &YourServer,
    _args: Value,
    _session_id: Option<String>,
) -> Result<MCPResult, String> {
    // TODO: Fetch from database
    // let resources = db.resources.list(&server.session_id).await?;

    // Mock data for example
    let resources = vec![
        ("res_abc123", "Example Resource 1", "Active"),
        ("res_def456", "Example Resource 2", "Inactive"),
    ];

    // ✅ IDs VISIBLE IN TEXT (Rule 3: Dual-Channel Response)
    let resource_list = resources.iter()
        .map(|(id, name, status)| format!("  • {} | {} | {}", id, name, status))
        .collect::<Vec<_>>()
        .join("\n");

    let result_text = format!(
        "Found {} resource(s):\n\n{}\n\n\
         💡 NEXT STEPS:\n\
         - Use getResource(id) for full details\n\
         - Use updateResource(id, ...) to modify\n\
         - Use deleteResource(id) to remove",
        resources.len(),
        resource_list
    );

    // Structured data for UI table rendering
    let structured_data = json!({
        "resources": resources.iter().map(|(id, name, status)| json!({
            "id": id,
            "name": name,
            "status": status
        })).collect::<Vec<_>>(),
        "total": resources.len()
    });

    Ok(MCPResult {
        content: vec![text(result_text)],
        structured_content: Some(structured_data),
        is_error: Some(false),
    })
}

// Helper: Generate unique ID
fn generate_id() -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    format!("res_{:x}", rng.gen::<u32>())
    // Or use: uuid::Uuid::new_v4().to_string()
    // Or use: crate::utils::generate_short_id()
}
```

### Step 6: Register Server in Global Registry

Registration requires **three** coordinated edits. Miss any one and the regression tests
will fail immediately.

#### 6a. Module declaration — `src-tauri/src/mcp/builtin/mod.rs`

```rust
pub mod your_server; // Add this line
```

#### 6b. Service registry — `src-tauri/src/agent/tools.rs`

This is the single source of truth for every service canonical name.

```rust
pub(crate) const BUILTIN_SERVICE_REGISTRY: &[BuiltinServiceEntry] = &[
    // ... existing entries ...
    BuiltinServiceEntry { canonical: "your_server", optional: false },
    //                                ^^^^^^^^^^^^
    //                                Must exactly match your_server::NAME
];
```

Set `optional: true` if the service should only be enabled when the agent config
explicitly lists it (e.g. `browser`, `bootstrap`). Core services use `false`.

#### 6c. Regression test list — `src-tauri/src/agent/tools.rs` (tests module)

```rust
fn each_builtin_server_name_is_in_registry() {
    use crate::mcp::builtin;
    let all_names: &[&str] = &[
        // ... existing entries ...
        builtin::your_server::NAME, // ← add this
    ];
    // ...
}
// Also add to: builtin_server_names_are_unique, registry_and_server_list_are_in_sync
```

All four regression tests share the same `all_names` pattern. Update each one.

#### 6d. Session instantiation — `src-tauri/src/mcp/builtin/mod.rs`

```rust
impl BuiltinServerRegistry {
    pub fn new_session_instance(
        &self,
        server_id: &str,
        session_id: String,
    ) -> Option<Arc<dyn BuiltinMCPServer>> {
        match server_id {
            // ... existing servers
            "your_server" => Some(Arc::new(YourServer::new(session_id))),
            _ => None,
        }
    }
}
```

> **Why three places?** `mod.rs` wires the module into the build; `BUILTIN_SERVICE_REGISTRY`
> drives runtime routing and alias resolution; the regression test list enforces that every
> registered canonical has a concrete server `NAME` backing it — and vice-versa.

### Step 7: Add Integration Tests

**File:** `src-tauri/src/mcp/builtin/your_server/mod.rs`

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_resource_generates_id() {
        let server = YourServer::new("test_session".to_string());

        let args = json!({
            "name": "Test Resource",
            "description": "Test description"
        });

        let result = handlers::handle_create_resource(&server, args, None).await.unwrap();

        // ✅ Verify ID is in text content (Rule 3)
        let text_content = result.content.iter()
            .find_map(|c| match c {
                MCPContent::Text { text } => Some(text.as_str()),
                _ => None
            })
            .expect("Expected text content");

        assert!(text_content.contains("ID:"), "ID must be in text for AI");
        assert!(text_content.contains("res_"), "ID must be visible in output");

        // ✅ Verify ID is also in structured content (for UI)
        assert!(result.structured_content.is_some());
        let data = result.structured_content.unwrap();
        assert!(data.get("resource_id").is_some(), "ID must be in structured data");
    }

    #[tokio::test]
    async fn test_update_validates_id_existence() {
        let server = YourServer::new("test_session".to_string());

        let args = json!({
            "id": "nonexistent_id",
            "name": "Updated Name"
        });

        let result = handlers::handle_update_resource(&server, args, None).await.unwrap();

        // ✅ Verify hallucination firewall (Rule 2)
        assert_eq!(result.is_error, Some(true), "Should return error for invalid ID");

        let text_content = result.content.iter()
            .find_map(|c| match c {
                MCPContent::Text { text } => Some(text.as_str()),
                _ => None
            })
            .unwrap();

        // ✅ Verify success hint pattern (Rule 5)
        assert!(text_content.contains("listResources"), "Error should suggest recovery tool");
    }

    #[test]
    fn test_tools_have_no_id_in_create_schema() {
        let tools = YourServer::tools_static();
        let create_tool = tools.iter()
            .find(|t| t.name.starts_with("create"))
            .expect("Should have create tool");

        // ✅ Verify Rule 1: Immutable ID Rule
        let props = &create_tool.input_schema.properties;
        assert!(!props.contains_key("id"), "Create tool must NOT have ID parameter");
    }
}
```

---

## Design Manifesto Compliance Checklist

Use this checklist before submitting any builtin tool implementation:

### Rule 1: The Immutable ID Rule ✅

- [ ] CREATE tools have NO `id` parameter in schema
- [ ] UPDATE/DELETE tools have REQUIRED `id` parameter
- [ ] System generates IDs using UUID/CUID/domain format
- [ ] Generated IDs are returned in tool responses

### Rule 2: The Hallucination Firewall ✅

- [ ] All UPDATE/DELETE handlers validate ID existence FIRST
- [ ] Validation happens BEFORE any database write
- [ ] Invalid IDs return structured errors (not raw DB errors)
- [ ] Error messages suggest recovery tools (Rule 5)

### Rule 3: The Dual-Channel Response Rule ✅

- [ ] **Critical IDs are in TEXT content** (AI can read them)
- [ ] Text content is complete narrative (what happened, IDs, status)
- [ ] Structured content is in JSON (for UI rendering)
- [ ] AI-visible content is self-sufficient (no dependency on JSON)

### Rule 4: AI-Native Descriptions ✅

- [ ] Tool descriptions use data-oriented language (extract, use, target)
- [ ] No human UI actions (click, type, enter, copy)
- [ ] Parameter semantics are documented only in `input_schema` field descriptions
- [ ] Tool descriptions do not duplicate schema parameter docs (no `PARAMETERS:` blocks)
- [ ] Prerequisites explicitly documented
- [ ] Workflow steps numbered and clear
- [ ] Examples show expected patterns

### Rule 5: The Success Hint Pattern ✅

- [ ] All errors include recovery suggestions
- [ ] Suggestions reference tools from same server
- [ ] Error format: "❌ Problem. 💡 Use toolName() to fix"
- [ ] No raw "Not Found" errors without context

### Rule 6: Memory-Augmented Mutation Rule (New) ✅

- [ ] All state-changing tools (UPDATE/DELETE/COMPLETE) have optional `summary` or `reason` parameter
- [ ] This parameter allows agent to Explain Why/How
- [ ] Stored alongside the data change (not discarded)

### Rule 7: The State Echo Rule (New) ✅

- [ ] Agent-provided summaries are echoed back in `get_service_context`
- [ ] Echoed summaries are truncated if too long (e.g., >50 chars)
- [ ] Context prompt prioritizes recent state changes + reasons

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Hidden IDs (Rule 3 Violation)

```rust
// ❌ WRONG: ID only in structured_content
let result_text = "Resource created successfully.";
let data = json!({ "id": resource_id });  // AI can't see this!
```

```rust
// ✅ CORRECT: ID in BOTH channels
let result_text = format!(
    "Resource created (ID: {}).\n\nUse getResource(\"{}\") to view",
    resource_id, resource_id
);
let data = json!({ "id": resource_id });
```

### ❌ Pitfall 2: Trusting Agent IDs (Rule 2 Violation)

```rust
// ❌ WRONG: Direct database access
db.resources.update(&args.id, data).await?;
```

```rust
// ✅ CORRECT: Validate first
if !db.resources.exists(&args.id).await? {
    return Ok(operation_failed_error(...));
}
db.resources.update(&args.id, data).await?;
```

### ❌ Pitfall 3: Human-Centric Language (Rule 4 Violation)

```rust
// ❌ WRONG: UI-oriented description
description: "Click the resource to select it, then copy the ID"
```

```rust
// ✅ CORRECT: AI-oriented description
description: "Extract resource ID from listResources() output for subsequent operations"
```

### ❌ Pitfall 4: Dead-End Errors (Rule 5 Violation)

```rust
// ❌ WRONG: No recovery path
Err(format!("Resource '{}' not found", id))
```

```rust
// ✅ CORRECT: With recovery hints
Ok(operation_failed_error(
    "Get Resource",
    &format!("Resource '{}' not found", id),
    vec!["Use listResources() to see available IDs".to_string()],
    ToolGroup::YourServer
))
```

### ❌ Pitfall 5: Duplicated Parameter Docs (Schema Drift Risk)

```rust
// ❌ WRONG: Parameters documented in both schema and description
description: "Update resource.\n\nPARAMETERS:\n- id: Resource ID\n- name: New name"
```

```rust
// ✅ CORRECT: Keep parameter details in schema only
props.insert("id".to_string(), string_prop(Some(1), Some(50), Some("Resource ID")));
props.insert("name".to_string(), string_prop(Some(1), Some(100), Some("New resource name")));

description: "Update an existing resource.\n\nPREREQUISITE: get valid ID from listResources()."
```

---

## 🚫 Critical Anti-Patterns

Check for these subtle design flaws that cripple agent reasoning:

### 1. The "State Amnesia" Pattern

- **Symptom**: Agent completes a task but loses the _reason context_.
- **Example**: `completeTask(id)` (No summary)
- **Result**: Agent forgets _how_ it solved the problem. If user asks "How did we fix X?", the agent has to search chat history or Hallucinate.
- **Fix**: Always include optional `summary`, `reason`, or `context` parameters in state-changing tools (Rule 6).

### 2. The "Implementation Gap"

- **Symptom**: Tool design docs specify rich parameters, but implementation omits them as "optional/skippable".
- **Example**: Design says `checkTodo(id, summary)`, code implements `checkTodo(id)`.
- **Result**: Agent tries to use the planned feature but fails silently or gives poor data.
- **Fix**: Treat the Tool Schema as a binding contract. Optional parameters are functional requirements for AI reasoning.

### 3. The "Blind Alley" Response

- **Symptom**: Tool returns `void` or generic "Success".
- **Result**: Agent is left in a void, unsure if the action persisted.
- **Fix**: Always return an "Echo" of the new state (Rule 7).

---

## Code Templates

### Template: Error Response with Hints

```rust
use crate::mcp::builtin::error_guidance::{operation_failed_error, ToolGroup};

return Ok(operation_failed_error(
    "Operation Name",
    "Specific error description",
    vec![
        "Use suggestedTool() to find correct value".to_string(),
        "Additional context or constraint".to_string(),
    ],
    ToolGroup::YourServer
));
```

### Template: Success Response with Dual Channels

```rust
use crate::mcp::utils::success_hint::SuccessHint;

let result_text = format!(
    "Operation completed (ID: {}).\n\n\
     Details: {}\n\n\
     💡 Use nextTool(\"{}\") to continue workflow",
    generated_id, details, generated_id
);

Ok(SuccessHint::new(
    result_text,
    vec![format!("Use verifyTool(\"{}\") to check status", generated_id)]
).to_mcp_result_with_data(Some(json!({
    "id": generated_id,
    "metadata": additional_data
}))))
```

### Template: ID Generation

```rust
// Option 1: Short readable IDs
fn generate_id() -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    format!("prefix_{:x}", rng.gen::<u32>())
}

// Option 2: UUID (standard)
fn generate_id() -> String {
    uuid::Uuid::new_v4().to_string()
}

// Option 3: CUID (collision-resistant)
fn generate_id() -> String {
    use crate::utils::generate_short_id;
    generate_short_id()
}
```

---

## Testing Strategy

### Unit Tests (Per Tool)

```rust
#[tokio::test]
async fn test_create_tool_dual_channel_response() {
    let result = handlers::handle_create(...).await.unwrap();

    // Test text content has ID
    let text = extract_text(&result);
    assert!(text.contains("ID:"), "Must show ID in text");

    // Test structured content has ID
    let data = result.structured_content.unwrap();
    assert!(data.get("id").is_some(), "Must have ID in JSON");
}

#[tokio::test]
async fn test_update_tool_hallucination_firewall() {
    let result = handlers::handle_update(invalid_id_args).await.unwrap();

    assert_eq!(result.is_error, Some(true));
    let text = extract_text(&result);
    assert!(text.contains("listResources"), "Must suggest recovery");
}
```

### Integration Tests (Full Workflow)

```rust
#[tokio::test]
async fn test_create_update_delete_workflow() {
    let server = YourServer::new("test_session".to_string());

    // 1. Create resource
    let create_result = server.call_tool(
        "createResource",
        json!({"name": "Test"}),
        None
    ).await.unwrap();

    // 2. Extract ID from text (simulate agent reading)
    let id = extract_id_from_text(&create_result);

    // 3. Update with extracted ID
    let update_result = server.call_tool(
        "updateResource",
        json!({"id": id, "name": "Updated"}),
        None
    ).await.unwrap();

    assert_eq!(update_result.is_error, Some(false));
}
```

---

## Frontend Integration

After implementing the Rust backend, add TypeScript wrappers:

**File:** `src/lib/backend/your-server-api.ts`

```typescript
import { safeInvoke } from './core';
import type { MCPResponse } from '@/lib/mcp';

export async function createYourResource(
  serverName: string,
  name: string,
  description?: string,
): Promise<MCPResponse<unknown>> {
  return safeInvoke('call_builtin_tool', {
    serverName,
    toolName: 'createResource',
    arguments: { name, description },
  });
}

export async function listYourResources(
  serverName: string,
): Promise<MCPResponse<unknown>> {
  return safeInvoke('call_builtin_tool', {
    serverName,
    toolName: 'listResources',
    arguments: {},
  });
}
```

---

## Summary

**Key Principles:**

1. **No ID inputs for CREATE** - System generates, agent receives
2. **Validate before writes** - Hallucination firewall on all ID-based operations
3. **Dual-channel responses** - IDs visible in BOTH text (AI) and JSON (UI)
4. **AI-native descriptions** - Data operations, not UI actions
5. **Recovery hints** - Every error suggests a path forward

**Quality Gates:**

- [ ] `pub const NAME: &str = "your_name";` declared in server module (not an inline literal in `fn name()`)
- [ ] `fn name(&self)` returns `NAME` (the const), not a raw string
- [ ] `BuiltinServiceEntry { canonical: "your_name", optional: … }` added to `BUILTIN_SERVICE_REGISTRY` in `agent/tools.rs`
- [ ] `builtin::your_server::NAME` added to `all_names` in **all three** regression test functions in `agent/tools.rs`
- [ ] `cargo test registry` passes (4/4 registry regression tests green)
- [ ] All tests pass (unit + integration)
- [ ] Manifesto compliance checklist complete
- [ ] Frontend TypeScript wrappers added
- [ ] Server registered in builtin registry (`mod.rs` module decl + session instantiation match arm)
- [ ] Documentation includes workflow examples

**When in doubt:** Look at existing implementations (workspace, planning, knowledge) and follow their patterns for session management, error handling, and response formatting.
