---
name: padosoft-ci-workflow-gates
description: >-
  Use this skill when writing or reviewing a CI workflow or a gate that guards a merge — a GitHub Actions
  file, a required check, a validator script, a secret scan, a branch or tag ruleset — and whenever the user
  says a check went green without checking anything, a workflow did not start, a label does not trigger the
  run, CI minutes are being burned on every push, a required check cannot run before merge, or a rule can be
  bypassed. It covers what actually makes a gate a gate, the trigger and permission semantics that silently
  replace your defaults, and the cost tiering. Do not use it to design deployment pipelines, to pick a CI
  provider, or to debug a failing application test.
license: MIT
compatibility: >-
  GitHub Actions for the trigger and ruleset specifics; the reasoning about what makes a gate real applies to
  any CI system.
metadata:
  version: 0.3.0
  author: Padosoft
  summary: A gate that cannot fail is not a gate.
  profiles: devops
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: ci, github actions, gate, workflow, permissions, ruleset, secret scanning, required checks, supply chain, signing
---

# CI workflow gates

**A gate that cannot fail is not a gate**, and the ways one stops being able to fail are rarely visible in
the diff that broke it. Most of what follows is a green check that had not looked at anything.

---

## 1. The gate has to be able to see the whole contract

A manifest that lists what must exist, but **omits itself and its own workflow**, stays green after half the
contract is deleted. Enumerate every mandatory rule, workflow, validator and file — including the ones doing
the checking.

Related shapes of the same failure:

- **Presence-only matching accepts an empty contract.** Checking that a `Tests:` marker exists says nothing
  about whether anything follows it. Require non-empty content, and accept both inline prose and a following
  block, because documents legitimately use both.
- **A detector as strict as the parser cannot see malformed input.** If the strict parser only accepts
  `M01-S02`, a candidate detector built on the same pattern is blind to `M01-SO2` and `M01-S100` — exactly
  the typos it exists to catch. **The candidate detector must be broader than the parser**, then report what
  it found that the parser rejected.
- **Validating the items does not validate the set.** Unique ids and well-formed entries still allow one
  entry to silently disappear. If the count is part of the contract, version the manifest and assert it.

## 2. A security gate fails closed, or it is decoration

```text
❌ files larger than N are skipped      → a credential in a large file walks through
✅ scan everything within the limit, and REJECT what exceeds it
```

Skipping is the failure mode that looks like handling. Anything the scanner cannot process is a **finding**,
not a pass.

Three traps that come from the filesystem rather than from the rule:

- **Symlinks escape.** Reading a candidate path before checking its link metadata lets a tracked symlink
  point outside the repository. Check link metadata first — and check again *after* creating output
  directories, because an intermediate link can redirect a write that is lexically inside the repo.
- **Path listings are display forms.** Tools quote or escape non-ASCII and control characters in their
  human-readable output; treating that form as a literal path makes the file silently unreachable, so the
  scanner reports clean on a file it never opened. Use the tool's machine-readable output.
- **Encoding hides patterns.** Decoding every stream as UTF-8 leaves NUL bytes between ASCII characters of a
  UTF-16 file, and regexes stop matching. Scan the decoded content **and** a NUL-normalised view.

## 3. Do not regex a structured file

A workflow, a manifest, a front matter block: parse it, then traverse the parsed structure.

Regex over raw text cannot tell an executable expression from a comment that mentions it, so a safety comment
becomes a false positive — and, worse, a real occurrence inside a quoted string is missed. It also breaks on
layouts that are perfectly valid: a key wrapped across lines, keys in a different order.

And it misses what is not at the top level: **validating only the root `permissions` map misses a job-level
one**, which replaces the safe root grant rather than narrowing it. Validate the root and **every job**.

## 4. Trigger semantics that replace your defaults

- **Declaring `pull_request.types` replaces the default list.** A workflow that declares only
  `labeled, unlabeled` no longer runs on `opened`, `reopened` or `synchronize` — a new PR, or a pushed head,
  gets no run at all. List every type you still need.
- **A label-gated job is inert if the trigger does not subscribe to the label event.** The condition can be
  perfectly correct and never evaluated, because adding the label starts no run.
- **A required check cannot run on the merge commit before the merge exists.** Gating on "the exact merge
  SHA" makes the pre-merge gate impossible: require the checks on the final PR **head** SHA.
- **Pass the base SHA in from the event**, and verify or fetch it. Building a diff-based gate on an assumed
  remote-tracking ref works until a checkout mode changes.
- **Normalise and compare a complete condition**, never a substring: two substring checks are both satisfied
  by an impossible `A && B`, and the job never runs.
- **Requiring a script by name in the run text accepts `echo script.ps1`.** Compare the parsed command.

## 5. Conclusions are not the whole result

A job can succeed **and** emit an annotation — a deprecated runtime, a rate limit, a fallback. Inspect
annotations as part of the gate, not only the conclusion, or the deprecation notice nobody read becomes a
broken action six months later.

Pin actions to an **immutable SHA**, not a floating tag, and check that the tag you pinned is the current
official one before freezing it.

## 5b. Supply chain: what runs is not what you reviewed

Pinning the action is the start of it, not the end.

- **Hardened runtime flags do not pin the bytes.** Read-only filesystems, dropped capabilities and
  no-new-privileges protect the *invocation*; a mutable image tag can change the executable between two
  runs. Require an immutable digest, and fail **before** dispatch when the operator has not supplied one.
  Render deployment templates with `repository@digest`, and keep the tag fallback as a visibly
  non-production choice.
- **An integrity hash is not an identity.** It proves the bytes did not change, not who produced them.
  Verifying a signature proves the supplied key signed it — **pin the expected key identity too**, or an
  authentic document signed by the wrong key passes. Rotate the approved key and its identifier together.
