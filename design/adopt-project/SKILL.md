---
name: adopt-project
description: Apply agent-starter patterns to an EXISTING project - audits the codebase, proposes components by invasiveness tier (hooks, skills, CLAUDE.md, lint configs, patterns), and applies only what the developer approves. Use when the user says adopt, retrofit, "apply agent-starter to this project", or wants starter patterns in an existing codebase.
user_invocable: true
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep
---

# Adopt agent-starter in an Existing Project

<!-- Mirrors ADOPT.md in the agent-starter repo. If ADOPT.md changes, update this skill to match. -->

Use on an existing codebase. Never on a green field - that's `/new-project`.

An existing project has state to audit, every change is potentially
destructive, and adoption must be incremental. So the flow is **audit-first,
merge-don't-overwrite, opt-in per component**.

## Safety rails (read first)

- Create a branch before any write: `git checkout -b adopt/agent-starter`.
  Everything below is reversible by dropping the branch.
- Read every file before modifying it. Append and merge; never replace a file
  the developer wrote.
- After each merge-tier step, run the project's own test suite (and linter, if
  present). A red suite means stop and surface it.
- If the project has no tests, say so explicitly and default to the
  non-invasive tier only.
- Surface contradictions between starter patterns and existing conventions;
  never resolve them silently.

## Phase 1: Interview

Ask one at a time:

1. **Components** - which are you interested in? (hooks / skills / CLAUDE.md +
   memory / lint configs / code patterns / "audit first, then decide")
2. **Repo path** - local path to agent-starter, e.g. `~/code/agent-starter`
   (only needed if files will be copied).

## Phase 2: Audit (read-only)

Build a gap report before proposing anything.

**Detect the stack:**

- `package.json` + `tsconfig.json` → TypeScript/JavaScript
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- Both → monorepo: audit each half separately
- Neither → other stack; only Tier 1 and CLAUDE.md apply

**Inventory** (present as a table: component | what exists | starter offering | conflicts):

- **Lint/format:** ESLint configs (flat or legacy), `biome.json`, Prettier;
  ruff (`ruff.toml` or `[tool.ruff]` in pyproject), mypy/pyright configs
- **Tailwind design system:** `tailwindcss` 4.x in `package.json` dependencies,
  or a shadcn `components.json`. Either one makes the project a candidate for
  the `@shadcn/lint` fragment (Tier 3). Record the ESLint major.minor while
  here: the plugin needs 9.30+.
