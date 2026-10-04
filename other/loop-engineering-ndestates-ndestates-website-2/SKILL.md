---
name: loop-engineering
description: >
  Loop engineering for this template: design systems that prompt agents, not hand prompts.
  Cache is king — all loops are cache-first. Assess maturity, pick next pattern, run loop-audit.
  See LOOP.md, patterns/, and loop-budget.md.
argument-hint: "e.g. 'assess readiness', 'add PR babysitter loop', 'explain L1 vs L2'"
user-invocable: true
disable-model-invocation: false
---

# Loop Engineering (orchestrator template)

**Principle:** You design loops; agents execute inside them. **Cache is king:** every loop starts with manifest + lean cache — never source-first.

## Stack in this repo

| Layer | Files |
|-------|-------|
| Registry | `LOOP.md`, `patterns/registry.yaml` |
| Memory | `STATE.md`, `loop-run-log.md` |
| Budget | `loop-budget.md`, `token_policy` in manifest |
| Skills | `loop-triage`, `loop-verifier`, `chain`, `cache-efficient`, `load-project-cache-first` |
| Schedule | `.github/workflows/loop-daily-triage.yml` |
| Audit | `scripts/loop-audit.sh` |

## Maturity (14-step shorthand)

1–4 Unlock: loop vs prompt; cache + STATE as spine  
5–9 Primitives: `/goal` conditions, verifier, worktrees, schedule  
10–14 Compound: lessons → skills; eval gates; safety boundaries  

This template ships at **L1 daily-triage** (steps 5–6 + cache).

## Start here

1. `.github/prompts/load-project-cache-first.prompt.md` or `.github/skills/cache-efficient/SKILL.md`
2. `bash scripts/loop-audit.sh`
3. `.github/skills/loop-triage/SKILL.md` → `.github/skills/loop-verifier/SKILL.md`
4. Read `patterns/daily-triage.md` before adding loops

## Adding loops

- Register in `LOOP.md` + `patterns/registry.yaml`
- Set `cache_files_required` and `max_source_files`
- Default **L1** until `loop_policy.allow_l2: true` with human approval

## Related

- On-demand skill chains: `CHAIN.md`, `.github/skills/chain/SKILL.md` (shared cache, minimal handoffs)
- Token mode: `.github/skills/cache-efficient/SKILL.md`