---
name: skill-conductor
description: >
  Create, edit, evaluate, and package agent skills. Use when building a new
  skill from scratch, improving an existing skill, fixing a skill that never
  triggers or fires unreliably, running evals to test a skill, benchmarking
  skill performance, optimizing a skill's description, reviewing third-party
  skills for quality, or packaging skills for distribution — even if the user
  doesn't explicitly say "skill" (e.g. "teach Claude to do X", "make the
  agent always follow Y"). Not for using skills or general coding
  tasks.
---

# Skill Conductor

Full lifecycle management for agent skills: **draft → test → review → improve → repeat**.

One skill to rule them all — from architecture to packaging. The core loop is always the same: write something, test it, see what fails, fix it, test again.

## Runtime requirements (pre-flight)

Before any mode that touches scripts (CREATE, IMPROVE, VALIDATE, OPTIMIZE, PACKAGE), run the pre-flight block → **`references/runtime-setup.md`** (checks `uv`, sets `UV_BIN`/`SKILL_CONDUCTOR_DIR`, verifies LLM access). If `uv` is absent, stop and tell the user.

## How to communicate

Read context cues. If the user is a skill author iterating on their own work, be direct and technical. If they're new to skills, explain the _why_ behind each step — not just what to do, but why it matters. Default to conversational, not robotic.

- Explain trade-offs when there's a real choice to make
- Use concrete examples over abstract rules
- When something fails, explain the root cause, not just the fix
- Imperative voice in instructions: "Extract the data", not "You should extract"

## Modes

Detect mode from context. If ambiguous, ask.

| Mode        | When                                             | What happens                                                    |
| ----------- | ------------------------------------------------ | --------------------------------------------------------------- |
| 1. CREATE   | "build a skill", "new skill for..."              | Full lifecycle: intent → architecture → scaffold → write → test |
| 2. IMPROVE  | "fix this skill", "it doesn't trigger"           | Diagnose → eval loop → gated self-update → iterate              |
| 3. VALIDATE | "test this skill", "run evals"                   | Structural checks + trigger testing + BinEval scoring           |
| 4. REVIEW   | "review this skill", third-party assessment      | 11-point quality gate, quick and focused                        |
| 5. OPTIMIZE | "improve triggering", "description optimization" | Automated description optimization with train/test split        |
| 6. PACKAGE  | "package for distribution"                       | Validate + bundle into .skill file                              |

---

## Mode 1: CREATE

### Step 1: Capture Intent

Before writing anything, extract 2–3 concrete scenarios.

Ask:

- "What specific task should this skill handle?"
- "What would a user say to trigger it?"
- "What should NOT trigger it?"

Don't move on until you have a clear picture of what the skill does, for whom, and when. This prevents the most common failure: a skill that does _something_ but triggers for the wrong things.

### Step 2: Baseline (TDD RED)

Before writing the skill, verify the agent fails without it:

1. Take one scenario from Step 1
2. Run it in a clean session without the skill
3. Document what went wrong — what the agent guessed, what it missed

If the agent already handles it perfectly, the skill is unnecessary. This sounds obvious, but it's the most skipped step and the most valuable one.

### Step 3: Architecture

Choose a primary pattern from `references/patterns.md` (can combine):

| Pattern                 | Use when                                 |
| ----------------------- | ---------------------------------------- |
| Sequential workflow     | clear step-by-step process               |
| Iterative refinement    | output improves with cycles              |
| Context-aware selection | same goal, different tools by context    |
| Domain intelligence     | specialized knowledge beyond tool access |
| Multi-MCP coordination  | workflow spans multiple services         |

Choose degrees of freedom — this determines how much control vs. flexibility the skill gives the agent:

| Freedom             | When                                        | Example                 |
| ------------------- | ------------------------------------------- | ----------------------- |
| Low (scripts)       | fragile, error-prone, must be exact         | PDF rotation, API calls |
| Medium (pseudocode) | preferred pattern exists, some variation ok | data processing         |
| High (text)         | multiple valid approaches, judgment needed  | design decisions        |

