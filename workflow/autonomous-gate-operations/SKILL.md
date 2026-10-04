---
name: autonomous-gate-operations
description: Use when driving or reviewing an unattended LLM-gated engineering process — enforce "no un-run greens" (reviewers execute the harness themselves), guard exit codes from pipe-masking, root-fix named flakes, and keep resumable state plus a written terminal state.
stacks: [python, powershell, any]
domains: [any]
phases: [gate, release]
tags: [autonomy, llm-gates, process, audit, flaky-tests, decide-and-log]
scope: kit
---
**When to use.** Any multi-day autonomous run with LLM reviewers as the only check. *Why:* the trail
is only as trustworthy as its weakest execution claim; all three of our gate rounds caught real
defects precisely because the reviewer re-ran everything instead of reading the driver's prose.

**Procedure.**
1. Reviewers run the harness/trace/probes themselves and quote real output; a verdict citing an
   un-run result is invalid. Fresh context per round; findings routed with severities; verdict blocks
   recorded append-only.
2. Never mask exit codes (`cmd | tail` in a `&&` chain ate a red test through two commits); check
   `$?` explicitly. Never run the test suite concurrently with pipeline jobs sharing output dirs.
3. Decide-and-log instead of blocking on absent humans: every judgment call gets a rationale in the
   append-only log; ratified decisions are extended or corrected by entry, never silently re-decided.
4. Keep honest-red visible: failing baselines recorded before fixes; Draft/Blocked items never
   claimed; disclosures (e.g. judge noise floor) promoted to the surface the human signs.
5. Root-fix flakes an unattended loop would trip on (ours: Windows `os.replace` sharing violation →
   bounded winerror-scoped retry + two tests), and maintain a per-turn resume note ending with the
   explicit terminal state ("no pending agent action — do not reopen gates").
6. **Done when:** an independent reviewer can APPROVE from executions and the written trail alone,
   with zero claims they had to take on faith.

**Knowledge:** FIELD-KNOWLEDGE-NOTHOMEWRECKER.md §F4 (+ §F1/§F2 for the loop and evidence rules).