- **Instructions:** `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, `AGENTS.md`
- **Hooks:** `.claude/settings.json` hook entries; agent-starter hooks already
  installed system-wide (`~/.claude/hooks/.agent-starter-version` - record the
  stamped version to compare against the repo `VERSION`)
- **Skills:** which starter skills are already present system-wide - check
  `~/.claude/skills/{commit,commit-push-pr,simplify,remember,dream,new-project,adopt-project,reflect}`.
  Hooks and skills are **user-global**, so anything already installed already
  covers this project - don't re-propose it.
- **Tests:** `package.json` `scripts.test`, pytest/tox config, Makefile targets
- **File-size health:** run `bash <repo-path>/hooks/check-codebase-health.sh`
  from the project root, or
  `find src -name '*.ts' -o -name '*.py' | xargs wc -l | sort -rn | head -20`
- **Patterns already present:** central error registry? env boundary? Result
  types? (grep for scattered `process.env` / `os.environ`, raw
  `throw new Error` / `raise Exception`)

## Phase 3: Propose

Present the menu grouped by invasiveness, with per-item conflict notes from
the audit. Wait for explicit approval per item (or "all of tier N"). Nothing
is applied unapproved.

### Tier 1 - Non-invasive (no project-file conflicts possible)

- **Hooks:** skip if the audit found them already installed and current (stamped
  version matches the repo `VERSION`) - they're user-global and already cover
  this project. If stale, offer to update by re-running `bash <repo-path>/install.sh`
  (idempotent). Otherwise run it now: it installs to `~/.claude/hooks/` and
  merges the settings.json wiring with jq. Note for the developer: hooks are
  **user-global** - they will also fire in their other projects.
- **Skills:** copy only the ones the audit found **missing** from
  `<repo-path>/skills/` to `~/.claude/skills/`; leave already-present skills
  as-is (`for s in ...; do [ -d ~/.claude/skills/$s ] || cp -r <repo-path>/skills/$s ~/.claude/skills/; done`).
- **Self-improvement ledger:**
  `mkdir -p .harness/reflections && echo '.harness/ledger.jsonl' >> .gitignore`
  - the hooks log to it automatically; `/reflect` reads it.

### Tier 2 - Additive (append, never replace)

- **No CLAUDE.md** → copy `<repo-path>/templates/CLAUDE.md`, fill in project
  name and description.
- **CLAUDE.md exists** → append only the sections it lacks: Memory System,
  Git Safety, Implementation Notes, Self-improvement loop. Read the existing
  file first; if its instructions contradict a starter section, list the
  contradictions and let the developer choose. The diff must show additions
  only.
- **`.claude/rules/starter-patterns.md`** → the apply-on-touch file (Tier 4).

### Tier 3 - Merge-required (developer approval per file)

**TypeScript:**

- **No linter** → copy `templates/biome.jsonc` + `templates/eslint.config.mjs`
  from the repo, install deps (see AGENT.md step 4 there), run on the
  codebase, and report the damage. Where existing code fails a rule en masse,
  downgrade that rule to `warn` with a ratchet note instead of fixing
  hundreds of violations in the adoption branch.
- **Existing ESLint** → offer two paths: (a) cherry-pick the Tier 1
  correctness rules from `guides/lint-rules-for-ai.md` into their config, or
  (b) migrate to the starter flat config, carrying their custom rules over.
- **Prettier present** → don't add Biome's formatter (two formatters fight);
  adopt the ESLint half only.
- **Tailwind v4 present** (per the inventory) → offer
  `templates/eslint.shadcn.mjs` + `npm i -D @shadcn/lint`, spread into their
  flat config as `...shadcnRules`. Adapt `settings.shadcn.ui` and the
  `**/components/ui/**` override to where their components live. Existing
  ESLint below 9.30 has to be upgraded first. Run it on the codebase and
  downgrade rules that fail en masse to `warn` with a ratchet note, same as
  the base config.

**Python:**

- **No ruff config** → copy `templates/ruff.toml` +
  `templates/pyrightconfig.json`, run `ruff check`, report counts per rule
  family, and downgrade noisy families per-project rather than mass-fixing.
- **`[tool.ruff]` in pyproject.toml** → merge the starter's `select`/`ignore`
  lists into pyproject. Do **not** drop a standalone `ruff.toml` next to it -
  ruff.toml silently takes precedence and their existing config stops
  applying.
- **mypy in use** → don't add pyright without asking; two type checkers
  disagree with each other more than they catch for each other.

**Foundation templates (both stacks):** copy only where the pattern is absent
- env boundary (`env.ts` / `env.py`), error registry (`errorIds.ts` /
`error_ids.py`), truncator (`truncate-for-context.ts` /
`truncate_for_context.py`). Adapt import paths to the project's layout. Skip
any the project already has an equivalent for.

### Tier 4 - Gradual-only (never a bulk refactor)

Write `.claude/rules/starter-patterns.md` with apply-on-touch guidance:

```markdown
# Starter patterns - apply on touch

Apply these when already editing the relevant code. Never as a bulk refactor.

- Editing a file over 300 lines → split per the file-size hook's suggestions
  (types / constants / validation / utils).
- Touching a `throw` / `raise` site → route it through the error registry
  (`guides/error-id-registry.md`).
- Changing a fallible function's signature → consider returning a Result
  (`guides/discriminated-union-results.md`).
- Touching an env read → move it behind the env boundary
  (`guides/zod-at-the-boundary.md`).
- Adding a long-running operation → thread cancellation through it
  (`guides/abort-signal-threading.md`).
- Adding a new tool → use the directory-per-tool layout
  (`guides/tool-authoring-pattern.md`).
```

Explicitly out of scope: restructuring directories, rewriting existing error
handling, or converting APIs wholesale. The starter's layout is a target for
new code, not a migration mandate.

## Phase 4: Apply

Execute the approved items tier by tier, in tier order. After each Tier 3
item, run the project's lint and tests; stop on red. One commit per component,
so the developer can drop any single adoption from the branch.

## Phase 5: Verify

Confirm each item before reporting done:

- [ ] All changes on the adoption branch; default branch untouched
- [ ] Gap report presented; every applied item was explicitly approved
- [ ] Existing CLAUDE.md content preserved (diff shows additions only)
- [ ] Project tests + lint pass (or were already red and are unchanged)
- [ ] `.harness/ledger.jsonl` gitignored, if the loop was adopted
- [ ] Contradictions surfaced and the developer's choices recorded
      (in CLAUDE.md or the implementation notes)
