---
name: agent-context-audit
description: >
  Audit a repo's agent context — CLAUDE.md files, codebase docs, skills, and
  tool/MCP designs — against Anthropic's Claude 5 context-engineering guidance
  ("unhobbling": Anthropic cut ~80% of Claude Code's system prompt with no eval
  loss). Finds overconstraint, conflicting instructions, redundancy, stale
  facts, and missing "unknown knowns"; produces a scored findings report with
  concrete rewrites, then applies approved fixes. Use when someone says "audit
  my CLAUDE.md", "context audit", "unhobble this repo", "review our agent
  docs/skills/tools", or after upgrading to Claude 5-generation models.
user_invocable: true
---

# agent-context-audit — unhobble this repo's agent context

Goal: find where this repo's context (CLAUDE.md, docs, skills, tool designs)
**hobbles** a Claude 5-generation model — overconstrains it, contradicts itself,
repeats itself, or hides context the model actually needs — and leave behind a
findings report plus approved fixes.

Background: Anthropic removed over 80% of Claude Code's system prompt for
Claude 5 models with **no measurable loss** on coding evals. Older context was
written for models that needed rules; newer models need judgment, good
interfaces, and the facts they can't infer. This skill audits against that
shift, plus the "finding your unknowns" framework (the gap between the *map* —
your prompts/docs — and the *territory* — the actual codebase).

You are **auditing first, fixing second**. Do not edit anything until Step 4.

## The six shifts (the audit rubric)

Every finding maps to one of these. Cite the shift number in the report.

