---
name: fast-lean-proof-loop
description: "Shorten Lean 4 proof iteration with a warm editor session, dependency-aware reverse-import build plans, and lemma lookup that Lean itself confirms, while a separate full build plus axiom audit stays the promotion gate."
---

# Blitzdiät (fast-lean-proof-loop)

Use this skill while editing a Lean proof inside an already configured project. It reduces feedback latency without weakening the final acceptance gate.

## Keep the interactive loop warm

1. Open the authoritative project root in a Lean-aware editor and keep its language-server session alive across edits.
2. Change one theorem or dependency cluster at a time. Read the first load-bearing error before following cascades.
3. Search existing project and ArkLib sources before writing new infrastructure.
4. Verify every exact candidate name in one Lean process:

```bash
python3 scripts/lean_symbol_check.py \
  --project-root /absolute/path/to/project \
  --source-root ProximityPrize \
  --query 'encoder_injective|ProtocolClaim' \
  --import ProximityPrize.Benchmark.TargetLower \
  --name ProximityPrize.Benchmark.ProtocolClaim \
  --timeout-seconds 120 \
  --output /absolute/path/to/symbol-check.json
```

Text search produces candidates only. A name becomes verified only when the emitted `#check` batch exits successfully in the pinned project environment.
The helper kills its full process group and writes a `TIMEOUT` receipt if dependency hydration or elaboration exceeds the bound; a timeout verifies no name.

## Build only the affected reverse-import closure

Generate a plan from the files actually edited:

```bash
python3 scripts/lean_fast_loop.py plan \
  --project-root /absolute/path/to/project \
  --source-root ProximityPrize \
  --changed ProximityPrize/SubmissionLower/ChangedLemma.lean \
  --output /absolute/path/to/affected-plan.json
```

The plan parses local imports, computes every local module that depends on the changed files, and chooses the outermost affected roots as Lake targets. Inspect the plan, then run the same source-bound calculation:

```bash
python3 scripts/lean_fast_loop.py run \
  --project-root /absolute/path/to/project \
  --source-root ProximityPrize \
  --changed ProximityPrize/SubmissionLower/ChangedLemma.lean \
  --output /absolute/path/to/incremental-build.json
```

Use `--dry-run` to check target selection without compiling. If imports are generated, conditional, or outside the indexed source root, add the missing root explicitly to the final command and record why.

## RCI loop

1. **Inspect:** warm editor diagnostic, changed file, reverse-import plan, and verified symbol candidates.
2. **Critique:** identify the earliest failing dependency, stale import, guessed lemma name, or over-broad rebuild root.
3. **Improve:** make the smallest theorem, import, or target correction.
4. **Verify:** rerun the affected build and retain its source-manifest receipt.

Do not respond to a cascading error list with a broad refactor. Fix the earliest load-bearing error and recalculate the closure after every import change.

## Promotion gate

The fast loop is not the shipping receipt. Before promotion, follow [references/promotion-gate.md](references/promotion-gate.md) and `$lean-arklib-proofs`: rebuild the exact official target from the authoritative source, run the full repository build required by policy, run the axiom and placeholder audits, verify source size and imports, run the independent falsifier, and refresh the benchmark. Preserve both incremental and final receipts so speed does not obscure what was actually checked.
