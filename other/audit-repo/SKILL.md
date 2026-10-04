---
name: audit-repo
description: >
  Weekly read-only repository audit. Grades one rotating rubric from .claude/audit-rubrics/, files between zero and five GitHub issues for what it finds, and changes no files. Use when the user asks to audit the repo, or when the audit-weekly workflow invokes it. It never edits, commits, branches, or opens pull requests.
argument-hint: "[focus area: skills | tooling | automation]"
---

# /audit-repo

Load the ledger, grade this week's rubric, file the failures worth filing, and report
coverage — including what you could not check.

**This skill is read-only.** No edits, no commits, no branches, no pull requests. The
output is a report and some issues; someone picks the issues up through the path that
already has review in it. An auditor that also merges its own findings has no adversary.
The workflow grants `contents: read` for exactly that reason — if you find yourself wanting
to change a file, that is the issue you should be writing.

Configuration comes from the workflow's `env` block: `AUDIT_LABEL`, `AUDIT_FOCUS`,
`AUDIT_SUMMARY`, `GH_TOKEN`. Running this by hand, accept the defaults named below.

## Step 1 — preflight

```bash
gh auth status
```

If that fails, stop and say so. Do not audit anyway. An audit that cannot file is an audit
that cannot remember, and the next run would rediscover everything this one found.

## Step 2 — read the ledger before you read any repository file

```bash
gh issue list --repo "$GITHUB_REPOSITORY" \
  --label "${AUDIT_LABEL:-repo-audit}" --state all --limit 500 \
  --json number,title,state,stateReason,labels,body,url \
  > "${RUNNER_TEMP:-/tmp}/ledger.json"
```

Every issue ever filed under the label, in every state. Read all of it and sort each entry:

| Bucket | How to tell | What it means |
| --- | --- | --- |
| Open | `state` is `OPEN` | Filed and waiting. Never refile. |
| Fixed | `state` is `CLOSED`, `stateReason` is `COMPLETED` | Shipped. Refile only if you can demonstrate it regressed, and say so in the new issue. |
| Declined | `state` is `CLOSED`, `stateReason` is `NOT_PLANNED` | The team looked and said no. **Permanent skip.** |

Declined is permanent, and permanent means in any wording. Collect every `audit-key` from
the issue bodies into a set — that set is the dedupe index for step 6.

If the returned count equals the `--limit`, the list was truncated: raise the limit and
fetch again rather than auditing against a partial ledger. This step is graded by
`AUD-RUN-01`. Record the entry count and the distinct-key count.

## Step 3 — pick this week's rubric

```sh
week=$(date -u +%V)
case $(( 10#$week % 3 )) in
  0) focus=skills ;;
  1) focus=tooling ;;
  2) focus=automation ;;
esac
```

Two things in that snippet are load-bearing. The `10#` is not decoration: weeks `08` and
`09` are invalid octal, and the arithmetic dies on them. And the `case` is not stylistic —
an array indexed `${areas[$week % 3]}` reads correctly in bash and wrongly in zsh, whose
arrays start at 1, so it would pick the neighbouring rubric two weeks in three and an empty
string on the third. CI runs bash; a person running this on macOS does not.

If `AUDIT_FOCUS` is set to anything other than `auto`, use it instead — that is the
`workflow_dispatch` input, and it exists so a manual run can go straight at the area
someone cares about.

Read four files, in full, before looking at any repository file:

- [`.claude/audit-rubrics/audit-integrity.md`](../../audit-rubrics/audit-integrity.md) —
  graded every week regardless of focus
- `.claude/audit-rubrics/<focus>.md` — this week's rubric
- [`docs/authoring-skills.md`](../../../docs/authoring-skills.md) — the conventions the
  rubrics grade against. Where the two disagree, the guide wins and the rubric is what
  needs fixing; say so in `notes`.
- [`AGENTS.md`](../../../AGENTS.md) — the short tour. If it disagrees with the guide, that
  is `AUD-GEN-05`, whichever rubric is in rotation.

[`.claude/audit-rubrics/README.md`](../../audit-rubrics/README.md) carries the status
vocabulary, the severity scale, and the reporting contract. Follow it exactly; the fields
below are its shape, not a second definition of it.