**Freedom test:** ask "if the agent makes a mistake here, what is the consequence?" High consequence → low freedom (an exact script it must not modify). Low consequence → high freedom (prose, let it judge). Calibrate per step, not per skill — one skill can hold both.

**Golden rule: read `references/sop-practices.md` before authoring or reviewing ANY skill.** It holds the canonical **10 authoring principles** (universal): pre-flight, no-process-in-description, MOC (SKILL.md = map, not prose), fresh-practitioner author, TWI "why", blind-agent test, inline checklists, one-term-per-concept, cut-the-fat (env/keys OUT of SKILL.md), match-the-form-to-the-failure. For **procedural** skills (business process with branching: request, quote, onboarding, escalation) the same file also has the deep SOP methodology — format selection, 7-step process, procedural checklist.

### Step 4: Scaffold

```bash
uv run scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets]
```

Or create manually:

```
skill-name/
├── SKILL.md          # required — the brain
├── scripts/          # deterministic operations (executed, not loaded)
├── references/       # detailed docs (loaded on demand)
└── assets/           # templates, images for output (never loaded)
```

### Step 5: Write SKILL.md

#### Frontmatter

```yaml
---
name: kebab-case-name
description: >
  [What it does]. Use when [4-5 phrasing variations users actually say] — even
  if they don't explicitly say "[canonical term]". Do NOT use for [negatives].
---
```

The description is the single most important line — it decides whether the skill triggers at all. The full formula, the pushy clause and worked GOOD/BAD examples live in `references/sop-practices.md` Principle #2. Read it before writing one.

- `name`: lowercase, digits, hyphens only. No consecutive hyphens. Matches folder name. Max 64 chars
- `description`: max 1024 chars. No angle brackets. No process/workflow steps
- **Don't put workflow in the description** — tested: when the description lists process steps, the agent follows it and skips the body entirely

#### Body structure

```markdown
# Skill Name

## Overview

What this enables. 1-2 sentences. Core principle.

## [Main sections]

Step-by-step with numbered sequences.
Concrete templates over prose.
Imperative voice throughout.

## Common Mistakes

What goes wrong + how to fix.

## Troubleshooting (if applicable)

Error: [message] → Cause: [why] → Fix: [how]
```

#### Writing rules

- **One term per concept.** Pick "template" and stick with it — not template/boilerplate/scaffold (Principle 8)
- **SKILL.md = map, not prose.** Body is a table-of-contents pointing to references; detail lives there (Principle 3)
- **No secrets/env in SKILL.md.** No keys, passwords, tokens, env values, or user-absolute paths (`/home/<user>`, `/Users/<user>`) — reference them, never inline (Principle 9a)
- **Progressive disclosure.** SKILL.md = brain (<500 lines). References = details. One level deep
- **Token budget.** Frequently loaded: <200 words. Standard: <500 lines. Heavy: move to references/
- **No junk files.** No README, CHANGELOG inside the skill
- **Scripts:** bundle when same code rewritten repeatedly, or operation is fragile. Must return descriptive stdout/stderr on failure
- **Imperative voice.** Use "Extract the data", not "you should extract" or capitalized "MUST/NEVER" — explanation > rule (see `references/sop-practices.md` Principle 5, TWI)

### Step 6: Test Cases & Eval Loop

This is the critical step — most failures hide here. Treat it as three sub-phases.

Before the full loop, micro-test the wording of anything you just wrote (5+ fresh-context reps, always with a no-guidance control) → `references/pressure-testing.md`. For a discipline skill — one that makes the agent follow a rule it's tempted to break — a pressure scenario from that file is mandatory, not optional.

#### 6a. Pre-flight (before spawning anything)

- [ ] `evals/evals.json` exists with 3–5 prompts (see `references/schemas.md`)
- [ ] Workspace dir created: `<skill-name>-workspace/iteration-1/`
- [ ] Each eval has a descriptive name (not just `eval-0`) and `eval_metadata.json`
- [ ] Anthropic key for executor subagents is set
- [ ] `uv` and `eval-viewer/generate_review.py` are reachable from current working dir

