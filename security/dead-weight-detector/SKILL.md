---
name: dead-weight-detector
description: Analyze how much each direct OSS dependency is actually used in first-party code, cross-reference that against live maintenance-health signals from the package's own registry (release recency, maintainer count, download volume, known unpatched vulnerabilities), and recommend keep vs. replace with first-party code. Trigger this whenever the user asks "is this dependency worth keeping," "should we drop this package," "audit our dependencies," "which OSS packages are barely used," "should we inline this instead of using a dependency," "is X well maintained," or wants a dependency health check. Requires live network access for the health-check phase, unlike this plugin's other skills.
---

# Dead Weight Detector

## Why this skill exists

A dependency usually gets added for a good reason: a one-line import, one function call, problem solved. Nobody revisits that choice later. Each dependency added this way is a small, permanent liability: it has to be kept patched, it's a supply-chain trust surface, and if the upstream project goes quiet that risk just sits there, unreviewed, indefinitely.

[`cartridge-scanner`](../cartridge-scanner) already answers *what* dependencies exist and roughly how many. This skill goes one level deeper, per dependency: how much of it is actually used in first-party code, and is the package itself still a going concern? Then it renders a judgment: keep it, watch it, or replace it with first-party code that's fully under this team's control. Same evidence-gathered-mechanically, verdict-reasoned-qualitatively spirit as [`player-two-verdict`](../player-two-verdict) and [`tilt-check`](../tilt-check), not a score nobody can argue with.

## When to use this

- The user wants to know if a specific dependency, or the dependency set as a whole, is worth keeping.
- The user is deciding whether to inline a small piece of functionality instead of adding or keeping a dependency for it.
- The user wants a maintenance-health check on their dependencies: is anything effectively abandoned, single-maintainer, or carrying a known unpatched vulnerability in the version actually pinned.
- The user names a specific package and asks "should we drop this."

If the user just wants an inventory (what exists, how many, what package managers), that's `cartridge-scanner`'s job, run it first if that inventory doesn't already exist in the conversation.

## Step 0: Prerequisite check

Confirm `python3` is on PATH, `${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py` requires it and this skill can't run without it. If it's missing, stop and tell the user plainly.

Confirm the target path exists and is readable.

The `usage` phase (Step 1) is fully local and needs no network access. The `health` phase (Step 5) requires live network access to package registries, note that plainly up front so the user isn't surprised later, but don't block on it here, the usage-only path still works without network.

## Step 1: Run the local usage scan

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py usage <path>
```

Fully local, no network. Returns every direct dependency across all ten ecosystems `cartridge-scanner` covers (JavaScript via npm/yarn/pnpm, Python, Go, Java, Ruby, PHP, Rust, .NET, Dart, C/C++), each with `files_importing`, `call_site_count`, `distinct_symbols_used`, and a computed `usage_tier` (`minimal` / `light` / `moderate` / `heavy`).

These tiers are a starting heuristic, not a precise measurement. Two known sources of noise, say so if a specific result looks off rather than trusting the number blindly:

- **Regex-based symbol counting can overcount** when a bound identifier's name also appears inside the import path/module string itself (e.g. a package literally named the same as its own path segment). Read the actual call sites in Step 4 before trusting a borderline number.
- **Ruby, PHP, and C/C++ get a weaker signal** (`"usage_signal": "weak"` in the output). Dynamic dispatch and PSR-4 autoloading defeat static symbol matching for Ruby/PHP; a C/C++ `#include` doesn't bind a symbol at all, and mapping a header path to a Conan/vcpkg package name is a convention, not a registry-enforced rule. All three ecosystems' `call_site_count` is really just a `require`/`use`/`#include` occurrence count, not real usage depth. Treat these results as a starting point for manual review, not a verdict input on their own.

## Step 2: Full usage-tier table

Every direct dependency gets one row here, this is cheap (no network) and complete, it's the transparency layer even for dependencies that never get a full deep-dive below. Group by ecosystem, sort lowest-usage first within each group so the reader sees the interesting rows immediately.

## Step 3: Triage the deep-dive set

Select dependencies for the full workup (Steps 4-7):

- Any dependency at `minimal` or `light` usage tier, capped at **15 per run**. If more than 15 qualify, take the 15 with the lowest `call_site_count` and say plainly that the rest were left at the table-only level, same pattern as `player-two-verdict`'s finding cap.
- Any package the user explicitly named, regardless of its usage tier, this forces inclusion even for a `heavy`-tier dependency if that's specifically what they asked about.

Dependencies at `moderate`/`heavy` usage tier that weren't named by the user get one line in the table and nothing more, don't spend a health-check network call justifying something that's obviously earning its keep.

## Step 4: Read the actual call sites

For each triaged candidate, open the files from Step 1's `files_importing` list and read the real call sites, enough to describe in one or two plain-language sentences what the dependency is actually being used for. This is what makes Step 6's judgment call credible instead of a guess from the package name alone.

