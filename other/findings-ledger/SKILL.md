---
name: findings-ledger
description: Use when recording, tallying, or triaging stochastic review findings — the append-only JSONL ledger where Tier 2 (advisory, unevidenced) reviewer output goes instead of blocking language. Triggers on "log this finding", "ledger add", "tally the findings", "triage findings", "is this finding recurring", "retire this noise", or whenever a reviewer produces an unevidenced concern that should be measured for recurrence rather than chased. For the review itself see code-review-and-quality or skill-library-review; for verifying formal claims with deterministic evidence see adversarial-claims-reviewer.
when_to_use: |
  Use when a reviewer (human or agent) produced a Tier 2 finding — pure LLM
  judgment with no deterministic evidence artifact — and it needs to be recorded
  so recurrence across independent runs can be measured; when tallying which
  findings keep coming back; or when triaging the ledger for promotion (encode
  as a Tier 0/1 check) and retirement (age out as noise) candidates.

  Not when: the finding has a failing script or counterexample — that is Tier 1
  evidence; attach the artifact and let it gate (see adversarial-claims-reviewer).
  Not when conducting the review itself — use code-review-and-quality for source
  code or skill-library-review for library definitions; this skill only stores
  their unevidenced residue.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Findings Ledger

Stochastic judgment proposes; deterministic verification disposes (tier
doctrine: review-tiers — `.claude/rules/review-tiers.md`). This skill is the *proposes* side's
inbox: a single append-only JSONL at `.claude/ledger/findings.jsonl` where
Tier 2 findings accumulate fingerprinted, so the same defect phrased two ways
across runs usually collides to one entry (a heuristic — see the limits doc)
and recurrence across independent runs — not rhetoric — decides what gets
investigated.

## The ledger file

- **Location:** `.claude/ledger/findings.jsonl`, one JSON event per line.
- **Append-only.** Status transitions are new events for the same fingerprint;
  prior lines are never mutated. Current status = the fingerprint's most recent
  event.
- **Gitignored by default** (machine-local noise). **Team-shared mode:** in
  `.gitignore`, replace the `.claude/ledger/` line with `.claude/ledger/*.lock`
  (the lock sidecar stays local) and commit the findings file so recurrence is
  measured across the whole team's runs. Append-only + stable ordering keeps
  the diffs reviewable.
- **CI runners don't persist it.** Appends made during a CI job vanish with
  the runner — and CI must never push the ledger back to the repo. Upload the
  run's findings as a build artifact and harvest locally instead; patterns in
  [references/ledger-format.md](references/ledger-format.md).

Entry fields: `fingerprint`, `file`, `claim`, `tier`, `source`, `run_id`,
`date`, `evidence` (path or null), `status`
(`NEW | RECURRING | INVESTIGATING | PROMOTED | RETIRED-NOISE`).
Full schema, lifecycle, and fingerprint-normalization limits:
[references/ledger-format.md](references/ledger-format.md).

## Commands

All via [scripts/ledger.py](scripts/ledger.py) (python3, stdlib only; exit 0 =
ok, 2 = setup/usage error; output ordering is deterministic). Resolve the script path first — [references/install-paths.md](references/install-paths.md):

```sh
PROJ="${CLAUDE_PROJECT_DIR:-.}"
# 1. Repo checkout
LEDGER="$PROJ/.claude/skills/findings-ledger/scripts/ledger.py"
# 2. Project Codex install
[ -f "$LEDGER" ] || LEDGER="$PROJ/.agents/skills/findings-ledger/scripts/ledger.py"
# 3. Global Claude Code install
[ -f "$LEDGER" ] || LEDGER="$HOME/.claude/skills/findings-ledger/scripts/ledger.py"
# 4. Global Codex install
[ -f "$LEDGER" ] || LEDGER="$HOME/.agents/skills/findings-ledger/scripts/ledger.py"

python3 "$LEDGER" add \
  --file <path> --claim "<one sentence>" --tier 2 \
  --source <agent-name> --run-id <id> [--evidence <path>]

python3 "$LEDGER" tally
python3 "$LEDGER" triage [--threshold 2] [--age-days 14]
python3 "$LEDGER" promote <fingerprint> [--status INVESTIGATING] [--evidence <path>]
python3 "$LEDGER" retire <fingerprint>
```

- `add` computes the fingerprint (sha256 of file path + normalized claim text)
  and marks a repeat sighting `RECURRING`. A `--tier 1` finding without
  `--evidence` is demoted to tier 2 automatically — the tier rule, enforced.
- Recurrence counts **distinct run ids**, not raw sightings — an agent
  repeating itself within one run cannot cross the threshold alone.
- `triage` lists fingerprints at/over the recurrence threshold as promotion
  candidates, and still-`NEW` single-run findings older than the age cutoff
  as retire-as-noise candidates. The `/triage-findings` command (repo-local
  maintainer tooling; not shipped by the installer) wraps this and proposes a
  ratchet target per candidate; the human disposes.
- `promote` refuses to record `PROMOTED` without `--evidence` — a promotion
  *is* its encoded check.

## The ratchet

A recurring fingerprint is a candidate to leave the stochastic layer forever:
investigate → encode as a `scripts/validate.sh` rule (Tier 0) or an
exit-nonzero evidence script (Tier 1) → `promote` with the encoded check as
`--evidence` → no LLM ever re-litigates it. Singles nobody re-reports get
`retire`d. The ratchet only turns toward lower variance.

## Related skills

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — produces the findings this ledger stores
- [skill-library-review](../skill-library-review/SKILL.md) — library-audit findings route here when unevidenced
- [adversarial-claims-reviewer](../adversarial-claims-reviewer/SKILL.md) — the Tier 1 pattern: evidence artifacts instead of ledger entries
