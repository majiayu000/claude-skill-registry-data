---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models, sorts them into tiers, and writes the platform's model file that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.config/dev-platform/pstack-models.md`, the file that sets pstack's model per role on this platform. Every pstack skill reads it through `bin/pstack-model`, and the loop reads it for its workers. It replaces Cursor's `~/.cursor/rules/pstack-models.mdc`.

The skills never name a model. Each role names a **tier slug**, `<tier>[.<n>]-<effort>`: `judgment-max`, `judgment.2-max`, `implementation-xhigh`, `mechanical`. The file's `tier` lines say which model families fill each tier, in order; `.n` picks the nth family, which is how a panel gets a second family. So a skill keeps its own logic about how strong and how deliberate each role should be, and this file alone decides what that means on this machine. A role may still name a concrete slug (`fable-max`, `codex:gpt-5.6-sol-high`) to pin it.

## Steps

### 1. Detect available models

A family is what a runtime accepts as a model: for Claude Code the `Agent` tool's `model` (`fable`, `opus`, `sonnet`, `haiku`) or a full id `claude --model` accepts; for Codex, `codex:<model>` as `codex --model` accepts it. Confirm a family by running it once (`claude -p --model <model> --effort low 'reply ok'`, `codex exec --model <model> 'reply ok'`) or from the account's documented entitlements; `ai-account status` names the verified accounts. If you cannot detect any, ask the user to paste the models they have. Never write a family you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid.

### 2. Load current state

`bin/pstack-model defaults` prints the default file, the shape in step 5. If `~/.config/dev-platform/pstack-models.md` exists, read it: its `# budget` line, its `tier` lines and its role values are the current choices, and a line it lacks takes the default. A role line whose role is not in the defaults, such as `how critics`, is from a retired role. Drop it. A file from before tiers has concrete role values and no `tier` lines; it still works, and step 3 offers to move it to tier slugs.

### 3. Tiers, budget, and confirm

**(a) Fill the tiers.** From the detected families, order each tier strongest first:

- `judgment`: the strongest reasoning families. Put a family from a different vendor second, so `.2` gives panels a second opinion.
- `implementation`: capable, cheaper families for bounded work with a check behind it.
- `mechanical`: the cheapest family, for triage, formatting and summaries.

Drop any default family that was not detected. A tier left empty needs a choice. Show the tiers and ask whether to accept them. Prefer AskUserQuestion over free text.

**(b) Ask for a budget.** Offer these four options with these exact labels, and name the current budget when the file records one.

- `unlimited — keep max`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(c) Apply it.** Build the working table from the defaults, and on a re-run keep any role you changed by tier, family, list, or alias. `unlimited` leaves every effort as in that table. `large`, `medium`, and `small` set the effort token of every slug, panel entries included, to `xhigh`, `high`, or `medium`. The effort token is the last hyphen token, on the ladder `max` > `xhigh` > `high` > `medium` > `low`; a slug without one, like `mechanical`, keeps none. So `small` turns `judgment-max` into `judgment-medium` and `implementation-xhigh` into `implementation-medium`. A concrete slug whose result is not detected takes the same family's detected slug with the highest effort at or below the target, else needs a choice. `inherit-parent` and `auto` do not change.

**(d) Show the roles and confirm.** Show every role with its slug and what it resolves to (`bin/pstack-model resolve '<role>' --all`), and list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the tier slugs, the detected families, and `inherit-parent` and `auto` (both mean: this role runs on the parent chat model). For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every family on a `tier` line and every concrete slug must be detected. `inherit-parent` and `auto` always pass. After writing, `bin/pstack-model resolve '<role>' --all` must print a model for every role. If anything fails, stop and ask again.

### 5. Write the file

Write `~/.config/dev-platform/pstack-models.md`: the `# budget` line with the chosen label and its target effort, the `tier` lines, and one line per role, using the same labels dev-plat uses. Overwrite the whole file so re-runs stay idempotent. The defaults, which `bin/pstack-model defaults` prints:

```
# pstack model configuration. Tier lines map each tier to its model families, in order;
# role lines name a tier slug `<tier>[.<n>]-<effort>` or a concrete model. Delete a line to fall
# back to the default. `inherit-parent` or `auto`: the role runs on the parent chat model.
# budget: unlimited (max)
tier judgment: fable, codex:gpt-5.6-sol, opus
tier implementation: sonnet, codex:gpt-5.6-sol
tier mechanical: haiku
feature, refactoring: implementation-xhigh
bug-fix: implementation-xhigh
perf-issue: implementation-xhigh
hillclimb: implementation-xhigh
judgment and prose: judgment-max
hardest tasks: judgment-max
how explorer: implementation-xhigh
how explainer: judgment-max
why investigators: implementation-xhigh
why synthesizer: judgment-max
reflect tooling: judgment.2-max
reflect judgment, divergent, synthesizer: judgment-max
arena runners: judgment-max, judgment.2-max, implementation-xhigh
arena cross-judge pool: judgment-max, judgment.2-max, implementation-xhigh
swarm workers: implementation-xhigh
architect runners: judgment-max, judgment.2-max, implementation-xhigh
interrogate reviewers: judgment-max, judgment.2-max, implementation-xhigh
```

The loop reads two of these lines for its workers, through `bin/pstack-model --runtime claude`: `feature, refactoring` for implementation tasks and `judgment and prose` for tasks labeled `spec`, `decision`, `privacy` or `security`; `documentation` tasks take the `mechanical` tier. `docs/models.md` states what the tiers are for.

### 6. Confirm

Tell the user the file was written and that it applies to new sessions and to workers the loop starts after this. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on without pushing.
