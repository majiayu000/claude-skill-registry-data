---
name: learnings-keeper
description: |
  Persistent cross-session knowledge base. Manages per-project learnings that compound
  across sessions — patterns, pitfalls, preferences, and project quirks. The agent
  gets smarter on your codebase over time. At session start, searches relevant learnings.
  During sessions, logs discoveries. Supports review, search, prune, and export.
  Use proactively when the agent encounters a durable project quirk, user preference,
  or pattern that would save 5+ minutes next time. Also use at session start to recover
  context. Triggers: "remember this", "log this", "what have we learned?", "show learnings".
---

# Learnings Keeper

You manage the **persistent knowledge** that makes the agent smarter across sessions.
Each project gets a `learnings.jsonl` file. Learnings compound — the agent reads
relevant entries at session start and logs new discoveries during work.

This is the memory the agent keeps between conversations.

---

## How It Works

```
Session 1                  Session 2                  Session 3
─────────                  ─────────                  ─────────
Works on auth flow         Reads auth learnings       Reads auth + api learnings
Logs: "JWT stored in       (max 3, scored by          (max 3, old ones decay)
httpOnly cookie"           relevance + decay)         Reinforces auth learning
                           Applies session 1 learning  → it lives longer
                           Logs: "Rate limiting
                           uses token bucket"
```

Each session builds on previous knowledge. The agent gets faster without
context rot because:
- **Hard cap:** max 3 learnings ever injected into context
- **Staleness decay:** 14-day half-life — unused learnings fade
- **Reinforcement:** frequently-used learnings survive decay
- **Compaction:** >5 entries on the same key get summarized into one
- **On-demand:** learnings are queried surgically, not dumped at session start

---

## Learnings Format

Each entry is a JSONL line:

```json
{
  "ts": "2026-04-29T10:30:00Z",
  "type": "pattern|pitfall|preference|quirk|operational",
  "key": "kebab-case-identifier",
  "insight": "Human-readable description of what was learned",
  "confidence": 8,
  "source": "observed|user-stated|inferred",
  "files": ["path/to/relevant/file.ts"],
  "skill": "skill-name-if-from-skill",
  "branch": "feature/auth",
  "tags": ["auth", "security"]
}
```

### Types

| Type | When to use | Example |
|------|------------|---------|
| `pattern` | Recurring code/arch pattern | "Error responses always use `{error, message, code}` format" |
| `pitfall` | Thing that broke and will break again | "Environment variables in Next.js need NEXT_PUBLIC_ prefix for client" |
| `preference` | User's stated taste/choice | "Prefers explicit error handling over try/catch wrappers" |
| `quirk` | Project-specific weirdness | "Port 3000 conflicts with AirPlay on macOS — use 3001" |
| `operational` | Command/fix that saves time | "Database reset: `npm run db:reset && npm run db:seed`" |

---

## Step 0: Session Start — Load Relevant Learnings

At the start of every session, get a tight context snippet — never the full file:

```bash
# This is what the agent calls. Returns at most 3 lines, or nothing.
python3 -c "
from distr.core.learnings.keeper import get_context_learnings
ctx = get_context_learnings()
if ctx:
    print(ctx)
else:
    print('LEARNINGS: 0 relevant')
"
```

Output: at most 3 lines like `[learnings] key: insight`. If nothing relevant,
returns None — inject nothing into context. The agent stays lean.

---

## Step 1: During Session — Log New Learnings

Log a learning when:
- You discover a durable project quirk that would save 5+ minutes next time
- A pattern is confirmed by the user ("yes, we always do it that way")
- A pitfall is encountered that will recur
- The user states a preference explicitly
- A debug session reveals a non-obvious fix

**Do NOT log:**
- Obvious facts ("this project uses TypeScript")
- One-time transient errors
- Things the user could trivially infer

### Logging command

```python
from distr.core.learnings.keeper import log_learning

log_learning(
    entry_type="pitfall",
    key="auth-middleware-swallows-errors",
    insight="auth.ts middleware returns 200 with empty body on token expiry instead of 401. Check for empty response bodies.",
    confidence=9,
    source="observed",
    files=["distr/core/auth/middleware.py"],
    tags=["auth", "security"],
)
```

