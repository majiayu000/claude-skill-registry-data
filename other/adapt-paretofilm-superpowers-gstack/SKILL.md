---
name: adapt
description: Set up or upgrade a project's CLAUDE.md for the Superpowers + GStack workflow. Analyzes the project, picks the skills; scripts/adapt-claude-md.py does every write, losing nothing.
---

# Adapt to Superpowers + GStack

Invoke with: `/superpowers-gstack:adapt`

One procedure for every project. A project with no CLAUDE.md gets one; a project with
a CLAUDE.md keeps everything it has and gains (or upgrades) the plugin's sections.
There is no separate setup skill any more — adapt on an empty project *is* setup.

**Division of labour.** You decide *what* the project gets: its type and stack, which
skills are relevant, the domain sensitivity, the placeholder values. The script
`scripts/adapt-claude-md.py` does *every write* to CLAUDE.md: the snapshot, the header,
retired sections, skill renames, each marker-managed block with its growth check,
attribution sentinels, heading demotion and `emitted=` provenance, Model Routing, the
verify diff and the report. **Never edit CLAUDE.md by hand in this skill and never paste
a block yourself** — the script is deterministic, idempotent and fail-closed; a hand
edit is neither.

Begin every Bash call with the two bindings below — shell state does not survive
between calls, and an unset `$SKILL_DIR` resolves the script to a path python3 cannot
open:

```bash
SKILL_DIR='<the base directory the Skill tool printed when this skill loaded>'
SCRIPT="$SKILL_DIR/../../scripts/adapt-claude-md.py"
[ -f "$SCRIPT" ] || SCRIPT=$(ls ~/.claude/plugins/cache/*/superpowers-gstack/*/scripts/adapt-claude-md.py 2>/dev/null | sort -V | tail -1)
[ -f "$SCRIPT" ] || { echo "BLOCKED — adapt-claude-md.py not found; run /plugin update superpowers-gstack"; exit 2; }
```

**Dependency check:** verify both upstream frameworks are installed:

```bash
ls -d ~/.claude/plugins/cache/claude-plugins-official/superpowers/*/ 2>/dev/null | head -1
ls -d ~/.claude/skills/gstack/ 2>/dev/null
```

If either path is missing, STOP and tell the user:

> This plugin is glue for two upstream frameworks. Install them first:
>
> **Missing: Superpowers** — `/plugin marketplace add claude-plugins-official` then `/plugin install superpowers`
>
> **Missing: GStack** — `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`
>
> Only mention the framework(s) that are actually missing. Restart Claude Code after installing, then run `/superpowers-gstack:adapt` again.

**Directory check:** the working directory must be the target project. If it looks like
a different project (the superpowers-gstack repo itself, say), STOP:

> You're currently in `[cwd]`. This skill needs to run from your target project directory. Start a new Claude Code session:
> ```
> cd /path/to/your-project && claude
> ```
> Then run `/superpowers-gstack:adapt` again.

## Process

Follow the steps in order. Three `STOP HERE` gates ask the user something; end your
message at the question each time.

### Step 1: Analyze the project

