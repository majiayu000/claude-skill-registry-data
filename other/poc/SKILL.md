---
name: poc
description: Structured proof-of-concept exploration with hypothesis testing and reproducible experiments
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, WebFetch, WebSearch
---

# POC: Structured Exploration

Run disciplined proof-of-concept experiments. Explore ideas with structure, capture learnings, and make informed proceed/drop decisions.

**Philosophy:** POCs are for learning, not shipping. But "exploration" doesn't mean "chaos." Every experiment should be reproducible, every claim verifiable.

## Usage

```
/poc <idea-or-hypothesis>
/poc --resume <worktree-path>
/poc --status <worktree-path>
/poc --terminate <worktree-path>
```

Examples:
- `/poc "Can we extract structured data from HTML in BQ using Vertex AI cost-effectively?"`
- `/poc --resume .worktrees/poc-vertex-html`
- `/poc --terminate .worktrees/poc-vertex-html`

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  /poc "idea"                                                │
│      ↓                                                      │
│  Phase 1: Initialize                                        │
│  - Create worktree                                          │
│  - Clarify hypothesis (questions one at a time)             │
│  - Define success/fail criteria                             │
│  - List approaches to test                                  │
│  - Set up POC.md                                            │
│      ↓                                                      │
│  Phase 2: Explore (iterative)                               │
│  - Run experiments                                          │
│  - Log results with reproduce commands                      │
│  - Capture unknown unknowns                                 │
│  - Checkpoint: "Continue, pivot, or stop?"                  │
│      ↓                                                      │
│  Phase 3: Terminate                                         │
│  - Fill results summary                                     │
│  - Write verdict                                            │
│  - Decision: Proceed → /brainstorm | Drop → cleanup         │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Initialize

### Step 1.1: Create Worktree

```bash
# Generate slug from idea
SLUG="poc-$(echo "$IDEA" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)"
BRANCH="poc/$SLUG"
WORKTREE=".worktrees/$SLUG"

# Create worktree
mkdir -p .worktrees
git worktree add "$WORKTREE" -b "$BRANCH"

# Initialize structure
mkdir -p "$WORKTREE/scripts"
mkdir -p "$WORKTREE/data"
```

### Step 1.2: Clarify the POC

Ask questions ONE AT A TIME to understand:

1. **Hypothesis**: "What do you think might work? What are you trying to learn?"
2. **Success criteria**: "How will you know this POC succeeded? Be specific."
3. **Fail criteria**: "What would tell you to stop or that this approach won't work?"
4. **Constraints**: "Any budget limits, time constraints, or tech requirements?"
5. **Approaches**: "What different approaches do you want to compare?"
6. **Evaluation dimensions**: "What matters? Cost? Accuracy? Speed? Rank them."

### Step 1.3: Create POC.md

Create `$WORKTREE/POC.md` with the template (see below).

### Step 1.4: Set Up Test Data

Ask: "What data will you test against? Do you have ground truth for measuring accuracy?"

Options:
- User provides sample data → copy to `$WORKTREE/data/`
- Need to generate sample → create script in `$WORKTREE/scripts/setup_data.py`
- Use existing data → document location

---

## Phase 2: Explore

This phase is iterative. For each experiment:

### Step 2.1: Plan Experiment

Before coding, state:
- Which approach are we testing?
- What specific question does this answer?
- How will we measure the result?

### Step 2.2: Write Spike Code

Write minimal code to test the hypothesis. Place in `$WORKTREE/scripts/`.

**Requirements:**
- Script must be runnable standalone
- Script must output measurable results (not just "it worked")
- Include `--sample` or similar flag to control scope

Example:
```python
# scripts/test_approach_a.py
"""Test Approach A: Direct Vertex extraction from raw HTML."""

import argparse
import time
from pathlib import Path

def main(sample_size: int):
    results = {"correct": 0, "total": 0, "cost": 0.0, "latency": []}

    # ... implementation ...

    print(f"Processed {results['total']} rows")
    print(f"Cost: ${results['cost']:.4f} (avg ${results['cost']/results['total']:.6f}/row)")
    print(f"Accuracy: {results['correct']}/{results['total']} ({100*results['correct']/results['total']:.1f}%)")
    print(f"Avg latency: {sum(results['latency'])/len(results['latency']):.2f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=10)
    args = parser.parse_args()
    main(args.sample)
```

### Step 2.3: Run and Capture

Run the experiment and capture output verbatim:

```bash
cd $WORKTREE
python scripts/test_approach_a.py --sample=100 2>&1 | tee results/exp1_output.txt
```

### Step 2.4: Log in POC.md

Add to Experiment Log with **exact reproduce command** and **verbatim output**:

```markdown
### Exp 1: Approach A - Direct Vertex Extraction
**Date:** 2026-01-21 14:30
**Approach:** A

**Reproduce:**
\```bash
cd .worktrees/poc-vertex-html
python scripts/test_approach_a.py --sample=100
\```

**Output:**
\```
Processed 100 rows
Cost: $0.0200 (avg $0.000200/row)
Accuracy: 70/100 (70.0%)
Avg latency: 1.23s
\```

**Learned:** Accuracy too low for production use. Most failures are on nested tables.
**Next:** Try Approach B with HTML preprocessing to flatten tables first.
```

### Step 2.5: Update Known/Unknown

- Check off answered Known Unknowns
- Add any Unknown Unknowns discovered

### Step 2.6: Checkpoint

After each experiment (or every 2-3 experiments), ask:

```
Checkpoint: We've run N experiments.

Current best: Approach [X] with [metrics]
Remaining unknowns: [list]

Options:
1. Continue exploring - [what's next]
2. Pivot - [new direction based on learnings]
3. Terminate - [we know enough to decide]

What would you like to do?
```

---

## Phase 3: Terminate

When user chooses to terminate (or enough is learned):

### Step 3.1: Fill Results Summary

Create comparison table in POC.md:

```markdown
## Results Summary
| Approach | Cost/row | Accuracy | Latency | Verdict |
|----------|----------|----------|---------|---------|
| A: Direct | $0.0002 | 70% | 1.2s | ❌ Too inaccurate |
| B: Preprocess | $0.0003 | 88% | 1.8s | ⚠️ Close but not quite |
| C: Hybrid | $0.0004 | 94% | 2.1s | ✅ Best balance |
```

### Step 3.2: Document Code Artifacts

List what was created:

```markdown
## Code Artifacts
| File | Purpose | Keep? |
|------|---------|-------|
| `scripts/test_approach_a.py` | Baseline direct extraction | No |
| `scripts/test_approach_c.py` | Hybrid approach - winner | Yes, extract |
| `scripts/preprocess_html.py` | HTML flattening utility | Yes, extract |
| `data/sample_100.json` | Test dataset | Reference only |
```

### Step 3.3: Write Verdict

```markdown
## Verdict

**Decision:** Proceed / Pivot / Drop

**Rationale:**
[2-3 sentences explaining why]

**Confidence:** High / Medium / Low
[What would increase confidence?]
```

### Step 3.4: If Proceeding

```markdown
### Path Forward

**Recommended approach:** [C: Hybrid]

**Key learnings for implementation:**
1. HTML must be preprocessed to flatten nested tables
2. Vertex AI gemini-1.5-flash is sufficient (no need for pro)
3. Batch requests in groups of 10 for cost efficiency
4. Expected cost at scale: ~$X/month for Y rows

**Gotchas to avoid:**
1. BQ has 10MB response limit - paginate large results
2. Vertex rate limits - implement exponential backoff

**Extract from POC:**
- `scripts/preprocess_html.py` → `src/utils/html_preprocessor.py`
- `scripts/test_approach_c.py` → reference for implementation

**→ Run:** `/brainstorm "Implement HTML extraction pipeline using Vertex AI hybrid approach"`
```

### Step 3.5: Cleanup Decision

Ask user:

```
POC complete. Cleanup options:

1. Archive learnings, delete worktree
   - Copy POC.md to docs/pocs/ in main repo
   - Remove worktree and branch

2. Keep worktree for reference
   - Worktree stays at .worktrees/poc-vertex-html
   - Can revisit later

3. Delete everything
   - Remove worktree, branch, no archive

Which option?
```

Execute based on choice:

```bash
# Option 1: Archive
cp $WORKTREE/POC.md docs/pocs/$(date +%Y-%m-%d)-$SLUG.md
git add docs/pocs/
git commit -m "docs: archive POC learnings - $SLUG"
git worktree remove $WORKTREE
git branch -D $BRANCH

# Option 2: Keep
echo "Worktree preserved at $WORKTREE"

# Option 3: Delete
git worktree remove $WORKTREE --force
git branch -D $BRANCH
```

---

## POC.md Template

