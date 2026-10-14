---
name: leetcode-interview-coach
description: "Route disclosure-controlled coaching for LeetCode-style and coding-interview attempts. Use for natural-language coaching requests and for combined or ambiguous workflows spanning stuck, lcd, salvage, optimize, best, check, follow-up, visualize, low-level, and quiz. A directly invoked skill takes priority over this router."
---

# LeetCode Interview Coach

Route the user's request to the right workflow while preserving the smallest solution-reveal boundary they asked for.

## Prefer the direct skills

| Base skill | Contract |
|---|---|
| `follow-up` | Exactly one hard, unanswered follow-up |
| `check` | Complexity audit, solution untouched |
| `lcd` | Lowest-cost diagnostic, no fix |
| `stuck` | Smallest useful progressive hint |
| `salvage` | Minimum working repair |
| `optimize` | Improve without replacing the idea |
| `best` | Interview-canonical full solutions |

| Overlay skill | Contract |
|---|---|
| `visualize` | Interactive disclosure-safe mental model |
| `low-level` | Relevant systems mechanism |
| `quiz` | Adaptive retrieval and transfer practice |

When the user invokes one or more of these directly, let those skills govern. Never ask the user to invoke this router first.

## Route the request

For a natural-language coaching request, or when a named skill is not installed, select the matching workflow and read the sibling file completely before responding:

- `stuck` → [../stuck/SKILL.md](../stuck/SKILL.md)
- `lcd` → [../lcd/SKILL.md](../lcd/SKILL.md)
- `salvage` → [../salvage/SKILL.md](../salvage/SKILL.md)
- `optimize` → [../optimize/SKILL.md](../optimize/SKILL.md)
- `best` → [../best/SKILL.md](../best/SKILL.md)
- `check` → [../check/SKILL.md](../check/SKILL.md)
- `follow-up` → [../follow-up/SKILL.md](../follow-up/SKILL.md)
- `visualize` → [../visualize/SKILL.md](../visualize/SKILL.md)
- `low-level` → [../low-level/SKILL.md](../low-level/SKILL.md)
- `quiz` → [../quiz/SKILL.md](../quiz/SKILL.md)

If a sibling file is unavailable, follow the compact contract in the tables above rather than failing.

## Compose workflows

Base skills are ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

- When a prompt names several base skills, the least-revealing one sets the response contract and disclosure ceiling, whatever order they were typed in. A spoiler cannot be taken back, so the ceiling always falls to the safest request in the prompt.
- Name the governing skill in one short line when the prompt asked for a higher rung than it received, so the user can re-ask for the higher rung on its own.
- `visualize`, `low-level`, and `quiz` are order-independent overlays. They never raise the ceiling.
- Satisfy compatible overlays as one coherent response. If an overlay conflicts with an exact base output contract, the base contract wins.
- With no base skill named, infer the user's current stage and the strongest solution already established in the thread.
- `follow-up` always remains exactly one unanswered question.
- Read [references/composable-modes.md](references/composable-modes.md) whenever two or more overlays are active.

## Mark the changes

A marker tells the user what to edit in a file they already have, so it belongs only on a patch against existing code.

- A line the user must add → `NEW`
- An existing line the user must change → `MOD`
- An unchanged line shown for context → no marker

Write the marker as a trailing comment in the target language's own comment syntax, and never mix two languages' syntax: `// NEW` in C, Java, JavaScript, Go, or Rust; `# NEW` in Python, Ruby, or shell; `-- MOD` in SQL or Lua; `<!-- NEW -->` in HTML.

Do not mark code the user has no existing version of. When every line is new there is nothing to distinguish, and the markers are pure noise.

## Inspect the attempt

1. Read the problem, constraints, code, visible line numbers, error, observed output, and relevant thread context from the screenshot, image, attachment, or paste.
2. Infer the language and attempted algorithm. Do not ask for facts that are visible or safely inferable.
3. Use source line numbers when they are shown. Otherwise label counted lines `pasted line N` or `visible line N` and name the neighboring statement. Never invent a file line.
4. Ask one focused question only when a missing problem rule or cropped code makes the requested judgment unsafe. Otherwise state the assumption and proceed.
5. Do not edit, run, or submit the user's code without permission. `visualize`, alone or with `quiz`, authorizes only the user-facing HTML and the temporary preview artifacts that response needs.
6. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.

## Preserve interview quality

Reward clarification, a stated invariant, syntactically valid code, deliberate tests, complexity justification, and concise tradeoff communication. For questions about specific companies' expectations, read [references/interview-calibration.md](references/interview-calibration.md).
