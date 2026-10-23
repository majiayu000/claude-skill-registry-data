---
name: documentation-adr
description: "Use when a significant architecture decision that is hard to walk back is taken: the ADR template, what belongs there rather than in inline docs, and the never-delete-always-supersede rule."
---

# documentation-adr

Step 3 of the pipeline (`WORKFLOW.md`, after `archi`), for any significant decision that is
expensive to undo: not for documenting every minor choice. Every rule below holds in a repo with
**nothing installed** (`CONVENTIONS.md`, rule A).

## When
After `archi` (3), as soon as a structural decision is taken (choice of a technology, of a
migration pattern, of a boundary between modules): never for a local, easily reversible choice.

**An ADR is not written unprompted.** A significant decision is *proposed* as an ADR — its six
fields, in the chat reply or the PR description — never *committed as a new file* on your own
initiative. Writing the file is triggered by one of: the user explicitly asks for it; the project
already has an established ADR practice (an existing `docs/adr/`-shaped folder, or a house
convention naming one); or the user accepts the proposal. A repo with a documentation policy that
treats an unsolicited doc file as a defect (`no-project-docs`-shaped: code and commit/PR messages
carry the explanation, not a prose file nobody asked for) is the default case to assume absent a
signal otherwise, not the exception.

**An applied override is recorded, not hidden.** Where a repo's own documentation policy governs, write what
it requires, and leave one short neutral trace addressed to whoever can decide (a line in the PR description,
the task summary or an ADR): which rule was overridden, by what, and that it is a resolved case. Never phrase
it as "a conflict between mentis and the house rules" to a non-technical stakeholder — that framing reads as
broken even when the case is a normal, resolved one, and has already caused a real project to get abandoned
and restarted over nothing. Raise one specific, named question to the decider only when no rule anywhere
actually resolves the case.

## Steps

**Read only the section the task actually needs.** The rules live one file per section under
`references/`; §1 decides which kind of document this is, §2 is the template, §3 applies when a
recorded decision changes, and §4 is the one sentence a held tension needs.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Tell the three types of documentation apart | before writing anything down | [`01-three-types.md`](./references/01-three-types.md) |
| 2 | The six fields, always the same | proposing an ADR, or reviewing a written one | [`02-template.md`](./references/02-template.md) |
| 3 | Never delete, always supersede | a recorded decision is changed, reversed or has stopped being true | [`03-supersede.md`](./references/03-supersede.md) |
| 4 | Say when a trade-off is permanent | the decision holds a tension rather than resolving one | [`04-permanent-tradeoff.md`](./references/04-permanent-tradeoff.md) |

## Output / checkpoint
Every significant decision from the `archi` step has its six fields **proposed**, in chat or the PR
description; an ADR **file** exists only where writing one was actually triggered (see `## When`),
and where it does, never a field left empty "to go faster" (§2.7).

## Guardrails
Don't write an ADR for a trivial/reversible choice: reserved for decisions that are expensive to
undo. **Don't create the file on your own initiative** — propose it, and let an explicit ask, an
existing ADR folder, or acceptance of the proposal be what actually creates it; a repo's own
no-unsolicited-docs policy, where one exists, wins over this block's default. **Never delete a record
and never edit a decision in place** (§3.1, §3.6). Stay publishable (rule C): an ADR contains no secret
and no client name, only the technical decision.

## Origin
A rewrite of a market generalist catalogue's `documentation-and-adrs` skill, with §4 reduced from a
market `preserving-productive-tensions` skill. The full provenance, the 2026-08-11 correction against
the real house documentation policy and the refresh log are in
[`references/origin.md`](./references/origin.md).
