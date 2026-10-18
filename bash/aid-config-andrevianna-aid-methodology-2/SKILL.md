---
name: aid-config
description: >
  View or update AID pipeline settings. Use this skill when you need to see how the pipeline
  is configured, or change one setting such as the project name, its type, or the minimum
  grade. A bare invocation prints every value in a table and, on the first run, creates
  `.aid/settings.yml` from the template. Passing a key -- `/aid-config` name -- views and
  updates that one setting interactively.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit AskUserQuestion
argument-hint: "(none) view all  |  <key> view+update one (e.g., name, minimum_grade)"
---

# AID Project Configuration

`/aid-config` reads and writes `.aid/settings.yml` — the single source of truth
for AID pipeline settings (grades, heartbeat, project identity).

**Two modes, nothing else.**

| Invocation | What it does |
|---|---|
| `/aid-config` | Show all settings as a table. On first run (no `settings.yml`), copy the template into place first, then show. |
| `/aid-config <key>` | Show the current value of `<key>`; prompt for new (with suggestions + always a free-form option); validate; write in place. |

Examples: `/aid-config name`, `/aid-config minimum_grade`,
`/aid-config source_control`.

---

## Pre-flight

- ✅ `Default` or `Auto-accept edits` → proceed
- ❌ `Plan mode` → STOP. This skill writes files.

---

## Mode 1 — Show all settings (`/aid-config`)

### Step 1: Ensure `.aid/settings.yml` exists

If `.aid/settings.yml` is missing:
- Create `.aid/` directory if absent (do NOT touch `.aid/knowledge/` or other subdirs).
- Copy `.aid/runtime/templates/settings.yml` → `.aid/settings.yml` verbatim.
- Print: `Created .aid/settings.yml from template.`

### Step 2: Render the table

Read `.aid/settings.yml`. Print a table with these columns:
`Key | Value`

Order: `name`, `description`, `type`, `source_control`, `minimum_grade`, `heartbeat_interval`.

If any value matches a `<placeholder>` pattern (e.g., `<project-name>`), append ` ⚠ unset` after the value.

### Step 3: Suggest commands for unset values + the general update form

After the table, print the line:
```
Run /aid-config <key> to update any value.
```

If ANY rows were marked `⚠ unset`, ALSO emit a copy-pasteable command per unset row, so the user can act without having to assemble the key themselves:

```
N values unset. To set them:
  /aid-config name
  /aid-config description
```

Exit. No prompt; no further interaction.

---

## Mode 2 — View/update one key (`/aid-config <key>`)

### Step 1: Validate the key argument

Accepted keys:
- `name`
- `description`
- `type`
- `source_control`
- `minimum_grade`
- `heartbeat_interval`

If the key doesn't match: print `❌ Unknown key: <key>` + the accepted list + exit.

### Step 2: Ensure `.aid/settings.yml` exists

Same as Mode 1 Step 1.

### Step 3: Read current value

Run:
```bash
bash .aid/runtime/scripts/config/read-setting.sh --path <key> --default '(unset)'
```

Print: `Current value of <key>: <value>`.

### Step 4: Prompt for new value

Use `AskUserQuestion` for ALL keys with:
- A `Keep current value` option (description: shows the current value)
- 2–3 suggestion options from the Suggestions table below

Each option has only `label` + `description`. **Do NOT use the `preview` field** — the preview field switches the UI to a side-by-side layout that suppresses the auto-injected `Other` free-text input. With `description` only, the standard layout shows the `Other` field automatically and the user can always type a custom value.

Do NOT add an explicit `Other` option in the options list — the tool injects it automatically (and only renders it correctly when no option carries a `preview`).

For free-text-natural keys (`name`, `description`), the Suggestions table says `(no defaults)` — render the question with just `Keep current value` + the auto-injected `Other` field; the user types their value into Other.

Question text format (keep brief, mention free-text via Other if the user might want it):

```
New value for <key>?  (pick a suggestion or type your own via 'Other')
```

### Step 5: Validate

Per the Validation table below. If invalid: print the validation error + re-prompt (loop back to Step 4).

### Step 6: Save in place

