---
name: running-bug-review-board
description: >-
  Runs real-user QA, manual test plans, UX bug hunts, build sign-off,
  bug filing, and bug triage for web or iOS/iPadOS apps. Use when asked
  "QA this", "is this ready to ship?", or similar. Produces P0/P1/P2
  bug reports, YES/NO phase sign-off, tracker sync guidance, and an
  HTML QA dashboard; keeps Interactive BRB triage in a separate session.
---

# Running the Bug Review Board (BRB) QA pass

This skill runs a **real-user QA pass** on an app and feeds the output
into a Bug Review Board: a folder of structured bug reports, per-pass
run reports, a self-contained HTML dashboard, and a final YES/NO sign-off
the team can act on. Engineering's tracker (Linear / GitHub / Jira /
Notion) syncs bi-directionally so QA and engineering stay in step.

It generalizes a battle-tested workflow that already shipped phase QA on
Mokuhoe — the techniques are repo-agnostic.

## Why this exists

Most engineers test their own code. They confirm what they wrote works.
That misses the bugs **real users hit first** — stale state across
flows, mobile overflow, copy that lies, paths that 404 mid-onboarding,
race conditions between auth and routing.

This skill simulates a real user. The QA agent acts like a careful,
mildly unforgiving customer who does not read the source code.

## Two workflows — Auto QA and Interactive BRB

The skill splits the work into two distinct modes that share artifacts
but **run in separate sessions** on purpose:

- **Auto QA pass** — the agent drives the app, runs scenarios, files
  bugs, generates the HTML report, writes a verdict. Optimized for
  thoroughness and speed.
- **Interactive BRB** — a *different* agent meets with the user to
  triage open / in-progress / fixed bugs. Runs the bi-directional pull
  first, applies pattern-based heuristics to surface duplicates and
  clusters, walks each bug, flips statuses, syncs to the tracker,
  regenerates HTML, writes minutes. Optimized for shared judgment.

Keep them separate. Running BRB inside an auto pass lets triage bias
contaminate discovery and confuses attribution. See
[references/brb-interactive.md](references/brb-interactive.md).

## The trifecta — three hats, one pass

For every pass, wear all three hats:

- **Product Manager.** Confirm the build delivers the user-visible
  promise documented in the product spec or phase doc. If it does not,
  that is a product gap, not a bug — flag it in the run report.
- **QA.** Execute every scenario from a real user's perspective on the
  primary supported viewport(s). Capture evidence (snapshot, console,
  server data when relevant). Pass / Fail / Blocked.
- **Engineer.** Watch for invalidated assumptions: phase doc says "X
  uses function Y" but Y was renamed; new client orchestration appeared
  in a flow the docs say is server-driven; fields exist in UI that
  aren't in the spec. **Finding gaps is the point** — don't reverse-
  engineer the docs to match buggy behavior.

Do **not** fix product code unless the user explicitly asks. Test,
document, file bugs, hand off.

## Discover the app first (or you'll write bad tests)

Before writing a single test, understand the **intent** of the app —
what the customer is hired to do with it. See
[references/discovering-the-app.md](references/discovering-the-app.md)
for the full investigation playbook. The short version:

1. Read the product spec / README / landing page / pitch deck (in that
   priority order) for what the app **promises**.
2. Read the phase doc (or current sprint plan) for what was **just
   built**.
3. Read prior QA gates / checklists for what passed before — regressions
   are your highest-value finds.
4. Read the bug-reports index — open bugs are scenarios you must re-test
   first.
