---
name: docs
type: Skill
title: "docs — place, edit, dedupe, verify and delete documentation"
description: "The procedure for every doc change in common-docs or a repo's CLAUDE.md, FEATURE.md or SKILL.md. Use when creating, editing, moving or deleting a doc, finding duplicate or disagreeing docs, planting a repo pointer, consolidating a node, or on /docs and the daily docs-steward run."
tags: [meta, docs-system]
timestamp: 2026-10-02T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/docs/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# docs — the procedure

The rules are [the rules of this bundle](/policies/document-types.md) and the
[domain tree](/policies/domain-tree.md). Read both once; this skill is only how to apply them.

## 1. Place it

1. Find the subject's node in the [domain tree](/policies/domain-tree.md) (Domain → Feature →
   Sub-feature). The doc goes in that node's folder under `systems/`, or in a temporary
   `projects/` folder only while work is tangled across two or more homes.
2. No node fits: add a feature where its domain clearly holds it (same commit, tell Arman), or
   propose the change in chat. Never invent a domain.
3. Something already covers the subject? Edit that file. Never create a parallel doc.
4. A repo keeps only rules tied to a code path in that directory (a trap, an import ban, a file
   map). Everything with meaning (what, why, status, plans, contracts, vision) lives in the node.

Done when: the target path is a node folder and no other file covers the subject.

## 2. Edit = whole-document review

1. Read the whole doc, not the section you came for.
2. Verify every claim you keep or add against live code, the DB, or git. A doc's own "verified"
   is not evidence. What cannot be checked here is marked `UNVERIFIABLE — <what would prove it>`.
3. Put the change where it belongs and merge in place: no addenda, no "Update:" blocks, no
   history, no changelog. Two lines saying one thing become one.
4. Cut what a frontier model already knows and what a command or file read reveals.
5. Never lose a rule: tightening keeps every invariant, path and pointer. Removing a rule is
   something you say out loud in your report.

Done when: the doc reads as one voice and every claim in it is currently true.

## 3. Dedupe and verify (one subject)

1. **Census.** Grep the subject's terms across common-docs and every repo it touches; follow
   one ring of links. List every file that makes claims about it.
2. **Elect the survivor**: the node's file from step 1.
3. **Classify each disagreement:** fact vs fact → reality decides, fix the loser; doc vs
   Arman's words → his words win, and code that drifted from them is a finding, not a doc fix;
   his words vs his words, or a disagreement about meaning → step 6, never resolved by you.
4. **Move, never copy.** One source file at a time: merge its unique truth into the survivor,
   `git rm` the source, repoint every inbound reference in every repo, commit all of it in one
   command. A file never exists in two places across a commit.
5. **Prove it.** For every deleted path, grep all repos plus common-docs: it comes back empty.

Never touch: generated files, a `.md` that code reads (grep `.py`/`.ts` for its name first),
a published package README, `inbox/`, a repo's `.arman/`. A spotted duplicate that is not
blocking you is still yours: run this section or dispatch it, never just report it.

## 4. Delete what is finished

Finished work shrinks to a status phrase on the node ("Gmail: live"). Finished projects, closed
handoff items, stale plans and bannered "superseded" docs are deleted, never archived. Git
holds history.

## 5. Arman's words

Any verbatim quote of Arman found outside a `VISION.md` moves, verbatim and dated, into the
closest node's `VISION.md` (create it with `type: Vision`, `authority: owner` if missing), and
the source line is cut. An agent's paraphrase attributed to him is deleted. Never rewrite,
trim or "fix" existing VISION content. You never set `authority: owner` on your own writing.

## 6. Conflicts

A disagreement about intent or a ruling: one or two sentences in
[/operations/conflicts.md](/operations/conflicts.md), then ask Arman in chat. When he answers:
delete the entry, apply the answer, tell him how many remain.

## 7. Repo pointer lines

