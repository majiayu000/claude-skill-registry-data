---
name: make-it-hireable
description: Upgrade a student or college project into something that impresses interviewers by adding what real engineering teams expect (README, tests, CI, env config, error handling, linting, deployment, a fixed security flaw) in small, reviewed steps on a separate branch. Use when the user wants to improve a project for their resume, make a project production-ready or interview-ready, clean up a college project, or "make my project look professional".
---

# Make it hireable

The gap between a "college project" and "someone who can work on our codebase" is usually the same 8–10 things. This skill closes that gap in the candidate's real project, with them in the loop, so they can explain every change in an interview.

## 0. Setup

1. Call the Skill tool with "cracked-profile" (target role shapes priorities: a backend role cares about APIs, tests and DB; frontend about performance, accessibility and UX).
2. Confirm the project is the current directory and is a git repo. If it isn't a git repo, offer `git init` plus an initial commit first, so every change is reversible.
3. Check `git status`. If there are uncommitted changes, stop and ask them to commit or stash first.

## 1. Audit

Read the project: manifests, entry points, structure, config, tests, CI, deploy files, README. Score it against the checklist in [CHECKLIST.md](CHECKLIST.md) and show it as a table: `Item | Status (✅/🟡/❌) | Evidence (file:line)`.

Then propose an **upgrade plan**: the 5–8 highest-impact items, ordered by *interview value per hour of work*. Each item gets: what changes, the files touched, the estimated size (S/M/L), and **the interview talking point it creates** ("Now you can say: 'I added integration tests for the payment flow and a CI pipeline that blocks merges on failure.'").

**Wait for approval.** They can pick a subset.

## 2. Execute, one item at a time

1. Create a branch: `git checkout -b hireable/<short-name>`.
2. For each approved item:
   - Make the change in the project's existing style, language and framework. Don't rewrite the stack.
   - Verify it actually works: run the tests, build, lint, and start the app if feasible. Never claim it works without running it.
   - Commit with a clear conventional message (`test: add integration tests for cart API`).
   - Explain the change in 2–3 sentences **so they can explain it in an interview**: what, why, and the trade-off. If they can't explain it, the change is worth nothing on a resume.
3. Things you must **not** do: invent features, fake data or metrics, add dependencies without saying why, delete their code without asking, or push to a remote or deploy without explicit permission.

## 3. Wrap up

1. Summary table of what changed, with commit hashes.
2. **Resume bullets** reflecting the upgrades, using `[N]` placeholders for unknown metrics.
3. **Interview talking points**: 5 likely questions about these changes, with answers.
4. Next steps that need them (e.g. "Add your real Postgres URL to Vercel env and deploy").
5. Re-score the checklist and log a scorecard via the Skill tool with "cracked-profile". Dimensions: **Docs, Testing, Code Quality, Security, Deployability**. Show the before → after.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
