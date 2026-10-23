---
name: save-session
description: 'Saves session progress, failures, and next steps for later resumption. Use when ending a work session, preserving context before limits, or handing off unfinished work.'
argument-hint: '[optional: topic override]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(date:*)
  - Bash(git:*)
---

# Save Session

Capture everything that happened in this session — what was built, what worked, what failed, what's left — and write it to a dated file so the next session can pick up exactly where this one left off.

**Questions:** class `checkpoint` (Step 5 review); headless (no question tool or chat turn): the file is written; report its path and finish. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## When to Use

- End of a work session before closing Claude Code
- Before hitting context limits (run this first, then start a fresh session)
- After solving a complex problem you want to remember
- Any time you need to hand off context to a future session

## Process

### Step 0 — Read the session-state contract

**Before writing anything, read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/session-state.md` (mandatory). It owns store, filename, and file format — follow it, do not restate it here.**

### Step 1 — Gather context

Before writing the file, collect:

- All files modified during this session (use `git diff` or recall from conversation)
- What was discussed, attempted, and decided
- Any errors encountered and how they were resolved (or not)
- Current test/build status if relevant

### Step 2 — Create the sessions folder if it doesn't exist

Create the canonical sessions folder (per the contract) in the user's Claude home directory:

```bash
mkdir -p ~/.claude/session-data
```

### Step 3 — Write the session file

Create a fresh file per the contract — never append to a previous session's file.

### Step 4 — Populate the file with the full template

Use the "File Format" template in the contract, following its interpretation rules: write every section honestly, "Nothing yet" / "N/A" for genuinely empty sections — an incomplete file is worse than an honest empty one. Exception: "Environment & Setup Notes" is optional — omit it entirely when there is nothing to record.

### Step 5 — Show the file to the user

After writing, display the full contents and ask:

```
Session saved to [actual resolved path to the session file]

Does this look accurate? Anything to correct or add before we close?
```

Wait for confirmation. Make edits if requested.

---

## Session File Format

The full session-file template, filename, and store rules live in the shared contract at `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/session-state.md` — read it and populate its "File Format" template exactly. Do not duplicate the template here.

---

## Example Output

```markdown
# Session: 2024-01-15

**Started:** ~2pm
**Last Updated:** 5:30pm
**Project:** my-app
**Topic:** Building JWT authentication with httpOnly cookies

---

## What We Are Building

User authentication system for the Next.js app. Users register with email/password,
receive a JWT stored in an httpOnly cookie (not localStorage), and protected routes
check for a valid token via middleware. The goal is session persistence across browser
refreshes without exposing the token to JavaScript.

---

## What WORKED (with evidence)

- **`/api/auth/register` endpoint** — confirmed by: Postman POST returns 200 with user
  object, row visible in Supabase dashboard, bcrypt hash stored correctly
- **JWT generation in `lib/auth.ts`** — confirmed by: unit test passes
  (`npm test -- auth.test.ts`), decoded token at jwt.io shows correct payload
- **Password hashing** — confirmed by: `bcrypt.compare()` returns true in test

---

## What Did NOT Work (and why)

- **Next-Auth library** — failed because: conflicts with our custom Prisma adapter,
  threw "Cannot use adapter with credentials provider in this configuration" on every
  request. Not worth debugging — too opinionated for our setup.
- **Storing JWT in localStorage** — failed because: SSR renders happen before
  localStorage is available, caused React hydration mismatch error on every page load.
  This approach is fundamentally incompatible with Next.js SSR.

---

## What Has NOT Been Tried Yet

- Store JWT as httpOnly cookie in the login route response (most likely solution)
- Use `cookies()` from `next/headers` to read token in server components
- Write `middleware.ts` to protect routes by checking cookie existence

---

## Current State of Files

| File                             | Status         | Notes                                           |
| -------------------------------- | -------------- | ----------------------------------------------- |
| `app/api/auth/register/route.ts` | PASS: Complete | Works, tested                                   |
| `app/api/auth/login/route.ts`    | In Progress    | Token generates but not setting cookie yet      |
| `lib/auth.ts`                    | PASS: Complete | JWT helpers, all tested                         |
| `middleware.ts`                  | Not Started    | Route protection, needs cookie read logic first |
| `app/login/page.tsx`             | Not Started    | UI not started                                  |

---

## Decisions Made

- **httpOnly cookie over localStorage** — reason: prevents XSS token theft, works with SSR
- **Custom auth over Next-Auth** — reason: Next-Auth conflicts with our Prisma setup, not worth the fight

---

## Blockers & Open Questions

- Does `cookies().set()` work inside a Route Handler or only in Server Actions? Need to verify.

---

## Exact Next Step

In `app/api/auth/login/route.ts`, after generating the JWT, set it as an httpOnly
cookie using `cookies().set('token', jwt, { httpOnly: true, secure: true, sameSite: 'strict' })`.
Then test with Postman — the response should include a `Set-Cookie` header.
```

---

## Notes

- Each session gets its own file — never append to a previous session's file
- The "What Did NOT Work" section is the most critical — future sessions will blindly retry failed approaches without it
- The file is meant to be read by Claude at the start of the next session via `/ycc:resume-session`
- Store, filename form, and file format are owned by `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/session-state.md` — follow it for any new session file
