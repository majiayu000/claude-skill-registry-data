---
name: sflow-advise
description: Guide unclear SFlow situations with grounded safe choices.
argument-hint: "[QUESTION | ERROR | WHAT SHOULD I DO?]"
---

# Advise me when I am unsure

<!-- sflow-output-contract: guided-actions -->
**Output contract:** Use read-only CLI evidence, preserve warnings and ordered actions, and change nothing unless explicitly requested.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

Use this when the developer is confused, stuck, or does not know which SFlow route applies.

1. Resolve machine-local Home state first. An active Story and repository are optional; chat history is
   not lifecycle evidence, and an empty Home result is not permission to search for either.
2. With a question or error, run `singularity-flow home --json --request "$ARGUMENTS"`. With no argument, run `singularity-flow recommend --json`.
3. If the result is ambiguous or has no confident route, preserve every returned choice and ask the developer to select one. Never choose on their behalf.
4. When the question is about product behavior rather than current state, run `singularity-flow explain "$ARGUMENTS" --here --json` and cite the returned packaged topic. Do not answer product behavior from memory.
5. When the returned guidance recommends `singularity-flow workspace reinitialize`, present `/sf-admin reinitialize` as the Copilot route. Explain that it previews an exact workspace/repository scope and requires the returned plan ID before applying; do not run either command from this advisory skill and never substitute factory reset.
6. Only when Home returns an active Story and exact repository path, run `singularity-flow nextsteps <WORK-ID> --json`
   there for an unexplained blocker. Run `singularity-flow doctor <WORK-ID>` only
   when guidance calls for repository diagnosis.
7. Present:
   - **What I found** — workspace, repository, Work ID, phase, and exact blocker or uncertainty.
   - **Why** — the evidence, refusal code, or cited rule that caused it.
   - **Safest next step** — one action, why it is preferred, and its `/sf-*` route.
   - **Other choices** — only genuine alternatives returned by SFlow.
   - **What changes** — always “Nothing yet” for this advisory skill.
8. Preserve warnings, unavailable reasons, revisions, and confirmations. Do not retry failures.
9. Never generate, submit, approve, reject, recover, reset, commit, push, or execute a suggestion. The developer must separately invoke its `/sf-*` skill.
