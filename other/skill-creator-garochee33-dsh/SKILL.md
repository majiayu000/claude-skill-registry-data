---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
 - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
 - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages.

---

## Communicating with the user

Pay attention to context cues to understand how to phrase your communication. In the default case:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

---

## Creating a skill

### Capture Intent

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works?

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research, research in parallel via subagents if available, otherwise inline.

### Write the SKILL.md

- **name**: Skill identifier
- **description**: When to trigger, what it does. Make descriptions a little "pushy" — include both what the skill does AND specific contexts for when to use it.
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│ ├── YAML frontmatter (name, description required)
│ └── Markdown instructions
└── Bundled Resources (optional)
 ├── scripts/ - Executable code for deterministic/repetitive tasks
 ├── references/ - Docs loaded into context as needed
 └── assets/ - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited)

Keep SKILL.md under 500 lines. Reference files clearly from SKILL.md with guidance on when to read them.

#### Writing Patterns

Prefer imperative form. Explain the **why** behind instructions — don't just use MUST/NEVER. Use theory of mind and make skills general, not narrow to specific examples.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts. Save to `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

---

## Running and evaluating test cases

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. Don't spawn with-skill runs first and come back for baselines later.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory.

### Step 2: While runs are in progress, draft assertions

Draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable and have descriptive names.

Update `eval_metadata.json` files and `evals/evals.json` with assertions once drafted.

### Step 3: As runs complete, capture timing data

Save to `timing.json` in each run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4: Grade, aggregate, and launch the viewer

1. **Grade each run** — spawn a grader subagent that reads `agents/grader.md`. Save results to `grading.json`. Use fields `text`, `passed`, and `evidence`.
2. **Aggregate into benchmark**:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
3. **Do an analyst pass** — read `agents/analyzer.md` for what to look for.
4. **Launch the viewer**:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   In headless environments, use `--static <output_path>` instead.

**ALWAYS generate the eval viewer BEFORE evaluating inputs yourself. Get results in front of the human ASAP.**

### Step 5: Read the feedback

When the user is done, read `feedback.json`. Empty feedback means the user thought it was fine. Kill the viewer server when done:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

### How to think about improvements

1. **Generalize from the feedback** — create skills that work across many prompts, not just the test examples.
2. **Keep the prompt lean** — remove things that aren't pulling their weight.
3. **Explain the why** — transmit understanding, not just rules.
4. **Look for repeated work across test cases** — if all test runs wrote the same helper script, bundle it in `scripts/`.

### The iteration loop

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/`
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for user review, read feedback, improve again, repeat

Keep going until the user is happy, feedback is all empty, or you're not making meaningful progress.

---

## Advanced: Blind comparison

For rigorous comparison between two versions, read `agents/comparator.md` and `agents/analyzer.md`. Give two outputs to an independent agent without telling it which is which, and let it judge quality.

---

## Description Optimization

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Queries must be realistic, concrete, and specific. Focus on edge cases and near-misses for the negative cases.

### Step 2: Review with user

1. Read template from `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to `/tmp/eval_review_<skill-name>.html` and open it
4. User edits and clicks "Export Eval Set" → downloads to `~/Downloads/eval_set.json`

### Step 3: Run the optimization loop

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Splits eval set 60/40 train/test. Iterates up to 5 times. Returns `best_description` selected by test score.

### Step 4: Apply the result

Update the skill's SKILL.md frontmatter with `best_description`. Show before/after and report scores.

---

## Package and Present

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

---

## Environment-specific notes

### Claude.ai
- No subagents — run test cases one at a time, skip baseline runs
- No browser — present results inline, skip quantitative benchmarking
- Skip description optimization (requires `claude -p` CLI)

### Cowork
- Subagents available — full parallel workflow works
- No display — use `--static <output_path>` for eval viewer
- Feedback downloads as `feedback.json`

### Updating an existing skill
- Preserve the original name (directory name + frontmatter `name` field)
- Copy to a writeable location before editing (`/tmp/skill-name/`)

---

## Reference files

- `agents/grader.md` — evaluate assertions against outputs
- `agents/comparator.md` — blind A/B comparison
- `agents/analyzer.md` — analyze why one version beat another
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

## Core loop (summary)

1. Figure out what the skill is about
2. Draft or edit the skill
3. Run claude-with-access-to-the-skill on test prompts
4. Generate eval viewer → get human review → run quantitative evals
5. Repeat until satisfied
6. Package and return to user
