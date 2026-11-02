---
name: secure-llm-features
description: Use when shipping or reviewing an LLM feature that reads untrusted text or has tools — prompt-injection threat model, least-privilege tools scoped by the user's token, safe output handling, per-user rate and cost limits, logs without prompt PII; mapped to the OWASP LLM Top 10 (2026).
---

# Secure LLM Features

A model cannot tell instructions from data, so any text it reads (a document, a web page, a ticket, a tool result) can try to steer it. You cannot prompt that away. You design so that a steered model has no power: its authority is the user's token, its writes need a human, its output is escaped like any untrusted input, and its spend has a ceiling. The contract and the OWASP map are in [llm-security.md](../_shared/llm-security.md).

## 1. Audit current state

Read `.claude/stack-profile.md` (`languages`, `backend.track`, `frontend`, `ai`). If absent, detect per [stack-profile.md](../../core/_shared/stack-profile.md). Change nothing yet; build the picture:

```bash
grep -rnE "llm\.(generate|stream)|messages\.(create|stream|parse)|@mcp\.tool|registerTool" src       # every model call and tool
grep -rnE "(userId|user_id|tenantId|tenant_id|accountId)" src | grep -iE "tool|schema|z\.object"    # identity as a tool input
grep -rnE "dangerouslySetInnerHTML|v-html|innerHTML|marked\(|markdown-it|react-markdown" src       # output sinks
grep -rniE "(logger|console)\.[a-z]+\(.*(prompt|messages|completion|content)" src                    # prompt content in logs
grep -rniE "api[_-]?key|password|secret|bearer|internal only|do not reveal" prompts                  # secrets or policy in prompts
grep -rnE "maxTokens|max_tokens" src | grep -v platform/llm                                        # per-call limits
grep -rnE "eval\(|new Function|child_process|exec\(|subprocess|\$queryRawUnsafe|sql\.raw" src       # dangerous sinks fed by text
```

Draw the threat model in a table: **assets** (whose data), **untrusted text sources** (documents, tickets, web, user), **tools** with their effect (read or write) and scope, **sinks** (browser, terminal, SQL, shell, another API). Every row without a control is a finding.

## 2. Decide what to do

Fix in this order; stop when the audit is clean:

1. A tool takes identity from input, or runs with a service credential instead of the user's → bind tools to the principal (step 5).
2. Retrieval without a tenant filter in SQL and RLS → [build-rag-pipeline](../build-rag-pipeline/SKILL.md).
3. A write tool without a human confirmation → proposal and confirm.
4. Model output reaches a sink unescaped → sanitize.
5. No per-user budget or rate limit, or a call without `max_tokens` → budget guard.
6. Prompts or completions in logs or span attributes → remove.
7. No injection case in the eval set → add them ([set-up-llm-evals](../set-up-llm-evals/SKILL.md)).
- All present and `Verify` passes → "already in place".

## 3. Detect the track

| Signal | Branch |
|---|---|
| Chat or Q&A, no tools | Output handling, budgets, logging. Skip tool binding |
| RAG | Add tenant isolation and the delimiter rules; the answer step gets no tools |
| Agent with tools | Everything; plus a step cap and the reader/actor split ([security-patterns.md](./security-patterns.md#rule-split-the-reader-from-the-actor)) |
| You publish an MCP server | [build-mcp-server](../build-mcp-server/SKILL.md): OAuth audience, scopes, confirmation by elicitation |
| You consume third-party MCP servers | Pin versions, review tool descriptions on every update, scope what they may reach |
| Browser or terminal renders the output | Sinks table in [security-patterns.md](./security-patterns.md#rule-treat-model-output-as-untrusted-at-every-sink) |

## 4. Install only what's missing

Nothing beyond the seam ([build-llm-seam](../build-llm-seam/SKILL.md)) and Zod. If you render markdown, use a renderer that does not emit raw HTML (`markdown-it` 15 with its default `html: false`, `react-markdown` 10) or sanitize the HTML with DOMPurify 3; checked 2026-10-09 that `markdown-it` escapes `<script>` and blocks `javascript:` links but **does** render a remote image, which is the exfiltration case the helper below removes.

## 5. Generate the seams

Code: [security-code.md](./security-code.md).

```
src/platform/llm-security/output.ts     # sanitizeModelMarkdown: HTML, images, links, control sequences
src/platform/llm-security/tools.ts      # Principal, defineTool, bindTools: scopes, no identity input, write proposals
src/platform/llm-security/budget.ts     # userBudget guard, BudgetStore
src/platform/llm-security/budget-pg.ts  # Postgres store (migrations/0002_llm_usage.sql)
```

Edit: the image host allow-list (empty by default: every image is removed), the daily limit per user, scope names, the worst-case cost estimate per task.

## 6. Wire it up

1. Build a `Principal` from the verified session or token in the request handler (user, tenant, scopes). Pass it down; never derive it from request body or model output.
2. Give the model `bindTools(principal, tools).descriptors` and execute its calls through `.call(name, input)`. Cap the loop at 10 steps. A `needs_confirmation` result goes to your UI as a confirmation dialog; only the user's click calls `.confirm(actionId)`.
3. Wrap each model call in `budget.guard(principal.userId, worstCaseUsd, () => llm.generate(…))`. Map `BudgetExceeded` to `429` with `Retry-After`. Add a per-minute rate limit at the gateway or in middleware (see the status-code guidance in [api-contract-patterns.md](../../backend/design-http-api/api-contract-patterns.md)).
4. Run `sanitizeModelMarkdown(text, ALLOWED_IMAGE_HOSTS)` before rendering, then render with a renderer that escapes HTML. Terminal and IDE sinks: strip control sequences (the same function does).
5. Logs and spans carry ids, task, tokens, cost, error kind. The seam does this already; delete any logging of prompts, messages or completions.

## 7. Verify

```bash
pnpm vitest run tests/security.test.ts        # sanitizer, tool binding, confirmation, budget
grep -rniE "(logger|console)\.[a-z]+\(.*(prompt|messages|completion)" src   # expect: no output
```

Expected: tests pass: a tool call that names another user is ignored, a user without the scope never sees the tool, a write returns `needs_confirmation` and only the same user can confirm it, an exfiltration image is removed, a second call past the daily limit throws `BudgetExceeded`.

Then attack your own feature with the cases in [security-patterns.md](./security-patterns.md#rule-test-the-effects-not-the-wording) (instruction in a document, markdown-image exfiltration, a request for another tenant's data, a prompt-extraction attempt) and assert on **effects**: no tool call happened, no image URL came out, no other tenant's text appeared. Put them in the eval gate.

## References
- [security-patterns.md](./security-patterns.md): rules and why. [security-code.md](./security-code.md): code.
- [llm-security.md](../_shared/llm-security.md): trust boundaries, OWASP LLM Top 10 (2026) map, merge checklist.
- [security-baseline.md](../../core/_shared/security-baseline.md), [logging-contract.md](../../core/_shared/logging-contract.md).
- [stack-versions.md](../_shared/stack-versions.md).
