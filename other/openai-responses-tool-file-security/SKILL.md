---
name: openai-responses-tool-file-security
description: Review an OpenAI Responses API integration for unsafe hosted-tool exposure, file-search scope failures, function-calling validation gaps, and conversation-state or tool-loop escalation.
last_reviewed: 2026-04-27
---

# OpenAI Responses Tool and File Security

## First Principle

**The Responses API is stateless by design — but `previous_response_id` re-introduces state. Every response that chains to a prior response inherits its context, including any injected content from earlier turns.**

The OpenAI Responses API was designed to be simpler and more controllable than the Assistants API by eliminating persistent server-side thread state. But `previous_response_id` re-creates conversation state in the application layer. If prior responses contain injected instructions, tool outputs from attacker-influenced sources, or file content the user was not authorized to see — and that context is re-injected into new responses — the "simpler" stateless API has become a stateful injection chain. The application is now responsible for validating what it re-injects, because the API will not.

Read the base [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md) first for the shared control model. This skill narrows the controls to OpenAI-hosted tool and file surfaces.

## Framework Focus

- `responses.create`, conversation state, and `previous_response_id`
- Built-in tools such as file search and other hosted tools
- Custom function calling, `tool_choice`, `max_tool_calls`, and structured tool arguments
- Uploaded files, vector stores, and file-backed retrieval

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Uploaded files, vector-store contents, tool arguments, response items, and tool outputs are all validated before they influence application logic or future requests. |
| **Scope** | Files, vector stores, tools, and conversation state are scoped per user and per task. No cross-user file access, no tool exposure beyond what the current context requires. |
| **Isolate** | If the model misuses a hosted tool or produces unsafe tool-call output, the failure is contained and cannot widen file access, trigger unsupported actions, or poison future responses. |
| **Enforce** | JSON schema validation, response-item parsing, file authorization checks, and explicit tool configuration are deterministic code controls — not defaults trusted from the API. |

## RT.1 Hosted Tool Invocation and File Scope Review

**The Responses API-specific risk:** Hosted tools (file search) and custom functions are attached at the request level. If files or vector stores are attached without per-user authorization checks, the model can retrieve and disclose content from any attached resource — regardless of whether the current user owns or is authorized to access those resources.

### Check

- Is every file and vector store attached to a response request authorized for the current user before the request is made?
- Are hosted tools enabled only on the specific response paths that require them — not globally across all requests?
- Is `tool_choice` configured to prevent the model from spontaneously invoking sensitive tools when the current request does not require them?

### Action

- **Per-request file and vector-store authorization.** Before attaching any file ID or vector store ID to a `responses.create` call, verify that the current user owns or is explicitly authorized to access that resource:

```python
def create_authorized_response(user: User, message: str, file_ids: list[str]):
    # Authorize every file before attachment
    for file_id in file_ids:
        if not file_authorization.is_authorized(user=user, file_id=file_id):
            raise UnauthorizedFileAccessError(f"User {user.id} not authorized for {file_id}")

    return client.responses.create(
        model="gpt-4o",
        input=message,
        tools=[{"type": "file_search", "vector_store_ids": authorized_vector_stores(user)}],
        tool_choice="auto",
    )
```

- **Minimum tool exposure.** For each response path, define which tools are required and attach only those. If a response path is informational-only, do not attach file search, code interpreter, or custom functions.
- **Treat tool outputs and retrieved file snippets as untrusted content.** When tool output or file search results are returned in response items and re-used in subsequent requests, apply the same untrusted-content labeling and injection pattern filtering used for indirect prompt injection sources.

### Failure Modes

- A file ID stored in the application is attached to every request as a "convenience context." Users who should not have access to that file can query its contents through the model.
- `tool_choice` is set to `"required"` for file search. The model is prompted to search for and disclose information from any attached vector store, regardless of the user's original query.
- A custom function returns attacker-controlled JSON. The application trusts the structure because it came from the Responses API and uses it directly in a downstream database query.

## RT.2 Conversation State and Tool Loop Containment

**The Responses API-specific risk:** Chaining responses via `previous_response_id` re-injects the prior response's full context — including tool calls, tool results, and any content that appeared in earlier turns — into the next request. This makes multi-turn conversations a tool-loop injection surface.

### Check

- Before passing a `previous_response_id` to a new request, is the prior response's content validated for injected instructions, unauthorized tool calls, or cross-user content?
- Are tool loops bounded by a maximum call count enforced in the application — not just by the API's `max_tool_calls` parameter?
- Are function call arguments validated against a strict schema before execution — regardless of whether they came from a single-turn or multi-turn request?

### Action

- **Validate prior response content before chaining.** Before using `previous_response_id`, inspect the prior response's `output` items. If any tool calls, tool results, or text items contain injection signatures or unexpected tool invocations, do not chain to that response — start a fresh context.

```python
def safe_chain_response(prior_response_id: str, new_message: str, user: User):
    prior = client.responses.retrieve(prior_response_id)
    for item in prior.output:
        if item.type == "function_call" and not tool_policy.is_authorized(item.name, user):
            log_security_event("unauthorized_tool_in_prior_response", item)
            prior_response_id = None  # Start fresh rather than chain to compromised context
            break
    return client.responses.create(
        model="gpt-4o",
        input=new_message,
        previous_response_id=prior_response_id,
    )
```

- **Application-level tool loop circuit breaker.** Track the number of tool calls across a conversation chain. If a chain exceeds the configured maximum (e.g., 20 tool calls in a session), terminate the chain and require explicit user re-initiation.
- **Strict function call argument validation.** For every function call in the response output, parse the arguments against a strict JSON schema and validate business-rule constraints before execution. Never execute function arguments based on shape alone.
- **Parse response items deterministically.** Do not access response output via `.text` or free-form field extraction. Parse each item by its declared type (`function_call`, `file_search_call`, `message`) and process only known, expected types.

### Minimum Deliverable Per Review

- [ ] Responses API request map: which tools, files, and vector stores are attached per endpoint, and what is the authorization check for each
- [ ] File and vector store authorization path: implemented before attachment, not after
- [ ] `previous_response_id` validation: what is inspected before chaining, and what triggers a fresh start
- [ ] Tool loop circuit breaker: maximum call count and termination behavior
- [ ] Function call argument schema validation: per-function schema and business-rule checks

## Quick Win

**Implement file authorization before every `responses.create` call that attaches files.** Check the user's authorization for each file ID before attachment. This single check prevents the most common file-scope failure — where a file ID stored in a shared session or application state is attached to requests from users who should not have access.

## References

- Shared tool-use control model → [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md)
- File search as hosted retrieval → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
