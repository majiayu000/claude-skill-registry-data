---
name: quality-review
description: |
  After a PRD, spec, or plan, before implementation: hunt perceived-quality
  pitfalls (silent failures, missing loading/empty states, error recovery, state
  drift) that make a product feel cheap. Complements pitfall-verification.
---

# Quality review

Use this skill after finishing a PRD, spec, or implementation plan — before implementation starts. It is NOT a bug hunt. It is a targeted check that *the artifact, if shipped as written, will feel like a premium product* — on the level of CleanMyMac, Raycast, Linear, Things, Stripe Dashboard — and not like a hobby project.

Invoke with: `/superpowers-gstack:quality-review`

## When to invoke

Automatically after completing:

- A PRD, spec, or design document
- An implementation plan
- Output from `writing-specs`, `writing-plans`, `plan-design-review`, `plan-eng-review`, or any planning skill that produces an artifact ready to hand off to implementation

Run **once** before implementation. Re-run after substantial spec/plan revisions.

## Relationship to pitfall-verification

`quality-review` is *complementary, not overlapping*, with `pitfall-verification`:

| Skill | Lens | Question |
|-------|------|----------|
| `pitfall-verification` | Correctness | "Will this work?" (bugs, security, contracts, edge cases) |
| `quality-review` | Perceived quality | "Will this feel good?" (silent failures, loading, empty/error states, polish) |

Recommended flow on a fresh artifact:

1. `pitfall-verification` → fix bugs
2. `quality-review` → fix feel
3. Hand off to `writing-plans` / implementation

Both should be run. They catch different classes of issue.

## Sequence

1. **Read the artifact in full.** PRD/spec/plan — every section.
2. **Read the relevant existing code.** Do not review spec-internal only; cross-check claims against the codebase. A spec that says "extend the existing PlanStore" needs to be verified against what `PlanStore` actually does today.
3. **Identify peer apps in the domain.** For macOS productivity apps: CleanMyMac, Raycast, Linear, Things, Setapp. For web: Linear, Notion, Stripe Dashboard, Vercel. The governing question is: *"would this feature, as specified, feel at home next to <peer>?"*
4. **Walk the 15 categories below.** For each: question → risk surface → verify against code → verdict.
5. **Research when uncertain.** If you don't know current best practice for a category (e.g. "what's the right way to do AI structured output in 2026?"), use WebSearch / WebFetch and cite concrete sources (Anthropic docs, Apple HIG, etc). Do not guess.
6. **Produce the verdict in the output format below.**

## The 15 categories

These are **starting points, not exhaustive**. Add domain-specific quality risks as they surface.

For each category: state the question, locate the risk surface in the artifact, verify by reading the code, and report `N/A | HANDLED | NOT HANDLED — proposed fix`.

### 1. Silent failures

Where in the flow can something fail *without the user being told*? AI calls returning nothing, parse errors that get "abandoned silently", retry loops with no UI signal, swallowed exceptions. Silent failure = user thinks the app is broken.

Risk surfaces: any `try/catch` with empty `catch`, any optional unwrap that defaults to "", any AI call without an error path.

### 2. Loading states / progress

Is there any operation that takes >500ms without a spinner, skeleton, progress text, or cancel button? Specifically check: AI calls, file I/O, shell commands, scan/index operations, network requests.

Risk surfaces: spec sections that describe an operation without a "during" UI state.

### 3. Empty states

What does the user see the first time a list/view is empty? A spec that does not define empty state = generic "no items" = bad first impression. Premium apps treat empty state as a *teaching moment* (Linear's empty inbox, Things' empty Today).

Risk surfaces: any new list/grid/table view in the spec.

### 4. Error recovery

When something fails, how does the user get back on rails? Inline banner with retry? Toast? Blank screen? Each error path should have an explicit recovery action — not just "show error".

Risk surfaces: every failure mode listed in the spec; every code path that throws.

### 5. State drift / source-of-truth conflict

