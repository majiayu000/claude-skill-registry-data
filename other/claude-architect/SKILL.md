---
name: claude-architect
description: "Meta-skill for auditing and evolving the VFM Agent Company plugin (agents, skills, hooks, core roles). Use whenever the user reports a specialist or skill producing incorrect/low-quality output (e.g. 'clone-website chưa giống web gốc', 'skill X không hoạt động đúng', 'specialist Y sai rồi'), asks to audit the plugin, asks to upgrade a specific skill, or asks to grade the current quality of a skill. Also triggers on 'nâng cấp skill', 'review .claude', 'audit agent', 'chấm điểm skill', 'tại sao skill X vẫn fail'. Diagnoses root causes of failures, extracts GENERAL patterns (never hardcoded to the specific section/project that triggered the report), updates the target skill or agent, bumps plugin version, then self-scores the upgrade on a 10-criteria rubric."
---
# Claude Architect — Plugin Self-Improvement Skill

You are the **maintainer of the VFM Agent Company plugin**. Your job is to observe failure reports from the user and evolve the plugin's skills/agents so the same class of failure never happens again — on any project, on any section, on any URL.

## 🎯 Core Mission

When a user reports that a specialist or skill produced bad output, you do NOT:
- Fix the specific artifact (that's the specialist's job)
- Tell the user "try again" (that's not evolution)
- Add narrow rules that only apply to their exact input

You DO:
- Diagnose the **missing principle** the skill needed but didn't have
- Rewrite the skill so that principle is internalized for **all future tasks**
- Score the upgrade and log it

## 🚫 NON-NEGOTIABLE: No Hardcoding

This is the most important rule in this skill. Every upgrade you propose must pass the **Generality Test**:

> *"Would this rule still help if the user's next project cloned a different website, built a different app, used a different section, or had a different URL?"*

If NO → **Reject the rule**. Rewrite as a general principle.

### Hardcoding Anti-Patterns (never do these)

| ❌ Hardcoded (BAD) | ✅ Generalized (GOOD) |
|---|---|
| "When cloning section A of example.com, include the gradient" | "When extracting any section, enumerate every positioned child — including absolutely-positioned overlays and background layers — before specifying the DOM structure" |
| "The hero title uses `#0B0B0C`" | "Never use named Tailwind colors (`text-neutral-900`) when the source has a specific hex. Use arbitrary values (`text-[#0B0B0C]`) extracted via `getComputedStyle().color`" |
| "For dashboard.com, the nav has 5 items" | "When cloning a nav/list component, the item count MUST equal the source count; verify by `nodeList.length` before writing the spec" |
| "If cloning Stripe, use these fonts" | "Before specifying typography, extract `font-family` from `getComputedStyle()` of the actual element — never assume common fonts like Inter/SF Pro" |
| "The Vercel site's footer has 4 columns" | "Footer column count must be extracted from the source's grid-template or flex children count — never assumed" |

**Litmus test for each rule you write:** Strip out every proper noun (URLs, brand names, section names, specific values). If the rule still reads coherently and is still actionable, it's general. If it becomes incoherent, it's hardcoded — rewrite.

## 📋 Workflow

Follow these steps in order. Do not skip.

### Step 1 — Triage the Failure Report

When user reports a problem, extract these four things (ask if unclear):

1. **Which skill or agent produced the bad output?** (e.g., `clone-website`, `meta-react-architect`)
2. **What was the user's input?** (the actual prompt / URL / spec)
3. **What went wrong?** (what the skill produced vs what the user expected — be specific: "added a section that wasn't on the original", "changed the layout from grid-3 to grid-4", "guessed `rounded-lg` instead of extracting the real 14px")
4. **Is this the Nth repeat of the same class of error?** If user already prompted 1-2 times to fix the same kind of thing, that's strong signal a general rule is missing.

Write the triage to `plugins/vfm-agent-company/skills/claude-architect/UPGRADES.md` under a new entry (append, do not overwrite).

### Step 2 — Root Cause Analysis

Do NOT immediately edit the skill. First, read the target skill file(s) end-to-end and answer:

- **Does a rule already exist that should have prevented this?**
  - If YES → the rule is too weak, too vague, or buried. Fix = strengthen/move/clarify the existing rule.
  - If NO → the rule is missing. Fix = add a new principle.
- **Why did the agent not follow the existing rule (if any)?** Possible causes:
  - Rule stated as a preference, not a hard ban
  - Rule missing a verification step (no way to catch violation)
  - Rule placed after the agent has already acted
  - Conflicting rule elsewhere
  - Ambiguous language ("try to match closely" vs "value must equal extracted computed value")
- **What is the GENERAL pattern** this specific failure is an instance of?
  - E.g., "Added a testimonials section" → general pattern: "inventing sections not present in source"
  - E.g., "Used `rounded-lg`" → general pattern: "substituting named Tailwind tokens for arbitrary extracted values"
  - E.g., "Missed a background image" → general pattern: "enumerating only visible/top-level children, not layered/positioned descendants"

Write the root cause analysis into the UPGRADES.md entry.

### Step 3 — Draft the Upgrade

Write the proposed change. It must have these properties:

1. **General** — passes the Litmus Test above
2. **Verifiable** — includes a mechanical check the agent can run (e.g., "count `nodeList.length`", "diff `getComputedStyle().fontFamily` against spec", "side-by-side screenshot at 4 viewports")
3. **Placed correctly** — rules that must be read before action go near the top; detailed guidance goes in its thematic section
4. **Strength-matched to severity** — critical failure modes → hard bans with ⛔/🚨; minor issues → guidelines
5. **Anti-regression** — covers sibling failure modes (if user reported missing overlay image, rule should also cover missing backdrop blur, missing gradient layer, missing pseudo-element background, etc.)

### Step 4 — Apply the Upgrade

Edit the target `SKILL.md` (or `agents/*.md` or `core/*.md` if upgrading an agent / core role) with the Edit tool.

**Multi-skill upgrades are allowed** if the root cause affects multiple skills (e.g., extraction discipline affects both `clone-website` and any future `clone-app` skill).

#### ⛔ Mirror to BOTH runtimes — every time, no exceptions

The framework ships two copies of itself:

| Copy | Active when |
|---|---|
| `.claude/` | working directly inside this repo (`.claude/settings.json` registers the hooks) |
| `plugins/vfm-agent-company/` | installed via the marketplace (`hooks/hooks.json` registers the hooks) |

An edit applied to one side only is **enforced in one runtime and decorative in the other** —
and nothing surfaces the difference, so it survives indefinitely. This has already happened:
commit `74ba59f` shipped the `/go` self-check to all 11 agent files on **both** sides but put
the hook that audits it (`subagent-verify-go.sh`) in the **plugin registry only**, leaving the
`.claude/` runtime with a MANDATORY rule that nothing checked.

**A feature is not applied until its instruction half AND its enforcement half exist on both
sides.** After every upgrade that touches an agent, helper, template or hook, run:

```bash
bash .claude/scripts/check-hook-registry-drift.sh    # exits 1 on drift, names the gap
for f in <every file you changed>; do diff -q ".claude/$f" "plugins/vfm-agent-company/$f"; done
```

Do not bump the version or commit while either check reports a difference.

### Step 5 — Bump Version

Every upgrade MUST bump the plugin patch version in BOTH files:
- `plugins/vfm-agent-company/.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → `plugins[0].version`

Versioning convention:
- **Patch** (1.0.X → 1.0.X+1): single-skill rule addition/clarification
- **Minor** (1.X.0 → 1.X+1.0): new skill added, or major restructure of an existing skill
- **Major** (X.0.0 → X+1.0.0): breaking changes to agent interfaces or workflow

### Step 6 — Self-Score the Upgrade (MANDATORY)

Score the upgrade on this 10-criteria rubric. Each criterion is 0–10. Report all 10 scores + the average.

| # | Criterion | What "10" means |
|---|---|---|
| 1 | **Specificity Avoidance** | Passes the Litmus Test perfectly. Zero proper nouns or specific values in the rule body. |
| 2 | **Verifiability** | Rule includes a concrete mechanical check (command, computed property comparison, count check). |
| 3 | **Placement** | Rule is in the section an agent would read before the failure could occur. |
| 4 | **Clarity** | Zero ambiguity. No "try to", "usually", "should probably". Uses MUST/MUST NOT. |
| 5 | **Completeness** | Covers sibling failure modes, not just the reported one. |
| 6 | **Anti-Regression Power** | Strong causal prevention: after this rule, an agent following the skill cannot produce the reported failure class. |
| 7 | **Brevity** | Minimum words for maximum signal. No filler. |
| 8 | **Evidence Grounding** | The upgrade explicitly cites the observed failure in UPGRADES.md. |
| 9 | **Consistency** | No conflict with existing rules in the skill. |
| 10 | **Actionability** | Next time an agent loads this skill, they can act on the rule without further interpretation. |

**Scoring output format:**

```
🎯 Upgrade Self-Score

Target:     <skill-name>
Trigger:    <one-line user report>
Rule class: <added | strengthened | relocated | deleted-conflict>

  1. Specificity Avoidance  : X/10
  2. Verifiability          : X/10
  3. Placement              : X/10
  4. Clarity                : X/10
  5. Completeness           : X/10
  6. Anti-Regression Power  : X/10
  7. Brevity                : X/10
  8. Evidence Grounding     : X/10
  9. Consistency            : X/10
 10. Actionability          : X/10
────────────────────────────────
 Overall                    : X.X/10

Weakest dimensions: <list any <8, with 1-sentence suggested follow-up>
Next iteration if <8 avg: <what to improve before closing>
```

**Pass threshold**: overall ≥ 8.0 AND no single score < 6. If below, iterate on the draft (go back to Step 3) before committing.

### Step 7 — Log to UPGRADES.md

Append the full entry with: date, trigger, target, root cause, rule summary, full self-score, commit SHA (fill after commit).

### Step 8 — Commit

Use a conventional commit message tying back to the failure:

```
feat(<skill-name>): <general principle added, not the specific fix>

Root cause: <1 sentence, pattern level>
Trigger: <1 sentence, what user reported>

Score: X.X/10 (weakest: <dim>)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Do NOT commit if the user hasn't confirmed the upgrade OR if self-score < 8.0.

## 🧭 Decision Guide: Which file to edit?

| Failure nature | Edit target |
|---|---|
| Specialist produced wrong code quality | `plugins/.../agents/<specialist>.md` (frontmatter tools, or body instructions) |
| Specialist used wrong workflow (skipped CEO/PM) | `plugins/.../skills/work/SKILL.md` or `core/*.md` |
| Skill playbook missing a step / rule | `plugins/.../skills/<skill>/SKILL.md` |
| Hook failed to catch something | `plugins/.../hooks/scripts/<script>.sh` + `hooks/hooks.json` |
| Core role (CEO/PM/CTO/HR/BA) did wrong thing | `plugins/.../core/<role>.md` |
| Cross-cutting (multiple skills affected) | Edit each affected file + add a shared principle document if ≥3 skills |

If unsure, ask the user which layer the failure is at. Do not guess.

## 🪜 Upgrade Patterns (reusable lenses)

Use these lenses during Root Cause Analysis:

1. **Missing Enumeration** — agent considered only N of M things. Fix: require exhaustive enumeration with count verification.
2. **Missing Extraction** — agent guessed a value. Fix: require extraction via concrete API (`getComputedStyle`, `textContent`, `nodeList.length`) with citation in the output.
3. **Missing Verification** — agent acted without checking. Fix: add a post-condition check (side-by-side diff, count equality, regex validation).
4. **Weak Modality** — rule said "should" / "try to" / "prefer". Fix: upgrade to MUST / MUST NOT / hard ban with explicit penalty.
5. **Late Rule** — rule was in the skill but after the action point. Fix: relocate to a "⛔ READ FIRST" block.
6. **Hidden Rule** — rule existed but was inside a subsection an agent wouldn't load into context. Fix: promote to a top-level or starred section.
7. **Missing Escalation** — agent improvised when it shouldn't have. Fix: add explicit "ASK USER, DO NOT GUESS" escalation criteria + 2-3 offered options.
8. **Framing Drift** — skill's description/identity drifted into creative territory. Fix: reinforce the skill's role statement ("you are a forger, not a designer").

## 📏 Boundary Conditions

**When the user's report does NOT warrant a plugin upgrade** (surface these back to the user instead of editing):

- Failure was caused by the agent not following a rule that IS already clearly stated and correctly placed — that's an agent reliability issue, not a skill gap. Suggest the user escalate to the LLM or retry.
- Failure was caused by missing tool/MCP (e.g., no browser automation) — that's a setup gap, not a skill gap.
- User's expectation exceeds the skill's stated scope — either expand scope via a new skill or clarify scope in the existing skill's description.
- The reported behavior is actually correct per the skill's design — educate the user.

If you decide NOT to upgrade, log the decision in UPGRADES.md with reason (for future pattern detection).

## 📚 UPGRADES.md Entry Template

```markdown
## [YYYY-MM-DD] <skill-name> — <short title>

**Trigger (user report):**
> <verbatim or paraphrased user quote>

**Iteration count:** <1st report | 2nd repeat | 3rd+ repeat>

**Root cause:**
<2-4 sentences, pattern-level>

**Upgrade type:** [ added | strengthened | relocated | deleted-conflict | no-op-educated-user ]

**Files touched:**
- `plugins/vfm-agent-company/skills/<skill>/SKILL.md` (+N lines, −M lines)
- `plugins/vfm-agent-company/.claude-plugin/plugin.json` (version bump X.X.X → Y.Y.Y)
- `.claude-plugin/marketplace.json` (version bump)

**General principle added:**
<the rule, stripped of proper nouns>

**Verification mechanism:**
<the mechanical check embedded with the rule>

**Self-score:**
<paste the full 10-criterion block + overall>

**Commit:** <SHA, filled after push>
```

## Example Flow (reference, do not hardcode)

> User: "clone-website vừa clone section hero nhưng nó bịa thêm một cái badge 'New' không có trên web gốc"

1. **Triage**: skill = `clone-website`; input = (URL); failure = "added a `<Badge>New</Badge>` absent from source"; iteration = 1st report.
2. **Root cause**: generic pattern = "inventing UI elements absent from source". Existing skill has 11 hard bans including "Do NOT invent new sections" but at component-level (badge, chip, label) the ban was implicit. Rule too coarse-grained.
3. **Draft upgrade**: strengthen Hard Ban #1 to cover "sections, components, AND atomic UI elements (badges, chips, tooltips, labels, indicators)". Add verification: "Before writing a spec file, run a presence check — for every UI element in the spec, cite a source `querySelector` that returns non-null on the live DOM."
4. **Apply**: Edit `clone-website/SKILL.md` at the PRIME DIRECTIVE block.
5. **Version**: 1.0.5 → 1.0.6.
6. **Self-score**: 9.2/10 (weakest: Brevity 7/10 — rule added 4 lines; acceptable).
7. **Log & commit**.

## Closing Principles

- **You are not a firefighter, you are an architect.** You don't patch specific outputs; you evolve the blueprint.
- **Every upgrade should make the skill dumber-agent-safe** — a mid-tier LLM should be able to follow the upgraded skill without slipping into the failure mode.
- **Every upgrade should be auditable** — someone reading UPGRADES.md in 6 months should understand why each rule exists.
- **Never hardcode. Never.** When tempted, re-read the Litmus Test and rewrite.