If any item fails — fix before proceeding. A missing workspace dir mid-run loses outputs.

#### 6b. Run loop (do all in one turn)

| What | Key move | Why |
|---|---|---|
| Spawn with-skill runs | One subagent per eval, skill active, save outputs to `iteration-N/<eval-name>/with_skill/` | Parallel = same wall time as one run |
| Spawn baseline runs in the same turn | Same prompt, no skill (or old version snapshot for IMPROVE), save to `without_skill/` or `old_skill/` | If you wait, baselines drift in time and aren't comparable |
| Draft assertions while runs execute | Pull verifiable statements from eval prompts | Don't waste the 5–15 min of subagent time |
| Capture timing on each notification | Save `total_tokens`, `duration_ms` to `timing.json` immediately | Notification is the only source — process per-arrival, don't batch |

#### 6c. Post-run checklist

- [ ] All `timing.json` files written (one per run)
- [ ] Each run has a `grading.json` with fields `text`, `passed`, `evidence` (not `name`/`met`)
- [ ] `benchmark.json` aggregated: `uv run scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>`
- [ ] Analyst pass done — see `agents/analyzer.md` for what to look for (non-discriminating assertions, high-variance evals, time/token tradeoffs)
- [ ] Eval viewer launched: `uv run eval-viewer/generate_review.py <workspace> --skill-name <name> --benchmark <path>`
  - In headless mode: `--static <output.html>` and send file to user
  - For iteration 2+: add `--previous-workspace <previous-iteration-path>`
- [ ] User saw the viewer **before** I started editing the skill

The last bullet is the trap. If you skip user review and "improve" based on your own reading of outputs, you optimize against your taste, not the user's.

### Step 7: Verify & Refactor

1. Does the skill trigger automatically for the right queries?
2. Does the agent follow body instructions (not just description)?
3. Does the output meet use case requirements?
4. Does it NOT trigger on unrelated queries?

If any fail → iterate. Find how the agent rationalizes around the skill, plug loopholes, re-verify.

---

## Mode 2: IMPROVE

### Step 1: Diagnose

Read the existing SKILL.md completely. Identify the problem class:

| Problem             | Signal                      | Fix                                                      |
| ------------------- | --------------------------- | -------------------------------------------------------- |
| Undertriggering     | skill doesn't load          | add keywords, trigger phrases, file types to description |
| Overtriggering      | loads for unrelated queries | add negative triggers, be more specific                  |
| Skips body          | follows description only    | remove process/workflow from description                 |
| Inconsistent output | varies across sessions      | add explicit templates, reduce freedom, add scripts      |
| Too slow            | large context               | move detail to references/, cut body to <500 lines       |

### Improvement mindset

1. **Generalize from feedback.** You're iterating on a few examples, but the skill will be used on thousands of prompts. Don't overfit — avoid fiddly patches or oppressive MUSTs for one test case. Try different metaphors or patterns instead
2. **Keep the prompt lean.** Read transcripts, not just outputs. If the skill makes the model waste time on unproductive steps, remove those instructions and see what happens
3. **Explain the why.** LLMs have good theory of mind. Instead of ALWAYS/NEVER in caps, explain the reasoning — it's more powerful and robust. If you're writing rigid rules, reframe as explanations
4. **Look for repeated work.** If all test runs independently write the same helper script, bundle it in `scripts/`. Saves every future invocation from reinventing the wheel
5. **Apply the authoring canon.** Read `references/sop-practices.md` — the 10 canonical principles (universal) map directly to skill failure modes: process leaking into description, SKILL.md bloated instead of a map, env/keys inlined, silent improvisation from missing "why", missed edge cases, agents skipping end-of-doc checklists, a rule whose form doesn't match its failure. For process skills (ticket, quote, escalation) also apply the deep SOP methodology in the same file

### Step 2: Eval Iteration Loop

