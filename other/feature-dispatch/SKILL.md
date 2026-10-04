---
name: feature-dispatch
description: Watch the user's most recent message for non-trivial feature work and recommend the right entry into the feature-* chain (/feature-storm or /feature-design) before any code is written. Use proactively when the user describes a new capability, system, or feature whose first-cut implementation would plausibly exceed ~75 lines of code. Recommend /feature-storm when the requirement is vague or high-level and still needs scoping at the product layer (goals, users, success criteria, rough technical direction). Recommend /feature-design when the user is relatively clear on what they want but the work still needs a proper technical design (data model, interfaces, dependencies, failure modes) before code lands. Skip silently for small bug fixes, single-function additions, refactors, renames, doc edits, dependency bumps, config tweaks, or anything the user explicitly framed as a quick / throwaway / spike change; skip when the user already typed /feature-storm, /feature-design, /feature-plan, or /feature-implement; skip when work is already in flight inside a feature-* chain or a /bug-* skill. Routes via a single AskUserQuestion call with three explicit options (recommended skill, alternative skill, continue without dispatch) and on selection hands over by invoking the chosen skill via the Skill tool.
user-invocable: false
disable-model-invocation: false
allowed-tools: AskUserQuestion, Skill
---

# feature-dispatch — Route feature-shaped prompts into the right entry skill

You are running the `feature-dispatch` skill. You were invoked proactively because the user's most recent message looks like a feature request that is non-trivial enough to warrant scoping or design before any code is written. Your only job is to **recommend** the right entry into the feature-* chain (`/feature-storm` or `/feature-design`) and, if the user accepts, **hand over** to that skill via the `Skill` tool. You do not read files, write files, run commands, or do any work yourself.

If at any step below you decide this prompt does **not** in fact warrant dispatch (e.g. it's small, it's a bug, the user already chose an entry skill, or work is already in flight), stop the skill silently and let the parent conversation continue. Do not announce that you considered dispatching.

This skill has four steps (Steps 1–4). Execute them in order.

## Step 1 — Confirm the prompt is in scope

Re-read the most recent user message. **Stop the skill silently** (no chat output, no `AskUserQuestion`, no `Skill` call) if any of the following holds:

- The user already typed a slash command for the feature-* chain (`/feature-storm`, `/feature-design`, `/feature-plan`, `/feature-implement`) or for the bug workflow (`/bug-submit`, `/bug-fix`) — that explicit choice wins.
- The conversation is already in flight inside a feature-* chain (a stage file was just written, a chain-in offer was just made, or the most recent assistant turns are clearly executing one of those skills).
- The request is a bug, defect, regression, or production incident — that belongs in `/bug-submit` or `/bug-fix`, not the feature chain.
- The work is plainly small: a rename, a one-line fix, a typo, a doc-only edit, a single-function addition, a dependency bump, a config tweak, or any refactor where the user named the exact target.
- The user explicitly framed the work as quick, throwaway, exploratory, or one-shot ("just hack it", "quick script", "throwaway", "don't overthink it", "spike", "experiment", etc.).

Otherwise continue to Step 2.

## Step 2 — Estimate scope and pick a recommendation

Estimate, **silently** (do not narrate, do not enumerate files in chat), how many lines of code a competent first-cut implementation of the user's request would take. Round to the nearest plausible bucket.

- **< ~75 LOC** → stop the skill silently. The work is small enough that dispatching adds friction.
- **≥ ~75 LOC** → continue.

Now decide which entry skill to recommend:

- **Recommend `/feature-storm`** when the requirement is **vague, high-level, or under-specified at the product layer** — goals, users, scope, success criteria, or rough technical direction are not yet clear. Typical signals: aspirational phrasing ("we should have a way to…", "it'd be cool if…"), naming a problem rather than a solution, multiple plausible interpretations, no explicit user or use-case, or the user asking for ideas.
- **Recommend `/feature-design`** when the requirement is **relatively clear at the product layer but still needs a real technical design** before code lands. Typical signals: the user names a concrete capability and a rough shape, but key technical decisions are still open (data model, interfaces, dependencies, failure modes, security/privacy, performance budget, integration points).

Record your choice as `recommended` and the other as `alternative`. Also draft a one-line restatement of the user's request that you will paste into the question so the user can correct your reading in the same step.

## Step 3 — Offer the choice via `AskUserQuestion`

Call `AskUserQuestion` **exactly once**. Order the options so the recommended skill appears **first** and is clearly marked. Both feature skills appear as concrete options; the third explicit option lets the user continue the parent conversation without dispatching.

- **question**: `"This looks like non-trivial feature work for <one-line restatement>. Want me to route into the feature-* chain?"` — replace `<one-line restatement>` with the paraphrase from Step 2.
- **header**: `"Route this feature?"`
- **multiSelect**: `false`
- **options** (order matters — the recommendation must be first):
  - `{ "label": "Run /<recommended> (Recommended)", "description": "<one-sentence reason this is the better fit for this request>" }`
  - `{ "label": "Run /<alternative>", "description": "<one-sentence reason you might prefer this instead>" }`
  - `{ "label": "Continue without dispatch", "description": "Skip the feature chain and handle this in the current conversation." }`

Substitute `<recommended>` and `<alternative>` with the actual skill slugs from Step 2 (`feature-storm` or `feature-design`). Do not invent a fourth option — `AskUserQuestion` already appends "Other" automatically.

## Step 4 — Hand over

Based on the user's selection:

- **Recommended skill picked** → invoke that skill via the `Skill` tool with the user's original request as the single argument (a faithful short paraphrase is fine if the original is very long). Stop immediately after — the target skill owns the rest of the conversation.
- **Alternative skill picked** → invoke it the same way.
- **"Continue without dispatch" picked** → stop the skill silently and continue the parent conversation normally. Do not summarize, do not restate the question, do not apologize for asking.
- **"Other" picked** → treat the user's free-text as the new request and stop the skill silently; the parent conversation handles it. Do not loop back into Step 1.

## Constraints (non-negotiable)

- **Never write files, never run commands, never modify state.** This is a pure router. Your only side effects are the `AskUserQuestion` call in Step 3 and the `Skill` invocation in Step 4.
- **At most one `AskUserQuestion` per invocation.** If the user declines, do not retry, re-frame, or follow up.
- **Do not call `lessons-capture`.** This is a light routing skill on the same tier as the other internal helpers; reflection overhead isn't worth it for one question.
- **Honor the silent-skip rules in Step 1.** Dispatching the wrong prompt is worse than not dispatching at all — false positives erode trust in the router.
- **Do not chain past the handover.** Once you invoke the target skill in Step 4, you are done; that skill (and any further chain-in it offers) takes over.
