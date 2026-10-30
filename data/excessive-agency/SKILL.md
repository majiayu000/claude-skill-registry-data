---
name: excessive-agency
description: Detects autonomous agents that take irreversible or high-impact actions
  without human approval. Use when building autonomous LLM agents,
  implementing multi-step agent pipelines, writing code where LLM output
  triggers real-world actions (file writes, API calls, emails, database
  changes, code execution), or designing agentic workflows with tool use.
---

# Excessive Agency (OWASP LLM08:2025)

## What this checks

Prevents autonomous agents from taking irreversible or high-impact actions without
human oversight. When an LLM can directly write files, send emails, or modify databases,
a single compromised or hallucinated step can cause unrecoverable damage.

## Vulnerable patterns

- Agent dispatches an irreversible action (send mail, delete record, deploy, drop table) immediately on LLM instruction with no human confirmation step
- Single LLM response authorizes a high-impact production action with no impact classification or approval gate
- Agent runs with write access to resources beyond what the task requires — no least-privilege scoping at the tool boundary
- No kill switch, pause mechanism, bounded iteration count, or audit trail for agent actions
- Tool that accepts a raw query string, shell command, or code blob built by the LLM rather than typed structured parameters

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Actions are classified by impact, and the classifier gates dispatch.** Low-impact
   (reversible, narrow scope) may proceed; high-impact (irreversible, broad scope,
   external side effects) blocks on human approval. A classifier that's defined but
   never branched on is the bug this skill prevents.
2. **Tool boundaries enforce an explicit allowlist of actions and resources** —
   path prefixes, API endpoints, table names. The LLM does not choose what's
   allowed; the tool handler does, and rejects anything outside the list before
   dispatch.
3. **Every executed action is audit-logged before dispatch**, with enough context
   to reconstruct what happened: the action name, its parameters, the prompt that
   produced it, and the operator who approved it (if any). After-the-fact logging
   is insufficient — if dispatch crashes, the log is gone.
4. **Irreversible actions cannot be invoked transitively through LLM-generated
   parameters.** A tool named `run_sql` that accepts arbitrary queries violates
   this; a tool named `archive_record(id)` that only issues a scoped update does not.
5. **When the task seems to require LLM-generated SQL, shell commands, or arbitrary
   code strings, redesign the tool interface.** Expose typed parameters (table
   name, filter fields, numeric limits, path components) and reject raw strings
   at the handler boundary. A regex/denylist over a raw query string is
   bypassable through encoding, Unicode, or patterns the author didn't
   anticipate — it is not a substitute for a structured parameter schema.

Translate these principles to the audited file's language, agent framework, and
tool-dispatch surface. Use the framework's documented approval / human-in-the-loop
hook — do not invent ad-hoc confirmation prompts inside the prompt template.

## Verification

Confirm these properties hold regardless of language or framework:

- [ ] Every destructive action taken by the agent is gated by an explicit human confirmation step
- [ ] Agent tools enforce a path allowlist or action allowlist at the tool boundary
- [ ] Agent loops have a bounded iteration count or a dry-run preview mode
- [ ] Irreversible actions cannot be invoked transitively via LLM-generated parameters alone

## References

- CWE-272 ([Least Privilege Violation](https://cwe.mitre.org/data/definitions/272.html))
- CWE-250 ([Execution with Unnecessary Privileges](https://cwe.mitre.org/data/definitions/250.html))
- [OWASP LLM08:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm08-excessive-agency/)
