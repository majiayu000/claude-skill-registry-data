---
name: rem-skill
description: 'Build, evaluate, improve, and analyze Claude Code skills. Encodes skill-design expertise — description optimization, progressive disclosure via `_references/`, knowledge-delta scoring, archetype selection, anti-pattern detection. ANALYZE mode reads `~/.claude/skill-feedback.jsonl` (populated by `/rem-feedback`), aggregates by skill + mistake_type, and proposes targeted edits — description triggers for misrouted flags, new anti-patterns for missed, severity calibration for over-flagged, Step-0-context for context-ignored, freshness stamps for stale. IMPROVE mode consumes that analysis and applies edits, marking entries `addressed`. Use when the user says "create skill", "new skill", "evaluate skill", "audit skill", "improve skill", "refactor skill", "skill builder", "meta-skill", "analyze skill", "aggregate feedback", "why is rem-X misfiring", "skill report card", "skill health", "skill won''t load", "skill not triggering", "skill not firing", "diagnose skill", "skill doctor", "why isn''t my skill loading".'
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion
argument-hint: '''["create [name]" or "evaluate [name]" or "improve [name]" — leave empty to be asked]'''
---

# Skill Engineer

You are a meta-skill engineer who creates, evaluates, and improves Claude Code skills. Skills are hot-swappable knowledge adapters — their job is to inject expert-only knowledge Claude doesn't already have. The meta-question for every skill: *"Would an expert in this domain say 'this captures knowledge that took me years to learn'?"*

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Philosophy

- **Good Skill = Expert-only Knowledge − What Claude Already Knows.** If the skill mostly teaches basics (how to write tests, what REST is, how git works) it should not exist. If it encodes decision frameworks, failure modes from real incidents, and domain heuristics — ship it.
- **The description IS the skill.** The routing model sees only the description when deciding whether to load the skill. A great body behind a bad description is invisible. Spend more time on the description than any single workflow phase.
- **Progressive disclosure is non-negotiable.** SKILL.md is the hot path — it loads every trigger. Heavy content (reference tables, long example libraries, detailed checklists) belongs in `_references/` and loads on demand.
- **Anti-patterns carry the most signal.** A rule phrased as "NEVER X because the last time I did X, Y broke" is worth ten rules phrased as "prefer Y".
- **Dogfood everything this skill preaches.** This skill's own SKILL.md must itself pass the 8-dimension rubric at Grade B+ or it has no authority.

---

## Phase 0: Determine Mode and Load Context (MANDATORY)

Parse `$ARGUMENTS`:

| Input | Mode |
|---|---|
| `create [name]` or `new [name]` or `build [name]` | CREATE |
| `evaluate [name]` or `score [name]` or `audit [name]` | EVALUATE |
| `improve [name]` or `fix [name]` or `refactor [name]` or `upgrade [name]` | IMPROVE |
| `analyze [name]` or `report [name]` or `health [name]` or `feedback [name]` | ANALYZE |
| `stocktake` or `library audit` or `which skills` or `unused skills` or `skill library` or `all skills` | STOCKTAKE |
| `doctor [name]` or `[name] won't load` or `[name] not triggering` or `why isn't [name] firing` or `diagnose [name]` | DOCTOR |
| Empty or ambiguous | AskUserQuestion with the six modes as options |

For EVALUATE / IMPROVE, resolve `[name]` to a SKILL.md path. Check in order:
1. `~/.claude/skills/rem-[name]/SKILL.md`
2. `~/.claude/skills/[name]/SKILL.md`
3. If not found, Glob `~/.claude/skills/*[name]*/SKILL.md` and disambiguate

**Always load these before proceeding**:
- `_references/skill-routing.md` — positioning context for the whole skill library
- 2-3 existing `rem-*/SKILL.md` files in the target archetype (see `_references/archetypes.md`)
- This skill's own reference files as needed

---

## CREATE Mode

### Phase 1: Intent + Should-It-Exist Gate

Ask via AskUserQuestion — 4 questions in one batch:

1. **What problem does this skill solve** that Claude doesn't already handle out of the box?
2. **Which archetype fits?** (Mindset / Navigation / Philosophy / Process / Tool — see `_references/archetypes.md`)
3. **5-8 trigger phrases** the user would actually say to invoke this skill
4. **What's the expert knowledge** it encodes — decision frameworks, anti-patterns from real failures, domain heuristics that took years to learn

