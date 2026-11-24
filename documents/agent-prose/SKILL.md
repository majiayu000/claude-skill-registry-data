---
name: agent-prose
description: "Use when creating or editing anything an agent reads: a skill, instruction file, packet template or agent doc. Not for docs written for people."
user-invocable: false
---
# Agent prose
Gate: get the user's OK before editing instructions that govern the agent itself (G3). See gates.md in the skill house-rules.
Job: Make any document an agent reads smaller and more reliable.
Takes: a draft.   Gives: a shorter document that behaves the same each run.

## Steps

1. **Weigh the two costs.** Text that loads every session is paid for on each turn. Text kept out of view is paid for in someone's memory, a price that only makes sense where a human should be doing the deciding. Choose how the document is reached:

   | Reach | Pays | Gets |
   |---|---|---|
   | Agent can reach it | Always-loaded text | Autonomy, reuse by other documents |
   | Only the user calls it | Relies on memory, and nothing else can call it | No context cost |

   Give a piece its own agent-reachable entry only if it has its own trigger or another caller. Reference used by two user-only items goes in a plain file. When user-only items multiply, add a single router that can recommend them and can't start them.

2. **Write the lines that lead elsewhere.** Whether an agent ever opens outside material depends on the in-context line that names it and says when to open it. When agents miss the material, rewrite that line, and pull the material inline only as a last resort. Cross-references use the forms ``Use the skill `<name>` `` and ``the file `gates.md` in the skill `house-rules` ``, because every host can follow those.

3. **Write the description.** Say what the thing is. Give one trigger for each case that is really different. Open on the most telling word, and drop whatever the body says anyway.

4. **Rank by urgency.** Put ordered actions first, then on-demand reference, and move everything else out behind one pointer line. What every path needs stays, and what only some paths need moves. Everything about one concept lives together, and each meaning has one home. Excess length is a fault in itself, however useful each line is.

5. **End each step in a finish condition** that can be checked and leaves nothing out: "every caller listed" beats "review the callers". Demanding complete coverage makes the agent dig further, and it works on flat reference too. With a loose condition agents hurry, more so when they can see what comes next. Tighten the condition first. If it can't be tightened and hurrying actually shows up, hide the following steps behind a true context break such as a fresh agent. An inline call resets nothing.

   Split a document only for a gain: by order, so agents don't run ahead, or by how it gets invoked. A merge puts later steps in view too soon.

6. **Choose words.** A single familiar word, used consistently, steers behaviour and triggering more firmly than a long phrase. A coined term has to be defined, which costs text, so look for an existing word first. Say what you want done, because a ban makes the banned idea more prominent. Save bans for hard guardrails and state the positive beside them.

7. **Cut.** Skip anything the agent can see for itself in scripts, config, folder layout or help text, unless finding it is expensive. Record what it can't see: unwritten conventions, reasons, gotchas. Re-check old lines too. Adding feels safe and deleting feels risky, so stale text accumulates. Remove any whole sentence the model would behave the same without.

8. **Run it.** Behaviour is the only real test. Give the document to a fresh agent on a real task and watch what it does. Settle any argument about a line the same way. If you can't run it, label the result `[untested]`. To show that a cut, rewrite or model swap changed nothing, follow the file `eval-run.md` in this skill.

## Done when

- Every step in the document ends in a checkable, exhaustive finish condition.
- Every pointer to outside material says when to read it, and every cross-reference uses an allowed form.
- Each meaning has one home, and no sentence is left that changes nothing.
- The description states what the thing is, with one trigger per distinct case.
- The document was run and the observed result is stated, or it is labelled `[untested]`.
- Any edit to instructions that govern the agent had the user's OK first.