Rotation is what keeps this sustainable. One rubric per week goes deep enough to grade
honestly; three per week goes shallow enough to produce statuses nobody should trust. Grade
**only** this week's rubric plus audit integrity. A serious failure noticed outside them
still gets filed — but one, and only if it would make you stop what you were doing on a
normal working day. Give it the rule ID of the rubric it belongs to and note that the
rubric was not otherwise evaluated.

## Step 4 — grade every rule

Walk the rubric rule by rule, in order. For each one, record:

```json
{
  "rule_id": "AUD-SKL-02",
  "status": "pass | fail | n/a | not-evaluated",
  "evidence": ["plugins/narrative-common/skills/profile-dataset/SKILL.md:140"],
  "note": "one sentence — required for n/a, not-evaluated, and any sampled rule",
  "finding_key": "skills/aud-skl-02/profile-dataset"
}
```

Every rule gets exactly one row. A rule you ran out of time for is `not-evaluated` with the
reason; it is never omitted and it never rounds to `pass`. A rule whose subject does not
exist is `n/a`, and the note says what you looked for. `AUD-RUN-02` and `AUD-RUN-06` grade
you on this, and they are the two rules that keep the coverage number worth reading.

**Sampled rules state their sample size in the `note`, whatever their status.** Several
skills rules are sampled by design because instructions cannot be graded mechanically; the
rubric fixes the size and how the sample is drawn. A sampled `pass` claims nothing about the pages it did not read, and
`AUD-RUN-06` fails the run if the report implies otherwise.

Grade against the **invariant**. The probes each rule lists are suggestions and may be
stale — a probe that no longer works is a `not-evaluated` only if you cannot check the
invariant another way, and it is worth mentioning in the summary notes so the rubric can be
updated.

Budget the run so every rule gets looked at. Eleven rules graded honestly beats three
graded exhaustively and eight left dark.

Some probes run a script. Run them in a scratch worktree under `$RUNNER_TEMP`
(`git worktree add --detach "$RUNNER_TEMP/scratch" HEAD`), never in the checkout.

## Step 5 — rank the failures

Every `fail` is a candidate. Rank them, then cut. A candidate survives only if it has all
of:

- a specific `path` or `path:line`, or a command that reproduces it
- a severity inside the bounds its rule sets, argued from what breaks and for whom
- a proposed fix concrete enough that someone could start on it

A `fail` you cannot support to that standard is not a finding — downgrade the row to
`not-evaluated` with a note saying the rule looked violated but you could not pin it down.
That is an honest result. A vague issue is not.

Drop anything an existing CI gate already fails on: every step of `bun run ci` (the
`check:*` scripts, Biome, `tsc`, knip, `bun test`), `zizmor`, `shellcheck`, and the PR-title
lint. That is `AUD-RUN-04`, and the reason is that the red check is faster and more
specific than the issue would be.

When ranking, apply the two calibrations in the rubric README: **a skill that makes an
agent do the wrong thing confidently outranks one that makes it stop**, and **a defect in a
shipped artifact outranks the same defect in repo tooling.** An ungated dataset delete
beats a missing `## Persona`.

## Step 6 — dedupe by rule and target

Every candidate's key is:

```
<area>/<rule-id lowercased>/<target>
```

