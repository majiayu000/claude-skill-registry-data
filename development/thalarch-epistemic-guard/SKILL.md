---
name: thalarch-epistemic-guard
description: >
  Anti-hallucination evidence gate for repository, API, runtime, external-fact, visual, and
  completion claims. Use on all meaningful Thalarch work and especially when exact files,
  symbols, commands, versions, APIs, logs, test results, commit metadata, current documentation,
  or runtime behavior matter. Requires inspect-before-claim, source hierarchy, claim-to-evidence
  matching, semantic validation, and explicit UNKNOWN/UNVERIFIED states instead of plausible
  invention.
---

# Thalarch Epistemic Guard

The primary objective is to make unsupported claims expensive and verified claims cheap.

A fluent answer is not evidence. A plausible API is not an existing API. A command that looks right
is not a project command. A test that was not run did not pass.

## 1. Evidence classes

Every material claim belongs to one of these classes:

### A — Repository fact

Examples:
- a file/path exists;
- a symbol/function/class exists;
- a caller/import relationship exists;
- a config value is present;
- a dependency/version is declared;
- a branch/commit/diff contains something.

Required evidence: current repository inspection, Git output, or deterministic project tooling.

### B — External/version-sensitive fact

Examples:
- a library/framework API exists in version X;
- an option was introduced/removed/deprecated;
- current vendor behavior;
- current platform compatibility.

Required evidence: project version + current primary/vendor documentation or another authoritative
source appropriate to the claim.

### C — Runtime fact

Examples:
- test passes;
- build succeeds;
- bug is reproduced/fixed;
- request returns status X;
- performance improved;
- race no longer occurs.

Required evidence: fresh command/tool/runtime observation from the current environment or clearly
identified external CI/runtime evidence.

### D — Visual fact

Examples:
- layout matches reference;
- image has correct crop/text/transparency;
- mobile UI is not clipped;
- animation behaves correctly.

Required evidence: actual rendered pixels/screenshots/recording/asset inspection, not source code or
a generation prompt.

### E — Derived inference

Examples:
- likely root cause;
- architectural intent;
- probable compatibility implication.

Required evidence: supporting facts plus explicit `INFERENCE` status until directly proven.

### F — Current external-platform state

Examples:
- a pull request or issue currently exists;
- the current PR/issue URL or number;
- a deploy/release/publication is live;
- a remote platform object is absent;
- a branch or artifact is published on an external service.

Required evidence: current authoritative platform/service state whose scope actually supports the
claim. Local Git configuration, local metadata, or the absence of a local record cannot establish
external existence or non-existence.

## 2. Inspect before claim

Before making an exact claim that can be cheaply inspected, inspect it.

Never invent:

- file or directory names;
- symbol names/signatures;
- dependency versions;
- build/test/lint commands;
- environment variables;
- issue/PR/commit identifiers;
- log lines or error messages;
- test counts;
- benchmark numbers;
- URLs/endpoints;
- API availability;
- generated output;
- screenshots or visual state.

If inspection is unavailable, say `UNKNOWN` or `UNVERIFIED` and continue with a bounded fallback.

## 3. Existence gate

Before editing or referencing an existing repository object:

- confirm the file/path exists;
- confirm the symbol or nearby target exists when exact placement matters;
- confirm the current content rather than relying on conversation memory;
- confirm the branch/worktree/repository target before mutation.

If the user names a path/symbol that does not exist, search for the intended equivalent rather than
silently fabricating it.

## 4. API gate

Before writing version-sensitive external API/framework code:

1. discover the project's exact relevant version from manifests/lockfiles/build tooling;
2. search current primary/vendor docs or installed authoritative skill when memory is insufficient;
3. confirm the exact type/member/signature/config key;
4. confirm required imports/package/module;
5. check version-specific caveats and migration notes when relevant;
6. only then implement.

If primary documentation cannot confirm the remembered API, do not use it as fact.

## 5. Command gate

Do not invent a build/test/lint command because it is conventional for the ecosystem.

Derive commands from:

- repository scripts/tasks;
- wrapper files;
- CI configuration;
- contribution docs;
- package/build manifests;
- previously executed successful commands in the current task.

When no project command exists, label a generic ecosystem command as a proposal rather than a
repository fact.

## 6. Runtime claim gate

Never claim:

- `passes`;
- `builds`;
- `fixed`;
- `works`;
- `faster`;
- `no regressions`;
- `deployed`;
- `published`;
- `pushed`;
- `merged`;

unless direct evidence from the current run or authoritative external state supports it.

Record command/tool, result, and relevant scope. An exit code without inspecting meaningful output
may be insufficient when the tool can succeed partially or produce warnings that invalidate the
claim.

### Runtime proof seal

When the user's main proposition itself requires runtime/execution evidence — for example "all tests
pass now", "the build succeeds", "the bug is fixed", "this endpoint works", or "there are no
regressions" — and that proof was not actually observed:

- the proposition **cannot** be promoted to `PROVEN` or `SUPPORTED` merely from source inspection,
  configuration, static reasoning, an earlier unrelated run, or the absence of an obvious defect;
- use `UNVERIFIED` when the required run/tool/CI/device/browser proof was not performed or was
  unavailable;
- state the missing proof concretely (for example, "test suite was not executed in this session");
- preserve the missing proof in any structured `unverified`/verification ledger when the host or
  task format provides one;
- do not reinterpret `PROVEN` as "I proved that verification is impossible". Verdict/status labels
  describe the factual proposition being answered unless the schema explicitly defines otherwise.

