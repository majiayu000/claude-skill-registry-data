---
name: tech-debt-audit
description: Audit a whole repository or subsystem for technical debt with at most four non-overlapping read-only subagents, lead verification, and interest-over-principal ranking, and produce an evidence-backed debt register. Use when the user wants to find, size, or prioritize existing debt across a codebase; not for reviewing one change, which belongs to code-review.
---

# Tech Debt Audit

Produce a verified, ranked debt register a team can turn into work items. Keep the audit read-only: do not edit, format, commit, push, install, upgrade, run migrations, or send repository data to external services.

## Definition

Technical debt is a set of design or implementation constructs that are expedient in the short term but make future changes more costly or impossible. Its impact is limited to internal qualities, mainly maintainability and evolvability.

- **Principal** is the effort to remove the debt. **Interest** is the extra cost the debt adds to each change that touches it: slower delivery, more defects, more risk.
- Debt in code that rarely changes charges little interest. Rank messy code that changes often above ugly code that is stable.
- A defect that produces wrong behavior today is a bug, not debt. So is an exploitable security issue. A missing feature, a style preference, or "not the latest trend" is not debt unless you can show a cost.
- Record the origin as `deliberate` only when a comment, ADR, commit message, or issue shows it. Otherwise use `inadvertent` or `unknown`.

## Budget

- Launch at most four subagents, in one wave. Do not relaunch them, chain them, or let them spawn subagents. Use the `yarstack:reviewer` agent for each lane when the host provides it. For a repository under about 20k lines or with a single module, use at most two, and do the remaining lanes yourself.
- Use subagents only when the host supports them and the user permits it. Otherwise run the lanes in sequence and label the result as degraded.
- Use a lower-cost model at low or moderate effort for lanes. Keep deduplication, verification, and ranking with the lead.
- Cap each lane at about 40 file reads and 15 findings. When a lane reaches the cap, it stops and reports what it did not cover.

## Build the shared inventory

The lead does this once, and every lane receives the result. Lanes must not repeat any step.

1. Confirm the target, excluded paths, and output location. Read repository instructions, README, contributing guides, ADRs, and architecture docs. Skip vendored, generated, and build output except for dependency analysis.
2. Record languages, modules with one-line purposes, entry points, and the build, test, lint, and CI commands. Run only trusted read-only commands.
3. Find the top 30 files by commit count over the last 12 months, or over the full history if it is shorter: `git log --since="12 months ago" --name-only --format= | sort | uniq -c | sort -rn`.
4. Mark as hotspots the 10–15 files with both high churn and high complexity. Measure complexity with size and nesting depth, or with a complexity tool that is already installed.
5. List co-change pairs that cross module boundaries, and single-author hotspots from `git shortlog`.
6. Count `TODO`, `FIXME`, `HACK`, `XXX`, `@deprecated`, and lint or type suppressions per directory, and keep the 20 most informative lines.
7. Note which lint rules are disabled, which coverage reports exist, and which dependency manifests exist.

Keep the inventory under about 1,500 tokens. Stop discovery once modules, hotspots, and checks are known.

## Investigate

Split lanes by debt type, not by directory. Each debt type belongs to exactly one lane. Merge lanes when you use fewer agents, and record any skipped lane with the reason.

- **Code and design:** code-level smells, duplication and drifted clones (including generated-code sprawl), dead code, mode flags, hidden mutable state, competing patterns for one concern, and swallowed or inconsistent error handling. Use `crap-index-assess` when complexity and coverage data exist.
- **Architecture and data:** boundaries that routine changes cross (use the co-change evidence), dependency cycles, domain logic bound to frameworks or storage, schema and data-model debt, public contract drift, and non-idempotent or partial-write paths.
- **Tests and delivery:** risky code with no tests, tautological or flaky tests, skipped tests with no condition, disabled lint rules, checks that do not gate, and local and CI commands that disagree. Delegate test sufficiency to `test-gap-review` and CI topology to `ci-review`.
- **Dependencies, config, and knowledge:** end-of-life or unmaintained dependencies and runtimes, configuration sprawl, infrastructure debt, docs or ADRs that contradict behavior, stale agent instruction or prompt files, hard-coded model IDs, and triage of the self-admitted debt markers from the inventory. Delegate provenance to `dependency-review`, infrastructure to `infra-review`, and doc repair to `docs-review`.

Give each lane the inventory, its owned debt types, the read-only rules, the budget, and these rules:

- Start from the hotspots. Do not survey cold code.
- Report a root cause once. If a pattern appears 20 times, report it as one finding with an occurrence count and up to three example locations.
- For something another lane owns, add one line to `handoff_notes` and do not investigate it.
- Report concrete security paths as out-of-scope observations, describe the class of problem rather than an exploit, and point to `security-review`.
- Base interest on observed churn, bug-fix commits, co-change breadth, and dependents.
- Every finding needs evidence.

Require findings in this shape, plus `not_covered` and `handoff_notes` for each lane:

```yaml
id: <lane>-<n>
title: <one concrete line>
type: <owned debt type>
locations: [path:line]          # up to three examples
occurrences: <count>
evidence: <code, command output, or git statistic>
impact: <which changes become slower or riskier, and for whom>
interest: high | medium | low
principal: S | M | L | XL       # S < 1 day, M ≤ 1 week, L ≤ 1 month, XL > 1 month
contagion: yes | no             # spreads through copying or dependents
origin: deliberate | inadvertent | unknown
fix_sketch: <smallest safe step in one or two sentences>
confidence: high | medium | low
fingerprint: <type>:<path or module>:<root-cause slug>
```

## Verify and rank

1. Merge findings with the same `fingerprint`. Then merge findings that share locations and a root cause, keeping the strongest evidence.
2. Open the cited locations for every high-interest finding and for at least one in five of the others. Look for mitigations elsewhere, such as a framework guarantee, database constraint, middleware, test, or CI gate, and for a documented deliberate trade-off. Mark each finding `confirmed`, `downgraded` with new ratings, or `rejected` with the reason. Agreement between lanes is not evidence.
3. Rank by interest ÷ principal, scoring interest as high 3, medium 2, low 1, and principal as S 1, M 2, L 3, XL 4. Raise contagious items and items in top hotspots.
4. Group the ranked items:
   - `pay now`: high interest, small or medium principal.
   - `plan`: high interest, large principal. Give the first safe step, the rollback point, and the check that proves progress.
   - `contain`: contagious items. Give a guardrail that stops the spread, such as a lint rule, a CI check, or an architecture test.
   - `accept`: low interest. State why carrying the debt costs less than fixing it.
5. Never invent currency or hour totals.

## Result

Write the report to the agreed location, or return it inline. Include:

- a summary of at most eight lines covering the top themes and the first action;
- the hotspot table;
- the register sorted by group and rank;
- themes that link item IDs;
- at most five prevention guardrails, each tied to a contagious or recurring item;
- rejected and accepted items with reasons;
- commands run, skipped or failed lanes, missing evidence, and areas not covered;
- out-of-scope bugs and security observations, one line each.

Recommendations do not authorize implementation. Finish only when every lane has returned or has a recorded failure, every finding has a disposition, and every register entry has current locations and evidence.
