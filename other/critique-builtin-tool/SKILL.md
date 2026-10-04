---
name: critique-builtin-tool
description: Audit and critique builtin MCP tool implementations in LibrAgent. Use when auditing existing builtin MCP server implementations for compliance, reviewing pull requests that add or modify builtin tools, validating tool implementations against the Tool Design Manifesto v2.1, or identifying potential issues before they reach production.
---

# Critique Builtin MCP Tool Skill

## When to Use This Skill

Use this skill when:

- Auditing existing builtin MCP server implementations for compliance
- Reviewing pull requests that add or modify builtin tools
- Validating tool implementations against the Tool Design Manifesto v2.1
- Providing constructive feedback on tool design and implementation
- Identifying potential issues before they reach production

**Prerequisites:** Familiarity with Tool Design Manifesto v2.1, Rust, and MCP protocol basics.

---

## Audit Methodology

### Step 1: Understand the Tool Design Manifesto Rules

Before auditing, internalize these 5 critical rules:

#### **Rule 1: The Immutable ID Rule (Schema Design)**

- **Never** expose system-critical IDs as input for CREATE operations
- CREATE tools: System generates ID, agent receives it
- UPDATE/DELETE tools: ID is required input (validated before use)

#### **Rule 2: The Hallucination Firewall (Execution Logic)**

- **Never** trust agent-provided IDs without validation
- Check existence BEFORE any database/state mutation
- Return logic errors (not DB errors) with recovery hints

#### **Rule 3: The Dual-Channel Response Rule (Output)**

- **Text content** (what AI sees): Complete narrative with IDs, status, next steps
- **Structured content** (what UI sees): JSON for rendering tables/graphs
- Critical IDs MUST be in BOTH channels

#### **Rule 4: AI-Native Descriptions (Input)**

- Use data operation terms: "extract", "use", "target"
- Avoid human UI actions: "click", "type", "copy", "paste"
- Document prerequisites explicitly
- Show workflow patterns, not button clicks

#### **Rule 5: The "Success Hint" Pattern (Error Handling)**

- Every error includes path to success
- Suggest recovery tools from same tool group
- Format: "❌ Problem. 💡 Use toolName() to fix"
- Never raw "Not Found" without context

---

## Step 2: Gather Code Artifacts

Collect these files for analysis:

```bash
src-tauri/src/mcp/builtin/your_server/
├── mod.rs              # Server struct + trait impl
├── tools/*.rs          # Tool schema definitions
├── handlers/*.rs       # Tool execution handlers
└── types.rs            # Domain types (if any)
```

**Critical Files to Examine:**

1. **Tool Schemas** - Check for ID parameters in CREATE operations
2. **Tool Handlers** - Check for validation before mutations
3. **Response Building** - Check dual-channel compliance
4. **Error Messages** - Check for recovery hints

---

## Step 3: Rule-by-Rule Audit Process

### ✅ **Auditing Rule 1: Immutable ID Rule**

**What to Look For:**

```rust
// ❌ VIOLATION: ID parameter in CREATE tool
pub fn create_resource_tool() -> MCPTool {
    let mut props = HashMap::new();
    props.insert(
        "id".to_string(),  // ❌ Agent can hallucinate this!
        string_prop(Some(1), Some(50), Some("Resource ID (optional)")),
    );
    // ...
}
```

```rust
// ✅ COMPLIANT: No ID parameter
pub fn create_resource_tool() -> MCPTool {
    let mut props = HashMap::new();
    props.insert(
        "name".to_string(),  // ✅ Only business data
        string_prop(Some(1), Some(100), Some("Resource name")),
    );
    // No "id" field at all
}
```

**Audit Checklist:**

- [ ] All CREATE tools have NO `id` parameter in schema
- [ ] UPDATE/DELETE tools have REQUIRED `id` parameter
- [ ] IDs are generated server-side (UUID/CUID/domain-specific)
- [ ] Generated IDs are returned in responses

**Common False Positives:**

- File paths are NOT system IDs (user-controlled, not DB PKs) ✅ OK
- Session IDs passed as options (not creation parameters) ✅ OK

---

### ⚠️ **Auditing Rule 2: Hallucination Firewall**

**What to Look For:**

```rust
// ❌ VIOLATION: Direct database access without validation
pub async fn handle_update_resource(args: Value) -> Result<MCPResult, String> {
    let args: UpdateArgs = serde_json::from_value(args)?;

    // ❌ No existence check - agent can hallucinate ID
    db.resources.update(&args.id, data).await?;

    Ok(success_result())
}
```