Read `.aid/settings.yml` into memory. `settings.yml` is a flat file — every user-editable
key is a top-level scalar (`<key>: <value>`), no section nesting. Replace the top-level line
for `<key>` if one is present; otherwise append a new top-level `<key>: <value>` line at the
end of the file. Preserve all other lines and inline comments exactly as they are. Use a
same-directory temp file + `mv -f` for crash-safety (POSIX atomic rename), but no lock-dir
mutex — `aid-config` is interactive single-user; concurrent writes are not a real failure mode.

### Step 7: Confirm

Print: `✓ <key>: <old> → <new>` and exit.

---

## Validation table

| Key | Valid values |
|---|---|
| `name` | Non-empty string, no whitespace |
| `description` | Non-empty single-line string (NO newlines — settings.yml uses inline YAML scalars) |
| `type` | `brownfield` or `greenfield` |
| `source_control` | `none`, `git`, `svn`, or `mercurial` |
| `minimum_grade` | Regex `^[A-F][+-]?$`. E-grades are accepted but rarely useful as a floor. |
| `heartbeat_interval` | Positive integer (minutes). `0` disables heartbeat. |

---

## Internal keys (producer-written — NOT user-configurable)

`/aid-config` deliberately does **not** expose these — they are absent from *Accepted keys*
(Mode 2 Step 1) **and** from the Validation table above. They are written and maintained
by pipeline producers, never by the user. Running `/aid-config knowledge` (or any
`knowledge.*` sub-path) is rejected as an unknown key (`❌ Unknown key`) — that is the
intended behavior, not a gap.

| Key | Owner / contract |
|---|---|
| `knowledge` | Nested block `{source: <default-branch>, last_update: <ISO-8601 commit date>, doc_set: [...], term_exclusions: [...]}`. `knowledge.source` (the branch compared for KB freshness) and `knowledge.last_update` are written by `aid-discover` (on KB approval, FR35) and `aid-housekeep` (re-stamp on KB-DELTA refresh, FR36); read by the dashboard reader for outdated-detection (feature-007 FF-A2). `knowledge.doc_set` and `knowledge.term_exclusions` are runtime-written by `aid-discover`; `knowledge.doc_set` is also appended (one entry per document created) by document-creating `create` skills -- `/aid-create-roadmap`, `/aid-create-backlog`, `/aid-create-architecture`, `/aid-create-stack`, `/aid-create-testing-strategy`, `/aid-create-cicd` -- in the same run that creates their document, using the same R13 append-block idiom. `/aid-create-mvp` is the one planning sibling that is **not** on this list: it writes no KB document, so it appends no entry. Absence-tolerant — a missing `knowledge` block means "no baseline recorded" and the reader stays `approved`. Producer write-path (R13): the first write is a multi-line nested block (`source:` + `last_update:` + `doc_set:` + `term_exclusions:`) via the append-block idiom; a later `last_update` re-stamp is a single-line replace of that nested line. |

---

## Suggestions table (for Mode 2 AskUserQuestion)

| Key | Suggestions |
|---|---|
| `name` | (no defaults — user types their own) |
| `description` | (no defaults — user types their own) |
| `type` | `brownfield`, `greenfield` |
| `source_control` | `none`, `git`, `svn`, `mercurial` |
| `minimum_grade` | `A+`, `A`, `B+` |
| `heartbeat_interval` | `0` (disabled), `1`, `5` |

Always include a `Keep current value` option and let `AskUserQuestion`'s built-in `Other` field handle free-form input.

---

## How consumer skills read settings

Consumer skills (`/aid-discover`, `/aid-execute`, etc.) resolve `minimum_grade` using this order:

1. **`minimum_grade` in `.aid/settings.yml`** — use if present
2. **Hardcoded skill default** — use only if `.aid/settings.yml` is missing entirely, or the key is unset

The canonical resolution helper is `.aid/runtime/scripts/config/read-setting.sh`. Consumer skills invoke:

```bash
bash .aid/runtime/scripts/config/read-setting.sh --key minimum_grade --default A
```

---

## Schema reference

Canonical schema: `.aid/runtime/templates/settings.yml`. Flat top-level scalar keys
(`name`, `description`, `type`, `source_control`, `minimum_grade`, `heartbeat_interval`) as
described in the tables above. The `knowledge:` block is producer-written — see
*Internal keys* above, not user-configurable via this skill.
