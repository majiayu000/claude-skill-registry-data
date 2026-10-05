---
name: peer-review
description: Orchestrates rigorous peer review with three reviewers (methodology+completeness, statistics, impact+provenance). Manages revision cycles until unanimous acceptance.
user-invocable: true
---

# Peer Review Workflow

Execute rigorous peer review of synthesized papers.

## The Three Reviewers

Spawn three reviewer subagents in parallel. Each has expanded focus.

### 1. Methodology Reviewer
Focus: Rigor + Completeness
- Arithmetic consistency (do numbers add up?)
- Mock data detection (np.random without disclosure = REJECT)
- Reproducibility (can someone replicate from description?)
- Honest failure reporting
- **All RQs addressed** (check against world_model.json)
- **All artifacts used** (no orphaned experiment results)
- **PRISMA numbers consistent**

### 2. Statistics Reviewer
Focus: Statistical correctness
- Number verification against source files
- Appropriate statistical tests for data type
- Effect sizes and confidence intervals (not just p-values)
- Multiple testing correction where needed
- **Figures reference real data files**

### 3. Impact Reviewer
Focus: Contribution + Provenance
- Scope vs claims honesty
- Failure disclosure (are negative results hidden?)
- Overclaiming detection
- Abstract matches actual results
- **Every claim has DOI + exact quote**
- **Source types match confidence** (blog ≤ 0.7, article ≤ 1.0)
- **Spot-check 3-5 quotes are verbatim**
- **Run DOI validation**: `python3 .claude/hooks/validate-doi.py`

## MANDATORY: Compile PDF Before Review

**Before spawning reviewers, compile the PDF:**

```bash
cd $SESSION_DIR/synthesis
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex

# Verify PDF exists and has content
ls -lh paper.pdf  # Should be > 50KB
```

**Why compile first?**
- LaTeX errors block reviewer assessment
- Some issues (figure placement, citation format, encoding) only visible in PDF
- Reviewers should see what the reader will see

**If compilation fails:** Fix LaTeX errors before spawning reviewers. Common fixes:
- Missing packages: `\usepackage{...}`
- Undefined citations: Check references.bib has all cited keys
- Encoding issues: Ensure UTF-8 and escape special chars

## Spawning Reviewers

```
# Spawn all 3 reviewers IN PARALLEL (single message, 3 Task tool calls)

# 1. Methodology reviewer (includes completeness checks)
Task: Spawn reviewer-methodology subagent
Prompt: "Review paper.tex AND paper.pdf for methodological rigor AND completeness.
Check: arithmetic, mock data, reproducibility.
Also verify: all RQs addressed, all artifacts used, PRISMA consistent.
Check PDF for: formatting issues, figure placement, readability.
Save methodology_review.json with verdict and issues."

# 2. Statistics reviewer
Task: Spawn reviewer-statistics subagent
Prompt: "Review paper.tex AND paper.pdf for statistical correctness.
Verify numbers match source files, appropriate tests, effect sizes.
Check figures reference real data files.
Check PDF for: figure rendering, table formatting, equation display.
Save statistics_review.json with verdict and issues."

# 3. Impact reviewer (includes provenance checks)
Task: Spawn reviewer-impact subagent
Prompt: "Review paper.tex AND paper.pdf for contribution AND provenance.
Check: scope vs claims, failures disclosed, no overclaiming.
Also verify: every claim has DOI+quote, spot-check 3 quotes verbatim.
Check PDF for: citation formatting, reference list completeness.
Run: python3 .claude/hooks/validate-doi.py
Save impact_review.json with verdict and issues."
```

## External Validation (Recommended)

Include at least one Codex reviewer:

```bash
codex exec --full-auto -m gpt-5.2-codex -o codex_review.txt \
  "Review this paper for scientific validity. Check:
   1. Do claims match evidence?
   2. Are limitations honest?
   3. Any overclaiming?

   Paper: $(cat paper.tex)

   Output JSON with verdict (ACCEPT/REVISE/REJECT) and issues."
```

## Acceptance Criteria

**NOT majority vote. Unanimous acceptance required.**

- All THREE reviewers must give ACCEPT
- If ANY reviewer gives REVISE/REJECT → revision cycle
- Codex reviewer has veto power if included

## Revision Cycle

If not unanimous acceptance:

1. **Collect all issues** from reviewer JSONs
2. **Resume synthesizer** using saved agent ID (preserves context)
3. Synthesizer must address EVERY issue:
   - **FIX**: Make the change
   - **REBUT**: Explain why reviewer is wrong (with evidence)
   - **ACKNOWLEDGE**: If can't fix, explain in Limitations
