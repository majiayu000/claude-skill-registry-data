---
name: cargo-hold-cleanup
description: Remediate a container image finding (base image OS package CVE, build-installed binary CVE, distro/base image swap, or image config issue like running as root or privileged mode), from ownership resolution through an applied, diffed fix. Parses Snyk CLI JSON, Snyk Container SARIF, or pasted console output. Trigger this whenever the user pastes a container/image scan finding, a Trivy/Grype/Snyk Container/Docker Scout result, or asks to "fix this base image CVE," "patch this Dockerfile finding," "why is this container running as root," or "remediate this image vulnerability." If the finding resolves to an application dependency (npm/pip/maven/go/gem/cargo) rather than the image itself, this skill hands off to `patch-for-the-high-score` (or `patch-boss-rush` for a faster pass) instead of remediating it here.
---

# Cargo Hold Cleanup

## Why this skill exists

Container findings are not SCA findings wearing a different hat. A base image CVE has no manifest or lockfile to bump, its fix target is a `FROM` line or a `RUN` step. A "no fix available" OS package finding has a whole decision tree (remove, swap base, assess reachability, compensating control, time-boxed exception) that doesn't exist for application dependencies. A finding that says "running as root" isn't a CVE at all. Routing all of this through the same logic `patch-for-the-high-score`/`patch-boss-rush` use for source and dependency fixes would either mangle the container-specific cases or quietly ignore them. This skill is the dedicated path for container image findings, and only container image findings.

## Scope

**In scope**: base image OS package CVEs, build-installed binary CVEs, buildpack/Jib/ko/apko/Bazel-built image findings, vendor/third-party image findings, injected sidecar findings, and image config findings (root user, privileged mode, missing capability drops, writable root filesystem).

**Out of scope, hands off instead of remediating**:
- A finding that resolves to an application dependency (npm/pip/maven/go/gem/cargo, manifest + lockfile) hands off to [`patch-for-the-high-score`](../patch-for-the-high-score) (or [`patch-boss-rush`](../patch-boss-rush) if the user signals speed over ceremony, same default rule those two already use between each other). State the handoff and stop, don't remediate it here.
- Source code fixes (SAST-class findings), IaC misconfiguration outside the image itself, Kubernetes manifest security policy beyond the admission-policy fallback in the playbook, and registry access/configuration are all out of scope entirely, not a handoff, just not this skill's job.

## When to use this

- The user pastes a container/image scan finding (Trivy, Grype, Snyk Container, Docker Scout, or similar) and wants it fixed.
- The user asks about a base image CVE, a Dockerfile-level finding, or a "running as root"/"privileged container" config finding.
- The user asks specifically about a container finding as opposed to a general "fix this finding" that could be any type, that broader case is `patch-for-the-high-score`/`patch-boss-rush`.

## Step 0: Prerequisite check

Confirm this is a git repo and `git` is available, both are needed for the diff and PR steps later (Steps 6-8). If this isn't a git repo, say so and ask whether to continue read-only (investigation and a recommendation, no diff or PR) or stop.

Confirm `AskUserQuestion` and `EnterPlanMode` are available, both are used throughout this skill's remediation flow.

## Step 1: Parse the input

Extract from whatever's pasted: scanner/tool name, vulnerability ID (CVE/GHSA), package name and installed version, fixed-in version if one exists, the `introducedThrough` or dependency path, severity, and the image reference (repo:tag or digest) the finding was raised against. For a config finding, extract the specific control that's missing or misconfigured instead (no CVE ID exists for these).

Also ask, or infer from what's already visible in the session, three pieces of context before proceeding:
- Is a Dockerfile available in this repo, or is this a vendor/pulled-as-is image with no build config here at all?
- Is the image first-party (this org builds it) or vendor/third-party?
- Is registry metadata available (build date, current digest for the tag) to check rebuild cadence in Step 3?

Self-resolve what the repo can answer (find the Dockerfile, check the registry if credentials are already configured) rather than asking the user for anything the working tree or an already-authenticated CLI can answer directly. Only ask when it genuinely can't be resolved locally.

### Formats this skill parses

**Snyk CLI JSON** (`snyk container test --json`), key fields:
```json
{
  "vulnerabilities": [{
    "id": "SNYK-DEBIAN12-OPENSSL3-1234567",
    "title": "Out-of-bounds Write",
    "severity": "high",
    "packageName": "openssl",
    "version": "3.0.11-1~deb12u1",
    "fixedIn": ["3.0.11-1~deb12u2"],
    "from": ["docker-image|myapp@1.4.0", "debian:12", "openssl@3.0.11-1~deb12u1"]
  }]
}
```
The `from` array is the `introducedThrough` path: reading it bottom-up shows the base image (`debian:12`) directly owning the package, no manifest in between, that's a Base Image OS Package finding per the ownership table.

