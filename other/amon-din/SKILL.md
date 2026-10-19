---
name: amon-din
description: Use when the user runs /amon-din [<count>], /amon-din all [<count>], /amon-din add <id>[:<label>]..., or /amon-din remove <id>... — render the most recent CI runs (default 3, override with <count>) for the current branch (or all branches with `all`), or mutate the per-project `ci_routing.md` auto-memory (`add`/`remove`, TeamCity only). Dispatches to GitLab CI (via glab) or TeamCity (via REST). Never triggers, retries, or cancels CI itself. First run on an unbound repo prompts once.
purpose: Renders recent CI runs for the current branch (or all branches) from GitLab CI or TeamCity.
user_invocable: true
stage: weigh
---

# Amon Dîn — The Beacon of Gondor

The first beacon of Gondor, the watchtower of Anórien. When fire kindles, it speaks one truth — what burns at the front. So this skill: it does not weigh, does not advise, does not gate. It reports. A handful of recent runs (three by default), one table, plain.

## Ethos

- **Read by default.** No write paths, no triggers, no retries — only fetch and render.
- **Backend by binding, not by guess.** The repo's `ci_routing.md` auto-memory names the flavor; the skill dispatches. No CI auto-detection.
- **The current branch is the focus** unless the caller explicitly widens scope with `all`.

## Argument parsing

**Render verbs**:

- `/amon-din [<count>]` — read the binding, fetch the last `<count>` pipelines on the current branch, render the table.
- `/amon-din all [<count>]` — same as above but lift the branch filter; the last `<count>` across the whole project / buildType.

`<count>` is a positive integer between **1 and 50**. Default is **3** when omitted. The render-verb tokens are **order-independent**: `/amon-din 10 all` and `/amon-din all 10` mean the same thing — "10 across all branches". Numbers outside 1..50 are rejected with: *"Amon Dîn counts in measure — the lookback must be between 1 and 50."*

**Binding-management verbs** (TeamCity only; reject on GitLab):

- `/amon-din add <id>[:<label>] [<id>[:<label>] ...]` — append entries to the `buildTypes` list. Idempotent: ids already present are skipped with a one-line note. Labels default to the id when the colon form is omitted.
- `/amon-din remove <id> [<id> ...]` — drop entries from the `buildTypes` list. Alias: `rm`. Ids not present surface a one-line note and are otherwise ignored.

Dispatch rule: if the **first non-numeric** positional is `add`, `remove`, or `rm`, route to the binding-management workflow and treat all remaining positionals as ids — no count interpretation. Otherwise route to the render workflow, where the lone `all` token (if any) widens the branch scope and the lone integer (if any) sets `<count>`.

Reject any other first non-numeric positional with: *"Amon Dîn knows only `all`, `add`, `remove` as verbs; everything else is the default beacon."*

## Workflow

### 1. Verify a git repo

```bash
git rev-parse --show-toplevel
```

If it errors, stop:
> Not in a git repo — Amon Dîn watches no road here.

Capture the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

If `all` is the verb, the branch is recorded for the header but **not** passed to the hook.

### 2. Resolve the CI binding

The binding lives in the per-project auto-memory file `ci_routing.md`. Frontmatter:

```yaml
---
name: CI Routing
description: This project's CI binding for /amon-din
type: reference
---
```

Body — one of:

```
flavor: gitlab
```

or

```
flavor: teamcity
buildTypes:
  - id: PetProject_Build
    label: Build
  - id: PetProject_Test
    label: Test
```

A repo may carry **one or more** TeamCity buildTypes (build, test, deploy, per-platform variants); the skill renders a section per id. The `label` field is optional — when absent, the id stands as its own label.

**Legacy single-buildType form** is still accepted on read:

```
flavor: teamcity
buildTypeId: PetProject_Build
```

The skill normalises this to a single-entry list (`label = id`) at load time.

If the file is **absent** from the auto-memory:

