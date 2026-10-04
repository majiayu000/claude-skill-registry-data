---
model_tier: inherit
name: rule-writing
description: "Use when creating or editing a rule in src/rules/ — trigger wording, always vs auto classification, size budget — even when the user just says 'add a rule for X'."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

<!-- cloud_safe: degrade -->

# rule-writing

## When to use

* Creating a new rule in `src/rules/{name}.md`
* Rewriting an existing rule (not a typo fix)
* Deciding whether something should be a rule at all
* Converting a learning from `learning-to-rule-or-skill` into a concrete rule

Do NOT use this skill when:

* The content is a multi-step workflow → use `skill-writing`
* The content is reference material agents cite → use `guideline-writing`
* The content is a user-invoked action → use `command-writing`

## Rule vs skill vs guideline — critical test

| Intent | Artifact |
|---|---|
| "Agent must always/never do X" | **Rule** |
| "When Y happens, run these steps" | **Skill** |
| "Here is knowledge the agent may cite" | **Guideline** |

A rule is a **constraint** — it states a boundary, not a workflow. If the
content needs numbered steps, it is a skill.

## Procedure

### 0. Run the Drafting Protocol

Creating or materially rewriting a rule **must** go through Understand →
Research → Draft from the
[`artifact-drafting-protocol`](../../rules/artifact-drafting-protocol.md) rule.

* **Understand** — which agent behavior is wrong today? What should change?
  Can you point to a concrete incident or repeated pattern?
* **Research** — **inspect** `src/rules/` for overlap
  and **analyze** `rule-type-governance`, `size-enforcement`,
  `skill-quality` before drafting.
* **Draft** — propose frontmatter (`type`, `description`) first, wait for
  confirmation, then fill the body.

### 1. Classify type — `always` vs `auto`

Normative source: [`rule-type-governance`](../../rules/rule-type-governance.md).

* `always` — universal behavior (language, scope, safety, verification)
* `auto` — triggered by description match on domain/symptom

Default to `auto`. `always` must be justified — if >50% of conversations
don't need it, it is `auto`.

### 2. Write a trigger-style description

The `description` field **is** the trigger. Describe **when** the rule
applies, not **what** it contains. Hard cap: **200 characters** (the
linter errors `description_too_long` above it); the rule schema
(`rule.schema.json`) additionally sets `maxLength: 190`.

```yaml
# Bad — describes content, won't match reliably:
description: "PHP coding standards"

# Good — trigger-shaped, names domain + symptoms:
description: "Writing or reviewing PHP code — strict types, naming, comparisons, early returns, Eloquent conventions"
```

When iterating on phrasing, delegate to the
[`description-assist`](../description-assist/SKILL.md) skill — approval-gated,
no silent edits, max two rounds.

### 3. Write the rule body

* Short, constraint-only, easy to scan.
* Bullet lists, tables, do/don't blocks — not paragraphs of prose.
* No numbered procedures — if you need steps, it is a skill.
* Link out to guidelines for deep reference instead of inlining them.

### 3b. Path conventions in frontmatter and body — load-bearing

Three different surfaces, three different rules. Mixing them up will
either fail the schema (`./scripts-run src/scripts/validate_frontmatter`) or
fail `./scripts-run src/scripts/lint_load_context`. Canonical reference:
[`templates/rule.md`](../../templates/rule.md) § Path conventions and
[`docs/contracts/load-context-schema.md`](../../../docs/contracts/load-context-schema.md).

| Field | Form | Example |
|---|---|---|
| `load_context:` / `load_context_eager:` | **Logical name** rooted at the source — never `src/` | `contexts/execution/verification-mechanics.md` |
| `triggers[].path_prefix:` | **Literal match pattern** the host evaluates against the file the agent is editing — not rewritten | `src/skills/` (source-of-truth rules) or `agents/`, `app/`, `.augment/` |
| Body links to guidelines / contracts | **Verbatim relative form** — `../../docs/...` works in any markdown viewer; rewriter handles depth | `[guideline](../../docs/guidelines/<group>/<name>.md)` |