**Snyk Container SARIF**, same data, different shape:
```json
{
  "runs": [{
    "results": [{
      "ruleId": "SNYK-DEBIAN12-OPENSSL3-1234567",
      "level": "error",
      "message": { "text": "openssl@3.0.11-1~deb12u1 has a fix available in 3.0.11-1~deb12u2" },
      "properties": { "packageName": "openssl", "introducedThrough": ["debian:12"] }
    }]
  }]
}
```

**Pasted human-readable console output**, e.g.:
```
✗ High severity vulnerability found in openssl
  Description: Out-of-bounds Write
  Introduced through: debian:12, openssl@3.0.11-1~deb12u1
  Fixed in: 3.0.11-1~deb12u2
```

All three carry the same fields under different names, extract the same set regardless of which one lands.

### Example findings by outcome

**Base image OS package, fix available**: the SNYK-DEBIAN12-OPENSSL3 example above. `introducedThrough` bottoms out at `debian:12`, no manifest, `fixedIn` is populated.

**No fix available**:
```
✗ Critical severity vulnerability found in glibc
  Introduced through: alpine:3.18, musl@1.2.4-r0
  Fixed in: No fix available
```

**Introduced-through points to an application dependency** (out of scope, hand off):
```
✗ High severity vulnerability found in lodash
  Introduced through: myapp@1.4.0, package.json, lodash@4.17.20
```
`package.json` sitting in the path is the signal, this is an app dependency finding regardless of the fact that it surfaced from a container scan of the built image.

**Config finding, no CVE**:
```
Dockerfile:12  [MEDIUM] Container is running as root, no USER instruction found
```

## Step 2: Ownership resolution

Read the Ownership Resolution table in `${CLAUDE_PLUGIN_ROOT}/references/container-remediation-playbook.md`, don't restate it, classify the parsed finding against it and state the resolved layer as the first line of output. This runs before any remediation attempt, and before the pre-triage checks in Step 3.

If the finding resolves to **App dependency**: output the classification, state the handoff target ([`patch-for-the-high-score`](../patch-for-the-high-score) by default, `patch-boss-rush` if speed was signaled), and stop. Nothing further in this skill runs.

If the finding resolves to **Vendor or third-party image**: skip straight to the No-fix-available path in Step 4 regardless of whether a fix version exists upstream, since this skill has no repo target to edit either way. The output is an upgrade-path recommendation, vendor escalation note, or compensating control, not a diff.

Also check the Edge Cases section of the playbook here: a finding in a discarded multi-stage build stage is a false positive at the image level, and a CVE that also shows up in an SCA scan of the same repo gets flagged as overlapping and deferred to the SCA-side flow rather than fixed twice.

## Step 3: Pre-triage checks

Read the Pre-triage Checks section of the playbook and run both, in order, before proposing any change:

1. **Rebuild cadence**: if the image build date is more than roughly 30 days old, or the pulled base digest isn't current for its tag, state that plainly as the output and stop, don't propose an edit until the user confirms the image under test is current. Ask via `AskUserQuestion` whether to proceed with the rebuild-and-rescan-first recommendation or continue anyway with a known-stale baseline.
2. **Presence and necessity**: is the vulnerable package actually needed in the shipped image? If it can be dropped (multi-stage build, smaller base image that never installs it), that's the preferred fix, propose it before an upgrade, not after.

## Step 4: Remediation, or the no-fix path

**If a fix is available**: read the Remediation Templates section of the playbook for the shape of the change (base image bump with digest pinning, inline pinned upgrade if no patched tag exists yet, build-installed binary version+checksum bump, distro switch, or image config directive). Draft the specific before/after change for this finding following that template.

**If no fix is available**, or the finding resolved to a vendor image: read the No-fix-available Decision Order in the playbook and work it in sequence, remove if unused, swap base image if possible, assess reachability, apply a compensating control, only reach for a time-bound exception once 1 through 4 are genuinely exhausted. If an exception is the actual output, populate every field the playbook's Exception Required Fields list demands, don't produce a partial one, and ask the user directly for whatever fields you can't infer (named owner, expiry).

## Step 5: Plan and gate on complexity

Check the OWASP Docker Security Cheat Sheet (and the NodeJS Docker Cheat Sheet if the base image is Node-based) in `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md` as advisory input, cite it in the plan if it shapes the approach, skip silently if nothing in it applies to this specific finding.

