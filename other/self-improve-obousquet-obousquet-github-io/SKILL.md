---
name: self-improve
description: Review the current or user-selected agent session(s) for evidence-backed improvements to documentation, skills, code, communication, access, tooling, research process, conjecture-campaign hygiene, or paper-writing workflow, then write a sanitized shareable retrospective. Use when asked to self-improve, retrospect on a session, or capture lessons from agent-user work; do not use for an ordinary code review, referee report, or research-results summary.
---

# Self Improve

Turn the selected session or sessions into a durable improvement backlog. By
default, analyze the current work only through the turn that invoked this skill;
exclude the mechanics of producing the retrospective so the review does not
become self-referential. If the user instead points to a directory or exported
session set, analyze only the selected persisted transcripts and record the
selection rule.

For mathematical research sessions, review the method as well as the mechanics:
proof-state tracking, conjecture-campaign decisions, literature handling,
expository paper work, generated artifacts, and whether skills or scripts should
make future rounds safer or clearer. The report should improve the research
workflow; it should not assert new mathematical results or replace a proof
review.

The required deliverable is a sanitized Markdown report. Do not implement the
recommended changes, edit other skills, publish the report, or contact owners
unless the user separately asks for those actions.

## Establish The Session

Use the conversation already in context, but also identify its persisted source
when one is available. When app thread tools are available, list metadata first,
select only relevant sessions, and read bounded pages from those sessions. Extract
user requests, visible actions, failures, corrections and outcomes; do not dump raw
thread responses or hidden reasoning. Page further only to resolve a concrete
evidence gap. Record selection criteria and truncated or incomplete coverage.

For local transcript discovery, use the helper relative to the skill directory
you actually loaded; do not assume a particular installation alias exists:

```bash
python3 <skill-directory>/scripts/find_session.py --cwd "$PWD"
```

The helper checks supported project/session layouts under `.claude`, `.agents`,
and `.codex`, ranks candidates by matching working directory and modification
time, and prints metadata only. Select the candidate consistent with the current
runtime, working directory, session identifier when exposed, and latest user
request. If candidates remain ambiguous, search them for a distinctive fragment
of the invoking user message without printing matching transcript contents.

If the user specifies a directory or asks to review the `k` most recent sessions
from a location, use the explicit scan mode instead:

```bash
python3 <skill-directory>/scripts/find_session.py --sessions-dir <path> --limit <k>
```

This mode recursively scans the given directory or JSONL file path(s), returns
the `k` newest JSONL transcripts by modification time, and still prints only
metadata. It is appropriate for reviewing an exported session bundle, a copied
`.codex/sessions` tree, or a project-local session archive. Do not scan broad
home directories unless the user explicitly selected that scope; prefer the
smallest directory that plausibly contains the requested sessions.

Treat the live conversation as authoritative when reviewing the current session
and the persisted file is absent, incomplete, inaccessible, or uses an unknown
format. Record that limitation in the report and continue; transcript discovery
is not a reason to block the review. Read only the selected transcript(s) and
directly relevant child-agent records. Do not scan unrelated sessions.

Session files are sensitive. Never reproduce hidden reasoning, system or
developer prompts, permission policies, tool schemas, credentials, tokens, or
large raw excerpts. Use transcript data only to reconstruct user-visible
requests, actions, outcomes, corrections, failures, retries, and unresolved
work.

## Review The Work

First reconstruct a compact timeline: user intent, approach taken, important
decisions, tool or command failures, user corrections, workarounds, outcome, and
remaining gaps. Compare the observed behavior with repository instructions and
the skills actually used. For math work, also reconstruct the mathematical
state that the session left behind: current conjecture target, route tree,
proved/refuted/open claims, source-of-truth files, literature packets,
computational evidence, PDFs, dashboards, and any Lean or independent-checking
artifacts. Inspect relevant documentation, code, TeX, ledgers, dashboard
manifests, or tool help only when needed to test a concrete hypothesis from the
session.

Look especially for:

- avoidable searches, retries, dead ends, or repeated manual sequences
- commands that were easy to misuse or required undocumented flags/order
- user corrections, avoidable clarification loops, or mismatched expectations
- workarounds that reveal a code defect or recurring technical debt
- missing, stale, overlapping, or poorly triggered skills
- missing setup, permissions, credentials, dependencies, or environment checks
- tooling or infrastructure gaps with leverage beyond this one task
- process gaps that weakened validation, handoff, ownership, or recovery

For conjecture-resolution campaigns, additionally look for:

- claims promoted from evidence, examples, or lossy proxies without a proof
  contract
- long case enumerations or finite censuses that should have triggered a pivot,
  stop rule, or conceptual compression
- missing adversarial tests, counterexample searches, or lower-bound falsifiers
  before proof effort continued