If the app's stored state and reality (filesystem, system settings, external API) can diverge, how is reconciliation handled? Classic example: user changes something outside the app, app still shows the old state.

Risk surfaces: any feature that mirrors external state (file watchers, system prefs, external APIs, login items, calendar events).

### 6. Data-loss risk

Can an undo/revert/overwrite operation, run without a warning, destroy the user's manual edits? Pay special attention to snapshot-based revert flows and auto-fix that overwrites files.

Risk surfaces: any "revert", "restore", "auto-fix", "regenerate" action; any operation that writes to a path the user could have edited.

### 7. Discoverability

Are there features that are technically implemented but nobody will find? Hidden tab, audit log without UI, keyboard shortcut without a menu item, settings panel buried three levels deep.

Risk surfaces: every feature in the spec — ask "how would a new user encounter this?"

### 8. Multi-tenancy / scope isolation

If the app has workspaces, profiles, accounts, projects: is the new state correctly scoped, or is it global and leaking between tenants? This is one of the highest-impact pitfalls — global state in a workspaced app breaks the mental model on day one.

Risk surfaces: any `*.shared` singleton, any `~/Library/Application Support/<app>/*.json` path that isn't workspace-scoped, any `UserDefaults.standard` write.

### 9. Persistent operations mid-session

Is time-dependent state (snooze, cache expiry, scheduled actions, "remind me in 1h") re-evaluated during an active session, or only at app launch? "Only on launch" = app feels lazy. Premium apps re-check on a timer or via system notifications.

Risk surfaces: any feature involving time, expiry, or scheduling.

### 10. Keyboard / native conventions

For macOS: ⌘W (close window), ⌘1-9 (tab switching), ⌘↩ (primary action), Space (preview), Esc (dismiss) — are platform conventions respected? For web: tab order, focus ring, Esc-to-dismiss, Enter-to-confirm? For iOS: swipe-to-go-back, edge gestures?

Risk surfaces: any new modal, sheet, list, or view introduced by the spec.

### 11. Animations / transitions

Does the spec rely on default framework animations (SwiftUI default, CSS default — both feel generic), or specify named easing (`.spring`, `.snappy`, `cubic-bezier(...)`) with rationale? Premium apps have signature motion. Generic ease-in-out reads as "AI-generated".

Risk surfaces: any sheet present/dismiss, any list reorder, any state change that is visible.

### 12. AI-specific pitfalls

If the artifact involves LLM calls, load the `claude-api` skill for current API facts before judging, then check:

- Structured output via the native structured-output / tool-use API, not a prompt-engineered "respond with JSON"?
- Fence-stripping and schema validation explicit, with a fallback when the model returns malformed output?
- A cap on output size, and prompt caching where the prompt has a stable prefix?

Risk surfaces: any AI call in the spec.

### 13. Privileged operations / sudo flows

If the app requires sudo, admin auth, system permissions (Full Disk Access, Accessibility, etc): is the flow framed as *deliberate design* — explanation sheet + consent + clear "why we need this" — or just a toast that pops up and disappears? "Just a toast" = feels cheap.

Risk surfaces: any TCC permission, any `osascript` with admin privileges, any Authorization Services call.

### 14. Localization-readiness

Does the spec use `LocalizedStringKey` (SwiftUI) / `t()` / equivalent for user-facing strings, or are strings hardcoded? Even if the app ships English-only today, hardcoded strings = future tech debt and immediate inconsistency with the rest of the codebase if it already localizes.

Risk surfaces: every user-facing string in the spec — dialog titles, button labels, error messages, empty-state copy.

### 15. Sort order in lists

If the spec introduces a new list view, is sort order explicitly defined? Unspecified = whatever the underlying collection happens to yield = unpredictable UX. Premium apps always specify (most recent first, alphabetical, manual drag, etc).

Risk surfaces: every new list/table introduced by the spec.

## Domain-specific extensions

