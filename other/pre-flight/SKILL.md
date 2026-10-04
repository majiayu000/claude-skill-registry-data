---
name: pre-flight
description: Use this skill whenever the user wants to verify a side project is ready for its first real user — after `/autopilot` or `/factory` has reported "shipped" but before sending any DM. Also trigger when the user says "/pre-flight", "is my side project ready", "check before I DM users", "first-user readiness check", "the eval my agents skipped", "did my agent actually ship a product", or "ship/fix/rebuild verdict". Takes the live URL + idea.md + scope.md + one named first-user target as input. Runs four eval questions (Output / Trace / Component / Drift) against the live URL, writes pre-flight.md with pass/fail per question, surfaces the top 3 blockers ordered by impact × effort, and outputs a SHIP / FIX / REBUILD verdict. Companion to /autopilot and /factory — the eval rung the Lead the Machine series never wrote.
---

# Pre-flight — Is Your Side Project Ready For Its First Real User?

The 4-question eval between "agent says done" and "user says it works." One pass takes 2-5 minutes. Catches the 30-second SMTP misconfig, the stubbed Stripe integration, and the slow idea-drift that turns "podcaster show notes" into "AI productivity for solopreneurs" by Saturday 5.

Ship With AI artifact #26 · post-LtM methodology · companion to [4 questions that tell you if your side project is ready for a real user](https://shipwithai.substack.com/).

## When to run

Invoke when the user:

- Types `/pre-flight` or `/pre-flight <live-url>`
- Asks "is my side project ready?", "should I DM users yet?", "is the live URL actually working end-to-end?"
- Has just completed a `/autopilot` or `/factory` run and wants the readiness check before launch
- Wants a SHIP / FIX / REBUILD verdict before launch-day

Do NOT invoke when the user wants to:

- Ship code that hasn't reached DEPLOY yet (use [/autopilot](../autopilot) — pre-flight assumes a live URL exists)
- Collect post-launch user feedback (use [collect-feedback](../collect-feedback) — that's the next step *after* pre-flight passes)
- Plan launch posts and outreach (use [launch-day](../launch-day) — pre-flight runs *before* launch-day)
- Audit a multi-project portfolio's mortality (use [/factory](../factory)'s Phase 5 reflection instead)

## Input surface

- `/pre-flight` → operate on `cwd` — auto-discover live URL from `package.json` / `.vercel/project.json` / `wrangler.toml` / `.env`
- `/pre-flight <live-url>` → operate on `cwd` with the URL pre-filled

If `cwd` is not a git repo or has no `idea.md` / `scope.md` from a prior `/autopilot` run, warn and ask whether the user has shipped a project here yet.

## Process

### Phase 1 — Discovery (silent, ~15 seconds)

Read, in order, and form an internal picture:

1. `git status` and `git log --oneline --all | head -10` — confirm git repo + find the first commit (where `idea.md` was born — needed for Question 4)
2. Read `idea.md` if it exists (current version)
3. Read `scope.md` if it exists (the feature list)
4. Use `git show $(git rev-list --max-parents=0 HEAD):idea.md` to get the ORIGINAL `idea.md` from the first commit — needed for drift comparison
5. Read `CLAUDE.md` for existing `## Lessons` section — preserve and append
6. Check whether `curl`, `jq`, `npx playwright` are available
7. Check for any `pre-flight.md` from prior runs — note this is a fresh run vs a re-run

Do not print anything user-facing during this phase.

### Phase 2 — Interview (exactly four questions)

Ask these four questions, in this order, and wait for the user to answer each before proceeding. Do **not** ask follow-up questions. Four questions is the budget.

**Q1.** What's your live URL? (The deployed one. Include the protocol.)

> Example: "https://bedtime-story-co.vercel.app"

**Q2.** Where is your `idea.md`? (Path relative to cwd. If unsure, the skill will use the one in cwd from `/autopilot`.)

> Example: "./idea.md"