5. **Detect the project type(s).** A repo can ship more than one app —
   a **web + iOS monorepo** is common — so **collect every surface whose
   signals are present** instead of stopping at the first hit. Two
   disambiguation rules resolve *overlapping signals inside a single
   app*; they are **not** a reason to skip a genuinely separate surface:
   - **Electron / Tauri beats Web app for the same app.** An Electron /
     Tauri project (`electron`, `@electron/`, `@tauri-apps/` in
     `package.json`, or `electron-builder.yml` / `tauri.conf.json`) also
     contains `package.json` and web framework deps, but those deps
     belong to the desktop app — count it **once** as a desktop app, do
     **not** also count it as a separate **Web app**.
   - **macOS vs iOS on a shared `*.xcodeproj` / `*.xcworkspace`.** A bare
     Xcode project is shared between the two, so don't classify on it
     alone — require a platform-specific marker (below).

   The surfaces, with the playbook each activates:
   - **Electron / Tauri desktop app** → use
     [computer-use-playbook.md](references/computer-use-playbook.md). (On
     non-macOS hosts where Computer Use is unavailable, the playbook's
     graceful-degradation table directs you to drive the app's dev-server
     URL via [browser-playbook.md](references/browser-playbook.md)
     instead.)
   - **Web app** (web framework deps without Electron / Tauri markers) → use
     [browser-playbook.md](references/browser-playbook.md).
   - **iOS / iPadOS app** (an iOS-specific marker is present — `.iOS(...)`,
     `platform :ios`, `UIDeviceFamily`, or an `ios/` directory) → use
     [ios-simulator-playbook.md](references/ios-simulator-playbook.md).
   - **Native macOS app** (a macOS-specific marker is present — `.macOS(...)`,
     a `.app` bundle, or `LSMinimumSystemVersion` — and no iOS marker) → use
     [computer-use-playbook.md](references/computer-use-playbook.md).
   - **Mixed (monorepo)** — signals for two or more distinct surfaces
     above (e.g. web framework deps **and** an iOS marker) → run **every**
     matched playbook; the test plan gets per-platform scenario blocks.
     A web match must **never** short-circuit a co-located iOS (or macOS)
     pass.
   - **Other** (no UI signals) → no UI playbook activates.

   Also note whether **Codex Computer Use** is available (macOS only) —
   it enables a human-fidelity pass on web apps and is the only way to
   reach a native Mac or Electron/Tauri app. Most VMs (Cursor cloud, CI)
   won't have it, so never make the pass depend on it.
6. **Detect the issue tracker** (Linear, GitHub, Jira, Notion, or
   none). Surface every signal found and **ask the user to confirm**
   before writing `qa-config.json`. See
   [issue-trackers.md](references/issue-trackers.md).
7. List the public routes / surfaces / entry points and decide which a
   real new user would touch.

If the user says "QA this app" but no docs exist, **ask** — see
[references/discovering-the-app.md § Asking the user](references/discovering-the-app.md).

## Workflow (any phase, any repo)

```
1. Scope        → which surface / phase / build
2. Discover     → product intent + recent change + open bugs
                + project type + issue tracker (confirmed)
3. Plan         → manual test plan (scenarios, IDs, expected, gates)
4. Prepare      → env, build, test accounts, viewport / device matrix
5. Mode         → parallel coordinator OR sequential wrap-up
6. Execute      → real-user scenarios with evidence
7. File bugs    → P0/P1/P2 with reproduction steps
8. Merge        → results + verdict (YES/NO + open P0/P1)
9. Generate HTML → apply html-report-style-guide.md
10. Hand off    → next QA agent (if NO) or engineering (if blockers)
11. Schedule BRB → separate session for interactive triage
```

Detail in [references/workflow.md](references/workflow.md).

## Mode picker