**Complexity gate**: trivial means a single `FROM` tag/digest bump or a single `RUN` step version+checksum bump, touching only the Dockerfile (or single build config file for buildpack/Jib/ko cases), with no distro switch and no follow-on changes to entrypoint scripts, healthchecks, or user/permission setup required. If **any** of the following hold, a distro switch, a change that also requires touching an entrypoint/healthcheck/permissions because of the Breakage Warning List in the playbook, or an unclear blast radius, stop and call `EnterPlanMode` instead of the fast path below. State plainly which condition tripped the gate, and cite the specific breakage classes from the playbook that make this non-trivial.

**Trivial path**: present the fix plan (max 6 sentences, junior-engineer clear) plus any breakage warnings from the playbook that apply even to this small a change (a patch-level bump rarely triggers them, a minor version bump can). Use `AskUserQuestion` (proceed / don't fix). Only touch a file after explicit approval.

## Step 6: Apply & show diff

Apply the approved fix. Show the full `git diff`. Never run `git commit` or `git push` here. State plainly that the change sits uncommitted in the working tree, the user's to review and commit.

## Step 7: Regression check requirement

This is a hard rule, not optional guidance: after any base image change, instruct the user to rebuild and rescan the full image, then diff the complete result set against the pre-fix scan, resolved, introduced, and unchanged, not just confirm the target vulnerability ID cleared. Base image bumps routinely trade one CVE for several others picked up from the new base. Read the Verification Steps list in the playbook and present it as the required sequence, state explicitly that scanning the local build layer cache is not sufficient evidence, the pushed registry artifact and the running workload both have to report clean.

## Step 8: Offer a PR

After the diff is shown and the regression-check instructions are given, ask via `AskUserQuestion` whether to turn this into a PR.

- **If yes**: propose a branch name and PR title/body, the user can override either, then create the branch, commit with a message describing the fix and citing the finding, push, and run `gh pr create` following this environment's standard Summary/Test-plan PR template. Include the required post-merge rescan step in the PR body's test plan, not just in this session's output.
  - Branch: `fix/container-<short-slug>`, e.g. `fix/container-openssl-base-bump`, `fix/container-nonroot-user`.
  - PR title: `Fix: <plain description> (<CVE/GHSA ID or config control name>)`.
- **If no**: stop, leave the diff in the working tree.

## Voice and format

- No em dashes.
- Plain, direct, evidence-cited, same register as `patch-for-the-high-score`/`patch-boss-rush`: a senior engineer briefing a junior on something they need to act on today.
- Never narrate intermediate investigation steps, only the structured output below.

Use this structure:

```
📦 [BASE IMAGE OS PACKAGE / APP DEPENDENCY / BUILD-INSTALLED BINARY / BUILDPACK / VENDOR IMAGE / SIDECAR / IMAGE CONFIG] - [REBUILD & RESCAN FIRST / FIX NOW / NO FIX - COMPENSATING CONTROL / NO FIX - EXCEPTION / HANDOFF / VENDOR ESCALATION / FALSE POSITIVE]

Resolved layer: [from the ownership table, one line, so the routing is verifiable]

Summary: [2-3 plain-language sentences, no jargon, no citations]

[If REBUILD & RESCAN FIRST: state the stale build/digest evidence, stop here pending user confirmation]
[If HANDOFF: state the introducedThrough evidence pointing to a manifest, name the target skill, stop here]

Evidence:
- [scanner field, image reference, introducedThrough path, or Dockerfile line, factual, no interpretation]

Fix target: [FROM line / RUN step / build config / chart or operator version / Dockerfile directive / admission policy / no repo target]

Proposed change:
[diff, or vendor escalation note / exception draft with every required field, when no code change is possible]

Breakage risks: [from the playbook's breakage warning list, only the ones that actually apply to this change]

Fix Plan (max 6 sentences, junior-engineer clear):
1. ...
[cite the OWASP Docker Security Cheat Sheet or NodeJS Docker Cheat Sheet here if one applied]

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

Regression check required:
[the verification steps sequence from the playbook, stated as required next actions]

[AskUserQuestion: create a branch + PR for this? yes, with proposed branch/title / no]
```

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/references/container-remediation-playbook.md`: the ownership resolution table (Step 2), pre-triage checks (Step 3), remediation templates and breakage warning list (Steps 4-5), no-fix decision order and exception fields (Step 4), verification steps (Step 7), and edge cases (Step 2). This skill's core logic lives here, cited throughout rather than restated.
- `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`: the Docker Security Cheat Sheet and NodeJS Docker Cheat Sheet, used in Step 5 as advisory input on the fix approach.
- [`patch-for-the-high-score`](../patch-for-the-high-score) and [`patch-boss-rush`](../patch-boss-rush): the handoff targets for any finding Step 2 resolves to an application dependency instead of the image itself.
