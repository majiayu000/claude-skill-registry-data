---
name: evaluate-tech
description: Structured evaluation before adopting a library, tool, or hosted service — enumerate candidates wide, then score every one against an identical rubric where maintenance health is a mandatory gate, not an afterthought. Use when the user asks "which library/package should I use", "what should we use for X", "which service/vendor should we pick", "is this package still maintained", "alternatives to X", "should we add this dependency", "should we switch to X", "pick a tool/service for", "evaluate this dependency/tool/service", or is choosing between named options to adopt. Covers code dependencies (npm, pip, pub, cargo, go), CLI/dev tools and dev software, and SaaS/API/hosted services. For learning how to USE something already chosen, or for open-ended technical research, use research-tech instead.
argument-hint: <what you need> [| candidate, candidate, ...]
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Evaluate Tech

Adopting a library, tool, or service is a decision you live with, not a lookup. This skill enforces the two things ad-hoc evaluation reliably skips:

1. **Maintenance health is checked for every candidate, upfront** — never discovered later because someone thought to ask. A recommendation that flips the moment "is it maintained?" comes up was never a recommendation.
2. **Your current implementation is not a constraint on the search.** Requirements get triaged into hard (eliminates) and soft (costs money). Anchoring on how the code happens to be written today is the main way good options get silently dropped.

Applies to code dependencies, CLI/dev tools, and hosted services. The process is identical; only the criteria block differs.

Not for learning how to use something already decided on, or open-ended research — that is `research-tech`.

## Workflow

### Step 1: State the job, without naming anything

One sentence: *"We need something that ⟨capability⟩ so that ⟨outcome⟩."*

No product names, no API shapes, no "like X but". If the request arrived as "should we use Zod?", reverse-engineer the job first — the answer changes when the job turns out to be "validate API responses at the boundary" rather than "validate everything everywhere".

Then check what is already there: grep the manifest (`package.json`, `pubspec.yaml`, `pyproject.toml`, `Cargo.toml`, `go.mod`) and the lockfile. An existing dependency that already covers the job is the cheapest candidate and is routinely missed.

### Step 2: Triage constraints — hard vs. soft

The anti-anchoring step. Do this explicitly and show the user the table.

| | Definition | Effect |
|---|---|---|
| **Hard** | Breaks or cannot ship if violated: language/runtime, target platforms, license policy, deployment environment, actual compliance requirements, offline operation | Eliminates candidates |
| **Soft** | How the code happens to be written today: current architecture and patterns, existing wrappers and abstractions, current data shapes, state-management choice, team familiarity, "this is how we do it here" | Becomes an integration-cost line. **Never eliminates.** |

**The test:** state what concretely breaks if it is violated. If the answer is "we'd have to change some code", it is soft. If it is "it does not run on our runtime", it is hard.

Common mislabels worth catching: "it has to work with our Redux store" (soft — an adapter, or the candidate brings its own store), "it must be a React hook" (soft — wrap it), "we need TypeScript types" (usually soft — types can be written), "it must be free" (often soft — price it and let the user decide).

React/Flutter/Node *is* hard. "The way we currently use React" is not.

Read the conversation and relevant project docs before treating missing context as a
decision. If an unresolved choice about the job, priorities, or acceptable tradeoffs
would change the candidate pool or ranking, invoke `blind-spots` on that evaluation
brief before enumerating candidates. Supply the recon and hard/soft lists; keep
candidate capabilities and costs as research questions.

Use its returned brief to update the job and constraints. Confirm any inferred hard
constraints in this same scoping exchange; reuse decisions already explicit in the
request, docs, or a parent workflow. A settled brief proceeds directly to Step 3,
without another interview or confirmation.

### Step 3: Enumerate wide — do not evaluate yet

Target **5-8 candidates** before any filtering — a floor, not a stopping condition. Resist narrowing early; the point of this step is coverage.

**Run at least two independent modalities, one of which must be faceted registry search.** Prose search alone reliably misses tools whose name is short or generic and whose pitch is written in capability terms rather than product terms. The miss is silent: the field still comes back looking full.

| Modality | How |
|---|---|
| **Faceted registry** (required) | `gh search repos "<term>" --topic <ecosystem-topic> --sort stars`; npm/PyPI/crates category browse. Facets surface what prose ranking buries. |
| Prose / web search | Capability phrasing, then again in a competitor's sales vocabulary |
| Curated lists | `awesome-*` and ecosystem directories — **if one appears in your results, open it**; it is a field someone else already enumerated by hand |
| Incumbent-relative | "alternatives to ⟨incumbent⟩"; the incumbent's own README "similar projects" section |
| Dependency-relative | What comparable projects depend on; the framework's own docs, where a first-party option often hides |

