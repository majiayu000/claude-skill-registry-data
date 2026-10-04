---
name: grill-me
description: Run a focused, evidence-backed interview to sharpen a plan, feature idea, design, or technical approach before implementation. Use when the user invokes grill-me, asks to pressure-test an idea, wants clarifying questions, or needs decisions walked through before code is written.
---

# Grill Me

Run a focused design interview. Completing the interview does not authorize implementation.

## Process

1. Identify the decision and subsystem in scope. Recover previous answers, accepted constraints, explicit deferrals, and delegated ownership from the conversation and relevant project records. Do not re-ask settled questions unless new evidence or the user reopens them.
2. Inspect answers discoverable from files, commands, docs, or repo state before asking. Distinguish verified reference facts, inferences, and proposals; do not present a proposed fixture or design as historical fact.
3. Ask concrete questions about unresolved requirements, risks, dependencies, and tradeoffs that affect the current decision. Keep questions within the owning subsystem; identify cross-system dependencies without silently deciding another owner's work.
4. Offer a recommendation and its reason when useful. A suggested or preselected option becomes a confirmed decision only when the user chooses it. Record deferral and uncertainty explicitly rather than filling them with defaults.
5. Follow a decision branch until it has an answer, explicit deferral, or inspectable fact. Stop when the requested plan is sufficiently specific or the user accepts the remaining uncertainty. Honor an explicit stop immediately.

## Output

Keep questions grouped and numbered, in short dependency-ordered batches. Use a question tool when available and appropriate. Carry answers forward between batches; avoid questionnaires whose later questions depend on unresolved earlier choices.

When enough is known, summarize:

1. Confirmed decisions
2. Open decisions
3. Implementation implications

Keep reference facts and recommendations labeled separately from confirmed decisions. If the user requested a durable decision record, update its existing authoritative location; otherwise summarize in the conversation without inventing another document.
