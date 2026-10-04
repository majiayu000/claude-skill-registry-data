---
name: next-action-strategist
description: Chooses the single best immediate ChefFlow next action from current session, queue, context-window, dirty-workspace, research, and skill state. Use when the user asks "what should I do right now", "what next", "next move", whether to hand off/close, continue extracting research, queue work, groom, fire-prep, verify, or choose a skill.
user-invocable: true
---

# Next Action Strategist

Use this skill to answer a session-control question with one concrete recommendation. This is not an implementation skill. Its job is to prevent drift by choosing the safest highest-leverage next move now.

## Routing

1. Classify the request as session strategy, context triage, queue strategy, handoff decision, research extraction, verification closeout, or skill routing.
2. Apply always-on rules first: `AGENTS.md`, Build Queue First, dirty workspace protection, canonical dev server policy, and hard-stop safety rules.
3. Load `.claude/skills/omninet/SKILL.md` when present.
4. Load only the most specific additional skill if the recommendation depends on it: `close-session`, `pick-up`, `status`, `morning`, `warmup`, `feature-deepener`, `research-to-build`, `queue-groomer`, `completion-gate`, `live-browser-experience-audit`, or `prompt-builder`.

## Required Checks

Run or inspect, keeping output concise. If a command fails, report the failure and continue from available evidence:

```powershell
git status --short
node .agents/skills/build-queue/scripts/build-queue.mjs status
node .agents/skills/build-queue/scripts/build-queue.mjs domain-plan --status active
node .agents/skills/build-queue/scripts/build-queue.mjs workspace
```

Read only the files needed to judge current state:

- `AGENTS.md`
- `.claude/skills/omninet/SKILL.md`, if present
- `docs/.codex-workspace-brief.md`, if present
- `docs/session-log.md`, `.planning/HANDOFF.json`, or `docs/hermes/morning-report.md` when session continuity matters

## Decision Inputs

Judge the next action from evidence, not vibe:

- Context health: low context, compacted history, unresolved threads, unclear latest request, missing handoff, or stale session log.
- Workspace risk: dirty/untracked files, queue-file edits, generated artifacts, likely file collisions, or unclear ownership.
- Queue posture: active/in-flight/blocked counts, duplicate risk, domain-plan readiness, fired run status, and queue readiness.
- Proof posture: runtime evidence, tests, browser proof, console/network/server logs, finish-checks, and proof packs.
- Research posture: whether findings became goal, scope, acceptance criteria, risks, dependencies, and verification.
- Authorization posture: whether the user authorized queueing, firing, direct hotfix, read-only audit, or only decision support.
- Skill fit: the smallest current skill that can produce the next artifact without expanding scope.

## Decision Ladder

Choose the first matching recommendation that truly applies:

1. **Handoff and close** when context is low, the thread is fragmented, the next agent needs a clean start, or dirty workspace risk makes continuation unsafe.
2. **Verify and finish** when work is in-flight or code changed but runtime proof, tests, proof pack, finish-check, or browser evidence is incomplete.
3. **Block or recover** when there is a broken server, failed verification, missing auth/tenant proof, unresolved merge/file collision, or unclear ownership.
4. **Deepen/extract research** when there is valuable research, screenshots, transcripts, specs, or findings that have not been turned into acceptance criteria or queue-ready work.
5. **Groom or queue** when the idea is valuable but not implementation-ready, duplicates may exist, or queue priority/readiness is unclear.
6. **Fire-prep** when queue items are active, coherent, high-priority, and need run ID, context pack, file ownership, collision preflight, and verification plan.
7. **Continue focused work** only when context is healthy, workspace risk is understood, scope is already authorized, and the next step is obvious.
8. **Ask one question** only when a missing user decision would materially change the next action.

## Recommendation Labels

Use one exact label: `handoff-and-close`, `verify-before-done`, `block-and-recover`, `extract-research-to-queue`, `groom-or-dedupe-queue`, `fire-prep-only`, `continue-authorized-work`, `inspect-more-evidence`, or `ask-one-blocking-question`. Do not return a list of equal options.

## Calibration Gate

Before output, check evidence inspected vs inferred, 2-4 rejected alternatives, user-pressure/sycophancy risk, dirty-work/queue/proof/context/authorization risk, whether a smaller reversible step preserves optionality, and whether any files, queue IDs, skills, verification results, or certainty were invented. If the recommendation fails this gate, downgrade to `inspect-more-evidence`, `ask-one-blocking-question`, or `handoff-and-close`.

## Handoff Prompt Requirements

When recommending `handoff-and-close`, include a copy-paste handoff prompt with current objective, newest user request, what changed, dirty workspace warning, files touched by the current agent when known, queue status, in-flight/blocked concern, recommended first skill, exact first commands, preserve-unrelated-work warning, and the first decision the next agent must make.

## Output

Return a decisive answer in this shape:

1. **Current Situation**: 3-6 bullets grounded in observed repo, queue, skill, and session evidence.
2. **Best Next Action**: one taxonomy label plus one recommendation, stated plainly.
3. **Why This Beats The Alternatives**: compare against 2-4 plausible alternatives.
4. **Exact Next Prompt**: a copy-paste prompt for the next agent/session when useful, or `not needed`.
5. **Stop/Continue Guidance**: say whether to continue here, create handoff and close, queue, groom, fire-prep, verify, inspect more evidence, or ask one question.
6. **Confidence**: `high | medium | low`, one-sentence why, and one sentence naming what would change the recommendation.

## Guardrails

- Do not implement code.
- Do not create queue items unless the user explicitly asks to queue now.
- Do not fire work unless the user uses ChefFlow firing language.
- Do not invent queue IDs, files, skill names, or verification results.
- Mention dirty workspace risk when `git status --short` is not clean.
- Separate mandatory next action from useful-but-not-now expansion.
- If recommending handoff, include the handoff prompt requirements above.
- Be decisive but not overconfident. Challenge weak assumptions without flattery or forced agreement.
