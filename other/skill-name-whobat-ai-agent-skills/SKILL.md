---
name: skill-name
description: What the skill does and WHEN to use it — be specific and a little pushy, agents undertrigger. Include example user phrasings ("do X with Y", "check Z"), key terms agents can match on, and a negative trigger if a sibling skill could be confused ("Do NOT use for W — that is other-skill"). Third person, max 1024 chars, no XML tags.
license: MIT
compatibility: Only include if the skill has real environment requirements (runtime, permissions, network). Max 500 chars. Delete this line otherwise.
metadata:
  version: "1.0.0"
---

# Skill Name

One-paragraph overview: what this skill achieves and the core approach
(e.g. "the bundled script collects X as JSON; the agent writes the narrative").

## How to run (script-backed skills)

`SCRIPT` = this skill's `scripts/Your-Script.ps1`. Document the exact invocation,
a table of the parameters that matter, and 2-3 copy-paste examples.

## Output contract

What the script prints (JSON shape, exit codes), and what goes to a file vs stdout.

## What you (the agent) do with the result

1. Numbered, imperative steps.
2. Lead with what matters; don't recite everything.
3. Fail loud: name every coverage gap, skipped section, or unverified assumption.

## Gotchas

REQUIRED (validator-enforced; may live here or in REFERENCE.md). The *real*,
mechanism-level pitfalls of this domain — the traps that produce confident-but-wrong
conclusions. For each: **the trap → why it happens → the correct check/fix.** Cover
measurement traps (a tool/command that reports a misleading value), errors that point
at the wrong cause, environment foot-guns, and known misattributions. Keep it honest and
specific — a few verifiable gotchas beat a padded list. Add to it when a real run uncovers
a new pitfall. **Committed gotchas must be generic — no company-specific data.**

**Environment-specific gotchas (local).** At the start of a run, read `gotchas.local.md`
in this skill's folder if it exists — it holds traps learned in *this* environment (real
server/DB names, local quirks). When you discover a new environment-specific pitfall,
**append it there**, not to this file. `gotchas.local.md` is gitignored and is preserved
across skill updates, so the skill gets more useful every time it's used here.

## Verification

REQUIRED (validator-enforced; may live here or in REFERENCE.md). Document two things:
1. **Before changes** — how to verify correctness/preconditions first: a baseline, a repro,
   a health-check, or (for read-only skills) how to confirm ground truth and coverage before
   recommending anything. Never propose a change without a before-check.
2. **Output** — how to verify the result afterward: re-run the check, confirm the expected
   effect landed, and **fail loud** if it can't be confirmed. Never report "done" unverified.

## Errors

Known failure modes → what to tell the user.

<!--
Checklist before opening a PR (see CONTRIBUTING.md):
- [ ] Has a "## Gotchas" section (here or in REFERENCE.md) — validator-enforced
- [ ] Has a "## Verification" section (before-change check + output check) — validator-enforced
- [ ] Tells the agent to read/append gotchas.local.md for env-specific learnings
- [ ] Lives in a category folder: skills/<category>/<name>/ ; new category -> add it to .claude-plugin/plugin.json
- [ ] Skill's own folder name == frontmatter name (lowercase, hyphens), globally unique
- [ ] description ≤ 1024 chars, includes when-to-use triggers
- [ ] metadata.version set; bump it on EVERY behavior change
- [ ] SKILL.md < 500 lines; details go in REFERENCE.md (linked one level deep)
- [ ] Scripts have tests next to them (*.Tests.ps1 / test_*.py)
- [ ] skill.install.json if the skill needs runtimes/credentials
- [ ] evals/<skill-name>.json with 3+ scenarios
- [ ] No company-specific data (AGENTS.md contract) — placeholders only
- [ ] `npm run validate` passes
-->
