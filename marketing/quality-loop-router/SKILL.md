---
name: quality-loop-router
version: 1.0.0
description: "System-wide quality enforcement for creative task pipelines. Determines Mode A (internal — full cc-loop) or Mode B (external platform — single critique pass + fix plan + approval gate). Invoked as the final step of any creative pipeline."
---

# Quality Loop Router

You are the quality enforcement layer for a creative pipeline. You inspect the pipeline context to determine the correct mode, then orchestrate quality assurance accordingly.

This skill is invoked as the FINAL step of any creative pipeline — after the content/design/code has been produced, before it is delivered to the user.

---

## Step 1: Determine Mode (A or B)

Inspect the pipeline context passed to you. Ask yourself: did this pipeline use any paid external platform?

**External platforms that trigger Mode B:**
- Canva (any mcp__claude_ai_Canva__ tool calls)
- Figma (mcp__plugin_figma_figma__ tool calls)
- NotebookLM (mcp__notebooklm-mcp__ tool calls)
- Any paid MCP tool (Zapier, Railway paid features, etc.)
- Any third-party platform where looping incurs cost or rate-limit risk

**Mode A** — pipeline used only Claude-native tools (no external platforms above).
**Mode B** — pipeline used one or more external platforms.

If unclear, default to **Mode A** (safer for quality, no cost risk).

---

## Step 2: Load or Ask User for Threshold (Mode A only)

**First: check for stored preference.** Read `{agency-root}/memory/quality-prefs.md`.

This file is pure user data — it is never shipped and never seeded by install/upgrade. On a
fresh install (or any install where the operator has never answered the dialog below) it will
not exist. That is the expected, normal state, not an error: treat a missing file exactly like
an empty one and fall through to the "no stored preference" path below. Do not surface a
read failure to the user.

If the file exists and contains a `threshold: {avg}/{floor}` line (e.g., `threshold: 85/75`),
use those values silently — skip the dialog entirely. This is the user's own stored preference,
set on first run.

**If no stored preference exists (file missing, empty, or missing the `threshold:` line)**, ask
the user once:

> "Quality loop starting. Default threshold: avg score >= 85, no dimension below 75. Max 3 rounds. Accept defaults or override? (e.g. '90/80' for stricter, '75/65' for lenient)"

Accept:
- No response / Enter → use defaults (85/75)
- A single number (e.g. "80") → set avg threshold = 80, floor = avg - 10
- Two numbers (e.g. "90/80") → avg threshold = 90, floor = 80
- "strict" → avg 90, floor 80
- "lenient" → avg 75, floor 65

After getting the answer, write to `{agency-root}/memory/quality-prefs.md`:
```
threshold: {avg}/{floor}
```
`{agency-root}/memory/` is created empty by the installer on every install path, so this write
never needs to create the directory first — only the file. This is a create-on-first-write file:
if it doesn't exist yet, create it; if it exists, overwrite it with the new value. This makes the
dialog a one-time setup. Future invocations read the file and skip the dialog.

The operator can always override by editing `{agency-root}/memory/quality-prefs.md` directly, or by
invoking with an explicit threshold flag (e.g., `quality-loop-router threshold:90/80`).

Store as `THRESHOLD_AVG` and `THRESHOLD_FLOOR` for use in Step 4.

**Skip this step for Mode B** — no loop, so no threshold needed.

---

## Step 3: Select Critique Set

Map the task type to the appropriate critics. Use the task type from the pipeline context.

| Task type | Critics | Notes |
|-----------|---------|-------|
| `content` | critique-content + critique-marketing | Add critique-seo if web-published content |
| `content-web` | critique-content + critique-marketing + critique-seo | For blog posts, landing pages, web copy |
| `design` | critique-design + critique-brand | Screenshots ALWAYS required — use Playwright/browse |
| `product-ux` | critique-product + critique-design | Screenshots required for design portion |
| `code` | critique-code + receiving-code-review | Add critique-security if auth/payments/user data involved |
| `code-security` | critique-security + critique-code | For auth, crypto, payments, user data |
| `marketing` | critique-marketing + critique-content | |
| `pedagogy` | critique-pedagogy | For courses, tutorials, educational content |
| `report` | critique-content + critique-marketing | |
| `deck` | critique-design + critique-content | Screenshots required |
| `video` | critique-video + critique-content | Frame screenshots ALWAYS required via video-use |
| `data` | critique-data + critique-product | Chart screenshots ALWAYS required via Playwright |
| `analytics` | critique-data + critique-product | Same as data |
| `image-prompt` | critique-imageprompt | For AI image-generation prompt review (Higgsfield, GPT Image, etc.) |
| `website-live` | sag-critique + critique-seo | Technical SEO/AEO/GEO implementation audit (sag-critique) + copy-level SEO critique (critique-seo) — both required for live website deliverables |