1. **Rules → Judgment.** Hard rules ("NEVER…", "ALWAYS…", "do not add
   comments", "one-line docstrings max") that encode a *preference*, not a real
   constraint, should become judgment framing ("write code that reads like the
   surrounding code") — or be deleted if the model would infer it anyway.
   Keep hard rules only where violation is genuinely costly (security, prod
   data, irreversible actions, legal/billing).
2. **Examples → Interface design.** Long tool-usage examples and few-shot
   transcripts constrain exploration. Prefer expressive interfaces: good
   parameter names, enums that hint at valid states, tight descriptions.
   In tool/MCP definitions, an enum of `pending | in_progress | completed`
   teaches more than three worked examples.
3. **Upfront context → Progressive disclosure.** Anything long that's only
   sometimes needed (review checklists, deploy runbooks, style deep-dives)
   should move out of CLAUDE.md into a skill or linked file loaded on demand.
   CLAUDE.md is loaded *every* session — it should carry only what every
   session needs.
4. **Repetition → Concise, single-home instructions.** The same instruction
   appearing in CLAUDE.md *and* a skill *and* a tool description is a bug:
   copies drift and eventually conflict. Each instruction gets exactly one
   home — tool-usage guidance lives in the tool description, repo gotchas in
   CLAUDE.md, team opinions in skills.
5. **Manual memory → Automatic memory.** Sections telling the agent to
   hand-maintain notes/changelogs in CLAUDE.md, or accumulated session-specific
   trivia, are obsolete where auto-memory exists. Flag CLAUDE.md content that
   is really *memory* (per-user, per-incident, time-bound) rather than
   *repo truth*.
6. **Simple specs → Rich references.** Where docs describe behavior in loose
   prose, prefer pointing at the real thing: `@`-referenced source files, a
   test suite, an HTML mockup, a rubric a verifier can score against. Code-based
   specs beat prose paraphrases of code.

Cross-cutting failure modes to hunt alongside the shifts:
- **Conflicts** — instructions that clash across layers (e.g. "document
  thoroughly" in one file, "DO NOT add comments" in another). Highest-value
  findings; a conflict forces the model to deliberate or guess on every task.
- **Staleness (map ≠ territory)** — docs naming files, commands, flags, or
  services that no longer exist, or missing ones that now do. Verify every
  concrete claim you audit against the actual repo.
- **Missing unknown-knowns** — things obvious to the team but written nowhere:
  the non-obvious build step, the directory you must never touch, the reason a
  weird pattern exists. These are what CLAUDE.md is *for* ("repository
  gotchas rather than obvious patterns").

## Step 0 — Inventory the context surface

Collect everything that gets assembled into an agent's context here. Look for
the capability, not a specific filename:

- **CLAUDE.md files** — root, nested per-directory, `~/.claude/CLAUDE.md` only
  if the user asks for a global audit. Also `AGENTS.md`, `.cursorrules`,
  `.github/copilot-instructions.md` if present (same disease, same cure).
- **Skills** — `.claude/skills/**/SKILL.md`, `skills/**/SKILL.md`, plugin
  skills committed to the repo.
- **Tool designs** — MCP server definitions the repo owns (tool names,
  descriptions, parameter schemas), custom slash commands, hooks, and any
  agent definitions (`.claude/agents/*.md`).
- **Codebase docs agents are pointed at** — README, CONTRIBUTING, docs/
  referenced from CLAUDE.md or skills.

Record rough sizes (lines/tokens) per artifact — total always-loaded weight is
itself a finding when large.

## Step 1 — Audit each artifact against the rubric

For each artifact, walk the six shifts and cross-cutting modes. For every
finding record: **file:line, quote, shift #, severity, proposed rewrite**
(the actual replacement text — or "delete", with one line of why it's safe).

Severity:
- **high** — conflicts between layers; rules that block correct behavior;
  stale facts an agent would act on.
- **medium** — overconstraint, redundancy, always-loaded bulk that belongs in
  a skill.
- **low** — style, phrasing, minor bloat.

Verify before you flag: a claim of staleness must be checked against the repo
(does that script exist? does that command run?); a claim of redundancy must
cite both locations.

## Step 2 — Probe for unknowns (the gaps docs don't show)

Auditing text only finds what's written. Now find what's missing:

- **Blind-spot pass:** skim the actual territory — build config, CI, scripts,
  the weirdest-looking directories — and list load-bearing facts that appear in
  no doc. Each is a candidate "unknown known" to add.
- **Knowledge quiz:** write 5–10 questions a fresh agent must answer to work
  here safely ("how do I run one test?", "what must never be committed?",
  "which service is the source of truth for X?"). Answer each *using only the
  audited docs*. Unanswerable questions = gaps; wrong answers = stale docs.
- **Git check:** `git log --oneline -20 -- <doc>` — a CLAUDE.md untouched for
  months in an active repo is presumptively stale; recent churny areas of the
  codebase with no doc coverage are presumptive gaps.

## Step 3 — Report

Deliver a findings report (markdown in the repo, e.g.
`docs/agent-context-audit-YYYY-MM-DD.md`, or just in the reply if the user prefers):

1. **Scorecard** — per artifact: size, finding counts by severity, one-line
   verdict (keep / trim / restructure / delete).
2. **Findings table** — file:line, quote, shift #, severity, proposed rewrite.
3. **Gaps** — missing unknown-knowns from Step 2, each with proposed text and
   the home it belongs in (CLAUDE.md vs skill vs tool description).
4. **Projected result** — estimated always-loaded context before → after.

Lead with the top 3–5 highest-value changes; don't bury a layer conflict under
twenty style nits.

## Step 4 — Apply (with approval)

Ask which findings to apply (all high, everything, or cherry-pick). Then:
- Make the edits exactly as proposed in the report.
- When moving content out of CLAUDE.md into a skill, create the skill and leave
  a one-line pointer behind.
- Keep each change reviewable — don't reflow or rewrite text you didn't flag.
- If `/doctor` is available in this Claude Code install, suggest the user also
  run it as a second opinion on CLAUDE.md/skill sizing.

## Anti-patterns for the auditor

- Deleting a hard rule that guards something genuinely irreversible — the
  point is removing *fake* constraints, not real ones.
- Flagging brevity as a problem — short, dense CLAUDE.md files are the goal.
- Rewriting voice/style wholesale — preserve the team's phrasing where content
  is sound.
- Reporting a finding without a concrete rewrite — every finding must be
  actionable as written.

Sources: Anthropic, "The new rules of context engineering for Claude 5
generation models" (claude.com/blog); "A field guide to Claude Fable: finding
your unknowns" (claude.com/blog).
