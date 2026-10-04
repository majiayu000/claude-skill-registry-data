---
name: tool-use-execution-security
description: Review an agentic AI system for insecure tool calling, unsafe code or shell execution, excessive permissions, confirmation bypass, argument injection, sandbox escape risk, and action-policy failures across languages and frameworks.
last_reviewed: 2026-04-27
---

# Tool Use and Execution Security

## First Principle

**The model's tool calls are text outputs. If you execute them without validation, you are letting the model control your production environment.**

A model that can call tools is a model that can take real-world actions. The path from "the model says to call deleteDatabase()" to "deleteDatabase() runs" is entirely determined by your application code — not the model. If your application executes tool calls based on model output without a validation layer in between, the model's output is your command interpreter. And if the model can be prompted into producing attacker-controlled tool calls, the attacker is running code in your infrastructure.

## Attack Mental Model

Attackers targeting agentic systems have three primary vectors:

1. **Argument injection** — craft a prompt that causes the model to produce tool arguments containing shell metacharacters, SQL fragments, or path traversal sequences that bypass application-side sanitization.
2. **Permission escalation** — cause the model to invoke a privileged tool (admin, delete, send-email) that is registered in the kernel but not intended for the current user context.
3. **Confirmation bypass** — use indirect content or multi-turn context to cause the model to produce approval-state output that the application interprets as a pre-authorized action.

The attacker's goal is not to break the model — it is to make the model produce the right text at the right moment.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every tool name, argument, and output is validated by deterministic code — schema, allowlist, policy — before the tool executes or its output is consumed. |
| **Scope** | Tools are granted per user role and per task context, not globally. The model sees only the tools it is authorized to call for this specific request. |
| **Isolate** | Code, shell, SQL, and file tools run inside sandboxed environments. A compromised tool call cannot reach the host, core data stores, or ambient credentials. |
| **Enforce** | Confirmation and approval state is tracked by application code, not inferred from model output. The model can propose actions; it cannot authorize them. |

## 3.1 Function Calling Authorization

**The core vulnerability:** The model is told what tools exist. If all registered tools are visible to all users, the model can call any tool for any user — with or without attacker assistance.

### Check

- Is each tool call validated against the current user's role and scope before execution?
- Does validation happen in deterministic code, or does the application trust that the model will only call permitted tools?
- Can the model discover tools through auto-registration or broad kernel inspection that were not intended for this user's context?

### Action

- **Per-request tool allowlist:** Construct the tool list dynamically per request based on user role, session context, and task. Never expose the full tool registry to every request.

```python
# Wrong — all tools exposed globally
tools = kernel.get_all_tools()

# Right — scoped per user and task
tools = tool_registry.get_tools_for(user=current_user, task_type=request.task)
```

- **Pre-execution policy check:** Before invoking any tool, run a deterministic check: Is this tool in the user's allowlist? Are the arguments within permitted bounds? Is a confirmation token required and present?
- **Argument validation:** Validate every argument against a typed schema. Reject calls with unexpected fields, out-of-range values, path traversal patterns, or shell metacharacters. Treat argument validation failure as a security event, not a formatting error.

### Failure Modes

- The tool registry contains admin functions registered for developer convenience. A prompt injection causes the model to call them on behalf of a basic user.
- The application checks tool name authorization but not argument values — an attacker injects `../../../etc/passwd` into a file-read argument.
- A multi-turn conversation builds implicit approval context. The model produces tool calls that the application interprets as confirmed because the prior turn said "yes."

## 3.2 Output Execution Sandboxing

**The core vulnerability:** Code execution, shell access, SQL execution, and file manipulation are all tool calls. If they run with ambient production credentials in the host filesystem, a single injection compromises the entire environment.

### Check

- Do code, shell, SQL, and file tools run inside isolated environments (container, gVisor, WASM sandbox, chroot)?
- Are read-only tools separated from mutating tools, with different authorization requirements?
- Is the execution environment's network egress restricted to the minimum required set of endpoints?

### Action

- **Sandbox every execution tool.** Code execution runs in a container with no filesystem access beyond a temp directory, no outbound network access beyond approved APIs, and a hard CPU/memory/time limit.
- **Separate read from write.** Read-only tools (fetch, search, read-file) have lower authorization requirements than mutating tools (write-file, delete, send-email, database-write). Require explicit confirmation tokens for mutating tools.
- **No ambient credentials.** Execution environments use scoped service accounts with the minimum IAM permissions required. Never mount production credentials into an agent sandbox.

### Minimum Deliverable Per Review

- [ ] Tool inventory: name, description, authorization scope, execution environment, and credential requirements
- [ ] Per-user, per-role tool allowlist and enforcement point
- [ ] Argument validation path per tool (schema, type, bounds, injection patterns)
- [ ] Sandbox boundary for each execution tool (container image, network rules, filesystem mount)
- [ ] Confirmation and approval flow for mutating tools — tracked in application code, not inferred from model output

## Quick Win

**Add a per-request tool allowlist.** If every request sees every registered tool, you have no tool-scope boundary. Construct the tool list dynamically from the user's role. This single change eliminates the most common privilege-escalation path in agentic systems.

## References

- Framework-specific review notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
- Multi-agent trust boundaries → [agentic-trust-boundaries/SKILL.md](../agentic-trust-boundaries/SKILL.md)