`research-tech` in Product/Market mode if the space is unfamiliar. Pass nested research the settled brief and a focused factual question.

**Write queries from the capability, not from your implementation.** Queries built out of the harnesses, formats, or APIs the current code handles return tools that describe themselves the way the current code does — the Step 2 anchoring failure, relocated into the search box where nothing checks for it.

Always include these, explicitly, even if they lose:

- **The platform primitive** — stdlib, browser API, or framework built-in. `Intl.DateTimeFormat` beats a date library more often than people expect.
- **Build it ourselves** — with a rough size estimate. Sometimes the honest answer for 80 lines of logic.
- **Do nothing / defer** — is this needed now?
- **At least one candidate that violates a soft constraint.** If every candidate fits current architecture perfectly, the search was anchored. Go back to Step 3.

**Before leaving this step, answer one question in writing:** *which modality I ran would have found a tool with a short generic name and no product terms in its description?* If the honest answer is "none of them", enumeration is not finished, whatever the candidate count says.

List candidates with a one-liner each. Do not research them yet — mixing enumeration with evaluation causes early anchoring on the first plausible option.

### Step 4: Hard filter

Eliminate **only** on hard constraints, recording the specific constraint for each. If more than 6 survive, shortlist to 5 and state which were dropped and on what basis — the user may object, which is the point of saying it out loud.

### Step 5: Evaluate in parallel — identical rubric

Dispatch one sub-agent per surviving candidate, launching each batch together as runtime capacity allows. Use the template in `references/agent-prompt.md`, filling its placeholders with the settled job, constraints, and priorities while keeping the evaluation rubric identical. Workers return newly discovered scope blockers to you; they do not interview the user themselves.

**Dispatch workers with read/search/fetch tools and no file edits.** Each returns a scored evaluation. Disable delegation tools for ordinary workers where supported; read-only access alone does not prevent delegation. If a candidate needs coordinated research, assign its subtasks, descendant count, and stopping condition explicitly and include them in the overall allocation.

**Send every agent the same evaluation criteria.** The coordination assignment may differ, but do not add candidate-specific hints ("check whether this one's commits are bot-authored", "this package had a maintainership change"). It feels helpful and it silently corrupts the comparison: the candidate you hinted at gets a check its rivals never got, so a difference in the results may just be a difference in the prompts. If a check is worth doing for one candidate, it is worth doing for all — put it in `references/criteria.md`, where every agent reads it.

**Screen inline before dispatching — never with agents.** A full evaluation costs roughly 80-90k tokens; a screening *agent* still costs 15-25k, so fanning out screeners only pays if it eliminates more than about a third of the field. It usually doesn't, and then it costs more than it saves. Run the screen yourself in one batched command instead — a few thousand tokens for the whole field:

```bash
for r in owner/repo1 owner/repo2 …; do
  gh repo view "$r" --json pushedAt,isArchived,licenseInfo
  gh api "repos/$r/stats/participation" --jq '.all | add'   # commits, 52wk
done
```

Drop anything archived, license-incompatible, or clearly `UNMAINTAINED` (no push in 18+ months **and** zero commits) before spending an agent on it. Keep this output — Step 6 needs it as the independent baseline for cross-checking agent claims, so it is not extra work either way.

Do **not** eliminate on a low commit count here. This screen cannot see the bot-vs-human split, and a bot-dominated repo looks *healthy* by raw count — that call needs an agent.

Pick one profile for the whole comparison:

| Profile | Use for |
|---------|---------|
| **Library** | Code deps — npm, pip, pub, cargo, go, gem |
| **Tool** | CLI and dev software — linters, bundlers, migration tools, local binaries |
| **Service** | SaaS, APIs, hosted platforms, anything with a bill and an account |

Full rubric in `references/criteria.md`: core C1-C8 (maintenance · adoption · fit · integration cost · license · security · exit cost · docs) plus the profile block.

Do not skip agents for candidates you expect to lose. The comparison is only worth something if every cell was filled by the same rubric.

### Step 6: Cross-check

Before writing the recommendation:

- **Re-verify every maintenance verdict** that decides the outcome against the Step 5 screen output you already have. If the winner is winning partly because a rival looked stale, confirm that rival's dates yourself. Agents hallucinate release dates. A mismatch between an agent's figure and the screen means re-dispatch that candidate, not split the difference.
- **Recency of the evidence itself** — a comparison blog from 2023 describes a world that may no longer exist.
- **Adversarial pass**: what makes the top pick wrong in 12 months? Single maintainer? Vendor-owned with a CLA? Pinned to a framework version about to move? Losing downloads?
- **Anchoring audit**: did any candidate get marked down for something that is really a soft constraint? Re-read Step 2's soft list against every C4.

