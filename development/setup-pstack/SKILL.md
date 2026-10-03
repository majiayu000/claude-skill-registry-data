---
name: setup-pstack
description: Configure which models pstack uses per role and at what budget. Writes the model configuration the pstack session hook loads into every session, overriding the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.claude/pstack-models.md`. The pstack SessionStart hook loads it into every session and subagent, and it overrides the skill defaults. When the file is missing the hook falls back to `~/.claude/skills/poteto-mode/pstack-models.md`. `PSTACK_MODELS_FILE` overrides both for one run.

This skill is rewritten for Claude Code. Upstream detects the editor's model slugs and lowers the reasoning-effort token per budget. The Agent tool takes a model alias and has no per-subagent effort, so here a budget picks the tier per role and the length of each panel.

## Steps

### 1. Detect available models

Any alias the Agent tool's schema lists is a valid Agent `model` value, and so are `inherit-parent` and `auto`. The session context lists pstack's tiers strongest first, from `MODEL_TIERS` in `~/.claude/skills/poteto-mode/hooks/kinds.mjs`. Recommend the top tier for judgment roles.

### 2. Load current state

If `~/.claude/pstack-models.md` exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from `~/.claude/skills/poteto-mode/pstack-models.md`.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer AskUserQuestion over free text. Offer these four options, and name the current budget when the file records one.

| Budget | Judgment roles | Code roles | Runner panels | Cross-judge pool | Interrogate reviewers |
|---|---|---|---|---|---|
| `unlimited` | `tier 1` | `tier 2` | `tier 1, tier 1, tier 2` | `tier 1` | `tier 1, inherit-parent` |
| `large` | `inherit-parent` | `tier 2` | `inherit-parent, tier 1, tier 2` | `inherit-parent` | `inherit-parent, tier 1` |
| `medium` | `inherit-parent` | `tier 2` | `inherit-parent, tier 2` | `inherit-parent` | `inherit-parent, inherit-parent` |
| `small` | `inherit-parent` | `tier 3` | `inherit-parent, tier 2` | `inherit-parent` | `inherit-parent, inherit-parent` |

`tier 1` is the first alias of the tier list in the session context, `tier 2` the second and `tier 3` the third. Write the alias, never the label.

Judgment roles are `judgment and prose`, `hardest tasks`, `how explainer`, `why synthesizer`, `reflect tooling` and the `reflect` judgment line. Code roles are `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `how explorer`, `why investigators`, `swarm workers`. Runner panels are `arena runners` and `architect runners`.

A judge never runs below the parent model, so every judgment role, the cross-judge pool and the interrogate reviewers take only `inherit-parent`, `auto` or the top tier. Budget lowers the tier of the roles that produce work, never a judge. Runner panels may include `tier 2`, because runners produce candidates and a judge grades them.

No runner panel or reviewer list drops below two entries. The **principle-exhaust-the-design-space** principle needs two structurally distinct candidates. The cross-judge pool is exempt, because Arena spawns one judge from it.

**(b) Apply it.** Build the working table from the budget row. On a re-run keep any role the user changed by hand.

**(c) Show the roles and confirm.** Show every role with its model. Ask whether to accept as-is or change specific roles. For panel roles the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it.

### 4. Validate

Every alias written must be in the Agent tool's schema. `inherit-parent` and `auto` always pass. Every entry of a judgment role (the `JUDGMENT_ROLES` set in `~/.claude/skills/poteto-mode/hooks/catalog.mjs`) must be `inherit-parent`, `auto` or the top tier. A role the user set below that goes back to the budget row, and you tell them why.

### 5. Write the file

Write `~/.claude/pstack-models.md` in the same shape as `~/.claude/skills/poteto-mode/pstack-models.md`: the comment header, a `# budget:` line with the chosen label, and one line per role using the same labels poteto-mode uses. Overwrite the whole file so re-runs stay idempotent.

### 6. Confirm

Tell the user the file was written and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, open the `create-verification-skill` skill and follow it. On no, move on without pushing.

## Standing skips

To waive a writing convention in every session, the user writes `skip <name>: <reason>` lines to `~/.claude/pstack-skips.md`, as in `skip technical-writing: commit messages follow the team's guide`. A standing skip may name only `technical-writing`, `unslop`, `docs-prose`, `pr-prose` or `pr-draft`. A skill name counts as that skill read for every ask, and a rule name drops that ask. The hook ignores a line that names anything else, such as `ledger`, `design`, `deslop` or a playbook, and counts only the name of a line it honors, never its reason.

A `.claude/pstack-skips.md` in the directory a session starts in counts for that project only after the user trusts it. Trust is a line `trust <project root> <sha256 of the file>` in `~/.claude/pstack-skips.md`. A changed file needs a new trust line. At the start of each session the hook shows the user every active, ignored and untrusted standing skip, and for an untrusted file it prints the exact trust line to add.

The hook refuses an agent's write to either file. When the user asks to opt out of a convention for good, give them the exact line to add.
