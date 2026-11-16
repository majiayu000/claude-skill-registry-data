---
name: skill-factory
description: >
  Analyze session work and automatically convert reusable patterns into Claude Code skills.
  Use when: "세션을 스킬로", "스킬 만들어", "이거 스킬로", "skill factory",
  "이 작업 자동화해", "스킬 추출", "make this a skill", "extract skill",
  "convert to skill", "스킬 팩토리", "자동 스킬 생성".
  Differs from skill-creator (archived) and manage-skills (drift detection):
  this skill actively analyzes sessions, checks for duplicates, and creates skills via Agent Teams.
disable-model-invocation: true
argument-hint: "[--dry-run] [--no-team] [--target name] [--scope global|project]"
---

# Skill Factory

Automated pipeline: session analysis -> duplicate check -> skill creation.
Requires: Python 3.8+, bash, git. Agent Teams path requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

| Existing Skill | Role | skill-factory Difference |
|----------------|------|--------------------------|
| skill-creator (archived) | Manual 6-step guide | Automated pipeline |
| manage-skills | Drift detection (verify-* skills) | Proactive skill generation (manage-skills verifies existing; skill-factory creates new) |
| continuous-learning | Passive pattern extraction | On-demand + team execution |

## Parameter Parsing

Parse `$ARGUMENTS` for flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Analyze and report only, no file creation |
| `--no-team` | false | Run sequentially without Agent Teams |
| `--target` | (auto) | Specific pattern name to extract |
| `--scope` | global | `global` (~/. claude/skills/) or `project` (.claude/skills/) |

If no arguments, run full auto-detection pipeline.

## Phase 1: Session Analysis

Collect what happened in this session:

```bash
# Uncommitted changes
git diff HEAD --name-only 2>/dev/null

# Recent commits on current branch
git log --oneline -20 2>/dev/null

# Branch diff from main
git diff main...HEAD --name-only 2>/dev/null
```

From collected changes, identify **candidate patterns** - repeatable workflows that appeared:

1. **Multi-step sequences** - 3+ actions performed in consistent order
2. **Tool combinations** - Specific tools used together (e.g., Grep + Read + Edit)
3. **Domain procedures** - File types or directories accessed with specific operations
4. **Repeated transformations** - Same type of change applied to multiple files

If `--target` is specified, focus analysis on that named pattern only.

For each candidate, produce a JSON entry (internal, not shown to user):

```json
{
  "name": "pattern-name",
  "description": "What was done repeatedly",
  "files": ["path/a.ts", "path/b.ts"],
  "steps": ["Step1", "Step2", "Step3"],
  "step_count": 3
}
```

Present findings to user:

```
Session Analysis Complete

Candidate Patterns Found: N

1. [pattern-name] - "Description of what was done repeatedly"
   Files: path/a.ts, path/b.ts (N files)
   Steps: Step1 -> Step2 -> Step3

2. [pattern-name] - "Description"
   ...

Which patterns should become skills? (select or 'all')
```

Wait for user selection before proceeding.

## Phase 2: Similarity Check

For each selected pattern, check against existing inventory.

**Step 1: Scan inventory**
```bash
bash $HOME/.claude/skills/skill-factory/scripts/scan-inventory.sh --scope all > /tmp/sf-manifest.json
```

**Step 2: Score similarity**
```bash
python3 $HOME/.claude/skills/skill-factory/scripts/similarity-scorer.py \
  --candidate "<pattern description>" \
  --candidate-name "<pattern-name>" \
  --manifest /tmp/sf-manifest.json \
  --top 3
```

**Step 3: Apply decision logic** (see [references/decision-tree.md](references/decision-tree.md))

Present results to user:

```
Similarity Check Results

Pattern: "pdf-batch-edit"
  Top match: nano-pdf (score: 0.72) -> MERGE
  Recommendation: Extend nano-pdf with batch operations

Pattern: "config-updater"
  Top match: init-project (score: 0.45) -> UPDATE
  Recommendation: Add config-update subsection to init-project

Pattern: "api-load-test"
  Top match: e2e (score: 0.24) -> CREATE
  Recommendation: Create new skill

Action for each pattern? (CREATE / UPDATE / MERGE / SKIP)
```

Wait for user decision per pattern.

## Phase 3: Blueprint

For each CREATE/UPDATE/MERGE decision, design the skill structure.

### CREATE Blueprint

Select template type from [references/skill-templates.md](references/skill-templates.md):
- **Workflow** for sequential processes
- **Task/Tool** for operation collections
- **Reference** for domain knowledge
- **Verification** for automated checks

Generate blueprint:

```
Blueprint: api-load-test

Type: Workflow
Scope: global (~/.claude/skills/)
Structure:
  api-load-test/
  ├── SKILL.md (~200 lines)
  │   ├── Frontmatter: name, description with triggers
  │   ├── Overview
  │   ├── Prerequisites
  │   ├── Workflow (4 steps)
  │   └── Output Format
  └── scripts/
      └── run-load-test.sh

Key sections:
  1. Target URL configuration
  2. Load profile definition
  3. Test execution
  4. Results analysis

Approve this blueprint? (y/n/edit)
```

Wait for user approval.

### UPDATE Blueprint

For UPDATE verdicts (score 0.3-0.6), plan a lightweight addition to the existing skill:

```
UPDATE Blueprint: config-updater -> init-project

Target skill: ~/.claude/skills/init-project/SKILL.md
Action: Add subsection "## Config Update" with steps
Estimated diff: +20-40 lines in existing SKILL.md
```

### MERGE Blueprint