| Situation | Mode | Reference |
|-----------|------|-----------|
| Fresh full pass on a phase, multi-agent OK | Parallel coordinator | [references/parallel-coordinator.md](references/parallel-coordinator.md) |
| Fresh full pass **and the `waves` / `waves-codex` skill is installed** | Parallel coordinator, run as a bounded wave (coverage gate, structured handoffs, tiered verification, cheap-model shards) | [references/parallel-coordinator.md § Run the pass as a wave](references/parallel-coordinator.md) |
| Prior parallel run stalled or partial | Sequential wrap-up | [references/sequential-wrapup.md](references/sequential-wrapup.md) |
| Solo agent, small surface | Sequential, ordered top-to-bottom | [references/sequential-wrapup.md](references/sequential-wrapup.md) |
| Re-testing 1–3 fixed bugs after engineering shipped | Sequential, scoped to bug Test IDs | [references/sequential-wrapup.md](references/sequential-wrapup.md) |
| **Need to triage the open bug backlog with the human** | **Interactive BRB (separate session)** | [references/brb-interactive.md](references/brb-interactive.md) |
| **Repo is a native macOS app, or you want a human-fidelity pass on the real signed-in app** | Auto pass + Computer Use playbook (macOS) | [references/computer-use-playbook.md](references/computer-use-playbook.md) |
| **Repo is an iOS / iPadOS app** | Auto pass + iOS playbook (use a companion skill for input) | [references/ios-simulator-playbook.md](references/ios-simulator-playbook.md) |
| No test plan exists yet | Generate plan first | [references/test-plan.md](references/test-plan.md) |
| Phase doc lists features not yet implemented in code | Stop. Tell user — QA needs a working build | — |

## Surfaces — which playbook activates

Detected during the discovery step. Match repo signals to the
playbook(s) for **every** surface present — usually one, but a monorepo
matches more than one (see **Mixed** below). Record the choice(s) in
`docs/qa/qa-config.json` so later passes don't re-litigate it.

| Surface | Signals | Playbook |
|---------|---------|----------|
| **Electron / Tauri desktop app** *(check first — beats Web app)* | `electron`, `@electron/`, or `@tauri-apps/` in `package.json`; `electron-builder.yml`; `tauri.conf.json` | [computer-use-playbook.md](references/computer-use-playbook.md) |
| **Web app** | `package.json` with web framework deps (no Electron / Tauri markers), `app/` / `pages/` / `src/routes/`, deploy config for Vercel / Netlify / Cloudflare | [browser-playbook.md](references/browser-playbook.md) (add [Computer Use](references/computer-use-playbook.md) for a human-fidelity pass on a Mac) |
| **iOS / iPadOS app** | `Package.swift` with `.iOS(...)`, `Podfile` with `platform :ios`, `Info.plist` with `UIDeviceFamily`, `ios/` directory (bare `*.xcodeproj` / `*.xcworkspace` are shared with macOS — require at least one of these iOS-specific markers) | [ios-simulator-playbook.md](references/ios-simulator-playbook.md) |
| **Native macOS app** | `Package.swift` with `.macOS(...)`, a `.app` bundle, `Info.plist` with `LSMinimumSystemVersion` | [computer-use-playbook.md](references/computer-use-playbook.md) |
| **Mixed (monorepo)** | Signals for two or more distinct surfaces above (e.g. web + iOS) — a web match must not short-circuit the iOS / macOS pass | Run **every** matched playbook — the test plan gets per-platform scenario blocks |
| **CLI / library / backend** | No UI signals | Neither UI playbook; QA focuses on integration tests + error paths |

For iOS app QA, our skill **orchestrates** (discovery, test plan, bug
filing, BRB) and **defers the simulator driving** to one of the
iOS community's purpose-built skills — AXe (Cameron Cooke),
XcodeBuildMCP (Cameron Cooke / Sentry), ios-simulator-skill (Conor
Luddy), ios-build-verify (Josh Adams), baguette (tddworks),
ios-idb-skill (Hao Wu), serve-sim-skill (malopezr7),
swiftui-autotest-skill (Yusuf Karan), xcode-build-skill (pzep1), and
App Store Connect CLI + skills (Rudrank Riyam) for the TestFlight
hand-off. See the playbook for the recommended-stack table.

## Issue tracker integration

The skill **discovers and confirms** — it never assumes. The
[discovery ceremony](references/issue-trackers.md) probes signals
(`LINEAR_API_KEY`, `gh auth status`, Atlassian URL, registered MCP
servers, etc.) and surfaces every finding to the user before writing
`docs/qa/qa-config.json`. Once confirmed, the agent files bugs
locally and syncs to the tracker (push at file time or BRB time per
config) and pulls engineering's status changes back (default ON for
BRB start). Bi-directional reconciliation rules are spelled out in the
reference so divergences surface as user-decision diffs, never silent
overwrites.

