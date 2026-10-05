---
name: preflight
description: Run the deterministic readiness check on an intent spec before an agent builds against it. Six calibrated gates, computed by pure functions — no model judgment, same spec always gets the same verdict. Use before implementing an intent, before handing a spec to another agent, or whenever the user asks "is this spec ready?".
---

<what-to-do>

Call the `check_intent_readiness` MCP tool (Pathmode). With no arguments it resolves `intent.md` from the MCP client's declared workspace roots or the server launch directory: the file at the repository root, or, when there is none, the single `intent.md` in an `intent/` folder. When `intent/` holds several, it refuses and lists them; ask the user which one, then pass it as `path`. If that repository has no `intent.md`, or the repository cannot be identified, it refuses instead of substituting a workspace or local "current" intent. Pass `spec` inline to preflight a draft before saving it, or `intentId` when the user deliberately selects a specific saved intent.

In connected mode, when the repo-bound file carries a cloud id, check for PM judgment before implementation: call `list_intent_change_requests` with that id. For every open request, call `get_intent_change_request`, apply the requested field/item change deliberately to `intent.md`, and call `intent_save` with the request's exact `changeRequestId` and `baseRepoBodyRevision`. A decisions or product-choice request is applied by the server exactly as written, so save it with no other edits. If the request is unworkable, call `reject_intent_change_request` with a concrete reason instead of pretending it was applied. After an applied request, re-run the readiness check, report that the new repository revision is pending human authorization, and STOP. Do not begin implementation until a later `get_agent_prompt` confirms that the exact current revision is authorized by a signed-in product manager.

Show the user the verdict block exactly as returned — the blocker strings are the calibrated gate output, do not paraphrase them.

If the verdict fails: repair, one blocker at a time. For each failing gate, ask the user ONE targeted question, and propose your best-guess answer from the spec and the codebase so they can correct rather than compose. Apply the agreed fix to the same authority you loaded: when `intent.md` exists, call `intent_save` (it also syncs in connected mode); only use `update_intent` when no local file exists. Then re-run `check_intent_readiness`. When you read the codebase to propose an answer, keep what you learned: pass it to `intent_save` as `implementationContext`, or call `record_implementation_context` for a cloud-only intent. It does not affect the verdict, and it saves the implementing agent from rediscovering what you just read. Stop when the verdict passes or the user explicitly accepts a named gap.

If the verdict passes: say so and stop. Do not invent extra requirements beyond the six gates.

</what-to-do>

<supporting-info>

## What the six gates check

1. **Title** — a short, specific noun phrase, not a placeholder or generic label ("Bulk edit" passes; "New feature" fails).
2. **Objective** — names an actor and a concrete problem or capability; rejects buzzword-dressed vagueness with no number.
3. **Outcomes** — at least two, and at least two-thirds measurable: a threshold, an observable capability, or a concrete state change. "Users are happier" fails.
4. **Constraints** — at least one violable statement, something an implementation could actually break ("Never double-charge on retry"). Bare adjectives fail.
5. **Edge cases** — at least one scenario with a defined expected behavior.
6. **Verification** — at least one check concrete enough to run without asking the author.

## Why deterministic matters

The gate is pure functions over the spec text: no model call, no network. Re-running never changes the verdict unless the spec changed. That makes it a floor you can put in front of any implementation work — and it means a passing verdict is reproducible evidence, not an opinion. The same gate runs live at preflight.pathmode.io.

Every `intent_save` also stamps the verdict into the file's frontmatter as `readiness:` ("passed 6/6", or "failed N/6" with the blocking gates named), so anyone reading intent.md — human or agent — sees the gate state without re-running anything. A failing verdict never blocks the save; the gate reports, the user decides.

A saved intent can also carry product choices its brief proposed and no human has resolved. Those are not one of the six checks: the verdict reports them separately ("⛔ Not ready to hand to an agent: N product choices still unresolved"), the frontmatter appends "— blocked by N unresolved product choice(s)", and `get_agent_prompt` in execute mode says do not implement. A recommendation attached to an open choice is an assumption. With a workspace connected, ask the product manager to resolve or explicitly exclude it in Pathmode; do not resolve it from the repository. Without one (keyless), ask the person about each open choice, recommendation first, and record each explicit answer with `answer_product_choice`, quoting their words for that choice. A blanket "go with the recommendations" answers none of them. The verdict then reads "answered locally (unverified)": a faithful record of the conversation, not verified approval.

## Division of labor with the other skills

- `preflight` — deterministic verdict: IS the spec ready? Cheap, run it first and often.
- `grill-intent` — adversarial model-driven review: is the spec WISE? Run it when preflight passes but the stakes are high.
- `compile-intent` — builds a spec from a vague problem. Preflight what it produces.

</supporting-info>