1. Prompt via `AskUserQuestion` — "Which CI serves this repo?" with options `gitlab`, `teamcity`.
2. If `teamcity`, prompt a second question — "TeamCity buildTypeIds (comma-separated, optionally `id:label` per entry)?" (open input via `Other`). Examples:
   - `PetProject_Build` — one buildType, label defaults to id.
   - `PetProject_Build, PetProject_Test` — two buildTypes, labels default to ids.
   - `PetProject_Build:Build, PetProject_Test:Test` — two buildTypes with explicit labels.
3. Parse the comma-separated input into the `buildTypes` list. Whitespace around commas and colons is trimmed. Empty entries are skipped.
4. Write the file using the standard memory protocol (see global "How to save memories"); add a `- [CI Routing](ci_routing.md) — <one-line>` pointer to `MEMORY.md`.
5. Continue.

If the file **is** present but malformed (no `flavor`, or `flavor: teamcity` with neither `buildTypes` nor `buildTypeId`), surface the problem plainly and stop:

> Amon Dîn cannot read its binding — `ci_routing.md` is missing required fields. Edit or delete it, then summon again.

### 3. Dispatch

| Flavor   | Hook                                        | Args                                   |
|----------|---------------------------------------------|----------------------------------------|
| gitlab   | `~/.claude/hooks/amon-din-gitlab.sh`        | `<count> [<branch>]`                   |
| teamcity | `~/.claude/hooks/amon-din-teamcity.sh`      | `<buildTypeId> <count> [<branch>]`     |

`<count>` is the value the caller supplied (or 3 when omitted). When the verb is `all`, omit the branch argument.

For **GitLab**, dispatch is a single hook call.

For **TeamCity**, iterate over the `buildTypes` list and call the hook **once per id** (in the order they appear in `ci_routing.md`). Each call returns the rows for that one buildType, rendered as its own subsection (see step 4).

The hook prints zero or more pipe-delimited lines:

```
<id>|<status>|<branch>|<timestamp>|<url>
```

`<status>` is one of: `success`, `failed`, `running`, `queued`, `cancelled`, `unknown`. The hook has already normalised the forge's native vocabulary into this set; the skill body does no further translation.

If a hook call exits non-zero, surface the stderr verbatim, mark that subsection as unavailable (`⚠  unavailable — <short reason>`), and continue with the rest of the list. The skill does not abort the whole render on a single TeamCity buildType failure. For GitLab — single dispatch — a non-zero exit stops the run.

### 4. Render

#### Aggregate blockquote

Lead with a single blockquote line distilled from **all** subsections:

- All sections green (top row `success` everywhere) → `> All green on <branch> — the road is clear.`
- Any section failed → `> <label> failed <age>` (the worst news wins; if multiple sections show failures, pick the most recent).
- Any section running and none failed → `> <label> running on <branch>.`
- Mixed otherwise → `> <P> of <M> build types green on <branch>.` where M is the count of subsections.
- Single-section repos use the simpler form: `> <N> green on <branch> — the road is clear.` / `> Last build failed on <branch> · <age>.` / etc.

#### Header line

Below the blockquote, one header line:

`amon-din  <branch> · <flavor> · <project-name>`

- For `gitlab`: `<project-name>` is the repo's `group/project` path.
- For `teamcity`: `<project-name>` is the joined labels of every buildType, e.g. `Build, Test, Deploy`. Single-buildType repos render just the one label.

If the verb is `all`, replace the branch slot with `(all branches)`.

#### Subsections

Render one block per buildType (TeamCity) or one block (GitLab). Each subsection:

```
▓ <label> (<buildTypeId or project>)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚫 #142  master   3m ago    https://...
  ✅ #141  master   47m ago   https://...
  ⏳ #140  feature  running   https://...
───────────────────────────────────────
  1 of 3 green · 1 failed · 1 running
```

The `▓ <label>` subheader is omitted for GitLab and for single-buildType TeamCity repos — go straight to the row table.

Symbols:

- `✅` — success
- `🚫` — failed
- `⏳` — running
- `⏸` — queued
- `⚪` — cancelled / unknown

Timestamps: relative — `<n>s ago`, `<n>m ago`, `<n>h ago`, `<n>d ago`, or `yesterday`. Running rows show `running` instead of an age; queued rows show `queued`.

