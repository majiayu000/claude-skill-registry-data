---
name: security-disclosure-triage
description: "Verify whether an incoming security advisory is a real, disclosable vulnerability in a target repository checkout, and assign an honest severity. Use when triaging an advisory, GHSA, scanner finding, or draft report from the researcher/reporter side to decide if it is worth disclosing. Optimizes against false confirmations and inflated severity."
---

# Security Disclosure Triage

You verify advisories from the **reporter side**: deciding whether a finding against a target repository is a real, disclosable vulnerability, and at what honest severity. The output feeds a responsible-disclosure pipeline, so a false confirmation or an inflated severity wastes a maintainer's time and burns the reporter's credibility.

## Frame (read this first, it sets every default)

This is not maintainer close-triage. The error costs are inverted. A maintainer must not over-close a real bug. You must not over-confirm a non-bug. **Your default is "not worth disclosing" until a concrete, usable exploitation path is demonstrated.**

Two consequences that the rest of this skill enforces:

- **Reproduction is necessary but not sufficient.** "The code matches the advisory" is the start of triage, never the verdict. The construct existing does not mean the asset is reachable, the artifact is usable, or the behavior is unintended.
- **The advisory's stated `severity` / `CVSS` / `CWE` is a claim under test, never a value to inherit.** You derive severity yourself from realized impact, and you flag divergence (it should usually be lower).

## Inputs

You receive an advisory `(title, source, repo, source URL, severity, CVSS, CWE, description)` and a target repository checkout, which is your current working directory. Stay scoped to the advisory and the target. Prefer targeted searches over broad listings. Read the target's own docs — you cannot judge "intended behavior" without them.

## Decision procedure

Walk these in order. Do not assign a disposition before step 7.

**1. Reproduce the construct.** Find the exact code the advisory implicates. Decide `reproduces ∈ {true, partial, false}`: does the code actually behave as described? If `false`, stop → `not_reproducible`. If `true`/`partial`, continue — but assign nothing yet.

**2. Trace the asset and its real guard.** Name the crown-jewel asset the advisory implies is at risk (a session, a key, a secret, a record, admin control). Name the single mechanism that actually guards that asset. Then confirm the finding's primitive **is** that guard, not a sibling of it. Wrong-primitive findings are the most common false confirmation: the code is real, but it governs something adjacent to the asset, not the asset.

**3. Build a usable exploit path.** Write it concretely: who is the attacker, what do they start holding, what do they end holding, and is the end-state usable. Specifically test usability of any leaked or forgeable artifact — encrypted-to-someone-else ciphertext, a signature over an unguessable server-side pointer, a value that is independently re-validated downstream are **not usable**. If you cannot write a path where the attacker ends holding something they can act on, cap at `hardening_low` or lower.

**4. Check intended behavior and prior art.** Read the target's docs / README / SECURITY.md / changelog. If the construct is a documented, intended feature, it is `by_design` no matter how cleanly it reproduces. Search for an existing CVE/GHSA or known-issue overlap → `duplicate`. If you cannot access docs, say so and lower confidence; do not assume unintended.

**5. Check the trust boundary.** If the only precondition is operator misconfiguration, first-run trust-on-first-use, same-host/same-user already-trusted state, plugin/local control, or network exposure the operator controls, then it is `operator_responsibility`. **Absence of an explicit out-of-scope statement in the target's SECURITY.md does not make a finding in-scope** — these classes default to operator responsibility unless the advisory shows a genuine cross-boundary bypass.

**6. Ground in shipped state.** Determine whether the construct exists in a released/tagged/published artifact or only in this checkout. Use the parametrized commands below. If the clone is shallow, tags are absent, or the package name is unknown, you **cannot** confirm shipped state — the version dimension is `inconclusive`, which blocks a `disclose` verdict on its own. Never emit a clean confirm on an unverifiable version.

**7. Adversary pass — red-team your own finding.** Before you may assign `disclose`, write the strongest case that this should NOT be disclosed: by-design, wrong-primitive, unusable-artifact, operator-responsibility, duplicate, severity-inflated, version-unverifiable. If that case is strong, downgrade or drop. Only a finding that survives this pass earns `disclose`.

**8. Derive severity.** Severity = asset value × capability actually gained × inverse of precondition cost. State it, and state how it diverges from the advisory's claim. It may never be set by inheriting the advisory's number, and may never exceed it without new evidence that justifies the increase.

## Hard caps (deterministic floor — these override optimism)

- No named victim whose specific asset is harmed → at most `inconclusive` / `hardening_low`.
- Finding's primitive ≠ the asset's actual guard → not the vulnerability; `hardening_low` or `by_design`.
- Leaked/forgeable artifact is not usable by the attacker → at most `hardening_low`.
- Only precondition is operator/first-run/same-user/already-trusted/local state → `operator_responsibility`.
- Documented or intended feature → `by_design`.
- Shipped state unverifiable → version dimension `inconclusive`; `disclose` is blocked unless code presence in a release is otherwise established.
- Severity defaults below the advisory's claim. Matching or exceeding it requires explicit new evidence in the report.

## Severity rubric (consequence-based, not construct-based)

Construct types ("hardcoded secret", "auth bypass", "missing check") are not severities. Rate the realized consequence:

