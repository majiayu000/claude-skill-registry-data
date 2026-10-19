---
name: variant-analysis
description: >
  After one vulnerability is confirmed, find its siblings: extract the root
  cause, generalize it in steps (exact, structural, semantic), search the
  codebase and its history with grep, Semgrep, and manual tracing, and record
  coverage so the hunt has a stopping point. Use when a bug was just fixed or
  reported and you need to know where else the same mistake exists, or when
  turning a CVE or advisory into a codebase-wide check. Not for first-pass
  auditing (use security-code-review) or deciding if one finding is real
  (use vulnerability-validation).
compatibility: >
  Agent Skills-compatible coding agents with read access to the repository;
  ripgrep and Semgrep optional. Semgrep example verified with CLI 1.174.0.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "security, variant-analysis, root-cause, semgrep, ripgrep, code-search, regression"
  topics: "security, code-review"
---

# Variant Analysis

Bugs cluster. The same author, the same copied snippet, the same misunderstood API, or the same missing helper produces the same flaw several times. Variant analysis turns one confirmed bug into a bounded, recorded search for its relatives. Defensive and authorized only: search code you are permitted to review.

Related skills: `vulnerability-validation` (the seed must be confirmed first), `semgrep-rule-authoring` (turning the pattern into a tested rule), `security-differential-review` (finding the introducing commit), `secure-coding` (the fix).

## Non-negotiable rules

1. Start from a confirmed seed bug with a known fix. A guess is not a seed.
2. State the root cause in one sentence before searching. Searching for the syntax of the seed finds only clones.
3. Record every query and its hit count. Coverage you cannot show did not happen.
4. Triage hits individually; a regex hit is a candidate, not a finding. Hand candidates to `vulnerability-validation`.
5. Read-only analysis. Do not run suspicious code from the repository to "see what happens" outside a sandbox.

## Workflow

### 1. Extract the root cause
Ask four questions about the seed: what untrusted value, what dangerous operation, what control was missing or wrong, and why did the author get it wrong (misread API, forgot a path, trusted a caller, copied code)? The last answer predicts where variants live.

Example root cause: "a request-derived filename is joined onto a base directory and opened without checking the resolved path stays inside the base (CWE-22)".

### 2. Build the generalization ladder
Search at each rung, widening only as hits stay informative.

| Rung | Search for | Tool |
| --- | --- | --- |
| Exact | The seed's literal snippet and its clones | `rg -n -F 'literal'` |
| Structural | Same API, any arguments: every call to the dangerous function | `rg -n 'open\('`, Semgrep pattern |
| Semantic | Same flaw via different APIs, wrappers, aliases, or languages: other file-opening helpers, `send_file`, archive extraction, template includes | Semgrep taint rule, manual tracing |
| Contextual | Same author, same module, same feature, same era | `git log --author`, `git blame`, sibling handlers |
| Cross-repo | Forks, copies, sibling services, vendored code, other languages implementing the same protocol | Same queries per repository (authorized only) |

### 3. Find the hiding places
- Sibling handlers of the vulnerable endpoint (export, download, preview, thumbnail, backup).
- Other callers of a helper whose contract was misunderstood.
- Older versions of the file: `git log -S'os.path.join' -- path` shows where the pattern entered.
- Wrapper functions that rename the dangerous API; search for the wrapper too.
- Test helpers and admin tooling that reuse the pattern.
- Generated or templated code that stamps the pattern repeatedly; fix the generator.

### 4. Encode the pattern as a rule when it recurs
Write a Semgrep rule following `semgrep-rule-authoring`, with the seed as a `ruleid:` test and the fix as an `ok:` test. Tested example for the root cause above (Semgrep 1.174.0, all annotated lines passed, see [references/semgrep-example.md](references/semgrep-example.md)): a taint rule from `flask.request.args.get(...)` to `open(...)`, with `secure_filename` as sanitizer. It flagged both the seed (`download`) and a variant that builds the path in an intermediate variable (`export`), and stayed quiet on the sanitized version. Known blind spot: it does not recognize a `realpath` containment check, so a correct fix written that way would be a false positive.

### 5. Triage and record
Table each candidate: location, query that found it, verdict (vulnerable, safe because X, needs validation), evidence level. Safe-because reasons are valuable; they show which guards the codebase relies on.

### 6. Decide when to stop
Stop when (a) the last two rungs yielded no new true positives, (b) every call site of the dangerous API is classified, and (c) the remaining unclassified hits are listed. Then fix the root cause once, preferably with a shared safe helper or a lint/Semgrep guard, rather than patching each site differently.

## Worked example

Seed: advisory says `GET /download?name=` allowed `../` traversal; fix added `secure_filename`.
- Root cause: request filename joined and opened, no containment.
- Exact rung: `rg -n 'os.path.join\(BASE' ` finds 2 more identical joins in `download` neighbors.
- Structural rung: `rg -n 'open\(' app/` returns 31 hits; 6 take values derived from requests.
- Semantic rung: grep for `send_file(`, `send_from_directory(`, `tarfile.extractall(`, `shutil.unpack_archive(` finds an archive-import endpoint that extracts user archives without member path checks (same class: CWE-22, different API).
- Contextual rung: `git blame` shows the `export` handler was written by copying `download` before the fix.
- Result table: 3 vulnerable, 5 safe (constant paths), 1 needs validation. One shared `safe_join(base, name)` helper replaces the patches, and the Semgrep rule runs in CI.

## Anti-patterns

- Searching only for the seed's exact text.
- Stopping at the first variant, or never stopping; no recorded coverage means no end.
- Treating every grep hit as a vulnerability and flooding the owner.
- Fixing each variant differently, creating new inconsistencies.
- Ignoring other languages and services that implement the same logic.
- Writing the rule but not testing it against both the seed and the fix.

## Verification checklist

- [ ] Seed confirmed and fix known
- [ ] Root cause written as one sentence
- [ ] Queries and hit counts logged for each rung used
- [ ] Every candidate classified with a reason
- [ ] Root-cause fix or shared helper proposed; recurring pattern encoded as a tested rule
- [ ] Stop condition stated; unclassified remainder listed

## References

- [references/semgrep-example.md](references/semgrep-example.md): tested variant rule
- [references/scenarios.md](references/scenarios.md): activation and evaluation scenarios
- [references/sources.md](references/sources.md): sources and provenance