Subsection footer: `<P> of <N> green · <F> failed [· <Q> running] [· <C> queued] [· <X> cancelled]`. Drop a trailing clause when its count is zero.

#### Worked example — multi-buildType TeamCity (default count = 3)

```
> Test failed on master · 3m ago.

amon-din  master · teamcity · Build, Test

▓ Build (PetProject_Build)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ #210  master  12m ago   https://...
  ✅ #209  master  1h ago    https://...
  ✅ #208  master  3h ago    https://...
───────────────────────────────────────
  3 of 3 green

▓ Test (PetProject_Test)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚫 #87   master  3m ago    https://...
  ✅ #86   master  47m ago   https://...
  ✅ #85   master  2h ago    https://...
───────────────────────────────────────
  2 of 3 green · 1 failed
```

### 5. Empty result

If a subsection's hook returns zero rows, render the subheader and a single line in its place:

> No recent runs for `<branch>`.

No body table, no footer for that subsection.

If **every** subsection is empty (single-buildType GitLab, or a freshly bound TeamCity project that has never run), render the header line and one line below:

> Amon Dîn sees no fires — no recent runs for `<branch>` in this CI.

No subsections, no footer.

## Workflow — `add` / `remove` verbs

Both verbs mutate `ci_routing.md` and never call a hook.

### Preconditions

- The binding must exist. If `ci_routing.md` is absent, stop with: *"No binding to mutate — run `/amon-din` to record one first."*
- The binding's `flavor` must be `teamcity`. If it is `gitlab`, stop with: *"GitLab repos have no buildTypes — the binding is a single project ref."*

### `add` workflow

1. Parse each positional argument as `<id>[:<label>]`. Trim whitespace around colons and commas; reject empty tokens.
2. For each entry, in order:
   - If the id is already present in `buildTypes`, skip and emit `= <id> (already present)`.
   - Otherwise append `{id, label}` (label = id when omitted) and emit `+ <label> (<id>) — added`.
3. Save the updated `ci_routing.md`. The `MEMORY.md` pointer line is unchanged.
4. Render the binding table (see "Render shape" below).

### `remove` workflow

1. For each positional argument (id only — no label):
   - If the id is not in `buildTypes`, emit `? <id> (not present)` and continue.
   - Otherwise remove the entry and emit `- <label> (<id>) — removed`.
2. If the resulting list would be empty, **refuse the operation** — restore the in-memory list, do not save, and stop with: *"Refusing to leave the binding empty — delete `ci_routing.md` to unbind, or `add` a replacement first."*
3. Otherwise save the updated `ci_routing.md`.
4. Render the binding table.

### Render shape (both verbs)

```
amon-din  binding · teamcity · 3 buildTypes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  = Build  (PetProject_Build)    already present
  + Test   (PetProject_Test)     added
  + Deploy (PetProject_Deploy)   added
```

The header carries the literal token `binding` in the slot where render verbs carry the branch — this signals to the reader that the table reports configuration, not pipelines.

Markers:

- `+` — newly added
- `-` — removed
- `=` — already present (idempotent skip on `add`)
- `?` — not present (no-op on `remove`)

## Rules

- Read-only against the CI — never triggers a build, retries a job, or cancels a run. The `add` / `remove` verbs only ever touch the local `ci_routing.md`; they never reach TeamCity or GitLab.
- No fallback between backends — if the named flavor errors, surface the error and stop.
- The binding lives in `ci_routing.md`; an explicit `cd` does not override it. Three paths to change it: `add` / `remove` for incremental edits, direct file edit for restructuring, or delete the file (with its `MEMORY.md` pointer) to re-prompt from scratch.
- Tokens never appear in logs or output. Hooks resolve them via `secret.sh teamcity` (TeamCity) or `glab` config (GitLab) and pass nothing through stdout.
- The skill never edits `~/.claude/`, `~/.bashrc`, or any file outside the project tree's auto-memory.
- `add` and `remove` are TeamCity-only — they have no meaning for GitLab and are rejected on a `gitlab` binding.
- `remove` will not leave the binding empty; the last entry must be removed by deleting the file, not by emptying the list.
