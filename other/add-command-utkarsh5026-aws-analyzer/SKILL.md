---
name: add-command
description: Add a new report command to an existing analyzer end to end - output design, pure analysis and findings, the analyzer method, the View method, tests, README and the docs guide - following the product rules in CLAUDE.md. Use for "/add-command dynamodb hot partitions" or whenever a user-facing View command is added or substantially reworked.
argument-hint: "<service> <what the user wants to see or decide>"
---

# Add a command

Request: `$ARGUMENTS`. The first word is the analyzer (`s3`, `dynamodb`, ...). The rest describes what the
user wants to see or decide.

If `src/aws_analyzer/<service>.py` doesn't exist, stop and suggest `/new-analyzer`. If the need is too vague to
design an output for, ask one question about the decision the user is trying to make.

## 1. Learn the neighbourhood

- Run `.venv/bin/python .claude/skills/demo/demo.py <service> 'ui.help()'` to list the existing commands. Pick
  the one or two closest to the request and read them in all layers: the View method (section 5), its
  analyzer method (section 4) and the pure functions and dataclasses it uses (sections 3 and 2). Also read
  their tests. Good models: DynamoDB `value_counts` / `table_info` and S3 `summary` / `what_if` / `deleted`.
- Look for something to reuse before writing anything new: parsing (`parse_s3_uri`, `parse_size`,
  `parse_time`, `_as_count`, key coercion), formatting (`human_*`, `_units`, `_plural`, `format_value`),
  existing iterators (`iter_objects`, `iter_items`) and existing `*_findings` functions.
- If the command needs an AWS API the analyzer doesn't call yet, check that it is read-only. Get / List /
  Describe / Head / Scan / Query / Select are fine. Anything that writes is out of scope, even behind a flag.
  Note the IAM permission it needs.

## 2. Design the output before the code

Write the report as the user will see it: a text mock, like the `mode="text"` output. Answer these:

- **The decision.** What will the user do after reading this? Put the number that drives that decision in a card.
- **Title and subtitle.** Say what was read ("408 items read (the whole table)") and any filter.
- **Cards.** Three to six of them, in human units, with the cost or read units of the command itself when it
  reads data.
- **Findings.** Write each as `(level, message)`: what's wrong, why it matters, the price where you can compute
  it, and the next step (a command, a setting, or the exact call to copy). Use `warn` only for things worth
  acting on.
- **Tables.** Put the detail here, the longest table last, with bars where a share matters.
- **Next.** The two or three commands the user would run after reading this, with the arguments filled in from
  the result (`get('orders', 'USER#0', 'ORDER#0000')`, not `get(table, key...)`).
- **The one-argument call.** Pick defaults so it's useful: a sensible `n` / `top`, a scan `limit=` that stops
  early, and a note saying the result is partial.
- **Failure paths.** Plan what shows instead of a traceback when a section can't be read (AccessDenied), an
  optional package is missing, or the input is wrong.

Name the command in the same style as the existing ones: short, and a noun or verb the user would guess
(`largest`, `value_counts`, `what_if`). The docstring's first paragraph is the help() text, so it describes what
the user will see. Add the command to the View's `_GROUPS` under the task it belongs to.

If the request left real choices open (what to rank by, what counts as "too big"), show the mock and confirm it
before building.

## 3. Build it layer by layer

Build in section order, so each layer can be tested on its own:

1. **Section 2, data model.** Add a `@dataclass` for the result. Give it a `to_df()` if it's tabular (pandas
   through `_require`), and `errors: dict[str, str]` if it reads several config sections.
2. **Section 3, pure analysis.** Write the computation and a `<name>_findings(result, prices=None)` that returns
   `[("warn" | "info", message)]`. No AWS calls, so it works on S3 Inventory rows or a DynamoDB export. Make it
   public (no underscore) when a user could call it on their own data.
3. **Section 4, analyzer method.** It calls AWS and returns the dataclass. It never prints. It accepts the same
   forgiving inputs as its neighbours. For long reads, take `limit=` and `progress=` and mark truncation. Catch
   `ClientError` per config section into `errors` instead of raising, so one missing permission doesn't take
   down the whole report.
4. **Section 5, View method.** Decorate it with `@_friendly_errors` and annotate it `-> None`. Wrap long calls in
   `with self._progress(...) as tick:` and pass `progress=tick`. Build blocks (`_Title`, `_Cards`, `_Findings`,
   `_Note`, `_Table`, `_Text`, and last `_Next` with calls made by `_call(...)`) and end with `self._show(blocks)`.
   Never print or build HTML directly. Show the price basis (`self._price_basis()`) next to any estimate. Give a
   card a tone only when a warning in the same report is about it; show statuses in tables as `_Tone` cells, a
   snippet to copy as `_Text(code=True)`, and raw JSON or tags with `collapsed=True`.

A helper that another service has, or could use, goes in `_kit/` once (`_bedrock/` for one only the Bedrock pair
uses), never as a copy: `rules.py` fails when a service defines a name `_kit` has.

## 4. Tests

Add tests to `tests/test_<service>.py`, each in the section with the matching `# ----- ` divider:

- **Pure functions**, with no moto: the numbers, edge cases (empty input, one item, wrong-typed input), and the
  findings. Assert on key phrases of each message, including the next-step text.
- **The analyzer method**, on moto with the existing fixtures. Other tests assert exact counts on the shared
  fixture data, so seed extra data inside your test instead of changing a shared fixture.
- **The View**, in text mode, through `run(capsys, ui.<command>, ...)`. Assert on the title, a card value and a
  finding.
- **A failure path**, when the command has one: a missing permission or a missing resource should show a note,
  not a traceback. Use `monkeypatch` or `botocore.stub.Stubber` to raise the `ClientError`.

## 5. Docs

- In `README.md`, under this service:
  - add a row to the command table
  - add the data method to "Getting the data" if it's new
  - list the pure function if it's public
  - add any new IAM permission to the permissions paragraph
- In `docs/<service>.md`:
  - add a row to the table under "Command reference" (`{ #reference }`)
  - add a paragraph in the section where the command fits
  - add the IAM permission under "Permissions"
  - Keep the page's existing Markdown conventions and tone, and check it with `mkdocs build --strict`.
- In `CHANGELOG.md`, add a bullet under `## [Unreleased]` → `### Added` (or `### Changed` for a reworked
  command): the command, and what the user can find out or do with it.
- If the command deserves a screenshot, say so and point to `/demo --html` (see the demo skill). Don't
  replace the images.
- Update CLAUDE.md only if the command changes the architecture: a new block type, a new convention, or a new
  price table.

## 6. Verify

1. Run `/check`, and fix everything it finds.
2. Run `/demo <service> 'ui.<command>(...)'` with the one-argument call and one call with options. Read the
   output as the notebook user would, and check it against step 2's mock and the product rules. Fix what reads
   badly. If the demo data can't set off the command's findings, extend `seed_<service>()` in
   `.claude/skills/demo/demo.py`.

## 7. Report

Give the user:

- the command's signature and help() line
- a short excerpt of the demo output
- the files changed (the analyzer sections, tests, README, docs)
- new IAM permissions
- anything left open

Don't commit unless asked.
