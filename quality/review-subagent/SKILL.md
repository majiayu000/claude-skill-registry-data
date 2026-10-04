---
name: review-subagent
description: "Review, improve, and adversarially verify a generated subagent package (subagents/<slug>/): a reviewer panel finds real issues, then grounded fixes, then an independent adversarial re-verify, converging to zero must-fix. Use after a package is generated (e.g. by /author-subagent) to take it from validates to trustworthy. Invoked as /review-subagent <slug> [--rounds N]."
---

# Skill: review-subagent

**Trigger:** `/review-subagent <slug> [--rounds N]` — run after a subagent package is
generated (e.g. by `/author-subagent`) to review, improve, and adversarially verify it.

**Purpose:** Take a just-generated subagent package `subagents/<slug>/` from "validates" to
"trustworthy": a reviewer panel finds real issues → **grounded** fixes → an **independent
adversarial re-verify of those fixes** → converge to zero must-fix. Stops before git merge (the
package converges on a `review/<slug>` branch; the human merges).

Complements `author-subagent` (generates) and `subagent-maintenance` (source/platform changes).
This skill reviews the QUALITY of a generated package, not the health of a generation run.

**Load-bearing principle:** *never trust a delegated fix.* A first fix pass and even a hardening
pass routinely leave real defects (incomplete fixes, surviving over-claims). Every improvement is
independently re-verified before it is trusted. `validate` PASS ≠ complete/correct.

---

## Step 1 — Preconditions

Require `subagents/<slug>/profile.yaml`. If absent, stop — nothing to review.

## Step 2 — Select the reviewer panel DYNAMICALLY (never a fixed list)

The panel is two parts. Choose it **fresh every run** so a newly-generated reviewer is automatically
eligible — as the factory produces more advisors/reviewers, they become reviewers for future subagents.

**A. Structural lenses — always, domain-independent** (built into the loop; they review the
subagent-*as-a-generated-artifact*):
`agent-skills-advisor` (skill authoring) · `profile-reviewer` (release-readiness) ·
`faithfulness-reviewer` (over-claim) · `ai-agent-engineering-reviewer` (agent design) · plus the
deterministic gates `validate_generated_package` + `quote_scan`.

**B. Domain lenses — selected dynamically**, to independently cross-check that the new subagent's
guidance is domain-CORRECT (accurate, complete, current):

1. **Read the live roster** — `ls .claude/agents/*.md .claude/agents/generated/*.md`; for each, read
   the frontmatter `name` + `description` (what it reviews/advises, its when-to-use / not-for). Do
   this *every run* — the roster grows over time; do not hardcode it.
2. **Read the target's domain** — `subagents/<slug>/profile.yaml` `role` + `when_to_use` (+ the source
   topic / `source-pack.manifest.yaml`).
3. **Select the 1–3 best domain matches** — the roster agents whose expertise overlaps the target's
   domain. Match *semantically* on the descriptions. **Exclude** the target itself, the four structural
   lenses, and any agent whose `when_not_to_use` rules out this domain. If the package ships code / an
   MCP server / tests, also add `python-reviewer` and the relevant `mcp-*-advisor` / domain advisor. If
   nothing in the roster fits, **structural-only is correct — say so**.
   - *Illustrative only (NOT a fixed map — the pick is whatever the current roster offers for the
     current target):* a DB-advice subagent → `postgresql-sqlite-advisor`; a security one →
     `application-security-reviewer` / `mcp-security-advisor`; a testing one → `software-testing-advisor`;
     an architecture one → `software-architecture`; a k8s one → `cloud-native-kubernetes-advisor`.
4. **Record the chosen panel** (structural + the dynamic domain names) so the run is reproducible, and
   confirm each chosen agent is actually deployed under `.claude/agents/`.

## Step 3 — Headless review→fix→review loop (context-clean)

Run detached, passing the dynamic domain panel as `DOMAIN_REVIEWERS`:

```bash
DOMAIN_REVIEWERS="<name1> <name2> …" \
  bash campaign/detach.sh bash campaign/review-subagent-loop.sh <slug>
# env: MAXROUNDS(3) MODEL(claude-opus-4-8) REV_EFFORT(high) FIX_EFFORT(high) DOMAIN_REVIEWERS("")
```

Each round runs a **fresh `claude -p`** for the review (the 4 structural lenses + your dynamic domain
lenses via Task + the deterministic gates → consolidated
`subagents/<slug>/reports/review-loop/<slug>.rN.review.md` ending `MUST_FIX_COUNT: <n>`) and another
fresh session for the fix. It gates on `MUST_FIX_COUNT=0` AND `validate` PASS, commits converged work to
a `review/<slug>` branch, else caps after `MAXROUNDS`.

**Monitor by ARTIFACTS, never transcripts** (context hygiene): poll `reports/review-loop/*.rN.review.md`
for `MUST_FIX_COUNT`, count `<slug>.CLEAN`, tail `campaign/logs/review-loop.log`. Wait via the **Monitor
tool** or **ScheduleWakeup** — a plain `run_in_background` sleep-loop gets reaped by the env; the setsid
loop itself survives. Expected shape: `mf` starts small, a fix can surface its own gaps (round 2 may
*rise*), round 3 converges toward 0.

## Step 4 — Triage any residual

If the loop caps with residual, read only the final-round `rN.review.md` (small — the consolidated
findings, not the `.jsonl` transcript). Classify each surviving must-fix:
`real-blocker | real-polish | drift-nitpick` × `mechanical | needs-source(grounded) | owner-decide`.
A thorough panel legitimately caps at 1–3 real items; that is convergence, not failure.

## Step 5 — Improve (grounded)

