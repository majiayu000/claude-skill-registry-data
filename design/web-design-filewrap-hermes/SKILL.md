---
name: web-design
description: "Build a site through gated checkpoints and five judgers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, website]
    category: web
    related_skills: [telegram-rich-messages, telegram-widgets]
---

# Web Design Skill

Design and deliver a website through a fixed 30-stage pipeline with five judgers, human checkpoint gates, and executor-enforced budgets. Load-on-demand only: this skill never auto-loads. It covers websites and webapps (HTML/CSS/JS/TS) only — never mobile apps, branding, print, or general coding.

## When to Use

- The user asks for a website, webapp, landing page, or site redesign.
- The user asks to revise a site this skill already delivered (revision rounds, not a new run).
- Do not use for a mobile app, a logo or brand system, a print layout, or a general coding task — decline with a one-line redirect to the right lane.
- Do not use for a single-file fix or a quick snippet: the pipeline is for a site, not a patch.

## Prerequisites

- The user is admitted (owner or an admitted user); the load gate declines anyone else.
- The `web-designer` toolset is available in this conversation: `web_designer_start`, `web_designer_status`, `web_designer_approve`, `web_designer_stop`, `web_designer_judge`.
- Cards render through `telegram-rich-messages`; the preview entry rides the existing widget/local-viewer path (`telegram-widgets`). Never build a second browser or preview system.
- One active run per user/thread. A second run on the same thread is refused while one is active.

## How to Run

1. **Run the load gate.** Call `web_designer_start` with the request in the user's own words. It reports `started` with a `run_id`, or `declined` with a reason. A decline ends here — do not start the pipeline anyway.
2. **Drive the stages in order** (see Procedure). Before starting a stage, read its skills from `web_designer_status` (the `skills` field) and load each one with `skill_view` — the skill files live under `skills/web-design/<name>/` and the stage-to-skill map is `gateway/web_designer/skills.py`, which the machine reads. Load-on-demand only: a skill loads for its stages and never auto-loads, and no skill contacts the user directly — this coordinator is the only router. After each stage, checkpoint state before starting the next; never advance on uncheckpointed state.
3. **Pause at each checkpoint gate** and send the card. Resume only on an explicit human decision via `web_designer_approve` or a card tap.
4. **Judge, fix, re-judge.** All five judgers run over every build. A failure goes back into the fix loop; a repeated failure escalates to the user with the best passing version, never a silent delivery.
5. **Deliver preview plus handoff package.** There is no deploy target and no publish step in Phase 1.

## Quick Reference

Pipeline (30 stages, in order): load gate, intake, brief, scope freeze, research, IA, wireframe, copy, direction, font, colour, theme, icon, tokens, components, stack, build, preview, visual judger, a11y judger, performance judger, content judger, responsive judger, fix loop, checkpoints, delivery, checkpointing, rollback, revisions, routing/audit.

Checkpoint gates (pause, card, explicit decision): brief, wireframe + IA, design direction, pre-delivery preview.

Budgets (audit boundaries 5.1–5.10, 5.16, 5.29): 20 build iterations; 3 identical errors in a row; 3 no-progress iterations; 3 fix–re-judge cycles per issue; 120 minutes per build, 45 per revision round; 150,000 tokens per build (warn at 80%); $2.00 per build, $10.00 per day; 30 tool calls per run; sub-agent depth 2, fan-out 4; 2 revision rounds per deliverable; 200 files, 50 MB total, 2 MB per file.

Never-without-approval gates: publish/deploy, spend money, real user data and PII, contact third parties, DNS/domain/hosting changes, delete or destructive operations. Approval timeout (30 minutes) is a deny: pause durably, never proceed. The user's stop halts immediately — `web_designer_stop` is the kill switch.

## Procedure

### 1. Load gate and intake

The gate loads the skill only for a website/webapp request from an admitted user. Intake asks adaptive questions to understand the wanting, not just the words: what the site must do, for whom, and what success looks like. Cap clarification turns; decide cheap reversible choices alone.

### 2. Brief and scope freeze

Synthesise the brief and restate it back against the user's intent, not their literal wording: problem, audience, primary action, success measure, tone, non-goals. Send the brief card (Approve / Approve with changes / Reject). Freeze scope on approval: anything beyond the frozen brief is a change request, not a silent addition.

### 3. Research, IA, wireframe, copy