The condense-time rewriter (`scripts/condense.ts::_rewrite_paths`) is
idempotent and depth-aware — it resolves logical names and body links
to the deployment-correct relative path at condense time, leaving
`path_prefix:` literally as written. The schema regex
(`scripts/schemas/rule.schema.json`) and `scripts/lint_load_context.ts`
both reject the `src/` prefix in `load_context:` /
`load_context_eager:` with an error pointing at the canonical logical
name.

### 4. Enforce the size budget

Normative source: [`size-enforcement`](../../rules/size-enforcement.md) +
`docs/guidelines/agent-infra/size-and-scope.md`.

| Category | Target |
|---|---|
| Ideal | < 60 non-empty lines |
| Acceptable | < 100–120 lines |
| Hard limit | < 200 lines |

Linter emits `long_rule` above ~80 non-empty lines. Above that, justify in
the PR or split by responsibility.

### 5. Validate

* Run `./scripts-run src/scripts/skill_linter src/rules/{name}.md`
  → must report **0 FAIL**.
* Run `bash scripts/condense.sh --sync` to regenerate `dist/agent-src/rules/{name}.md`.
* Run `./scripts-run src/scripts/condense --generate-tools` to project into `.claude/`, `.cursor/`, `.clinerules/`, `.windsurfrules`.
* Run the full CI pipeline locally (see `Taskfile.yml` in this repo for
  the script list) — must exit 0 except for tolerated warnings.

### 5b. Budget-discipline gate — hard stop

After validation, before declaring the rule done, run:

```bash
./scripts-run src/scripts/measure_augment_budget --check
```

If utilisation is `≥ 0.95` (or the check exits non-zero), **STOP** and
invoke [`rule-refactor`](../rule-refactor/SKILL.md). Do NOT:

* Trim the new rule further to "just fit" — if it needs that body to
  do its job, the rule is right and the rule set around it is wrong.
* Raise `FAIL_THRESHOLD` in `scripts/measure_augment_budget.ts` —
  threshold-lift is explicitly forbidden (see the
  [`validation-budget`](../../rules/validation-budget.md) rule and
  the `rule-refactor` Iron Law).
* Promote an always-rule to auto to dodge the cap if the rule's
  semantics require always-on visibility — that breaks the rule, not
  the budget.

The discipline: budget pressure is the signal that the rule **set**
needs a cleanup pass, not that the new rule needs to be smaller. The
`rule-refactor` skill runs the audit and proposes merge / delete /
move-to-context / promote-to-skill so the new rule earns its space.

### 6. Governance baseline (when introducing a new linter check)

**Advisory, reviewer-checked — no CI gate.** When the same PR adds a
new check to `scripts/skill_linter.ts` (or strengthens an existing
one) such that previously-clean rules now warn, the PR body MUST
record the pre-existing violations on `main` in a Markdown table:

```markdown
### Pre-existing baseline (informational)

| Code | Count on main | Bucket |
|---|---:|---|
| {new_code} | N | (a) genuine fix · (b) accept · (c) check too aggressive |
```

Forward-only: the new check applies to **the rule under review** and
to **future** edits. The baseline table is informational so reviewers
can distinguish genuine debt from acceptable carry-overs without
diffing the full lint output. See
`agents/evidence/analysis/lint-warning-triage.md` for the 3-bucket reference.

## Frontmatter shape

```yaml
---
type: "auto"              # or "always"
description: "Trigger-shaped sentence — domain + symptoms — schema max 190 chars"
alwaysApply: false        # true only if type: always
source: package           # or project for consumer-local rules
load_context:             # logical names only — `contexts/<area>/<file>.md`
  - contexts/execution/verification-mechanics.md
triggers:                 # path_prefix is literal, not rewritten
  - path_prefix: "src/rules/"
routes_to:
  - "skill:related-skill"
---
```

