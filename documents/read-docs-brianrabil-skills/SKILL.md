---
name: plan-mode-read-docs
description: Read documentation for a named tool, API, version, or feature. Use when the user asks how a documented capability works, including setup, signatures, and limits.
license: MIT
---

# Read Docs

Extract the contract for the user's version and use case; avoid reciting a whole manual.

1. Identify the product, installed version, and feature. Read the supplied page or matching installed and official docs. Follow links that determine setup, parameters, behavior, or limits.
2. Verify the exact commands, signatures, defaults, and prerequisites against the relevant version. Use source code or examples to resolve ambiguity, but label behavior inferred from code separately from documented guarantees.
3. Explain the shortest working configuration or sequence for the user's case. Include a small example only when each part is supported by what you read; name the boundary where the docs stop.
4. Cite the specific pages or local files behind material claims. Finish when the user can apply the documented feature and can see which details remain unverified.

Reading docs is read-only. If the user asks for a comparison beyond the docs, use `plan-mode-research`; if they ask for implementation, handle that as a separate requested action.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
