---
name: ios-code-audit
description: Use when the user asks for a "code audit", "comprehensive review", "find tech debt", "what should I clean up", or similar broad-scope assessment of a Swift project. Run a thorough audit of an iOS / macOS Swift codebase — bugs, dead code, duplication, Swift concurrency issues, deprecated APIs…
---

# iOS Code Audit Skill

## Operating rules

- **Read-only investigation, single deliverable.** No code changes — the output is `CODE_AUDIT.md` at the repo root.
- **Every finding cites `path/to/file.swift:LINE` (or a line range).** "Throughout the codebase" is never acceptable for a Critical or High item.
- **Severity is assigned conservatively.** Critical means crash / data loss / memory corruption / security exposure. Don't inflate. See the severity guide below.
- **Verify every Critical claim before propagating.** Agents will sometimes overstate severity. Open the cited file and confirm the bug is real. If you can't reproduce the claim by reading the lines, demote or drop.
- **Group by root cause, not by occurrence.** If one missing `@MainActor` annotation triggers seven warnings, that's one finding listing the seven sites, not seven findings.
- **`Dead/` (or any explicitly-archived directory) is excluded.** Check `CLAUDE.md` / project README for any "do not edit" directories before launching agents.

## Workflow

### Step 1 — Scope the codebase

Quick measurements to brief the agents:

```bash
find . -name "*.swift" -not -path "./.git/*" -not -path "./Dead/*" -not -path "*/Pods/*" -not -path "*/.build/*" | xargs wc -l 2>/dev/null | tail -1
find . -name "*.swift" -not -path "./.git/*" -not -path "./Dead/*" 2>/dev/null | wc -l
find . -name "*.metal" 2>/dev/null | wc -l
```

Also identify the **hot-spot files** (largest LOC, central state):

```bash
find . -name "*.swift" -not -path "./.git/*" -not -path "./Dead/*" -exec wc -l {} \; | sort -rn | head -10
```

Read `CLAUDE.md` if present — it usually flags central state files (e.g., `AppState.swift`, `CaptureState.swift`), the rendering pipeline, and any intentionally-excluded directories.

### Step 2 — Capture compiler ground truth

Run a build and extract every warning. This becomes the canonical input for the concurrency / deprecation portions of the audit — you should never have to *guess* whether concurrency warnings exist.

**Preferred (Xcode MCP, if connected):**

```
mcp__xcode__XcodeListNavigatorIssues(tabIdentifier, severity: "warning")
```

This returns a structured list with `path`, `line`, `message`, `severity`. Deduplicate (multi-target compilation produces duplicates) and bucket by root cause.

**Fallback (`xcodebuild` from CLI):**

```bash
xcodebuild -project <Project>.xcodeproj -scheme "<Dev scheme>" -configuration Debug build 2>&1 \
  | grep -E "warning:" | sort -u
```

If the build is incremental (returned in <2s), it likely skipped most files. Touch a Swift file under each target or run `clean build` to get a complete warning set.

### Step 3 — Launch the three parallel Explore agents

**One message, three tool calls.** Each agent gets a focused brief from `references/agent-prompts.md`:

- **Agent A — Concurrency & API modernity.** Feed it the warnings captured in Step 2.
- **Agent B — Dead code, duplication, refactor candidates.** Feed it the hot-spot list and any known-stale files from `CLAUDE.md`.
- **Agent C — Bugs, logic errors, security, performance.** Feed it the hot-spot list and any specific subsystems the user has called out (camera pipeline, IAP, API client, etc.).

Each brief enforces the per-finding template (see below). Do not let agents return summaries — insist on specific file:line findings.

### Step 4 — SwiftUI expert pass (if SwiftUI is in use)

If the project has SwiftUI views, invoke the `swiftui-expert-skill` separately *after* the agents return, scoped to `Views/` (or wherever the SwiftUI surfaces live) plus shared UI helpers. Ask specifically for:

- `@State` / `@Bindable` / `@Observable` misuse
- Modifier ordering bugs
- View-body work that should be hoisted (formatters, decoders, sorts)
- Accessibility / Dynamic Type / dark-mode gaps
- Missing `Equatable` on hot leaf views
- Liquid Glass / iOS 26 adoption opportunities (only if requested)

You may need to read a few view files yourself to confirm patterns the skill identifies.

### Step 5 — Verify the Critical findings

Before writing the report, **open the cited lines for every Critical-flagged finding** and confirm:

- The code matches what the agent described.
- The impact claim is real (e.g., if an agent says "memory corruption," is the buffer actually undersized? Trace the math.).
- The recommended fix is sensible.

This step has caught hallucinated severity in prior runs. Demote or drop items that don't pan out. **Never propagate a Critical you haven't personally verified.**

### Step 6 — Synthesize `CODE_AUDIT.md`

Use the skeleton in `references/report-template.md`.

**Mandatory: the rendered report must include section numbers in every heading.** This is not cosmetic — it is the report's primary interface. Users file issues like "fix §5.4" and "is §3.1 done?", and they cannot do that if headings are unnumbered. **Generating an unnumbered report is a defect, not a stylistic choice.** Reports without numbers will be rejected.