Tracker IDs live in the bug front-matter — `Tracker / Linear`,
`Tracker / GitHub`, `Tracker / Jira`, `Tracker / Notion`,
`Tracker / lastSyncedAt`. The HTML report renders them as tags on
every bug card.

Helpers:
[`scripts/bugs-needing-sync.sh`](scripts/bugs-needing-sync.sh) lists
bugs missing tracker IDs (push candidates).
[`scripts/bugs-needing-pull.sh`](scripts/bugs-needing-pull.sh) lists
bugs whose `Tracker / lastSyncedAt` is stale (pull candidates).

## HTML report (Zite + Dieter Rams)

At the end of every pass and every BRB session, regenerate
`docs/qa/report/index.html` plus per-bug and per-run detail pages by
applying [html-report-style-guide.md](references/html-report-style-guide.md).

The report reads like a magazine, not a Kanban board. Typography does
the work — priority is the word `P0` in small caps, status is the word
`Open`, verdict is a single display-type word (`YES` or `NO`). One ink
colour for body, one quiet terracotta accent for links and CTAs,
hairline rules for separation. No coloured chips, no pills, no
shadows. A 640px reading column on every screen size; on desktop, bug
detail pages add a quiet right rail for metadata. On mobile, a sticky
thumb-zone duplicates the primary action so the reader doesn't have
to scroll back up.

The information hierarchy is engineered for the engineer-reviewer's
sweep: **Title → Deck → Impact → Actual / Expected → Risk to fix →
Steps → Evidence**. The bug template grew `Impact` and `Risk to fix`
sections in v0.3 (additive — old bugs render gracefully without them).

**Markdown stays the source of truth.** HTML is read-only and
regenerated. Never edit the HTML to change bug state — edit the
markdown and regenerate. The dashboard is what stakeholders open
during BRB and ship reviews.

## Pattern-based triage suggestions

The Interactive BRB opens with a **Suggestions** card surfaced by a
catalog of named heuristics in
[triage-heuristics.md](references/triage-heuristics.md) — same suspect
file, steps-prefix overlap, same console error, same persona+surface+
outcome, phase cascade, cosmetic cluster, regression marker, same
owner. Every suggestion cites a heuristic name and the matching text
so the user always sees *why* something was flagged. No embeddings, no
LLM API, no auto-merge. The agent suggests; the user decides.

The same heuristics are also opt-in during the auto pass at file time
(`triage.runHeuristicsOnFile`, default `false`) so the pass can ask
"file new, or update BUG-007?" instead of double-filing.

## Scaffold folders if missing

If the target repo has no QA folder structure yet, run the bundled
scaffolder to create it:

```bash
bash <skill>/scripts/scaffold-qa.sh "$REPO_ROOT" PHASE_NUM [SLUG]
```

