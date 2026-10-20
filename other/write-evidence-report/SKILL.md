---
name: write-evidence-report
description: >-
  Load before a product is launched or written about: roll the latest test, QA,
  performance, security, and usability results into product/EVIDENCE.md. Trigger on "are we ready
  to launch", "what have we proven", or before a blog post or listing about the product.
argument-hint: "[product or path]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs git to pin the report to a commit. Running the test suite needs the project's own test
  runner; without it the Tests area is written as not run.
license: Apache-2.0
---

# Write the evidence report

Roll every Prove result into one committed file, `product/EVIDENCE.md`, that a later stage reads
instead of the scattered reports. Done means a dated section for the current commit sits at the top
of the file, every area has a status, and every claim under Claims cites the result behind it.

The checks leave their reports in the git-ignored `.agents_workspace/`, dated, one folder each. A
blog post or a listing that needs "is it tested, fast, safe, usable?" cannot use them: they vanish
on a fresh clone and none answers for the product as a whole. This file is the one answer.

## Procedure

1. **Pin the commit.** Run `git rev-parse --short HEAD` and `git status --porcelain`. A dirty tree
   is named in the report, because results then describe code nobody can check out.
2. **Run the test suite once.** Find the command in the repo's `CLAUDE.md`, README, CI workflow, or
   manifest scripts, run it, and record the command and its summary line (passed, failed, skipped).
   This run is the task, so it needs no separate request. When it cannot run (missing service,
   secret, or runner), the Tests area is `not run` with the reason.
3. **Collect the latest result per area.** Read, newest first, and take one per area (per metric
   for performance, per target for usability):

   | Area        | Source                                                                                                                                                                                    |
   | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | QA          | `.agents_workspace/qa/<timestamp>/QA_REPORT.md`                                                                                                                                           |
   | Performance | `.agents_workspace/perf/<metric>.md`                                                                                                                                                      |
   | Security    | `.agents_workspace/security-audit/SECURITY_AUDIT-<date>.md`                                                                                                                               |
   | Usability   | `.agents_workspace/ux-audits/<target>/run-<NNN>/UX_AUDIT.md` and `ERROR_MESSAGES.md`                                                                                                      |
   | Plan        | each plan in `product/plans/` with status `building`, plus each `built` plan whose `## Record` has no Evidence line yet: phases `done` with evidence, and any check-against-plan findings |

   With no such plan, the Plan area reads `none in flight`, not `not run`: nothing was skipped.
   Any other area with no source is
   `not run`, and names the skill that produces it: QA
   `ceh-testing:explore-app-for-bugs`, performance `ceh-testing:measure-performance`, security
   `ceh-security-audit:audit-codebase-security`, usability
   `ceh-usability-audit:simulate-newcomer-first-run`.

4. **Mark staleness.** For each result, find the commit it ran against (the report names it, or
   take the last commit before its date). When `git log --oneline <that>..HEAD` is not empty, the
   area is `stale` with the commit count, because the code moved after the check.
5. **Write the claims.** List only what a reader outside the team may be told, each one sentence
   with the area and figure behind it: "All 212 tests pass at a1b2c3d", "p95 search latency 38 ms
   on <machine>". A `stale`, `not run`, or `open issues` area yields no positive claim about the
   thing it checks.
6. **Add a dated section at the top of `product/EVIDENCE.md`**, below its `# Evidence: <product>`
   title, in the Output format. Never edit an earlier section: each one is what was proven at its
   commit, and a plan's Record cites it by date. With no file, create it with the title. A file in
   the older single-run layout keeps its content, under a section heading dated from its **Written**
   line. Commit it with the change it describes or on its own.
7. **Record the evidence in each plan.** Append an Evidence line to the `## Record` of each plan in
   the Plan area: the section date, the short SHA, and every area that is not `passed`.

## Rules

- Every figure is copied from a report or this session's test run, never estimated, reworded, or
  softened. A critical security finding stays critical.
- The file stands alone. Copy the numbers in: a link into `.agents_workspace/` breaks on any clone
  but the author's. Name the source path only as a pointer for the author.
- Never run the other checks from here. They are their own skills, and some need a running app or
  a person. Report them `not run` and name the skill.
- Open issues are listed, not judged: critical and high security findings, confirmed QA bugs not
  yet fixed, usability blockers, and plan items missing or failing their check.

## Output

```markdown
# Evidence: <product>

## YYYY-MM-DD at <short-sha>

**Tree:** clean | dirty (<n> files)

| Area        | Status                                          | Result                         | Checked at    |
| ----------- | ----------------------------------------------- | ------------------------------ | ------------- |
| Tests       | passed \| failed \| not run                     | `<command>`: <summary line>    | <sha>         |
| QA          | passed \| open issues \| stale (<n>) \| not run | <bugs found / fixed>           | <sha or date> |
| Performance | ...                                             | <metric>: <value> on <machine> | ...           |
| Security    | ...                                             | <counts by severity>           | ...           |
| Usability   | ...                                             | <blockers / friction counts>   | ...           |
| Plan        | ...                                             | <items built / missing>        | ...           |

### Open issues

- <area>: <issue, severity where the report gives one>. "None" when empty.

### Claims

- <one sentence a launch post may state> (<area>, <figure>)

### Not run

- <area>: <reason, and the skill that produces it>

<earlier sections follow, unchanged, newest first>
```

## Stop conditions

- The test suite fails → still write the report with Tests `failed`, list the failures under Open
  issues, and make no Tests claim. A failed run is evidence too.
