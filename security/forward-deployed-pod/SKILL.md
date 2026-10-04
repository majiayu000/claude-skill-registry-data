---
name: forward-deployed-pod
description: Use to review the output of any GOAL phase (a Goal Brief, a spec, a diff or PR, an eval report, a release plan, or telemetry) from four forward-deployed perspectives at once. Convenes a pod of four persona-agents (FD Product Manager, FD Tech Lead, FDE, FD Domain Expert/Business Owner), auto-selecting which lenses matter for the current phase (read from .goal/state.json), and returns one synthesized Pod Review with a verdict and a queue of proposed actions. The pod advises; the human decides and holds the gate. Use when the user asks for a pod review, a multi-perspective review, or to review a phase's work, and at GOAL phase gates.
---

# Forward Deployed Pod

A forward-deployed pod, made of four persona-agents, reviews the current phase's work from four perspectives at once, so no single class of failure slips through. It is the **think** layer: the pod reasons and recommends. The human decides and holds the gate. It never merges, ships, or acts on its own authority (agency-design Level 1 to 2, never Level 3). It is the concrete multi-perspective verifier that `agency-design` points to: several advisor lenses check the work before a human looks, then batch to a single verdict and the one highest-leverage fix.

## What to do

1. **Find the phase and the target.** Read the current phase from `.goal/state.json` (`{ "phase": "...", "project": "..." }`). If it is missing, ask the user which phase applies, or default to all four lenses. Identify the target under review: a Goal Brief (Discover), a spec (Specify), a diff or PR (Build), an eval report (Evaluate), a release plan (Deploy), or telemetry and traces (Learn). If the user named an artifact, use it.

2. **Convene the lenses.** Read `references/phase-lens-matrix.md` and select the lenses for the phase. Scale to the stakes: a trivial, reversible change may convene only the lead lens, or skip the pod. Do not run four heavyweight reviews on a one-line change.

3. **Dispatch the convened lenses in parallel.** For each convened lens, dispatch a subagent with that role's prompt from `references/roles/` (product-manager.md, tech-lead.md, fde.md, domain-business.md) and the target. Run them independently so no lens anchors another.

4. **Synthesize.** Merge the findings: deduplicate overlaps, surface disagreements between lenses as explicit tensions (do not average them away), and order by severity (blocker, then important, then minor).

5. **Turn findings into proposed actions.** For any finding that implies doing something, emit an ActionRequest following `references/action-seam.md` (the reference implementation is `seam/action_seam.py`): set the action, target, rationale, reversible, stakes, and action_class (deterministic or real_world). The pod proposes; it does not execute. Deterministic actions are carried out later by the agent's own tools (Bash, Edit), gated by the permission prompt; real_world actions need an external action runtime (for example Computer Use or a browser MCP) and are surfaced for the human, not run here. Gate everything real-world, irreversible, or above low stakes for human approval, and record every proposed action in the audit.

6. **Write the Pod Review.** Fill `references/pod-review-template.md`, save it as `pod-review.md` in the working project, and show it to the user. The verdict (ready, ready with fixes, or not ready) names the single highest-leverage fix. The proposed-action queue lists each action with its stakes, class, handler, approval status, and result.

## Self-check before you finish

Check the Pod Review against this rubric, and fix anything that fails:

- Every convened lens produced findings.
- Disagreements are surfaced as tensions, not hidden or averaged.
- The verdict names one highest-leverage fix.
- Every proposed action carries stakes, reversibility, class, and approval status.
- Every high-stakes, irreversible, outbound, or real-world action is gated for human approval.
- The review is advisory: no action was taken on the pod's own authority.

## Scope to the stakes

Full pod at high-stakes gates (a Discover decision, a spec, a release, an eval verdict). A subset or a single lens for a small, reversible change. The failure mode to avoid is approval-of-everything, which turns the pod itself into the constraint.

See `references/examples/jobmate-distractor-filter.md` for a worked run across all six phases, including where an external action runtime is needed.
