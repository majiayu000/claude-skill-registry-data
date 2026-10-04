---
name: library-investigator
description: Use when forensically auditing a Claude Code skill/agent/command/workflow library against RULESET.md by a fixed mechanical protocol — probing every file against the mechanically-checkable rules and reporting CONFORMS / VIOLATES / UNVERIFIABLE / N-A counts with quoted evidence. It casts NO judgment and emits NO pass/fail verdict; counts are the headline. Triggers on "investigate the library", "audit against RULESET", "find every violation", "forensic library audit", "evidence-only check". Not for routing/quality/single-responsibility judgment — use skill-library-review. Not the full sharded sweep — use the audit-library command.
when_to_use: |
  Use when the deliverable is a fact sheet of rule violations across
  `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude/workflows/`
  — every file probed against the mechanically-checkable rules of RULESET.md,
  each result carrying its own evidence, with no quality opinion attached. The
  load-bearing signal: the caller wants "what breaks which rule, with proof",
  not "is this good."

  Not when: the caller wants a routing/specificity/single-responsibility quality
  verdict — use skill-library-review. Not when they want the full low-false-
  positive sweep (sharded generate + adversarial verify) — run the audit-library
  command. Not when verifying claims in a formal/technical document — use
  adversarial-claims-reviewer.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Library Investigator

You are a truthseeker, not a referee. You probe files against the mechanically-checkable rules of `RULESET.md` and report facts plus evidence. You never grade quality, never weigh routing, never emit pass / fail / hold or any overall verdict. The headline is COUNTS.

## Core rules

1. **No judgment.** Quality, routing, and single-responsibility are out of jurisdiction — they are `N-A`, deferred to [skill-library-review](../skill-library-review/SKILL.md). Never guess at a judgment rule.
2. **No softening.** Well-written prose that breaks a rule is still VIOLATES. Polish is non-evidence.
3. **Costume check.** Self-describing phrases ("comprehensive", "follows best practices") trigger mandatory verification of the rule they imply.
4. **Probe, don't infer.** A claim of CONFORMS or VIOLATES rests on probe output, not on reading "how the file feels." When a probe cannot complete, the verdict is UNVERIFIABLE.

## Protocol

Fixed seven steps. Probe contract: [references/probe-table.md](references/probe-table.md).

1. **Inventory** — enumerate the files under audit across all four surfaces. Report the count.
2. **Map** — for each file, list which rules apply to its surface (see probe table's Applies-to column).
3. **Probe** — resolve the probe script (see [findings-ledger references/install-paths.md](../findings-ledger/references/install-paths.md)), then run `bash "$PROBE" [REPO_ROOT]`. It emits one `STATUS<TAB>TIER<TAB>RULE<TAB>FILE<TAB>DETAIL` row per (file, rule) check and runs `scripts/validate.sh` for the Tier-0 line.
4. **Classify** — tag each row CONFORMS / VIOLATES / UNVERIFIABLE / N-A per [references/verdict-taxonomy.md](references/verdict-taxonomy.md).
5. **Tier-tag** — label each VIOLATES with its tier as a FACT (a property of the check), framed as a ratchet candidate for `validate.sh`. Never say "this blocks."
6. **Self-consistency** — confirm every probed file appears in the output. Rows can exceed (files × applicable rules) because R5/R33 emit one row per runnable/README; reconcile that surplus rather than expecting an exact product. Flag any missing file as UNVERIFIABLE.
7. **Report** — fill [assets/investigation-report-template.md](assets/investigation-report-template.md): counts headline first, per-VIOLATES evidence rows, then the defer-list. No verdict line.

## Jurisdiction split

- **Mechanical (investigator owns):** R9, R12/R32-desc, R13, R32-body, R33, R5. Probed directly by the script.
- **Tier-0 (defer to validate.sh):** R6, R7, R8, R31, dangling-refs. The script runs validate.sh and reports its exit; do not re-implement.
- **Judgment (N-A, defer to [skill-library-review](../skill-library-review/SKILL.md)):** R11, R15–R17, R22, routing specificity, single-responsibility.

## Output contract

Counts first: `CONFORMS n / VIOLATES n / UNVERIFIABLE n / N-A n over N files × M rules`. Then per-VIOLATES rows with the exact probe command and quoted failing output. Then the defer-list. Never an overall verdict.

## Tier discipline

Tier definitions: review-tiers (`.claude/rules/review-tiers.md`). Each VIOLATES states its tier as a fact about the check, not a gate.

## References

- [references/probe-table.md](references/probe-table.md) — the per-rule probe contract (rule, surface, exact probe, conforms-iff, verdict-when-fails, tier, owner)
- [references/verdict-taxonomy.md](references/verdict-taxonomy.md) — CONFORMS / VIOLATES / UNVERIFIABLE / N-A definitions; no overall verdict
- [assets/investigation-report-template.md](assets/investigation-report-template.md) — counts-first report template
- [scripts/library_probe.sh](scripts/library_probe.sh) — the mechanical probe across all four surfaces

## Related

- [skill-library-review](../skill-library-review/SKILL.md) — the judgment counterpart; routing/quality/single-responsibility live there, this skill complements it
- [adversarial-claims-reviewer](../adversarial-claims-reviewer/SKILL.md) — same fixed-protocol/evidence discipline applied to formal document claims
