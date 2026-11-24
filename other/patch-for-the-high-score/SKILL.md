---
name: patch-for-the-high-score
description: The full remediation workflow for a pasted security finding (SAST, SCA, Secrets, IaC, or DAST), from investigation through to an applied, diffed, optionally-PR'd fix. Loads app context from mini-map, investigates using the same evidentiary standard as player-two-verdict, judges SCA patch-vs-upgrade tradeoffs using dead-weight-detector's health signals, and gates on fix complexity before touching anything risky. Trigger this whenever the user asks to "remediate this finding," "fix this properly," "walk through fixing this vulnerability," "generate a fix for this CVE/CWE," or wants the deliberate, context-aware path from finding to applied patch. For a fast, standalone pass on a probably-simple finding with no context-loading ceremony, that's `patch-boss-rush` instead.
---

# Patch for the High Score

## Why this skill exists

Every other skill in this arcade stops at a verdict or a report. [`player-two-verdict`](../player-two-verdict) tells you if a finding is real. [`dead-weight-detector`](../dead-weight-detector) tells you if a dependency is worth keeping. Nothing actually closes the loop and fixes the thing. This skill is that loop: take a pasted finding, decide if it's real to the same standard already established elsewhere in this repo, and if it is, plan a fix a junior engineer could follow, get explicit sign-off, apply it, show the diff, and optionally turn it into a PR, without ever committing or pushing on its own say-so.

It reuses rather than reinvents: the finding-parsing and per-type investigation checklists already built for `player-two-verdict`, the dependency health-tier logic already built for `dead-weight-detector` (same script), and the condensed app context already built for [`mini-map`](../mini-map). The new part is the decision layer on top: classify the finding, judge patch-vs-upgrade for dependencies, gate on fix complexity, and manage the apply/diff/PR lifecycle.

## Governing philosophy: default to fixing, not dismissing

The outcomes here are not symmetric. Investigating a finding and drafting a fix that turns out to be unneeded costs a few minutes, and nothing is ever applied without explicit approval. Waving off a real vulnerability as scanner noise ships an exploit. Scanners are genuinely noisy, so False Positive stays a real, evidence-backed outcome, not something taken off the table, but the bar to call something a false positive here is the same one `player-two-verdict` already holds findings to: find a specific reason it's wrong. Ambiguity is not a reason to dismiss, it's a reason to fix.

## When to use this

- The user pastes a finding and wants it actually fixed, not just triaged.
- The user asks to remediate, patch, or resolve a specific CVE/CWE/scanner finding.
- The user wants the deliberate path: app context loaded, dependency health considered, complexity gated before anything risky happens.

If the user wants speed over ceremony on a finding that's probably simple, that's [`patch-boss-rush`](../patch-boss-rush) instead, it does its own lightweight version of this without loading any other skill's artifacts.

If the finding is a container image finding (base image OS package, build-installed binary, buildpack/builder, vendor image, sidecar, or image config like running as root), that's [`cargo-hold-cleanup`](../cargo-hold-cleanup) instead, it has its own ownership-resolution and no-fix-available logic this skill doesn't carry. A container scan finding that resolves to an application dependency (npm/pip/maven/go/gem/cargo) still belongs here, `cargo-hold-cleanup` hands those off to this skill by design.

On a bare "fix this" with no urgency/speed signal either way, this is the default: the safer, context-loaded path.

## Step 0: Prerequisite check

Read `${CLAUDE_PLUGIN_ROOT}/skills/player-two-verdict/SKILL.md` in full before proceeding, specifically its Steps 1, 3, and 4. This skill reuses that skill's parsing and per-finding-type investigation checklists directly, not a paraphrase of them from memory, load the actual file even if `player-two-verdict` already ran earlier in this session.

**Smoke test**: confirm this is a git repo (`git rev-parse --show-toplevel`) and confirm the current branch (`git branch --show-current`). If this isn't a git repo, stop and ask before continuing, don't guess and don't proceed against the wrong tree.

**Hard context gate**: look for `.SEC-Arcade-save_states/MINI_MAP.md`. If it's missing, tell the user this skill requires it and use `AskUserQuestion` to offer generating it now (two options: generate it now, or stop here). Generating it means following [`mini-map`](../mini-map)'s own `SKILL.md` in full, which in turn may cascade into generating a threat model if that's also missing. Once `MINI_MAP.md` exists, read it, it's the app context (identity/session, hardening, trust boundaries, business logic invariants) used when writing the fix plan and judging blast radius in Step 4.