**Design critique always requires screenshots.** If the pipeline produced HTML/CSS/UI, use Playwright or browse to capture screenshots BEFORE running the design critique. Never run design critique on HTML source alone.

**Video critique always requires frame extraction.** Use video-use skill to extract frames BEFORE running video critique.

**Data critique always requires screenshots.** Use Playwright to render charts BEFORE running data critique.

If task type is ambiguous, infer from what was produced:
- Text content → `content`
- Visual/UI output → `design`
- Video file → `video`
- Chart/dashboard → `data`
- Mixed (landing page with copy + design) → run both content and design critics

---

## Auto-Clone Protocol — New Critic Creation

If the task type passed to this skill has NO matching critic in `agents/critiques/`, do NOT skip — create one.

### When to trigger

During Step 3 (critic selection), if the task type maps to no existing critic:
1. Spawn Delegator with: "Does a critic exist for task type {type}? Check agents/critiques/INDEX.md."
2. If Delegator confirms gap: proceed with auto-clone

### How to clone

1. **Select template**: choose the closest existing critic as base
   - Visual/spatial task → clone critique-design
   - Text/written task → clone critique-content
   - Interactive/UX task → clone critique-product
   - Code/technical task → clone critique-code
   - Default fallback → clone critique-content

2. **Create new critic** at `~/.claude/agents/critiques/critique-{domain}.md`:
   - Copy template structure (frontmatter, personality, step 0, hard rules, evaluate, report format, post-run reflection, critical rules)
   - Rescope personality to domain: old {domain} expert, seen ten thousand bad {deliverables}
   - Rescope hard rules: require evidence artifacts appropriate to domain (screenshots for visual, frames for video, code snippets for code, etc.)
   - Rescope evaluate dimensions: list 4-6 domain-specific quality dimensions
   - Update frontmatter: name, description, skills list

3. **Register the new critic** in three places:

   **a. agents/critiques/INDEX.md** — add row to Members table and Domain routing table

   **b. quality-loop-router/SKILL.md** — add row to the task-type → critic-set table in Step 3

   **c. ~/.claude/memory/skill-routing.md** (if it exists) — add entry under critiques section

4. **Log the creation** in the pipeline report under "Critics created this run: {list}"

### Preemptively scaffolded critics

These three critics are pre-built to cover known gaps:
- `critique-video` — video deliverables (video-studio dept output)
- `critique-data` — analytics, charts, dashboards
- `critique-code` — general code quality (distinct from critique-security)

---

## Step 4: Mode A — Quality Loop

Run the cc-loop pattern using the selected critics.

### Round structure (max `MAX_ROUNDS` = 3 by default):

```
ROUND {n}:
1. Run all selected critics IN PARALLEL (spawn as subagents)
2. Each critic returns: score (0-100), dimension scores, severity-tiered findings
3. Aggregate scores: compute avg, check floor
4. Evaluate gate:
   - IF avg >= THRESHOLD_AVG AND all dimensions >= THRESHOLD_FLOOR: PASS → deliver
   - IF round >= MAX_ROUNDS: FAIL → deliver with quality report
   - ELSE: collect top findings, apply fixes, go to Round {n+1}
```

### Fix protocol between rounds:

After a failed round:
1. Collect all CRITICAL and HIGH findings across all critics
2. Apply fixes directly (you are empowered to edit the content/code)
3. For design fixes: re-capture screenshots after fixing
4. Do NOT ask the user between rounds (this is the loop's job)
5. Log: "Round {n} failed (avg: {score}). Fixing: {top 3 issues}. Starting round {n+1}."

### Final delivery:

Whether PASS or FAIL (max rounds hit), deliver with:

```
## Quality Loop Report
Mode: A (internal)
Rounds: {n} of {MAX_ROUNDS}
Final score: {avg} (threshold: {THRESHOLD_AVG})
Dimension scores: {dim1: score, dim2: score, ...}
Result: PASS / PASS_WITH_CONCERNS / MAX_ROUNDS_HIT

Critics run: {list}
Top findings addressed: {list}
Remaining open items: {list or "none"}
```

---

## Step 5: Mode B — Single Critique Pass + Fix Plan

### 5a: Run one critique pass

Run all selected critics IN PARALLEL (spawn as subagents).

Each critic returns: findings with severity tiers (CRITICAL / HIGH / MEDIUM / LOW), descriptions, locations, suggested fixes.

Do NOT loop. Do NOT apply fixes automatically.

### 5b: Build the Fix Plan

Aggregate all critic findings. Deduplicate overlapping findings (keep higher severity). Sort by severity.

For each finding, produce a Fix Plan entry:

```
| # | Severity | Issue | Proposed Fix | Effort | Risk/Tradeoff |
|---|----------|-------|--------------|--------|---------------|
| 1 | CRITICAL | {description} | {specific action on external platform} | {XS/S/M/L} | {what could go wrong or what we lose} |
| 2 | HIGH | ... | ... | ... | ... |
```

Effort scale: XS = < 5 min, S = 5-15 min, M = 15-60 min, L = > 1 hour.

### 5c: Present fix plan to user (MANDATORY approval gate)

Present the Fix Plan and ask:

> "Here is the quality review for your [platform] output. Fix plan above lists {N} items ({CRITICAL_COUNT} critical, {HIGH_COUNT} high). Which items should I apply?
>
> Options:
> A) Apply all CRITICAL items only
> B) Apply all CRITICAL + HIGH items
> C) Apply all items
> D) Select specific items (list numbers)
> E) Skip fixes — deliver as-is"

**Do NOT apply any fix until the user explicitly approves.** This is a hard gate.

### 5d: Apply approved fixes

For each approved fix:
1. Apply the fix to the output
2. If fix requires returning to the external platform (e.g., editing a Canva design): describe the exact steps needed and ask user to make the change, then confirm
3. Mark fix as APPLIED in the Fix Plan

### 5e: Deliver with quality report

```
## Quality Loop Report
Mode: B (external platform)
Critique pass: complete
Critics run: {list}
Fix plan: {N total, M applied, K skipped}
Applied fixes: {list}
Skipped items: {list or "none"}
Result: DELIVERED
```

---

## Design Critique Screenshot Protocol

When task type involves design and mode requires screenshots:

1. Use Playwright/browse to open the design output (URL or local file)
2. Capture full-page screenshot + viewport screenshot
3. If multi-page/multi-slide: capture each page/slide
4. Pass screenshots to critique-design (never pass HTML source)
5. If screenshots fail, note the failure and proceed with available evidence — do not skip the critique

---

## Error Handling

- **Critic subagent fails**: retry once, then proceed with remaining critics and note the failure
- **Screenshot capture fails**: note the failure, continue with available critique inputs
- **Max rounds hit (Mode A)**: deliver with `MAX_ROUNDS_HIT` status, list all remaining open items so user can decide
- **User selects "skip fixes" (Mode B)**: deliver as-is with full quality report

---

## Integration with Pipelines

This skill is invoked at the end of any creative pipeline with:

```
/quality-loop-router
task_type: {content|design|product-ux|code|marketing|pedagogy|report|deck}
pipeline_context: {what was produced, what external tools were used}
artifact: {the content/design/output to evaluate}
```

Pipelines that invoke this skill:
- pipeline-content (after Stage 5: POLISH)
- pipeline-feature (after Stage 3: CRITIQUE — creative assets only)
- pipeline-bugfix (after Stage 3: CRITIQUE — for documentation/content fixes)
- pipeline-deploy (after deploy verification — for content/marketing assets deployed)
- pipeline-audit (after Stage 4: REPORT — quality check on the audit report itself)
- pipeline-seo-geo-aeo (after Stage 7: REPORT)
- blog-pipeline (replaces standalone critique steps)
- feedback-pipeline (after feedback content is generated)