Research real inspiration and record provenance. Draw the information architecture (sitemap, flows, content model), then the low-fidelity wireframe, then the copy skeleton. The wireframe gate sends the wireframe + IA card for approval before any visual direction work.

### 4. Direction and decisions

Explore 2–3 named design directions and send the direction card; the user picks one, the others are dropped. The pick records the chosen direction on the run and approves the direction gate. Then decide, in order, by the coordinator's decision rules — never by free-form taste: font (at most two typefaces), colour, theme (light/dark and surface model), icon. Each decision is a card pick; the selected option is shown first with a clear selected state. A font, colour, or theme pick records the choice on the run for the agent to complete the stage — those stages have no checkpoint gate.

### 5. Tokens first

Define design tokens before building: primitive → semantic → component, three tiers, named by role not look (surface and text roles, never colour values). Tokens are the single source of truth; the build uses tokens only, never hardcoded values. Then inventory the components and choose the stack (TypeScript in scope) with a build plan.

### 6. Build and preview

Build from the tokens, components, and plan. Run locally and open the preview through the widget/local-viewer path. Record screenshots at 1440, 768, and 375 pixels. If no preview is available, say so plainly — never imply one exists.

### 7. Judge

Run the five judgers over the project dir with `web_designer_judge`, one per call: `visual`, `a11y`, `performance`, `content`, `responsive`. Each verdict is pass or fail plus exact findings plus the rules it could not check — never a silent pass.

Judger contracts:

- `visual`: geometry, layout, typography, colour, spacing. Rules live in `gateway/web_designer/rules.py` (R001–R110; R070/R071 are merged, R071 resolves to R070).
- `a11y`: WCAG 2.2 AA — 4.5:1 for normal text, 3:1 for large text and non-text. The accessibility gate blocks delivery.
- `performance`: budgets and Core Web Vitals — LCP at most 2.5s, INP under 200ms, CLS under 0.1 at the 75th percentile. The performance gate blocks delivery.
- `content`: copy clarity, honesty, no fake urgency or fake scarcity.
- `responsive`: behaviour across the 1440/768/375 viewports; breakpoints only where content breaks.

A finding names the rule, severity (blocker, defect, change, observation), location, expected versus actual, and evidence (screenshot path, file and line, or measured value). Rules a judger could not evaluate are listed as unchecked in its verdict.

### 8. Fix loop

Fix in priority order, capped and evidence-driven: at most 3 fix–re-judge cycles per issue, at most 3 identical errors in a row, at most 3 iterations with no change. A judger failure goes back through the loop; repeated failure escalates to the user with the best passing version.

### 9. Checkpoints and delivery

The preview gate sends the preview card before delivery. Delivery is the preview plus the handoff package: package contents, judger summary, known limitations and defects, and revision instructions. No deploy target, no publish button. After delivery, revisions take consolidated feedback only, at most 2 rounds, each under the 45-minute cap.

### 10. State and audit

Every run lives under the active profile home at `<home>/web-designer/<run_id>/`: `state.json` (the run record), `audit.log` (append-only, one line per stage, decision, and tool result), and `project/` (the site). A crash never silently resumes a run: an interrupted run is marked failed, and a resume starts from the last checkpoint, skipping completed stages. Use `web_designer_status` for run status, stage, budgets used, and last verdicts.

## Pitfalls

- Never skip a judger or report a pass for rules that were not evaluated — unchecked rules are listed, not hidden.
- Approve with changes needs the listed changes: pass them as `note` to `web_designer_approve`. A card tap alone cannot list them, so the tap asks the user to send the changes as a message instead.
- Never hardcode a font, colour, spacing, or size in the build; every value comes from the tokens.
- Never add scope after the freeze without a change request, and never ship a deploy or publish step — Phase 1 has no deploy path.
- Never present a probe or a single measurement as user-facing latency or a live result.
- Never resume a checkpoint gate on silence: a timeout is a deny, and the run pauses durably until the user decides.
- Never let a fix loop run past its caps; escalate with the best passing version instead.

## Verification

- The load gate accepted the request and one run id exists under the profile home.
- The brief, wireframe, direction, and preview gates each show an explicit recorded decision in `audit.log`.
- All five judgers ran; each verdict lists its findings and its unchecked rules, with no unjudged judger at delivery.
- Budgets hold: tokens, cost, tool calls, iterations, and file counts are all inside the caps in `web_designer_status`.
- Delivery contains the preview and the handoff package, with limitations stated and no deploy step.
