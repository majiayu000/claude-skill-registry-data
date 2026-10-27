---
name: triage-backlog
description: >
  Triage a GitHub issue backlog — classify, prioritize, dedup, and groom issues.
  Repo-agnostic: each repo supplies its own label taxonomy via a triage.json config.
  Use when: triaging new issues, clearing the needs-triage queue, grooming the backlog,
  prioritizing issues, hunting duplicates, splitting oversized issues, or deciding what
  to work on next. Triggers: triage, needs-triage, issue queue, backlog grooming,
  prioritize, reprioritize, dedup issues, label issues, what should I work on next.
metadata:
  version: 0.10.0
---

# Issue Triage

Repo-agnostic GitHub issue triage. Reads every issue in **one** `gh` call, derives all
signals locally, and leaves mutation to explicit `gh` commands you run after deciding.

Reasons about abstract concepts (untriaged / blocked / owner-decision markers, ordered
priority axis, area/type tag families). Each repo maps them onto its own label names —
see [taxonomy](references/taxonomy.md).

## Workflow

0. Pass the taxonomy gate (Step 0 below) — resolution must succeed before anything else.
1. Resolve the repo (`-Repo` > config `repo` > origin remote > error) and taxonomy
   ([taxonomy](references/taxonomy.md)).
2. Show the queue (terminal) — needs-triage issues with form-proposed priority/area.
3. Emit signals JSON + HTML report — the full decision payload. **Unconditional:**
   run this even when the queue is empty. The board (including the `grooming` block
   over all open issues) is this session's deliverable, not a byproduct of triage.
4. Triage each queued issue from the payload ([pass](references/workflows.md)).
5. Apply with `gh`, then handle closes/splits/re-anchors ([ops](references/operations.md)).
6. **Surface the report link** — always give the user the `file://` URL of the
   generated board. A run that ends without handing over the link is incomplete.

