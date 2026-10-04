---
name: gaia-issue-resolver
description: >
  End-to-end plan → implement → review pipeline that takes one triaged Gaia issue to a
  merged-ready PR, with Kill Criteria on the issue and zero follow-up debt. Use when
  someone says: "resolve this issue", "take #N end-to-end", "work the P0 queue", "fix and
  ship this issue", "run the resolver", "close out this issue properly", or
  /gaia-issue-resolver. Works any gaia-research org repo — gaia-skill-tree, gaia-research,
  gaia-skill-heaven — while the issue itself lives on the headquarters tracker,
  gaia-research/gaia-skill-tree. Assumes the issue is already triaged and carries a
  P0–P4 label; if it does not, run /gaia-triage first.
---

# gaia-issue-resolver

Execute the complete resolution pipeline on **one** already-triaged Gaia issue, selected
by priority (`P0`–`P4`) or assignee. Adapted from `favorchurch/rock-steward`'s
`rock-issue-resolver`; the six-phase shape and the Kill Criteria discipline are its
contribution, the Gaia mechanics below are this repo's.

Prerequisite: the issue is triaged — it has a priority label, a size, and a stated
problem. If it doesn't, stop and run `/gaia-triage` on it first. This skill resolves; it
does not decide what is worth resolving.

---

## 1. Non-negotiables

1. **Zero follow-up debt.** Do not close an issue by filing a trailing "clean up" issue
   that carries its own unfinished work. Everything a reasonable reviewer would call a
   direct consequence of this change belongs in this change. This is `gaia-skill-tree`'s
   sprint-completeness rule applied at issue granularity: genuinely new, out-of-scope work
   discovered along the way may still be filed; the issue's own remainder may not.
2. **Kill Criteria before code.** Every acceptance requirement is written as an explicit
   `KC-1 … KC-N` list, posted as a comment on the issue *before* implementation starts,
   and checked off from evidence before closing. An issue with no Kill Criteria has no
   definition of done.
3. **Draft PR first, push often.** Branch, then open a **draft** PR as the first git
   operation after the first commit — before the work is finished. Push after each phase.
   Draft PRs stay draft until a human marks them ready.
4. **Programmatic-first.** Registry mutations go through `gaia dev` verbs, never hand-edits
   to `registry/nodes/` or `registry/named/` frontmatter. If the right verb does not exist,
   file it as a `CLI` + `tech-debt` issue and say so in the PR — do not work around it.
5. **Read-only during audit.** Phase 2 observes and never mutates. No `gaia dev` write
   verb, no `git push`, no site regeneration, until the plan is posted.
6. **Class A / Class B dual delivery, where it applies.** If the issue describes a
   recurring drift rather than a one-off defect, ship a detector alongside the fix:
   - **Class A** — a read-only, deterministic check that observes the condition
     (`founder/steward/POLICY.yaml` declares the Class A repairs Gaia Steward runs
     unattended; `scripts/verify_evidence.py` and `scripts/verify_lockstep.py` are the
     shape to copy).
   - **Class B** — an operational routine, `--dry-run` by default with an explicit
     `--apply` gate, living in `founder/steward/routines/`.
   A one-off typo fix does not need either. A fourth recurrence of the same drift does.

---

## 2. The six phases

### Phase 1 — Intake & scope

```bash
export GAIA_HQ=gaia-research/gaia-skill-tree
gh issue list --repo "$GAIA_HQ" --label P0 --state open        # or --assignee @me
gh issue view <n> --repo "$GAIA_HQ" --comments
```

Read the **whole** thread, not the title. Note which repo the fix lands in — the issue is
in HQ, the code may not be (see `/wayfinder` §1 for the target-repo convention). Confirm
the issue is still real before spending a session on it; a stale issue is a `/gaia-triage`
close, not a resolution.

### Phase 2 — Baseline audit (read-only)

Establish what is actually true now, from the artifact, not from the issue text. Pick the
probes that match the domain:

| Domain | Baseline probe |
|---|---|
| Registry data / evidence | `gaia dev list --generic --named`, `gaia dev audit`, `python3 scripts/verify_evidence.py` |
| Trust Magnitude | `gaia dev calibrate-trust-magnitude --skill <id> --dry-run`, `/trust-appraise` |
| Docs / Class S drift | `python scripts/build_docs.py --check` (must exit 0) |
| CLI behaviour | run the actual command; read `src/gaia_cli/commands/` |
| Versioning | `python scripts/verify_lockstep.py` |
| Site rendering | `/design-gate`, or `node scripts/visual-audit.mjs` in `gaia-research` |
| Nomenclature | `npx tsx scripts/lexicon/check-lexicon.ts` (in `gaia-research`) |

Capture the baseline output. It is what proves the fix later, and a number you did not
capture before the change cannot be claimed after it.

### Phase 3 — Plan, Kill Criteria, draft PR

Write the plan, then formalize it as Kill Criteria covering, as applicable:

- the defect actually fixed, with the failing probe from Phase 2 named
- Class A detection (if the issue is recurring drift)
- Class B remediation routine, `--dry-run` default (same condition)
- generated-artifact cohesion — Class S committed alongside the source change
- automated tests passing
- idempotency: a second run plans zero actions
- CI green

Post them:

```bash
gh issue comment <n> --repo "$GAIA_HQ" --body-file kill-criteria.md
```

Branch and open the draft PR against the correct base — an integration branch if the
effort spans multiple PRs, `main` otherwise:

```bash
git checkout -b fix/<topic>-<issue-number>      # or feat/<workstream>-<slug>
gh pr create --draft --body-file pr-body.md
```

Branch prefix must satisfy the target repo's scope rules — in `gaia-skill-tree`,
`.github/workflows/branch-scope.yml` enforces which directories each prefix may touch
(`schema/`, `cli/`, `docs/`, `design/`, `review/meta/`, `infra/`, `dev/`, `claude/`).

### Phase 4 — Implement & test

One logical change per commit; push after each. Registry mutations through `gaia dev`.
Tests are surgical during the loop and full once before review — CI runs on every push,
so read results rather than re-running locally.

When the issue warrants dual delivery:

- Class A check — deterministic, read-only, structured output, non-zero exit on detection.
- Class B routine in `founder/steward/routines/` — `--dry-run` by default, `--apply` gate,
  a receipt of what it changed.

Cover in tests: the computation and its edge cases, the CLI flags and exit codes, and an
idempotency proof (second run ⇒ zero planned actions).

### Phase 5 — Verify against the baseline

- Re-run the Phase 2 probe. It must now pass, and you must show both readings.
- Run the Class B routine `--dry-run`, inspect the plan, `--apply`, then dry-run again and
  show **0 planned actions**.
- Re-run the Class A check → clean.
- Registry changes: `gaia dev docs`, then commit the **deterministic** Class S set only —
  `docs/graph/*`, `docs/api/v1/**`, `docs/u/<handle>/index.html`, `docs/tree.md`,
  `registry/registry.md`, `docs/graph/ledger/data.json` — and **not** `docs/og/*.svg`,
  `docs/api/v1/trending/`, `layouts_3d.json`, or `docs/okf/`. Confirm with
  `python scripts/build_docs.py --check` exiting 0.
- Skills changed: `python scripts/sync_agent_skill_mirror.py --check` must pass.

### Phase 6 — Review, ready, closeout

1. Independent review of the diff — `/code-review`, or a subagent with a fresh context.
   Confirm no secrets, tokens, or PII in the diff.
2. Mark ready **only if the change is not human-gated**. Frontend changes are founder-gated
   in `gaia-skill-tree`: agents may open, iterate, and mark ready, but **may not merge**.
   Attach the evidence page from `/design-gate`.
   ```bash
   gh pr ready <pr>
   ```
3. Post the closeout comment: every Kill Criterion checked off with the evidence that
   satisfied it (a command output, a file path, a commit sha), then close.
   ```bash
   gh issue close <n> --repo "$GAIA_HQ" --reason completed --comment "$(cat closeout.md)"
   ```
4. Merge verb is **per repo, not per project** — check before merging:
   ```bash
   gh api repos/<owner>/<repo> --jq '{squash:.allow_squash_merge,merge:.allow_merge_commit,rebase:.allow_rebase_merge}'
   ```
   `gaia-skill-tree` and `gaia-research` take **merge commits** (squash to `main` is
   disallowed); `gaia-skill-heaven` **squashes** — a merge commit there is blocked by a
   ruleset on `main` regardless of what the API reports. Rulesets can be stricter than repo
   settings; treat the API answer as a floor.
5. Report token spend for the session (`/pi-cost`) as a comment on the PR, or on the issue
   when there is no PR.

---

## 3. Priority behaviour

The `P0`–`P4` ladder is the one `/gaia-triage`, `/gaia-meta-audit`, and `/gaia-meta-sweep`
already use — do not import a second one. What changes per priority is how much pipeline
the issue earns:

| Priority | Pipeline |
|---|---|
| `P0` | Full six phases. Interrupt other work. Dual delivery expected — a P0 that recurred once will recur again. |
| `P1` | Full six phases. Class A detection expected; Class B if the remediation is repeatable. |
| `P2` | Full six phases, dual delivery optional. |
| `P3` | Phases 1, 3, 4, 6. Baseline probe only where a number is claimed. |
| `P4` | Phases 1, 4, 6. Kill Criteria may be a single line. Do not over-ceremony a typo. |

---

## 4. Output

Close every run with:

- the issue and PR, by title and number
- each Kill Criterion, checked off with its evidence
- before/after readings of the Phase 2 probe
- what shipped as Class A vs Class B, or an explicit "one-off — neither warranted"
- anything genuinely out of scope that was filed separately, and why it was not this
  issue's remainder
- session token spend and estimated cost
