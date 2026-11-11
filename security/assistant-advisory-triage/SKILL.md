---
name: assistant-advisory-triage
description: "Decides what to do with an incoming security advisory, advisory draft, or vulnerability report such as a GHSA or CVE report: close, keep open, or keep open but narrow, checked against shipped releases. Use when triaging or dispositioning a reported vulnerability; not for threat modelling, code or dependency vulnerability audits (assistant-security), implementing a known fix, or writing release notes."
---

# Triage a Security Advisory

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](../../tools/progress/operating-guidance.md) for this activity. Keep the triage method, authority and completion evidence below; single-pass work needs no progress artifact.

Decide what a maintainer should do with an incoming security advisory, advisory draft or vulnerability report: `close`, `keep open`, or `keep open but narrow`. The common failure is closing a report because the fix is on main while a shipped release is still affected. Judge each advisory on its own evidence, and say how each fact was established.

## Method

Work through these checks in order. Each one can decide the verdict, so do not skip ahead.

1. **Trust model.** Read the project's published security policy or trust model first. A prerequisite that already sits inside trusted host, same-user, operator or plugin state is out of scope when the policy says so. If there is no policy, say so, state any trust-model premise you rely on as an explicit assumption, and do not close on that assumption: keep the advisory open and ask the maintainer to confirm the trust model.
2. **Shipped release.** Establish, with commands or artifacts you actually inspected:
   - the latest shipped release on each channel the project publishes (tags, package registry versions), plus any older lines the policy declares supported;
   - whether the vulnerable code is present in that release, for example by reading the file at the tag (`git show <tag>:<path>`);
   - whether any shipped release contains the fix, for example `git tag --contains <fix-commit>`.

   Being fixed on main, without a shipped release that contains the fix, is never by itself a reason to close.
3. **Exploit path.** Decide whether the report shows a real boundary bypass, as opposed to prompt injection alone, control by a same-host same-user process that could already read or write the state, or a helper whose semantics differ from documented configuration. When this needs fresh reachability or exploit-path analysis of the implicated code, hand that analysis to `assistant-security` and use its confirmed or needs-validation result.
4. **Duplicates.** Search published advisories, fixed issues and related pull requests for the same root cause. Name the canonical record when one exists; otherwise state what was searched.

## Verdict

- `close` only for one of these reasons: duplicate of an existing advisory or fixed issue (name it); invalid against shipped behaviour; out of scope under the project's security policy (cite it); or fixed before any affected release.
- `keep open` when a shipped release on a published or supported line is affected, including when the fix exists only on main.
- `keep open but narrow` when the bug is real but the stated severity or impact is overstated; say what the narrowed impact is.

If a deciding fact could not be established, say which and keep the advisory open rather than closing on an assumption.

## Hardening

Report any hardening suggestion separately from the verdict, labelled as not required for closure. Offer it only when it is concrete, low-risk and preserves intended user workflows. If it would need a product or security-model change, say so and do not present it as a required fix.

## Authority

Triage is read-only by default. Reading advisories, tags and published package versions through the user's available access is allowed when the user asked for triage. Post a comment, close, publish or edit an advisory, request a CVE, or contact the reporter only when the user's task authorizes that specific action; otherwise return draft text and post nothing. Follow the project's disclosure policy for public wording; without one, keep exploit detail out of draft public text and ask the user before including it. When the user authorizes a fix, hand off to `assistant-workflow`.

## Output

For each advisory, lead with its identifier or link, then a line of the form `Verdict: close`, `Verdict: keep open` or `Verdict: keep open but narrow`. Then give the evidence that decides it, in this order: trust-model reference; implicated code references; shipped-release facts with how each was established; duplicate search result. After that, the separate hardening note, any draft maintainer text, and what remains unverified.
