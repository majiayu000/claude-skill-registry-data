---
name: explain-code
description: Explain how code/features work by tracing execution flow. Saves markdown to ~/Developer/explanations/ and previews in browser.
---

# Code Explainer Skill

Explain how a feature or codebase works with focus on data flow and key logic.

## When to trigger

- User asks: "how does this work", "explain this feature", "remind me how X works"
- Before making changes to unfamiliar code
- When revisiting old code

## Instructions

1. **Identify scope:**
   - Ask user what feature/file/function to explain if unclear
   - For features: find entry points (routes, components, CLI commands)
   - For files: focus on that file and its direct dependencies

2. **Map the flow:**
   - Trace execution path from entry to exit
   - Identify key decision points (if/match statements, loops)
   - Note external calls (APIs, DB, file I/O)
   - Track state changes and side effects

3. **Extract key info:**
   - **Purpose:** What problem does this solve?
   - **Entry points:** Where does execution start?
   - **Data flow:** Input → transformations → output
   - **Key logic:** Important algorithms, validations, business rules
   - **Side effects:** DB writes, API calls, file changes, state updates
   - **Dependencies:** External libs, services, other modules

4. **Output format:**
   ```
   ## What it does
   [1-2 sentence summary]

   ## How it works
   1. [Step 1 with file:line references]
   2. [Step 2 with file:line references]
   3. [Step 3...]

   ## Key files
   - path/to/file.ts:123 - [what happens here]
   - path/to/other.rs:45 - [what happens here]

   ## Important logic
   [Any non-obvious algorithms, validations, or business rules]

   ## External dependencies
   [APIs called, DB tables used, services involved]

   ## Gotchas
   [Edge cases, assumptions, constraints, footguns]
   ```

5. **Focus on:**
   - The "why" behind non-obvious code
   - Critical paths and error handling
   - State mutations and side effects
   - Include file:line references for easy navigation

6. **Keep concise:**
   - Skip obvious stuff (standard library usage, simple getters)
   - Focus on the unique/complex parts
   - Summarize repeated patterns instead of listing each instance

## Tool access
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write

## Output method

1. **Generate explanation** in the format above
2. **Determine project name:**
   - Get current directory name or git repo name
   - Example: if in `/path/to/my-project`, project is `my-project`
3. **Write to explanations directory:**
   - Create dir: `~/Developer/explanations/<project-name>/` if not exists
   - Write file: `~/Developer/explanations/<project-name>/<feature-name>-<timestamp>.md`
   - Use feature name from user query (e.g., "auth", "parser", "sync-logic")
   - This keeps explanations outside project so they won't be committed
4. **Preview:**
   - Run `gh markdown-preview ~/Developer/explanations/<project-name>/<file>.md` in background
   - This starts a server and opens browser, but runs in background to yield control
   - User can stop server later with Ctrl+C or by killing the process
5. **Output to terminal:**
   - Show file path where explanation was saved
   - Show brief summary
   - Inform user that preview server is running in background

## Examples

**User:** "How does authentication work?"
**Output:**
```
## What it does
JWT-based auth with refresh tokens. Access tokens expire in 15min, refresh in 7 days.

## How it works
1. User sends credentials to /api/auth/login (routes/auth.ts:23)
2. Validate against DB, generate access + refresh tokens (lib/auth.ts:45)
3. Store refresh token in httpOnly cookie (lib/auth.ts:67)
4. Middleware validates access token on protected routes (middleware/auth.ts:12)
5. If expired, /api/auth/refresh issues new access token (routes/auth.ts:89)

## Key files
- routes/auth.ts:23 - Login endpoint, credentials validation
- lib/auth.ts:45 - Token generation with JWT
- middleware/auth.ts:12 - Token verification on each request

## Important logic
- Tokens signed with RS256 (private key in env)
- Refresh rotation: old token invalidated after refresh
- Rate limiting: 5 login attempts per 15min per IP

## Gotchas
- Refresh tokens stored in DB, must clear on logout
- Clock skew tolerance: 30 seconds
- CORS credentials must be true for cookies
```

## Principles

- Assume the user wrote this but forgot
- Be a helpful reminder, not a lecture
- Trace the actual execution path
- Point to specific lines for deep-dive
- Highlight non-obvious decisions
