---
name: improve-codebase-architecture
description: Audit a codebase or subsystem for architecture simplification - shallow or pass-through modules, scattered concepts, naming drift, sibling workflows that disagree, weak test seams. Use when the user asks what to simplify or restructure. Not for a narrow fix or for implementing an already chosen design.
---

# Architecture audit

Goal: less effort to use, change, and debug the code, with required behavior preserved. Fewer files or lines is not by itself an improvement.

1. Establish the need first. Read callers, docs, ADRs, tests, and history before judging a mechanism; code that looks redundant may encode a domain rule.
2. Look for:
   - One rule implemented in two places that disagree, especially across languages or processes (a pre-check here, an enforcer there). Name the inputs on which they diverge.
   - Sibling paths (create/update, push/PR, CLI/API) whose names, owners, validation, or failure handling differ without a domain reason. Keep asymmetries the domain justifies.
   - Shallow modules whose callers must know their internals (protocols, sentinels, ordering). Deepen; do not split.
   - Deletion test: if a module were removed, would its responsibility vanish or move into callers? Name what would move.
3. Avoid: new interfaces or ports with one implementation, merging code that changes for different reasons, rewrites, cosmetic renames, invented metrics.
4. Report a few ranked candidates, each with file:line evidence, the concrete friction, the change, its migration cost, and the test that pins current behavior. "Keep as is" and "insufficient evidence" are valid results. Write in the project's own vocabulary, not architecture jargon.
5. Stop at recommendations unless the user selected a candidate to implement.