### Example

After discovering that the auth middleware swallows errors silently:

```
Logged learning: "auth-middleware-swallows-errors"
Type: pitfall
Insight: "auth.ts middleware returns 200 with empty body on token expiry instead of 401. Check for empty response bodies in auth flow."
Confidence: 9/10
```

### Reinforcing (keep good learnings alive)

When a learning proves useful — the agent applied it and it worked — reinforce it.
This bumps its score so it survives staleness decay longer:

```python
from distr.core.learnings.keeper import reinforce_learning
reinforce_learning("auth-middleware-swallows-errors")
```

3+ reinforcements make a learning survive pruning indefinitely.

---

## Step 2: Search Learnings

When the user asks "what have we learned about X?":

```
Search learnings by:
- Key substring: grep "auth" learnings.jsonl
- Tag: grep "security" learnings.jsonl
- Recent: tail -20 learnings.jsonl
- By file: grep "middleware/auth.ts" learnings.jsonl
```

Output format:
```
LEARNINGS: "auth" (3 matches)
═══════════════════════════════
[2026-04-15] pitfall | auth-middleware-swallows-errors (confidence: 9/10)
  auth.ts middleware returns 200 with empty body on token expiry...

[2026-04-20] pattern | jwt-storage-strategy (confidence: 8/10)
  JWTs stored in httpOnly cookies, never localStorage. Refresh tokens...
```

---

## Step 3: Prune Stale Learnings

Periodically (every 10+ sessions), offer to prune:

- Learnings with confidence < 5 and age > 30 days
- Learnings about deleted files
- Learnings superseded by newer ones
- Learnings the user explicitly dismisses

Ask: "N learnings may be stale. Review and prune?" Options: yes, no, auto-prune low-confidence.

---

## Step 4: Cross-Project Learnings

When enabled by user preference, search learnings from OTHER projects on the same
machine. This finds patterns that apply across codebases.

```bash
# Cross-project search
for dir in ~/.decisions/learnings/*/; do
  if [ "$dir" != "~/.decisions/learnings/$SLUG/" ]; then
    echo "--- $(basename $dir) ---"
    tail -3 "$dir/learnings.jsonl" 2>/dev/null
  fi
done
```

User controls via: "enable cross-project" / "disable cross-project".

**Privacy:** Cross-project search stays local. No data leaves the machine.

---

## Step 5: Export / Backup

```bash
# Export all learnings as readable markdown
echo "# Learnings for $SLUG" > learnings-export.md
echo "" >> learnings-export.md
while IFS= read -r line; do
  echo "## $(echo "$line" | jq -r '.key') ($(echo "$line" | jq -r '.type'))"
  echo ""
  echo "> $(echo "$line" | jq -r '.insight')"
  echo ""
  echo "Confidence: $(echo "$line" | jq -r '.confidence')/10 | Source: $(echo "$line" | jq -r '.source') | Date: $(echo "$line" | jq -r '.ts')"
  echo ""
done < "$LEARN_FILE" >> learnings-export.md
```

---

## Integration Points

- **At session start:** `session-retro` and `ceo-scope-review` search learnings for context
- **During debugging:** `systematic-debugging` searches for similar past bugs
- **During review:** `pre-flight-review` checks learnings for known pitfalls
- **At session end:** `session-retro` logs top 3 patterns as learnings

This makes every skill smarter over time — learnings are the common substrate.

---

## Key Principles

- **Log once, benefit forever.** One 30-second log saves 15+ minutes every future session.
- **Be conservative.** Only log things that will actually help next time. Noise degrades search quality.
- **Compound visibly.** Show the user when a learning is applied: "Prior learning applied: auth-middleware-swallows-errors (confidence 9/10, from Apr 15)"
- **Stay local.** Learnings are project-scoped by default. Cross-project is opt-in.
- **Let the user edit.** Show what was logged, let the user correct or dismiss.