## Step 5: Run the live health check

Only for the names triaged in Step 3, this is what keeps network calls bounded:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py health <ecosystem> <repo_path> <name> [<name> ...]
```

`<repo_path>` is used to resolve each name's pinned version from the local lockfile. Read `${CLAUDE_PLUGIN_ROOT}/references/registry-health-signals.md` for exactly which fields are available per ecosystem and the tier thresholds, don't restate that table, cite it. Report `"n/a"` fields honestly as unavailable for that ecosystem, never imply a number that wasn't returned.

**Ignore the `vulnerabilities` field and the `health_tier` field entirely.** This skill does not evaluate CVE exposure, that's `patch-for-the-high-score`'s job; `health_tier` can come back `at_risk` purely because of a vulnerability match, which would make it a misleading input into a report that isn't reporting on vulnerabilities at all. Step 6 below derives its own status label directly from the remaining fields: `recency`, `maintainers`, `downloads`, `deprecated`, `abandoned`, `repository_url`, `archived`, and `registry_status`.

- `deprecated`: a maintainer-declared deprecation message (npm's `deprecated` field, or a fully-yanked latest release on PyPI). Quote the message directly rather than paraphrasing it.
- `abandoned`: a hit against the curated abandoned-package list (`{"reason": ..., "replacement": ...}`). When present, its `replacement` is the answer to feed into Step 7/8 directly instead of judging replacement complexity from scratch.
- `archived`: `true` if the package's GitHub repository is flagged archived (read-only), `null` if it's hosted somewhere other than GitHub or couldn't be resolved. GitHub-only coverage, see the reference doc for exactly which ecosystems this applies to.
- `registry_status`: `"not_found"` means the registry returned a 404, a confirmed absence, worth flagging as likely a private/internal package or a typo rather than presenting identically to `"failed"` (a transient network/timeout error, genuinely just unknown for now).

## Step 6: Derive a status label

Apply this decision list to every triaged dependency, top to bottom, first match wins, using only the fields named in Step 5:

1. **Abandoned** - `abandoned` is set.
2. **Deprecated / EOL** - `deprecated` is set.
3. **Archived** - `archived` is `true`.
4. **Unsupported** - release over 12 months old, or 0 maintainers found.
5. **Slowing** - release 3-12 months old, or a single maintainer, or low download volume, but still active.
6. **Supported** - recent release and (2+ maintainers or high download volume).
7. **Unknown (Not Found)** - `registry_status` is `"not_found"`.
8. **Unknown (Check Failed)** - `registry_status` is `"failed"`.

A dependency that was never triaged into the health-check set (moderate/heavy usage, not user-named) gets **Not Checked** in the full inventory table (Step 9), it was never run through this list at all.

## Step 7: Judge replacement complexity

This is the actual value this skill adds over a mechanical script: is what's being used trivial to hand-roll, or genuinely risky to reimplement? Calibration anchors:

- **Usually trivial to inline**: a single string-padding/formatting helper, a basic debounce/throttle, a small array/object utility (chunk, unique, flatten), a simple retry loop, a one-off validation regex wrapper.
- **Usually not worth reinventing**, even at low usage: anything cryptographic (hashing, signing, random token generation), timezone/calendar math, HTML/URL/SQL sanitization or escaping, parsers for a real format (JSON is fine to trust the stdlib for, a custom binary or config format usually isn't), anything implementing a security control (auth, CSRF, rate limiting).

State which bucket the used surface falls into and why, in one or two sentences, don't just assert it.

If Step 6 landed on **Abandoned**, skip the from-scratch judgment and name its `replacement` directly instead, that's a maintained, community-vetted answer rather than a guess at hand-rolling complexity.

## Step 8: Final verdict

One of four, always evidence-cited back to Steps 1-7:

- **KEEP**: `moderate`/`heavy` usage, or Status is **Supported** regardless of usage tier (a well-maintained, widely-used dependency used lightly is still fine, e.g. a small well-known utility with no real risk in carrying it).
- **CANDIDATE TO INLINE**: `minimal`/`light` usage tier AND the used surface was judged trivial to hand-roll in Step 7.
- **KEEP BUT WATCH**: usage tier is fine on its own, but Status is **Deprecated/EOL**, **Archived**, **Unsupported**, or **Slowing**. Not urgent, but flag it and recommend planning ahead rather than waiting for a forced migration.
- **NEEDS HUMAN JUDGMENT**: signals conflict (e.g. trivial-to-inline usage but Status came back **Supported** and widely relied upon elsewhere too), or Status is **Unknown**. Don't force a verdict the evidence doesn't support, say what's missing and what would resolve it.

Also name a concrete next action for every triaged dependency, not just the verdict label, e.g. "replace with `String.prototype.padStart`" or "migrate to `zoneinfo` (stdlib, Python 3.9+)", not just "inline it."

## Step 9: Write the report

### Voice

- No em dashes.
- Table-first for the risk overview and full inventory, bulleted (not narrative-paragraph) writeups for the triaged deep-dive set.
- Every usage claim traces to a `file:line`-style citation from Step 4. Every status claim traces to a named field from Step 5's output (`recency`, `maintainers`, `downloads`, `deprecated`, `abandoned`, `archived`), not a vague "looks unmaintained."
- State plainly whenever a signal came back `n/a` or `unknown`, don't paper over a gap with a confident-sounding sentence.
- Every table and list is sorted worst-status-first: Abandoned > Deprecated/EOL > Archived > Unsupported > Slowing > Supported > Unknown (Not Found) > Unknown (Check Failed) > Not Checked, so the reader sees what needs attention first without scanning the whole report. Ties break by usage tier ascending.

### Format

```
# Dead Weight Report: [repo/directory name]