The improvement cycle mirrors CREATE Step 6, but focused on the broken behavior. Micro-test each candidate wording before it enters the loop, and re-run the pressure scenarios if the skill enforces a rule → `references/pressure-testing.md`.

1. Run the failing case with current skill → document failure
2. Apply fix using writing rules from CREATE Step 5
3. Run eval again → grade with `agents/grader.md`
4. Launch viewer: `uv run eval-viewer/generate_review.py <workspace>`
   - **Headless/Cowork:** use `--static <output.html>` instead of live server
5. Review, provide feedback, iterate

### Step 3: Gated Self-Update Loop

Drive iteration off failing BinEval questions, not taste — and accept edits only against evidence the editor never saw. Full rules: `references/bineval-method.md` § Gated self-update loop.

1. **Freeze the split once per session:** `uv run scripts/split_evals.py evals/evals.json --holdout 0.4 --write <workspace>/split.json` — deterministic, stratified by the optional per-eval `category`. Never re-split after seeing results
2. Run ALL evals on the current version and grade (see Mode 3 Stage 3 + `references/bineval-method.md`) → collect `failing[]`
3. Analyze failures on TRAIN cases only: spawn `agents/analyzer.md` with train transcripts + gradings to produce generalized, deduped lessons. Held-out grading stays unopened until the gate
4. Apply **at most 3 atomic edits** (add/delete/replace one rule, paragraph, or table row; one edit = one lesson, labeled). No wholesale rewrites — small diffs keep cause and effect attributable at the gate
5. Re-run ALL evals. **Gate — accept iff:** (a) no held-out assertion flips pass→fail vs the parent (a flip counts only once it reproduces in 2 consecutive runs — single runs are noisy); (b) train pass-rate strictly improves; (c) no NEW failing critical question. Held-out improvement is welcome but not required — with 5–8 held-out cases, demanding it measures luck
6. Record per-assertion transitions (improved / regressed / persistent-fail / stable-success) → `transitions` block in benchmark.json
7. Terminate when train `failing[]` (or its critical subset) is empty, or after 3 iterations. Keep the best ACCEPTED version by held-out pass-rate, then train pass-rate

### Step 3b: Blind Comparison (optional, for major changes)

When you have two meaningfully different versions:

1. Run both versions on the same evals
2. Spawn `agents/comparator.md` — answers the SAME binary questions for outputs A and B without knowing which skill produced which
3. Comparator reports per-dimension yes-rate for each version; winner = higher overall yes-rate, tiebreak = critical-dimension yes-rate
4. Spawn `agents/analyzer.md` — unblinds results, analyzes WHY the winner won
5. Apply insights to improve the losing version

This prevents bias. The comparator judges output quality, not skill design.

---

## Mode 3: VALIDATE

Three stages, run in order.

### Stage 1: Structural Validation

```bash
uv run scripts/eval_skill.py <skill-folder>
```

Checks: frontmatter, naming, description quality, process leak detection, body size, structure, scripts. Target: 10/10, no warnings.

### Stage 2: Discovery (trigger testing)

Generate 6 test prompts:

- 3 that SHOULD trigger the skill
- 3 that should NOT (similar-sounding but wrong domain)

Run each in clean session. Target: 6/6 correct.

For automated trigger testing at scale, use:

```bash
uv run scripts/run_eval.py --eval-set <path> --skill-path <path> --runs-per-query 3
```

### Stage 3: BinEval Scoring

Evaluate with atomic binary yes/no questions across 5 dimensions — each answered 1/0 after a written critique citing evidence. See `references/bineval-method.md` for the method, `references/quality-questions.md` for the question bank, and `agents/bineval.md` for the evaluator that emits `bineval.json`.

The 5 dimensions: **Discovery, Clarity, Structure, Robustness, Completeness**.

Questions for the skill-artifact come from two sources (`question_source: "hybrid"`):

