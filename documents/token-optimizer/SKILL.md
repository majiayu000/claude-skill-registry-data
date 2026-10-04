---
model_tier: medium
name: token-optimizer
description: "Use BEFORE any verbose CLI run, large file read, doc conversion, or near-context handoff — decision tree keyed by intent citing the canonical token-saving asset."
domain: process
scope:
  write: []
  verification_reason: "an index-and-routing skill — it names other artefacts to load and writes nothing. Absence of a write is not something a command can prove."
execution:
  type: assisted
  handler: shell
  allowed_tools: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# Token Optimizer — decision tree + catalog

## Iron Law

```
CONSULT THIS SKILL BEFORE THE ACTION, NOT AFTER.
THE TREE NAMES THE CANONICAL ASSET — DO NOT RESTATE OR DUPLICATE IT.
```

## When to use

Proactively, BEFORE you:

- Run a verbose CLI command (tests, linters, build, git log, large `grep`)
- Read or paste a large document, log, or tool dump
- Repeat the same tool call across many files / records
- Approach the context-window limit and need to hand off
- Make a cost-aware decision (which model, which budget, when to stop)

Reactively when output already burned tokens — record the lesson, do
not re-explore. Cite the leaf, move on.

## Procedure

1. **Classify intent** — match the situation to one branch of the tree below.
2. **Cite the leaf** — name the canonical asset (rule, skill, or upstream link).
3. **Apply** — execute the cited asset's contract; do NOT inline its content.
4. **Verify** — output respects the cited Iron Law (redirect, wrap, batch, etc.).

### Decision tree

```
INTENT
├── Verbose CLI output incoming
│     → cite [cli-output-handling](../../rules/cli-output-handling.md)
│       (Iron Law: redirect / tail / grep / wrap)
│     → cite [rtk-output-filtering](../rtk-output-filtering/SKILL.md)
│       (rtk wrapper — upstream reports 60-90% on tests/linters/git)
│
├── Large document or paste (PDF, DOCX, HTML, transcript)
│     → cite markitdown (upstream: https://github.com/microsoft/markitdown)
│       Convert FIRST, then read the markdown — never paste raw binary.
│
├── Large file read (source / data / log already in the tree, > 800 lines)
│     → cite [token-efficiency § Size-gated reads](../../rules/token-efficiency.md)
│       (size → structural grep → bounded slice; never a full read on spec)
│
├── Repeated tool-call across N targets
│     → cite [token-efficiency](../../rules/token-efficiency.md)
│       (batch, parallelize, prune; one tool call > many)
│
├── Near context limit, work not finished
│     → cite [agent-handoff](../../domains/meta/agent-handoff/command.md)
│       (session picker + generated handoff; auto-seeds the fresh chat)
│
├── Cost-aware decision (model pick, budget, stop-criterion)
│     → cite /cost:report (when shipped) — until then, fall back to
│       [token-efficiency](../../rules/token-efficiency.md) and
│       [direct-answers § Brevity by Default](../../rules/direct-answers.md)
│
└── API-bill lever (stable prefix reused across calls · non-interactive
    bulk cohort · model/effort pick against the paid Anthropic bill)
      → cite [api-cost-levers](../../../docs/guidelines/agent-infra/api-cost-levers.md)
        (prompt caching ~0.1x reads · Batch -50% · model tiering · effort)
```

## Catalog

| Asset | Path | Trigger keywords | What it does |
|---|---|---|---|
| `cli-output-handling` | `src/rules/cli-output-handling.md` | `verbose`, `tail`, `grep`, `CLI` | Wrap-tail-grep contract for any verbose command |
| `rtk-output-filtering` | `src/skills/rtk-output-filtering/SKILL.md` | `rtk`, `verbose`, `filter`, `wrap` | Project-local rtk filters; wrapper command |
| `token-efficiency` | `src/rules/token-efficiency.md` | `redirect`, `verbose`, `concise`, `tool`, `large file` | Batch + parallelize tool calls; brevity floor; size-gated reads (probe → grep → slice above 800 lines) |
| `agent-handoff` | `src/domains/meta/agent-handoff/command.md` | `handoff`, `fresh`, `chat`, `context`, `resume`, `session` | Session picker + generated handoff auto-seeding the next session |
| `direct-answers` | `src/rules/direct-answers.md` | `brevity`, `flattery`, `severity`, `tiered` | Iron-Law brevity floor (kernel) |
| `markitdown` | upstream: github.com/microsoft/markitdown | `PDF`, `DOCX`, `HTML`, `convert` | Document → markdown converter (authoritative-link only) |
| `/cost:report` | TBD — an internal roadmap (local-only) § P1.2` | `cost`, `model spend`, `budget` | Per-session cost telemetry (planned) |
| `api-cost-levers` | `docs/guidelines/agent-infra/api-cost-levers.md` | `cache`, `caching`, `batch`, `tiering`, `effort` | Anthropic billing levers: prompt caching, Batch API, model tiering, effort/output right-sizing |

## Output format

1. Name the cited asset by its leaf id (e.g. `cli-output-handling`, `rtk-output-filtering`).
2. State the Iron Law in one line; do NOT inline the asset's body.
3. If multiple branches match, cite all relevant leaves (no merge, no rewrite).
4. End with the action you take next, citing the asset that authorizes it.

## Gotcha

- Catalog rows live and die with their target asset. If you edit a
  cited asset's trigger keywords or scope, update the matching row in
  this skill in the same commit (enforced by
  [`token-optimizer-maintenance`](../../rules/token-optimizer-maintenance.md)
  rule + `scripts/check_token_optimizer_freshness.ts` CI gate).
- Tree must stay scannable (≤ 50 lines incl. labels). Catalog rows
  carry the long form.
- Authoritative-link assets (`rtk` upstream, `markitdown` upstream,
  pricing constants) are never copied — always linked.

## Do NOT

- Do NOT inline content from a cited asset. If the leaf is "rtk does X",
  the agent reads `rtk-output-filtering`. Duplication = drift = stale.
- Do NOT replace any rule. The rules carry the Iron Laws; this skill
  carries the lookup index.
- Do NOT define new policies — every leaf must cite an existing rule,
  skill, or upstream asset.
- Do NOT consult this skill AFTER tokens were already burned — record
  the lesson and move on.

<!-- TELEMETRY: consulted=[uncomment + ISO timestamp on each consult] context=[CLI|doc|repeat|handoff|cost] -->
