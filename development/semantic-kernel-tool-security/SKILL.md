---
name: semantic-kernel-tool-security
description: Review a Semantic Kernel agent or planner for unauthorized plugin execution, unsafe function routing, excessive connector permissions, missing argument validation, insecure memory use, and weak sandboxing around code or action execution.
last_reviewed: 2026-04-27
---

# Semantic Kernel Tool Security

## First Principle

**Semantic Kernel's auto-invocation is a feature that treats the model's output as execution instructions. If you register more plugins than the current user context requires, you have handed the model the keys to capabilities it should not have.**

Semantic Kernel's planner and automatic function calling are designed to let the model decide which plugins to invoke and with what arguments. This is the intended design — and the core security risk. The model's plugin selection is model output, not deterministic policy. If all registered plugins are visible to all users, and if the planner can call them without a per-invocation authorization check, then any injection that influences the model's plugin selection has effectively invoked those capabilities with the ambient permissions of the service account.

Read the base [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md) first for the shared control model. This skill narrows the controls to concrete Semantic Kernel review points.

## Framework Focus

- Native and prompt-based plugins, function registration, and plugin exposure rules
- Planners, automatic function calling, kernel arguments, filters, and memory connectors
- Connectors to files, HTTP APIs, databases, enterprise systems, and code execution surfaces

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | `KernelArguments`, planner output, plugin parameters, connector responses, and every model-proposed action are validated by deterministic code before execution. |
| **Scope** | Registered plugins, connector permissions, planner reach, and environment-specific function exposure are bounded to the current user's role and task context. |
| **Isolate** | If the model is injected or misbehaves, it cannot escape from Semantic Kernel plugins or connectors into the host environment, core systems, or sensitive data stores. |
| **Enforce** | Typed plugin contracts, JSON schema validation, policy filters, and explicit allowlists are the enforcement layer — not the expectation that the model will call only appropriate plugins. |

## SK.1 Function Calling Authorization

**The Semantic Kernel-specific risk:** Plugins registered for developer convenience, internal tooling, or cross-cutting infrastructure are visible to the planner and automatic function calling by default. A model steered by an injection can invoke administrative or mutating plugins that were never intended for the current user's context.

### Check

- Is the set of plugins registered in the kernel for each request derived from the authenticated user's role — or is a broad global plugin set registered for all requests?
- Does the planner configuration prevent discovery and invocation of internal-only or administrative plugins that should not be reachable from user-facing requests?
- Is there a pre-invocation authorization check for every plugin call — independent of whether the planner approved the call?

### Action

- **Per-request plugin registration.** Build the kernel's plugin set dynamically from the user's role and task context. Do not register all plugins globally and rely on the model to call only appropriate ones.

```csharp
// Wrong — all plugins globally registered
kernel.ImportPluginFromObject(new AdminPlugin(), "admin");
kernel.ImportPluginFromObject(new UserPlugin(), "user");
kernel.ImportPluginFromObject(new DataPlugin(), "data");

// Right — scoped to user role and task
var allowedPlugins = pluginRegistry.GetPluginsForRole(currentUser.Role, request.TaskType);
foreach (var plugin in allowedPlugins)
    kernel.ImportPluginFromObject(plugin.Instance, plugin.Name);
```

- **Pre-invocation policy filter.** Use Semantic Kernel's function filter pipeline to add a pre-invocation check that validates: Is the function being called in the current user's allowlist? Are the arguments within permitted bounds? Is a confirmation token required?

```csharp
kernel.FunctionFilters.Add(new AuthorizationFilter(policyEngine, currentUser));

class AuthorizationFilter : IFunctionFilter
{
    public async Task OnFunctionInvocationAsync(FunctionInvocationContext context, Func<FunctionInvocationContext, Task> next)
    {
        if (!_policy.IsAuthorized(context.Function.Name, _user, context.Arguments))
            throw new UnauthorizedException($"Function {context.Function.Name} not authorized for {_user.Role}");
        await next(context);
    }
}
```

- **Validate `KernelArguments` against typed schemas.** Before any plugin executes, validate its arguments against a typed schema. Reject arguments that contain path traversal, injection metacharacters, out-of-range values, or unexpected fields.
- **Separate read-only from mutating plugins.** Read-only plugins (search, read, fetch) require lower authorization. Mutating plugins (write, delete, send, admin) require explicit confirmation tokens and higher-privilege role.

### Failure Modes

- An admin plugin is registered globally for convenience. A user-facing request is injected to invoke the admin plugin directly. The planner calls it because it is registered and the auto-invocation sees it as applicable.
- Plugin outputs are passed back to the kernel as trusted context. A poisoned API response instructs the kernel to call a different plugin sequence. The kernel follows it because the output appears in the same context as trusted planner state.
- All plugins share the same service account credentials. A read-only plugin call uses an identity that also has write permissions to the production database.

## SK.2 Output Execution Sandboxing

**The Semantic Kernel-specific risk:** Semantic Kernel connects to enterprise systems — databases, file systems, HTTP APIs, code execution surfaces — through connectors. These connectors often use ambient service account credentials. A single injected plugin call can reach any system the connector's identity has access to.

### Check

- Do code, shell, database, and file plugins run inside isolated environments — or do they run with the host process's ambient credentials and filesystem access?
- Are connector credentials scoped to the minimum permissions required for each plugin's task — or do they inherit broad service account permissions?
- Are memory connectors and planners isolated from plugin execution so they cannot be used as side channels to bypass plugin authorization?

### Action

- **Sandbox high-risk plugins.** Code execution, shell access, SQL execution, and file manipulation plugins must run inside a brokered sandbox — container, gVisor, or equivalent — not as direct calls from the host process. The sandbox must restrict: filesystem access (temp directory only), network egress (approved endpoints only), execution time (hard limit), and memory usage.
- **Scoped connector credentials.** Each connector uses a scoped service account with the minimum IAM/RBAC permissions required for that plugin's task. A search plugin does not share credentials with a write plugin. A read-only database connector uses a read-only database user.
- **Log every plugin invocation.** Every plugin call must emit an audit log entry: function name, `KernelArguments` (redacted if sensitive), authorization outcome, and caller identity. Do not log raw secrets or PII in argument values.

### Minimum Deliverable Per Review

- [ ] Semantic Kernel plugin inventory: name, description, role allowlist, connector type, credentials used, and sandbox boundary
- [ ] Pre-invocation filter implementation and authorization policy source
- [ ] Per-request plugin registration: how is the plugin set scoped per user role?
- [ ] Connector credential scope: one credential per plugin or shared? minimum permissions verified?
- [ ] Sandbox configuration for high-risk plugins: isolation mechanism, network rules, filesystem scope

## Quick Win

**Audit which plugins are currently registered globally.** List every plugin registered in the kernel at startup. For each one, ask: "Could a basic user be harmed if an injection caused the model to call this?" If the answer is yes for any plugin, move that plugin to a role-gated registration path before the next deployment.

## References

- Shared tool-use control model → [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md)
- Leakage concerns in logs or memory → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