```rust
// ✅ COMPLIANT: Validation before mutation
pub async fn handle_update_resource(args: Value) -> Result<MCPResult, String> {
    let args: UpdateArgs = serde_json::from_value(args)?;

    // ✅ Hallucination firewall
    if !db.resources.exists(&args.id).await? {
        return Ok(operation_failed_error(
            "Update Resource",
            &format!("Resource '{}' not found", args.id),
            vec![
                "Use listResources() to find the correct ID".to_string(),
                "IDs are case-sensitive".to_string(),
            ],
            ToolGroup::YourServer
        ));
    }

    // Safe to proceed
    db.resources.update(&args.id, data).await?;
    Ok(success_result())
}
```

**Audit Checklist:**

- [ ] All ID-based operations validate existence FIRST
- [ ] Validation happens BEFORE database writes
- [ ] Invalid IDs return logic errors (not DB constraint errors)
- [ ] Error messages suggest how to find valid IDs

**Common Pitfalls:**

- Registry lookups that assume ID exists ❌
- Direct `.get(id).unwrap()` without checking ❌
- Generic `not_found_error` without context ⚠️ (functional but not ideal)

---

### 🔍 **Auditing Rule 3: Dual-Channel Response (CRITICAL)**

**This is the most commonly violated rule. Check carefully!**

**What to Look For:**

```rust
// ❌ VIOLATION: ID only in structured_content (AI can't see it!)
let result_text = "Process started successfully";
let data = json!({
    "process_id": process_id  // ❌ INVISIBLE to AI
});

MCPResult {
    content: vec![text(result_text)],  // ❌ No ID in text!
    structured_content: Some(data),
}
```

```rust
// ✅ COMPLIANT: ID in BOTH channels
let result_text = format!(
    "Process started successfully (ID: {}).\n\n\
     Use pollProcess(\"{}\") to check status",
    process_id,  // ✅ Visible to AI
    process_id
);
let data = json!({
    "process_id": process_id  // ✅ Also in JSON for UI
});

MCPResult {
    content: vec![text(result_text)],
    structured_content: Some(data),
}
```

**Audit Process:**

1. **Find all response building code** - Search for `MCPResult`, `SuccessHint`, `to_mcp_result`
2. **Extract the text content** - What does the AI actually see?
3. **Check for critical IDs** - Are process IDs, resource IDs, session IDs visible?
4. **Verify in structured_content** - Is the same data in JSON for UI?

**Audit Checklist:**

- [ ] All generated IDs appear in text content (AI-visible)
- [ ] Text content is self-sufficient (no dependency on JSON)
- [ ] Critical values repeated in structured_content for UI
- [ ] No orphaned IDs (only in JSON, not in text)

**Testing Trick:**

```
Read only the text field. Can an agent:
1. Know what happened?
2. Extract the ID for next operation?
3. Understand the current state?

If NO to any → Violation of Rule 3
```

---

### 📖 **Auditing Rule 4: AI-Native Descriptions**

**What to Look For:**

```rust
// ❌ VIOLATION: Human UI-centric language
description: "Click the resource to select it, then copy the ID and paste it into the update tool"
```

```rust
// ✅ COMPLIANT: AI-native workflow description
description: "Extract resource ID from listResources() output.
Use the ID as input to updateResource() for modifications.

WORKFLOW:
1. Call listResources() to view available resources
2. Identify target resource and extract its ID
3. Pass ID to updateResource(id, newData)

PREREQUISITE: Resource must exist (created via createResource)"
```

**Audit Checklist:**

- [ ] No human UI verbs: click, type, copy, paste, drag, select
- [ ] Uses data operation verbs: extract, use, pass, call, retrieve
- [ ] Prerequisites explicitly documented
- [ ] Workflow shows tool call sequences
- [ ] Examples demonstrate actual usage patterns

**Red Flags:**

- References to "UI", "button", "dialog", "form", "screen"
- Phrases like "enter your input", "click to confirm"
- Missing prerequisite tools in workflow

---

### 💡 **Auditing Rule 5: Success Hint Pattern**

**What to Look For:**

```rust
// ❌ VIOLATION: Raw error, no recovery path
.ok_or_else(|| format!("Process '{}' not found", process_id))?
```

```rust
// ⚠️ PARTIAL: Generic hints (not context-specific)
return Ok(not_found_error("Process", process_id, ToolGroup::Workspace));
// Uses default hints like "Use listDirectory" ❌ Wrong for processes
```

```rust
// ✅ COMPLIANT: Context-specific recovery hints
return Ok(operation_failed_error(
    "Poll Process",
    &format!("Process '{}' not found", process_id),
    vec![
        "Use listProcesses() to see all active processes".to_string(),
        "Process IDs are case-sensitive and must match exactly".to_string(),
        "Process may have finished - check with readProcessOutput()".to_string(),
    ],
    ToolGroup::Workspace
));
```

