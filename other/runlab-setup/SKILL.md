---
name: runlab-setup
description: Set up runlab for this athlete — choose a data source, prove it can actually deliver, create the data root, and run the first import. Use when the user asks to "set up runlab", "install runlab for my runs", "connect my watch data", or invokes /runlab:runlab-setup. Creates files and can take minutes, so only the user starts it.
allowed-tools: Read, Bash, AskUserQuestion
disable-model-invocation: true
argument-hint: "[data-root-directory]"
---

# runlab setup

Onboarding has one job: end with a data root that contains real runs, and with an
honest statement of which analyses this source can and cannot support. A setup
that finishes with an empty cache and a cheerful summary is the failure mode to
avoid.

## Standing rules for this whole workflow

- Every script is invoked through the interpreter shim, never through a bare
  `python3`:

  ```
  bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/<script>.py" [arguments]
  ```

- Before relying on a flag, run the script with `--help`. If it disagrees with
  what is written here, follow `--help` and say the skill is out of date. If a
  script is missing or exits 127, say so plainly and stop. Do not read the raw
  files yourself and do not compute a substitute; the whole design rests on
  numbers coming from scripts.
- Never write `profile.json` or anything under `state/` with Write or Edit. A
  PreToolUse hook blocks it. `init-db.py` writes the profile at setup;
  `update-db.py` writes it afterwards.

## Step 1 — preflight

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py" --json
```

Options: `--root <dir>` to check a specific data root, `--offline` to skip every
network check, `--strict` to treat warnings as blocking.

The output holds `ok`, `n_checks`, `counts`, `checks[]` and `blocking[]`. Each
check carries its own verdict and, where something is missing, the hint that
names it. Relay the hint; do not paraphrase a reason code into a guess.

If the preflight already finds a data root, this project is set up. Ask whether
the user wants a second project or a re-import, and overwrite nothing.

## Step 2 — choose the source with AskUserQuestion

Present only sources whose preflight is green, plus the ones a purchase would
unlock. State the real cost and the real capability loss. The long form, with
endpoints, device requirements and the vendors' own pages, is in
`${CLAUDE_PLUGIN_ROOT}/docs/SOURCES.md` — read it before answering a question
this table does not cover.

| Source | Prerequisite | Running mechanics? |
|---|---|---|
| FIT files (HealthFit) | HealthFit, one-time purchase; Apple Watch SE or Series 6 and newer on watchOS 9+ | yes |
| Runalyze REST | Supporter tier | yes, for activities that were uploaded as FIT |
| Runalyze MCP | Premium tier, personal API token | yes, plus streams and health data |
| GPX / TCX files | none | **no** — no ground contact, no vertical oscillation |

Mechanics is the capability that separates form analysis from distance
counting. If the user picks GPX or TCX, say in the same breath which skills
will return `insufficient_data` forever.

## Step 3 — create the data root

Default location: `<project>/rundata`. Any directory works; the marker file
`.runlab-root` is what makes it findable, not the name.

`init-db.py` reads the onboarding answers as JSON on stdin, or from a file.
Write the answers to a scratch file first so the user can read them before
anything is created, then:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/init-db.py" \
  --answers-file <answers.json> --dry-run
```

`--dry-run` validates and reports the plan without writing a byte. Run it first,
every time. Then drop the flag to create. Other flags: `--data-root` overrides
`answers.data_root`, `--force` claims a directory that already holds unrelated
files, `--no-register` skips the project registry.

The answer keys are a closed set — an unknown key is a typo, not an extension:
`data_root`, `label`, `sources`, `athlete`, `anchors`, `zones`, `preferences`,
`custom_patterns`, `register`, `schema_version`, `note`.

```json
{"data_root": "/path/to/project/rundata",
 "label": "marathon block",
 "sources": {"fit": {"dirs": ["/path/to/HealthFit/Documents"]}},
 "athlete": {"birth_date": "1990-05-04", "sex": "female"},
 "anchors": {},
 "register": true}
```

**Leave `anchors` empty unless the athlete actually knows a value.** There is no
"220 minus age" in this script and there must be none in your answers either. A
missing anchor blocks a zone statement; a wrong one produces a confident false
statement, and three months later nobody can tell it from a measurement. If a
value is known, record it with its quality: `measured`, `estimated`,
`working_value`, `literature`, `lower_bound`. A formula result is `estimated`.

The script is idempotent: a second call creates nothing, destroys nothing, and
reports per artefact whether it was created or already there.

## Step 4 — first import

Fetch the activities with the sync script, then confirm what landed:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" \
  --section computed.activities --section computed.data_quality
```

Long histories take minutes. Report what arrived from `computed.activities`
(`n_running`, `first_date`, `last_date`, `span_days`) and
`computed.data_quality.channels`, where every channel gives `n` and `n_total`.
Never a share without its denominator.

## Step 5 — say what is now possible

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" --section computed.gates
```

Each gate lists `requirements[]` with `have`, `need` and `shortfall`. That is the
honest closing summary, and it needs no invention:

1. Gates with `ok: true` — analyses that work today.
2. Gates with `missing[]` — what is short, quoted as the `shortfall` ("three more
   weeks with runs"), not as "not enough data".
3. Capabilities the chosen source can never deliver — from the table above.

Then hand over: `/runlab:runlab-status` for the short view,
`/runlab:runlab-report` for the full one.

## Failure modes worth naming out loud

- **Sport filtering.** A German Runalyze account calls the sport `Laufen`, an
  English one `Running`. Adapters normalise this to `running`; if the first
  import returns zero runs, that is a bug to report, not an empty training
  history to accept.
- **iCloud placeholders.** FIT files in an iCloud folder may be stubs that
  trigger a download on open. `sync.py` skips unmaterialised files and reports
  how many; relay that number instead of pretending the import was complete.
- **Duplicates.** One workout can arrive twice, from the watch and from a second
  device. Ids are content-derived, so duplicates collapse — but if the report
  shows a suspicious pair, name it.
