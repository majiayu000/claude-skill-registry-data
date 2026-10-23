---
name: research-primary-sources
description: 'Use when a decision depends on how a library, platform, protocol, or tool behaves, and that behavior can change by version. Also use it when the user says "check the docs", "is this still true?", or "what does the spec say?". Finds the first-party source for the installed version and reads it. Separates what the source guarantees from what you infer. Not for debugging a failure in your own code (use `diagnose-before-editing`).'
metadata:
  shadowclone-category: research
  shadowclone-section: workflow
  shadowclone-applies-when: when a decision depends on facts outside the repository
---
# Research Primary Sources

## Use when

A decision depends on outside facts about a library, a platform, a protocol, a standard, or a tool. Those facts change with versions, and memory or a search snippet can be out of date.

## Gates

1. Is the question specific enough to have one answer?
2. Did you record the installed version, the runtime, and the platform that the answer must match?
3. Did you read the first-party source itself, such as the specification, the official documents, the source code, or the release notes?
4. Does each claim say whether the source guarantees it or you infer it?
5. If no source answers the question, did you say so and keep the choice easy to reverse?

## Process

1. Write the decision as a question. Record the version, the runtime, the platform, and the limits that apply.
2. Find the source that defines the behavior. Prefer the specification, the official documents, the source code, a release note, or a first-party issue.
3. Open the exact page or file. Check that its version and date match yours.
4. Compare the source with the installed code. Explain each difference that comes from a version or an environment.
5. Write the answer, the link or `file:line` for each claim, and the limit that it puts on the change.

## Example

**Situation:** A change must know which instruction file a coding agent reads when two files exist in one folder.
**Easy route:** Answer from memory: "it reads both".
**Hidden cost:** If memory is wrong, an install can write a file that hides a file of the team, and nobody notices.
**Best route:** Open the official documents for the installed version, find the section about file order, and quote it.
**Evidence:** The documents said that the agent reads the override file first, and reads at most one file in each folder. The install now stops before it writes a file that hides another one.

## Guardrails

- A search result is a lead. Read the source that it points to.
- Quote only the lines that support the decision.
- Keep credentials, private links, and user data out of research notes.
- If the evidence is old, say so, and name the version that it covers.

## Completion

- The answer, or the exact unknown.
- Each claim with its source: a link, or a `file:line`.
- The version that each source covers.
- The limit that the answer puts on the change.
