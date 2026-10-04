---
name: lean-builtin-tool-auditor
description: Audit builtin MCP tool implementations in LibrAgent for schema accuracy, minimal complexity, and non-bloated hints. Use when reviewing builtin tools for compliance, validating tool schemas, checking for over-engineering, or ensuring next-action hints are concise and relevant.
---

# Lean Builtin Tool Auditor

Audit builtin MCP tools against three principles: correct schemas, no over-engineering, minimal relevant hints.

## 1. Schema Correctness

Tool schemas must be accurate and complete.

**Check:**

- [ ] Parameters have correct types (string, number, boolean, object, array)
- [ ] Required fields are marked required
- [ ] Descriptions are clear and actionable for AI agents
- [ ] No redundant or unused parameters
- [ ] Enum values are exhaustive and correct
- [ ] Default values are safe and sensible

**Anti-pattern:**

```rust
// ❌ WRONG: Vague type, missing required, unclear description
props.insert("path".to_string(), string_prop(
    None, None,
    Some("file location")
));

// ✅ CORRECT: Explicit type, required, actionable description
props.insert("path".to_string(), string_prop(
    Some(1), Some(255),
    Some("Absolute or relative path to target file")
));
```

## 2. No Over-Engineering

Keep implementations simple and maintainable.

**Check:**

- [ ] No alias proliferation (one canonical name per tool)
- [ ] No unnecessary wrapper functions or indirection
- [ ] No over-generalized helpers that obscure logic
- [ ] Error handling is direct, not wrapped in multiple layers
- [ ] No premature abstraction for one-off cases

**Anti-pattern:**

```rust
// ❌ WRONG: Alias error hints bloat
match tool_name {
    "readFile" => self.handle_read_file(...),
    "read_file" | "read" => Ok(MCPResult::error("Did you mean 'readFile'?")),
    _ => Err(format!("Tool '{}' not found", tool_name)),
}

// ✅ CORRECT: Simple match, agent learns from schema
match tool_name {
    "readFile" => self.handle_read_file(...),
    _ => Err(format!("Tool '{}' not found", tool_name)),
}
```

## 3. Hints Without Bloat

Next-action and recovery hints must be required, relevant, and concise.

**Check:**

- [ ] Success hints only when agent needs guidance
- [ ] Error hints include 1-2 specific recovery steps
- [ ] No generic "Use toolX to do Y" when toolX is obvious
- [ ] No redundant hints already in message body
- [ ] No edit-promotion padding on read-only tools
- [ ] Hint text is copy-pasteable (includes exact parameters)
- [ ] Hints are **outcome-conditioned**: steady path stays empty/minimal; phase boundaries may escalate once; repeated failures escalate instead of repeating the same retry

**Exception (not bloat):** State-gated escalation after a milestone or stuck loop is intentional augmentation. Fixed "always promote sibling tool X" on every call is bloat.

**Anti-pattern:**

```rust
// ❌ WRONG: Bloated success hints on read-only tools
let hint = SuccessHint::new(
    format!("Directory listing for '{}':\n\n{}", path, listing),
    vec![
        format!("Use readFile('{}/filename')", path),
        format!("Use listDirectory('{}/subdir')", path),
        "Use search to find content".to_string(),
    ]
);

// ✅ CORRECT: Data speaks for itself
let hint = SuccessHint::new(
    format!("Directory listing for '{}':\n\n{}", path, listing),
    vec![]  // Only add hints when agent actually needs next step
);
```

**Anti-pattern:**

```rust
// ❌ WRONG: Vague error recovery
return Err("Operation failed".to_string());

// ✅ CORRECT: Specific recovery
return Err(format!(
    "Process '{}' not found. Use listProcesses() to find active processes.",
    process_id
));
```

## Audit Workflow

1. Read the tool schema (`mod.rs` or `tools/*.rs`)
2. Read the handler implementation
3. Read response building code for hints
4. Check each dimension above
5. Report only high-confidence issues

## Reference

For full design standard, see `docs/guides/builtin_tool_bp.md`.