Read what exists (skip what does not): `CLAUDE.md`; package files (`package.json`,
`Package.swift`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`, `plugin.json`);
test configuration; CI (`.github/workflows/`, `.gitlab-ci.yml`); git state (branch,
remotes, recent branch names); the root layout; `docs/`; `.gstack/track`.

If there is no CLAUDE.md, or the stack cannot be read off the files, ask in one
message: project type; test framework (or none yet); deploy target (or none); browser
UI and its URL (or none); security concerns (auth, user data, payments, external APIs);
for a native app, the platform (iOS / macOS / both). Then summarize what you found —
concisely, what matters for the transition.

### Step 2: Confirm the stack

> Based on my analysis, this is a **[type]** using **[stack]**. Tests run with `[command]`. [Deployed to X / not deployed]. [Has browser UI at X / No browser UI]. Track: [web / ios / macos / both].
>
> Is this correct? Anything to add?

**STOP HERE.** Do not add "next steps" or anything after the question.

### Step 3: Evaluate skills and model routing

Read `roster.md` (sibling of this file) and pick, for this project, the relevant
Superpowers skills and the relevant GStack skills per phase. Leave out rows marked
`User-started only`: they stay the user's to invoke and stay out of the routing draft.
Read `model-routing.md` (sibling) for the per-skill base tiers, and infer the
project's **domain sensitivity**:

- real-time audio / DSP / signal processing, or any lock-free concurrency → **very high**
  (a plain SwiftUI CRUD app with none of these is **medium**)
- database migrations / ETL / data transforms, or security concerns from Step 1 → **high**
- web / mobile UI feature work → **medium**
- CLI tools / libraries / format plumbing → **low**
- ambiguous → ask one line: "How silently could a subtle bug here compound — very high / high / medium / low?"

Present the selection (Superpowers; GStack by phase; excluded, with a reason each),
then the base tiers for the selected skills and the inferred sensitivity, and ask:

> Does this look right? Any skills to add or remove, or a different sensitivity? (Say so if you want no Model Routing section at all.)

**STOP HERE.** Repeat until confirmed.

### Step 4: Resolve the script's inputs

1. **Track.** `.gstack/track` if present (`ios` | `macos` | `both`; anything else is
   `BLOCKED — invalid .gstack/track`, stop and say so); absent means web. If Step 2
   established a native platform and the file is missing, write it:
   `mkdir -p .gstack && printf '%s\n' "$TRACK" > .gstack/track`.
2. **E2E executor pin** — only when track is `macos` or `both`. If `.gstack/e2e-executor`
   exists the script reads and validates it; do not re-ask. If it does not exist, ask
   **once** with `AskUserQuestion`:

   > Where should this project's committed macOS UI tests run? A VM rig gives isolation — a UI test that grabs the screen cannot fight you for focus, two runs cannot collide on one machine, and an unattended run does not need anyone logged in. It requires `vm-e2e` on `PATH`; without it the tests still run, on this machine, with a warning.
   >
   > - **On this machine** (recommended) — no extra setup, and what every project does today.
   > - **In the VM rig** — needs the rig installed; a teammate without it gets a warning and a host run, not a failure.

   Default to `host` if unclear, then write the pin and keep it committable:

   ```bash
   mkdir -p .gstack && printf '%s\n' "$ANSWER" > .gstack/e2e-executor   # host or vm
   if git check-ignore -q .gstack/e2e-executor 2>/dev/null; then
     grep -q '^!\.gstack/e2e-executor$' .gitignore 2>/dev/null \
       || echo '!.gstack/e2e-executor' >> .gitignore
     git add .gitignore && git add -f .gstack/e2e-executor
   else
     git add .gstack/e2e-executor
   fi
   ```

   Do not check whether `vm-e2e` is installed before asking — the pin records a project
   decision, not this machine's capabilities. iOS-only and web projects get no file and
   no question.
3. **Placeholders** — resolve every token the emitted blocks carry, per
   `blocks/PLACEHOLDERS.md`: `DOMAIN_SENSITIVITY` from Step 3 (every track);
   `IOS_SIMULATOR` and `DEVELOPMENT_TEAM` on native tracks (the resolution commands are
   in that file — run them, do not guess). Each becomes a `--set TOKEN=value`. The script
   refuses with `UNRESOLVED PLACEHOLDER` and writes nothing if one is missing; that is
   the guard, not an inconvenience.
4. **Workflow profile.** Ask it before the routing draft (item 5), which follows the answer. If `.gstack/workflow` exists the script reads and validates it; do not re-ask. If it does not exist, ask **once** with `AskUserQuestion`:

   > How should this project work?
   >
   > - **Vibe** (recommended) — one intake round, then the feature is finished autonomously and you review it once. Your one checkpoint on the way is the acceptance tests, which are then locked. Adds the `Vibe contract` section and a project context skill.
   > - **Classic** — the skills' own approval gates (design, plan, execution method, landing menu), as before.

   Write the pin and keep it committable:

   ```bash
   mkdir -p .gstack && printf '%s\n' "$PROFILE" > .gstack/workflow   # vibe or classic
   if git check-ignore -q .gstack/workflow 2>/dev/null; then
     grep -q '^!\.gstack/workflow$' .gitignore 2>/dev/null \
       || echo '!.gstack/workflow' >> .gitignore
     git add .gitignore && git add -f .gstack/workflow
   else
     git add .gstack/workflow
   fi
   ```

   A run with nobody to answer writes no `.gstack/workflow`: the script then uses
   classic and says so in its notes. With `vibe` the script also creates
   `.claude/skills/<project>-context/SKILL.md` from a template when no `*-context` or
   `*-kontekst` skill exists, and never overwrites one.

5. **Skill routing draft** — only when CLAUDE.md has no `## Skill routing` heading.
   Write it to `.gstack/adapt-routing.md` from this template, tight (row descriptions
   ≤ 15 words, decision-tree lines ≤ 10 words, no rationale prose), only the skills
   confirmed in Step 3, sections that do not apply omitted:

   ```markdown
   ## Skill routing

   This project uses Superpowers + GStack. Each owns a distinct phase.

   ### GStack — [phases]
   **Planning:** [selected Phase 1 skills, one line each]
   **Review & QA:** [selected Phase 3 skills]
   **Ship & Monitor:** [selected Phase 4 skills]

   ### Superpowers — Implementation
   - [selected skills]

   ### Routing Logic
   [project-specific decision tree, e.g. Ready to build →
   `/superpowers-gstack:vibe` with the vibe profile, `/superpowers:brainstorming` with
   classic; Bug during coding →
   /superpowers:systematic-debugging; Bug found in QA → /investigate; Code complete →
   /review [→ /qa <url>]; Security-sensitive → /cso before /review; Ready to ship →
   /ship; Trivial change → just do it]

   ### Rules
   - Never run GStack and Superpowers skills in the same phase
   - Never nest subagents from different frameworks
   - `/superpowers:systematic-debugging` for bugs found during implementation; `/investigate` only for bugs found in QA or production
   - Superpowers specs go in `docs/superpowers/`; GStack state lives in `~/.gstack/projects/`

   ### Session Management
   - `/clear` when transitioning between GStack and Superpowers phases; save architecture decisions to `docs/` first
   - Skip `/clear` for small projects (< 5 tasks, < 30 min)

   ## Project
   ### Tech Stack / Testing / QA URL / Deployment
   [from Step 2 — omit what does not apply]
   ```

   If `## Skill routing` already exists, the script leaves it alone (its marker-managed
   subsections are still upgraded), so write no draft. If the old section routes to
   skills that no longer exist, the script renames `macos-/ios-native-review` →
   `apple-native-review` and `macos-/ios-e2e-scaffold` → `e2e-scaffold`, and
   drops `ios-visual-explore` rows itself.

### Step 5: Dry run, then ask

```bash
SKILL_DIR='<the base directory the Skill tool printed>'
SCRIPT="$SKILL_DIR/../../scripts/adapt-claude-md.py"
python3 "$SCRIPT" --dry-run --mkdirs \
  --set 'DOMAIN_SENSITIVITY=<value>' [--set 'IOS_SIMULATOR=<value>' --set 'DEVELOPMENT_TEAM=<value>'] \
  [--routing-file .gstack/adapt-routing.md] [--no-model-routing]
```

Exit 2 is a refusal with the reason on stderr (`BLOCKED`, `UNRESOLVED PLACEHOLDER`,
`UNREADABLE`): fix the input it names and re-run; never work around it by editing the
file. Exit 0 prints the report — **Changes made / Preserved / Removed (not plugin
prose) / Deferred (grown past its block, not upgraded)** — and ends with one JSON line.

Present, in this order:

1. The gap analysis: what already works, what the run will add or upgrade, anything in
   the existing CLAUDE.md that contradicts the workflow ("never use subagents", "don't
   use TDD"). With the vibe profile, also list every rule that contradicts the vibe
   contract ("write a PRD before any code", "ask before each phase") and let the user
   choose which one stands. Also note whether there is a remote and a branch workflow (`/review` and `/ship`
   need both; if on `main` with uncommitted work, warn and do not branch for the user).
2. The report's `Deferred` entries, if any. Each is a plugin-managed section that has
   grown past its block — project knowledge is living inside it, and replacing it would
   destroy that. For each one, show the `at_risk` lines from the JSON and offer two
   outcomes: **move that content into a new unmarked section and upgrade** (recommended
   — the script rescues the lines it cannot find in the block, plus the section's own
   subheadings, into `## <project> — notes rescued from "<heading>"`, where no upgrade
   will ever touch them), or **leave the section at its old version** and skip its
   upgrade this run.
3. The report's inline notices — a section the script could not attribute to a past
   emitter (preserved, current block inserted below it), a markerless
   `Code reuse discipline` or `Model Routing` that is the project's own.

Then ask: "Shall I proceed with these changes?" — naming the move/leave choice for
every deferred section.

**STOP HERE.** Do not continue until the user answers. A run with nobody to answer (a
`--print` session that pre-answered Steps 2–3, a subagent, an orchestrator) proceeds
with every deferred section **left** at its old version — the script's own default;
a stale section is recoverable, a deleted one is not.

### Step 6: Apply and report

Run the same command without `--dry-run`, adding `--rescue <marker>` (the `marker` field
of the deferred entry, e.g. `--rescue gstack-xcode-tools`) for every section the user
chose to move. The script snapshots CLAUDE.md to `.gstack/CLAUDE.md.pre-adapt` (rotated,
never overwritten; excluded from git via `.git/info/exclude`) before its one write,
creates `docs/superpowers/specs/` and `plans/` with `.gitkeep`, and prints the final
report.

**Relay the report to the user verbatim.** Its three labels —
`**Removed (not plugin prose):**`, `Nothing project-authored was removed.` and
`**Deferred (grown past its block, not upgraded):**` — stay in English even when the
rest of your message is in the user's language; tooling greps them. The Removed block
lists every removed line the new block does not carry; it is over-inclusive by design
(a reworded plugin sentence can land there), so read it as candidates for a glance,
not as a verdict. The Snapshot line names the restore command; repeat it. When the report
says the script created `.claude/skills/<name>/SKILL.md`, run `git add` on that file (like the
pin), so a worktree cleanup does not lose it.

Whenever a marker-managed section was replaced, add:

> **Where project knowledge belongs.** A heading carrying a `gstack-<name>-vN` marker is plugin-owned: `/adapt` replaces the whole section on every upgrade. Pasting rescued content back into one guarantees a repeat at the next upgrade. Project findings — the measurement you took, the flag that turned out to work, the thing that cost you an hour — belong in your own H2 section with no marker. `/adapt` leaves those alone, with one exception: the headings it manages are reserved even when unmarked, because an unmarked copy of one reads as an older emitted section. Prefix your own headings with this project's name and none of them can collide.

Then ask:

> Would you like me to run a comprehensive review of the adaptation? It checks that the routing matches your stack and test setup, that nothing project-authored was lost (re-reading `diff .gstack/CLAUDE.md.pre-adapt CLAUDE.md`), that existing conventions do not contradict the new rules, and that `docs/superpowers/` is in place. Recommended for projects with a complex existing setup.

**STOP HERE.** If the user says yes: re-read the new CLAUDE.md end to end; cross-check
the routing against the project (`/qa` without a browser UI, `/cso` without auth or
user data, are wrong); re-read the `<` side of the snapshot diff with fresh eyes for
project content wearing plugin-shaped wording; check for contradictions with existing
instructions; walk three or four common scenarios through the Routing Logic. Fix what
you find and re-verify.

### Step 7: Suggest next steps

> **Next steps:**
> - Vibe profile? → `/superpowers-gstack:vibe <what to build>` — and fill in the context skill as you learn the project
> - Working on a new feature? → `/superpowers-gstack:vibe` (vibe profile) or `/superpowers:brainstorming` (classic)
> - Have code ready for review? → `/review`
> - Want a product-framing session first? → type `/office-hours` yourself; it is never routed automatically
>
> **Tip:** Run `/superpowers-gstack:adapt` again after major project changes (new deploy target, added test framework) and after every plugin upgrade — the session-start hook nudges when the CLAUDE.md version marker lags.

**What this skill never changes:** test configuration, CI pipelines, git hooks (unless
they directly conflict), code-style or lint configuration, and any CLAUDE.md content
outside the sections the script manages.
