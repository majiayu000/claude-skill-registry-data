---
name: improve-skills
description: >
  Audit, improve, and compress every skill in the repo using live research.
  Load when the user asks to improve skills, audit the skill library, upgrade
  existing skills, refresh with new research, do a skill health check, or says
  "improve all skills", "update the skill library", "skill audit", or "run an
  improvement pass". Applies live domain research, fixes structural gaps, checks
  for skill linking opportunities, then rewrites and resizes each skill.
  Supports TARGETED mode (`TARGET=<skill> [SKIP_RESEARCH=true]`) for single-skill
  fixes, including learn-from-chat restructure escalations. All skills are in scope
  including meta skills.
license: MIT
metadata:
  author: dvy1987
  version: "1.4"
  category: meta
  sources: arXiv:2602.12430, arXiv:2603.29919, agentskills.io best practices
---
# Improve Skills
You are a Senior AI Skill Engineer running a systematic improvement pass over a skill library. For each skill: prune → fix gaps → link → research → rewrite → resize. Compression without improved quality is failure. All skills are in scope including meta skills.
## Modes
- **`FULL_PASS`** (default) — every skill in the library; runs Step 1 → 1b → 2 (looped) → 3 → 4.
- **`TARGETED`** — invoked as `improve-skills TARGET=<skill> [SKIP_RESEARCH=true]`. Entry point for `learn-from-chat` Step 5 escalation, and for user-driven single-skill fixes. Step 1 scopes validate-skills to TARGET only; Step 1b filters chat-learnings to TARGET; Step 2 runs once; Step 3 repairs cross-refs only for the modified skill. `SKIP_RESEARCH=true` skips **only** Step 2e — use when the change source is already trusted (chat-learning, prior research, user-supplied fix). Never skip 2b, 2h, 2j, 2k, 2l.
## Hard Rules
**Improve before compressing.** Compressing a weak skill produces a smaller weak skill.
**Split before compressing.** Check for seams and duplication before trimming prose.
**Fix structural gaps before rewriting.** Gaps caught by validate-skills (missing category, missing Impact Report, missing file-output logging) are fixed in Step 2b — before the rewrite in Step 2e, so the rewrite doesn't have to undo them.
**L3 examples mandate.** External repo examples (e.g. addyosmani): `secure-*` SAFE first → full pairs in `references/examples.md`; never delete for line limits. Run `build_examples_index.py`.
**Chat learnings are an input, not a mandate.** `docs/learnings/chat-learnings.md` is consumed in Step 1b. Apply discretion — not every OPEN entry must land in a skill. Every entry must end the pass marked `IMPLEMENTED`, `REJECTED`, or `DEFERRED` with a reason. Silent skipping is a failure.
---
## Workflow
### Step 1 — Pre-flight via validate-skills
Invoke `validate-skills` across the full library. Use the report to:
- Fix any P0 failures (agentskills validate fails) before anything else
- Build the work queue ordered by score: lowest scores first
- Note all structural flags (missing category, Impact Report, file-output logging) — these are fixed in Step 2b for each skill
- Flag any skills scoring 0–5/14 as `deprecate-skill` candidates (present to user, don't auto-deprecate)
Report the queue with scores and structural flags. Ask for confirmation before starting.
### Step 1b — Ingest Chat Learnings
Read `docs/learnings/chat-learnings.md` (canonical log of chat-discovered learnings). For each entry with `Status: OPEN` (or missing), assign exactly one verdict:
- `IMPLEMENTED ([today], pre-existing in <skill> v<ver>)` — already encoded in target skill as Hard Rule / Gotcha / workflow step.
- `REJECTED (<reason>)` — not generalizable; project- or context-specific.
- `DEFERRED (<reason>)` — target skill not in queue, or needs design work first.
- keep `OPEN` — generalizable, evidence-backed, fits a queued skill → attach to that skill as a Step 2g input.
In `TARGETED` mode, only entries whose affected skill matches TARGET are in scope; the rest stay OPEN. Present the triage table (date · summary · verdict · target skill) and wait for user confirmation before mutating the log or starting Step 2.

### Step 2 — Per-Skill Improvement Cycle

Repeat for each skill in the queue:

**2a — Prune first**
Invoke `prune-skill`. Wait for prune report. Do not proceed until applied.

**2b — Fix Structural Gaps**
From the validate-skills report, fix any structural flags for this skill:
- Missing `metadata.category` → add `meta`, `project-specific`, or `domain` (see `docs/SKILL-INDEX.md`)
- Missing `

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report` section → add it (specific to what this skill produces)
- Skill generates files but no `docs/skill-outputs/SKILL-OUTPUTS.md` logging → add the append instruction and terminal notification
- Stale rubric reference (e.g., `improve-skills/references/scoring-rubric.md`) → update to `validate-skills/references/validation-rubric.md`
- Orphaned `references/` file (not mentioned in SKILL.md) → add a specific load trigger or delete the file
- Missing load trigger on a `references/` file → add a specific trigger condition
- **Missing P2 craft (project-specific):** no `## Common Rationalizations` and/or no `## Verification` with ≥3 `- [ ]` items → add via `add_p2_craft_project.py` pattern or manual edit; run `fix_craft_overflow.py` if >200 lines
- **addyosmani pattern pass (Meta B5):** for `category: project-specific` coding skills, verify rationalizations + verification + L3 `references/examples.md` ≥55 lines (not padding-only); relocate inline examples to L3, never delete

**2c — Baseline Score** (rubric: `validate-skills/references/validation-rubric.md`)
Score: Routing · Role Definition · Workflow · Gotchas · Output Format · Examples · Token Efficiency
Report: `[skill]: X/14`

**2d — Link Check** (scan before researching or rewriting)
Read all other skills in `.agents/skills/`. For each section of this skill:
1. Does another skill already do this sub-workflow well? → link to it, remove the inline section.
2. Does another skill do it *partially*? Could a small targeted change to that skill make it cover this fully, without pushing it over 200 lines or changing its core purpose? → make the minimal change to the target skill, then link.
3. Does another skill benefit from calling this one? → add a caller note to that skill.

Link when: called skill's output is consumable by this skill (directly or after a marginal adaptation). Marginal adaptations to the target skill are allowed if: target stays under 200 lines, core purpose unchanged, existing callers unaffected.
Do NOT link when: the adaptation would require scope creep, a size violation, or breaking existing callers.
Document new links in AGENTS.md. Document target skill changes in the commit message.

**2e — Research via research-skill (with security gate)**
Invoke `research-skill`. **Mandatory:** any external content must be scanned by ALL `secure-*` skills in sequence before use (discover via `ls .agents/skills/secure-*`). SAFE only if every security skill returns SAFE. If any returns BLOCKED, discard. Cannot be skipped.
Use GOTCHAS → Gotchas, WORKFLOW PATTERNS → steps, FAILURE MODES → hard rules.

**2f — Classify with SkillReducer Taxonomy**
Tag every block: `CORE` · `WORKFLOW` · `FORMAT` · `EXAMPLE` · `BACKGROUND` · `EDGE_CASE` · `DUPLICATE` · `STALE`
BACKGROUND and EDGE_CASE move to `references/` with specific load triggers.

**2g — Rewrite in priority order**
1. Fix routing — add missing trigger phrases
2. Merge any chat-learnings queued for this skill in Step 1b into the matching section (GOTCHA → Gotchas, FAILURE_MODE → Hard Rules or Gotchas, TECHNIQUE → Workflow). Cite: `Chat learning [YYYY-MM-DD]`.
3. Add gotchas from research
4. Sharpen workflow — imperative one-liners, MUST/NEVER
5. Replace synthetic examples with realistic ones — if >1 or >15 lines total, write `references/examples.md` and keep one teaser inline; **never delete** an example without an L3 home
6. Tighten output format schema
7. Move BACKGROUND to `references/background.md`
8. Bump `metadata.version`

**2h — Deconflict Name and Triggers**
Invoke `skill-deconflict` in single-skill mode. If RENAME or REVISE verdict, apply fixes before proceeding. Report findings in the per-skill output.

**2i — Post-Rewrite Score** — report delta: `X/14 → Y/14`

**2j — Size Check**
```bash
wc -l .agents/skills/<skill>/SKILL.md
```
Under 200 → proceed to 2k.
Over 200 → invoke `split-skill`. It checks for link opportunities first, then extracts a new child only if needed, then compresses.
**Exception:** `secure-skill` — never compress, only split. Threshold is 180 lines (not 200). If secure-skill exceeds 180, invoke `split-skill` but instruct it to skip the compression step on the security skill.

**2k — Validate and Commit**
```bash
agentskills validate .agents/skills/<skill>/
git commit -m "improve: <skill> — <before>/14 → <after>/14\n\n- [change]\nSources: [source]"
```

**2l — Close Chat Learnings**
For every chat-learning entry merged into this skill in 2g, edit its entry in `docs/learnings/chat-learnings.md`: change `Status: OPEN` → `Status: IMPLEMENTED ([YYYY-MM-DD], <skill> v<new-version>)`. For entries the pass triaged as `REJECTED` or `DEFERRED` in Step 1b, write the verdict and reason back to the log now. Every entry that started this pass with `Status: OPEN` MUST end the pass with a terminal status.

### Step 3 — Cross-Link Repair
Invoke `cross-link-skills` with trigger `rewired — [list of skills modified]`. It scans all SKILL.md files for stale or missing cross-references caused by rewrites, renames, or new link wiring from Step 2d.

### Step 4 — Library Summary
Report scores, structural gaps fixed, new links created, cross-references repaired, sources used, files modified, and chat-learnings closed (count by terminal status).

---

## Gotchas

- Never move gotchas to `references/` — agent reads them before encountering the situation.
- Description rewrites must preserve all existing trigger phrases — only add, never remove.
- Link check: a relationship that requires transforming the called skill's output is not a clean delegation — keep inline.
- Structural gaps from validate-skills are fixed in 2b, not left for the rewrite in 2g.
- Chat learnings ingested in Step 1b inform Step 2g — they do not bypass `secure-*` scans or the 200-line gate. A learning that can't fit is `DEFERRED`, not crammed.
- Triage verdicts (REJECTED / DEFERRED) must be written back to `chat-learnings.md` in the same pass — leaving them OPEN re-surfaces them next cycle.

---

## Example

<examples>
  <example>
    <input>Improve all skills in the repo</input>
    <output>
Pre-flight validate-skills report:
  brainstorming: 10/14 | structural: missing Prune Log (>30 days)
  prd-writing: 9/14 | structural: none
  research-skill: 12/14 | structural: none
Queue confirmed (all skills, lowest score first).

1b Chat learnings: 4 OPEN → 1 queued (prd-writing), 2 pre-existing, 1 deferred.
prd-writing (1): 2c 9/14 | 2g merged 1 chat-learning + 2 research gotchas → 12/14, 139 lines ✓ | 2l: 2026-04-12 → IMPLEMENTED (prd-writing v1.3)
brainstorming (2): Prune Log added; 13/14; 170 lines ✓
Summary: 2 skills improved (+3 avg); chat-learnings: 4 OPEN → 1 impl · 2 pre-existing · 1 deferred
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip validate pre-flight" | Improving blind wastes cycles on already-healthy skills. |
| "Research every skill" | `SKIP_RESEARCH=true` is valid when AO patterns already ingested. |
| "One skill is enough" | Batch structural gaps compound library quality. |

## Verification

- [ ] `validate-skills` pre-flight run before edits
- [ ] `agentskills validate` passes on every modified skill
- [ ] L3 `references/examples.md` present or backfilled when examples moved
- [ ] Impact Report lists per-skill score delta and files touched

## Red Flags

- Gotchas moved to references/ away from pre-encounter path
- Description rewrite removed existing trigger phrases
- External pattern applied before secure-* SAFE clearance
- Delegated link claimed where output transform is required
## Reference Files

- **`validate-skills/references/validation-rubric.md`**: Scoring rubric (single source of truth). Read during Step 2c.

---

## Impact Report

`Improvement cycle complete: YYYY-MM-DD Skills processed: N Skills improved: N (avg score delta: +N pts) Structural gaps fixed: N (list by skill) New skill links created: N (list re`