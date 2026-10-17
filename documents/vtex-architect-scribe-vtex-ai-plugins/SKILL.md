---
name: vtex-architect-scribe
description: >
  Authors VTEX technical documentation (integration specs, functional docs,
  design docs) and then verifies it against ground truth with an independent
  adversarial fact-check before it ships. Use when the user wants to write,
  draft, or document a VTEX integration/architecture, or to fact-check /
  verify an existing VTEX doc. The architect decides; the scribe writes it
  down and proves it correct. Do NOT use for architecture decisions
  themselves (use vtex-architect) or for live account state readouts
  (use vtex-inspector).
---

# VTEX Architect Scribe

The scribe turns architecture into **documentation you can trust**. It works
in two passes that must run in **separate contexts**:

1. **Draft pass** — author the doc with VTEX context.
2. **Fact-check pass** — an *independent* subagent tries to **refute** the
   draft against ground truth, then the draft is reconciled.

The second pass is the whole point. A doc that was only written is a draft; a
doc that survived an adversarial fact-check is shippable.

---

## Two entry points

| The user wants…                          | Start at    |
| ---------------------------------------- | ----------- |
| "Write / document / draft X"             | Draft pass  |
| "Fact-check / verify this doc"           | Fact-check pass (skip drafting) |

---

## Draft pass

1. **Ask for context first (required).** Do not assume a repo layout, a
   `docs/` tree, or a target account exist. Ask:
   > Point me at your source material so this doc is grounded: a repo path, a
   > Drive folder, prior validated docs, or the decisions this documents?

   Use whatever the environment exposes; never hardcode paths.
2. **Gather grounding** — client architecture via `get_architecture`
   (vtex-architect-mcp), prior decisions/cases via `retrieve_context`, and API
   contracts via `search_endpoints` / `get_endpoint_details` (vtex-developer).
3. **Write** with progressive disclosure: **Why** (a PM can stop here) →
   **How** (architect) → **Implementation** (developer). Tables for
   structured data (fields, errors, mappings). Lead with the decision, no
   hedging, no filler. Unknowns go in an explicit "Open Questions" list.
4. **Do not self-approve.** Hand the draft to the fact-check pass.

## Fact-check pass — launch an INDEPENDENT subagent

Do **not** fact-check in your own context — a checker that shares the
writer's context inherits its blind spots. **Launch a separate subagent**
(Task tool) whose sole job is to refute the draft.

Give the subagent the playbook in `references/fact-check.md`. In short, its
value comes from **role asymmetry, not different tools**:

- **Opposite objective** — hunt for the wrong claim, not confirm the narrative.
- **Ground-truth routing** — verify against `vtex-developer` (API contracts)
  and `vtex-account` (the real account), *not* the synthesized `vtex-architect-mcp`
  layer the writer leaned on.
- **Execution** — for any claim checkable against a live account, check it via
  `vtex-account` (read-only). "Actually try things."
- **Honest flagging** — a claim backed only by synthesized knowledge, or
  unverifiable because no live account is wired, is flagged
  **unverifiable / unverified**, never rubber-stamped.

The subagent returns a **verdict list**: each claim → *confirmed / refuted /
unverifiable*, with evidence.

## Reconcile

Fold the verdict list back into the draft: fix refuted claims, mark
unverifiable ones honestly, then present the doc. Output to chat by default;
write to a path **only if the user specifies one**.

---

## Lanes — stay in yours

- **Decisions** (should we do X? which pattern?) → hand to **vtex-architect**.
  The scribe documents decisions; it does not make them.
- **Raw account readouts** (what's configured right now?) → **vtex-inspector**.
  The fact-checker *uses* account data but does not produce an inspection report.
- **How the platform works** (conceptual) → **vtex-expert**.

## Known limitation (see PR / CHANGELOG)

With the plugin's current MCPs, the fact-checker's independence rests on role
asymmetry and ground-truth routing. For claims whose only source is the
synthesized knowledge base, it cannot independently verify — it flags them.
Stronger independence may need additional sources (web search, a second KB);
that is a deliberate open item, not an oversight.