**Q3.** Where is your `scope.md`? (Path relative to cwd. Used to map promises to actual features.)

> Example: "./scope.md"

**Q4.** Who is the **one named first user** you're planning to DM after this passes? (Their handle, last 7 days of activity, or short bio — used by Question 3 to interpret what "value" means for THEM, not in the abstract.)

> Example: "Sarah Chen, POD seller on r/sideproject, posted yesterday about losing track of print queues across Etsy and Shopify."

All other calibration comes from Phase 1 discovery. Do not ask follow-ups.

### Phase 3 — Probe (silent, ~2-5 minutes)

Run the four eval questions sequentially. **Each is its own check; do not short-circuit on a fail — the user needs the full report.**

#### Question 1 — Output: does the URL actually work?

1. Run `bash ${SKILL_DIR}/scripts/probe-output.sh <URL>` to test:
   - URL returns 2xx with HTML
   - Each visible CTA on the landing page routes to a 2xx endpoint
   - If a signup form is found, POST a synthetic email (`pre-flight+$TS@example.com`) and confirm the response includes a user-id or session token (not just a 200)
2. Capture findings as `pre-flight-trace/q1-output.json`

**Pass** = URL + CTAs + signup all return 2xx and persist data
**Fail** = any 4xx/5xx, any CTA without backing route, any signup that returns 2xx but doesn't persist

#### Question 2 — Trace: can one user complete the core flow?

1. Run `bash ${SKILL_DIR}/scripts/probe-trace.sh <URL>` (uses headless Playwright if available, falls back to curl chain)
2. The trace walks: sign up → confirm email (check inbox API or SMTP catch — if unavailable, flag as manual) → log in → reach first-value moment → trigger second-value moment
3. Capture screenshots at each step into `pre-flight-trace/screens/`
4. Capture findings as `pre-flight-trace/q2-trace.json`

**Pass** = the trace completes end-to-end without dev-knowledge gaps
**Fail** = any step requires the user to know something a stranger wouldn't, OR any step 404s, OR the verification email never arrives within 60 seconds

#### Question 3 — Component: does each promise resolve to working code?

1. Fetch the landing page HTML. Extract each visible "feature" claim (headlines, bullets, CTAs).
2. For each promise, search the codebase for the route or component that delivers it.
3. Flag any promise that:
   - Has no matching route or component
   - Has a matching component containing `TODO`, `FIXME`, `stub`, or `mock`
   - References an external service (Stripe, Resend, OpenAI, etc.) without an env var present in production
4. Capture findings as `pre-flight-trace/q3-component.json`

**Pass** = every promise on the landing page resolves to working, non-stubbed code
**Fail** = any promise has no resolving code or has a stub

#### Question 4 — Drift: are you still shipping the original idea?

1. Compare the ORIGINAL `idea.md` (from the first commit) to the live product's landing page + reality.
2. Score drift on three dimensions:
   - **User drift** — has the target user changed? (e.g., "podcasters" → "content creators" → "solopreneurs")
   - **Job drift** — has the job-to-be-done changed? (e.g., "extract show notes" → "manage workflows")
   - **Outcome drift** — has the success outcome changed? (e.g., "save 30 min per episode" → "increase productivity")
3. Capture findings as `pre-flight-trace/q4-drift.json`

**Pass** = drift score ≤ 1 dimension changed AND change was deliberate (mentioned in `CLAUDE.md ## Lessons` or `git log`)
**Fail** = ≥ 2 dimensions changed OR change is silent (no Lessons entry explaining why)

### Phase 4 — Synthesize (silent, ~30 seconds)

1. Read all four `pre-flight-trace/q*.json` files.
2. Score each question pass/fail.
3. Compute the verdict:
   - **SHIP** — all 4 questions pass. Rare on a first run.
   - **FIX** — 1 or 2 questions fail with concrete fixes available. Most common verdict. Lists the 3 highest-leverage blockers.
   - **REBUILD** — 3+ questions fail, OR Question 4 fails with silent drift. The live product isn't the idea you wrote in session 1. The DM you're about to send won't match what the reader signs up to use.
