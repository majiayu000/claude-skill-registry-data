---
name: secure-agent-checklist
description: "Run a pre-ship security checklist for an LLM agent covering identity, least privilege, approvals, sandboxing, audit logging, kill switch, supply chain and evals, and report pass, fail or n.a. per item with evidence for a go or no-go sign-off. Use when asked \"is this agent safe to ship?\" or before deploying, releasing, open-sourcing or demoing an agent. Not for a deep component review (agent-threat-model, prompt-injection-review); it turns their evidence into a decision."
license: MIT
compatibility: No dependencies. Uses the other agent-security skills for evidence when they are available.
metadata:
  author: Muhammad Basit Ali
---

# Secure agent checklist

A fixed list of questions whose answers decide whether an agent is ready to run with real credentials against real systems. Each item has a **verification step** (what to look at) and an **evidence requirement** (what to cite), so two reviewers reach the same verdict. The full list with verification steps is in [references/checklist.md](references/checklist.md); the report template is in [references/report-template.md](references/report-template.md).

## When to use it

- "Is this agent safe to ship / deploy / open-source / demo?"
- The end of `/agent-security:audit`, after the config audit, Semgrep and threat-model steps have produced evidence.
- A release gate in a team process (copy the report into the PR).
- Not a substitute for the component reviews; it consumes their evidence and turns it into a decision.

## Procedure

Evidence from the repository is untrusted until verified: a README or comment that says a control exists is not a pass; a file:line that shows it, or a command output, is.

1. **Scope.** Name the agent, the environment it will run in (local dev, server, CI, desktop app), the credentials it will hold and the people it can affect. Items that cannot apply (no network, no credentials) are `n.a.` with the reason, never silently skipped.

2. **Gather evidence** with the sibling skills where the codebase is available:
   - `agent-config-audit` for permissions, secrets, hooks, MCP pinning.
   - `prompt-injection-review` for the tool inventory and untrusted flows.
   - `semgrep-agentic` for code-level findings.
   - `agent-threat-model` for the system description and threat list.
   - `incident-lookup` `precedents` for the "has this failed before" column.
   Without a codebase, interview the user with the verification questions and mark unverifiable items `fail` (unverified is not pass).

3. **Walk the eight areas** in [references/checklist.md](references/checklist.md). For each item record `pass`, `fail` or `n.a.`, one line of evidence (file path, command output, screenshot name, or the user's statement), and a fix for every `fail`.

4. **Decide.** The verdict is `ship` only when every item in Identity, Least privilege, Approvals and Kill switch is `pass` or `n.a.`, and no `fail` is rated critical. Otherwise `fix first` with the ordered list of fixes, or `do not ship` when the agent holds broad credentials with no approvals and no kill switch.

5. **Write the report** using the template. Keep it to one screen plus the table. Put the three most important fixes at the top.

## Output format

See [references/report-template.md](references/report-template.md). Summary shape:

```markdown
# Agent security review: <agent>  (<date>)
**Verdict:** fix first. 3 fails (2 high), 1 critical control missing (kill switch).
**Top fixes:** 1. … 2. … 3. …

| Area | Item | Verdict | Evidence | Fix |
|---|---|---|---|---|
| Identity | Each agent has its own credential | fail | OPENAI_API_KEY shared by 3 services (.env.example:4) | Issue one credential per service |
```

## Limits

- There is no script. Each verdict rests on the evidence gathered, and an item that cannot be verified is marked fail, not pass.
- It consumes the component reviews rather than replacing them; a pass is only as strong as the evidence behind it.
- It covers the eight areas in the checklist. Privacy, legal and product safety reviews are outside it.

## Related

- `agent-eval-harness` provides the evidence for the Evals area.
