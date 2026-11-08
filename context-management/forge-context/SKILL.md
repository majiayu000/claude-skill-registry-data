---
name: forge-context
description: "Use when context degrades (context vol, vergeet instructies) or before /compact."
# W2-BUDGET original description (listing budget): "Use when a long session degrades (vergeet instructies, context vol, oude fout keert terug) or before /compact or a handoff: diagnose, mask, compact on time, split work into fresh agents."
---

# Forge playbook — Context health

**Self-improvement substrate:** before applying this skill, read `learnings.md` in this skill's own
folder and honor its corrections. After a run that produced a genuine correction, append it there with
a date and real evidence — never invent a lesson that did not happen.

The context window is a working desk, not a filing cabinet. Quality does not fade evenly: it holds, then
drops at a cliff. This skill keeps a Forge session (Lead, Boss or Workflow `agent()`) on the good side of
that cliff. It is method only: no hooks, no scripts, nothing installed.

## Where this skill stops (siblings)
| Question | Skill |
|---|---|
| "How full am I / what does this cost / tokens / usage / caching" | `forge-token-economy` (owns `/context`, `/usage`, the budget audit) |
| "Regenerate the mission snapshot" | `forge-snapshot` (writes `FORGE_SNAPSHOT.md`; hooks also run it) |
| "How did we do X before / remember this" | `forge-memory` |
| "Fix CLAUDE.md" | `claude-md-improver` |
This skill decides **when** and **how** to compact, mask, split or restart. It does not measure tokens.

## 1. Diagnose before you act
Name the pattern first; each has a different fix. Detail and symptoms: `references/degradation-patterns.md`.

| Pattern | What you see | First fix |
|---|---|---|
| Lost in the middle | A fact or rule is in context, yet ignored | Move it to the start or the end; restate it next to the task |
| Poisoning | A wrong claim (a bad tool result, a hallucinated path) keeps coming back | Find the source turn, state the correction once, re-derive from the real file |
| Distraction | Old exploration crowds the current task | Mask or summarise the old output |
| Confusion | Two tasks bleed into each other | Split: one task per agent or session |
| Clash | Two sources disagree (old plan vs new owner ask) | Surface the conflict; the newest owner instruction wins; record which one lost |

**Before you blame the context, rule out the prompt.** If the same instruction also fails in a fresh,
short context, the instruction is the problem. One bad answer is noise; a repeated drop after the
session grew is signal.

## 2. The four moves (write · select · compress · isolate)
1. **Write** — put state outside the window: the plan or status doc, `_scratch/` (gitignored), research
   dumps in `.claude/forge-research/`, lessons via `forge-memory`. Never loose files in the project root.
2. **Select** — load only what the step needs: Grep and Glob first, then targeted reads and diffs; no
   whole-repo dumps; no re-reading a file you just edited.
3. **Compress** — mask, then summarise (section 3). Summarising beats dropping.
4. **Isolate** — give an independent part its own fresh context: a Workflow `agent()` per part with its
   GOAT route (`agentType` with fixed model and effort, or explicit `model` and `effort`). Splitting costs
   overhead (each agent loads its own prompt and tools), so it pays off from about three real parts.

## 3. Mask first, compact second
**Observation masking (cheap, low risk).** Once a long tool output has given you its point, carry only
the point: "build log: 2 errors, both in `src/a.ts` line 40; full log at `_scratch/build.log`".
- Never mask: output from the latest turn, anything in an active reasoning chain, and **error output
  while debugging is still open** (keep it until the bug is fixed).
- Mask at once: duplicates, boilerplate headers, output already summarised.
- Keep the full text in a file and its path in the summary, so it can be re-read.

**Compaction (lossy).** Owner rule: compact on your own terms with a focus, around **60 %** context use;
never wait past 80 % (a model under heavy pressure writes worse summaries). Compact at a task boundary,
not in the middle of an edit. Decision table:

| Moment | Compact? |
|---|---|
| Research done, plan written to a file | Yes |
| Plan done, implementation starts | Yes |
| Debugging done, next feature | Yes |
| After a dead-end approach | Yes, drop the dead end |
| Halfway through a multi-file edit | No — paths and partial state get lost |

Run `/compact <focus>` with the next step as focus, for example `/compact keep: contract, files a.ts b.ts, next = tests`.

**Anchored summary, not a fresh rewrite.** Each compaction adds to the same fixed sections instead of
regenerating everything: Intent · Files touched (exact paths) · Decisions (with reason) · Current state ·
Next steps · Open risks. Keep identifiers verbatim: paths, commit SHAs, error codes, numbers. Never
summarise tool schemas or the owner's own words of the ask (`forge-scribe` keeps those verbatim).
Protect the early turns: the task setup and constraints cannot be re-derived later.