**Audit Checklist:**

- [ ] All errors include 2-3 actionable recovery steps
- [ ] Suggested tools are from same tool group
- [ ] Error format includes ✗ marker and 💡 hints
- [ ] No raw Err() returns without context
- [ ] Generic helpers used appropriately (or replaced with specific hints)

**Common Issues:**

- Using `not_found_error` helper for different resource types
- Missing tool suggestions for recovery
- Hints reference wrong tool group (browser hints for workspace errors)

---

## Step 4: Document Findings

### Compliance Matrix Template

```markdown
## Compliance Audit: [ServerName] Builtin Tools

| Rule                      | Status   | Grade | Evidence  |
| ------------------------- | -------- | ----- | --------- |
| 1. Immutable ID Rule      | ✅/⚠️/🔴 | A-F   | [Details] |
| 2. Hallucination Firewall | ✅/⚠️/🔴 | A-F   | [Details] |
| 3. Dual-Channel Response  | ✅/⚠️/🔴 | A-F   | [Details] |
| 4. AI-Native Descriptions | ✅/⚠️/🔴 | A-F   | [Details] |
| 5. Success Hint Pattern   | ✅/⚠️/🔴 | A-F   | [Details] |

**Overall Grade:** [A-F] - [Summary]
```

### Grading Rubric

**A (Excellent):** Fully compliant, exemplary implementation
**B (Good):** Compliant with minor improvements possible
**C (Acceptable):** Functional but has non-critical issues
**D (Needs Improvement):** Has violations that impact UX
**F (Critical Issues):** Blocking issues, not production-ready

---

## Step 5: Provide Constructive Feedback

### Feedback Template

````markdown
### [Priority Level] [Rule Name] - [Title]

