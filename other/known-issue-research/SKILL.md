---
name: known-issue-research
version: "1.2.0"
user-invocable: false
description: "External-research routing for confirmed code problems: triage whether the root cause is internal / external / hybrid, run a known-issue quick search before deep root-causing (platform silent failures, nested host runtimes, no code-level suspects), and evaluate industry-wide hard limits. Delegates all WebSearch discipline to effective-web-research. Referenced by PDCA hosts via frontmatter dependencies; load during the technical-analysis stage. Do NOT use for competitor product-behavior, interaction-boundary, or mechanism observation (competitive-research)."
dependencies:
  - effective-web-research
---

# Known Issue Research

> Internal shared skill for the technical-analysis stage of code-fixing workflows. Decides **when a confirmed problem needs external web research before (or instead of) deeper code-level analysis**, and how to act on the results.
>
> **Prerequisite check**: this skill declares `effective-web-research` in frontmatter `dependencies`. On load, verify it is available; if missing, abort and print the install command (`npx skills add FuDesign2008/open-skills -g`). No silent fallback.

## Step-number parameterization

This skill is shared by workflows with different step numbering. All jump targets below are written as placeholders — `{impact-assessment step}`, `{root-cause step}`, `{upstream-eval step}` — and the referencing workflow states its own numbering inline at the reference line (e.g. "jump to step 4"). Never hardcode a workflow's step numbers here.

## 1. Research routing triage

Run immediately after the problem's existence is confirmed. Decide which class the root cause most likely falls into — this adjusts the **priority** of later steps, never replaces them:

| Route | Signals | Emphasis |
|-------|---------|----------|
| 🟢 Internal-first | About "our code/logic/conventions"; root cause suspected in this repo | Code location first; quick search (§2) as optional fallback; root-cause analysis is the core |
| 🔵 External-first | Named third-party lib/framework/API + version; or "how to use / why / any known issue"; or any §2 trigger hits (platform silent failure / nested host / no code-level suspects) | Quick search (§2) becomes the **primary action** — search known cases first |
| 🟣 Hybrid (external-then-internal) | External concept + internal object ("does the X lib we use have vulnerability Y", "apply pattern X to our code") | §2 first to understand the concept externally, then internal root-cause analysis to apply it |

When unsure, default to **🟢 internal-first** (these workflows exist to change code; most root causes live in the repo).

> Relation to `effective-web-research` Step 0: that triage decides whether a *single search* should go external; this one decides the *whole problem's* research composition. Complementary — consult its Step 0 when unsure.

## 2. Known-issue quick search

**Triggers** (any one; in 🔵/🟣 routing this is the primary action, in 🟢 an optional fallback before instrumenting code):

- Platform/native component involved (Android WebView, iOS UIPickerView, browser API, OS-level control…) with a **silent failure** — no error, no crash, correct calls, completely unresponsive behavior.
- **Nested host runtime** (React Native, Electron, Cordova, WebView-in-App…) while the frontend logic looks entirely correct.
- **No code-level suspects**: call chain complete, parameters correct, logs show execution — yet it doesn't work at runtime.

**Execute**: WebSearch with "symptom keywords + platform/framework + year" across StackOverflow, GitHub Issues, official docs. **Parallel action** (mandatory when a named third-party lib/framework is involved or symptoms correlate strongly with platform-specific behavior): check the upstream dependency's Changelog / Release Notes / Issues for an already-fixed version — upgrading may be the simplest fix (hand off to the workflow's `{upstream-eval step}`, which delegates to `upstream-dependency-debug`).

**Result handling**:

| Outcome | Action |
|---------|--------|
| ✅ Known case found, root cause clear | Output the quick-search conclusion; jump to the `{impact-assessment step}`, skipping root-cause analysis |
| ✅ Upstream fix version found | Output the lead; proceed to the `{upstream-eval step}` to assess upgrade feasibility (a fixed-upstream lead is not yet a solution) |
| ⚠️ Related discussion, root cause partly clear | Feed findings into the `{root-cause step}` as reference |
| ❌ Nothing found | Skip silently; continue to the `{root-cause step}` |

### 2.1 Performance-pattern variant (for perf-optimize-workflow)

When the referring workflow is performance analysis (`perf-optimize-workflow`), treat §2 as a **known performance-pattern quick search** with these extra triggers (any one, before entering that workflow's hypothesis stage):

- Anomaly located but **cannot be classified** into the workflow's known performance-pattern table
- Suspected **framework/library performance bug or limit** (named framework + version)

**Execute** the same WebSearch discipline as §2, with query shape: `symptom + framework/lib + version + year`, preferring GitHub Issues, official changelog, StackOverflow.

| Outcome | Action |
|---------|--------|
| ✅ Known case / version bug | List the known fix as a candidate solution; focus later hypothesis validation on that direction |
| ⚠️ Related discussion, inconclusive | Feed into hypothesis directions |
| ❌ Nothing found | Skip silently; continue the workflow's next stage |

`perf-optimize-workflow` keeps its pattern table and stage orchestration; this subsection only owns the search methodology.

## 3. Industry-wide issue evaluation

**Trigger** (optional, pessimistic branch): the root cause clearly points to a hard platform / language / protocol / standard limit (e.g. browser security policy, JS single-threading, protocol constraints) with no obvious application-layer workaround.

**Execute**: WebSearch — is this a recognized industry-wide problem? How do mainstream frameworks / major companies handle it? Does any viable workaround exist?

**Result handling**:

| Outcome | Action |
|---------|--------|
| 🚫 Recognized hard problem, no viable solution | Output the evaluation report (template in [reference.md](reference.md)) and **pause for the user's decision** (explore workarounds / accept as-is) |
| ⚠️ Limited but workarounds exist | List workarounds as candidates in solution exploration; continue |
| ✅ Not industry-wide, a fixable problem | Continue to the `{impact-assessment step}` |

> Distinction from §2: §2 searches known cases *by symptom* ahead of root-causing (applies whether or not a solution exists); §3 evaluates *after the root cause is clear* whether the industry has a recognized solution (for the no-solution scenario). They never overlap.

## WebSearch discipline

All WebSearch execution in this skill follows `effective-web-research`: first its Step 0 triage (confirm the question is external, not solvable from the repo), then its 4 maxims (authority-first / currency check / cross-validate non-trivial claims / skip content farms); when the user demands rigor, switch to its strict mode and produce a report. Read that skill's current doc before searching — never from memory.

## Integration guide (for referencing workflows)

- **Declare** this skill in frontmatter `dependencies`; abort at startup if missing.
- **Reference line must state**: your step-number mapping for the placeholders above, and which of your steps §2/§3 slot into.
- **Keep your semantic variants in your own body** — e.g. jira-fix-workflow: §3 is a gate (not optional), a 🚫 outcome stops the flow and writes a Jira comment, and its report template lives in its own reference.md.
