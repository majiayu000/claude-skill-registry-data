---
name: code-health
description: New security, complexity and architecture findings in your changes - how to read the code-health review that blocks your stop when you finish, fix each finding or accept it on purpose, and run the check for a diff. Use with shark:code-authoring when you write or correct code in a project whose AGENTS.md has analyze rows.
---

# Code health

A project that opts in names its analyzers in AGENTS.md (`## Commands`: `analyze:file`, `analyze:diff`,
`arch:check`, `analyze:full`) and its limits in `## Quality budgets`. Shark runs them and shows you only what is
**new**: a finding that is not in the committed baseline, not allowed on purpose, and not in the file at the commit
where your session started. Old debt never shows. AGENTS.md wins over a rule here.

## 1. When you finish: the review

The shark hook `health-review` reviews your work when you end it, like a code reviewer. When the main session stops,
or when `shark:code-writer` or `shark:lead-engineer` ends, it runs `analyze:file` on each source file that changed
since the session started (also changes that you committed), and compares each file with its version at that commit.
It prints nothing when nothing is new. When something is new, it stops you from ending and gives you a digest. You
get each finding one time in a session, and at most 3 reviews block in one session. A later review checks only the
files that changed since their last review; when none changed, it only runs `git`. In a multi-repo workspace it reviews each repository in `## Repositories`, with the
project file of that repository (its `analyze:*` commands and budgets). `hook.review: off` turns it off.

```text
code-health: 2 new in src/billing/invoice.py (budget: ccn 10)
1. ERROR sec/sql-string-concat  L42  SQL text built from a value at run time ...
   Fix: use a bound parameter, for example execute("... WHERE id = ?", (value,)).
   id: 3f9c0a12b4de
2. WARN  cx/ccn  L60  `apply_discounts` ccn 9 -> 14 (budget 10).
   Fix: see complexity-playbook.md (guard clauses, extract function, table-driven rules).
   id: 8a71c3e09f42
+0 more. Not verified: none.
```

Treat a digest like a failing test:

1. **Fix it before you finish.** An `ERROR` is a defect that you made. Fix the code, not the rule. The fix hint
   names the safe form. For complexity, use [references/complexity-playbook.md](references/complexity-playbook.md).
2. **Or accept it on purpose**, only when the finding is a false positive or the brief asks for this exact code:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/code-health/scripts/health.mjs" baseline allow <id> --reason "<why>" [--lane <lane name>]
   ```

   A lane always gives `--lane`: lanes never write `.shark/health-baseline.json`. The lead folds lane entries into
   the baseline at merge, and lists each one in the merge log. "It was faster" is not a reason.
3. **A layer violation (`arch/...`) is a shared decision.** Do not change the architecture rule and do not allow
   it. Return it to your caller with the import that you need and why.

A digest about a line that you did not change is still yours when your change caused it (for example, a function
that crossed the complexity budget because you added a branch).

`code-health: not verified (...)` means that an analyzer is missing, crashed or timed out. Continue, and write
"code-health: not verified" with the reason in your report. Never report the code as checked.

## 2. Your report, and the check by hand

The review in §1 runs by itself. Run the same check by hand only when `hook.review` is `off`, or to check a branch
(for example before a merge):

```bash
node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/code-health/scripts/health.mjs" diff --base <the commit where your work started>
```

Exit 0: nothing new. Exit 1: the digest lists what is new; fix it or allow it as above. Exit 3: the project has no
analyze row (say "code-health: not configured"). Exit 4: an analyzer failed (say "code-health: not verified").
Your report has one line: `Code health: <n> new, <n> allowed (ids and reasons), not verified: <items or none>`.

## 3. Commands

| Command | Does |
| --- | --- |
| `health.mjs file <path> [--base <ref>]` | New findings of one file (what the hook runs). |
| `health.mjs diff [--base <ref>]` | New findings of all changed files, plus `arch:check`. |
| `health.mjs baseline record` | Records the committed baseline (`.shark/health-baseline.json`) from the current code. |
| `health.mjs baseline compare [--base <ref>]` | New, worsened and fixed findings. |
| `health.mjs baseline allow <id> --reason <text> [--lane <name>]` | Accepts one finding on purpose. |
| `health.mjs baseline fold` | Moves the lane allow files into the baseline (the lead, at merge). |
| `health.mjs sarif --out <file> [--only sec,arch,cx]` | Merged SARIF for CI, GitHub code scanning or SonarQube. |
| `health.mjs rules add` | Copies the starter rules for the languages of the project to `.shark/rules/`. Keeps a rule file that exists. |

Exit codes: 0 clean, 1 new findings, 2 usage error, 3 a command row is missing in AGENTS.md, 4 an analyzer crashed
or timed out.

## 4. Set it up in a project

`/shark:init` does this setup and checks it (`skills/init/scripts/doctor.mjs`). By hand: add the rows to AGENTS.md ›
Commands, and run `health.mjs rules add` to copy the starter rules of this skill to `.shark/rules/`:

| Key | Example (Python and TS) |
| --- | --- |
| `analyze:file` | `opengrep scan --quiet --disable-version-check -f .shark/rules --sarif-output={out} {file}` and `lizard --csv {file}` |
| `analyze:diff` | none (shark runs `analyze:file` on each changed file) |
| `analyze:full` | `opengrep scan --quiet --disable-version-check -f .shark/rules --sarif-output={out} .` and `lizard --csv .` |

- `/shark:doctor` installs Opengrep (the release binary, with its SHA-256 checked) and Lizard (hash checked) into the
  shark tool folder, and shark runs them from there with no PATH setup. Never install Opengrep from PyPI (a
  malicious package uses the name). Keep
  `--disable-version-check`. Do not use `--experimental`: in 1.33.1 it found nothing on the starter rules.
- One Opengrep 1.x scan of one file takes about 2 s, mostly start-up (p95 2.2 to 2.3 s, measured 2026-11-21). Shark
  scans the file and its base version in parallel. The review runs one time when you finish, not after each edit:
  per-edit checks cost tokens and wake-ups and changed no result in the cost check (2026-11-25).
- Use `lizard --csv`: the XML format has no end line and no parameter count.
- Write your own rules ([references/rule-authoring.md](references/rule-authoring.md)). Never copy rules from the
  Semgrep registry: their license does not allow distribution.
- Commit `.shark/health-baseline.json` after `baseline record`. A project with no baseline still works: shark then
  compares each file with its content at the start of the session.

The digest format and its limits are in [references/digest-format.md](references/digest-format.md).
