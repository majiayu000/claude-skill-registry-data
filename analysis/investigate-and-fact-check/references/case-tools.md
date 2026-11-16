# Local case tools

Use `scripts/case.py` when an investigation needs persistent records, registered evidence, or a handoff across sessions. Run it with Python 3.10 or newer from the installed skill or a repository checkout. It uses SQLite from the Python standard library. The existing templates and [evidence-manifest helper](../scripts/evidence_manifest.py) remain available for lighter work.

## Open or resume a case

Keep cases outside the reusable skill and its Git repository. Choose a directory whose parent already exists. On systems with symlink aliases such as macOS `/tmp`, use the resolved path. Subsequent commands reopen the same case database.

```sh
python3 scripts/case.py case init /path/to/case --title "Contract review"
python3 scripts/case.py case status /path/to/case
python3 scripts/case.py records --case /path/to/case claims
```

`case.json` identifies the case and its schema. `case.sqlite3` stores its records and ID counters. Use `originals/` for the managed byte store, `derivatives/` for working copies, `analysis/` for notes, `logs/` for supporting logs, and `publication/` for material cleared separately for sharing. Protect the case directory and its exports with the same access controls as the evidence. Refer to [evidence and source security](evidence-and-security.md) for handling sensitive cases.

## Record sources, evidence, claims, and relationships

```sh
python3 scripts/case.py source add --case /path/to/case \
  --locator https://example.com/record --name "Original award notice" \
  --origin-group original-award-notice --type public-record
python3 scripts/case.py evidence add --case /path/to/case \
  --file /path/to/notice.pdf --source-id S001 --method "manual download" \
  --retrieved-at-utc 2026-11-12T12:00:00Z
python3 scripts/case.py claim add --case /path/to/case \
  --text "The notice authorises a EUR 100,000 ceiling" --support E001 \
  --scope "Authorised ceiling as of the notice date" --verdict Supported \
  --confidence high --confidence-reason "The original notice directly gives the amount"
python3 scripts/case.py case check /path/to/case
```

Use the returned IDs. Source IDs start at `S001`, evidence at `E001`, claims at `C001`, entities at `N001`, relationships at `R001`, unverified leads at `D001`, and runs at `U001`. An evidence registration records its hash, size, original filename, source, method, and optional parent or run. It copies bytes into the case and preserves the supplied file. Repeat registration creates a separate observation and reuses matching stored bytes. Supply `--retrieved-at-utc` only when the actual retrieval time is known. Registration time is recorded separately.

Set `--derived-from S001` on a source that depends on that record. Repeat the option for several dependencies. An origin group is a researcher-supplied label. A different label or URL alone cannot establish independence. Repeat `--support` and `--contradict` to retain each side of the evidence. A claim defaults to `Unresolved`. Provide the scope and reasons for a verdict after inspecting the evidence. The checker follows recorded source dependencies and reports potential corroboration gaps for review.

Use `entity add` with a stable registry identifier when available. `relationship add` links two entity IDs to supporting evidence with `--evidence E001`. Set `--basis directly_documented` only when the source establishes that specific relationship. Keep an inferred link and its limitations explicit. Use `--help` on each subcommand for all available fields.

## Collection, export, and recovery

See [source connectors](source-connectors.md) before using `collect run` or `recon import`. `records --case /path/to/case runs` shows what each run attempted, what it recorded, and whether it finished, failed, or returned partial results. A run interrupted before completion remains visible as `running`. Review its saved records and invoke a new run if needed. Use `--refresh` for a fresh provider response. Preserve earlier observations when repeating a check.

```sh
python3 scripts/case.py case export /path/to/case --output /path/to/case-export
python3 scripts/case.py case report /path/to/case --output /path/to/case-report.md
python3 scripts/case.py case checkpoint /path/to/case --output /path/to/checkpoint.zip
python3 scripts/case.py case restore /path/to/checkpoint.zip /path/to/restored-case
```

The export contains a full `case-records.json` plus CSV views. Existing ledger CSVs use their template columns. JSON retains additional fields such as run links and duplicate IDs. The Markdown report renders recorded claims, supporting and contrary evidence, source information, unresolved questions, leads, and run status. It is an internal research export. Review it before sharing.

The checkpoint contains the case database, configuration, and regular files in the case directory. Pause other writers before taking a checkpoint. Outputs must be outside the case. Restore requires a new destination and checks the archive inventory, hashes, and case integrity. Treat the ZIP as confidential when it includes sensitive records. Keep an independently protected copy and record its digest. The archive hashes establish consistency against the manifest and do not authenticate the case's sources.

Successful commands print JSON and exit `0`. Integrity errors and partial or failed collection return `1`. Invalid arguments and filesystem errors return `2`. Review warnings even when `case check` exits successfully. Follow the existing templates if your harness cannot execute local tools.