See § 3b above for the load-bearing distinction between `load_context:`
(logical, rewritten), `triggers[].path_prefix:` (literal, verbatim),
and body links (relative `../../docs/...`, rewriter handles depth).

## Required: name the primary bias this rule overrides

```
EVERY RULE STATES, IN ONE SENTENCE, THE MODEL'S WRONG DEFAULT IT EXISTS TO
OVERRIDE. NOT THE HISTORY. NOT THE RATIONALE. THE TENDENCY.
A RULE THAT CANNOT NAME ONE IS A RULE WITH NO OBSERVED FAILURE BEHIND IT.
```

One sentence, near the top, in the shape *"left alone, the model
&lt;does the wrong thing&gt;"*:

- ✅ "Left alone, the model treats a question as an instruction and starts
  building."
- ✅ "Left alone, the model reports the happy path it just made pass and calls
  the change finished."
- ❌ "This rule exists because a session in June went badly." — backstory.
- ❌ "Correctness matters." — a value, not a tendency.
- ❌ "Agents sometimes make mistakes." — true of everything, discriminates
  nothing.

**Why this field and not a longer rationale.** It is the discriminator the
mechanism-must-match-an-observed-failure-mode discipline wants at *authoring*
time: a rule whose bias sentence is a plausible generality is a rule aimed at
nothing in particular, and that is visible in one line where it is invisible in
three paragraphs. The field is also the input to the removal question later —
`decision-review` asks whether the agent still exhibits the named tendency, and
that question cannot be asked of a rule that never named one.

**Retrofit is opportunistic, never a sweep.** Add the sentence when you touch a
rule for another reason. A batch edit across the rule set trips the
kernel-prefix byte-stability gate, and that gate is right to fire — the kernel
prefix is pinned deliberately.

## Optional: enumerate condition-action clauses

A rule body mixes two shapes. **Standing obligations** hold for every turn the
rule is loaded ("every reply mirrors the user's language"). **Condition-action
clauses** fire on a situation ("when the diff deletes a directory, surface it").
The router matches on frontmatter; in-body conditionals are prose, so a rule's
situational half is invisible to everything except a full read.

Where a rule carries more than two of them, group them under a
`## Conditions` heading, one bullet per clause, each in the shape
**`<condition>` → `<action>`**. Two effects, both cheap:

- A reader can answer "does this rule apply to what I am doing?" from a list
  instead of by reading the body.
- A condition that turns out to be unreachable becomes visible as a line, which
  is the input `decision-review` needs to ask whether the clause still earns its
  place.

Optional on purpose. A rule with one conditional does not need a section to hold
it, and a heading over a single bullet is ceremony.

## Optional: state the decision-impact class

`type:` is a **delivery** class — how the rule reaches the model. It says
nothing about what is at stake when the rule fires, and kernel-membership and
always-loaded-budget arguments were being made with no stated impact class at
all. `decision_impact:` carries that, with three values:

| Value | Meaning | Consequence |
|---|---|---|
| `overrides-model-default` | the model's base behaviour is wrong here | load-bearing; the strongest case for staying loaded |
| `encodes-house-choice` | the model would make *a* defensible choice, not *ours* | stays until the house choice changes |
| `already-complied-with` | the model does this unprompted | **the one value that permits removal** |

The third carries an evidence bar, enforced by `lint_decision_impact`: it
requires `decision_impact_evidence`, a pointer a reviewer can follow to the
observation. The bar exists because that classification is what permits deleting
a rule, and "the model probably does this anyway" is the cheapest possible way
to remove a floor that was working precisely *because* nothing had crossed it —
`active-remediation` names that failure as deleting a rule that is merely quiet.

**Optional, and backfill is opportunistic.** Classifying all 111 rules in one
batch is exactly the shape that trips `check_kernel_prefix_stability`. Add it to
new rules, and to a rule you are already touching for another reason.

## Output format

1. Complete rule file at `src/rules/{name}.md`
2. Frontmatter fully populated, no placeholders left
3. Linter output showing 0 FAIL
4. Confirmation that `bash scripts/condense.sh --sync` + `./scripts-run src/scripts/condense --generate-tools` ran clean