It creates (idempotent — won't overwrite existing files):

```
<repo>/docs/qa/
├── README.md                         # how QA works in this repo
├── qa-config.json                    # stub; discovery rewrites once user confirms
├── phase-NN-<slug>-manual-test-plan.md  # filled-in skeleton (if PHASE_NUM given)
├── report/                           # HTML report destination (agent generates)
├── bug-reports/
│   ├── README.md                     # index + status workflow
│   ├── _template.md                  # bug template
│   └── assets/                       # screenshots (incl. ios/ for iOS QA)
└── runs/                             # per-shard + coordinator merges + BRB minutes
```

If a different layout already exists in the repo (e.g. `tests/manual/`,
`qa/`, an issue tracker), **adopt that layout** — do not duplicate it.

## Always

- **Real user perspective.** Drive the app, not the source. Test from
  URLs and clicks (or simulator taps), not from `convex/users.ts` or
  the API layer alone.
- **Test mobile, tablet, and desktop.** Real users arrive on all three,
  and layout / overflow / tap-target bugs hide at the breakpoint you skip.
  Cover all three modes for web apps — reference sizes **mobile 375 × 812,
  tablet 768 × 1024, desktop 1280 × 800** (adjust to the spec's
  breakpoints). Lead with the app's **primary** target: take it from the
  product spec; if the spec is unclear, ask the user which mode matters
  most; if the user isn't available, infer the most likely primary from
  what you discovered in the repo (responsive CSS / breakpoints, framework
  defaults, marketing copy) and note the assumption. Record the modes and
  the chosen primary in `qa-config.json#platforms.web` so later passes
  don't re-litigate it. For iOS apps, the device matrix comes from
  `qa-config.json#platforms.ios.devices`.
- **One browser tab per agent.** Parallel agents on a shared tab cause
  auth-provider rate limits and stale sessions.
- **Capture evidence.** Snapshot or screenshot at the moment of failure,
  console errors verbatim, server data row when relevant.
- **File bugs immediately on FAIL** — see
  [references/bug-filing.md](references/bug-filing.md). Do not wait
  until end of pass.
- **Use the test account playbook.** See
  [references/test-accounts.md](references/test-accounts.md). If none
  documented, ask the user before guessing.
- **Session hygiene between scenarios.** See
  [references/session-hygiene.md](references/session-hygiene.md). Stale
  storage / cookies / `+test` email reuse silently poisons fresh-user
  flows.
- **Run the discovery ceremony** in
  [issue-trackers.md](references/issue-trackers.md) once per repo
  before filing bugs.
- **Regenerate the HTML report** at the end of every pass and every BRB
  session per [html-report-style-guide.md](references/html-report-style-guide.md).
- **For iOS app QA, defer the actual simulator driving** to a companion
  skill from [ios-simulator-playbook.md](references/ios-simulator-playbook.md);
  do not reinvent boot / tap / screenshot.

## Never

- Mark a scenario PASS from code inspection alone. The user does not
  experience source — they experience the app.
- Mark a phase gate ☑ without evidence (snapshot, server row, console
  clean).
- Fix product code unprompted. Document. File. Hand off.
- Skip the **Known issues / deferrals** section in the phase doc —
  those drive your scope and prevent false bugs.
- Rename phase docs or specs to match buggy behavior. Hides regressions.
- Run multiple QA browser sub-agents on one cursor-ide-browser tab.
- Reuse a previously-failed test email without changing the run-tag
  suffix.
- **Assume an issue tracker** without asking the user — even when
  signals are obvious.
- **Run Interactive BRB in the same session as an auto QA pass** —
  they are intentionally separate to keep triage bias out of discovery.
- **Auto-import tracker-only bugs** into local markdown without asking
  the user (default `pull.createLocalForUntracked: "ask"`).
- **Auto-merge bugs** the heuristics flag as duplicates — every
  merge / dedup needs user confirmation.
- **Edit the HTML to change bug state.** Edit the markdown; regenerate.
- **Use the iOS simulator playbook for web-app QA.** It's for iOS app
  projects only. Mobile web QA stays in the browser playbook.

## Bug priority (BRB taxonomy)

| Level | Definition | Action |
|-------|------------|--------|
| **P0** | Blocks core flow; data loss; auth bypass; security | Phase cannot ship; halt QA pass until triaged |
| **P1** | Feature broken or wrong; workaround exists | Blocks current phase sign-off |
| **P2** | Cosmetic, edge case, accessibility, dev console noise | Defer to polish phase or release hardening |

When in doubt between P0 and P1, choose **P0** if a user could land in
a non-recoverable state or lose data.

## Pass criteria (any phase)

- All scenarios in the phase manual test plan **PASS** (or are
  explicitly **deferred** with reason in the phase doc).
- Phase gate / checklist all green.
- No open **P0** or **P1** bugs against this phase.
- For phases that touch auth / invites / notifications: the regression
  matrix is green.

## Definition of done

Every pass ends with a coordinator merge doc whose top line reads:

> **Phase N ready? YES** — all gates ☑, no open P0/P1.
> **Phase N ready? NO** — list open P0/P1 + remaining unrun scenarios
> + a one-paragraph handoff prompt for the next QA agent.

If **NO**, the merge doc must be paste-ready into a new conversation.
The next agent should not need to rediscover state. See
[references/gate-merge.md](references/gate-merge.md).

The HTML report (`docs/qa/report/index.html`) is also regenerated and
committed.

## Browser tools (cursor-first, fallback ladder)

Default to **cursor-ide-browser** MCP when running inside Cursor. If
the session is in another tool or browser MCP is missing, fall back per
the ladder in [references/browser-playbook.md](references/browser-playbook.md):

1. cursor-ide-browser MCP (Cursor / Claude Code)
2. Chrome DevTools for agents (`chrome-devtools-mcp`) — auto-waits for
   results and adds DevTools-grade network / console / Lighthouse / a11y
   inspection; can attach to your real signed-in Chrome so auth flows
   don't get bot-flagged
3. browser-use MCP (provider-agnostic)
4. Playwright (CLI or MCP)
5. Codex Computer Use (macOS) — human-fidelity pass on the real signed-in
   app; see [computer-use-playbook.md](references/computer-use-playbook.md)
6. Driving manually + asking user to paste console errors / screenshots

Whatever tool, the **playbook** is the same: navigate → snapshot → act
on fresh refs → capture evidence → unlock when done. The reference
covers each tool's specifics, including how to drive like a human so the
app doesn't trip on bot detection or timing races. The pass must succeed
with whatever the environment has — don't depend on Computer Use, which
most VMs lack.

## Deliverables per pass

| Path | What |
|------|------|
| `docs/qa/qa-config.json` | Tracker + triage + report + platforms config (discovery rewrites the stub) |
| `docs/qa/phase-NN-<slug>-manual-test-plan.md` | (if newly generated) |
| `docs/qa/runs/QA-<shard>-run-YYYY-MM-DD.md` | Per-shard results |
| `docs/qa/runs/COORDINATOR-MERGE-YYYY-MM-DD.md` | Merge + verdict |
| `docs/qa/runs/BRB-YYYY-MM-DD.md` | (Interactive BRB only) session minutes |
| `docs/qa/bug-reports/BUG-NNN-*.md` + `assets/BUG-NNN/` | Each defect |
| `docs/qa/report/index.html` + `bugs/` + `runs/` + `assets.css` | Apple-language HTML dashboard |
| `docs/QA_GATES.md` (or your repo's equivalent) | Gate boxes updated |
| Phase doc § QA status | Sign-off note + link to merge |
| Tracker issues (Linear / GitHub / …) | If `syncOnFile` or after BRB |

Adapt paths to whatever the target repo already uses.

## References (load on demand)

- [references/workflow.md](references/workflow.md) — full PM/QA/Eng decision tree
- [references/discovering-the-app.md](references/discovering-the-app.md) — investigate intent + ask user when docs missing
- [references/test-plan.md](references/test-plan.md) — derive a phase manual test plan from spec + phase doc + gate
- [references/test-accounts.md](references/test-accounts.md) — Clerk / Auth0 / Supabase / custom — and the "ask the user" pattern
- [references/session-hygiene.md](references/session-hygiene.md) — stale storage, rate limits, persona suffixing
- [references/browser-playbook.md](references/browser-playbook.md) — cursor-ide-browser, Chrome DevTools MCP, browser-use, Playwright recipes + how to drive like a human (web apps)
- [references/computer-use-playbook.md](references/computer-use-playbook.md) — Codex Computer Use for web and native macOS apps (macOS; graceful fallback to a browser driver elsewhere)
- [references/ios-simulator-playbook.md](references/ios-simulator-playbook.md) — iOS / iPadOS app QA, curated companion-skill ladder (AXe, baguette, XcodeBuildMCP, ios-simulator-skill, ios-build-verify, …)
- [references/parallel-coordinator.md](references/parallel-coordinator.md) — shard map, write-path-first rule, copy-paste shard prompts, and running the pass as a bounded wave when `waves` / `waves-codex` is installed
- [references/sequential-wrapup.md](references/sequential-wrapup.md) — single-agent finish; copy-paste prompt
- [references/bug-filing.md](references/bug-filing.md) — bug template, severity, evidence rules, status transitions
- [references/gate-merge.md](references/gate-merge.md) — merge shard reports → gates + verdict
- [references/issue-trackers.md](references/issue-trackers.md) — discover-and-confirm ceremony, Linear / GitHub / Jira / Notion adapters, bi-directional sync
- [references/brb-interactive.md](references/brb-interactive.md) — Interactive Bug Review Board workflow (separate session)
- [references/triage-heuristics.md](references/triage-heuristics.md) — named heuristics catalog for duplicate / cluster detection
- [references/html-report-style-guide.md](references/html-report-style-guide.md) — Apple-language tokens, components, rendering rules
- [references/extending-the-skill.md](references/extending-the-skill.md) — add a tracker, heuristic, surface, or mode without rewriting
- [references/templates/](references/templates/) — bug-report, test-plan, run-report, coordinator-merge, brb-interactive-prompt, brb-minutes, qa-config.example.json, html-report/ skeletons

## Scripts

- `scripts/scaffold-qa.sh REPO_ROOT PHASE_NUM [SLUG]` — creates the QA
  folder layout, qa-config stub, and report folder in any repo.
- `scripts/bugs-needing-sync.sh REPO_ROOT [--tracker …]` — lists bugs
  missing a tracker ID; the agent reads the list and pushes per
  `issue-trackers.md`.
- `scripts/bugs-needing-pull.sh REPO_ROOT [--threshold 24h] [--tracker …]`
  — lists bugs whose `Tracker / lastSyncedAt` is stale; the agent reads
  the list and pulls per `issue-trackers.md`.

## Extending this skill

Adding a new issue tracker, triage heuristic, surface playbook, or mode
is additive — copy a section, fill it in, the agent picks it up on the
next session. Forward-compatible `qa-config.json` schema (`version: 1`,
unknown fields ignored), additive bug front-matter, versioned HTML
report marker. See
[references/extending-the-skill.md](references/extending-the-skill.md).

## Anti-patterns to avoid

| Don't | Why |
|-------|-----|
| Mark scenarios PASS from code inspection | Users don't experience source |
| Defer P0 bugs to "next phase" | Foundation bugs cascade everywhere |
| Trust prior PASS marks without re-running on a fresh build | Regressions appear from unrelated work |
| Run multiple QA agents on one browser tab | Auth providers throttle; sessions bleed |
| Edit the phase doc to match buggy behavior | Hides the regression — file a bug instead |
| File a bug without **Steps to reproduce** | Engineering can't act on it |
| Test only the happy path | The happy path is what engineers tested already |
| **Run BRB and an auto pass in the same session** | Triage bias contaminates discovery |
| **Sync bugs to a tracker without filling `qa-config.json`** | Duplicates and lost edits |
| **Use the iOS playbook to test a web app on Mobile Safari** | Out of scope; the iOS playbook is for iOS app projects only |
| **Auto-merge heuristic suggestions** | Every dedup needs user confirm |
| **Auto-import tracker-only bugs** as local markdown | Engineering may have filed them in a context QA shouldn't claim |
| **Edit the HTML to change bug state** | Markdown is the source of truth; regenerate the HTML |

## When a QA pass reveals work bigger than QA

If during the pass you find:

- A **missing feature** the phase claims exists (no code path at all)
- A schema diverging from the spec across multiple scenarios
- A P0 blocking every remaining scenario

Stop testing. Surface the finding. The user decides whether to escalate
to engineering or carve a smaller phase. Continuing wastes time on a
foundation that needs replacing.
