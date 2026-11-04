---
name: teamsecure
description: Use when running an adversarial security review of a code change — a GitHub PR, a local working-tree diff, or an explicit file list — and when wiring security review into a teamimplement run. Use when asked to security-review, audit, or vulnerability-assess freshly written or proposed code.
---

# teamsecure

Orchestrate an adversarial security review of a code change. You drive two isolated
agents — a **paranoid finder** and a **critical validator** — then verify the survivors
yourself and write a structured findings file.

You are the **orchestrator**. You spawn the agents, enforce the gates, and own the final
verification. You do not perform the first-pass find or the validation yourself; those are
the agents' jobs.

**The canonical, authoritative procedure is in `references/pipeline.md`.** Read it and
follow it exactly. This file is the entry point and the overview; `pipeline.md` is the
source of truth (it is the same procedure `teamimplement` cites, so the two stay in sync).

## When to use
- A PR needs a security review.
- A local, uncommitted change needs a security review (e.g. driven by `teamimplement`).
- An explicit set of changed files needs a security review.

## Input modes
The argument selects the scope:
- `<PR number>` → review a GitHub PR. Resolve the repo dynamically; never hardcode it.
- `--diff` → review the local working-tree / uncommitted changes (`git diff`).
- `--files <a> <b> ...` → review the explicit file list.

## Pipeline (overview — full detail in references/pipeline.md)
1. **Resolve scope** and build the authoritative changed-file list.
2. **Paranoid pass** — spawn `security-paranoid-reviewer`; receive coverage inventory + findings.
3. **Coverage gate** — verify coverage is complete (see `references/coverage-inventory.md`); re-dispatch the finder if not. Do not advance with incomplete coverage.
4. **Critical pass** — spawn `security-critical-reviewer` with the **findings list only** (context isolation is mandatory). Receive verdicts, severities, and attack examples for MEDIUM+.
5. **Verification** — independently re-trace every MEDIUM+ TRUE POSITIVE through the actual code (attack-example + precondition reachability + integration boundary). Drop/downgrade what does not hold.
6. **Output** — write the structured findings file per `references/findings-format.md`.

## Non-negotiables
- **Context isolation:** the validator never receives the finder's reasoning or exploration — only the final findings list. Passing the finder's scratch work to the validator defeats the purpose of the two-agent design.
- **Coverage gate:** every non-test backend file in the change must be explicitly accounted for before the critical pass. Silence is not coverage.
- **Attack-example gate:** no finding ships at MEDIUM+ without a concrete, code-traced attack example that proves the vulnerable state is reachable.
- **Read-only by default for PR mode:** when reviewing a GitHub PR, never post comments, reviews, approvals, labels, branches, or commits, and never trigger workflows. All findings go to the local findings file.

## Output
A structured markdown findings file. No HTML report and no chat widget — findings list only.

## Agents
- `security-paranoid-reviewer` — aggressive first-pass finder.
- `security-critical-reviewer` — skeptical validator.