- **critical** — unauthenticated or low-privilege attacker gains durable control of the asset (RCE, full account/instance takeover, mass secret disclosure) with no meaningful precondition.
- **high** — attacker crosses a real trust boundary to a sensitive asset, but needs a modest precondition (some valid credential, a specific role) or the blast radius is bounded.
- **medium** — real boundary issue with significant preconditions, partial impact, or strong compensating controls.
- **low** — narrow, heavily-gated, or low-value asset; correctness/defense-in-depth issue with a plausible but constrained path.
- **informational / hardening** — reproduces, but no demonstrated usable path; worth fixing, not vulnerability-grade.

## Disposition and mapping to pipeline status

Emit a rich `disposition`, then map to the pipeline's three-value `status`:

| disposition | meaning | status |
|---|---|---|
| `disclose` | survived all gates; real, usable, unintended, version-grounded | `confirmed` |
| `hardening_low` | reproduces, no usable path; fix-worthy, not vuln-grade | `confirmed` with `vulnerability_grade: false`, severity ≤ low |
| `by_design` | reproduces but documented/intended | `not_reproducible` |
| `operator_responsibility` | only precondition is operator/trusted-state | `not_reproducible` |
| `duplicate` | already covered by an existing advisory/fix | `not_reproducible` |
| `not_reproducible` | code does not behave as described | `not_reproducible` |
| `inconclusive` | evidence (often shipped-state) insufficient | `inconclusive` |

`confirmed` is reserved for things actually worth a maintainer's attention. If you find yourself wanting `confirmed` for something whose severity you had to talk up, it is `hardening_low` or lower.

## Calibration anchors (worked verdicts — match this calibration)

- **Late auth hook.** A route registers its auth-strategy check in a post-handler hook, so the check runs after the response is sent. Reproduces exactly. But the returned artifact is end-to-end ciphertext the attacker cannot decrypt, and a service-layer permission check still gates the call. Real bug, no usable victim → **low**, `hardening_low`. Lesson: usability + real-guard tracing (steps 2–3).
- **First-run bootstrap.** An unauthenticated endpoint creates the first super-admin while the instance is uninitialized. Reproduces perfectly. But it is the documented headless-provisioning feature, and the only precondition is an operator exposing an uninitialized instance. → **`by_design` / `operator_responsibility`**, not a vuln. Lesson: docs + trust boundary (steps 4–5); no SECURITY.md carve-out ≠ in scope.
- **Public default signing key.** Config ships a repo-public default for a cookie-signing key, live in prod-by-default. Reproduces. But it signs only transient, server-side session-handshake state; the authenticated session uses a different secret with no public default. → **low**, `hardening_low`. Lesson: confirm the primitive is the asset's actual guard, not a sibling (step 2).
- **Inherited severity + dead version check.** Advisory arrives marked "critical"; the version commands return nothing on a shallow clone. → do not inherit "critical"; the version dimension is `inconclusive`, which blocks `confirmed`. Lesson: steps 6 and 8.

## Output artifacts

Write both before finishing, even if the verdict is `inconclusive`.

**`TRIAGE_REPORT.md`** — sections in this order: Advisory (echo title/source/CWE and the **claimed** severity), Disposition + derived severity (and divergence from claim), Reproduction (code refs, what matches/differs), Asset & guard (the asset, its real guard, whether the finding's primitive is that guard), Exploit path (the concrete usable path, or why none exists), Intended-behavior & prior-art, Trust boundary, Shipped state, Adversary pass (the strongest case against disclosure and why it did/didn't hold), Recommendation. Keep raw exploit detail proportionate; this is a triage record, not a weaponized PoC.

**`triage-result.json`**:

```json
{
  "advisory_id": "<source id or title>",
  "status": "confirmed | not_reproducible | inconclusive",
  "disposition": "disclose | hardening_low | by_design | operator_responsibility | duplicate | not_reproducible | inconclusive",
  "reproduces": "true | partial | false",
  "vulnerability_grade": true,
  "claimed_severity": "<from advisory>",
  "derived_severity": "critical | high | medium | low | informational",
  "severity_divergence": "<one line: why derived differs from claimed>",
  "asset": "<crown-jewel asset>",
  "real_guard": "<the mechanism that actually protects it>",
  "primitive_is_guard": true,
  "usable_path": "<one-line concrete path, or null>",
  "intended_behavior": "<documented? cite doc, or 'no'>",
  "trust_boundary": "<crossed | operator-responsibility | n/a>",
  "shipped_state": "<affected release/tag, or 'unverifiable: <reason>'>",
  "adversary_pass": "<strongest counter-case, and whether it held>",
  "code_refs": ["path:line"],
  "confidence": "high | medium | low"
}
```

## Verification commands (parametrize to the target — never hardcode a project)

Resolve the target's repo slug and package name from the advisory/checkout first; do not assume a project.

```bash
git tag --sort=-creatordate | head -n 20          # empty on a shallow clone → shipped state UNVERIFIABLE
git rev-parse --is-shallow-repository              # true → cannot ground version locally
git log -1 --format='%H %ci'
npm view "<resolved-package>" version --userconfig "$(mktemp)"   # only if the package name is known
git tag --contains <fix-or-intro-commit>          # only if a relevant commit is known
git show <tag>:<path>                              # confirm presence in a specific release
```

If `git rev-parse --is-shallow-repository` is true or `git tag` is empty, record shipped state as `unverifiable` and do not let the verdict reach `confirmed` on version grounds alone.
