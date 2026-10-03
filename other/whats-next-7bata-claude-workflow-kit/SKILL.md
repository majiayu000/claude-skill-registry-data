---
name: whats-next
description: Determine and report what to do next for a /scaffold project. Triggers when the user says "what's next / what do I do now / whats next / where am I", and the project root has docs/PLAN.md.
allowed-tools: Read, Glob, Grep
---

# /whats-next

Read the plan and progress docs laid down by /scaffold, and tell the user what to do next. **Respond in English by default** (keep technical identifiers in English).

**The docs are the only source of truth.** Don't walk the codebase to answer this question; only spot-check code when the docs contradict each other and need cross-checking.

## Step 1: Read the progress files

1. `docs/PLAN.md` — Overall Roadmap, each Phase's status (title with ✅ = done), Spec Index
2. `docs/Progress.md` — the top-half "## Progress Overview" module status table (pending/doing/done) + the bottom-half changelog ("## Changelog", **newest first**, read the 2-3 most recent entries); older months are archived in `docs/archive/Progress-YYYY-MM.md` — only read those when tracing history
3. The latest design spec — the latest `docs/superpowers/specs/<date>-<topic>-design.md` pointed to by the Spec Index (if the index doesn't have it, Glob that directory and take the newest by date) — cross-check against Progress.md to judge whether it's already implemented
4. `docs/DECISIONS.md` — **newest first**, read the 2-3 most recent entries: any decision in the same domain as the next step must go into "Watch-outs"
5. `docs/MEETINGS.md` — only look at the **latest section**'s "Action Items": entries that are unchecked and don't appear in any plan go into part 4 of the output
6. `docs/REQUIREMENTS.md`'s "Goal Ledger" — entries with status `open`, listed one by one in part 5 of the output

ARCHITECTURE.md / DEPLOYMENT.md are design and deployment docs, not progress — don't read them; REQUIREMENTS.md's "Phased Roadmap" is only read when step 2's third row matches; its "Goal Ledger" is always read per item 6 above.

## Step 2: Locate the next step (check in order, stop at the first match)

| State | Next step |
|---|---|
| The latest spec is not yet implemented (Progress has no matching implementation record) | Use ultracode (Workflow multi-agent orchestration) to implement directly from that spec, unless Progress or the spec records that the user called a halt — in that case ask first |
| All specs are implemented (or there isn't one yet), and PLAN.md still has a Phase not marked ✅ | Run superpowers:brainstorming for the next Phase to produce a design spec (write it to `docs/superpowers/specs/`), then go straight to ultracode implementation once the spec is written — skip writing-plans; register the spec in the Spec Index |
| PLAN.md's Overall Roadmap is still `<!-- TBD -->` | First read REQUIREMENTS.md's "Phased Roadmap" as input, then use superpowers:brainstorming to define the phased roadmap |
| All Phases are ✅ | The project is complete per plan; suggest a retrospective or starting a new Phase |

## Step 3: Output contract (five parts, in order)

1. **Where you are** — one or two sentences: what was most recently completed, citing the date of Progress's latest entry
2. **Next step** — task name + the first concrete action (down to the file/command level) + source (which file, which section)
3. **Watch-outs** — decisions already made / pitfalls relevant to the next step, sourced from: DECISIONS.md's most recent entries + the Progress changelog, with citations; if this batch touched UI and Progress has no ui-sweep record, note here that a follow-up interaction regression scan is recommended (omit and don't push if not applicable); omit this section if none
4. **Meeting action items not yet in any plan** — unchecked action items from MEETINGS.md's latest section that haven't made it into any plan, prompting the user to decide where they go; items already logged in the Goal Ledger are not repeated here; omit this section if none
5. **Unsettled goals** — entries in REQUIREMENTS.md's Goal Ledger with status `open`, listed one by one, with any pinned to the top if they've been outstanding for more than 7 days; only list Goal Ledger entries; omit this section if none

End by asking the user: start now?

## Edge cases

- `docs/PLAN.md` or `docs/Progress.md` doesn't exist → this isn't a /scaffold project. State which file is missing, suggest running `/scaffold` first, and don't guess the next step
- Progress (overview table or changelog) contradicts the spec's implementation status (says done but no implementation record, or vice versa) → explicitly point out the contradiction and both sides' sources, suggest cross-checking before proceeding, don't silently pick one
- DECISIONS.md or MEETINGS.md doesn't exist → don't error, just skip the corresponding step (older projects may not have them)
- REQUIREMENTS.md doesn't exist, or has no Goal Ledger section → skip part 5, don't error (common for existing/legacy projects)