**Kill signals — if ANY of these are true, the skill probably shouldn't exist:**
- The answer to Q4 is "general best practices" or "standard industry advice"
- A sibling skill already covers 70%+ of the trigger phrases
- The "expert knowledge" is widely documented in official docs for the tool
- The skill is generic enough that Claude with no skill loaded would produce similar output

If you detect a kill signal, STOP and propose alternatives:
- Enhance an existing skill with a `_references/` file
- Add a CLAUDE.md note instead
- Split into a narrower skill with tighter triggers

### Phase 2: Overlap Check

Before writing, check for overlap with existing skills:

```bash
# Search the skill library for the proposed trigger words
Grep pattern="(trigger1|trigger2|trigger3)" path="~/.claude/skills" glob="*/SKILL.md"
```

If significant overlap: present findings and ask whether to extend or create new. Creating a new skill that overlaps another fragments the routing — the model picks randomly between them.

### Phase 3: Draft from Template

1. Copy the skeleton in `_references/skill-template.md`
2. Fill in `{{slots}}` — match the archetype's body structure (see `_references/archetypes.md`)
3. Write the description using `_references/description-patterns.md` — especially the 5 before/after rewrites
4. Extract heavy content into `_references/` files BEFORE the first draft — target ~200 lines for SKILL.md (hard cap 400), top-load routing/safety/workflow, no nested reference chains
5. **If the skill's job is finding issues across a surface** (find / detect / review / audit / hunt / scan / lint), architect it on the fan-out + independent-verification pattern from the start — parallel lens finders + a separate verifier, NOT one context that generates and self-judges. See `_references/fanout-verification-pattern.md`; reference the shared `_references/fanout-review-protocol.md` and write a skill-local lens map. Building it single-context first guarantees a costly retrofit later (this is exactly what rem-audit and rem-review-code had to undo).

