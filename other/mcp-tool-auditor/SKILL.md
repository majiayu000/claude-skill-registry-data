---
name: mcp-tool-auditor
description: Audit builtin MCP tool implementations against the Tool Design Manifesto. Use when reviewing builtin tools for compliance, checking context_prompt usage, validating text-first MCPResult design, or auditing canonical naming and session isolation correctness.
---

# MCP Tool Auditor

Audit builtin MCP tool implementations in LibrAgent for compliance with the Tool Design Manifesto.

## Audit Checklist

### 1. context_prompt vs structured_state

- [ ] `context_prompt` contains all information the AI needs (readable text, short IDs ok)
- [ ] `structured_state` is NOT relied upon for AI decision-making (AI never sees it)
- [ ] Critical IDs (full session IDs, process IDs, file paths) are in `context_prompt` text

### 2. MCPResult Text-First Design

- [ ] Critical data appears in `content` (text), not just `structured_content`
- [ ] Process IDs, file paths, status messages are copy-pasteable from text
- [ ] Error details are in text output
- [ ] `structured_content` is supplementary for UI rendering only

### 3. Canonical Naming

- [ ] Tool names follow project conventions (no alias proliferation)
- [ ] No redundant tools that could be consolidated

### 4. Session Isolation

- [ ] No global state in builtin server implementations
- [ ] Per-session state is scoped to session ID
- [ ] `MCPServiceProxy` instances are session-specific

### 5. Error Handling

- [ ] Errors return `Result<MCPResult, String>` consistently
- [ ] Error messages are actionable with next steps
- [ ] No `unwrap()` in production code paths

## Usage

Run audits against:

- `src-tauri/src/mcp/builtin/` - All builtin MCP servers
- `src-tauri/src/mcp/` - MCP integration layer
- `docs/guides/builtin_tool_bp.md` - Design standard reference

## Anti-Patterns to Flag

```rust
// ❌ WRONG: Critical ID only in structured_content
let result = MCPResult {
    content: vec![text("Background process started")],
    structured_content: Some(json!({
        "process_id": "7573a69b",  // AI can't see this!
    })),
    is_error: Some(false),
};

// ✅ CORRECT: ID visible in text output
let result = MCPResult {
    content: vec![text("Background process started (ID: 7573a69b)\nUse pollProcess(\"7573a69b\") to check status")],
    structured_content: Some(json!({
        "process_id": "7573a69b",  // Redundant but useful for UI
    })),
    is_error: Some(false),
};
```
