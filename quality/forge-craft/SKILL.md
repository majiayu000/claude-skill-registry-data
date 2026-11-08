---
name: forge-craft
description: "Use before calling work done: what would its user notice?"
when_to_use: "Triggers: klaar, af, opleveren, ziet er niet uit, design, details, review, polish, sloppy."
# W2-BUDGET original description (listing budget): in git history (4 KB file cap)
---

# forge-craft — the craft lens

Owner rule (Intelligence bar): before "done", ask who will look at this or work with it, and what they
would notice. Sloppy output is a defect, not a style: fix it, or say plainly what is still weak.

## When to run
- Before any deliverable is called done, handed over or shown to the owner: pages, copy, code,
  workflows, documents, spreadsheets, reports, games, CLIs, APIs, voice or chat agents.
- By the Boss that judges it: Verify Boss (next to the domain gate), Review Boss (stakeholder pass
  before sign-off), UI Boss (self-check before handing over). A builder may run it on its own work
  first; that never replaces the independent pass.

## Commands
```bash
node .claude/forge-bin/forge-craft.cjs lens --list                    # the lenses and their check counts
node .claude/forge-bin/forge-craft.cjs lens --type web-ui              # stakeholders, first ten seconds, checks, sloppy defects
node .claude/forge-bin/forge-craft.cjs plan --deliverables "web-ui,copy-and-content"   # combined plan for a mission
node .claude/forge-bin/forge-craft.cjs plan --domain website --text "<request>"  # domain lenses + what it names
node .claude/forge-bin/forge-craft.cjs review-template --type web-ui   # the self-critique form to fill
node .claude/forge-bin/forge-craft.cjs record --run <id> --type web-ui --file review.json  # filled form -> run evidence
node .claude/forge-bin/forge-craft.cjs check --run <id>                # recorded reviews still valid?
node .claude/forge-bin/forge-craft.cjs validate                        # schema + citations of every lens
```
Add `--json` for machine output. An unknown type gets its closest lenses plus `generic`, and says so.
Without Bash (Review Boss), Read the lens file itself: `.claude/config/quality/lenses/<type>.json`.

## How to run a craft pass
1. Pick the deliverable types; use `plan --domain` when unsure. Mixed work gets several lenses.
2. First ten seconds: open or use the deliverable cold, as each stakeholder, and write what you notice
   before you read a single check.
3. Work the block checks first, then the warn checks. Collect the evidence each check names: a
   screenshot that was read (not only captured), a command with its exit code, a rendered message, a
   recomputed figure.
4. Fill `review-template`: per stakeholder what they notice in ten seconds and on closer inspection;
   per check a mark, the evidence path, the finding, and the fix or the stated weakness.
5. Fix what you can now and inspect again. What stays weak goes into the report in plain words: what
   it is, who would notice, why it is not fixed now.

## Marks and rules
- Marks: CLEAN (inspected, evidence attached, nothing a stakeholder would notice) · DEFECT ·
  NOT_INSPECTED · N/A (with the reason).
- A block check marked DEFECT or NOT_INSPECTED means the deliverable is not done. A warn DEFECT is
  fixed or listed as a stated weakness.
- The tool never marks anything; only a reviewer with evidence does. Never mark CLEAN from reading
  code when the check asks for a screenshot or a run.
- A STALE LENS notice (a citation no longer matches its source) is reported, not ignored.

## Lenses
web-ui, copy-and-content, code, automation-workflow, documents-and-spreadsheets, data-and-reports,
game-and-interactive, cli-and-devtools, api-and-integration, voice-and-chat, generic. Each check says
whether it is cited (a playbook, a hard rule, an agent checklist or the owner's own evidence) or
professional practice (with a one-line reason).

## References
- `references/review-form.md`: how to fill the form well, with a worked example.
- `references/lens-authoring.md`: how to add or change a lens without padding or invented rules.