4. Synthesizer creates `revision_response.md`
5. **RE-COMPILE PDF after revisions:**
   ```bash
   cd $SESSION_DIR/synthesis
   pdflatex -interaction=nonstopmode paper.tex
   bibtex paper
   pdflatex -interaction=nonstopmode paper.tex
   pdflatex -interaction=nonstopmode paper.tex
   ```
6. **Resume same reviewers** using saved agent IDs to verify fixes (they review updated PDF too)

## Agent ID Tracking (MANDATORY)

**⚠️ This is NOT optional. Without agent IDs, revision cycles spawn fresh agents that don't remember their prior analysis.**

### Step 1: CREATE the tracking file FIRST (before spawning)

```bash
mkdir -p $SESSION_DIR/peer_review
cat > $SESSION_DIR/peer_review/agent_ids.json << 'EOF'
{
  "synthesizer": null,
  "methodology": null,
  "statistics": null,
  "impact": null,
  "cycle": 1
}
EOF
```

### Step 2: SAVE agent IDs IMMEDIATELY after spawning

**The Task tool returns an `agent_id` when an agent completes.** You MUST save it:

```bash
# After each Task tool completes, read the agent_id from the result
# Then immediately update the tracking file:

# Example - after methodology reviewer completes with ID "a7df9f1":
jq '.methodology = "a7df9f1"' $SESSION_DIR/peer_review/agent_ids.json > tmp.json && \
  mv tmp.json $SESSION_DIR/peer_review/agent_ids.json

# Also update world_model.json for cross-session visibility:
jq '.agents["reviewer-methodology"] = {"id": "a7df9f1", "status": "completed"}' \
  $SESSION_DIR/world_model.json > tmp.json && mv tmp.json $SESSION_DIR/world_model.json
```

### Step 3: USE saved IDs when resuming for revision

**In revision cycles, you MUST use the `resume` parameter:**

```
Task tool with:
  resume: "<saved-agent-id>"   # ← Use the saved ID, NOT a fresh spawn
  prompt: "Continue from where you left off. Review revision_response.md
    and verify the following fixes were made: [list issues from review]
    Re-review paper.tex and paper.pdf. Update your review JSON."
```

### Why This Matters

| Without Resume | With Resume |
|----------------|-------------|
| Fresh agent re-reads entire paper | Agent remembers prior analysis |
| May raise already-fixed issues | Knows what was already fixed |
| Circular feedback ("you already fixed this") | Productive revision cycle |
| Wasted tokens re-processing | Efficient targeted review |

### Common Failure Mode

**If you see reviewers raising the same issues in cycle 2 that were fixed in cycle 1:**
→ You forgot to use `resume` with the saved agent ID
→ The reviewer is a fresh spawn with no memory

**Check yourself:** Before every revision cycle reviewer spawn, verify:
1. `agent_ids.json` exists and has non-null IDs
2. Your Task tool call includes `resume: "<id>"`

## Convergence Detection

If 3 revision cycles with >70% similarity in issues:
- **Escalate to user** - something is stuck
- Don't keep looping indefinitely

## Review File Locations

```
$SESSION_DIR/peer_review/
├── methodology_review.json     # Rigor + completeness
├── statistics_review.json      # Numbers + figures
├── impact_review.json          # Contribution + provenance
├── agent_ids.json              # For resume tracking
├── codex_review.txt (optional)
├── reviewer_feedback_for_revision.json  # Combined for synthesizer
└── revision_response.md  # Synthesizer's responses
```

## Issue Format

Each reviewer issue must have:
```json
{
  "id": "METH-1",
  "severity": "major|minor|critical",
  "location": "Section 2.1, line 45",
  "issue": "Clear description",
  "required_action": "What to do",
  "verification": "How to verify fix"
}
```

## Workflow Loop

```
1. Spawn 3 reviewers (parallel, single message)
2. Wait for all reviews (poll for completion)
3. Check verdicts:
   - All 3 ACCEPT? → Done, paper passes
   - Any REVISE/REJECT? → Revision cycle
4. Revision cycle:
   a. Combine feedback for synthesizer
   b. Resume synthesizer for revisions (use saved agent ID)
   c. Resume reviewers to verify (use saved agent IDs)
   d. Go to step 3
5. Max 3 cycles, then escalate
```

**Rigorous review. Actionable feedback. Unanimous acceptance.**