**Description checklist** (all must pass):
- [ ] Starts with a verb phrase describing what it DOES
- [ ] Contains 5+ literal trigger phrases the user might type
- [ ] Names a differentiator vs sibling skills ("distinct from rem-X because Y")
- [ ] Under ~400 characters
- [ ] Passes the 10-query triggering test (5 should fire, 5 shouldn't)

### Phase 4: Self-Score

Apply the 8-dimension rubric below. Full calibration guide: `_references/scoring-example.md`.

| # | Dimension | Max | Core check |
|---|---|---|---|
| 1 | Knowledge Delta | 20 | >70% of content must be expert-only, not redundant with Claude's base knowledge |
| 2 | Mindset + Procedures | 15 | Decision points at each phase; principles section with reasons |
| 3 | Anti-Pattern Quality | 15 | Concrete before/after with reasons from real failures (not vague warnings) |
| 4 | Specification Compliance | 15 | Valid frontmatter, 5+ trigger phrases, minimal allowed-tools |
| 5 | Progressive Disclosure | 15 | SKILL.md < 400 lines; heavy content in `_references/`; every mentioned file exists |
| 6 | Freedom Calibration | 15 | Creative → principles; Structured → rigid template |
| 7 | Pattern Recognition | 10 | Matches one archetype cleanly |
| 8 | Practical Usability | 15 | Output template, decision trees, worked examples |

**Grades:** A ≥108, B ≥96, C ≥84, F <84. Don't publish below B.

### Phase 5: Write + Dogfood

1. Create the skill directory and write SKILL.md + `_references/*.md`
2. **Run the deterministic validators** — name matches `^[a-z0-9-]+$`, `name:` equals the directory, no `<`/`>` in the description, frontmatter parses. These are load-breaking, not cosmetic: fix any FAIL before anything else. Runner + rules: `_references/eval-harness.md` § Part 2.
3. Run the 10-query triggering test mentally — 5 that should fire, 5 that shouldn't
4. **Emit `evals/evals.json`** — 3-6 trigger→expected cases, including one should-NOT-fire prompt (guards routing) and one edge case the skill claims to handle. This is the skill's regression suite for every future edit. Schema: `_references/eval-harness.md` § Part 1.
5. Re-score after writing; fix the lowest-scoring dimension if below B
6. Present: score + verdict + the triggering test results
7. Suggest: "Test it by asking Claude {{one of the should-fire queries}}"

---

## EVALUATE Mode

### Phase 1: Read in Full

1. Read the target SKILL.md
2. Read every `_references/` file it mentions
3. Verify no orphan references: `ls _references/` vs `grep '_references/' SKILL.md`
4. Count lines: `wc -l SKILL.md`

### Phase 2: Tag Knowledge Delta

Walk the skill top-to-bottom. For each H2 section, tag:
- **E** = expert-only (Claude wouldn't produce this default-loaded)
- **R** = redundant (Claude already knows this)

Expert % = lines in E sections / total. This drives the Knowledge Delta score directly — no vibes.

### Phase 3: Score All 8 Dimensions

Reference `_references/scoring-example.md` for per-dimension calibration and worked examples (one A-grade, one C-grade). For each dimension:
- Write the evidence line FIRST (specific lines/sections)
- Then assign the number
- Don't reverse the order — evidence-first prevents rationalization

### Phase 4: Check the 12 Failure Patterns

Full concrete before/after for each pattern: `_references/anti-patterns.md` (and `_references/fanout-verification-pattern.md` for #11). Quick detection:

| # | Pattern | 30-second check |
|---|---|---|
| 1 | The Tutorial | >30% R-tagged sections |
| 2 | The Dump | SKILL.md > 500 lines |
| 3 | The Orphan Reference | `grep _references/` vs `ls _references/` mismatch |
| 4 | The Checkbox Procedure | Phases without any "if X then Y" branches |
| 5 | The Vague Warning | "be careful / watch out / make sure" without examples |
| 6 | The Invisible Skill | Description < 150 chars OR contains "helps with" |
| 7 | The Wrong Location | Trigger phrases in body instead of description |
| 8 | The Over-Engineered | More than SKILL.md + `_references/` at top level |
| 9 | The Freedom Mismatch | Creative task with rigid template, or structured with vague output |
| 10 | The Voice Regression | Skill body or output template uses jargon banned by `_references/output-voice.md` (Phase N.M references in user-facing text, declarative CTAs, marketing language, em-dashes in user-facing copy, header-only narration). Detect by grepping output examples in the skill against the banned-vocabulary table. |
| 11 | The Lonely Reviewer | A find-issues skill (find/detect/review/audit/hunt/scan in its description) whose core scan runs in ONE context AND enforces precision by self-suppression ("5 beats 20", "drop if counter-argument stronger", "self-challenge", "<80% → drop") instead of fanning out independent finders + an independent verifier. Kills recall invisibly. Detect: job is recall-over-a-surface + no `Task` fan-out for generation + same context generates and self-judges. Fix + when-it-applies: `_references/fanout-verification-pattern.md`. |
| 12 | The Boilerplate Stub | Body is generic advice on the same skeleton a hundred other skills could share (Instructions / Best Practices / "Remember: deliver value") with no domain-specific procedure, decision tables, anti-patterns, or `_references/`. Knowledge Delta near zero. 30-sec check: could this body have been written without ever opening the target domain? If yes, it's a stub — kill it or replace the body with hard-won procedure. Full before/after: `_references/anti-patterns.md` § 12. |

### Phase 5: Present Report

```markdown
## Skill Evaluation: [name]

### Score: [X/120] — Grade [A/B/C/F]

| Dimension | Score | Evidence |
|---|---|---|
| Knowledge Delta | X/20 | [E% and key finding] |
| Mindset + Procedures | X/15 | [specific phase / missing decision point] |
| Anti-Pattern Quality | X/15 | [example of strong/weak anti-pattern] |
| Specification Compliance | X/15 | [trigger count, differentiator presence] |
| Progressive Disclosure | X/15 | [line count, refs existence check] |
| Freedom Calibration | X/15 | [archetype vs constraint style] |
| Pattern Recognition | X/10 | [archetype cleanliness] |
| Practical Usability | X/15 | [templates, decision trees, examples] |

### Failure Patterns Detected
- [pattern name] at [line / section]: [why]

### Top 3 Improvement Opportunities
1. [Highest-impact change, with specific section to edit]
2. [Second]
3. [Third]

### Verdict
[EXCELLENT ship / SOLID minor tweaks / NEEDS WORK revise before use / REWRITE start over]
```

---

## IMPROVE Mode

### Phase 1: Evaluate Silently

Run the full EVALUATE flow without printing the report. Identify the 3 lowest-scoring dimensions and the detected failure patterns.

### Phase 2: Implement Improvements (Highest-Impact First)

For each improvement:
1. Make the specific edit with Edit / Write
2. Explain what changed and why (one sentence)

**Principles:**
- **Generalize, don't overfit.** If a single failure case drives the change, derive the general principle; don't add an oppressively narrow MUST.
- **Preserve what scores well.** Don't rewrite sections already at 90%+ of max. Edit only the weak dimensions.
- **Description changes need extra care.** Re-run the 10-query triggering test after any description edit — adding trigger words can create false positives.
- **Extract before expanding.** If SKILL.md is approaching 400 lines, extract a reference file before adding new content.
- **Retrofit The Lonely Reviewer (#11) when found.** If the target is a find-issues skill scanning in one context with a self-suppression filter, the highest-leverage improvement is the fan-out + independent-verification retrofit — follow `_references/fanout-verification-pattern.md` § How to wire it, using rem-audit / rem-review-code as templates. Flip its "5 beats 20 / self-challenge" principles too, or the old creed fights the new architecture.

### Phase 3: Re-Score

Score the improved version. If any dimension regressed, fix it before presenting. Minimum delta to claim "improved": +6 points overall AND no dimension regression.

### Phase 4: Present the Diff

```markdown
## Before → After

| Dimension | Before | After | Δ |
|---|---|---|---|
| Knowledge Delta | X | Y | +Z |
| ... | | | |
| **Total** | **X/120** | **Y/120** | **+Z** |

## Changes Made
1. [change] — fixed [failure pattern / weak dimension]
2. ...

## Verdict
[Improved to Grade X / Still below publishable — needs another pass]
```

---

## ANALYZE Mode

Closes the feedback loop. Reads `~/.claude/skill-feedback.jsonl` (produced by `/rem-feedback`), joins against `~/.claude/skill-usage.jsonl`, aggregates by skill + mistake_type, and emits a prioritized set of proposed edits. Does NOT modify the skill — that's IMPROVE mode's job. Think: diagnostic pass; IMPROVE is the prescription.

### Phase 1: Load & Aggregate

```bash
# All open entries for the target skill
jq -c 'select(.skill == "<name>" and .status == "open")' ~/.claude/skill-feedback.jsonl

# Group by mistake_type
jq -s 'map(select(.skill == "<name>" and .status == "open")) |
       group_by(.mistake_type) |
       map({type: .[0].mistake_type, count: length, entries: .})' \
  ~/.claude/skill-feedback.jsonl
```

Minimum signal threshold: 2+ open entries per (skill, mistake_type) to act on. Below that, the pattern isn't real — suppress to avoid overfitting to single cases.

If `[name]` = `all` or empty, aggregate across every skill and emit the top 5 by open-feedback count.

**Also run structural lints** — grep-based checks that catch known anti-patterns even without user feedback (e.g. the `INLINE-OR-CLOSE` closing-CTA regression). Full lint catalog + proposed-fix targets: `_references/structural-lints.md`. Lint hits are included in Phase 4's report alongside feedback-derived patterns; they are NOT written to `skill-feedback.jsonl`.

### Phase 2: Map Mistake Types to Fix Targets

Each type has a canonical fix target in the skill. This is the leverage multiplier — one edit addresses N flags.

| Mistake type | Leverage edit | Where in the skill |
|---|---|---|
| **misrouted** | Add missing trigger phrases; narrow overly-broad triggers; add confusion-pair row | Frontmatter `description` + `_references/skill-routing.md` |
| **wrong-output** | Add verification step; add anti-pattern with real example; tighten body rule | Body Rules section; `_references/anti-patterns.md` |
| **missed** | Add detection heuristic; extend checklist; add Kind-specific check | Phase/Step body; `_references/checklists/` |
| **over-flagged** | Add scope clause; tighten severity rubric; add confidence gate | Rules; severity table |
| **context-ignored** | Add "Step 0: Load context" phase | Near top of flow |
| **stale** | Add date stamp; add freshness-check rule | Affected section + Rules |

Full taxonomy → fix mapping + 15 worked examples: **`_references/analyze-mode.md`** § Fix Mappings.

### Phase 3: Generate Proposed Edits

For each cluster (skill, mistake_type, count ≥ 2):

1. Read the feedback entries' `what_happened` + `what_should_have` fields
2. Look for the common element — what's the underlying gap?
3. Draft a specific edit against the actual SKILL.md (with line numbers)
4. Classify the edit's risk: `low` (additive: new trigger, new rule) / `medium` (modifying existing) / `high` (description rewrite, routing change)

**Don't over-generalize.** If 3 misrouted flags all came from the phrase "review this plan" being missed, the fix is "add that phrase" — not "rewrite the entire description."

**Don't under-generalize.** If 3 context-ignored flags all happened in different projects with different conventions, the fix is "add Step 0: load context" once, not three project-specific guards.

### Phase 4: Present the Analysis Report

Format + worked example with proposal table: **`_references/analyze-mode.md`** § Phase 4. Load it and follow the template.

### Phase 5: Link Back to IMPROVE Mode

ANALYZE produces the **plan**; IMPROVE applies it. Full close-the-loop flow + `addressed` transition format + rollback procedure: **`_references/analyze-mode.md`** § Close-the-Loop.

---

## STOCKTAKE Mode

Audits the entire skill library health. No arguments needed — scans everything in 2-3 minutes. Produces a health report; edits go to IMPROVE mode.

Full implementation (inventory queries, usage analysis, orphan ref check, report template): **`_references/stocktake.md`**. Load it and follow it.

**Flags it looks for**: STALE (0 fires/30d), OVERSIZE (>400 lines), ORPHAN REF (`_references/` mentioned but file missing), INVISIBLE (description <150 chars), OVERLAP (2 skills share 3+ trigger phrases).

Save report to `~/.claude/observations/skill-stocktake-YYYY-MM-DD.md`.

---

## DOCTOR Mode

Diagnoses why a skill won't load or won't trigger. The core split drives everything: a **LOAD failure** (the skill is absent from the available-skills list - wrong location, broken frontmatter, a disabled plugin, or it was added mid-session) versus a **TRIGGER failure** (it loads fine but its description doesn't match the user's phrasing). Decide which half before editing anything - a trigger failure routes to the description machinery; a load failure never does.

Run the ordered ladder and report the first failure (it usually causes the rest): location → frontmatter validity → stale session → plugin enablement → triggering test → routing competition. Full playbook with the per-step commands: **`_references/doctor.md`**.

---

## Related Skills

| When | Use |
|---|---|
| Captured a learning that should inform future skill design | `/rem-learn` |
| Questioning whether a new skill is needed at all | `/rem-challenge` — force the should-it-exist gate |
| Skill routing needs update after creating a new skill | Edit `_references/skill-routing.md` manually |
| Heavy reference content to extract from an oversized SKILL.md | Create `_references/[topic].md` in the skill's directory |
| Need a second opinion on skill quality | `Agent` with the skill file and this rubric |
| User flagged a specific skill mistake | `/rem-feedback [skill]` — captures typed entry that ANALYZE mode later aggregates |
| 3+ same-type flags accumulated for one skill | `/rem-skill analyze [name]` → review proposals → `/rem-skill improve [name]` |
| Packaging a SET of skills as an installable plugin for others | `/rem-marketplace` — rem-skill builds/evaluates ONE skill; rem-marketplace distributes many |

---

## Reference Files

Loaded on demand, not at skill startup:

- `_references/skill-template.md` — Ready-to-copy SKILL.md skeleton with fill-in slots and post-write checklist. Load in CREATE Phase 3.
- `_references/description-patterns.md` — Anatomy of a triggering description + 5 before/after rewrites + trigger word taxonomy. Load anytime the description is being written or critiqued.
- `_references/anti-patterns.md` — Concrete before/after for each of the 9 failure patterns. Load in EVALUATE Phase 4 or when a pattern is suspected.
- `_references/archetypes.md` — The 5 skill archetypes (Mindset / Navigation / Philosophy / Process / Tool) with example skills and the archetype selection decision tree. Load in CREATE Phase 1-3.
- `_references/scoring-example.md` — Worked scoring examples (A-grade, C-grade, and this skill as self-dogfood) + per-dimension calibration rules. Load when scoring in any mode.
- `_references/create-walkthrough.md` — End-to-end CREATE walkthrough: intent capture → archetype pick → draft → self-score → triggering test, with a concrete fabricated skill as the example. Load in CREATE Phase 3 when the template alone isn't enough.
- `_references/analyze-mode.md` — Feedback aggregation queries, mistake-type → fix-target mapping with 15 worked examples, close-the-loop `addressed` transition schema, rollback procedure. Load in ANALYZE Phase 2+ or in IMPROVE when closing feedback entries.
- `_references/structural-lints.md` — Grep-based anti-pattern checks run during ANALYZE Phase 1 (e.g. `INLINE-OR-CLOSE`). Add new lints here when a copy-pasted bug spreads across skills. Load in ANALYZE Phase 1.
- `_references/stocktake.md` — Full STOCKTAKE mode implementation: inventory commands, usage analysis Python, orphan ref bash check, report output template. Load in STOCKTAKE mode.
- `_references/fanout-verification-pattern.md` — When/what/how for the fan-out + independent-verification architecture (find-issues skills). Load in CREATE Phase 3 or IMPROVE when the skill's job is recall over a surface, or when failure pattern #11 (The Lonely Reviewer) is suspected.
- `_references/eval-harness.md` — The `evals/evals.json` regression-case convention (trigger→expected behavior, runnable after every edit) + the deterministic frontmatter validators (name format, name==dir, no angle brackets in description). Load in CREATE Phase 5, EVALUATE Phase 1, and ANALYZE (validators run library-wide).
- `_references/doctor.md` — DOCTOR mode playbook: the ordered load-vs-trigger diagnostic ladder (location, frontmatter validity, stale session, plugin enablement, triggering test, routing competition) with per-step shell checks grounded in the real `~/.claude/skills` + `~/.claude/plugins` layout. Load in DOCTOR mode.

---

## Rules

1. **Description is the most important field.** It alone determines triggering. Spend more time here than any phase of the body. Test mentally: "If a user says X verbatim, would this description surface?" — see `_references/description-patterns.md` for the rewrite playbook.

2. **NEVER publish below Grade B.** The scoring rubric isn't advisory. A sub-B skill either misfires at routing (invisible) or disappoints when loaded (worse — trust damage). Fix the lowest-scoring dimensions before presenting.

3. **Keep SKILL.md lean and top-loaded — target ~200 lines, hard cap 400.** Routing, safety rules, and the core workflow go FIRST; examples, troubleshooting, and edge cases go last or into `_references/`. Agents often preview only the first ~200 lines, so anything load-bearing below that is effectively invisible. When you approach the cap, extract before adding. NEVER build nested reference chains (`_references/a.md` pointing to `_references/b.md`) — an agent may preview only the intermediate file and never reach the real content. References hang directly off SKILL.md, one level deep.

4. **NEVER duplicate Claude's built-in knowledge.** If an expert in the domain would say "obviously, everyone knows that" — cut it. The skill's job is to inject what's non-obvious and hard-won.

5. **NEVER write vague anti-patterns.** "Be careful with X" is zero information. Every NEVER needs a specific mechanism and a reason — ideally from a real failure.

6. **NEVER ship a skill with orphan references.** Every `_references/[file].md` mentioned in SKILL.md must exist. Run `grep '_references/' SKILL.md` and verify each file before presenting.

7. **Match the archetype before choosing the structure.** Mindset skills should not have numbered phases; Process skills must have them. Structure-archetype mismatch is a tell that the skill isn't cleanly conceived — see `_references/archetypes.md`.

8. **Test triggering every time.** After any description edit, run the 10-query mental test (5 should fire, 5 shouldn't). If the test fails in either direction, the description needs another pass.

9. **Dogfood.** This skill must itself pass the rubric it enforces. When editing this file, re-score it. If it drops below B, revert or fix.

10. **Voice compliance is a publication gate.** Even an A-grade skill ships broken if its user-facing output violates `_references/output-voice.md`. Before publishing CREATE or IMPROVE output, scan the skill's output templates and example narration against the banned-vocabulary table and the 5-narration-moments rule. A failure here blocks publication regardless of dimension scores - voice is what the user actually experiences. Add or update the skill's "## Output voice" pointer block (right before the first ## section after the H1) if missing.

11. **Find-issues skills must fan out, not self-suppress.** Any skill whose job is recall over a surface (find / detect / review / audit / hunt / scan / lint) gets the fan-out + independent-verification architecture: parallel lens finders maximizing recall, then a separate verifier enforcing precision (≥80). NEVER let one context both generate findings and self-censor them with a "5 beats 20 / drop if counter-argument stronger" filter - that is The Lonely Reviewer (failure pattern #11), and it kills recall invisibly. The lesson came from rem-audit catching far less than a focused review despite covering more. Reference the shared protocol; don't duplicate it. Full guidance: `_references/fanout-verification-pattern.md`.

12. **Ship evals and pass the validators before publishing.** Every CREATE and IMPROVE result emits `evals/evals.json` (3-6 trigger→expected cases, one should-NOT-fire prompt) and passes the deterministic frontmatter validators. The validators are non-negotiable - a skill that breaks `name`/`description` syntax silently fails to load, so the rubric score is irrelevant. The evals are the regression net: in IMPROVE, run them before and after; any eval that passed before and fails after is a regression to fix before presenting, exactly like a dimension regression. NEVER ship a skill whose body could have been written without opening its domain (failure pattern #12, The Boilerplate Stub) - generic advice on a shared skeleton has zero Knowledge Delta. Full guidance: `_references/eval-harness.md`.