## 4. Placement rule
Stable material first (rules, contract, architecture), working material last (the current file, the
failing test, the exact next step). Recall is best at the start and the end, weakest in the middle.
When a long document must stay, put its key points before it and its conclusion after it.

## 5. Working rules from file-based planning
Adapted as rules only (no hooks, no scripts):
- **2-action rule:** after every two search, browse or screenshot steps, write the key findings to the
  plan or `_scratch/` file before going on. Images and web pages do not survive compaction; text does.
- **Read before you decide:** before a major decision, re-read the plan's goal section.
- **Update after you act:** at the end of a phase mark it done, list the files changed, log the errors.
- **Never repeat a failure:** the same failing command twice in a row is a defect. Change the approach.
- **3-strike rule for one error:** attempt 1 diagnose and fix the cause; attempt 2 a different method;
  attempt 3 question the assumptions. Then stop and report what you tried. This sits under the GOAT
  ladder (one escalation per work package) and the recovery policy (safe alternatives before BLOCKED).
- **Read or write?** Just wrote it: do not re-read. Saw an image or web data: write it down now.
  New phase or after a gap: read the plan and findings again.

## 6. After compaction or a restart: prove you still know
Ask yourself these and answer each from a real source (plan doc, `FORGE_SNAPSHOT.md`, `git status`,
run events), not from memory:
1. Where am I? (current phase or work package)
2. Where am I going? (remaining steps)
3. What is the goal? (the owner's ask, verbatim if possible)
4. What have I learned? (decisions and findings with paths)
5. What have I done? (files changed, checks run with their real result)

Probe questions catch a bad summary: "which file did I change last?", "what was the exact error?",
"what did the owner forbid?". If an answer is missing or vague, re-read the source before going on.
A summary that looks sure can still be stale: check it against the current ask.

## 7. Safe restart boundaries
Start a fresh session (or a fresh agent) at a **finished** task boundary, never at a random token count.
Before leaving, persist: accepted scope and decisions · task status and the next task · files changed and
the working-tree state · exact verification commands and their outcomes · open questions, risks and
approvals still needed. Do not commit or push unless the owner authorised it; otherwise record that the
changes are uncommitted. In the new session, read those artifacts and the real `git status` first, and
never infer an approval from an old conversation that no durable file records.

## Honesty
Token counts here are estimates unless `/context` or a measured report shows them. Never claim a
compaction "kept everything"; say what was dropped. Thresholds from outside sources go stale with new
models — treat them as starting points.

## Provenance
- **muratcankoylan/Agent-Skills-for-Context-Engineering** — paths `skills/context-degradation/SKILL.md`,
  `skills/context-optimization/SKILL.md`, `skills/context-compression/SKILL.md`; pinned SHA
  `9ff0c99108b36d3b886defd825d8ac1f47dba374`; MIT License, Copyright (c) 2025 Context Engineering Agent
  Skills Contributors. Taken (rewritten): the five degradation patterns, write/select/compress/isolate,
  masking rules, the 70–80 % compaction warning, anchored iterative summaries, probe questions, placement
  rule. Excluded: Python examples, benchmark tables and model-specific thresholds, framework landscape.
- **addyosmani/agent-skills** — path `skills/context-engineering/SKILL.md`; pinned SHA
  `301b02b12bff98e4688e6984af6556802322bbde`; MIT License, Copyright (c) 2025 Addy Osmani. Taken
  (rewritten): what to cut first / protect until the end, compress before dropping, order for recency,
  restartable session boundaries. Excluded: rules-file templates, MCP integration section.
- **OthmanAdi/planning-with-files** — path `.agents/skills/planning-with-files/SKILL.md`; pinned SHA
  `8eef6dc6540dde5eef3fdc0ac487ad9c48ef3ba5`; MIT License, Copyright (c) 2026 Ahmad Adi. Taken (rules
  only, rewritten): 2-action
  rule, read before decide, update after act, never repeat failures, 3-strike protocol, read-vs-write
  matrix, 5-question reboot test. Excluded: all hooks (5 hook events), shell/Python/PowerShell scripts,
  slash commands, plan-file templates and install steps.
- **ECC `skills/strategic-compact/SKILL.md`** — pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`; MIT License, Copyright (c) 2026 Affaan Mustafa. Taken
  (rewritten): compact at logical boundaries, the phase-transition table, write before compacting,
  `/compact` with a focus. Excluded: the `suggest-compact.js` PreToolUse hook and its settings snippet,
  env variables, the third-party MCP tool suggestions.
The MIT notices above apply to the adapted portions; the full MIT text is at each source repository.
Verified 2026-11-05: every GitHub path above was fetched read-only at its pinned SHA from
raw.githubusercontent.com (HTTP 200; the GitHub API was unreachable), and the copyright lines were read
from each root `LICENSE`; the ECC catalog was confirmed at `e2b8a51` with `skills/strategic-compact`
present. Hidden-Unicode scan of the fetched text: clean.
