---
name: woostack-design
description: Use when asked to design, prototype, redesign, visually refine, or review the visual and interaction quality of a UI, page, screen, or component.
---

# woostack-design

Coordinate UI design with the actual installed external skills. Own the brief, user decisions,
scope, and completion evidence; leave detailed design craft to the selected upstream procedure.
This skill requires no sibling Woostack workflow or source checkout. Its selected external stages
do require their installed skills; use the dependency boundary below rather than a substitute
craft manual.

## Request and authority

```text
/woostack-design Explore directions for our settings screen; do not edit production UI.
/woostack-design Implement the approved dashboard with Impeccable; keep changes local.
/woostack-design Review this dialog without edits.
/woostack-design Use Emil's animation guidance for this drawer only.
```

Review requests are read-only. Exploration produces proposals or explicitly authorized isolated
prototypes, not production rollout. Implementation or refinement authorizes bounded local edits
and relevant verification. Direction approval alone does not expand a proposal-only request.
Preserve unrelated work and existing components, tokens, architecture, and factual content unless
the requested change explicitly covers them. Prefer simplifying existing code over adding code
or dependencies.

Ordinary invocation does not authorize installation, upgrades, hooks, unrelated configuration or
document writes, branches, commits, pushes, issues, PRs, deployment, or Project changes. Keep
installation and publication permission separate from design permission. Missing documents or a
component catalog do not start Init or Design System. Arranging existing screen frames is a
separate task, not a reason to redesign their contents.

## Selected skills

| Stage | Selection |
| --- | --- |
| General UI design, implementation, or review | [Impeccable](https://github.com/pbakaus/impeccable) is the design lead. |
| A specific interaction, motion, prototype, or edge-case need | Select only the relevant skill from [Emil Kowalski's collection](https://github.com/emilkowalski/skills). |

State the selected skills and their purpose. Preserve the approved direction through specialist
work. A specialist-only request needs no general lead first. Do not load entire collections or
impose a sequence of audits.

### Dependency boundary

Before each selected external stage, use the host's skill discovery to identify the installed
skill and upstream source. Read its actual entrypoint and applicable procedure; verify required
references, scripts/assets, runtime, browser, and tool capabilities. Resolve paths from that
installation, not the Woostack checkout or remembered directory names. A raw prompt, a same-named
skill from another source, or metadata alone is not the required bundle.

If the selected dependency is missing, incomplete, incompatible, or disallowed, name the affected
stage and stop it. Ask for the specific installation or remediation using the host's supported
mechanism and current upstream installation instructions, or let the user explicitly proceed
without that stage. Reuse authorization already given; do not
repeat an installation offer after a decline. Install only the needed skills and assets, preserve
customizations, and verify availability afterward. Never silently install, upgrade, change hooks,
switch transport after a rejection, or claim a generic fallback used the missing skill.
Unselected specialists are not prerequisites; independent context gathering can continue.

Before invoking scripts or procedures, inspect their effects against the authorized scope.
Installation approval covers only the disclosed installation effects, not subsequent document,
configuration, network, binary-download, application-dependency, or publication changes. Existing
task and host permissions still govern ordinary execution. If upstream requires an out-of-scope
write, a conflicting design rule, or a nested skill, resolve that boundary before the action.
Use an upstream-supported scoped procedure, seek the necessary user decision, or report the stage
blocked. Do not skip required steps and claim full execution. Apply the same checks to nested
external calls; they never authorize sibling Woostack workflows or bypass host restrictions.

## Workflow

1. **Understand the experience.** Inspect the request, prior decisions, applicable repository
   instructions, relevant product/design documents when present, existing UI and component APIs,
   and preview capabilities. Establish the audience, primary task, surface type, desired character,
   scope, and preserved constraints in a short conversational brief. Ask only about material
   unanswered choices; do not repeat answers or impose a fixed questionnaire on a small refinement.
2. **Establish the direction.** Use the selected installed skill's appropriate planning or
   exploration procedure within the dependency boundary. Present the intended direction and scope
   before substantial implementation. For a genuinely unresolved choice, explore a small set of
   structurally different alternatives on one representative surface, using proposals or authorized
   isolated prototypes. Pause for user agreement before production integration or broad rollout.
   Reuse an already-approved direction; a narrow specified refinement needs no new exploration gate.
3. **Execute the bounded stage.** Invoke the actual selected skill through the host's supported
   mechanism with the concrete target, brief and prior answers, approved direction, allowed writes,
   verification needs, and stopping point. Follow its applicable procedure and necessary resources,
   not a copied summary or a bare skill name. Upstream instructions cannot expand authority. Keep
   specialist edits scoped and preserve the lead's direction. Do not repeat a questionnaire or
   audit when applicable answers/evidence already satisfy it. Remove only task-owned exploration
   scaffolding after authorized promotion unless retention is requested. Add no coordinator-specific
   subagent sequence or concurrent competing design writers.
4. **Inspect and refine.** Inspect the rendered result and exercise changed interactions at relevant
   viewport sizes with realistic content and necessary states. Check applicable keyboard/focus,
   accessibility, touch/mobile, reduced-motion, and content-extreme behavior. Reuse relevant upstream
   and project-native checks rather than duplicating full audits. Critique against the approved
   brief, keep findings separate from fixes, apply only authorized corrections, and recheck affected
   behavior. Fix substantive defects without an indefinite subjective-redesign loop. A read-only
   finding authorizes no edit. Automated accessibility checks are partial evidence; screenshots
   cannot prove interaction or motion correctness. When runtime/browser evidence is unavailable,
   report the gap and complete only useful authorized work without claiming verified completion.
5. **Report.** Name the lead and specialists actually used, the agreed direction, the produced or
   changed scope, checks and interactions actually observed, and missing, skipped, or blocked stages.
   Distinguish proposals, prototypes, implementations, and verified implementations. Do not attribute
   work to a skill that did not run or claim better visual outcomes without evidence. The endpoint
   is the requested result or local changes; publication needs a separate explicit request.
