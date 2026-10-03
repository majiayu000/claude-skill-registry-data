---
name: merge-cleanup-deep
description: >
  Read-only, sub-agent-driven triage of the checkouts /merge-cleanup preserved (PRESERVE_UNPUSHED,
  PRESERVE_DIRTY, PRESERVE_UNVERIFIED_*): zip each clone to a dated backup with a manifest, fan out at
  most three read-only agents grouped by branch family, and establish per clone — by ancestry, by
  per-file content against development and open PR heads, and by QA attestation — whether its
  unlanded work is PR-WORTHY, SUPERSEDED, NEEDS-OWNER, or an ABANDON-CANDIDATE, then hand off
  (fresh-clone PR, issue comment, or /merge-cleanup teardown). Never mutates a clone and never
  deletes anything. Trigger on /merge-cleanup-deep, "deep scan the clones", "what is in these old
  clones", "which clones are worth a PR", "are these task clones safe to delete", or when a
  /merge-cleanup run leaves PRESERVE_* rows that the operator wants dispositioned. Not for landing
  PRs or tearing down clones — that is /merge-cleanup.
---

# /merge-cleanup-deep — Preserved-Checkout Triage (backup → fan-out → verdicts → handoff)

`/merge-cleanup` preserves any checkout it cannot *prove* landed, and its Phase 3 only escalates with
"recommend a deeper scan". This skill is that deeper scan. It owns the judgment the script refuses to
make — is the unlanded work in this clone worth a PR, already landed under another name, or scrap —
and it produces evidence an operator can act on. It reads; `/merge-cleanup` writes.

Strictly adheres to [`WORKTREE-SAFETY.md`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/WORKTREE-SAFETY.md) and [`AGENTS.md`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/AGENTS.md).

---

## Recite this — verbatim, as the first thing in your first response

> **Merge-Cleanup-Deep Discipline:**
> 1. **Intake from the scanner, never a second discovery (Phase 0).** Take `/merge-cleanup`'s audit
>    (`scan_clones.py --json`) and select the non-exempt `PRESERVE_*` rows; list live checkouts as
>    skipped, never as candidates.
> 2. **Back up before you look (Phase 1).** Zip every candidate with its `.git` to a dated backup
>    folder and write the manifest; no analysis starts on an un-backed-up clone.
> 3. **Fan out read-only, grouped by branch family (Phase 2).** At most three sub-agents, every clone
>    of one branch name to the same agent, hard read-only rules, evidence checklist a–g, verdicts
>    with the deciding line.
> 4. **Re-verify before you believe (Phase 3).** Every "unique defect" claim is re-checked against
>    current `development` and open issues; one landed-elsewhere claim per family is spot-checked by
>    the caller; ancestry is not content and a clean diff is not provenance.
> 5. **Hand off, do not mutate (Phase 4).** PR-WORTHY → fresh clone and cherry-pick; NEEDS-OWNER →
>    issue comment naming the backup; SUPERSEDED / ABANDON → the list goes to `/merge-cleanup`
>    teardown; a clone equal to an open PR head is a hold, named with its PR.
>
> **Overall Goal:** Every preserved checkout carries a verdict, the evidence line that decides it,
> a backup it can be restored from, and one next step — with nothing in any clone changed.

Then begin work.

---

## When to use / not use

- **Use** after a `/merge-cleanup` run leaves `PRESERVE_UNPUSHED` / `PRESERVE_DIRTY` /
  `PRESERVE_UNVERIFIED_*` rows and the operator wants to know what is in them; or standalone when a
  parent directory has accumulated task clones nobody remembers.
- **Do not use** to land PRs, to tear down clones, or to "fix" a clone in place. Teardown stays in
  `/merge-cleanup` Phase 6 (fresh inspection, Trash only, GH-534 A.5). PR creation goes through
  `/start-task`-style fresh clones. This skill writes only to the backup folder, the scratchpad, and
  — on request — a GitHub issue comment.

## Why a separate skill

`/merge-cleanup` is script-owned, parity-guarded and pinned by tests; its rule is *the script owns
the evidence and the cap, the caller owns the analysis*. This triage is caller-owned judgment, costs
three agents' worth of tokens per run, and must be opt-in. Discovery is not duplicated: Phase 0
consumes the scanner's JSON, and Phase 4 hands the disposable list back to the scanner's teardown.

---

## Phase 0 — Intake from the scanner

