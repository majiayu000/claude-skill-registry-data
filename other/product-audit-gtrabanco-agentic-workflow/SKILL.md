---
name: product-audit
user-invocable: true
disable-model-invocation: true
version: 3.4.0
metadata:
  opencode/autoinvoke: false
argument-hint: <path-or-area> (optional — defaults to the whole product)
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Audit the whole product across code, quality, process, docs, roadmap, and
  tooling; it owns the repo-wide bug hunt, security research, and broken-version
  investigation (scoped and budgeted per dimension, as distinct from
  `review-change`'s change-scoped review). Persist one severity-ranked,
  F-numbered report with proposals; never fix or file work. Triggers:
  "product-audit", "audit the product", "full health check", "are we product-ready",
  "CTO review".
---

# Product Audit

Product-wide health check. It only writes
`docs/audits/<n>-<YYYY-MM-DD>.md`; every proposed action remains a user decision.

## Turn contract — verify before ending the turn

```
✓ The full PRODUCT AUDIT report was printed in the fixed output format (health by dimension, F-numbered ranked findings, four proposal streams — the roadmap streams always present, `none — <why>` when empty)
✓ The report was WRITTEN to `docs/audits/<n>-<YYYY-MM-DD>.md` (incremental audit id) and committed — the file is the durable deliverable, the chat print is a copy
✓ Nothing else was fixed, filed, or changed — the report file is the ONLY mutation
✓ The closing `→ Next:` block is printed as the ABSOLUTE last output
```

About to end the turn with any box unchecked? The turn is NOT done — complete
the missing box first (weak models drop end-of-document duties; this list is
first on purpose).

## When to use

- Periodically (every few features) or at a product-ready milestone.
- When you want the broad, honest picture — quality, security, debt, docs, and
  roadmap — not the review of a single change (`review-change`) or PR (`audit-pr`).
- **It owns the repo-wide sweep.** Open-ended, repository-wide bug hunting,
  security research and broken-version investigation land **here** — scoped,
  sampled and budgeted per dimension (state what you sampled). The same hunt
  against one change is `review-change`'s job: neither skill absorbs the other's
  scope.

Unlike diff, PR, or docs-only reviews, this skill covers the whole product.

## Scope

The entire codebase and its process artifacts: source, tests, the docs tree, the
roadmap, the fix index, open issues, and every feature folder's planning docs.
Accept an optional path/area to focus a partial audit; state the scope and, if you
sample rather than exhaust a dimension, **say what you sampled** — never imply full
coverage you didn't do.

> **Tip (provisional).** The *user* can turn on `ultracode` (a research-preview
> Claude Code session setting — no skill can declare it) so this sweep fans out
> across parallel subagents instead of one context window; without it, sweep the
> dimensions sequentially — only wall-clock changes, never coverage.

## Step 0 — Discover the project (always first)

Per the agent guide's **Workflow conventions** + **documentation map**, then read
what THIS skill needs: the roadmap, the fix index, the feature folder layout, and
the verification gate. From the map decide the product's nature (web / mobile /
console / library / backend / infra). Defer deciding which dimensions apply until
`AUDIT_DIMENSIONS.md` has been loaded; that resource is the authoritative
applicability matrix. Note any optional platform review skills the project
installed (extras, never requirements — the internal pack covers every axis).

## Progressive loading — audit route

The reference allowlist is exactly the two paths below. Load both after Step 0,
in order; they are normative and one hop from this entrypoint.

1. Read [audit dimensions](references/AUDIT_DIMENSIONS.md), mark every dimension
   applicable or `n-a: <reason>`, and state any sampling.
2. Read [audit process](references/AUDIT_PROCESS.md), execute all ten steps, then
   return the fixed report below.

A missing resource stops the audit; never reconstruct it from memory. Optional
platform review skills remain extras, never replacements for the internal pack.

## Output format

This exact structure is BOTH the persisted file (`docs/audits/<id>-<YYYY-MM-DD>.md`)
and the chat print — identical content, no free-form variations between runs.
Every section below appears in every audit; a section with nothing to report
states `none — <why>` instead of being omitted (the roadmap streams especially:
"always build the roadmap picture", never silently skip it).

```
# PRODUCT AUDIT <id> — <product> — <YYYY-MM-DD>
Scope: <whole product | area>
Coverage: <dimensions run | sampled vs. exhaustive>
Verdict: <one-line honest health verdict>

## Health by dimension
  <dimension> .......... ✓ healthy | ⚠ concerns | ✗ at risk | n-a (why)
  ...
  Installed tooling ....... ✓ | ⚠ | ✗ | n-a

## Findings (severity-ranked, one F-sequence for the whole audit)
  F1 [SEV] <dimension> — <finding> — evidence: <file:line | metric | doc> — class: <fix-now|replan-in-unit|decision-required|proposal|ignore>
  F2 [SEV] ...
  [example — scope-export recurrence] F<k> [med] Workflow discipline — <N>
    consecutive units exported scope via `## Amendments`/descope issues —
    features are being cut too big for real capacity — evidence: <unit list +
    amendments/issues> — class: proposal — route: #64 (atomicity/split rules)

## Delta vs audit <prior-id>
  New: F<k>
  Unchanged: F<k> <- audit <prior-id> F<j>
  Resolved: <prior-id> F<j>
  (none — <why no equivalent-scope prior exists>)

## Proposals — the user decides which to act on

### Issues to open
  - <title> [sev] — from: F<k>[, F<j>] — <why> — route: /triage-issue <id> F<k> — evidence: <…>
  (none — <why>)