Run the scripts **from the target checkout** (`Set-Location <repo>`), invoking each
by absolute path from the installed skill folder (the folder containing this
`SKILL.md`). That single cwd choice makes config discovery (repo-local `triage.json`)
and the default output location ([Output location](#output-location)) both resolve to
the target repo with no extra flags. If you run from the skill folder instead, pass
absolute `-Config` and `-OutFile` paths.

## Step 0 — taxonomy gate (mandatory)

Every entry point resolves the taxonomy against the repo's **real** label set
(`gh label list`) and **stops** when a required label is missing. No queue, no
signals, no report — a stale config would otherwise render an empty queue as if
there were nothing to triage. A failed `gh label list` also stops the run: the
label set is never guessed.

On failure the scripts throw with both next steps:

- **A. Create the missing labels** (same taxonomy the failing run resolved; the
  printed command carries its `-Config` when one was in play):

  ```powershell
  .\scripts\triage-bootstrap.ps1 -Repo owner/name [-Config path/to/triage.json]
  ```

- **B. Map your own labels** (keep your repo's names): add a `triage.json`
  (`triage.json` / `.triage.json` / `.github/triage.json` in the target repo
  checkout — or pass `-Config <path>`) mapping each concept — see
  [taxonomy](references/taxonomy.md#config-file). Or preview one via
  `-WriteExampleConfig`:

  ```powershell
  .\scripts\triage-bootstrap.ps1 -Repo owner/name -WriteExampleConfig .github/triage.json
  ```

Then re-run the queue or signals script. `-NoLabelCheck` skips the gate for
offline/tests only: output may be wrong or empty, the payload is stamped
`taxonomy.label_check: "skipped"`, and `triage-report.ps1` refuses to render it.

## Queue

```powershell
Set-Location <repo>            # target checkout - run everything from here
$s = '<skill>\scripts'         # absolute path inside the installed skill folder
& "$s\triage-queue.ps1"        # the queue
& "$s\triage-queue.ps1" -All   # grooming view, grouped by priority
```

The queue is every open issue carrying the configured `needs_triage` label.

## Signals → decisions → apply

Do **not** make per-issue `gh` calls. One call produces every signal; you do the
semantic work on the payload; `gh` is used only to mutate.

```powershell
Set-Location <repo>
$s = '<skill>\scripts'
& "$s\triage-signals.ps1" -Json    # payload to the pipeline (add -OutFile to save)
& "$s\triage-report.ps1"           # signals (auto-generated if missing) + board
```

The JSON is self-describing (`taxonomy` block + `summary.priority_counts` keyed by
portable code). Per queued issue: labels, age, form-proposed priority/area,
roadmap/goal refs, issue refs, open-vs-closed dependency state, dedup candidates,
body excerpt — plus a `grooming` block. Read it once, decide the whole queue.

The report prints a path + `file://` URL — hand that URL to the user (Step 6).
Never spawn a browser — this often runs headless (VPS/Docker).

## Output location

**One location: `<repo>/.github/triage-backlog/`** — resolved automatically by
`triage-report.ps1` when `-SignalsFile`/`-OutFile` are omitted. Explicit
`-OutFile`/`-SignalsFile` still win for a single run; nothing else redirects it.
`triage-signals.ps1` writes there too when pointed at it, and makes the folder
self-ignoring just as the report does.

The board is an **ephemeral artifact**: it embeds issue titles and labels, so it
must never be committed. The skill enforces that itself — it writes a nested
`.gitignore` containing `*` into the folder, so the artifacts are ignored in any
repo without touching the repo's tracked root `.gitignore` (which would otherwise
surface as a diff the maintainer has to commit). `*` also ignores the `.gitignore`
itself, so the folder stays invisible to `git status` while remaining browsable on
disk. If the folder is somehow not ignored, the run warns.

`output_dir` in `triage.json` is **deprecated**: it is no longer honored, only
reconciled from.

### Migration from earlier versions

On activation in an existing repo the skill reconciles artifacts left behind by
earlier versions into the canonical folder, so a stale board neither lingers nor
looks lost:

| Deprecated location | Origin |
|---|---|
| `<git-dir>/triage-backlog/` | previous default |
| `<git-dir>/backlog-triage/` | pre-rename default |
| `.github/backlog-triage/` | pre-rename opt-in |
| `./cache/` | legacy non-git fallback |
| config `output_dir` | deprecated override |

Only the skill's own artifact filenames are moved, under hard rules — this runs
unattended and mutates the working tree:

- **Never overwrites.** The canonical copy is authoritative; a deprecated copy is
  by definition older. If the destination already exists the move is skipped and
  reported, so a stale payload can never displace a fresh one.
- **Never moves a git-tracked file.** A hand-written file that merely shares an
  artifact filename (e.g. a committed `docs/triage-report.html` reached through a
  config `output_dir`) is left alone and reported.
- **Never deletes anything.** A deprecated folder is removed only when it is left
  completely empty, and never under the git dir — git owns that tree.
- **Best effort.** A failed move warns and continues; migration is not a
  precondition for rendering.

The migration is idempotent and reported on stdout. It runs only for the
defaulted run (a bare `triage-report.ps1`); a caller that passed explicit
`-SignalsFile`/`-OutFile` has opted out and the repo is not mutated.
`-NoReconcile` skips it explicitly.

Definition of done: gate passed · board generated under
`<repo>/.github/triage-backlog/` · `file://` link handed to the user · queue
triaged (if any) · mutations applied.

## Autonomy contract

Apply-and-report with hard gates. Apply labels + post a rationale comment (the review
surface), no confirmation ping. Stop and confirm before closing, splitting, rewriting
a body, or changing a roadmap status. Ask one focused question when the priority
heuristic ties on this cycle's work or you would override the form-proposed priority.

## References

[taxonomy](references/taxonomy.md) · [pass + heuristics + grooming](references/workflows.md) · [scripts + close/split/re-anchor + cycle](references/operations.md)
