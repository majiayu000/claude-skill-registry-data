---
name: hoa-skill-set-audit
description: >-
  Use when asked to audit, prune or consolidate the whole set of skills a session is offered,
  across plugin, hub, project and repo sources. Finds overlapping or contradictory skills,
  shadowing, same-name drift, visibility mistakes, broken ../ closure and listing-budget
  truncation, ranks fixes and gives necessity verdicts. Not for reviewing one skill
  (hoa-skill-review), provenance or upstream freshness
  (hoa-skill-curate), reviewing one repo's practices (the explicit hoa-repo-reckoning shortcut),
  or editing skills.
disable-model-invocation: true
metadata:
  revision: "6"
  areas: "software-development,self-management"
  targets: "runtime-agnostic"
  summary: "audit the whole offered skill set: per-skill quality, overlap, shadowing, contradictions, same-name drift, visibility, ../ closure, listing budget; report-only"
  summary_zh: "审计会话实际提供的整套技能：单项质量、重叠、遮蔽、指令冲突、同名漂移、可见性、../ 闭包、清单预算；只出报告"
  kind: "entry"
---

# Skill Set Audit

Audits the set the model is actually offered in this session — every source at once — not one
skill. The unit of harm is the set: two good skills with one trigger, a stale copy that wins the
bare name, a hidden child a parent can no longer reach.

## Gates

- **Report-only.** Do not edit, hide, disable, move, install or delete anything. A change needs an
  owner confirmation that names each skill and action; carry it out through
  hoa-skill-curate's execution procedure. Hidden is a selection decision, not authorization.
- **The listing is truth for "offered"; disk is truth for content.** Never reconstruct the offered
  set from disk or memory, and never judge a skill's content from its listing line.
- **Every finding cites evidence**: a listing line, an `inventory.json` field, or `file:line`.
  Zero usage is evidence, not proof of low value; an unclear owner scenario is `needs confirmation`.
- **A/B probes require owner authorization for the cost.**
- Re-read this file after compaction before continuing the passes.

## Configuration and references

Set roots with repeatable `--host NAME` (claude, codex, pi, omp, opencode, dsh)
and/or `--root DIR` (any additional root, including those named in host config).
If neither flag is given, `SKILL_SET_AUDIT_ROOTS` supplies roots separated by the
OS path separator (unset by default). `--project DIR` defaults to the current
working directory for project-level roots. `CLAUDE_CONFIG_DIR` and `CODEX_HOME`
default to `.claude` and `.codex` under the OS home directory.

| When to read | Reference |
|---|---|
| When resolving host roots, precedence, visibility controls, shadowing, or listing budgets | [Host behavior](references/hosts.md) |
| Only when assessing overlap, visibility, pruning, or necessity in the set pass | [Set judgment](references/set-judgment.md) |
| Only if a script command fails (for example `uv` is not found) | [Troubleshooting](references/troubleshooting.md) |

## Procedure

For recommendations based on recent work, use `hoa-skill-curate`.

1. **Capture the offered set.** Copy the host's skill listing from this session's context
   verbatim into a scratch file outside the repo, one `- name: description` line per entry.
   Keep entries that show no description — they are truncation evidence. If the host shows no
   listing, say so, audit disk only, and mark every offered-set claim unverified.
2. **Enumerate disk.** Pass every host in
   play in one run, so `duplicates.by_name` compares copies across hosts:
   `uv run scripts/inventory.py --host <host> [--host <host> ...] [--root DIR ...] --offered <listing> > <scratch>/inventory.json`.
   Exit 1 means findings exist — the normal case; 2 means no usable root or listing.
   `offered.not_on_disk` holds namespaced plugin entries (`plugin:name`, expected: plugin skills
   come from the listing) and built-ins; for any other entry, add the missing root.
   `offered-twice` marks one bare name offered more than once (e.g. a plugin skill plus a disk copy).
3. **Per-skill pass** (inventory `findings` plus reading). Trigger clarity: the first sentence
   says when to use, the description names an anti-trigger and no workflow steps. Length vs the
   caps of the hosts in play (`description-over-cap` applies the DSH cap only with `--host dsh` or
   an unlabeled `--root`; `listing-entry-over-cap`). Frontmatter validity and hidden-key form.
   Broken references (`broken-link`). Oversized bodies (`body-over-limit`). Bundled files the body
   never names (`unreferenced-file`) — a missing "Additional resources" list means the model does
   not know they exist.
4. **Set pass.** Apply the set-level catalog to visible skills first, then hidden ones.
5. **Pruning and consolidation.** Assess each skill named in a set finding (or
   every skill for a full prune) on usage, overlap, core value, quality, and
   necessity. Protocol duplicated across a skill family: read
   [skill family integrity](../hoa-skill-create/references/skill-family-integrity.md)
   and follow it. If missing, report that it belongs in the same host root.
6. **Verify adversarially.** Give an independent reviewer the claims, their evidence anchors and
   scope, not the finder's reasoning. Re-read the evidence or rerun the probe, try to refute each
   claim, and record what was checked and a `confirmed`, `weakened` or `refuted` verdict. Drop
   refutations and narrow weakened claims. Personally re-check the evidence for high-impact fixes
   and proposed deletions. If fresh context is unavailable, perform a separate verification pass
   and label it `single-context`; do not present missing evidence as verified.
7. **Report** and stop.

## Report

Lead with counts (offered, on disk, visible, hidden, per root) and the highest-confidence take.
Then findings ranked by harm — wrong skill selected or unreachable first, drift and budget next,
hygiene last — each with evidence and one concrete fix: `merge`, `narrow description`, `hide`,
`retire`, `move to always-on index`, `retain`, or `needs confirmation`. A deletion or merge
proposal states the replacement or the scope reason. Include the necessity verdicts with evidence
and the verification mode. For more than ~20 rows, write the full table
as CSV/JSON in the scratch directory and link it; never let a large inventory hide the decision.
End with what was not verified and an explicit statement that nothing was changed.

## Pitfalls

- **Reconcile current listing and disk before declaring totals.** Platform gates, disabled
  settings, and malformed metadata make them differ. A stale inventory is not runtime truth.
- **Ignore `node_modules` phantom skills.** The inventory and host loaders skip them.
- **Lexical similarity only nominates pairs.** Low scores can compete; high scores can complement.
- **Do not patch user-owned, bundled, hub-installed, external, or pinned skills.** Report the boundary and recommend adoption or owner action.
- On channels that render tables poorly, attach CSV/JSON and give readable rows.

## Tools

- [scripts/inventory.py](scripts/inventory.py) — read-only root scanner; `--help`
  lists flags, JSON fields, and exit codes.
- [scripts/test_inventory.py](scripts/test_inventory.py) — tests on synthetic skill trees.