### Step 7: Recommend

Present in the conversation. Do not write files unless asked.

**Matrix** — candidates as rows, criteria as columns, ✅ / ⚠️ / ❌ per cell, with the maintenance column carrying its actual date:

```
| Candidate | Maint.                          | Adopt. | Fit | Integr. | License | Exit |
|-----------|---------------------------------|--------|-----|---------|---------|------|
| foo       | ✅ 2026-06 (1mo), 70 commits    | ✅ ↗   | ✅  | ⚠️ 6 files | ✅ MIT | ✅ low |
| bar       | ⚠️ 2026-05 (2mo), 81 but 74 bot | ✅ ↗   | ⚠️  | ✅ drop-in | ✅ MIT | ✅ low |
| baz       | ❌ 2023-02 (41mo), 0 commits    | ⚠️ ↘   | ✅  | ✅ drop-in | ✅ MIT | ✅ low |
```

The maintenance cell carries a date *and* a substance figure. "2026-05 (2mo)" alone would rank `bar` above `baz` and near `foo`, which is exactly the error the rubric exists to prevent.

Then, briefly:

- **Recommendation** with the two or three facts that actually decided it
- **Runner-up**, and the condition under which it wins instead
- **Soft constraints this asks you to change** — listed plainly, with cost. The user gets to weigh them; they were deliberately kept out of the filtering.
- **What would change this answer** — the concrete future event (maintainer walks away, license changes, v2 ships) worth watching
- **Ruled out**, one line each

State confidence, and name anything that stayed unknown. "Could not determine whether the export API includes historical data" is a finding, not a gap to paper over.

## Examples

**1. Anchored request corrected.** User: *"which React date picker should we use?"* → Job: "let users pick a date range on the booking form". Hard: React 18, RN Web, WCAG AA. Soft: "must accept our `{start, end}` shape" (an adapter), "must be styled with our Tailwind tokens" (headless candidates qualify). Wide list includes `<input type="date">` and a headless library. Result: two candidates that would have been cut for "wrong prop shape" survive to evaluation, and one wins.

**2. The failure this exists to prevent** (real run, 2026-07). User: *"CSV parsing for a Node backend"* → six candidates, C1 first. The one with the **highest commit count in the set** turned out to be 74/87 `renovate[bot]` with zero functional parser changes in 30 months and a 4.5-year median open-issue age. The **most-downloaded** one (54M/month, growing 3x) silently corrupted UTF-8 at chunk boundaries and discarded parse errors in the streaming path. In four of six cases the naive signal — recent release, high commit count, download growth — pointed the wrong way. All of them were ranked in the matrix on evidence rather than recommended and then retracted.

**3. Service.** User: *"what should we use for error tracking?"* → Service profile. Candidates include Sentry (self-host escape hatch), a competitor, and the platform's built-in logging. C5 surfaces Sentry's BUSL relicense history; C7 asks whether historical events can be exported; pricing computed at current and 10x volume.

**4. Correctly out of scope.** *"how do I configure Zod discriminated unions?"* → no decision to make. Use `research-tech`.

## Troubleshooting

**Every candidate looks maintained** — Release cadence is the easiest signal to fake and the least informative. `criteria.md` C1 makes the real checks mandatory: is anyone *changing the code* (commit substance, not commit count), does anyone *answer users* (maintainer comments in the last 12 months), do fixes *land* (open-PR backlog vs. merged), and is the current major quietly in maintenance-only mode while work happens on a v-next branch. A repo can ship a release every quarter with a bot writing 90% of its commits.

**Cannot determine last release** — No GitHub releases does not mean no releases; check the registry (`references/criteria.md` has per-ecosystem commands) and tags. If neither resolves, mark UNKNOWN — never assume current.

**An agent returns an unusable or empty report** — Re-dispatch that one candidate. Do not fill the gap from memory; training data is exactly the stale source this rubric exists to route around.

**The field looks complete and the recommendation still gets blindsided** — a candidate arrives from outside the process and beats everything scored. The cause is almost always Step 3 run in a single modality: rigor downstream of thin enumeration produces confident, well-evidenced, incomplete answers, which are worse than obviously thin ones because they do not invite challenge. Re-run Step 3 under the two-modality rule before re-scoring anything; the per-candidate work already done stays valid.

**Candidates are not comparable** — They solve different-sized problems. Return to Step 1: the job statement was too loose. Re-scope and re-enumerate.

**The user pushes back on a hard constraint** — They are usually right; they know the system. Move it to soft, re-run Step 4, and note that the candidate pool changed.
