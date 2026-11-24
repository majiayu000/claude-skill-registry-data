---
name: patch-boss-rush
description: A fast, fully self-contained remediation pass on a single pasted security finding (SAST, SCA, Secrets, IaC, or DAST), no app-context loading, no dependency-health lookups, no delegation to any other skill in this plugin. Does its own compact sanity check, plans a fix, applies it on approval, shows the diff, and optionally opens a PR. Trigger this whenever the user asks to "just fix this," "quick fix," "rush this," or wants fast remediation on a finding that's probably simple, without the full context-gathering ceremony. For the deliberate, context-aware workflow (app context, dependency staleness tradeoffs), that's `patch-for-the-high-score` instead.
---

# Patch Boss Rush

## Why this skill exists

Not every finding needs the full ceremony. A single obvious SQL injection in one function, a secret that clearly needs rotating, a dependency with a one-line patched version bump, these don't need an app-context file loaded first or a dependency's full maintenance history pulled up. This skill is the fast lane: read the finding, do a short sanity check with its own logic, plan a fix, get approval, apply it, show the diff. It is deliberately **standalone**, it does not read `.SEC-Arcade-save_states/MINI_MAP.md`, does not call `dead_weight_scan.py`, and does not delegate to `player-two-verdict`'s investigation checklists. Everything here is this skill's own, compact version of the same idea.

"Rush" describes how much ceremony a single finding gets, not how many findings get processed per run. This still handles one finding at a time.

## When to use this

- The user wants a finding fixed fast, and it looks like a self-contained, probably-simple case.
- The user explicitly asks to skip the full workflow.
- No `.SEC-Arcade-save_states/` context exists yet and the user doesn't want to generate it just to fix one finding.

If the finding is genuinely complex, touches security-sensitive business logic, or the user wants dependency staleness/tech-debt considered as part of an SCA fix, that's [`patch-for-the-high-score`](../patch-for-the-high-score) instead, it loads real app context and dependency health data before deciding.

If the finding is a container image finding (base image OS package, build-installed binary, buildpack/builder, vendor image, sidecar, or image config like running as root), that's [`cargo-hold-cleanup`](../cargo-hold-cleanup) instead, it has ownership-resolution and no-fix-available logic this skill doesn't carry. A container scan finding that turns out to be an application dependency still belongs here or with `patch-for-the-high-score`, `cargo-hold-cleanup` hands those off rather than fixing them itself.

On a bare "fix this" with no urgency/speed signal either way, default to `patch-for-the-high-score`, the safer, context-loaded path. Only take this skill when the request itself signals speed ("quick," "just," "rush") or explicitly opts out of the full workflow.

## Step 0: Prerequisite check

Confirm this is a git repo (`git rev-parse --show-toplevel`) and confirm the current branch (`git branch --show-current`). If this isn't a git repo, stop and ask rather than guessing, the fix, diff, and PR steps all depend on it.

Confirm `AskUserQuestion` and `EnterPlanMode` are available, both are used later in this skill's flow (Step 4 onward).

## Step 1: Parse the finding

Extract from whatever's pasted: tool name, rule ID, CWE/CVE, reported severity, file/line or package/version, code snippet, secret type/location, resource/template path. If a critical field like a line number is missing, find it yourself with grep or search rather than asking. If a bare CVE/CWE ID has no real description attached, web search it before going further, you need to know what the vulnerability actually is.

Confirm any file path the finding names actually exists in this working tree. If it doesn't, stop and ask rather than guessing.

## Step 2: Classify

- **First-party** (SAST, IaC, DAST): code or config this team wrote.
- **OSS dependency** (SCA): a third-party package.
- **Secret**: its own bucket regardless of source tool, it gets the rotation callout below instead of a full investigation.

A finding whose root cause is the container image itself (base image, build-installed binary, image config) isn't any of these three, hand it to [`cargo-hold-cleanup`](../cargo-hold-cleanup) instead.

## Step 3: Quick check

One short pass, not an exhaustive trace. The goal is the same as anywhere else in this plugin, find a specific reason the finding is wrong before accepting it's right, but the depth here is intentionally shallow:

- **SAST / DAST**: does the flagged input reach the sink without sanitization, encoding, or parameterization in between. One clear check, not a multi-hop trace through every possible caller.
- **SCA**: is the vulnerable function actually imported or called anywhere in first-party code (one-hop check, not a full call-graph trace), and what's the pinned version vs. the patched version.
- **Secrets**: is this a live credential, or a placeholder/example/test fixture.
- **IaC**: what's the actual effective configuration for the flagged resource, not just what the raw template shows.

If this turns up a clear, specific reason the finding isn't real, say so plainly and stop. Evidence-cited, same as everywhere else in this plugin, just without a five-level confidence scale: always state a plain confidence word (High / Medium / Low) in the output header, not just when it's non-obvious.

### Secrets fast path

If Step 3 found a live credential, the very first line of output, before anything else, is an urgent **"ROTATE THIS CREDENTIAL NOW"** callout with its scope and privilege. This skill can't rotate it, that happens outside the codebase and is the user's to do immediately. The code-side fix (remove the hardcoded value, load from an env var or secret manager) still goes through Step 4.

## Step 4: Plan the fix

Only if Step 3 didn't already rule the finding out.

- **Check OWASP guidance as an input, not a gate**: check whether `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`, the full 120-sheet OWASP Cheat Sheet Series catalog, has a sheet relevant to this finding's specific topic. Match directly on the vulnerability or technology involved (a JWT finding matches the JSON Web Token Cheat Sheet, an SSRF finding matches Server-Side Request Forgery Prevention), not through an OWASP Top 10 category. Advisory, always worth a look, never blocking. If something fits, let it shape the fix and name the sheet in the plan. If nothing fits, move on without forcing it.
- **Complexity gate**: trivial means a few lines, at most 2 files, no schema/API changes, a clear blast radius. If it touches more than 2 files, requires a schema/API change, or has an unclear blast radius, stop: call `EnterPlanMode` and work it out with the user through Claude Code's normal plan-mode workflow instead of the fast path below. Say plainly which condition tripped the gate.
- **Trivial path**: write the fix plan, max 6 sentences, plain language a junior engineer could follow, no unexplained jargon. Present it, then `AskUserQuestion` (proceed / don't fix). Only touch a file after explicit approval.

## Step 5: Apply & show diff

Apply the approved fix. Show the full `git diff`. Never run `git commit` or `git push` here. The change sits uncommitted in the working tree, the user's to review and commit.

## Step 6: Offer a PR

After the diff is shown, ask via `AskUserQuestion` whether to turn this into a PR.

- **If yes**: propose a branch name and PR title/body, the user can override either, then create the branch, commit with a message describing the fix and citing the finding, push, and run `gh pr create` following this environment's standard Summary/Test-plan PR template.
  - Branch: `fix/<category>-<short-slug>`, e.g. `fix/sast-sqli-users-api`, `fix/sca-lodash-cve-2021-xxxxx`, `fix/secret-hardcoded-api-key`.
  - PR title: `Fix: <plain description> (<CWE-XXX or CVE-XXXX-XXXX or package@version>)`.
- **If no**: stop, leave the diff in the working tree.

## Voice and format

- No em dashes.
- Plain, direct, evidence-cited. Shorter than `patch-for-the-high-score`'s output by design, this skill trades depth for speed.
- No narration of intermediate steps, only the structured output below.

Use this structure:

```
⚡ [FIRST-PARTY / OSS DEPENDENCY / SECRET] - [FIX NOW / FALSE POSITIVE] | Confidence: [High / Medium / Low]
[🚨 ROTATE THIS CREDENTIAL NOW - secrets only, live credential, appears above everything else]

Summary: [2-3 plain-language sentences, no jargon, no citations]

Evidence:
- `path/file.ext:line`, `functionOrSymbolName()`: [factual, no interpretation]
[1-3 bullets, kept short]

Fix Plan (max 6 sentences, junior-engineer clear):
1. ...
[cite the relevant OWASP Cheat Sheet by name here if one applied]

Action: [what happens next, tied to the AskUserQuestion below]
```

```
[AskUserQuestion: proceed with this fix / don't fix]
[or, if the complexity gate tripped: EnterPlanMode instead of the block above]
```

After approval and apply:

```
Diff:
[git diff output, in full]

[AskUserQuestion: create a branch + PR for this? yes, with proposed branch/title / no]
```

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`: the full OWASP Cheat Sheet Series catalog, used in Step 4 as advisory input on the fix approach. This is the only shared reference this skill uses, it's a static lookup table, not another skill's behavior or artifact.