4. Generate the top-3 blocker list, scored by `impact × (1 / effort)`:
   - impact = "first-user bounce probability" (high if Q1 or Q2 fails on a default user path)
   - effort = "minutes to fix" (curl-checkable env var = 5 min, missing component = 60+ min)
5. Write `pre-flight.md` to the project root using `${SKILL_DIR}/assets/pre-flight-template.md`.

### Phase 5 — Reflection (silent, ~15 seconds)

1. Read the synthesized report.
2. Extract the single most impactful failure mode encountered this run.
3. Append one new rule to the project's `CLAUDE.md` under `## Lessons`, phrased as a positive directive for the next pre-flight run.
4. Print the verdict + the path to `pre-flight.md` + the top 3 blockers (or "SHIP — send the DM" if no blockers).

## Output templates

See `${SKILL_DIR}/assets/pre-flight-template.md` for the canonical report format. The skill substitutes `{VERDICT}`, per-question `{PASS|FAIL}`, the 3 ranked blockers, and the trace-log path at synthesis time.

### CLAUDE.md ## Lessons section (appended by Phase 5)

```markdown
## Lessons (added {today as YYYY-MM-DD})

- {one project-shaped rule extracted from this pre-flight's biggest failure mode —
   phrased as a positive directive ("always cap SMTP test as part of DEPLOY gate")
   not a complaint about this run ("we forgot SMTP again")}
```

## Anti-patterns to avoid

1. **No more than four questions in Phase 2.** Four is the budget. The skill is supposed to be fast — readers run it Sunday morning before deciding whether to DM users Monday.
2. **No short-circuiting on first failure.** Run all four questions every time. A SHIP from Question 1 doesn't mean the trace works; a FAIL on Question 4 doesn't make Questions 1-3 irrelevant. The whole report is the artifact.
3. **No SHIP without all 4 passes.** SHIP is rare on the first pre-flight. The skill should default to FIX. If the user pushes for SHIP, ask which question they're overriding and why.
4. **No "approximate" blocker counts.** Top 3 means top 3, scored. If there are only 2 blockers, list 2. Never pad to 3 with cosmetic issues. The user is going to fix them in order.
5. **No auto-fixing the blockers.** Pre-flight is a diagnostic skill, not a remediation skill. The verdict is information; the human runs the fix.
6. **No silent drift verdicts.** If Question 4 fails because the product drifted, the report must NAME the dimension (user / job / outcome) and quote the before / after. Drift is the slowest failure mode; vague is the wrong response.
7. **No skipping the trace screenshots.** Question 2's screenshots are the most-cited artifact when readers reply to the post with their own pre-flight reports. Always save them to `pre-flight-trace/screens/`.

## What "done" looks like

The skill completed successfully when:

- A `pre-flight.md` exists at the project root with a SHIP / FIX / REBUILD verdict
- A `pre-flight-trace/` directory exists with `q1-output.json`, `q2-trace.json`, `q3-component.json`, `q4-drift.json` + `screens/` (if Question 2 ran)
- The project's `CLAUDE.md` has a new `## Lessons` entry naming the biggest failure mode and the positive directive that prevents it next time
- The user has an unambiguous one-line verdict at the top of `pre-flight.md`

The user should now be able to:

- Decide in <30 seconds whether to DM users today, fix and re-run pre-flight tomorrow, or rebuild based on drift
- Send the trace screenshots back to a beta-tester or first-user when soliciting feedback ("here's what the flow looks like — did you hit any of these?")
- Re-run `/pre-flight` after a fix cycle to confirm the blockers cleared
- Compound the skill's value over time as `CLAUDE.md ## Lessons` accumulates project-specific failure modes

## Start here

Begin with Phase 1 (silent discovery). Output nothing user-facing until Phase 2 (the four questions).