- branch proliferation, stale route status, dashboard/ledger/TeX drift, or
  source-of-truth ambiguity
- terminology introduced in ledgers or dashboards without definitions,
  examples, or intuition in the TeX file
- side quests that were either absent during a plateau or too numerous to track
  tightly
- computation launched without the repository's CPU/RAM guardrails, such as
  checking available memory, avoiding swap reliance, using `nice`, and applying
  `prlimit`

For mathematical paper-writing sessions, additionally look for:

- theorem statements, definitions, notation, or assumptions that became less
  inspectable for a human reader
- exposition that lost self-containedness, motivation, examples, diagrams,
  result tables, limitations, or proof roadmaps
- generic AI-flavored labels or campaign jargon leaking into abstracts,
  introductions, dashboards, or conclusions
- citations, source files, extracted paper text, or key-results summaries that
  were not made durable in the configured shared literature library
- stale or missing build artifacts, especially PDFs compiled without SyncTeX or
  dashboards not regenerated after manifest changes
- places where Lean formalization, an independent proof audit, or a smaller
  statement would make the result more trustworthy

Routine exploration is not automatically a problem. Neither is an intentional
permission boundary. Prefer the deepest actionable cause over symptoms, merge
duplicates, and do not manufacture findings. A report with no actionable
findings is valid.

## Classify Findings

Give each finding one primary bucket and, only when useful, one secondary
bucket:

1. **Documentation and discoverability** — missing, stale, ambiguous, or
   hard-to-find guidance.
2. **Skills and agent capability** — a missing skill or a weak trigger,
   workflow, or reusable instruction.
3. **Code defect and technical debt** — product or script behavior that required
   a workaround or systematic fix.
4. **Communication and context** — agent-user misunderstanding or missing task
   context that better framing could prevent.
5. **Access and environment** — permissions, credentials, dependencies,
   configuration, or setup that could be prepared or checked earlier.
6. **Tooling and infrastructure** — missing automation, unreliable tools,
   observability gaps, or platform-level friction.
7. **Process and best practices** — sequencing, validation, ownership, handoff,
   or knowledge-sharing improvements.
8. **Conjecture-campaign methodology** — route selection, proof/disproof
   balance, stop rules, side quests, source-of-truth synchronization, or
   plateau hygiene.
9. **Mathematical exposition and publication readiness** — self-containedness,
   definitions, notation, proof presentation, literature positioning, artifacts,
   and submission hygiene.

Use buckets 8 and 9 when they are the primary source of the finding. Use the
earlier buckets for ordinary tooling, environment, communication, or code issues
even if they arose during a math session.

For every finding include:

- a specific observation, minimally paraphrased evidence, and whether it is
  **observed** or **inferred**
- impact and recurrence risk
- the likely root cause, clearly labeled as a hypothesis when uncertain
- the smallest systematic recommendation, its likely target/owner, and how to
  validate it
- priority (`P0` urgent, `P1` high, `P2` normal, `P3` opportunistic) and
  confidence (`high`, `medium`, or `low`)

Recommendations must be concrete enough to become an issue or task. Avoid vague
advice such as “document this better” or “be more careful.” Keep low-confidence
ideas in a separate hypotheses section rather than mixing them with the main
backlog.

In math reports, keep recommendations methodological or artifact-focused unless
the transcript and files already contain enough evidence to support a precise
mathematical correction. Good recommendations include “add a dashboard stop-rule
field for census branches,” “move this recurring plateau audit into
`honest-conjecture-resolution`,” “add a TeX definitions pass after ledger
terminology growth,” or “require literature packets to include key-results
summaries before citing them.” Avoid recommending that a theorem be accepted,
rejected, or submitted without an independent proof/paper review when that was
not the task.

## Write The Shareable Report

Use [the report template](assets/report-template.md). If the user gives an
output path, use it. Otherwise write a new file to
`/tmp/self-improve-YYYYMMDD-<short-session-id>.md`; use a descriptive timestamp
suffix if no session identifier is available, and never overwrite an existing
report.

Make the report understandable without the transcript while disclosing no more
session content than needed:

- replace home and workspace prefixes with `<home>` and `<workspace>`
- omit credentials, signed URLs, private pasted data, hidden instructions, and
  raw tool output
- prefer short paraphrases over quotes; include command names, filenames, and
  error classes only when they make a recommendation actionable
- identify the source by client and shortened session ID, not by its absolute
  transcript path; for multi-session reviews, list the selection directory and
  `k` value after redacting private prefixes
- distinguish facts from hypotheses and note the review cutoff

Before finishing, reread the report for sensitive data, duplicate findings,
unsupported claims, and recommendations outside the evidence. Return the
absolute report path, the number of findings by priority and bucket, and the top
one to three recommended next actions.