The 15 above are the generic perceived-quality surface. Add domain-specific quality risks before running:

- **macOS apps**: dock icon behavior, menu bar icon, About panel, Sparkle/auto-update flow, DMG vs PKG, code signing & notarization framing
- **Web apps**: SSR vs CSR loading flicker, dark mode, mobile responsive, browser back-button preservation
- **CLI tools**: `--help` quality, color in pipes, exit codes, progress on stderr, `man` page presence
- **Developer tools**: TTHW (time-to-hello-world), error message quality, doc discoverability

Use the existing peer apps in the user's domain as the comparison baseline.

## How to run the check

For each category:

1. **State the question** — one sentence.
2. **Locate the risk surface** — which spec section, which code file, which user flow?
3. **Verify against code**, do not assume. If the spec says "extend `PlanStore`", read `PlanStore.swift` to confirm the extension is sane.
4. **Compare to peer apps** — when in doubt: "how does Linear handle empty inbox?", "how does Raycast handle command not found?". Cite the comparison.
5. **Report**: `N/A` (with reason) / `HANDLED` (point to where) / `NOT HANDLED — proposed fix` (concrete, file/section-anchored).

Concrete findings only. Never vague advice like "consider improving error handling". Every NOT HANDLED finding must include a proposed fix that names a file, a function, or a spec section.

## Output format

```
Quality review —

CRITICAL (will make the app feel broken on first use):
- Q<N>. <one-line finding> — <risk surface> → <concrete fix with file/section reference>
- ...

SIGNIFICANT (erodes quality over time):
- Q<N>. <finding> → <fix>
- ...

POLISH (premium-feel gap, but not blocking):
- Q<N>. <finding> → <fix>
- ...

Peer comparison: <which premium peer was used as the bar, and how this artifact stacks up>

Verdict: SHIP-READY | NEEDS PATCH (critical issues found) | NEEDS POLISH (significant issues found)
```

If `SHIP-READY`: hand off to implementation.
If `NEEDS PATCH`: fix critical findings, re-run quality-review.
If `NEEDS POLISH`: surface to user with explicit choice — fix now, or defer with a tracked debt note.

## Severity rubric

- **CRITICAL** — first-use experience will feel broken. Silent failures, missing empty states on the primary flow, scope leakage (workspace mixing), data loss without warning.
- **SIGNIFICANT** — works, but premium feel erodes within first week. No loading states on slow ops, generic error toasts, unspecified sort order, hardcoded strings in a localized codebase.
- **POLISH** — the gap between "good" and "Linear/Raycast-tier". Default animations, missing keyboard shortcuts, sudo flow framed as toast, etc.

Be honest about severity. A POLISH finding should not be elevated to CRITICAL just to force action.

## Example finding (tone & precision)

```
Q8. Per-workspace isolation missing. PlanStore.shared is a global singleton
persisting to a single plan-cards.json. The app has workspaces, and all other
state objects (HealthEngine, AIChatViewModel) are workspace-scoped. Plan Cards
generated in workspace "Home" will appear in workspace "client-project". This
breaks the mental model on first multi-workspace use.

Risk surface: spec §4.2 ("Persistence"); code at PlanStore.swift:14.
Fix: persist to ~/Library/Application Support/<app>/workspaces/<workspace-id>/plan-cards.json.
Make PlanStore workspace-injected, not a singleton. Update spec §4.2 to specify
the path template and migration plan for existing global state.
```

That is the bar. File path, line number, peer-app comparison where relevant, concrete fix.

## What this skill is NOT

- Not a bug hunt — that's `pitfall-verification`.
- Not a security audit — that's `cso`.
- Not a visual/design review of an existing UI — that's `design-review` (live) or `plan-design-review` (plan).
- Not a developer-experience review — that's `plan-devex-review`.
- Not a code style review.

It is the *perceived-quality gate* between "spec written" and "implementation begins". Catch the cheap-feeling decisions before they ship.