Apply the residual must-fix + high-value should-fix. **Grounded, always:**
- Introduce no claim not in `principles/principles.yaml`; a skill body cites only its own principle IDs.
- A faithfulness over-claim is *weakened* to its cited principle — verify the citation actually supports
  the rule (re-cite if not); never reword blind. A domain-accuracy finding is fixed only if the corpus
  grounds the correction — otherwise flag it (the subagent can't advise beyond its sources).
- On **any** version bump: increment `agent_version` **and** add both a `CHANGELOG.md` entry **and** a
  `provenance-ledger.md` Version History entry (supersession rule), then `cli export <slug>`
  (`cli stale --stamp <slug>` if digest WARNs) and `validate_generated_package` until 0 FAIL.
- Watch the phase-8 body-size **hard FAIL >1000 words**: if an edit tips the profile over, trim
  non-load-bearing prose in the same profile — never drop the fix.
- **Owner-decide / deliberate-design items are flagged, not fake-fixed.**

## Step 6 — Adversarial verify (the "enhance" — do NOT trust the fixes)

Spawn **independent** verifiers to check the improvements, adversarially:
- `faithfulness-reviewer` on the changed profile — re-derive every rule's claim-strength from
  `principles.yaml`; report anything still `SCOPE_BROADENED / HEDGING_REMOVED / CONTRADICTED`.
- Re-run the same **dynamic domain lenses** on any content that changed — confirm the fix is
  domain-correct and introduced no new domain error.
- If code/tests changed: an adversarial code/security reviewer per fix (`CONFIRMED-good | HOLE |
  BETTER-OPTION`), and prefer **mutation-tested** regression tests (revert the fix → the test must FAIL →
  restore), not "the suite passes".
- Any **HOLE** → fix (grounded) → **re-verify** (find → fix → re-verify). Loop until zero holes. Expect
  the first verify pass to find real gaps — that is the point.

## Step 7 — Converge + report

Report the converged state: the `MUST_FIX_COUNT` trajectory, what was fixed vs found-and-fixed-on-verify,
the **panel that was selected** (structural + dynamic domain), and any residual **owner-decide** items
(design/deployment, not code) left for the human. Confirm `validate` PASS. **Stop before merge** — the
verified package sits on `review/<slug>`; the human reviews + merges (CI-gate the PR: poll
`gh pr checks` until pass, then merge).

---

## Gotchas (hard-won)

- **Empty-prompt clobber:** `printf … | claude -p … </dev/null` — a trailing `</dev/null` overrides the
  piped prompt → claude runs only SessionStart hooks (~9.6KB hook-only runlog), instant `rc=1`, no output
  file. The pipe IS stdin; add no redirect. (Already fixed in `review-subagent-loop.sh`.)
- **bg sleep-monitors get reaped** by the env; the **setsid loop survives**. Monitor via the Monitor tool
  / ScheduleWakeup, and track progress by review-file artifacts, not the shared log string.
- **Ledger-bump:** a fix that bumps `agent_version` without a `provenance-ledger.md` entry re-creates a
  ledger-staleness must-fix every round → the loop never converges. The fix prompt now requires it.
- **`validate` PASS ≠ done.** It gates structure/anchors/quotes, not faithfulness over-claim, not domain
  accuracy, not code correctness, not fix completeness. The adversarial verify (Step 6) is the real gate.
- **`pkill -f <pat>`** self-kills the Bash-tool shell when the pattern is in your own command line (exit
  144). Kill by explicit PID or process-group; use the `[c]laude` bracket trick for pgrep.
- **Shared-working-tree fix-loss (root cause of "phantom fixes").** The loop used to commit only on
  CLEAN, so each round's fix edits sat *uncommitted* on the review branch — a **concurrent `git checkout`
  in the same working tree** (e.g. a human merging sibling PRs) silently discarded them, and the next
  `.fix.done` marker then claimed a version the disk never had. Fixes: the loop now (a) runs with an
  **overridable `REPO`** so a manager can point it at an **isolated `git worktree`**, and (b) **commits
  every round that reaches `validate` PASS** (durable). When taking a review over in-session, do the same
  — work in a worktree (`git worktree add -B review/<slug> <path> <base>`), not the shared main tree.
- **Marker-vs-disk.** A `.fix.done` marker is written by a possibly-dead/cap-killed session; it is not
  truth. Gate on the package's **actual `validate` state + `agent_version` on disk**, never the marker.
  A dead headless session may already be valid — check the package, not the marker.
- **Silent adapter/skill truncation is a whole class, and only a domain lens catches it.** A generator can
  render a *complete-looking* but truncated must-hold invariant or skill step (a 160-char cut, or a first
  sentence split inside `(e.g. …)`), silently dropping a safety hedge from the artifact the agent loads —
  and `validate`'s coverage check only sees the `[Pxxx]` **tag**, not the surviving **content**. The loop
  now has a deterministic truncation gate (`grep '…'` / dangling `(e.g`), and `compile_invariants` renders
  complete first sentences + fails on a truncated invariant — but the read that *found* this was
  `translation-quality-reviewer` (a domain lens on the safety skill), which 3 loop rounds + 5 other
  verifiers missed. Keep a safety-relevant domain lens on the panel for any safety/legal-bearing subagent.
- **The precedence / any multi-principle tie-breaker field is the hardest to converge** — it will surface
  a real, *distinct* finding for several rounds (scope → citation → inversion → conflation). Ground each
  clause STRICTLY to one principle's claim; don't over-trim (a trim inverted "governs *over* a literal
  rendering") and don't over-trust a domain reviewer's *suggested* wording without re-checking the corpus
  grounds it (a suggestion manufactured a P080 clinical-case-study anchor). Re-verify only the changed
  clause each round.
