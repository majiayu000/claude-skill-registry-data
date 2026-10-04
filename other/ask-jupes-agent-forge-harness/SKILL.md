---
name: ask
description: Answer questions about the codebase from knowledge files. Use when the user runs /ask or asks a domain/knowledge question about the repos.
---

# /ask — Query Domain Knowledge

Answers questions about the codebase using knowledge files. Flags stale knowledge and spot-checks answers.

## Usage
```
/ask how does authentication work
/ask what is the API contract for the users endpoint
/ask where should I add new API routes
/ask what patterns does the frontend use for state management
```

---

## Step 1 — Load Knowledge Files

```bash
cat knowledge/_shared.yaml
cat knowledge/repos/<most-relevant-repo>.yaml
```

If the question spans multiple repos: load each relevant repo's YAML.

If no knowledge files exist yet:
- Report: "No knowledge files found. Run `/sync-knowledge <repo>` to generate them."
- Attempt to answer from direct code exploration (Steps 2-3)

---

## Step 2 — Staleness Check

For each knowledge file loaded, check how far behind HEAD it is:

```bash
# Get the commit hash when the knowledge file was last updated
git log -1 --format="%H %ai" -- knowledge/repos/<repo>.yaml

# Count commits since then
git rev-list --count <that-hash>..HEAD
```

If a file is **>50 commits behind HEAD**:
```
⚠ knowledge/repos/<repo>.yaml is stale (73 commits behind HEAD).
  Some answers may be outdated. Run: /sync-knowledge <repo>
```

---

## Step 3 — Answer from Knowledge

Synthesize the answer from the loaded YAML files.

Format the answer as:
1. **Direct answer** — 2-4 sentences addressing the exact question
2. **Key files** — list relevant files with line references if known
3. **Pattern/convention** — the standard approach used in this codebase
4. **Example** — a short code snippet if helpful

---

## Step 4 — Spot-Check (mandatory)

Before delivering the answer, verify 2-3 claims against the actual codebase:

```bash
# Verify a claimed file exists
ls src/hooks/useAuth.ts

# Verify a claimed function exists
grep -n "export function useAuth" src/hooks/useAuth.ts

# Verify a claimed pattern is actually used
grep -r "export function use" src/hooks/ --include="*.ts" | head -5
```

If a spot-check fails (file missing, function not found):
- Note the discrepancy: "Knowledge file says X but I couldn't find it — it may have been moved or renamed."
- Correct the answer based on what you actually find
- Flag: "The knowledge file appears stale in this area. Run /sync-knowledge <repo>."

---

## Step 5 — Deliver Answer

```
## Answer: how does authentication work

Authentication in this codebase uses JWT with refresh token rotation.

**Flow:**
1. Login → `POST /api/auth/login` returns `{accessToken, refreshToken}`
2. Access token lives in memory (not localStorage) — 15 min expiry
3. Refresh token is httpOnly cookie — 7 day expiry
4. `useAuth` hook handles auto-refresh before expiry

**Key files:**
- `src/hooks/useAuth.ts` — auth state and refresh logic
- `src/api/auth.ts` — login, logout, refresh API calls
- `src/middleware/requireAuth.ts` — route protection HOC

**Pattern:** All protected routes wrap with `<RequireAuth>` component.
New endpoints require the `Authorization: Bearer <token>` header.

**Spot-checked:**
- ✓ src/hooks/useAuth.ts exists
- ✓ refreshToken function found at line 87
- ✓ RequireAuth component confirmed in src/middleware/

---
Knowledge source: knowledge/repos/my-frontend.yaml (12 commits behind HEAD — reasonably fresh)
```

---

## Handling Missing Knowledge

If the knowledge files don't cover the question:
1. Explore the codebase directly (Grep + Read)
2. Answer from source code
3. Note: "This topic isn't in the knowledge files. Consider running /sync-knowledge to capture it."
