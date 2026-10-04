---
name: workflow-security-report
description: Triage a GitHub code-scanning (CodeQL) finding and produce an immutable Markdown triage report plus an index row, recommending remediation or dismissal, with a permalink pinned to the finding's commit SHA for every code reference so the report stays valid after the code moves. Use when triaging, dismissing, or remediating a code-scanning or CodeQL alert or finding; writing a security finding report; recording why an alert is a false positive or how it was fixed; or maintaining security/code-scanning/index.md and the SECURITY.md triage reference. Takes a finding number or finding URL, fetches details with the gh CLI, assumes the current repository when only a number is given, and refuses findings that do not exist or are already closed. Not for Dependabot or dependency alerts, secret-scanning alerts, runtime incident response, or writing a threat model.
license: MIT
---

# Triage a code-scanning finding

Turn an open GitHub code-scanning (CodeQL) alert into a Markdown triage report that recommends
**remediation** or **dismissal**, recorded under `security/code-scanning/`. Reports are **immutable
once the finding is closed**, so every reference to repository code is a permalink pinned to the
finding's commit SHA — it must still resolve after the code moves or the line shifts.

## 1. Resolve the finding

The argument is a finding **number** or a finding **URL**.

- URL `https://github.com/<owner>/<repo>/security/code-scanning/<n>`: parse `<owner>`, `<repo>`, and
  `<n>` from it.
- Bare number `<n>`: the finding is in the **current repository**. Resolve it with
  `gh repo view --json nameWithOwner -q .nameWithOwner`.

## 2. Fetch the finding and guard

```sh
gh api repos/<owner>/<repo>/code-scanning/alerts/<n>
```

Stop and tell the user — writing nothing — if:

- the call 404s (the finding does not exist, or you lack access); or
- `.state` is not `open` (a `dismissed` or `fixed` finding is **closed**; its report is immutable and
  must not be re-triaged).

If the finding's details have already been provided to you (for example pasted into the prompt), use
them directly and skip the `gh` call.

## 3. Pin to the commit SHA

The immutable anchor is `.most_recent_instance.commit_sha`. Every reference to repository code in the
report — the flagged line and anything you cite in your analysis — is a GitHub permalink built from it:

```text
https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<line>
```

and the commit itself links `https://github.com/<owner>/<repo>/commit/<full-sha>`. Never reference
code by branch name, `HEAD`, or a relative path — those drift; the SHA does not.

See [reference.md](reference.md) for the full map from `gh api` fields to report fields (rule id, CWE,
tool version, severity, location columns, detection date).

## 4. Analyze and recommend

Read the flagged code **at that SHA** and decide:

- **False positive → dismiss.** Explain why the rule does not apply here (the taint premise fails, the
  value is bounded, the path is unreachable, …) and recommend dismissing in the code-scanning UI.
- **True positive → remediate.** Describe the fix and, once it lands, the commit that makes it, and
  recommend remediation.

Be concrete and verifiable — cite the surrounding code by permalink, not by assertion.

## 5. Write the report

Copy [templates/report.md](templates/report.md) to `security/code-scanning/<n>.md` (create the
directory on first run) and fill every placeholder. Keep the section order: `What CodeQL reported`,
then `Why this is a false positive` **or** `Remediation`, then `Resolution`. Set **Outcome** to
`False positive`, `Remediated`, or `Pending` — use `Pending` while the recommendation is made but the
finding is still open.

## 6. Update the index

If `security/code-scanning/index.md` does not exist, create it from
[templates/index.md](templates/index.md). Append one row linking the finding's GitHub alert, its
`./<n>.md` report, and the Outcome.

## 7. Ensure the SECURITY.md reference

Make sure the repository's `SECURITY.md` points at the triage index. If it lacks the section, add:

```markdown
## Code scanning triage

CodeQL findings are triaged in
[`security/code-scanning/index.md`](security/code-scanning/index.md), with a report per finding
recording why it was dismissed or how it was remediated.
```

If `SECURITY.md` does not exist at all, tell the user rather than inventing a full security policy, and
offer to create one containing this section.

## Immutability rules

- Never edit a report whose finding is closed. When CodeQL re-detects the same issue after code moves,
  it closes the old alert and opens a new number — that gets a **new** report which cross-links the
  old one by number and `./<n>.md`, rather than an edit to the closed report.
- Because every code reference is a SHA permalink, the report keeps resolving after the code moves —
  that is the whole point of pinning.
