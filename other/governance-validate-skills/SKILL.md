---
name: governance-validate-skills
description: >
  Validate the AI-SDLC skills under .claude/skills/ with the layered eval harness before relying
  on a new or changed one. Use when a skill has just been added or edited and needs checking, or
  when the user says "eval the skills", "validate this skill", "run the skill harness", "test the
  skills", "did my skill change break routing", or "check skill discriminability". This is the
  durable form of the "draft-only eval harness" the roadmap refers to. Do NOT use to validate the
  artifact graph or docs wiki (that is governance-check-graph), or to author or edit a skill's
  content.
---

# Validate Skills

Usable by **any** persona, typically Lead or Architect. Invoked as `/governance-validate-skills`.

A skill change is not done until it is validated. This is the sibling of `governance-check-graph`:
that gate validates artifacts and docs; this one validates the **skills themselves** - their
structure, how they route, and whether they add value over a competent baseline. It is
description-level and behavioural validation, not adoption.

Run it for any skill you add or change, and re-run the routing layer for the whole set when you
touch a description (routing is a shared space: one skill's triggers can collide with another's).

## The layers

| Layer | Question | Nature | How |
|---|---|---|---|
| 0 - static | Is every skill structurally sound and house-style clean? | deterministic | `MindNova/toolsCheck-SkillHygiene.ps1` |
| 1 - routing | Does each skill win its niche and avoid over-triggering? | subagent panel | independent routing judges over a prompt set |
| 2 - value | Does the skill beat a no-skill baseline on a real task? | subagent + blind judge | with-skill vs baseline, scored blind |
| 4 - cross-tool | Does the same SKILL.md trigger in Copilot CLI? | manual, off-Claude | cannot be driven from a Claude session; note as pending |

There is no Layer 3 here; the number is kept aligned with the roadmap's L0-L4 maturity language.

## Layer 0 - static (run first)

```powershell
MindNova/toolsCheck-SkillHygiene.ps1
```

Exits non-zero and names the offending skill and rule on any violation (name=folder, trigger-rich
description, persona line, Next-steps section, no em-dash, no line-citations, cross-refs resolve).
Fix and re-run until green before spending subagent budget on Layers 1-2.

To run this gate together with every other CA gate the pipeline runs (docs, code, story-traits,
plus the gate self-tests), use the local aggregator: `MindNova/toolsInvoke-LocalGates.ps1`
(add `-IncludeToolTests` to also run the Pester tests). It prints one pass/fail summary and exits
non-zero if any blocking gate fails, so it works as a pre-push check.

## Layer 1 - routing discriminability

Confirms each skill is the best pick for its own prompts and is NOT chosen for adjacent ones.

1. **Build the routing corpus** (what a routing agent actually sees - names + descriptions):
   ```powershell
   Get-ChildItem .claude/skills -Directory | Sort-Object Name | ForEach-Object {
     $d = Get-Content (Join-Path $_.FullName 'SKILL.md') -Raw
     if ($d -match '(?ms)^description:\s*>?\s*(.+?)\r?\n---') { "### $($_.Name)`n$($matches[1].Trim())`n" }
   }
   ```
2. **Write a prompt set** spanning three styles: straightforward (the skill's own trigger phrasing),
   paraphrased (same intent, different words), and adversarial keyword-bait (a prompt that contains
   the skill's keywords but whose true intent is a sibling skill - e.g. "we shipped X, create a
   story" baits enrich-ticket but must route to elaboration-upsert-user-story). Cover the changed
   skill's niche prompts AND its boundaries with each neighbour.
3. **Dispatch independent routing judges** (3 is a good default) as subagents. Each gets the corpus
   and the prompts and picks the single best skill (or "none") per prompt from descriptions only.
4. **Score:** the skill should win every one of its niche prompts and be rejected on every bait
   prompt; a tie/loss on a bait prompt is an over-trigger to fix (tighten the description or add an
   explicit "Do NOT use" exclusion), then re-run.

## Layer 2 - value vs baseline

Confirms the skill earns its place against a capable agent that does not have it.

1. **Run two agents on the same representative task** (use a DRY RUN - report the plan, no live
   writes): one **with-skill** (reads the SKILL.md), one **baseline** (no skill, but given the repo
   conventions a real agent would have).
2. **Judge blind:** a third subagent scores both plans against a rubric without being told which is
   which. Default rubric items (score 0-2 each): does it follow the skill's core discipline; does it
   avoid the failure the skill prevents; is the output complete and correct; does it respect the
   relevant gate or confirmation. Adapt the rubric to the skill under test.
3. **Read the result honestly:** skills win when they enforce a discipline the baseline drops; they
   tie when that discipline has moved into a gate. A tie is a signal the durable value now lives in
   the gate, not the prompt.

## Caveats (state them with results)

n is small (1 to 3 tasks, often 1 judge) - signal, not proof. Eval subagents may not inherit the
always-on `AGENTS.md` context a real session has, so baselines are slightly understated on always-on
rules. Layer 4 (Copilot cross-tool) is not runnable from a Claude session.

## Guardrails

- **Dry-run only.** Eval scenarios never perform live writes (no work item mutations, no PR, no file mutation in the
  product). The agents report what they would do; a live write needs its own confirmation gate.
- **Record the outcome** in the Validation status section of `docs/ai-sdlc/roadmap.md`, dated, with
  the per-layer result and the caveats. The roadmap is the durable record; chat threads are not.
- Pairs with `governance-check-graph` (artifact/doc integrity) and `governance-constitution`
  (the non-negotiables a skill must respect).

## Next steps

- `/governance-check-graph` (Lead) - validate artifact and doc-link integrity alongside skill hygiene.
- If a routing or value finding requires changing a skill, edit it, then re-run this harness before relying on it.
