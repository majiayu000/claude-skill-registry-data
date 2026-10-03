---
skill_id: inbox-triage
name: Inbox Triage — sort your inbox into reply-now / later / ignore
description: "Triage an email inbox — \"triage my inbox\", \"sort my inbox\", \"what emails need a reply\", \"clear my inbox\". Governs the Gmail or Workspace connector you already have rather than shipping its own integration."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
everyday_skill: true
triggers:
  - "triage my inbox"
  - "sort my inbox"
  - "what emails need a reply"
  - "clear my inbox"
collaborates_with:
  - planner
  - security-analyst    # CSO auto-loop — email is PII; never copied into logs
  - orchestrator        # the unattended "every morning" version (ADR-022)
external_tool:
  name: Gmail / Google Workspace connector (or any email MCP)
  source: Anthropic Connectors Directory (claude.ai/directory) — vetted; OR a Gmail MCP via `claude mcp add`
  pattern: ADR-018 (external-tool integration) + ADR-012 (overlay engine) — Maxim CONSUMES the connector, never rebuilds it
references:
  unattended_version: orchestrator/workflows/inbox-triage.mjs
  adr_external_tool: documents/ADRs/ADR-018-external-tool-integration-pattern.md
  adr_overlay_engine: documents/ADRs/ADR-012-overlay-engine-architecture.md
  adr_workflow_standard: documents/ADRs/ADR-022-autonomous-workflow-standard.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Inbox Triage

> **Does:** sorts your inbox into **reply-now / reply-later / ignore**, and drafts the urgent replies for your approval.
> **Solves:** an inbox so full you don't know where to start.
> **Triggers on:** *"triage my inbox"* · *"what emails need a reply"*

## How Maxim does this (consume the connector — never rebuild it)

Maxim does **not** ship its own Gmail integration. It uses the **email connector you already have** — the Anthropic **Gmail / Google Workspace connector** (vetted, GA, all users) or any email MCP you've added — and adds the layer the raw connector lacks: a triage *framework*, a *privacy gate*, and *confidence*. (ADR-018 + ADR-012: Maxim is the governed brain; the connector is the hands.)

**Per-surface availability (verified 2026-06-26):**
- **Claude Desktop / web:** turn on the Google Workspace → Gmail connector (`+` → Manage connectors). Works immediately.
- **Claude Code:** the Anthropic Gmail connector authenticates at **claude.ai → Settings → Connectors**, then appears in Claude Code automatically; or `claude mcp add` a Gmail MCP (use **`--scope user`** so it's available everywhere, including scheduled runs).

## What it does, step by step

1. **Pull** recent unread via the connector (e.g. `is:unread newer_than:1d`). Read-only.
2. **Classify** each message — **reply-now / reply-later / ignore** — using the Eisenhower matrix (urgency × importance), with the *sender + ask + deadline* as signals.
3. **Draft** replies for the reply-now set. The connector is **draft-only and cannot send** — drafts wait in your Gmail for one-tap manual send. This is a *platform-enforced* safety, on top of Maxim's own.
4. **Return** a digest: counts per bucket + the drafts awaiting you + the 1–2 that actually matter today.

## Behavioral + governance overlay

- **Frameworks (cited per ADR-007):** **Eisenhower Matrix** (urgency × importance) · **Fogg Behavior Model** (surface the easiest high-value reply first to beat inbox paralysis).
- **CSO auto-loop (non-negotiable):** email is personal data. `security-analyst` gates the run — message bodies/addresses are **never** copied into logs or external output; the RunLog stores counts and message-ids, not content.
- **No auto-send, ever:** drafts only (the connector enforces it; Maxim's dry-run reinforces it).
- **No-fabrication:** it triages only what the connector returns; it never invents senders, deadlines, or "urgent" flags.
- **Confidence tag (ADR-010)** on the triage — 🟡 if the connector isn't connected (it'll tell you how to connect, not guess).

## The unattended "every morning" version

The same skill, wrapped by **`mxm-orchestrator`** (ADR-022) as a scheduled workflow: runs each morning via the `usage-aware-scheduler`, **dry-run by default**, bounded by a budget guard, idempotent (won't re-draft the same thread), and **draft-only** end to end. Definition: `orchestrator/workflows/inbox-triage.mjs`. Go-live requires a connected email tool + explicit operator approval (`/mxm-workflow go-live inbox-triage`). For headless/scheduled runs, use a **user-scoped** Gmail MCP (interactive Desktop connectors assume the app is open).

## Output

A triage digest — `reply-now` (with drafts ready) · `reply-later` · `ignore` — counts + the 1–2 that matter most. Nothing sent.