Every repo that touches the node gets ONE line, in that feature's `FEATURE.md` or else the repo
`CLAUDE.md`, never a stub file and never restated content:
`Cross-repo system-of-record: /Users/armanisadeghi/code/common-docs/<path> — read it before touching this feature in ANY repo.`
A renamed or deleted doc orphans its pointers: grep every repo for the old path in the same
session.

Repo checks after a doc change: aidream `python3 scripts/check_doc_links.py` (`--all` for
package CLAUDE.md, PRINCIPLES.md, FOUND_DEFECTS.md, skills) and
`python3 scripts/check_docs_guards.py`; matrx-frontend `pnpm check:docs-guards` and
`pnpm check:doc-claims`. `FOUND_DEFECTS.md` IDs: [defect ownership § Entry IDs](/policies/reality-is-the-referee.md).

## 8. Finish

1. Frontmatter with a non-empty `type` on every new `.md`; bundle-relative links; the folder's
   `index.md` updated.
2. `python3 meta/scripts/okf_lint.py` exits 0. Editing a SKILL.md → also the
   [skill-authoring](/skills/skill-authoring/SKILL.md) rules and
   `python3 meta/scripts/skill_descriptions.py lint`.
3. **Fresh-reader review** for guidance you wrote (CLAUDE.md, SKILL.md, STATE, FEATURE, memory):
   dispatch one fresh `standard` agent with only the file paths and
   [reviewer-brief.md](/skills/docs/reviewer-brief.md) sent verbatim. Apply each `CUT`,
   `REWRITE`, `MOVE`; reject one only with a factual reason; answer each `ASK` from live
   evidence; turn a `GUARD` into code or a `feedback` item.
4. Commit by pathspec, `git pull --rebase`, push. Unpushed docs do not exist.

## Daily sweep (the docs-steward schedule)

Run in order; the commit message carries the scorecard (no log file).

- [ ] `okf_lint.py` to zero; `skill_descriptions.py lint --workspace`; `sync_skills.py --check`.
  In a detached worktree pass `MATRX_CODE_ROOT=/Users/armanisadeghi/code` or they find no repos.
- [ ] **Inbox:** each unprocessed item in `inbox/` is dispositioned per
  [/inbox/README.md](/inbox/README.md) and moved to `inbox/processed/<YYYY-MM>/`. Nothing in
  `inbox/` is ever deleted.
- [ ] **Tree drift:** every `platform.taxonomy_node.docs_path` exists; a new `systems/` folder the
  tree lacks gets added (clear domain) or a conflicts line plus a chat proposal.
- [ ] **Rotation health:** the separate dedupe-and-verify schedule runs §3 daily on the two nodes
  with the oldest `platform.taxonomy_node.last_reviewed_at` (nulls first) and stamps it. Report
  reviewed / never reviewed / oldest; a node past 45 days is an alarm in chat.
- [ ] **Delete finished:** §4 across new and touched docs.
- [ ] **Conflicts:** every entry in [/operations/conflicts.md](/operations/conflicts.md) is still
  open (a settled one is deleted) and phrased so he can answer it in seconds.
- [ ] **DDL guard log:** every row in `platform.ddl_guard_unacked` is acknowledged with live
  evidence through `platform.ddl_guard_ack(...)` or filed as a defect (run
  `select audit.refresh();` before reading certification).
- [ ] **Pointers:** repo guards from §7 run; pointer lines into this bundle resolve.
- [ ] **Expired facts:** grep `re-check after (\d{4}-\d{2}-\d{2})`; each past date becomes one
  `feedback` item ([declared vs observed state](/policies/declared-vs-observed-state.md)).
- [ ] Commit, push. Never create or change a schedule.

## Old skill names

| Old | Now |
|---|---|
| `docs-steward` | Daily sweep |
| `cross-repo-docs`, `context-docs` | §1, §2, §7, §8 |
| `dedupe-and-verify`, `doc-convergence`, `consolidate` | §3–§5 |
| `future-reader-review` | §8.3 |
