---
name: cognitive-output-refiner
description: "Trigger: refine output, summarize output, compact logs, reduce cognitive load, remove duplicates. Refines heavy textual output into a concise, faithful, non-duplicative version."
license: MIT
metadata:
  author: andresnator
  status: in-progress
  version: "2.0.0"
---

# Cognitive Output Refiner

## Activation Contract

Use only when the user explicitly asks in English to refine, summarize, compact, deduplicate, or reduce the cognitive load of textual output such as Markdown, console output, logs, test results, or agent responses.

Do not activate automatically just because output is long. If the input is already concise, say no refinement is needed and offer at most a micro-improvement.

## Hard Rules

- Preserve the input language. Do not translate unless asked.
- Redaction takes precedence over all exact-preservation requirements, including this output template. Never include credential material, including secrets, credentials, inline credentials, connection strings, URL-embedded credentials, API keys, access tokens, cookies, passwords, private keys, session identifiers, or authorization headers, in whole or in part; replace the full credential value with a placeholder such as `[REDACTED_TOKEN]`.
- Preserve useful diagnostic detail from errors, relevant stack frames, commands, paths, public/non-sensitive IDs, decisions, trade-offs, critical warnings, verification steps, and actionable next steps. When preserving stack frames, commands, or paths, redact usernames, local/private path prefixes, internal hostnames, credentials, and other sensitive identifiers while keeping non-sensitive filenames, function names, line numbers, error codes, and public IDs.
- When an ID's sensitivity is ambiguous, redact it. Preserve only clearly public identifiers.
- Be faithful by default. Label inferences as `Inference`, `Likely cause`, or `Possible next step`; never present them as input facts.
- Deduplicate by keeping one canonical version. Preserve meaningful differences explicitly.
- Target 30–50% of the original size by default; use 10–20% only for explicit ultra-compact requests. Fidelity beats size.
- Never overwrite source content. Produce a separate response or file.

## Decision Gates

| Input | Strategy |
|---|---|
| Markdown/docs | Preserve useful hierarchy, improve headings, merge duplicated sections. |
| Console/logs/tests | Group by signal: result, errors, warnings, files, commands, next steps. Preserve order only when causal. |
| Agent/LLM output | Remove repetition, separate decisions from explanations, cut unnecessary narrative. |

Create a file only when the user asks to save/create a document or provides a file as input. Save in the current working directory unless a path is provided. Infer the topic when possible; ask only if unclear. Use `{topic_snake_case}_v<semver>.md`; do not save the original. Start at `v1.0.0` when no prior refined version exists.

SemVer: patch for clarity/order/deduplication, minor for added information or structure changes, major for changed interpretation.

## Output Contract

Return this shape, omitting optional sections when empty. Optional sections are `Preserved Details`, `Information Loss`, and `Compression Notes`. Evaluate each Satisfaction Check item honestly before rendering; if any item fails, fix the output before asking the user.

```md
## TL;DR
- <2-4 bullets with the essential signal>

## Refined Output
<clean, grouped, non-duplicative output>

## Preserved Details
<errors, redacted commands/paths, public/non-sensitive IDs, decisions, redacted placeholders, or other must-preserve facts; never include credential material or ambiguous sensitive identifiers>

## Information Loss
<Low/Medium/High only when compression risk exists>

## Compression Notes
<meaningful removals, merges, or heading changes>

## Satisfaction Check
- [ ] Preserves the important facts.
- [ ] Removes duplicated/noisy content.
- [ ] Is easier to scan.
- [ ] Does not invent conclusions.
- [ ] Fully replaces credential material and redacts sensitive identifiers before rendering.

Are you satisfied with this refined version?
```

If the user is not satisfied, ask one correction question at a time:

```md
[Direct question]

Recommendation: [short suggested answer when useful]
```

Ask the question in normal chat, use `Recommendation: ...` only when useful, and do not add question headings, numbering, rationale blocks, or interview-length estimates. Use the `question` tool only for a closed confirmation or enumerated choice.

After resolving feedback, generate a new complete version, not a patch.

## Mini Example

Input headings `Error Details` and `More Error Details` that repeat the same failing test should become one `### Test Failure` section, with the duplicate merge noted in `Compression Notes`.
