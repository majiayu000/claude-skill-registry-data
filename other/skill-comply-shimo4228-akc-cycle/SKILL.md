---
name: skill-comply
description: "Measure whether a skill, rule or agent definition is actually followed. Use when a rule's or skill's real adherence is in question, or right after adding one."
compatibility: Requires Python 3.11+ and uv. Developed and tested on Claude Code; portable to other Agent Skills-compatible agents.
origin: shimo4228
user-invocable: true
---

# skill-comply: Automated Compliance Measurement

Measures whether coding agents actually follow skills, rules, or agent definitions by:
1. Auto-generating expected behavioral sequences (specs) from any .md file
2. Auto-generating scenarios with decreasing prompt strictness (supportive → neutral → competing), to show
   whether the target is followed even when the prompt does not support it
3. Running `claude -p` and capturing tool call traces via stream-json
4. Classifying tool calls against spec steps using LLM (not regex)
5. Checking temporal ordering deterministically
6. Generating self-contained reports with spec, prompts, and timelines

It measures runtime adherence only. A static quality audit is skill `skill-stocktake` / `rules-stocktake`, a reference-integrity
check is skill `skill-health`, and a with/without ablation of a skill's effect is skill `skill-creator` §5.

## Supported Targets

- **Skills** (`skills/*/SKILL.md`): Workflow skills like search-first
- **Rules** (`rules/common/*.md`): Mandatory rules like testing.md, security.md, debugging.md
- **Agent definitions** (`agents/*.md`): accepted as a target, but invocation is **not observable** today — every child
  runs with `Agent` denied (`scripts/child_settings.py` `DENIED_TOOLS`), so a step that expects an agent call cannot be seen

## Usage

> Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

```bash
# Full run
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run ~/.claude/rules/common/testing.md

# Dry run (spec + scenarios only: the two generation `claude -p` calls run, no agent runs)
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run --dry-run ${CLAUDE_PLUGIN_ROOT}/skills/search-first/SKILL.md

# Custom models
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run --gen-model haiku --model sonnet --classifier-model sonnet <path>

# Back to serial (when you hit rate limits)
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run --concurrency 1 <path>

# Only for specs that need Bash (off by default — read "Trust boundary" below first)
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run --allow-bash <path>

# Reuse a saved spec to compare across runs (skips LLM regeneration)
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run --spec results/<skill-name>.spec.yaml <path>
```

**Pinning the spec and comparing across runs**: the spec is the "exam paper". Each LLM
generation changes both the number of required steps and the ordering constraints, so the
generated spec is automatically saved to `results/<skill-name>.spec.yaml`
(not gitignored — it can be version-controlled). When re-measuring the same skill, load it
with `--spec` to pin the questions so scores become comparable. The next generating run
overwrites the file of the same name, so copy any spec you want to keep as a baseline under another name.
Note that scenario prompts are still LLM-generated and vary on every run — pinning for run-to-run
comparison stops at the spec; scenario non-determinism is out of scope.

## Run time and reading progress

The three scenarios are independent of each other (separate prompts, separate sandboxes, separate processes),
so by default all three run at once. Wall time is **the slowest single scenario**, not the sum of the three.
Classification (grading) is also per scenario, so it runs alongside them. The two stages spec generation → scenario
generation stay serial because the later stage consumes the earlier stage's output.

Parallelism does not change scores or reports. Completion order is used only for progress display;
the report is always assembled in supportive → neutral → competing order.
`--concurrency 1` returns to fully serial execution.

**Progress goes to stderr, results go to stdout**, so piping stdout does not hide progress:

```bash
# Progress is visible. Only stdout goes into tail; stderr reaches the terminal directly
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run <path> | tail -40

# Also keep progress in the log
uv run --frozen --project "${CLAUDE_SKILL_DIR}" python -m scripts.run <path> 2>&1 | tee run.log
```

**With `2>&1 | tail -40` you see nothing until the run ends** — `tail` without `-f` prints only at end of
input. Use `tee` to watch progress.

When even one scenario fails (e.g. the child process exits abnormally),
that scenario is not counted as 0% but reported to stderr as a "measurement failure", and the exit code is 1.
Reports for the remaining scenarios are saved as usual.

