---
name: document
description: >-
  Draft a technical document from an intent or a source. Triggers on "write the runbook / ADR /
  RCA / PR description / commit message / changelog / diagram / README / migration guide / API
  reference / experiment report / incident summary / onboarding doc / design doc". Markdown-first:
  produces a draft in a local file and NEVER publishes (no Confluence / Jira / Slack / GitHub
  posting — that is a separate concern). Reader-first voice: leads with the reader's question,
  cites every non-trivial claim to a repo path or quoted source, caps external quotes at 15 words,
  cuts filler. Audience-tuned (engineer / pm / exec / mixed) — the voice does not mix. GitHub
  context (PR / issue) is read via the gh CLI.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<intent-or-source> --type <artifact-type> [--audience engineer|pm|exec|mixed] [--write-to <path>] [-i|--interactive] [--deep]"
---

# document — draft a technical document (markdown-first)

Turns an intent or a source into a markdown draft engineers actually use. **Drafts to a local file. Never publishes.** Posting to Confluence / Jira / Slack / GitHub is a separate concern — this skill stops at a clean markdown file and tells you where it is.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you write (voice, citation rules, anti-patterns) | `persona.md` |
| The phased process + Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Per-artifact contract (lead-with / cap / must-include) | `types.md` |

## Quick start

1. **Resolve `--type`** against `types.md`. If the user didn't pass one, infer it from the intent ("write the runbook for…" → runbook) and **state the inference** in the output.
2. **Gather sources** (Phase 0 in `workflow.md`). GitHub PR/issue context is the `gh` CLI (`gh pr view <url> --json …`, `gh issue view <url> --json …`); repo facts come from Read / Grep / Glob; external links from WebFetch. For a doc that synthesizes multiple systems, fan out the `context-gatherer` agent.
3. **Read `persona.md`** and adopt the reader-first voice for the chosen `--audience` (default: engineer). The voice does not mix audiences — pick one.
4. **Draft** to `--write-to <path>` if given, else a sensible local path (`types.md` suggests one per artifact). Follow the type's lead-with / cap / must-include contract.
5. **Validate** (Phase 3): anti-pattern grep, citation check, length cap. Then report the draft path. Nothing is published.

## Workflow is the default for multi-source docs

"Always have a workflow." A doc that synthesizes more than one system — an RCA, an ADR weighing alternatives, a migration guide spanning two services — gets the Workflow in `workflow.md`: fan out `context-gatherer` + per-section drafting in parallel, stitch, then run a **completeness-critic** pass that asks "what's missing, what's uncited, what did we assert without evidence?" before the draft survives. A simple, single-source doc (a commit message, a one-screen README section) is drafted inline — say you skipped the Workflow.

## Modes

- **default** — gather, draft, validate, report the local draft path. Nothing is published.
- **`-i`** — confirm the type, audience, and outline with the user before drafting; walk the draft section-by-section.
- **`--deep`** — use a stronger reasoning profile; auto-select for RCAs, design docs, and anything synthesizing 3+ sources.
- **`--write-to <path>`** — write the draft to a canonical repo path (e.g. `docs/adr/0007-x.md`) instead of a scratch path. Still a draft; still not published.
