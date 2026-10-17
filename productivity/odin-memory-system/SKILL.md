---
name: odin-memory-system
description: Orchestration doctrine for the user-triggered operations that write to Yggdrasil Memory — Remember (promotion), Dream (consolidation), Forget (deletion).
---

# Memory System

## Purpose

Define the orchestration doctrine for the three command-triggered Yggdrasil Memory operations — Remember (promotion), Dream (consolidation), and Forget (deletion). Each operation is an orchestrated, reviewed pipeline that dispatches to specialists; this skill specifies the agent roles, review gates, and guardrails for each.

The write-side implementation — entry schema, directory structure, canonical templates — is owned by the `brokk-memory-curation` skill, which Brokk itself loads. Keep dispatch briefs at the orchestration level: name the operation, the inputs, and the scope; do not restate or invent implementation details.

## When to Use

- **Remember** — when a Yggdrasil Memory-promotion command (`/yggdrasil/remember`) or an equivalent natural-language request ("remember this finding") is received.
- **Dream** — when a Yggdrasil Memory-consolidation command (`/yggdrasil/dream`) is received, or when you proactively suggest consolidation to the user (e.g., after a subagent reports a contradiction with an `active`-status Memory entry).
- **Forget** — when a Yggdrasil Memory-deletion instruction is received, whether via the `/yggdrasil/forget` command or natural language, naming an explicit scope.

All three operations presuppose an existing knowledge base. **Fail-safe establishment:** If `.yggdrasil-memory/` is absent at the session working directory root when a Yggdrasil Memory command is invoked, inform the user and offer to establish it (scaffolded by Brokk per the `brokk-memory-curation` skill's canonical templates) before any write operation proceeds.

## Workflow

### Remember (promotion)

A user-triggered operation — initiated only by explicit user request via the `/yggdrasil/remember` command or an equivalent natural-language request; **never launched automatically at task wrap-up**. Only reviewed research is eligible.

1. If a subject is given, promote that finding/topic/Workfile. If the subject is empty, identify durable findings from the current task's reviewed research, propose the promotion list to the user, and proceed only on approval.
2. Task Brokk to distill the Heimdall-passed findings into Yggdrasil Memory entries, citing sources.
3. Heimdall reviews the Yggdrasil Memory write before it is final.
4. **Never promote secrets or credentials.**

### Dream (consolidation)

A user-triggered maintenance task, invoked via the `/yggdrasil/dream` command or an equivalent natural-language request. An optional focus scope (topic, area, or subset of entries) may narrow the audit; when omitted, the entire knowledge base is audited:

1. Task Mimir to audit the knowledge base for duplicates, contradictions, and staleness, re-verifying claims against current sources.
2. Heimdall reviews the audit before any action is taken on it.
3. Task Brokk to consolidate per the reviewed audit — merge, prune by reviewed judgment, or reorganize as warranted.
4. Heimdall reviews the resulting Yggdrasil Memory diff for fidelity before it is final.
5. Dream prunes by reviewed judgment but never silently performs a forget — deletion of user-named scope is a separate, explicitly confirmed operation.

### Forget (deletion)

Explicit user instruction — via the `/yggdrasil/forget` command or natural language — naming a scope. Never autonomous; never chains from another operation.

1. If the scope is empty or ambiguous, do **not** proceed — ask the user to name an explicit scope (topic, staleness filter, or full wipe).
2. Resolve the scope to the exact list of entries affected, present that list to the user, and obtain explicit confirmation before any deletion is dispatched. The command invocation is intent, not confirmation.
3. Task Brokk to delete exactly the confirmed scope.
4. Heimdall reviews the diff for exact-scope fidelity before it is final.
5. **Never commit the deletion** — leave it in the working tree; committing is the user's act.
6. Full wipe requires a second, explicit user confirmation — if your Communication Policy does not permit asking the user questions, the wipe cannot proceed.

## Quality Criteria

- **Only reviewed research is eligible for promotion.** No entry is written without a distinct upstream reviewed Workfile backing it.
- **Every write is reviewed.** Promotion, consolidation, and deletion each pass through a Heimdall review gate before they are final.
- **Never promote secrets or credentials.** Entries are git-tracked by default and visible in diffs.
- **Forget is always confirmed.** The exact list of entries to be deleted is presented to the user and explicitly confirmed before any deletion is dispatched.
- **Never commit deletions.** Changes are left in the working tree; committing is the user's act.
- **Dream never silently forgets.** Deletion of user-named scope is a separate, explicitly confirmed operation (Forget), not a side effect of consolidation.
- **Full wipe requires a second, explicit user confirmation — if your Communication Policy does not permit asking the user questions, the wipe cannot proceed.**

## Anti-Patterns

- **Auto-launching Remember at task wrap-up.** Promotion is user-triggered only. Never launch the pipeline without explicit user request.
- **Chaining Forget into Dream or any other operation.** Dream prunes by reviewed judgment; Forget obeys explicit, confirmed instruction. Keep the semantics separate. Never silently delete entries as a side effect of Dream.
- **Committing deletions.** Forget leaves changes in the working tree. Committing is the user's act, never the agent's.
- **Promoting without a reviewed source.** No entry may be created or modified without a distinct upstream reviewed Workfile backing it. If you are tempted to write something without a reviewed source, it does not belong in Yggdrasil Memory yet.
- **Expanding Forget scope beyond what was confirmed.** Delete exactly the confirmed list, nothing more. Never infer "related" or "probably stale" entries to delete alongside the confirmed scope.
- **Skipping the review gate.** Every write operation — promotion, consolidation, deletion — must pass through Heimdall review before it is final. No exceptions.