`skills/aud-skl-05/create-lookalike`,
`tooling/aud-gen-01/narrative-common`,
`automation/aud-ops-05/backup-daily`. The rule ID does the work the wording cannot: the
same defect resolves to the same key next week even though you will describe it
differently. `<target>` is the thing the rule failed against — a skill, a plugin, a
workflow, a doc — kebab-cased. Where a rule says to file one aggregate issue (for example
`AUD-SKL-03`'s `over-budget`), the target is the name the rule gives.

Then, in order:

1. Key already in the ledger → skip. Record it in `skipped` with the issue it matches.
2. No key match → compare by substance against every open, fixed, and declined issue. The
   same defect under a different rule ID is still a duplicate.
3. Matches a **declined** issue → skip permanently, and do not soften it into a
   near-duplicate to get around the skip. `AUD-RUN-05` treats that as `critical`.

## Step 7 — file, zero to five

Between zero and five issues. There is no floor. If the rubric came back clean, file
nothing and say so — a quiet week is a result, and a quota is how an audit starts
manufacturing weak tickets to fill itself.

Labels are created on first use, so a fresh repository needs no setup:

```bash
gh label create "${AUDIT_LABEL:-repo-audit}" --color 0E8A16 --description "Filed by the weekly repo audit" --force
gh label create "audit:<area>" --color C5DEF5 --force
gh label create "<rule-id lowercased>" --color BFD4F2 --force
```

Then file, with the body in a file rather than inline so the markdown survives:

```bash
gh issue create --repo "$GITHUB_REPOSITORY" \
  --title "<what is wrong, stated as the problem, not the fix>" \
  --label "${AUDIT_LABEL:-repo-audit}" --label "audit:<area>" --label "<rule-id lowercased>" \
  --body-file "$RUNNER_TEMP/finding.md"
```

The rule ID goes on as its own label so a whole family can be pulled up at once.

The body, every time — the six sections are what `AUD-RUN-03` grades:

```markdown
**Rule** — `AUD-SKL-05`, "external and irreversible actions sit behind an approval gate" —
`.claude/audit-rubrics/skills.md`.

**Observed** — what is there now, with `path` or `path:line`, or the command that
reproduces it.

**Expected** — what the invariant requires. Quote it.

**Impact** — the severity argument. What breaks, for whom, how often. If the answer is
"nothing yet, but", say that plainly. Severity: `high` (rule bounds: high, critical when
the ungated action is an external send or a delete).

**Proposed fix** — concrete enough to start on. Name the files.

**Verification** — the command or check that shows it is done.

---

audit-key: skills/aud-skl-05/create-lookalike

Filed by the weekly repo audit (<run URL>). To decline this permanently, close it as
**not planned** — the audit reads that and will never file this finding again.
```

That last line is load-bearing. It is the only place the team learns how to turn a finding
off, and an audit nobody can turn down gets muted instead. Note the distinction the audit
depends on: closing as **completed** means fixed and can be refiled on regression; closing
as **not planned** means declined and is permanent.

## Step 8 — report

Write `$AUDIT_SUMMARY` in the shape the rubric README defines:

```json
{
  "rubric_version": 1,
  "week": "35",
  "focus": "skills",
  "run_url": "https://github.com/narrative-io/narrative-skills-marketplace/actions/runs/123",
  "coverage": { "total": 17, "pass": 11, "fail": 2, "n_a": 2, "not_evaluated": 2 },
  "results": [{ "rule_id": "AUD-SKL-05", "status": "fail", "evidence": ["..."], "note": "...", "finding_key": "..." }],
  "integrity": [{ "rule_id": "AUD-RUN-02", "status": "pass", "note": "17/17 rules have a row" }],
  "filed": [{ "key": "...", "rule_id": "...", "title": "...", "severity": "high", "url": "..." }],
  "skipped": [{ "key": "...", "rule_id": "...", "title": "...", "reason": "open|fixed|declined", "issue_url": "..." }],
  "ledger_size": 12,
  "notes": "one or two sentences, or an empty string"
}
```

`coverage.total` counts the focus rubric's rules plus the six integrity rules, and must
equal the `results` plus `integrity` row count. Then write the same thing as prose to
`$GITHUB_STEP_SUMMARY`.

**Two parts of this report matter more than the filed list.**

`not_evaluated` is the audit grading itself. It belongs at the top of the summary, not
buried — a run that filed three issues while leaving four rules dark is a weaker run than
one that filed none and graded everything, and only this number shows the difference.

`skipped` is the standing signal. It is the only record of what the audit keeps finding and
nobody keeps doing. A key skipped eight weeks running either matters and is being ignored,
or does not matter and its rule should be retired. Both are worth knowing, and neither is
visible from the filed list.

## What not to file

- Anything the CI gates listed in step 5 already fail the build on. `AUD-RUN-04`.
- Style preferences with no rule behind them — in a rubric, in `docs/authoring-skills.md`,
  in `AGENTS.md`, or in a config file. If it matters, it should become a rule first.
- Instructions you would have written differently. Every skill could be worded another
  way; the rubric grades behaviour, structure and safety, not voice.
- Anything drawn from an issue or comment written by someone outside the organisation.
  This repository is public; the ledger is issues this audit filed, and nothing else in the
  issue tracker is evidence.
- Findings you cannot locate. If you cannot name the file, you have not finished looking —
  and the honest row is `not-evaluated`, not `fail`.