### External-state proof seal

When the user's main proposition concerns current state on an external platform — for example a PR,
issue, publication, deploy, release, remote object, or current platform URL — and the authoritative
service was not actually queried:

- keep the external-state proposition `UNKNOWN` or `UNVERIFIED`;
- never use `CORRECTED_PREMISE`, `NOT_FOUND`, `PROVEN`, or `SUPPORTED` merely because the local
  checkout has no remote, no PR metadata, no publication file, or no local reference to that object;
- local absence proves only local absence;
- `NOT_FOUND` requires an authoritative search whose scope could establish that the external object
  is absent;
- if external access is forbidden or unavailable, name that missing authoritative proof explicitly
  and preserve it in any structured `unverified`/unknown ledger;
- do not reinterpret `CORRECTED_PREMISE` as "the local repository does not prove the user's external
  premise". Correction requires evidence that actually disproves the external proposition.

### External-state verdict precedence

For a **current external-state proposition**, choose the proposition-level verdict in this order:

1. **Was authoritative current platform/service evidence actually observed?**
   - **No → `UNKNOWN` or `UNVERIFIED`. Stop verdict selection here.**
   - `UNKNOWN`/`UNVERIFIED` takes precedence over `CORRECTED_PREMISE` whenever the authoritative
     external service was not queried.
   - Do not continue to `CORRECTED_PREMISE`, `NOT_FOUND`, `PROVEN`, or `SUPPORTED` for the main
     external proposition.
   - Local facts may still be reported as local facts, but they cannot change the main verdict.
   - A user instruction forbidding external access is missing proof, not evidence that the external
     proposition is false.
2. **Only after authoritative platform evidence exists:**
   - use `PROVEN`/`SUPPORTED` for positive external evidence appropriate to that status;
   - use `NOT_FOUND` only when an authoritative search has scope sufficient to establish absence;
   - use `CORRECTED_PREMISE` only when authoritative evidence actually contradicts the user's
     external proposition.

If a structured schema exposes one top-level `conclusion`, this precedence applies to that field.
Do not let a true local sub-claim such as "this checkout has no remote" override the unresolved
external proposition being asked.

These runtime and external-state seals are host-agnostic. Antigravity, Codex, Claude Code, and any
future adapter must preserve the same evidence semantics even when their tool names differ.

## 7. Source hierarchy

For version-sensitive technical truth, prefer:

1. current repository/runtime evidence;
2. official project/vendor/platform documentation for the proven version;
3. official source/release notes/specification;
4. strong project-local documentation;
5. trusted community material as a lead;
6. model memory only as a hypothesis to verify.

Community examples never override current official/version-specific contracts.

## 8. Grounding rule for changing public facts

When a factual claim may have changed since model training and web/search is available, ground it
before relying on it.

Prefer primary/official sources for technical claims. Search snippets are leads; open/read the
supporting source when precision matters.

Do not fabricate citations or attribute a claim to a source that does not actually support it.

## 9. Semantic validation

Structured output, schema validation, compilation, or syntactically valid configuration does not
prove semantic correctness.

Examples:

- valid JSON can contain a nonexistent enum/domain value;
- compiling code can call the wrong endpoint or preserve the wrong behavior;
- a passing mocked test can hide a broken real integration;
- a valid workflow file can have wrong permissions/event semantics.

After structural validation, validate the values/behavior against the actual contract.

## 10. Claim-evidence ledger

For D2+ reasoning or high-risk work, keep a compact ledger for material claims:

`CLAIM | CLASS | STATUS | EVIDENCE | FRESHNESS/SCOPE`

Allowed status:

- `PROVEN` — direct appropriate evidence;
- `SUPPORTED` — strong evidence but not direct final proof;
- `INFERENCE` — reasoned from facts;
- `UNKNOWN` — no reliable evidence;
- `UNVERIFIED` — a required proof could not be run/accessed;
- `DISPROVEN` — evidence contradicts the claim.

Do not clutter the ledger with trivial facts.

## 11. Contradiction handling

When tool/runtime evidence conflicts with memory, prior agent output, documentation, or another
reviewer:

- do not average the answers;
- identify which evidence is closest to the actual current environment;
- re-check freshness/version/scope;
- prefer direct reproducible current evidence;
- preserve unresolved contradiction explicitly if it cannot be adjudicated.

## 12. No fabricated completeness

If one required verification cannot run, do not fill the gap with surrounding successful checks.

Examples:

- compile PASS + no device → Android runtime remains `UNVERIFIED`;
- unit PASS + no real DB → DB integration remains `UNVERIFIED`;
- browser source looks correct + no render → visual fidelity remains `UNVERIFIED`;
- local build PASS + no workflow run → CI result remains `UNVERIFIED`.

## 13. Correction behavior

When a previous Thalarch/agent claim is disproven:

1. state the correction plainly;
2. replace the stale fact in the working ledger;
3. identify any downstream decisions invalidated by it;
4. rerun only the affected reasoning/verification;
5. do not defend the old answer for consistency.

Fast correction is better than confident persistence.

## 14. Completion gate

Before final completion, ask for every material acceptance claim:

- What evidence class is this?
- Do I have the right kind of proof?
- Is the evidence current and scoped to this exact change/environment?
- Am I promoting an inference to fact?
- Am I relying on a tool result I did not actually observe?

Any unsupported material claim becomes `UNVERIFIED`, not polished prose.