For MERGE verdicts (score 0.6-0.8), plan a significant extension of the existing skill:

```
MERGE Blueprint: pdf-batch-edit -> nano-pdf

Target skill: ~/.claude/skills/nano-pdf/SKILL.md
Sections to add: "## Batch Operations" (new workflow section)
Scripts to add: scripts/batch-process.sh
Estimated diff: +60-100 lines in SKILL.md, +1 script
```

## Phase 4: Execution

Two paths based on `--no-team` flag and Agent Teams availability.

Check Agent Teams availability:
```bash
[ "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-0}" = "1" ] && echo "teams" || echo "no-team"
```
If `--no-team` is set or env var is missing/0, use Path B automatically.

### Path A: Agent Teams (default)

Read [references/team-composition.md](references/team-composition.md) for full team details.

**Team: 3 teammates (tami, jiwon, duri)**

```
TeamCreate -> "skill-factory-run"

TaskCreate -> tami's analysis tasks (T1-T6)
TaskCreate -> jiwon's creation tasks (T7-T12, blocked by T6)
TaskCreate -> duri's validation tasks (T13-T18, blocked by T12)

Task -> tami (Explore, sonnet, blue)
  "Analyze session, run scan-inventory.sh, run similarity-scorer.py, report findings"

Task -> jiwon (general-purpose, sonnet, green)
  "For CREATE: read skill-templates.md, create SKILL.md + resources based on blueprint"
  "For UPDATE/MERGE: read target skill, apply diff from blueprint, add new sections/scripts"

Task -> duri (general-purpose, sonnet, yellow)
  "Run validate-skill.sh, verify triggers, register skill"
```

Pipeline:
1. **tami** completes analysis -> reports to lead
2. Lead confirms with user (Checkpoint 1-2)
3. **jiwon** creates skill files -> reports to lead
4. Lead confirms with user (Checkpoint 3)
5. **duri** validates and registers -> reports to lead
6. Lead confirms with user (Checkpoint 4)
7. Shutdown all teammates, TeamDelete

### Path B: Sequential (--no-team)

Execute the same phases inline without Agent Teams:

1. Run `scan-inventory.sh` and `similarity-scorer.py` directly
2. **Checkpoint 1-2**: Present similarity results, ask user for CREATE/UPDATE/MERGE/SKIP per pattern
3. Design blueprint based on template selection
4. **Checkpoint 3**: Present blueprint, wait for user approval
5. Create/update skill directory and files based on approved blueprint
6. Run `validate-skill.sh` to verify
7. **Checkpoint 4**: Present validation results, ask user to register or edit
8. Register and log

### --dry-run Mode

Stop after Phase 3 (blueprint). Print the blueprint and exit without creating files:

```
DRY RUN COMPLETE

Patterns analyzed: N
Decisions: X CREATE, Y MERGE, Z SKIP
Blueprints generated: X

No files were created. Remove --dry-run to execute.
```

## Phase 5: Registration

After validation passes:

1. **Log creation** - Append to `~/.claude/skill-factory.log`:
   ```
   [2026-02-18T14:30:00] CREATED api-load-test (global) from session patterns
   [2026-02-18T14:30:00] MERGED batch-operations into nano-pdf
   ```

2. **Scope placement**:
   - `--scope global`: `~/.claude/skills/<name>/`
   - `--scope project`: `.claude/skills/<name>/`

3. **Optional CLAUDE.md update**: If project-scoped, offer to add skill reference to project CLAUDE.md.

## Output Format

Final report after all patterns are processed:

```
Skill Factory Report

Session: <branch-name or "main">
Patterns found: N
Patterns processed: M

Results:
  CREATED: api-load-test (global) - 4 files, 180 lines
  MERGED:  batch-ops into nano-pdf - 2 sections added
  SKIPPED: data-transform (0.85 match with data-research)

Files created/modified:
  ~/.claude/skills/api-load-test/SKILL.md
  ~/.claude/skills/api-load-test/scripts/run-load-test.sh
  ~/.claude/skills/nano-pdf/SKILL.md (updated)

Validation: ALL PASS
Log: ~/.claude/skill-factory.log

Next steps:
  Test the new skill: /api-load-test
  Review: cat ~/.claude/skills/api-load-test/SKILL.md
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No git history | Analyze only staged/unstaged changes |
| No patterns found | "No reusable patterns detected. Try after a more complex session." |
| scan-inventory.sh fails | Fall back to manual inventory (glob SKILL.md files) |
| similarity-scorer.py fails | Skip similarity check, default to CREATE |
| Agent Teams unavailable | Auto-fallback to `--no-team` mode |
| validate-skill.sh fails | Show errors, let user fix or cancel |
| User cancels at checkpoint | Abort gracefully, no partial files left |

## Related Files

| File | Purpose | When to Read |
|------|---------|--------------|
| [scripts/scan-inventory.sh](scripts/scan-inventory.sh) | Scan all skills/commands/agents to JSON | Phase 2 - always |
| [scripts/similarity-scorer.py](scripts/similarity-scorer.py) | 4-dim similarity scoring | Phase 2 - per pattern |
| [scripts/validate-skill.sh](scripts/validate-skill.sh) | Validate created skill structure | Phase 5 - after creation |
| [references/decision-tree.md](references/decision-tree.md) | CREATE/UPDATE/MERGE/SKIP logic | Phase 2 - for decisions |
| [references/team-composition.md](references/team-composition.md) | tami/jiwon/duri team setup | Phase 4 - Agent Teams path |
| [references/skill-templates.md](references/skill-templates.md) | Skill type templates | Phase 3 - blueprint design |
