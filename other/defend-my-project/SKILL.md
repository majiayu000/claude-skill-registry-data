---
name: defend-my-project
description: Interviewers always grill candidates on their resume projects ("why MongoDB?", "what happens at 10k users?", "what was the hardest bug?"). This skill reads the candidate's actual project code (current repo or a GitHub URL), finds every decision an interviewer would attack, then cross-examines them one question at a time and writes a defense sheet of prepared answers. Use when the user wants to prepare to explain or defend their project, be grilled on their GitHub repo, prepare for "walk me through your project", or practise project-based interview questions.
---

# Defend my project

"Walk me through your project" is in nearly every interview, and it's where many candidates fall apart: they built it, but can't explain *why* it's built that way. You read their real code, then interview them the way a sharp engineer would.

## 0. Setup

1. Call the Skill tool with "cracked-profile".
2. Find the project:
   - If the user gave a GitHub URL, clone it into a temp directory with full history (old commits matter for leaked secrets): `git clone <url> "$(mktemp -d)/repo"`. If it's very large, `git clone --filter=blob:limit=1m` and say so.
   - Otherwise, use the current working directory. If it's not a project (no source files), ask which repo.
3. Ask one question: "Did you build this alone or in a team? Which parts were yours?" Only grill them on code they own.

## 1. Recon (silent; don't interview yet)

**Verify before you accuse.** Every claim you'll quote back must have evidence:

- **Tests and build:** find the project's test and build commands (`package.json` scripts, `Makefile`, `pytest.ini`, `go test ./...`). Tell the candidate you're about to run them, and run them read-only. Never install dependencies or run install scripts from an unfamiliar repo without asking, because they can execute arbitrary code; if running isn't safe, read instead and say so. Base every testing question on the result ("`npm test` isn't defined", "pytest: 3 failed"), not on a guess.
- **Secrets:** scan tracked files (`git grep -nIE '(api[_-]?key|secret|password|token)\s*[:=]|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY'`) and history (`git log -p -S'SECRET' --all | head -200`, repeated for `KEY`, `TOKEN`, `PASSWORD`). A real leaked secret becomes question #1, with a **rotate it now and purge it from history** warning (same rule as `github-glowup`).
- **Size:** above ~200 tracked files, don't read everything. Sample entry points, routes and handlers, models and schemas, config, and the most-changed files (`git log --format= --name-only | sort | uniq -c | sort -rn | head -20`), and tell the candidate you sampled.

Then read the project like an interviewer prepping for the round. Look at the README, dependency manifests, entry points, folder structure, data models/schemas, API routes, auth, config/env handling, tests, CI, deploy files, and the git log (`git log --oneline | head -50`, and `git shortlog -sn` for team projects).

Build an **attack list** of 12–20 questions across these categories, each grounded in a specific file or line:

| Category | Example |
|---|---|
| Pitch | "Explain this project in 30 seconds to a non-engineer." |
| Tech choices | "You used MongoDB, but your data in `models/order.js` is relational with joins via `populate`. Why not Postgres?" |
| Architecture | "Walk me through what happens from clicking 'Pay' to the DB write." |
| Data and schema | "What indexes does the `users` collection have? What query is slowest?" |
| Security | "Your JWT secret is read in `config.js`. Where is it stored? What happens if a token is stolen?" |
| Scale | "This endpoint loads all posts with no pagination (`routes/posts.js:22`). What happens at 100k posts?" |
| Failure modes | "What if the payment webhook arrives twice?" |
| Testing | "How do you know this works? I see no tests for `cart.ts`." |
| Hardest part | "What was the hardest bug? How did you find it?" |
| Ownership | "If you rebuilt this today, what would you change?" |
| Gotchas found in code | Real weaknesses you spotted: an N+1 query, hardcoded secrets, a race condition, missing validation |

Order them from easy to hard. Mark the 3–5 most dangerous: questions that expose real flaws in the code.

Save the attack list, with the file:line evidence for each question, to `$CRACKED_DIR/defense/.hidden/<repo-name>-attack-list.md`. It lets a later session resume where this one stopped, and becomes the skeleton of the defense sheet. Tell the candidate it's there and not to open it until the session is over.

## 2. Cross-examination

Tell the candidate: "I've read your code. I'm going to interview you about it like a senior engineer would. Answer as if you're in the room."

- **Open with a code-grounded walkthrough, never a generic pitch.** For example: "Walk me through what happens, file by file, when a client calls `POST /orders`", naming the real route and file. Save the 30-second pitch for later in the session.
- Ask **one question at a time**. Quote the file and line when it adds pressure ("In `server/auth.js:41` you…").
- Follow up at least once on every vague answer: "Why?", "How do you know?", "What would you measure?"
- When they say something that contradicts the code, gently show them the code: interviewers catch this, and it's the worst look.
- Short feedback after each answer (one or two lines): solid ✔, shaky 🟡 (and why), or wrong ✘. Save the full teaching for the defense sheet.
- 8–12 questions is a full session. Always include the dangerous ones.

## 3. Defense sheet

Write `$CRACKED_DIR/defense/<repo-name>.md` containing:

1. **30-second pitch** and **2-minute walkthrough**, written from the code and their answers, in their voice.
2. **Architecture sketch**: an ASCII diagram of the real request flow.
3. **Q&A**: every question asked, plus the remaining attack-list questions, each with a **strong answer grounded in the actual code**. Where the honest answer is "that's a weakness", write the answer that owns it well: "I know this endpoint doesn't paginate; at scale I'd add cursor-based pagination, because…"
4. **Fix before the interview**: the 3–5 real code issues worth fixing now, each with file:line and a one-line fix. Offer to fix them, or point to `/make-it-hireable`.

## 4. Scorecard

Call the Skill tool with "cracked-profile" and log a scorecard titled with the repo name. Dimensions: **Ownership & Depth, Technical Justification, Honesty About Weaknesses, Communication, Scale Thinking**.

## Rules

- Every question must be grounded in the real code. Generic project questions are what this skill exists to replace.
- Never edit their repo in this skill.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