```markdown
# POC: [Title]

**Created:** [date]
**Worktree:** `.worktrees/[slug]`
**Branch:** `poc/[slug]`

## Hypothesis

[What we think might work / what we're trying to learn]

## Success Criteria

- [Concrete, measurable: "< $0.01/row at > 85% accuracy"]

## Fail Criteria

- [When to stop: "If no approach achieves > 70% accuracy"]

## Constraints

- [Budget limits]
- [Time constraints]
- [Tech requirements]

## Evaluation Criteria

| Criterion | Weight | How to Measure |
|-----------|--------|----------------|
| [Cost] | [High/Med/Low] | [$/row] |
| [Accuracy] | [High/Med/Low] | [% vs ground truth] |
| [Latency] | [High/Med/Low] | [seconds/request] |

## Approaches to Test

1. **[Approach A]**: [Brief description]
2. **[Approach B]**: [Brief description]
3. **[Approach C]**: [Brief description]

## Known Knowns

- [Facts we're confident about going in]
- [Established constraints or requirements]

## Known Unknowns

- [ ] [Question we need to answer]
- [ ] [Question we need to answer]
- [ ] [Question we need to answer]

## Test Data

- **Source:** [where the data comes from]
- **Sample size:** [N rows/items]
- **Ground truth:** [how we verify accuracy]
- **Location:** `data/[filename]`

## Quick Verify

```bash
# Re-run all experiments
cd .worktrees/[slug]
./run_all.sh

# Or individually
python scripts/test_approach_a.py --sample=100
python scripts/test_approach_b.py --sample=100
```

---

## Experiment Log

### Exp 1: [Title]
**Date:** [timestamp]
**Approach:** [A/B/C]

**Reproduce:**
```bash
cd .worktrees/[slug]
[exact command]
```

**Output:**
```
[verbatim output]
```

**Learned:** [insight from this experiment]
**Next:** [what this suggests we try next]

---

## Unknown Unknowns (Discovered)

- [Surprises discovered during exploration]

## Results Summary

| Approach | Cost | Accuracy | Latency | Verdict |
|----------|------|----------|---------|---------|
| A | | | | |
| B | | | | |

## Code Artifacts

| File | Purpose | Keep? |
|------|---------|-------|
| `scripts/[name].py` | [what it does] | [Yes/No] |

## Verdict

**Decision:** Proceed / Pivot / Drop

**Rationale:**
[Why this decision]

**Confidence:** High / Medium / Low

### If Proceeding

**Recommended approach:** [which]

**Key learnings for implementation:**
1. [must-have]
2. [must-have]

**Gotchas to avoid:**
1. [learned the hard way]

**Extract from POC:**
- `[source]` → `[destination]`

**→ Run:** `/brainstorm "[description for next phase]"`
```

---

## Resume Mode: `--resume`

When invoked with `--resume <worktree-path>`:

1. Verify worktree exists
2. Read `$WORKTREE/POC.md`
3. Display current state:
   ```
   Resuming POC: [title]

   Experiments run: N
   Last experiment: [title] ([date])
   Known unknowns remaining: M

   Current best: Approach [X] - [metrics]

   What would you like to do?
   1. Run another experiment
   2. Review/update an experiment
   3. Terminate and decide
   ```

---

## Status Mode: `--status`

When invoked with `--status <worktree-path>`:

1. Read `$WORKTREE/POC.md`
2. Display summary:
   ```
   POC: [title]
   Status: In Progress

   Experiments: N
   Approaches tested: A, B
   Approaches remaining: C

   Current leader: Approach B
   - Cost: $X/row
   - Accuracy: Y%
   - Latency: Zs

   Known unknowns: M remaining
   Unknown unknowns: K discovered

   Worktree: .worktrees/[slug]
   Branch: poc/[slug]
   ```

---

## Principles

1. **Reproducibility over trust** — Every result must have a reproduce command
2. **Verbatim output** — Don't paraphrase results, capture actual output
3. **One question at a time** — Don't overwhelm during clarification
4. **Checkpoints prevent rabbit holes** — Pause regularly to assess
5. **Learnings survive the code** — POC.md is the artifact, code is disposable
6. **Clean exit** — Always offer to archive or cleanup, never leave orphan worktrees

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Worktree already exists | Ask: resume or create new? |
| Experiment script fails | Capture error output, log as failure, continue |
| User wants to pivot | Update hypothesis, keep experiment log, continue |
| Dependencies missing in worktree | Set up or symlink from main repo |
| User abandons mid-POC | Offer cleanup options |
