---
name: context-optimization
description: Reduce active-session context bloat without losing decisions, errors, evidence, or verification state. Use when tool output is verbose, a long task is.
---

# Context Optimization

Preserve task quality first. Optimize what is loaded and repeated; do not hide diagnostic evidence or install invisible interceptors by default.

## 1. Diagnose the source

Classify the dominant pressure:

- repeated instructions or duplicate skill metadata;
- long command, test, build, or search output;
- large files read in full instead of targeted excerpts;
- stale exploration that no longer affects the plan;
- repeated summaries with no new information;
- missing checkpoint, causing the same facts to be rediscovered.

Use context-budget for a corpus-wide inventory. Continue here for active-task reduction.

## 2. Reduce input before output

- Search first, then read only relevant ranges.
- Use file lists, counts, hashes, and structured summaries before opening full bodies.
- Batch independent lookups when the host supports it.
- Prefer machine-readable filters and selectors over dumping complete datasets.
- Load detailed references only when their branch of the task is active.

## 3. Control command output safely

- Prefer concise or quiet flags only when they preserve errors and exit status.
- During diagnosis, keep the first failing trace; shorten repeated successful output afterward.
- Capture large raw output in a file when authorized, then report counts, failures, and representative excerpts.
- Do not redirect stderr or suppress warnings that may explain a failure.
- Paginate or cap listings and state that output was truncated.

## 4. Create a loss-aware checkpoint

Before compaction, handoff, or a long phase transition, record:

1. objective and acceptance criteria;
2. decisions and why they were made;
3. verified facts with source paths or links;
4. changes already made and tests run;
5. unresolved risks, failed attempts, and blockers;
6. exact next actions;
7. user preferences and prohibitions that still apply.

Keep raw evidence reachable by path instead of copying it into every summary.

## 5. Compress by relevance

Retain:

- safety and authorization boundaries;
- current plan and state;
- exact errors still under investigation;
- interfaces, schemas, invariants, and acceptance tests;
- provenance and uncertainty.

Summarize or drop:

- superseded hypotheses;
- repeated successful logs;
- boilerplate already available in a referenced file;
- duplicated source excerpts;
- exploration that cannot affect remaining decisions.

## 6. Verify after optimization

Check that the checkpoint can answer:

- What is being done and why?
- What has already changed?
- What evidence supports the current direction?
- What must not be changed or forgotten?
- What remains and how will completion be verified?

If any answer is missing, restore it before continuing.

## Guardrails

- Do not claim a hidden global hook exists.
- Do not install command proxies, modify runtime hooks, or intercept all commands without explicit authorization and verified host support.
- Do not hardcode a context-window size, provider, or model family.
- Do not trade debuggability for fewer tokens.
- Do not rewrite user-owned files merely to save session context.
