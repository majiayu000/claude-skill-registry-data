---
name: emperor-require-design
description: >-
  Emperor Time — REQUIRE + DESIGN. Grill intent Socratically, write acceptance
  criteria and a fat work order a zero-context worker can execute. Use when
  planning, writing a spec, designing an approach, brainstorming, or before any
  implementation. Pairs with G1/G2.
license: MIT
metadata:
  version: 0.4.127
  chain: judgment-chain
---

# Emperor Require-Design (G1/G2 wrapper)

## MUST — grill checklist first

Before any implementation action (product code, scaffolding, product deps, or
BUILD), open `skills/emperor-require-design/grill-checklist.md`
(Chain Jail leaf from Superpowers `brainstorming` → **HARD-GATE** only)
and/or run `scripts/emperor grill` (prints the mechanical GRILL / STEP / MUST card).

No jumping to impl without Step 5 design approval. Do not load whole
`brainstorming`; ET + require-design orchestrate.

## Steps

1. Run `scripts/emperor grill` → quote `GRILL checklist=yes`. Advance steps
   with `scripts/emperor grill --advance N N+1` (skips fail). Jumping to code
   → `scripts/emperor grill --reject-impl` (HARD-GATE exit 1). Path taxonomy:
   record `Path: spike|bounded|architectural` + `Stage approval: …`; validate
   with `scripts/emperor grill --check-path <task-dir>` (fails on missing path,
   stage skip, or impl before approval). Always-fail helpers:
   `--reject-no-path` / `--reject-stage-skip` / `--reject-impl-before-approval`.
2. Confirm G0/G1 exist. If not, load `skills/emperor-scope/SKILL.md` first.
3. Read `references/work-order.md` then copy `templates/work-order.md` to
   `.emperor/tasks/<id>/work-order.md` (architectural path; bounded may stay
   in-chat per grill leaf).
4. Every non-trivial task step must include: real paths, exact commands,
   `Expected: FAIL` then `Expected: PASS` strings. No TBD.
5. Fill the Plan header: Goal, Architecture, Tech Stack, Spec,
   Global Constraints, Review Focus (or `none (checked)`). Leaf from
   obra/superpowers writing-plans Plan Document Header — not the whole skill.
6. Rejected alternative is mandatory (one line).
7. Run `scripts/gate.sh g2 <task-dir>` (calls `scripts/lib/work_order.py`)
   and quote the tail before BUILD.
8. Judgment on the design (does the work order match G1?) uses
   `chains/judgment-chain/SKILL.md` → `gatekeeping.md` only.