Confirm `AskUserQuestion` and `EnterPlanMode` are available, both are used throughout this skill's flow.

## Step 1: Parse the finding

Parse whatever's pasted per `player-two-verdict`'s Step 1, loaded above: tool name, rule ID, CWE/CVE, reported severity, file/line or package/version, code snippet, secret type/location, resource/template path. Self-resolve a missing critical field via grep/search rather than asking the user, only ask when the repo genuinely can't resolve it. Web search a bare CVE/CWE ID with no real description before investigating further.

Confirm any file path the finding names actually exists in this working tree. If the finding references a repo or branch that doesn't match what's checked out, stop and ask before continuing.

## Step 2: Classify

Every finding lands in exactly one of three buckets, each driving a different path through Steps 3-4:

- **First-party** (SAST, IaC, DAST): code or config this team wrote.
- **OSS dependency** (SCA): a third-party package.
- **Secret**: its own bucket regardless of which tool flagged it, it needs a faster, different response than the investigate-then-plan-a-code-fix flow the other two buckets get.

A finding whose root cause is the container image itself (base image, build-installed binary, image config) isn't any of these three, hand it to [`cargo-hold-cleanup`](../cargo-hold-cleanup) instead of forcing it into one of these buckets.

## Step 3: Analyze & decide

Investigate using the per-finding-type checklist (SAST/SCA/Secrets/IaC/DAST reachability and evidence gathering) from `player-two-verdict/SKILL.md` Steps 1, 3, and 4, loaded in Step 1 above, and the same five-level confidence scale (Very High, High, Medium, Low, Very Low, never a coarser 3-tier scale). Work silently, no narration of intermediate steps.

Three possible outcomes:

1. **FALSE POSITIVE**: not exploitable here, evidence-cited to the same standard `player-two-verdict` demands. Stop, no fix follows. For SCA, still surface Package Health as its own line regardless of this verdict (same ordering rule `player-two-verdict` uses: an abandoned or stale package is a standing risk independent of whether this specific CVE is reachable, don't let an FP verdict erase that).
2. **GENUINE - FIX NOW**: proceed to Step 4.
3. **GENUINE - DEFER (accepted risk)**: rare, requires explicit reasoning, still needs the user's sign-off via `AskUserQuestion` before it's treated as settled. Produces a Risk Acceptance Justification, max 5 sentences, plain language, ready to paste into a ticket, same shape as `player-two-verdict`'s Suppression Justification field.

### Secrets fast path

Skip extended exploitability debate. Reuse `player-two-verdict`'s Secrets checklist: live credential vs. placeholder/test fixture, git history if it's absent from HEAD (a removed-but-once-committed secret is still exposed), evidence of prior rotation, scope and privilege of the credential. If it's live, the very first line of this skill's output, before anything else, is an urgent, unmissable **"ROTATE THIS CREDENTIAL NOW"** callout with the scope/privilege context, since this skill has no access to actually rotate a credential, that happens outside the codebase and is the user's to do immediately. The code-side fix, removing the hardcoded value and loading it from a secret manager or env var, still goes through the normal Step 4 flow afterward as a secondary, still-important action.

### SCA patch-vs-upgrade tradeoff

Once a dependency finding is confirmed genuine and reachable:

- Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py health <ecosystem> <repo_path> <name>`, the exact script `dead-weight-detector` already uses. It returns `recency`, `maintainers`, `downloads`, `vulnerabilities`, and a computed `health_tier` (`healthy`/`slowing`/`at_risk`/`unknown`). Read `${CLAUDE_PLUGIN_ROOT}/references/registry-health-signals.md` for the exact thresholds, don't restate that table, cite it.
- If `health_tier` is `healthy` or `slowing` and a minimal version bump clears the CVE: recommend the minimal patch.
- If `health_tier` is `at_risk` specifically because of staleness (`recency` over 12 months old, not just because of this CVE): recommend a fuller upgrade even beyond what's strictly needed to clear the CVE, explicitly framed as a tech-debt tradeoff, not just a vulnerability fix. Present both options via `AskUserQuestion`, minimal patch vs. full upgrade, rather than silently picking the larger scope.
- There is no "N versions behind latest" metric in `dead_weight_scan.py`, only release recency and health tier. Judge staleness from those, don't invent a version-count metric the tooling doesn't actually provide.

## Step 4: Plan the fix

Only for **GENUINE - FIX NOW** outcomes, this includes the code-side half of a secrets finding and either path of the SCA patch-vs-upgrade decision.

- **Check OWASP guidance as an input, not a gate**: before drafting the plan, check whether `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`, the full 120-sheet OWASP Cheat Sheet Series catalog, has a sheet relevant to this finding's specific topic. Match directly on the vulnerability or technology involved (a JWT finding matches the JSON Web Token Cheat Sheet, an SSRF finding matches Server-Side Request Forgery Prevention, a hardcoded secret matches Secrets Management), don't route through an OWASP Top 10 category first, that's a different, narrower lookup `dungeon-crawl-threat-map` uses for its own purposes, not this one. Always worth checking, never blocking. If something relevant exists, let it shape the actual fix approach, the right pattern, not just whatever satisfies the scanner, and name the sheet in the fix plan for further reading. If nothing genuinely matches (most IaC misconfigurations, a plain dependency bump), say nothing and move on, don't force a citation that doesn't fit.
- **Complexity gate**: trivial means a few lines, touching at most 2 files, no schema or API changes, a clear blast radius. If **any** of the following hold, touches more than 2 files, requires a schema/API change, or has an unclear blast radius, stop before writing a quick plan. Call `EnterPlanMode` and work the fix out with the user through Claude Code's normal plan-mode workflow instead of the fast path below. State plainly which condition tripped the gate.
- **Trivial path**: write a fix plan, max 6 sentences, plain language a junior engineer could follow end to end, no unexplained jargon. Present it, then use `AskUserQuestion` (proceed / don't fix). Only touch a file after explicit approval.

## Step 5: Apply & show diff

Apply the approved fix. Show the full `git diff`. Never run `git commit` or `git push` here, regardless of outcome. State plainly that the change is sitting uncommitted in the working tree, the user's to review and commit.

## Step 6: Offer a PR

After the diff is shown, ask via `AskUserQuestion` whether to turn this into a PR.

- **If yes**: that explicit ask is what authorizes committing, consistent with the rule that commits only happen when asked. Propose a branch name and PR title/body, the user can override either, then create the branch, commit with a message describing the fix and citing the finding, push, and run `gh pr create` following this environment's standard Summary/Test-plan PR template, populated with the finding's evidence and the fix's rationale.
  - Branch: `fix/<category>-<short-slug>`, e.g. `fix/sast-sqli-users-api`, `fix/sca-lodash-cve-2021-xxxxx`, `fix/secret-hardcoded-api-key`.
  - PR title: `Fix: <plain description> (<CWE-XXX or CVE-XXXX-XXXX or package@version>)`.
- **If no**: stop, leave the diff in the working tree.

## Voice and format

- No em dashes.
- Plain, direct, evidence-cited, same register as `player-two-verdict`: a senior engineer briefing a junior on something they need to act on today.
- Never narrate intermediate investigation steps, only the structured output below.
- The Fix Plan is the one section written for someone with less context than the rest of the output, no unexplained jargon, 6 sentences max, no exceptions.

Use this structure:

```
🛠️ [FIRST-PARTY / OSS DEPENDENCY / SECRET] - [FIX NOW / DEFER / FALSE POSITIVE] | Confidence: [level]
[🚨 ROTATE THIS CREDENTIAL NOW - secrets only, live credential, appears above everything else]

Summary: [2-3 plain-language sentences, no jargon, no citations]

Evidence:
- `path/file.ext:line`, `functionOrSymbolName()`: [factual, no interpretation]
[2-5 bullets, same evidentiary standard as player-two-verdict]

Justification:
- [reasoning bullet citing Evidence above by file:line]

Package Health: [SCA only, health_tier + recency + patch-vs-upgrade recommendation]

Risk Acceptance Justification: [DEFER only, max 5 sentences, ticket-ready]

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

- `${CLAUDE_PLUGIN_ROOT}/skills/player-two-verdict/SKILL.md`: Steps 1, 3, and 4, read in full in Step 0 and reused directly for parsing and per-finding-type investigation.
- `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`: the full OWASP Cheat Sheet Series catalog, used in Step 4 as a direct topic lookup to shape the fix approach.
- `${CLAUDE_PLUGIN_ROOT}/references/registry-health-signals.md`: health-tier thresholds, used in Step 3's SCA patch-vs-upgrade decision.
- `${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py`: the `health` subcommand, reused as-is in Step 3.
- `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: the `.SEC-Arcade-save_states/` folder convention Step 0's context gate depends on.