### Roadmap — add
  - <feature> — from: F<k> — <rationale & opportunity> — route: /unit-lane --from-issue <n>
  (none — <why>)

### Roadmap — remove / revise
  - <feature> — from: F<k> — <why it no longer fits> — route: triage-issue / roadmap edit
  (none — <why>)

### Tooling — register / re-design
  - <skill|MCP> — register in AGENTS.md (Optional review extras): <why> — route: user edits AGENTS.md
  - <skill|MCP> — would change <feature> scope: <why> — route: /unit-lane <slug>
  (none — <why>)

## Manual-verification checklist (what automation can't confirm)
  - <item> …

Finding set: F<k> + F<j> + F<m> (print every proposed finding; one finding → F<k>)
→ Next: /triage-issue <id> F<k> F<j> F<m> — classify the complete finding set in one batch (opens the ones that warrant it)
  · accepted bug/debt → /unit-lane --fix <n>   · accepted capability → /unit-lane --from-issue <n>
  · nothing to act on → the persisted report is the record; move on
```

Replace every finding placeholder with the complete actual set before printing;
never print `…` or only the first finding in a live hand-off.

`<id>` is the audit's incremental number (Process step 9). A finding is
addressable forever as `<audit-id> F<k>` — e.g. `triage-issue 3 F2` reads
`docs/audits/3-*.md`, locates F2, and opens/classifies the issue if warranted.
Suggest that routing; **never run triage or open issues here**.

Lead with the honest one-line health verdict (e.g. "shippable with 2 high-sev
security items to track first").

## Guardrails

- **Never auto-fixes, never opens issues, never edits the roadmap.** Output is a
  report + proposals; **every action is the user's decision.** The one file this
  skill writes is its own report under `docs/audits/` (plus `mkdir -p
  docs/audits`) — nothing else in the repo is touched.
- **Finding ids are `F1, F2, …` only** — one sequence per audit, severity-ranked
  order, never a different letter per problem type. Once persisted, ids are
  frozen: a later audit gets a new audit id, never renumbers an old file; cross-audit
  lineage lives only in Delta mappings as `<audit-id> F<k>`, never global slugs or
  replaced ids. When the user accepts, route: `triage-issue` files/classifies, `/unit-lane`
  adds roadmap work or scopes a concrete fix.
- **Never registers tooling or edits `AGENTS.md`.** The tooling sweep proposes a
  skill/MCP to register, but the user (or a routed `/unit-lane <slug>` run)
  performs the edit; a scope-affecting discovery routes to
  `/unit-lane <slug>`, which the user approves.
- Platform-adaptive: run only applicable axes; always list what you skipped and why.
- **No silent caps.** If you sampled, prioritized, or time-boxed a dimension, say
  so — never present partial coverage as exhaustive.
- Severity-ranked and deduped: cluster the same issue found via multiple axes or
  multiple feature docs into one proposal.
- Honor the project's **Workflow conventions** (docs-language, evidence): every
  finding/proposal cites a `file:line`/metric/doc/issue source; mark uncertainties *verify*.
- **Evidence also passes the fixed evidence-provenance gate** in
  `references/AUDIT_PROCESS.md`; uncertainties stay marked *verify*.

## Portability (agents other than Claude Code)

The workflow is the contract; Claude Code features are conveniences. On an
agent that lacks one, apply the fallback — never skip the step the feature
enables:

- **No slash-command menu** — where this skill says `/<skill>`, open that
  skill's `SKILL.md` (wherever your agent installed the skills) and follow it
  literally, in a fresh conversation: hand-offs assume a clean context.
- **No per-skill `model:`/`effort:`** — this is the widest, highest-stakes
  sweep in the workflow: run it on your **strongest** model at its deepest
  setting, as its own dedicated run — never squeezed into another task's
  context.
- **No `ultracode`/subagents** — sweep the dimensions sequentially (see the
  tip above); state coverage honestly either way.

## Relationship to other skills

```
product-audit (whole product, all axes, periodic)
   ├─ composes review-change axes (codebase-wide) + audit-docs (doc coherence)
   ├─ mines feature docs (decisions / known-issues / architecture-notes)
   ├─ sweeps installed skills / connected MCP servers (product-wide, periodic)
   └─ proposes ─┬─ Issues to open ........ ▶ triage-issue / unit-lane --fix
                ├─ Roadmap: add .......... ▶ unit-lane --from-issue
                ├─ Roadmap: remove/revise  ▶ triage-issue / roadmap edit   (user decides)
                └─ Tooling: register/re-design ▶ user edits AGENTS.md / unit-lane
```

- Broader than `review-change` (one change) and `audit-pr` (one PR); subsumes
  `audit-docs`'s coherence check as one of its dimensions.
- Hands nothing off automatically — it recommends, and the planning/fix/triage
  skills execute only when the user chooses to.

## Done when

- Every applicable dimension has a health verdict backed by cited evidence, and the
  skipped or sampled ones are stated.
- A severity-ranked, **F-numbered** findings list plus four proposal streams
  (issues to open, roadmap add, roadmap remove/revise, tooling
  register/re-design) exist — every stream present (`none — <why>` when empty),
  deduped, each proposal routed and citing its source findings.
- The report is **persisted and committed** as `docs/audits/<id>-<YYYY-MM-DD>.md`
  with the next incremental audit id, and printed in chat.
- Nothing else was fixed, filed, or changed — the user decides what to act on.
- The **closing `→ Next:` block is printed** — typically a batch
  `/triage-issue <id> F<k> …` for the proposed issues, then `/unit-lane` for the accepted work.
