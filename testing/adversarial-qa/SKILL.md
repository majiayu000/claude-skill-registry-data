---
name: adversarial-qa
description: >
  Exploratory, adversarial QA: exercise a feature through whichever surface(s)
  it exposes — UI, API, or both — and surface issues the plan and committed
  tests did not anticipate — not a re-verification of the spec. Invoked as
  /adversarial-qa for an ad-hoc session, or applied by the adversarial-qa
  sub-agent in the /feature workflow.
---

# /adversarial-qa — Exploratory QA

Exercise a feature in the running app and surface anything that looks wrong,
confusing, or likely to bite a real user. This is exploratory and adversarial,
not a re-verification of the spec — committed end-to-end tests encode the plan's
Requirements deterministically. Your job is to go beyond them.

If a plan was provided (inline or by path), read the Requirements section only
to understand what the feature does — not as a checklist to tick through.

If the caller passed a list of open deferred QA findings (even an empty
one — "none open" is a value, not an omission), use it as-is in step 5
below. Otherwise (an ad hoc `/adversarial-qa` run) get it yourself: run
`AGENTS.md` → *Task Tracking* → *List open deferred QA findings* if that
bullet holds a real command or tool call (not a `[TODO:]` placeholder and
not `none`), otherwise `gh issue list --label known-issue --state open`.
If the bullet holds a real command but you cannot execute it (e.g. it names
an MCP tool call you don't have), do **not** fall back to `gh` — that would
silently query the wrong tracker. Instead, report it under *Blockers* as
"known issues not checked: <reason>" and continue the rest of the pass.

---

## What to do

1. Determine the surface(s). From the plan's Requirements (or the diff, if no
   plan was given), decide whether the feature exposes a **UI** (templates,
   views, a controller path that renders a view/fragment/client-driven
   response), an **API** (a REST or other network-callable endpoint with no
   view layer), or both. Probe every surface the feature exposes — findings
   from one do not substitute for checking another.

2. Set up and drive the feature, per surface identified in step 1.

   - **UI surface** — start the local dev server with the project's dev-server
     command and drive the feature at the documented app URL (both in
     `AGENTS.md` → *Commands*) in a browser via the Playwright MCP. When you
     are done, stop it with the documented stop command — never `kill` by PID
     or hunt processes with `lsof`. If the server will not start or Playwright
     is unavailable, STOP and report the blocker. Do not substitute `curl`,
     SQL, or any other workaround for browser exploration on a UI surface —
     those answer different questions than what a real user experiences.

     For mechanical setup with a known, fixed sequence — logging in,
     navigating through boilerplate screens to reach the feature under test —
     batch the steps into one `browser_run_code_unsafe` call instead of a
     click/type/snapshot round trip per step; each round trip returns a full
     accessibility snapshot, which adds up fast. Reserve the granular tools
     (`browser_click`, `browser_snapshot`, etc.) for the actual exploration in
     step 3, where you need to see state after each action to decide the next
     one.

   - **API surface** — start the server the same documented way and issue
     requests against the same app URL (`AGENTS.md` → *Commands*) with `curl`
     via `Bash`. Stop the server the same documented way when done. If the
     server will not start, or a request needs credentials you don't have,
     STOP and report the blocker.

3. Probe beyond the happy path. Try things the planner likely did not
   enumerate, per surface:

   - **UI** — narrow viewports, keyboard-only navigation, browser back button,
     multiple tabs on the same form, paste of weird/long/XSS content,
     reloading mid-edit, error-toast timing, interactions with unrelated UI on
     the same page, stale state after a failed submit.

   - **API** — malformed, missing, or extra fields; wrong `Content-Type`;
     auth/authz boundaries (missing token, expired token, wrong role or
     tenant); idempotency and duplicate submission; pagination and limit edge
     cases; concurrent or racing requests; oversized payloads and
     unicode/injection strings in fields; status-code and error-envelope
     correctness; rate limiting.

4. Surface anything that looks off — even if it is not part of this feature's
   plan. Do not act "smart" by working around issues, inferring intent, or
   deciding a bug is "probably expected". Report it and let the developer
   decide.

5. Before writing the report, compare your findings against the known
   deferred issues gathered above (skip this if you reported a *Blockers*
   entry for them instead). A finding that matches an open `known-issue`
   goes in the *Known issues* section of the report (cite its task id), NOT in
   Findings — the developer has already triaged it once and should not have
   to re-triage it on every QA pass. If the observed behaviour is worse than
   or different from what the task describes, that difference IS a finding.

---

## Evidence

Only capture evidence once you've decided something is a finding worth
reporting — never while just looking around.

- **UI** — `browser_take_screenshot` returns an image, which costs
  meaningfully more than the text snapshots from `browser_snapshot`, so
  screenshotting every step of the exploration adds up quickly for no
  benefit. Take one only once a finding is confirmed.
- **API** — capture the request and response that shows the problem: method,
  URL, relevant headers, status code, and body.

Save each finding's evidence under `.qa-evidence/` at the repo root
(gitignored); every finding in the report MUST cite at least one evidence
file there, with a one-sentence description of what it shows.

---

## Output Format

```
### Findings
- [Short description] — [evidence path] — [severity: bug / concern / nit]

### Known issues (already deferred — no action needed)
- [task id] [title] — [still present / not observed on this pass]

### Blockers (if any)
[Anything that prevented you from exploring — server won't start, Playwright
unavailable, credentials needed, etc.]
```

An empty `Findings` section is a valid output if you genuinely probed the
feature and found nothing worth flagging. An empty output because you "ran out
of ideas" is not.
