---
name: callesnikov-continuous-learning-v2
description: Build and manage evidence-backed, project-scoped working instincts for Codex. Use when the user wants GPT-5.6 Sol to learn durable preferences from explicit corrections or repeated verified outcomes, inspect instinct status, import or export an instinct library, evolve related instincts into reusable skills or workflows, promote project knowledge to global scope, or prevent preferences from leaking across repositories.
---

# Callesnikov Continuous Learning v2

Convert repeated, verified working patterns into small local instincts with confidence scores. Keep project conventions isolated by default and promote only patterns that hold across projects.

## Codex operating mode

Use GPT-5.6 Sol as the reasoning layer and `scripts/instinct-cli.py` as the deterministic storage and lifecycle layer.

The bundled `hooks/` and background observer shell scripts are preserved as legacy ECC/Claude assets. Codex App does not expose the same Claude `PreToolUse` and `PostToolUse` hook contract, so do not claim those hooks are active and do not launch the legacy Claude observer loop. In Codex, learn explicitly from the current task context and user-approved local artifacts.

## Evidence threshold

Create or strengthen an instinct only from one of these signals:

- the user explicitly corrects a behavior or states a durable preference;
- the same workflow succeeds repeatedly and the user accepts it;
- repository conventions and tests consistently establish the pattern;
- the same evidence appears independently across tasks or projects.

Do not learn from a one-off guess, an unresolved failure, generated text the user did not accept, a temporary workaround, or the absence of feedback alone.

## Instinct contract

Keep each instinct atomic: one trigger, one action, one scope.

```markdown
---
id: prefer-focused-tests
trigger: "when changing a narrow behavior"
confidence: 0.7
domain: testing
scope: project
---

# Prefer Focused Tests

## Action
Run the smallest relevant test first, then broaden verification according to risk.

## Evidence
- User requested focused verification in two accepted tasks.
- Repository scripts expose a module-specific test command.
```

Use lowercase hyphenated IDs. Keep evidence concrete and dated when useful.

## Scope decision

Choose `project` by default for framework choices, file layout, architecture, naming, UI behavior, build commands, and repository-specific workflows.

Choose `global` only for a user preference or working rule that is explicitly universal or independently confirmed in multiple projects. Security slogans and generic best practices are not automatically user instincts.

## Workflow

### 1. Inspect current state

Set an explicit writable data directory before running the CLI. On Windows, prefer a user-local path:

```powershell
$env:CLV2_HOMUNCULUS_DIR = Join-Path $env:LOCALAPPDATA 'Callesnikov\continuous-learning-v2'
& <python> '<skill>\scripts\instinct-cli.py' status
```

Use the configured bundled Python when available. Run commands from the project root so git-based project detection works. `CODEX_PROJECT_DIR` may be set to an explicit repository root when the current directory is not sufficient.

### 2. Form a candidate

State the trigger, action, evidence, proposed scope, and initial confidence. Merge with an existing instinct when the ID and behavior match; do not create near-duplicates.

Suggested initial confidence:

- `0.3`: explicit but untested preference;
- `0.5`: one accepted correction with supporting repository evidence;
- `0.7`: repeated accepted behavior;
- `0.9`: repeatedly confirmed core rule with no contradictory evidence.

Never raise confidence because GPT-5.6 Sol can produce a persuasive explanation. Confidence follows evidence.

### 3. Import safely

Write the candidate to a temporary Markdown or YAML file, preview it, then import:

```powershell
& <python> '<skill>\scripts\instinct-cli.py' import '<candidate.md>' --scope project --dry-run
& <python> '<skill>\scripts\instinct-cli.py' import '<candidate.md>' --scope project --force
```

Use `--scope global` only when the scope decision above is satisfied. Keep raw conversation text out of the instinct body; store only the minimal evidence summary.

### 4. Review and evolve

```powershell
& <python> '<skill>\scripts\instinct-cli.py' status
& <python> '<skill>\scripts\instinct-cli.py' evolve
& <python> '<skill>\scripts\instinct-cli.py' evolve --generate
```

Treat generated skills, commands, and agent prompts as drafts. Review their triggers, frontmatter, scope, and evidence before installing or invoking them.

### 5. Share or promote

```powershell
& <python> '<skill>\scripts\instinct-cli.py' export --scope project --output '<instincts.yaml>'
& <python> '<skill>\scripts\instinct-cli.py' import '<instincts.yaml>' --scope project --dry-run
& <python> '<skill>\scripts\instinct-cli.py' promote '<instinct-id>' --dry-run
```

Preview imports, promotions, merges, project deletion, and pruning before any destructive execution. Never export raw observations or private repository content.

## GPT-5.6 Sol reasoning rules

- Use the long context to compare evidence across the task, not to inflate a pattern.
- Separate explicit user preference, repository fact, successful outcome, and model inference.
- Search existing instincts before creating a new one.
- Resolve contradictions by lowering confidence or splitting scopes.
- Prefer five precise instincts over one broad personality profile.
- Report exactly what was written, updated, promoted, exported, or left unchanged.

## CLI capabilities

`scripts/instinct-cli.py` supports:

- `status`: list project and global instincts;
- `import`: add or update an instinct library;
- `export`: write a filtered library;
- `evolve`: cluster instincts and optionally generate drafts;
- `promote`: move qualifying project instincts to global scope;
- `projects`: inspect, merge, garbage-collect, or remove project registry entries;
- `prune`: remove expired pending instincts.

Read the relevant CLI implementation before performing a destructive subcommand. Use `--dry-run` whenever available.

## Privacy

Keep storage local. Do not upload observations, code, prompts, or instinct libraries unless the user explicitly authorizes the destination and exact data. Export distilled patterns rather than raw sessions.
