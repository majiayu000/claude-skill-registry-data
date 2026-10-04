---
name: teach
description: >
  Generates a structured developer-facing markdown document that teaches how a specific feature, module, or
  piece of functionality works in the codebase. Use this skill whenever the user runs `/teach`, asks "how does X
  work", "explain the auth flow", "document how payments work", "walk me through the webhook system", or any
  request to understand and document internal codebase functionality. Also trigger when the user wants to produce
  onboarding docs, feature walkthroughs, or "how it works" references for developers. Always use this skill even
  if the user only gives a vague description — use the provided context or file hints to locate the relevant code
  yourself and build the teaching doc from there. This skill writes for developers reading the codebase — for
  end-user/customer-facing help docs, use the eli5-features skill instead.
---

# Teach Skill

Generates a polished, developer-facing markdown document that explains how a specific piece of codebase
functionality works — tracing execution, data flow, dependencies, and gotchas — so developers can quickly
understand, debug, or extend it.

---

## Invocation

The user will typically invoke this with:

```
/teach <topic> [context]
```

Examples:
```
/teach payments
/teach "how auth middleware works" --files src/middleware/auth.ts src/lib/session.ts
/teach webhook system -- context: lives in src/webhooks/, uses Bull queue, writes to postgres
/teach affiliate commission flow -- entry point is src/api/affiliate/payout.ts
```

Context can be:
- Specific file paths (`--files` or just listed inline)
- A description of where to look (`-- context: ...`)
- An entry point file or function name
- Nothing — Claude explores the repo to find it

Note: `--files` and `-- context:` are informal conventions inside free text, not parsed flags — interpret them
loosely rather than expecting exact syntax.

If no context is given, Claude should search for the topic using file names, function names, route definitions,
comments, and directory structure before asking the user for help.

---

## Teaching Methodology

Every generated doc MUST follow this structure. Do not skip sections.

### 1. What Is This?
One paragraph. Plain English. What does this feature/module do and why does it exist?
No code yet. Just purpose.

### 2. Entry Point
Where does execution begin? This could be:
- An API route (`POST /api/payments/charge`)
- A queue consumer (`worker.process('send-email', ...)`)
- A scheduled job, webhook receiver, CLI command, etc.

Include the file path and line range. Show the entry point code snippet.

### 3. Execution Flow
Step-by-step trace of what happens after the entry point fires. Use a numbered list.
For each step:
- What function/module is called
- What file it lives in
- What it does
- What it returns or mutates

Show code snippets for each meaningful step. Keep snippets tight (5–20 lines). Use comments in the snippets
to highlight what matters.

### 4. Data Flow
How does data move through the system?
- What comes in (request body, queue payload, DB row, etc.)
- How it's transformed at each stage
- What goes out (response, DB write, event emit, etc.)

If there's a DB schema involved, show the relevant table/model fields. If there's a type/interface that
defines the shape, show it.

### 5. Key Dependencies
List the internal modules and external packages this feature depends on. For each:
- Name + file path (for internal) or package name (for external)
- One-line description of its role in this feature
- Any non-obvious configuration or initialization required

### 6. Error Handling & Edge Cases
What can go wrong? How is it handled?
- Explicit try/catch or error middleware
- Validation failures
- External service timeouts or failures
- Known edge cases or TODOs in the code worth flagging

### 7. Where To Look If Something Breaks
Practical debugging guide. For each likely failure mode:
- What symptom the developer would see (log message, error response, etc.)
- Which file/function to inspect first
- Any relevant environment variables, feature flags, or config values

### 8. How To Extend This
If a developer needs to add to or modify this feature, what do they need to know?
- Where to add a new case/handler/step
- What conventions to follow (naming, error handling patterns, etc.)
- Any tests to update

---

## Output Format

- Output a single markdown file
- Filename: `how-[topic-slug]-works.md` (e.g., `how-payments-works.md`)
- Save to a `docs/` folder at the project root; if that doesn't exist, tell the user you're about to create it, then create it
- If a `docs/` folder already exists with an index or README, tell the user what reference you're about to add, then append it — don't silently mutate existing files
- After saving, print the file path and a one-line summary of what was documented

## Code Snippet Rules

- Always include the file path as a comment above each snippet: `// src/lib/stripe.ts`
- Keep snippets focused — trim irrelevant lines, use `// ...` to indicate omissions
- Prefer showing real code over pseudocode
- Do not reproduce entire files — extract only what teaches the concept

## Tone & Depth

- Write for a mid-level developer who is unfamiliar with this part of the codebase
- Assume they know TypeScript/Node/React/SQL — don't over-explain language basics
- Be specific and concrete. "This calls `chargeCard()` in `src/lib/stripe.ts`" is better than
  "This calls the payment function"
- Flag anything surprising, non-obvious, or that has caused bugs before (if visible in comments/git blame)

---

## When Context Is Provided

If the user provides file paths, use those as the starting point and trace outward.
If the user provides a description of where to look, search that area first.
If the user provides an entry point function/route, start there and follow the call graph.

Never ask the user to find the files for you unless the codebase search returns genuinely ambiguous results.
Use grep, find, and directory tree inspection to locate relevant code.

---

## When No Context Is Provided

1. Search for the topic keyword in: file names, function names, route definitions, class names, comments
2. Check common locations: `src/`, `app/`, `lib/`, `api/`, `services/`, `workers/`, `utils/`
3. Look at the directory tree for any folder that matches the topic
4. If multiple candidates are found, briefly note them in the doc intro and focus on the most likely one
5. Only ask the user for clarification if the codebase has genuinely ambiguous matches

---

## Redirects

If the request is for end-user or customer-facing help docs ("explain this to a customer", "write a help
article for X"), route to the `eli5-features` skill instead — this skill's output is developer-facing.

---

## Example Output Structure

```markdown
# How Payments Work

## What Is This?
...

## Entry Point
`POST /api/payments/charge` — `src/app/api/payments/charge/route.ts`

\`\`\`typescript
// src/app/api/payments/charge/route.ts
export async function POST(req: Request) {
  // ...
}
\`\`\`

## Execution Flow
1. **Validate request** — `src/lib/validators/payment.ts`
   ...

## Data Flow
...

## Key Dependencies
...

## Error Handling & Edge Cases
...

## Where To Look If Something Breaks
...

## How To Extend This
...
```
