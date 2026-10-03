---
name: culture
description: Project philosophy and decision-making heuristics. Load before scope debates, feature proposals, or refactors.
triggers:
  - proposal
  - "scope decision"
  - "should we add"
  - "refactor"
  - "minimalism"
---

# Culture

Three principles. They override personal taste.

## 1. Concepts > Code

If you can't explain *why* a change matters in one sentence, you're not ready to open a PR.

- Architecture decisions before implementation polish.
- Naming a thing precedes optimizing it.
- "I'll figure out the why during review" is a code smell.

When in doubt, write the proposal first. SDD is not bureaucracy — it's the discipline that prevents accidental complexity.

## 2. Pi philosophy: minimalism wins

Reference: [earendil-works/pi](https://github.com/earendil-works/pi). Mario Zechner built Pi reacting against agents that felt like *"spaceships with 80% unused functionality"*.

- **Core has 4 tools**: `Read`, `Write`, `Edit`, `Bash`. That's it.
- Anything else is a skill, plugin, or extension.
- If a feature can live as a plugin/skill, it does NOT belong in the core binary.
- "Nice to have" features are not features. They are open issues someone might pick up.

Default answer to "should we add this to core?" is **no**. The bar to clear is: *this cannot work as a plugin, and 80% of users will need it*.

## 3. AI-first, human-led

- Agents (Claude, opencode, Codex, Gemini) draft, search, and verify.
- Humans approve, merge, and own the result.
- Agents never push to `main`. Never bypass review. Never write irreversible side effects without confirming.

The human directs because the human knows the WHY. The agent executes because the agent is fast at the WHAT.

## Decision heuristics

| Situation | Rule |
|---|---|
| New feature proposed | Can it be a plugin? If yes → plugin. Default no to core. |
| Refactor "for cleanliness" | Has it caused a real bug or blocked a real feature? If no → skip. |
| New dependency | Justify in one sentence in the PR. If you can't, drop it. |
| Performance optimization | Measure first. If no benchmark backs the change, it's premature. |
| Backwards-compat shim | Only if there's a real downstream user. No "future-proofing". |
| "Standard pattern from $framework" | Trust the framework's defaults. Pattern-matching ≠ design. |

## What we do NOT optimize for

- "Looking professional" via excessive abstraction.
- "Showing the work" via verbose comments.
- "Future flexibility" for hypothetical users.
- "Matches what $popular-tool does" without owning the why.

## What we DO optimize for

- A user can read the code and understand it in ≤30 minutes.
- A new contributor can ship their first PR in ≤1 day.
- The binary stays under 7 MB.
- The terminal works reliably under load (high-throughput output, complex TUIs, signal storms).
