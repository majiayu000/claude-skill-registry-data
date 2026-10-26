---
name: verify-ui
description: Prove UI work actually works by driving the app on the simulator with Argent (build/launch, tap, screenshot, read logs), walking the Critical User Journeys, and visually inspecting each state against the spec's acceptance criteria. Use after any UI change — "verify", "check the UI", "does it work", "screenshots", "QA" — and always as the verification phase of feature work. Subsumes the old /qa-cuj command. Never declare UI work done without this. Needs Argent + macOS.
argument-hint: [spec number/slug, or a single CUJ id, or blank for all CUJs]
allowed-tools: Read Glob Grep Bash(npm run e2e*) Bash(npx expo *)
---

## Task

Verify the running app for **$ARGUMENTS** with evidence, not vibes. You are also wearing the QA-engineer persona (`docs/personas/qa-engineer.md`).

1. **Identify scope.** From the spec (or, if no spec, the current diff via `git diff --stat main`), list the CUJs touched (`docs/quality/critical-user-journeys.md`). New user-visible behavior with no CUJ/Maestro coverage → write the `.maestro/flows/<slug>.yaml` flow first (see `docs/conventions/testing.md`); that gap is itself a finding.
2. **Boot the app.** Ensure a simulator dev-client build exists; if not, build it (`npx expo run:ios` — ask before a long local build). Then use the **Argent** MCP tools to fresh-launch the app.
3. **Walk every journey.** Tap/swipe/type through each CUJ in scope **and its listed edge cases**. Probe beyond the script: rotation, backgrounding mid-action, relaunch for persistence, rapid repeated taps, extreme inputs, offline. Screenshot each journey's end state and any anomaly. If a screen feels slow, run a profiling session and summarize the trace.
4. **Look at every screenshot** (use the Read tool — actually look). Judge against: the spec's acceptance criteria, `docs/conventions/design-system.md` (states, typography, tokens), and accessibility (labels, roles, touch targets, reduced motion). Check the unglamorous states hardest: empty, loading, error, offline.
5. **Attest honestly,** following the report format in `docs/runbooks/agentic-qa.md`:

```
## UI verification — <slug> (<date> @ <sha>)
Verdict: VERIFIED | ISSUES FOUND (n)
| AC | Evidence (screenshot / flow step) | Verdict |
|----|-----------------------------------|---------|
| AC-1 | tasks-add.png / tasks.yaml step 2 | PASS |
…
Issues: [P1|P2|P3] <screen> — observed vs expected — repro — screenshot ref
Performance: <screen> — TTI / jank notes
```

6. **Close the loop.** Issues found → fix them (or hand back to `/implement-feature`) and re-run until VERIFIED. The screenshots you finish with are the evidence `/feature-report` will publish — keep them. Any finding worth preventing permanently → end with a `HARNESS:` proposal (run `/encode-lesson`).

An agent attesting "verified" with failing or unexamined screens is the single worst trust violation in this harness. When in doubt, mark ISSUES FOUND — a FAIL with good repro steps is a great outcome.