**Problem:** [Clear description of what's wrong]

**Location:** `file.rs` lines X-Y

**Current Code:**

```rust
// Show the problematic code
```
````

**Issue:** [Why this violates the manifesto]

**Recommended Fix:**

```rust
// Show the corrected code
```

**Impact:** [How this affects AI agents]

**Priority:** P0 (Blocker) / P1 (High) / P2 (Medium) / P3 (Low)

````

### Priority Guidelines

**P0 (Blocker):** Must fix before production
- Rule 3 violations (IDs invisible to AI)
- Rule 1 violations (ID input on create)
- Missing validation causing crashes

**P1 (High):** Should fix soon
- Rule 2 partial violations (poor error messages)
- Rule 5 violations (no recovery hints)

**P2 (Medium):** Nice to have
- Rule 4 improvements (better descriptions)
- Inconsistent error formatting

**P3 (Low):** Optional polish
- Documentation improvements
- Code organization

---

## Real-World Example: Workspace Tools Audit

### Initial Assessment (Incorrect)

```markdown
## 📊 Compliance Score

| Rule | Grade | Issue |
|------|-------|-------|
| 3. Dual-Channel Response | D 🔴 | Process IDs invisible to AI |

**Finding:** Process IDs only in structured_content, agents can't see them.

**Evidence:** Assumed text content didn't include IDs based on quick scan.
````

### Corrected Assessment (After Deep Analysis)

````markdown
## 📊 Compliance Score (CORRECTED)

| Rule                     | Grade | Evidence                        |
| ------------------------ | ----- | ------------------------------- |
| 3. Dual-Channel Response | A ✅  | Process IDs ARE in text content |

**Finding:** IDs are properly visible in BOTH channels.

**Evidence from code (lines 1075-1090):**

```rust
let hint = SuccessHint::new(
    format!(
        "Background process started successfully

• Process ID: {}  // ✅ VISIBLE
• Command: {}

💡 Next Steps:
Use pollProcess(\"{}\") to check status",
        process_id, command, process_id
    ),
    // ...
);
```
````

**Lesson:** Always verify by reading actual response text, not just scanning for patterns.

```

---

## Common Audit Mistakes to Avoid

### ❌ Mistake 1: Scanning Instead of Reading

**Wrong Approach:**
```

Search for "process_id" in structured_content → Found!
Assume it's not in text → Mark as violation ❌

```

**Right Approach:**
```

1. Find response building code
2. Extract literal text content
3. Read what AI actually sees
4. Then check structured_content
5. Verify both channels have critical data ✅

```

### ❌ Mistake 2: Assuming Generic Helpers Are Wrong

**Wrong Assumption:**
```

Code uses not_found_error() → Must be bad ❌

```

**Right Analysis:**
```

1. Check what not_found_error() returns
2. Read the default hints for this tool group
3. Verify hints match the resource type
4. If hints are generic → Suggest improvement ⚠️
5. If hints are wrong → Mark as issue 🔴

```

### ❌ Mistake 3: Missing Context

**Wrong Critique:**
```

"File operations lack validation" ❌
(Actually, they use SecureFileManager with validation)

```

**Right Critique:**
```

1. Trace validation through call stack
2. Check if validation helper exists
3. Verify validation catches edge cases
4. Only flag if genuinely missing ✅

````

---

## Validation Checklist

Before submitting audit findings:

- [ ] Verified code by reading actual implementations (not assumptions)
- [ ] Checked if violations are real or helper-abstracted
- [ ] Provided specific line numbers for issues
- [ ] Included code examples for both violation and fix
- [ ] Graded each rule independently
- [ ] Assigned appropriate priorities
- [ ] Tested recommended fixes compile (if providing code)
- [ ] Acknowledged what's already good (not just problems)

---

## Audit Report Template

```markdown
# [ServerName] Builtin Tools Audit Report

**Auditor:** [Name/System]
**Date:** [YYYY-MM-DD]
**Version:** [Code version/commit]

## Executive Summary

[Overall grade and key findings in 2-3 sentences]

## Detailed Analysis

### Rule 1: Immutable ID Rule - [Grade]

**Status:** ✅ Compliant / ⚠️ Partial / 🔴 Violation

**Findings:**
- [Finding 1]
- [Finding 2]

**Evidence:**
```rust
// Code examples
````

### [Repeat for Rules 2-5]

## Priority Fixes

### P0 (Blocker)

1. [Issue title] - [File location]
   - Impact: [Description]
   - Fix: [Code example]

### P1 (High)

[Similar format]

### P2 (Medium)

[Similar format]

## What's Already Good

- ✅ [Strength 1]
- ✅ [Strength 2]
- ✅ [Strength 3]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Conclusion

[Final assessment and next steps]

````

---

## Testing Your Audit

### Self-Validation Questions

1. **Did I read actual code or make assumptions?**
   - ✅ Traced through implementation
   - ❌ Assumed based on patterns

2. **Are my examples accurate?**
   - ✅ Copy-pasted from source
   - ❌ Paraphrased or invented

3. **Did I verify fixes would work?**
   - ✅ Tested or checked against working examples
   - ❌ Suggested theoretical fixes

4. **Am I being fair?**
   - ✅ Acknowledged what's good
   - ❌ Only listed problems

5. **Is my feedback actionable?**
   - ✅ Specific files, lines, and code examples
   - ❌ Vague "improve error handling"

---

## Advanced: Automated Audit Patterns

### Grep Patterns for Quick Scan

```bash
# Rule 1: Find CREATE tools with ID parameters
rg -A 10 'fn create_.*_tool' | rg 'props.insert.*"id"'

# Rule 2: Find direct database access without validation
rg 'db\.\w+\.(update|delete|insert)' | rg -v 'if.*exists'

# Rule 3: Find response building
rg 'MCPResult|SuccessHint::new|to_mcp_result'

# Rule 5: Find raw Err returns
rg 'Err\(format!\(".*not found'
````

### Code Review Checklist

When reviewing PR:

- [ ] New CREATE tools have no ID parameter
- [ ] UPDATE/DELETE operations validate before mutation
- [ ] Response text includes all critical IDs
- [ ] Error messages suggest recovery tools
- [ ] Tool descriptions are AI-native
- [ ] No human UI verbs in descriptions
- [ ] Success/error hints are context-specific
- [ ] Structured content mirrors text content

---

## Summary

**Key Principles for Effective Audits:**

1. **Read Code, Don't Assume** - Verify by tracing actual execution
2. **Context Matters** - Generic helpers may be appropriate
3. **Be Specific** - Provide exact locations and examples
4. **Be Balanced** - Acknowledge strengths and weaknesses
5. **Be Actionable** - Give clear fixes, not vague suggestions
6. **Validate Yourself** - Double-check before publishing findings

**Common Audit Flow:**

```
1. Gather code artifacts
2. Apply rule-by-rule checklist
3. Document findings with evidence
4. Prioritize issues (P0-P3)
5. Provide specific fixes
6. Validate audit accuracy
7. Submit constructive feedback
```

**When in Doubt:**

- Read the actual code path
- Check if helpers abstract the pattern correctly
- Look for working examples in the codebase
- Verify your recommended fix would compile
- Ask for second review if unsure

The goal is **constructive improvement**, not finding fault. Good audits help teams build better AI agent tools!