- **A parsed signing bundle is not a trust decision.** Verification has to bind the payload, the certificate
  identity, the issuer and the transparency evidence, and fail closed on a malformed or policy-less bundle.
  Pin a maintained verifier and track its advisories rather than reimplementing the cryptography.
- **A signature on a manifest does not cover the content the manifest lists.** Load listed resources before
  the first use, reject missing paths, duplicate ids and symlink escapes, and expand only explicit
  references. Signing policy belongs at the **import** boundary, where the content enters.
- **A clean dependency dashboard is not a gate.** Run the audit on every lockfile change, and re-run the
  build, the bundle and the full suite after a toolchain upgrade — the findings that matter are transitive
  and invisible to application tests. One repository can hold **more than one dependency perimeter**.
- **Test the published bundle, not the working tree.** Assets resolve differently once packaged, an offline
  or air-gapped bundle has its own release identity, and an optional driver pulled into the main bundle
  changes what every user downloads. The shipped examples are part of the supply chain too.

## 5c. Scanners earn their place by being read

A scanner nobody reads is a line in a bill. Four decisions make the difference:

- **Block on the diff, report on the history.** A secret introduced now must not merge; the accumulated
  history starts as a report, because a job born red and left red is disabled within a week — and then the
  diff is unprotected too. It becomes blocking after the triage.
- **Run dependency audits on the pull request *and* on a schedule.** An advisory published tomorrow concerns
  code nobody is touching, so a pull-request-only audit never sees it.
- **Audit the lock file, and do not exclude development dependencies** when the bundler puts them in the
  shipped bundle. "Which section is it declared in" is the wrong question; "does it reach the bundle" is the
  right one.
- **Ignore the unfixable, explicitly.** Output that contains items nobody can act on teaches people to skip
  the output.

Automated dependency updates: group patches and minors, **exclude majors**, and treat the bot's lock file as
a notification — whoever lands it regenerates the lock in a stable environment. Check the first run of any
new ecosystem rather than assuming it worked: a path that matches nothing reports success.

## 6. CI cost is part of the design

Rerunning every integration and browser matrix on every push makes feedback progressively slower and spends
minutes without improving the loop.

Two tiers:

| Tier | Runs on | Contains |
|---|---|---|
| **Fast** | every push | lint, types, unit, the cheap validators |
| **Extended** | a label, a schedule, or the merge queue | integration, browser, matrix |

Then make sure the extended tier's trigger actually subscribes to the label event (§4) and that the required
checks are the ones that can run pre-merge (§4).

## 7. Repository rules leave gaps at the edges

- **Protecting only the default branch** leaves every intermediate branch updatable directly, so a review
  requirement between feature and integration branches is bypassed by pushing to the integration branch.
  Apply a companion ruleset to the intermediate pattern.
- **Tag protection prevents update and deletion but does not reject an unsigned tag** created by an
  authorised actor. Verify the annotated tag's signature if that is what you meant.
- **A bypass actor on one combined ruleset bypasses everything in it.** Split creation from
  immutability so a bypass for one does not grant the other.
- **"Require a pull request" plus a separate "restrict updates" rule, with no bypass actor, can lock out the
  maintainers** and the platform itself from merging a valid PR. Test the rule with the account that will
  have to use it.
- **A prefix check accepts refs the VCS cannot create** (`..`, trailing dot) and refs that are nested deeper
  than intended — `task/a/b` passes a `task/` prefix check while breaking a one-segment topology. Validate
  the format with the VCS's own checker, and validate the segment count separately. Calling an external
  checker once per item can be slow: batch it, or check the format in-process and shell out once.

---

## Gotchas

- **The gate that never fired is not evidence of health.** Before trusting a new check, make it fail on
  purpose and watch the pipeline go red. A check that has only ever been green has not been tested.
- **Generated evidence is a versioned schema**, not a shape to guess. An ad hoc assertion guessing camelCase
  against a snake_case schema rejects valid output — and the fix is to read the schema, not to add the other
  spelling.
- **A gate that lives on someone's machine is not a gate.** It must be in the repository or installed
  reproducibly; anything else is supplementary and must be labelled as such.
- **Validator startup dominates its own runtime** when each case spawns a fresh repository and process, and
  more so where endpoint protection inspects every launch. Batch the cases rather than optimising the checks.
- **When the platform is down, a strict remote-first sequence idles everything.** Decide in advance what
  local work may continue and what must wait for the gate, and write it down before you need it.

## Checklist

- [ ] The manifest enumerates every mandatory file, workflow and validator — including itself
- [ ] Contracts require non-empty content, not just a marker
- [ ] Candidate detectors are broader than the strict parser, and report the difference
- [ ] Security gates fail closed; nothing is skipped silently
- [ ] Structured files parsed and traversed, never regexed
- [ ] `permissions` validated at root **and** every job
- [ ] `pull_request.types` lists every type still needed; label triggers subscribed
- [ ] Required checks gate the PR head SHA, not a merge SHA that does not exist yet
- [ ] Annotations inspected, not just conclusions; actions pinned to SHAs
- [ ] Fast/extended tiers, with the extended trigger actually wired
- [ ] Images and artifacts pinned by digest; key identity pinned alongside the signature
- [ ] Dependency audit on every lockfile change; the published bundle tested, not the tree
- [ ] Rulesets cover intermediate branches; tag creation and immutability split

## Final report

```
Workflow/gate: <name>
Triggers: <events and types> — label-gated? subscribed? yes/no
Permissions: root <…> · jobs <…>
Required checks: <which, on which SHA>
Fail-closed: <what happens to what the gate cannot process>
Cost tier: fast <…> | extended <…>
Proven by failing on purpose: yes | no
```