- **Deterministic** — emitted by `scripts/eval_skill.py --json` (the sole emitter), e.g. `DET-STRUCT-SKILLMD-EXISTS`, `DET-DISCOVERY-DESC-PRESENT`. Some are flagged critical.
- **Fixed bank** — the versioned llm questions in `references/quality-questions.md`; the judge answers them, never invents its own. (Generated per-task questions via the two-step meta-prompt belong to output grading in Modes 1–2, `agents/grader.md` — not to artifact scoring.)

The judge only answers the questions. YOU aggregate: per-dimension `dimension_scores` S_d = mean of that dimension's answers; overall S = mean of all answers. Never put the bands or the GATE into a judge prompt — a judge that knows the bar is biased toward it (`references/bineval-method.md`).

**Display bands:** S≥0.90 production-ready · 0.70–0.89 solid · 0.50–0.69 needs-work · <0.50 rewrite.

**GATE** = every critical question (deterministic + critical bank questions) answered 1. The GATE is the pass criterion — not the scalar S.

---

## Mode 4: REVIEW

Quick quality gate for third-party skills.

### Checklist (pass/fail)

```
[ ] SKILL.md exists, exact case
[ ] Valid YAML frontmatter (name + description)
[ ] name: kebab-case, matches folder, ≤64 chars
[ ] description: ≤1024 chars, no angle brackets
[ ] description has triggers ("Use when...")
[ ] description has NO workflow/process steps
[ ] No README.md inside skill folder
[ ] SKILL.md < 500 lines
[ ] References max 1 level deep
[ ] Scripts tested and executable
[ ] No hardcoded paths/tokens/secrets
```

Then run VALIDATE Stage 2 (discovery) on the description. Report score + checklist.

The deterministic subset of this checklist is emitted as binary BinEval question records by `scripts/eval_skill.py --json` (e.g. `DET-STRUCT-SKILLMD-EXISTS`, `DET-DISCOVERY-DESC-PRESENT`, `DET-ROBUST-NO-SECRETS`) — the sole emitter of those records.

The checklist exists because these are the failure modes that actually happen in practice — especially process-in-description, which causes the agent to skip the body entirely.

---

## Mode 5: OPTIMIZE

Automated description optimization. The description competes with other skills for Claude's attention — optimization finds the wording that triggers most accurately. The same train/held-out principle now gates body edits too — see Mode 2 Step 3.

### How it works

1. Create an eval set: 20 queries (10 should-trigger, 10 should-not)

#### Writing good eval queries

Queries must be realistic — concrete, detailed, with file paths, context, abbreviations, typos. Not `"Format this data"` but `"my boss sent Q4 sales final FINAL v2.xlsx, add profit margin % column, revenue is col C costs col D"`.

**Should-trigger (10):** Different phrasings of the same intent — formal, casual, implicit. Include cases where user doesn't name the skill but clearly needs it. Add competing-skill edge cases.

**Should-NOT-trigger (10):** Near-misses that share keywords but need something different. Adjacent domains, ambiguous phrasing. "Write fibonacci" as negative for PDF skill = useless — too easy. Make negatives genuinely tricky.

**Triggering mechanics:** Claude only consults skills for tasks it can't handle directly. Simple queries ("read this PDF") won't trigger skills regardless of description — Claude handles them with basic tools. Eval queries must be substantive enough that consulting a skill would help.

2. Review queries in the browser: `assets/eval_review.html`
3. Run the optimization loop:

```bash
uv run scripts/run_loop.py \
  --eval-set evals/eval_set.json \
  --skill-path <skill-dir> \
  --model <model-id> \
  --max-iterations 5 \
  --holdout 0.4 \
  --verbose
```

The loop:

- Splits queries into train (60%) and held-out (40%) to prevent overfitting
- Each iteration: evaluates current description → Claude proposes improvement → re-evaluates
- Improvement model sees only train results (blinded to held-out)
- Selects the best description by held-out score
- Opens live HTML report automatically

### Supporting scripts

| Script                           | Purpose                                    |
| -------------------------------- | ------------------------------------------ |
| `scripts/run_eval.py`            | Run trigger evaluation on a description    |
| `scripts/improve_description.py` | Claude proposes improved description       |
| `scripts/generate_report.py`     | HTML visualization of optimization history |
| `scripts/aggregate_benchmark.py` | Statistical aggregation of benchmark runs  |

