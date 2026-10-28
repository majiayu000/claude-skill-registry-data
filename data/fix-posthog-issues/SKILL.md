---
name: fix-posthog-issues
description: Triage active PostHog error-tracking issues by root cause, fix the legit ones, and resolve or suppress the rest with evidence.
disable-model-invocation: true
argument-hint: "Optional issue ids; defaults to all active issues"
compatibility: "Requires the PostHog MCP server"
---

# Fix PostHog Issues

Active PostHog error-tracking issues are mostly browser exceptions from the JS SDK,
plus server-side `$exception` captures. In a Livewire / Alpine SPA most of them are
**transient** navigation races, vendor throws, or browser noise, not bugs. Read the
stack, the occurrence spread, and the session timeline, not the headline. Walk from
the newest last-seen to the oldest.

**Project context.** Read `.agents/posthog.md` when the repo has one. It holds the
project id, the `before_send` filter file, the app's registration patterns, and the
precedent fixes. Then follow the repo's `AGENTS.md` / `CLAUDE.md` rules for tests,
asset builds, cache clears, and a dirty tree.

## 1. Load the working set

Read [`references/posthog-mcp.md`](references/posthog-mcp.md) before your first
PostHog call. It covers the single `exec` tool, the error-tracking tools, the status
lag, and `resolved` vs `suppressed`. Stay on the project named in the project context:
never switch projects. List `active` issues ordered by last seen.

## 2. Cluster by root cause

PostHog groups issues by exception type and top frame, **not by cause**. For example,
one `x-data` scope owner that morph-inserts late throws `X is not defined` for every
property its descendants read, and each property becomes its own issue. Group the
issues by shared cause before you fix anything. Fix each cause once, then dispose of
every issue in its cluster.

Completion criterion: every active issue in scope belongs to a cluster.

## 3. Classify each cluster

Pull event samples: stack frames, URL, `session_id`, and person. Open the app frame on
current `main`. Compare last-seen with deploys (`git log --oneline -- <file>`). Then
write one line per issue:

```
Issue <short-id>: [STALE | TRANSIENT | VENDOR | NOISE | LEGIT] — <one-line evidence>
```

- `Issue a1b2: TRANSIENT — Alpine "segment is not defined" on /leads/pipeline inside a nav window; 3 occ`
- `Issue c3d4: LEGIT — redirect sets skipRender, modal DOM outlives mountedActions=[]; 91 occ, 1 user`
- `Issue e5f6: VENDOR — thrown inside a Filament plugin's entangle; suppress`

Categories:

- **TRANSIENT**: a `wire:navigate` morph race or a bundle-hash change mid-deploy. The
  signatures are Alpine `X is not defined` / `Can't find variable`, Livewire
  `Illegal invocation`, `Could not find Livewire component`, `Snapshot missing`, and
  `Alpine.navigate|morph is not a function`. Resolve these (they auto-reopen on
  regression). Do not hunt them.
- **VENDOR**: the throw bottoms out in Livewire, Alpine, Filament core, or a
  third-party plugin. Suppress it. Leave vendor JS unpatched.
- **NOISE**: opaque cross-origin `Script error.`, ResizeObserver loops, link-scanner
  captures, non-Error captures, and `Failed to fetch` on navigate-away. Suppress these,
  or drop them in `before_send`.
- **STALE**: the issue stopped at a deploy of a known fix. Cite the sha and resolve.
- **LEGIT**: a steady-state error that fires **outside a navigation window**, has a real
  app frame, and recurs on one path.

**LEGIT vs TRANSIENT.** The best test is whether the error fires within a few seconds
of a `livewire:navigate` event. Secondary tests: a handful of occurrences spread across
many users and paths is transient, while dozens on one path from one user doing one
interaction is legit. A transient race is usually bracketed by `$pageleave` and
`$pageview` events for the same URL.

**When the top frame is a lie.** A top frame of `[Alpine] JSON.stringify` inside
`livewire.min.js` is Alpine's expression-error rethrow, not the thrower. Pull the
session's event timeline around the exception with `execute-sql`, and read what
surrounds it.

Completion criterion: every issue has a line.

## 4. Fix each LEGIT cluster at the right layer

- App Alpine component or page script: use the project's registration pattern.
- Livewire or Filament component behaviour: fix the PHP, with a Pest regression test.
- A class of noise you control: add a `before_send` matcher. Gate it to the navigation
  window unless the value is always benign, so a steady-state break still reports.
- Vendor or browser noise: add a suppression rule, never a vendor patch.

Make the minimal change and verify it. JS changes need the asset build. Commit one
logical fix per commit, and list every PostHog issue id the commit covers in its body
(`PostHog: <id>, <id>`). **Use plain refs only, never `fixes #NNN`.**

## 5. Set status

Set `resolved` on fixed, stale, and transient issues, and `suppressed` on vendor and
noise issues. Confirm each change with the single-issue read. A shipped JS fix leaves a
tail of occurrences from browsers that still run the old bundle, so note "pending
deploy verification". If an issue is LEGIT but blocked on an operator or a deploy, leave
it `active` and name what unblocks it. Resolve only issues whose cause is fixed or
transient.

Completion criterion: every issue in scope has its new status confirmed, or stays
active with a named blocker. Report `N active → M`, with one line per cluster, starting ✅ resolved or ⚠️ active with a blocker.

## 6. Offer a deploy re-check

If any issue is pending deploy verification, ask once whether to re-check it in 24–48
hours. On yes, schedule a one-time run where the harness can (in Claude Code, the
`schedule` skill's cloud routine; failing that, `CronCreate` with `recurring: false`,
which fires only while this session stays open, so say so). The prompt is plain text,
since a slash command for this skill cannot run from a schedule: "With the PostHog MCP,
read last-seen for issues <ids>; set back to active, with a note, any seen after
<deploy date> beyond the old-bundle tail." Otherwise, or on no, end the report with the
issue ids and the re-check date.
