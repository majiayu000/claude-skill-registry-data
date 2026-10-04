---
name: kaggle-playground-ops
description: Use when starting, operating, auditing, or finalizing a Kaggle Playground tabular competition involving OOF/CV, public notebooks or prediction assets, leaderboard probing, submission diffs, Public/Private split risk, or final submission selection.
---

# Kaggle Playground Ops

Run the competition as three separate evidence tracks: stable OOF modeling, controlled Public exploration, and explicit final selection. Optimize expected Private rank without discarding useful Public information.

## Start or Take Over

1. Read the competition rules, metric, split, deadline, submission quota, and final-selection count.
2. Read any existing `HANDOFF.md`, experiment ledger, scripts, scores, and submissions before proposing work.
3. Copy `assets/HANDOFF.template.md` and `assets/experiment_ledger.template.csv` when either artifact is absent.
4. Record every candidate's lineage and file hash. Run `scripts/fingerprint_assets.py` on downloaded public assets.
5. Load `references/playbook.md` for the detailed operating rules.

## Operate the Three Tracks

### Stable OOF track

- Preserve row-level OOF probabilities, fold IDs, class order, and test probabilities.
- Audit alignment and probability validity with `scripts/oof_audit.py`.
- Use nested validation for blend weights, class biases, thresholds, and candidate-selection rules.
- Keep candidates only when gains are fold-stable, class-safe, and meaningfully different.

### Public exploration track

- Download real notebook outputs; never trust titles or claimed scores alone.
- Fingerprint and deduplicate assets before treating them as independent evidence.
- Compare submissions with `scripts/submission_diff.py`.
- Grade evidence A/B/C as defined in the playbook. Spend submissions on one-variable tests with a written hypothesis.
- Store directly validated Public-only row patches separately. Never treat them as Private evidence.

### Final selection track

- Choose one Public-attack candidate and one independently trained OOF hedge when two slots are available.
- Do not spend both slots on files differing only by validated Public rows; their Private predictions are equivalent under a disjoint split.
- Resolve close hedge choices using nested OOF, fold stability, per-class recall, and prediction diversity—in that order.

## Stop Rules

- Do not tune and report on the same OOF labels.
- Do not submit an unlogged multi-variable change.
- Do not infer independence from different notebook names; compare file fingerprints.
- Do not let leaderboard feedback overwrite the stable-model evidence stream.
- Before deadline, stop low-evidence row guessing and verify exact final file IDs, hashes, and roles.

After Private reveal, complete the postmortem table in the playbook and separate method errors, deliberate risk choices, and outcome variance.