---

## Mode 6: PACKAGE

1. Run REVIEW checklist (Mode 4)
2. Validate:

```bash
uv run scripts/quick_validate.py <skill-folder>
```

3. Package:

```bash
uv run scripts/package_skill.py <skill-folder> [output-dir]
```

Creates `skill-name.skill` (zip with .skill extension). Verify: unzip in temp dir, check structure intact.

---

## Quick Reference

### Skill categories

1. **Document/Asset Creation** — consistent output (docs, designs, code)
2. **Workflow Automation** — multi-step processes with methodology
3. **MCP Enhancement** — workflow guidance on top of tool access
4. **Procedural / Process** — business procedures with decision points and exceptions (handling a request, generating a quote, processing an invoice, onboarding, escalation). For these → read `references/sop-practices.md`

### File purposes

| Directory   | Loaded?              | Purpose                  |
| ----------- | -------------------- | ------------------------ |
| SKILL.md    | on trigger           | brain — instructions     |
| references/ | on demand            | detailed docs, schemas   |
| scripts/    | executed, not loaded | deterministic operations |
| assets/     | never loaded         | templates, images        |

### Progressive disclosure budget

| Level             | When loaded            | Budget     |
| ----------------- | ---------------------- | ---------- |
| Frontmatter       | always (system prompt) | ~100 words |
| SKILL.md body     | on trigger             | <500 lines |
| Bundled resources | on demand              | unlimited  |

### Description formula

`[What it does]` + `Use when [4-5 phrasings users actually say]` + `even if they don't explicitly say "<canonical term>"` + `Do NOT use for [negatives]` — full rules and examples in `references/sop-practices.md` Principle #2.

## Reference Files

Load on demand, at the point of use named in each mode — never wholesale. Load an `agents/*` file only at the step that spawns that agent; load `references/schemas.md` only when writing or reading a JSON artifact. Everything else stays unloaded.

| Path                             | What's inside                              |
| -------------------------------- | ------------------------------------------ |
| `agents/grader.md`               | Evidence-based assertion grading           |
| `agents/comparator.md`           | Blind A/B output comparison                |
| `agents/analyzer.md`             | Post-hoc analysis + benchmark notes        |
| `agents/bineval.md`              | BinEval evaluator — emits `bineval.json`   |
| `references/patterns.md`         | 5 architectural patterns + anti-patterns   |
| `references/schemas.md`          | JSON schemas for evals, grading, benchmark |
| `references/bineval-method.md`   | BinEval method: dimensions, scoring, GATE  |
| `references/quality-questions.md`| BinEval question bank (deterministic + bank)|
| `references/pressure-testing.md` | Micro-tests for wording + pressure scenarios for discipline skills |
| `references/sop-practices.md`    | **Canon: 10 authoring principles (universal)** + deep SOP methodology for procedural skills |
| `references/runtime-setup.md`    | Pre-flight: uv/env/path checks, LLM-access options |
| `eval-viewer/`                   | Interactive HTML viewer for eval results   |
| `assets/eval_review.html`        | Trigger eval set editor                    |
| `scripts/eval_skill.py`          | Structural validation (10-point scoring)   |
| `scripts/init_skill.py`          | Skill scaffolder                           |
| `scripts/run_eval.py`            | Trigger evaluation runner                  |
| `scripts/run_loop.py`            | Eval + improve optimization loop           |
| `scripts/improve_description.py` | Claude-powered description improvement     |
| `scripts/aggregate_benchmark.py` | Benchmark statistics aggregator            |
| `scripts/generate_report.py`     | HTML report generator                      |
| `scripts/quick_validate.py`      | Quick validation for packager              |
| `scripts/test_smoke.py`          | Smoke tests for all scripts (12 tests)     |
| `scripts/package_skill.py`       | Skill → .skill packager                    |
| `scripts/utils.py`               | Shared utilities (parse_skill_md)          |