## Gotchas

* Writing a rule that duplicates an existing one — always grep first.
* Defaulting to `always` "just in case" — token cost is real, `auto` is default.
* Description like "Rule about X" — it must describe *when*, not *what*.
* Pasting a workflow into a rule — if it has numbered steps, split into a skill.
* Forgetting to run `./scripts-run src/scripts/condense --generate-tools` — downstream tools stay stale.
* Editing `dist/agent-src/rules/` or `.augment/rules/` directly — those are generated.

## Frugality Standards

Apply the [Frugality Charter](../../contexts/contracts/frugality-charter.md)
to every rule you author.

**Examples in this artifact:**
- Per the charter's default-terse rule, no intent prose in the rule
  body — start with the obligation, not a setup paragraph.
- Per the Iron-Law literal predicate, ALL-CAPS fenced obligations
  belong only when the rule sits on the
  [`kernel-membership`](../../../docs/contracts/kernel-membership.md)
  list.
- Per the cheap-question check, the rule's "When to ask" guidance
  must list decidable triggers, not vibe-based judgment.

**Pre-save self-check:**
1. Does the rule body open with the obligation, or with a setup
   paragraph?
2. Are any examples mere narration (no decidable test)?
3. Are ALL-CAPS Iron-Law blocks used outside a kernel-listed rule?
4. Are interactions duplicated from another rule rather than linked?

## Do NOT

* Do NOT inline long procedures
* Do NOT exceed the hard size limit without an explicit waiver
* Do NOT edit projections (`dist/agent-src/`, `.augment/`, `.claude/`, etc.)
* Do NOT skip the linter
* Do NOT create a rule when a guideline or skill is the right shape

## Cloud Behavior

On cloud surfaces (Claude.ai Web, Skills API) the package's
`scripts/skill_linter.ts`, `scripts/condense.ts`, and `task` runner
are not reachable. The skill still applies — with prose-only
validation:

* Emit the full rule file as a copyable Markdown block. Do not
  attempt to write to disk.
* Self-check the frontmatter against the rules: `type` is `always`
  or `auto`, `description` is trigger-shaped, `alwaysApply` matches
  `type`.
* Self-check the body: under the size budget (200 lines hard,
  120 soft), trigger sentence first, no embedded procedures.
* Tell the user to save under `src/rules/{name}.md`
  and run `task sync && task lint-skills` locally before committing.
* Do not call the linter or condenseor — they only run on the
  user's machine.

## Examples

Good description (trigger-shaped, names domain + symptoms):

> "Git commit message format, branch naming, conventional commits, committing, pushing, or creating pull requests"

Bad description (no trigger, too vague):

> "Commit conventions"

### Contrastive-example slot (optional, for the rule body)

The pair above governs descriptions. A rule whose obligation is easy to agree
with and hard to apply — what counts as a cheap question, when an interrupt is
an interrupt, which reply mirrors the user's language — needs the same treatment
for the **behaviour**, not just the frontmatter.

Six live corpora already carry those pairs:
[`direct-answers-demos`](../../../docs/guidelines/agent-infra/direct-answers-demos.md),
[`asking-and-brevity-examples`](../../../docs/guidelines/agent-infra/asking-and-brevity-examples.md),
[`language-and-tone-examples`](../../../docs/guidelines/agent-infra/language-and-tone-examples.md),
and `autonomy-examples` / `interrupt-examples` / `cheap-question-mechanics` under
`src/agent-src/contexts/execution/`. Follow one; do not invent a format.

The shape they share: the **wrong** version in the form it actually gets
written, the **right** version, and one line of **why** — the why is what makes
it a rule rather than a memorised case.

Where the pairs go is a size decision, not a taste one. A rule body is capped at
200 lines hard / 120 soft, so more than two or three pairs belong in a guideline
or context file the rule points at — same split
[`skill-writing`](../skill-writing/SKILL.md) § Contrastive-example slot uses.