```bash
python3 skills/2-daily/merge-cleanup/scripts/scan_clones.py --json \
  --primary "$PRIMARY" --root "$(dirname "$PRIMARY")" --prefix <repo-name> > "$SCRATCH/scan.json"
```

- Pass `--root` explicitly: `SAFE_ROOTS` does not include the primary's own parent, and SOP task
  clones are siblings of the primary (#722). An empty table is "unscanned", not "clean".
- Candidates are rows whose disposition starts with `PRESERVE_` and is not `PRESERVED_USER_EXCLUDE`
  or `PRESERVE_WIKI`. `PRIMARY_CHECKOUT` is never a candidate.
- Rows carrying `ACTIVE_WRITING`, `ACTIVE_PROCESS`, `ACTIVE_TICK_CLAIM`, or a driver lock are **live
  sessions**: list them under "live — skipped" with the reason, and never assign them to an agent.
  The same applies to any clone whose directory name matches an open PR's branch that another
  session is still pushing to.
- Record the shared facts every agent needs: `origin/<integration>` head, merged PR heads and
  squash SHAs for the branches involved, open PR heads (`gh pr list --state all --head <branch>`).

## Phase 1 — Backup before analysis

```bash
DEST="$HOME/Documents/Backups/<repo>-clones-$(date +%F)"; mkdir -p "$DEST"
printf 'clone\tbranch\thead\tdirty_files\tzip_sha256\tzip_bytes\n' > "$DEST/MANIFEST.tsv"
( cd "$(dirname "$PRIMARY")" && zip -ryq "$DEST/<clone>.zip" "<clone>" )   # -y keeps symlinks, .git included
```

- `.git` is included on purpose: the unpushed refs are the point. Exclude nothing but
  `node_modules`/`.venv` if size forces it, and say so in the manifest.
- The manifest row is written from the clone *after* the zip (branch, HEAD, dirty count, sha256,
  bytes) so a restore can be checked against it.
- Zipping is read-only for the clone; it may run in the background while Phase 2 starts.

## Phase 2 — Fan-out (≤3 read-only sub-agents)

Group candidates so that **every clone of one branch name goes to the same agent** — ancestry chains
between five clones of `feat/gh646-status-label` can only be established by one agent that can
fetch each HEAD into a temp ref. Balance the remaining clones for count. Use the prompt template in
[`agents/scan-prompt.md`](agents/scan-prompt.md); fill in the clone list, the shared facts, and the
report path. Sonnet-class agents are sufficient; the checklist does the work.

Hard rules the template carries (a violation is worse than an incomplete report):

- Never run `git checkout/switch/reset/stash/clean/rebase/merge/commit/push/branch -D`, `rm`, `mv`,
  or any test suite (`validate.sh`, `test/*.sh`, `pytest`) in a clone. Never edit a file in a clone.
- `git -C "<path>"` for every command; never `cd` into a clone.
- `git fetch` is allowed (origin, a PR head into `refs/deepscan/prN`, a sibling clone's HEAD into
  `refs/deepscan/<name>`); every `refs/deepscan/*` ref is deleted with `git update-ref -d` at exit.
  A clone whose `origin` is a local path fetches the integration branch from the GitHub URL.
- Report only to its own scratchpad file. Nothing else is written anywhere.
- Other agents' clones, the primary, and live-session clones are out of bounds.

Per-clone evidence checklist (the agent quotes commands and output):

| | Evidence | Command shape |
|---|---|---|
| a | remote, branch, HEAD, dirty files (diff shown unless a generated view), ignored files of note | `git remote -v`, `status --porcelain --untracked-files=all`, `status --ignored` |
| b | unlanded commits **per local ref** incl. `backup/*` and a detached HEAD, files touched | `log <dev>..<ref>`, `diff --stat $(merge-base <dev> <ref>)..<ref>` |
| c | landed-elsewhere: by **ancestry** (`merge-base --is-ancestor <ref> <merged-pr-head>`), by **content** per non-generated file (`diff <dev> <ref> -- <path>`; empty = landed; distinctive-identifier `git grep` on `<dev>` for reshaped hunks), and against **open PR heads** (`refs/pull/N/head`) | one line per file: LANDED / PARTIALLY LANDED (what remains) / NOT LANDED |
| d | QA attestation: `relay-drive: attest … approved`, `final QA approved`, `LGTM`, `QA approved` in commit messages, `relay-system/`, `PROJECT/2-WORKING/GH-*`; quote it and say **what** it attests (plan vs implementation) | `git log --grep`, `grep -rn` |
| e | linked issue(s) and state | `gh issue view N --json state,title,closedAt` |
| f | family view: ancestry between the clones of one branch name; which holds the superset | `merge-base --is-ancestor` pairwise on temp refs |
| g | **verdict** with the deciding evidence line and one next step | see below |

Verdicts:

- **PR-WORTHY** — unique, coherent work not on `development` or in an open PR, attested or one QA
  round from attested. Names the files and the issue it closes.
- **SUPERSEDED** — the content is on `development` or in an open PR; names the PR/commit and the
  diff that proved it (a deletions-only diff against the merged head is the classic signature).
- **NEEDS-OWNER** — unique work that is incomplete or unattested; names what is missing (a QA round
  that never ran, a `Blocked` status header, an escalated relay).
- **ABANDON-CANDIDATE** — nothing unique beyond generated views (`LEADERBOARD.md`, `releases.*`),
  scratch, backups whose content landed, or a doc `development` deliberately deleted.
- **HOLD** — HEAD equals an open PR's head exactly; keep until that PR lands or closes.

## Phase 3 — Synthesis with re-verification

The caller does not forward verdicts; it checks them.

- Every **"unique defect / unfiled finding"** claim is re-run against current `development`
  (`grep -n` the cited lines) and against `gh issue list --state all --search …` before it becomes
  intake. Today's finding: both "undisposed blockers" a QA relay surfaced were already #656/#657, and
  the fix for them lived in a *different* clone family.
- One **landed-elsewhere** claim per family is spot-checked by the caller with
  `git -C <clone> diff <dev> HEAD -- <path>`.
- Watch for the shared false positive: a file that `development` deliberately deleted after the
  clones forked shows as "unique" in every clone (`PROJECT/1-INBOX/GH-505-*.md` on 2026-09-21).
- Evidence standards (workhorse Rung 5): ancestry proves graph reachability; per-path blob/diff
  identity proves content; an attestation proves review, not landing. A commit not being an ancestor
  is **not** evidence its content is missing; a clean diff is **not** provenance.
- Produce one disposition table: clone · verdict · deciding evidence · next step. Copy the agent
  reports into the backup folder (`<DEST>/deep-scan/`) so the analysis outlives the session.

## Phase 4 — Handoff (no mutation here)

| Verdict | Handoff |
|---|---|
| PR-WORTHY | Fresh full clone from `origin/<integration>`, cherry-pick the named hunks/tests (never push the stale branch as-is — its base is typically dozens of commits old), final QA per repo policy, one PR naming the issues. |
| NEEDS-OWNER | Comment on the linked issue: clone name, backup zip path, what is missing. |
| SUPERSEDED / ABANDON-CANDIDATE | Hand the list to `/merge-cleanup … --teardown-only --execute` (fresh inspection, Trash only). Never `rm -rf`; never move a clone by hand. |
| HOLD | Name the PR; re-run after it lands. |
| live — skipped | Report; the owning session decides. |

The backup zips make teardown doubly recoverable (Trash + zip); say so in the report so the operator
can empty Trash without losing the restore path.

## Worked example — 2026-09-21, XYZ-forge, 14 preserved clones

3 agents (5/5/4, grouped by branch family), ~380k tokens, 20 minutes; zips 991 MB. Result: 1
PR-WORTHY (`closeout-evidence-fixes`: real fixes for #656/#657, final QA never run, base 64
commits old), 1 HOLD (`gh646-pr-completion` == draft #723 head), 12 SUPERSEDED/ABANDON — including
five independent re-executions of one GH-646 plan whose core connector was byte-identical to #723,
and a flightdeck branch whose diff against the merged #719 head was deletions only. No clone was
modified; every `refs/deepscan/*` ref was deleted.

## Safety guarantees

1. **Zero mutation of any clone.** Sub-agents run under hard read-only rules; the caller never
   writes into a clone either. Backups happen before analysis.
2. **Discovery and teardown are not duplicated.** Phase 0 is the merge-cleanup scanner's JSON;
   Phase 4 returns to the merge-cleanup teardown.
3. **Live sessions are never triaged.** Activity, open handles, tick claims, and driver locks make
   a checkout "skipped", not "candidate".
4. **Verdicts are re-verified.** No finding becomes an issue, and no clone becomes disposable, on a
   sub-agent's word alone.