## Target kinds and what can be measured

Where the target lives determines whether the child can see it. **If you measure while it is invisible,
you are measuring not skill compliance but "the bare behavior of an agent that does not have the skill".**

| Target | Visible to the child? | Measurement |
|---|---|---|
| global skill (`~/.claude/skills/`) | Visible | Measurable as is |
| project skill (repo's `.claude/skills/`) | **Not visible** | Placed in the sandbox before measuring (the two tiers below) |
| rule / agent definition / plain .md | Not a skill | No `Skill` call is expected |

Project skills are measured in two tiers. **Which tier was used always appears in the report's Summary** —
75% at Tier 1 and 75% at Tier 2 are different things, so they must not be confusable.

- **Tier 1 (default, no flag)** — only the frontmatter `name` and `description` are real;
  the body is a harmless stub. **Measures "did the agent reach for the skill".**
  Discovery and invocation are decided by `name` / `description` and the body plays no part, so this suffices
- **Tier 2 (`--load-target-skill`)** — places the real body. **Measures "does it follow the procedure".**
  The audited body becomes **instructions** to an unattended child, so it is opt-in. Only the single `SKILL.md`
  file is copied, not the directory (a skill with `references/` is measured short at Tier 2 —
  a visible limitation is preferred over a silent hole)

**Treat Tier 1 as a measurement layer, not containment** — the `description` always reaches the child, and its
500 characters can carry working commands to a child that has Read / Write / Edit / Glob / Grep.

Combining `--load-target-skill` with `--allow-bash` hands **an untrusted document both a payload
and an interpreter**, so it emits a warning.

## Trust boundary — the audited file is untrusted

The tool hands a .md you may not have written to an LLM that writes scenarios, then has an unattended
child agent run them. Treat the target's body as untrusted data. What the tool enforces, and what you control:

- **`setup_commands` are not executed.** Only `mkdir` / `touch` are interpreted, and only for paths that resolve
  inside the sandbox; everything else is rejected and reported to stderr
- **The child's tools are removed with `permissions.deny`, not `--allowedTools`** — `--allowedTools` is only an
  auto-approve list, so unlisted tools stay callable. The deny list removes `Bash` / `Agent` / `Workflow` /
  `ToolSearch` / `ScheduleWakeup` (source of truth: `scripts/child_settings.py`). `--allow-bash` takes Bash off
  the deny list, so pass it only for a target you trust
- `cwd` and `--add-dir` **widen** the child's access; they do not confine it
- **`<sandbox>/.claude/` and `<sandbox>/.git/` are reserved for the tool**, and `CLAUDE.md` / `AGENTS.md` /
  `.mcp.json` / `settings.json` / `settings.local.json` / `.gitignore` are rejected at any depth (case-folded) —
  these files are loaded or executed by Claude Code and git, or hide fixtures from the detector
- Each run gets its own sandbox root, `/tmp/skill-comply-sandbox/run-<pid>/<id>`, so parallel runs do not delete
  each other's sandboxes

When measuring an untrusted .md, run `--dry-run` first and read what it prints in full: the spec steps plus
the three fields an attacker may control — `prompt` (handed to the unattended child), and `setup_commands` and
`files:` (which touch the filesystem).

## Models

| Stage | Default | Why |
|-------|---------|-----|
| `--gen-model` | `haiku` | Spec / scenario generation. Short prompts, fast. |
| `--model` | `sonnet` | Scenario execution (the agent under test). Accepts `haiku` / `sonnet` / `opus` / `fable`. |
| `--classifier-model` | `sonnet` | Trace classification. Haiku times out on long traces (50+ events) and abstract specs (e.g. contemplative-axioms). Sonnet handles the load with a 300s timeout. |

## Report Contents

Reports are self-contained and include:
1. Expected behavioral sequence (auto-generated spec)
2. Scenario prompts (what was asked at each strictness level)
3. Compliance scores per scenario
4. Tool call timelines with LLM classification labels
5. Hook-promotion recommendations for low-compliance steps (informational)