## Risk Overview
| Dependency | Ecosystem | Status | Why | Next Action |
|---|---|---|---|---|
[one row per dependency whose Status is Abandoned, Deprecated/EOL,
Archived, or Unsupported, worst first]
[if none qualify: a single line saying so instead of an empty table]

## Summary

[one line per verdict category: counts and the standout names, so the
reader can act without re-reading the whole report]

## Legend

| Status | Meaning |
|---|---|
| Abandoned | Hit in the curated abandoned-package list, a maintained replacement is named. |
| Deprecated / EOL | Maintainer-declared deprecation (npm `deprecated`, or a fully-yanked latest PyPI release). |
| Archived | The package's GitHub repository is flagged archived (read-only). GitHub-hosted only. |
| Unsupported | Release over 12 months old, or 0 maintainers found, with no explicit deprecation/abandonment/archive signal. |
| Slowing | Release 3-12 months old, or a single maintainer, or low download volume, but still active. |
| Supported | Recent release and (2+ maintainers or high download volume). |
| Unknown (Not Found) | Registry returned a confirmed 404, likely private/internal or a typo. |
| Unknown (Check Failed) | Registry lookup failed transiently (network/timeout), genuinely unresolved. |
| Not Checked | Not in this run's health-check triage set (moderate/heavy usage, not user-named). |

| Usage Tier | Meaning |
|---|---|
| minimal / light | Below Step 3's triage threshold, eligible for the deep dive. |
| moderate / heavy | Above the triage threshold, table-only unless user-named. |

| Verdict | Meaning |
|---|---|
| KEEP | Earning its place, by usage or by Status. |
| CANDIDATE TO INLINE | Low usage and trivial to hand-roll. |
| KEEP BUT WATCH | Fine on usage, but Status flags a maintenance risk. |
| NEEDS HUMAN JUDGMENT | Signals conflict, or Status is Unknown. |

## Full Dependency Inventory

### [ecosystem]
| Dependency | Files | Call Sites | Usage Tier | Status |
|---|---|---|---|---|
[one row per direct dependency, Status severity first, usage tier
ascending as a tiebreak]
[repeat per ecosystem present]

## Deep Dive

### [dependency name] ([ecosystem])
- Usage: [files_importing] files, [call_site_count] call sites, tier [minimal/light/moderate/heavy]
- What it's used for: [1-2 sentences from Step 4, cited by file:line]
- Status: [status] - [the specific field/message backing it, e.g. the quoted
  deprecation message, or "recency 2015-03-24 (14mo), 1 maintainer"]
- Replacement complexity: [trivial / not worth reinventing / named replacement
  from the abandoned list], [why, 1 sentence]
- Verdict: [KEEP / CANDIDATE TO INLINE / KEEP BUT WATCH / NEEDS HUMAN JUDGMENT]
- Next action: [concrete step]

[repeat per triaged dependency, same Status-severity ordering]
```

If more than 15 dependencies qualified for the deep dive, note the cap and which ones were left at table-only level, per Step 3.

## Step 10: Offer to save

After producing the report, follow the save prompt defined in `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`. Frame it as something worth re-running periodically, dependency health drifts, a `KEEP` today can become `KEEP BUT WATCH` in six months without any code change on this side.

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/scripts/dead_weight_scan.py`: does the mechanical work, local usage-site scanning (Step 1) and live registry health lookups (Step 5). Reuses `cartridge_scan.py`'s file-discovery helpers but does not modify that script or its output.
- `${CLAUDE_PLUGIN_ROOT}/scripts/abandoned_packages.py`: the curated abandoned-package list `dead_weight_scan.py`'s health check consults, used in Steps 5-6.
- `${CLAUDE_PLUGIN_ROOT}/references/registry-health-signals.md`: which health signal is available per ecosystem and where it comes from, the OSV.dev ecosystem-name mapping, the GitHub-archived check's per-ecosystem repository URL sources, and the exact health-tier thresholds, used in Step 5.
- `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: the shared save-to-file convention, used in Step 10.
