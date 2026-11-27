---
name: report-claim-audit
description: >-
  Audit a status report or memo, dispatch summary or closeout digest against per-item records,
  manifests and validator logs. Recompute counts, find omitted files and price pending choices.
  At a phase wrap-up, reconcile the milestone index, release and production pins; list live runs,
  PRs and deferred loose ends. Read-only.
metadata:
  revision: "6"
  areas: "work-management,software-development"
  targets: "runtime-agnostic"
  summary: "audit report claims and omissions or close out a milestone against its task inventory, release, and actual deployment pin"
  summary_zh: "审计报告声明和遗漏，或用任务清单、实际发布与部署锁定版本核查阶段收尾"
  kind: "entry"
---

# Report claim audit

A daily dispatch, teammate handoff, or closeout digest is a set of claims, not evidence. This skill
is the pass that turns it into a decision brief the operator can answer with numbers instead of
re-reading the repo themselves.

## 0. Pin your authority before reading anything

Open the role contract that governs the run: who may write which paths, what needs operator
approval, what must never be written. Everything below is shaped by it — an audit run usually
licenses *reading* and at most a `notes`/`STATUS` write, never a repair of what it found.

At a phase or milestone wrap-up, even without a memo, read the [closeout checklist](references/milestone-closeout.md)
before reading summary prose.

## 1. Recount every claim from the artifact that owns it

- Numbers come from the per-item JSON, the control manifest, the index, or the validator's own output —
  never from the report's table. A report correct eight times running is still a hypothesis on the
  ninth.
- Re-derive derived counts (N of M complete, X cells missing a key) by walking the per-item files in
  code, not by re-reading the report's prose. Print what you computed next to what it claimed.
- Verify absence claims with the negative search. A confirmed absence is itself a finding about the
  surface: "no STATUS.md exists anywhere" reframes the run from *reading* status to *deriving* it, and
  that recurring cost belongs in the brief.
- When the report names a validation command, locate the script before trusting the result. A path that
  does not exist is your error, not a failed check: search the repo for the basename, run it, report
  that rc.
- Re-run the repo's cheap gates once (validator, test runner, portability check) and quote real counts
  — "205 tests, 0 failures, 8 environment skips" is proof; "tests pass" is not.

## 2. Look for what the report did not say

- Account for the deliverable set by **diffing lists**, never by grepping dump text. Enumerate the
  paths inside the control manifest and the acceptance record, enumerate disk by artifact pattern,
  diff both directions. A substring search over a serialized JSON dump misses a name nested under
  another key and false-positives on hex hashes. Shape:
  ```python
  d = json.load(open('control/artifact-manifest.json'))
  recorded = set(re.findall(r'[A-Za-z0-9._/-]+\.md', json.dumps(d, ensure_ascii=False)))
  # diff against a glob of the deliverable filename schema
  ```
- A file on disk but invisible to the record is a stronger finding than the "missing review" usually
  reported: it sits in a surface declared closed, so nobody will review it and later readers trust it.
  Lead with it. Read the accepted-artifact list *separately* from the manifest's general artifact list
  (rejected vs accepted decides the remedy) and count mentions in the closeout report — zero mentions
  corroborates the diff, it does not contradict it. Report four numbers together: on disk N, in
  manifest M, in accepted set K, mentioned V.
- Check `git status` and the worktree yourself; "clean tree" is a claim like any other, and it also
  tells you whether another writer is mid-edit.
- Separate **already ruled** from **pending**. An approved exception (a known dangling-link baseline,
  a registered legacy class) is not a decision item — listing it again trains the operator to ignore
  the whole list. Name it in one line as covered by the standing exception.

## 3. Price the decisions

- Compute the cheap mechanical facts (per-item sizes, key counts, aggregate characters) even when you
  cannot rank quality: they convert "72 drafts" into "72 drafts = 3.7M characters of semantic review",
  which usually answers the question by itself.
- One take per decision: recommend first, then the mechanism that makes the rejected branch expensive
  (what must be re-opened, re-sealed, re-reviewed, or re-run). State plainly what you cannot infer at
  all (external filing numbers, operator-only facts) instead of hedging around it.
- Keep recommendations inside the frozen envelope. Proposing a new research round, a new evidence class,
  or a re-opened lifecycle is an operator decision, not an audit finding.

## 4. Act only inside your boundary

- Do not invent the surface you found missing. A new status/notes file in a repo that has none, or in a
  subset of its projects, reproduces exactly the unaccounted-file defect you are reporting; inside a
  manifest-bound directory it is silently wrong.
- Route surface gaps to the role that owns that path. Hand over the **judgement**, not a prescription:
  the facts, the two possible rulings, the boundary (no commit, no claim change, no new file surface).
  A teammate told "fill the gap" fabricates entries to satisfy you.
- Never repair records, change pins, deploy, clean up, commit or push from an audit run. Leaving the
  tree untouched is a reportable result — say it was deliberate, and why (writes need approval).

## 5. Output shape

1. Verdict on the report: which claims you reproduced, with the numbers you computed.
2. Findings the report missed, defect first.
3. Numbered decisions, each with your take and the cost of the branch you reject, so the operator
   replies with a number instead of prose.
4. What you did and did not touch, including delegated handoffs by name.

Plain text in a terminal, one point per line, no markdown decoration: the operator may be reading this
on a phone.

## Pitfalls

- Reporting the digest's own counts back as verification of the digest.
- Declaring a named validator clean from an assumed path, or unclean because the path was wrong.
- Substring-grepping a serialized manifest to prove a file is or is not listed; walk the structure and
  extract path-shaped strings instead.
- Keeping state "durable" by dropping a notes file into a sealed artifact directory.
- Answering a decision list with questions instead of a recommendation plus the reason to reject the
  costly branch; "it depends" hands the question back unchanged.
- Re-raising items the corpus already covered with an approved exception.
