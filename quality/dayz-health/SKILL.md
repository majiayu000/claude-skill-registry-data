---
name: dayz-health
description: "Shows a mod's health page: the last build, the last test, the open findings from lint, the gates and review, and the history of every gate run. /dayz-gate stores each result as JSON under .server/!Health/<ModName>/ and the script writes the page as Markdown and HTML. Use when the user asks how a mod is doing, what is still open, or what the last build or test said."
argument-hint: "<ModName> [--json] | --all [--json] | record <ModName> <build|lint|ingame|behavior|visual|review> [FILE] [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-health

A script reads the stored results and writes the page. It starts no process and needs no DayZ Tools. It reads nothing on `P:\`, so it does not gate on `/dayz-preflight`. The AI only reads the summary and tells the user what is open and who owns it.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\health.py" <ModName> [--json]
python "<skill-dir>\health.py" --all [--json]
python "<skill-dir>\health.py" record <ModName> <kind> [FILE] [--json]
```

| Argument | Notes |
|---|---|
| `<ModName>` | Rebuild and summarize this mod's page. A mod that has a `workspace/<ModName>/` folder but no results gets a page that says so. A name with neither a workspace folder nor stored results (usually a typo) is refused with `ERROR`, and nothing is created; the message lists the mods that do have results. `record` applies the same check. |
| `--all` | Every mod that has stored results. |
| `record` | Store one result by hand. `<kind>` is `build`, `lint`, `ingame`, `behavior`, `visual` or `review`. `FILE` is the report; without it the script reads standard input. |
| `--json` | Print the summary as JSON after the first line. |

`record` takes the JSON output of `/dayz-gate <mode> --json` or `/dayz-lint --json` (the verdict line before the JSON, text after it and a UTF-8 byte order mark are all fine), or a `dayz-mod-reviewer` report as text: a `PASS` or `FAIL` line, then lines of the form `<SEVERITY> path:line: what is wrong, and the fix -> <owner>`. A review may also be JSON with a `findings` list (it is read as JSON only when the report opens with `{`, so a text review whose finding quotes braces, such as `modded class Foo {}`, stays text); its `severity` is `CRITICAL`, `WARN` or `NIT` as in the text form (`fail` or `error` also count as failures), and any other severity is refused. A `/dayz-gate build` report with a `lint` block is stored as two results, the lint step and the build, exactly as `/dayz-gate` stores it, and `record` prints both paths (`also_recorded` in `--json` names the lint one). `ERROR` reports are refused, since they say nothing about the mod. A report that is missing a field (for example a finding with no `text`, or a behavior check with no `id`) or has a field of the wrong type is refused with `ERROR` naming the field, and nothing is stored. A JSON report whose `mod` is not `<ModName>` is refused, so one mod's results never land on another's page. A `FAIL` review with no line of that form is refused; a review line that looks like a finding but does not match (for example `ERROR path:12: ...` or a missing colon) is not stored, and `record` prints a warning naming it (`unparsed` in `--json`).

## Where results go

`/dayz-gate` stores every `PASS` or `FAIL` it gives, so the history fills itself. A `build` run stores two results, one for its lint step and one for the build (the same happens when you `record` a build report by hand). Both carry the same time; the lint file is named one microsecond earlier, so the history lists the lint step before the build it belongs to. Each result is one file:

```
.server/!Health/<ModName>/results/<UTC time>-<kind>.json
.server/!Health/<ModName>/health.md
.server/!Health/<ModName>/health.html
```

The folder sits under `.server/`, which git ignores, and outside `workspace/<ModName>/`, so nothing in it is ever packed into the PBO. The newest 200 results per mod are kept.

```json
{
  "schema": 1, "mod": "MyVest", "time": "2026-10-21T12:00:00Z", "kind": "ingame", "verdict": "FAIL",
  "findings": [{"severity": "fail", "category": "null_pointer", "file": ".server/!ClientDiagLogs/script.log", "line": 40,
                "text": "NULL pointer to instance", "owner": "dayz-script-specialist", "fix": "...", "count": 1}],
  "warnings": 2
}
```

A `behavior` result also has `checks` (`id`, `status`, `reason`), a `visual` result has `shots` (`id`, `status`, `reason`, `ratio`), and a result can have a `summary` line.

## The page

Both files hold the same content:

- **Last build** and **last test** (the newest in-game, behavior or visual result), each with its verdict and time.
- **Latest result per gate**: build, lint, in-game test, behavior test, visual test and review, with failure and warning counts.
- **Open findings**: every finding in the newest result of each gate, failures first, with where, what, owner and fix. A finding closes when a newer result of the same gate no longer has it.
- **Behavior checks** of the latest behavior run.
- **Visual shots** of the latest visual run: each shot's result and why it did not pass.
- **History**: the newest 50 results.

Times are UTC. Open `health.html` in a browser, or read `health.md` in the editor. `record` and `/dayz-gate` rebuild both files every time.

## Output and exit codes

The first line is `OK` (exit 0) or `ERROR` (exit 2: bad or missing arguments, no cached project, a bad mod name, a mod with no workspace folder and no stored results, or a report that is not a `PASS` or `FAIL` result or is missing a field). On `ERROR` the next line says why (with `--json`, a JSON object with `"verdict": "ERROR"` and `error`). On `OK` there follows one line per mod and the paths of its two pages:

```
OK
  MyVest: last build PASS (Build, 2026-10-21 12:00:00 UTC); last test FAIL (In-game test, 2026-10-21 12:10:00 UTC); 1 open finding(s); 6 result(s)
    .server\!Health\MyVest\health.md
    .server\!Health\MyVest\health.html
```

## Recording review findings

`dayz-mod-reviewer` cannot write files. When a reviewer report reaches an agent that can run commands (the orchestrator, or the main session after "review my mod"), save it with `record <ModName> review`. The newest review replaces the open review findings of the one before.

## Limits

- Only results stored since this skill was added are on the page. Older gate runs left nothing to read.
- `/dayz-lint` and `/dayz-build-pbo` run on their own do not store anything; `/dayz-gate build` runs lint and stores both.
- A gate `ERROR` is not stored.

## Do not

- Don't edit the result files by hand. Run the gate again, or `record` a new result.