The numbering rules:

- **Top-level sections are numbered `## 1.` through `## 12.`** — exactly as listed below, in this order, even if a section has no findings (in which case write "_No findings._" under the heading rather than omitting the section).
- **Every finding is a numbered subsection** of the form `### N.M <short title>` where `N` is the parent section number and `M` increments from 1. Example: `### 5.1 Force-unwrap on Bundle.main.url`, `### 5.2 Missing .limited Photos auth handling`. **Never** emit a finding as `### <short title>` without the `N.M` prefix.
- **Numbers are stable across edits.** If a finding is removed during revision, leave the number and write `_REMOVED: <reason>_` as the body — do not renumber the surviving findings, or every external reference to "§5.4" breaks.
- **Executive summary items** (§1) are an ordered list `1.`, `2.`, … referencing the underlying numbered finding (e.g., "**[Critical] Force-unwrap on Bundle.main.url** — §5.1 — `path:line`").
- **Verification entries** (§12) reference findings by their subsection number, e.g., `- **§5.1** — open \`path\`, lines 42-47.`. Do not leave `<N.M>` placeholders from the template — fill them in.

Top-level sections, in order:

1. **Executive summary** — 5-10 highest-impact findings, one line each, with severity tag and a §N.M back-reference.
2. **Quick wins** — ≤30-minute fixes (delete stale files, remove debug `print`s, fix unused-let warnings, add accessibility labels).
3. **Concurrency**
4. **API modernity** — deprecations, iOS-17+ replacements
5. **Bugs / logic errors**
6. **Security**
7. **Performance**
8. **SwiftUI / UI**
9. **Dead code / duplication / refactor**
10. **Cross-cutting recommendations** — patterns worth applying repo-wide
11. **What was NOT audited** — explicit out-of-scope list
12. **Verification** — for each Critical/High, the exact lines that prove the claim

Per-finding template (note the leading `N.M`):

```markdown
### N.M <short title>
- **Location:** `path/to/file.swift:LINE-LINE`
- **What:** <observed problem in one sentence>
- **Why:** <impact / why it matters>
- **Action:** <recommended fix; no code, reference patterns>
- **Severity:** Critical | High | Medium | Low
```

Total length is comprehensive but scannable — aim for 50-100 findings. Group similar occurrences under one heading if a category has many instances (list the top 5-10 specific examples plus a count of the rest).

## Severity guide

- **Critical** — Likely to cause crashes, data loss, memory corruption, security exposure, or shipping the wrong server URL to production. Open the cited line yourself before assigning this.
- **High** — Real bug a user can hit; compiler warning that will become an error in a future Swift mode; a deprecated API that's actively being removed; an architectural concurrency issue.
- **Medium** — Performance / quality issue; refactor candidate; missing modernization with no functional bug.
- **Low** — Naming, cosmetic, code style, single-occurrence cleanup.

## Quality bar (final check before delivering)

- [ ] **Every top-level section is numbered `## 1.` through `## 12.`** and every finding is a numbered subsection `### N.M <title>`. Skim the rendered report — if any heading is missing its number, fix it before delivering. Reports without numbers will be rejected as defective.
- [ ] **Executive summary entries reference findings by §N.M**, and Verification entries do too — no literal `<N.M>` placeholders survived from the template.
- [ ] Every Critical and High finding has an exact line range. No "throughout the codebase."
- [ ] Concurrency findings cross-reference the actual Step-2 warning list.
- [ ] At least 3-5 Critical findings have been spot-verified by opening the cited file.
- [ ] Findings are grouped by root cause (one annotation → many warnings = one finding).
- [ ] The "What was NOT audited" section is explicit so the user knows the gaps.
- [ ] Report is ≤ ~80 distinct findings — bigger reports lose actionability.
- [ ] No code is included in the report itself — recommendations describe patterns, not implementations.
- [ ] The user can pull any single finding into a separate task without re-explaining context.

## Skill output

Always write to `CODE_AUDIT.md` at the **repo root** (the user's project working directory). Overwrite if it already exists — this skill produces a snapshot, not an append log. If the user wants history they can `git mv` previous versions before invoking.

## What this skill does NOT cover

- **Algorithmic correctness of Metal kernels / domain-specific code.** Surface obvious issues only; deep algorithmic review is out of scope.
- **Build settings, scheme configuration, Xcode project structure.** Beyond what's visible in shared schemes.
- **Third-party dependency internals.** SPM / CocoaPods packages are treated as black boxes.
- **Test coverage assessment.** Quick scan of test targets is fine; deep test review is a separate skill.
- **Localization correctness.** Audit can note untranslated strings but not assess wording.
- **Performance profiling.** The skill identifies *potential* hot paths (per-frame allocations, broad state, etc.) but doesn't run Instruments traces. For that, invoke `swiftui-expert-skill` and its trace tooling separately.

## References

- `references/agent-prompts.md` — The three Explore-agent briefs (copy-paste-ready, fill in the project context).
- `references/report-template.md` — Full skeleton for `CODE_AUDIT.md`.
