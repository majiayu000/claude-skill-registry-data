---
name: agent-gotchas
description: >-
  AI coding agents fail in consistent, predictable ways. They fabricate npm
  packages that don't exist. They catch errors and continue silently. They add
  features you never asked for. They lose context mid-session and forget what
  they were doing.
---
# AI Agent Gotchas

> AI agents are powerful but predictably unreliable. Know their failure modes.

## The Problem

AI coding agents fail in consistent, predictable ways. They fabricate npm packages that don't exist. They catch errors and continue silently. They add features you never asked for. They lose context mid-session and forget what they were doing.

These aren't bugs—they're fundamental characteristics of LLM-based agents. You can't fix them, but you can work around them.

The insight: AI agents are reliable tools with unreliable execution. Build guardrails, verify outputs, and design workflows that assume failure.

## The Pattern

### 1. Atomic Edits for Multi-File Changes

**Problem:** AI tools like Edit or Write run individually. If you make 5 file changes, there are 5 separate tool calls. Between tool calls, hooks can run, other sessions can interfere, or the agent can lose context.

**Example failure:**
```
Agent: "I'll update 3 files for the auth feature"
[Edit file1.ts] ✓
[PostToolUse hook runs, reformats file1.ts]
[Edit file2.ts] ✓
[Another session force-pushes, rebases branch]
[Edit file3.ts] ✗ Fails, branch state changed

Result: Partial implementation, inconsistent state
```

**Solution: Single-transaction pattern**

Use a shell script to make all changes atomically:

```bash
python3 << 'EOF'
import json

# Read all files
with open('file1.ts', 'r') as f:
    file1 = f.read()
with open('file2.ts', 'r') as f:
    file2 = f.read()
with open('file3.ts', 'r') as f:
    file3 = f.read()

# Make all changes
file1 = file1.replace('old1', 'new1')
file2 = file2.replace('old2', 'new2')
file3 = file3.replace('old3', 'new3')

# Write all files
with open('file1.ts', 'w') as f:
    f.write(file1)
with open('file2.ts', 'w') as f:
    f.write(file2)
with open('file3.ts', 'w') as f:
    f.write(file3)
EOF

# Atomic commit
git add file1.ts file2.ts file3.ts
git commit -m "feat: implement auth feature"
```

**Why this works:**
- All file changes happen in one tool call (Bash)
- Hooks run once at the end, not between edits
- Other sessions can't interfere mid-edit
- Agent can't lose context between files

**When to use:**
- Multi-file refactors (renaming, moving functions)
- Feature implementation spanning multiple modules
- Migration scripts (updating all files to new pattern)
- Any change where partial completion is invalid

### 2. Hook Interference

**Problem:** PostToolUse hooks (Prettier, ESLint --fix, formatters) can revert agent changes.

**Example failure:**
```typescript
// Agent edits file to add function
export function newFeature() {
  return "value"
}

// PostToolUse hook runs Prettier
// Prettier removes "unused" import the function depends on
import { dependency } from './lib';  // REMOVED by hook
export function newFeature() {
  return "value"  // Now broken, missing dependency
}
```

**Solution: Disable hooks for multi-step changes**

```bash
# Disable hooks temporarily
export SKIP_HOOKS=1

# Make changes
# ... agent edits files ...

# Re-enable and run manually
unset SKIP_HOOKS
npm run format
npm run lint:fix
git add .
git commit -m "feat: add feature"
```

**Or: Verify after each change**

```bash
# After agent edits
git diff  # Verify change is what you expect
npm run format  # Run formatters manually
git diff  # Verify formatters didn't break anything
git add .
git commit -m "feat: add feature"
```

**Where hooks interfere:**
- Prettier removing "unused" code that's about to be used
- ESLint auto-fixing away intentional patterns
- TypeScript auto-imports conflicting with manual imports
- Git hooks rejecting commits mid-workflow

### 3. Session Interference

**Problem:** Multiple AI sessions working on the same repository switch branches, force-push, or close PRs between each other's tool calls.

**Example failure:**
```
Session A (Terminal 1):
  [List files in feature/auth] ✓
  [Read auth.ts] ✓

Session B (Terminal 2):
  git checkout main
  git branch -D feature/auth
  git push origin :feature/auth

Session A (Terminal 1):
  [Edit auth.ts] ✗ Error: branch 'feature/auth' not found
```

**Solution: Use worktrees for isolation**

```bash
# Session A
git worktree add ~/.claude/worktrees/session-a feature/auth
cd ~/.claude/worktrees/session-a
# Work here, fully isolated

# Session B
git worktree add ~/.claude/worktrees/session-b feature/payments
cd ~/.claude/worktrees/session-b
# Work here, can't interfere with Session A
```

See [git-worktrees.md](git-worktrees.md) for full pattern.

**Worktree isolation prevents:**
- Branch switching mid-task
- Force-push overwrites
- PR closures breaking other sessions
- Merge conflicts from simultaneous edits

### 4. Context Window Overflow

**Problem:** Long AI sessions accumulate context (files read, commands run, conversation history). After 100K+ tokens, early context is lost. Agent forgets project structure, coding standards, or what it was doing.

**Example failure:**
```
Early in session:
  You: "Use functional components, no classes"
  Agent: "Got it, functional components only"

50 files later:
  Agent: "I'll create a class component for this feature"
  You: "I said no classes!"
  Agent: "Sorry, I don't see that instruction in our conversation"
```

**Solution: Proactive context save**

At ~70% context usage (~140K tokens), save state:

```bash
# Save current progress
cat > .claude/in-progress.md << EOF
# Auth Feature Implementation

## Completed
- [x] User model with email/password
- [x] JWT generation utility
- [x] Login endpoint

## In Progress
- [ ] Password reset flow
- [ ] Email verification

## Coding Standards
- Functional components only
- Functions < 50 lines
- Zod for validation (pattern: @lib/validators/user.ts)

## Next Steps
1. Implement password reset token generation
2. Add email sending service
3. Create reset verification endpoint
EOF

# Compress context
/compact

# Resume with loaded context
cat .claude/in-progress.md
# Continue work with fresh context window
```

**Automated context monitoring:**
```bash
# Add to shell prompt
function context_usage() {
  # Estimate based on conversation length
  if [ -f .claude/context-estimate ]; then
    cat .claude/context-estimate
  fi
}

PS1='[$(context_usage)] $ '
```

### 5. Fabricated Metrics

**Problem:** AI agents invent statistics, npm download counts, GitHub stars, or performance numbers when they don't have real data.

**Example fabrication:**
```markdown
## Our Library

- 100K+ npm downloads/month 🚀
- 5K+ GitHub stars ⭐
- 95% test coverage ✅
- Used by companies like Google, Netflix, Uber

(All numbers made up by AI)
```

**Real data:**
- 47 npm downloads/month
- 12 GitHub stars
- 60% test coverage
- No known enterprise users

**Solution: Use dynamic badges with real data**

```markdown
## Our Library

![npm downloads](https://img.shields.io/npm/dm/@scope/package)
![GitHub stars](https://img.shields.io/github/stars/user/repo)
![coverage](https://img.shields.io/codecov/c/github/user/repo)

<!-- Badges auto-update with real data -->
```

**Or: Fetch real metrics**

```bash
# Get npm downloads
npm_downloads=$(curl -s https://api.npmjs.org/downloads/point/last-month/@scope/package | jq '.downloads')

# Get GitHub stars
gh_stars=$(gh api repos/user/repo --jq '.stargazers_count')

# Update README with real data
sed -i "s/DOWNLOADS_PLACEHOLDER/$npm_downloads/g" README.md
sed -i "s/STARS_PLACEHOLDER/$gh_stars/g" README.md
```

**Never trust agent-provided:**
- Download counts, star counts, popularity metrics
- Performance benchmarks (unless you ran them)
- User testimonials or case studies
- "Industry standard" claims

**Always verify:**
- npm API for download counts
- GitHub API for stars/forks
- Your own analytics for user counts
- Actual benchmarks for performance

### 6. Dependency Hallucination

**Problem:** AI suggests packages that don't exist, outdated APIs, or deprecated libraries.

**Example hallucination:**
```typescript
// Agent suggestion
import { validateEmail } from '@utils/email-validator';
import { formatDate } from 'date-fns/format';
import { parseJWT } from 'jwt-helper';

// Reality
// @utils/email-validator - doesn't exist
// date-fns/format - wrong import path (should be 'date-fns')
// jwt-helper - package doesn't exist (maybe meant 'jsonwebtoken'?)
```

**Solution: Verify every new dependency**

```bash
# Before installing agent-suggested package
npm info <package-name>

# Check if it exists, last publish date, version
# If "ERR! 404 Not Found": package doesn't exist

# Check actual API
npm info <package-name> exports
# Or read the package README
```

**Red flags:**
- Package name too generic (`email-validator`, `jwt-helper`)
- No npm downloads/week listed
- Last publish > 2 years ago
- No GitHub link or documentation

**Safer approach:**
```
You: "I need to validate emails"
Agent: "Use @utils/email-validator"
You: "Does this package exist? Check npm API first"
Agent: [checks] "Package doesn't exist. Use 'validator' instead (2M downloads/week)"
```

### 7. Over-Engineering

**Problem:** AI agents add features you didn't ask for: caching, logging, metrics, retry logic, feature flags, etc.

**Example over-engineering:**
```typescript
// You asked for: "Add a function to get user by ID"

// Agent delivers:
async function getUser(
  id: string,
  options: {
    cache?: boolean;
    cacheTTL?: number;
    retry?: number;
    timeout?: number;
    includeDeleted?: boolean;
    includeMetadata?: boolean;
  } = {}
): Promise<User> {
  const cacheKey = `user:${id}`;

  if (options.cache) {
    const cached = await redis.get(cacheKey);
    if (cached) {
      logger.info('Cache hit', { userId: id });
      return JSON.parse(cached);
    }
  }

  let attempts = 0;
  while (attempts < (options.retry || 3)) {
    try {
      const user = await db.users.findById(id, {
        includeDeleted: options.includeDeleted,
        timeout: options.timeout || 5000
      });

      if (options.cache) {
        await redis.set(cacheKey, JSON.stringify(user), 'EX', options.cacheTTL || 300);
      }

      logger.info('User fetched', { userId: id, attempts });
      metrics.increment('user.fetch.success');

      return user;
    } catch (err) {
      attempts++;
      logger.error('User fetch failed', { userId: id, attempt: attempts, error: err });
      metrics.increment('user.fetch.error');

      if (attempts >= (options.retry || 3)) {
        throw err;
      }
    }
  }
}

// You needed:
async function getUser(id: string): Promise<User> {
  return db.users.findById(id);
}
```

**Solution: Constrain scope explicitly**

```
Add a function to get user by ID.

Requirements:
- Input: user ID (string)
- Output: User object or throw NotFoundError
- Implementation: Call db.users.findById()
- NO caching, NO retry logic, NO logging, NO metrics
- < 10 lines

Example:
async function getUser(id: string): Promise<User> {
  const user = await db.users.findById(id);
  if (!user) throw new NotFoundError('User not found');
  return user;
}
```

**Red flags for over-engineering:**
- Function is 3x longer than expected
- Added dependencies you didn't ask for
- Options object with 5+ parameters
- Feature flags for simple behavior
- Caching/retry/circuit-breaker for non-critical path

### 8. Silent Failures

**Problem:** AI agents catch errors and continue silently, hiding failures.

**Example silent failure:**
```typescript
async function processOrders(orders: Order[]) {
  for (const order of orders) {
    try {
      await processOrder(order);
    } catch (err) {
      // Agent added this silently
      console.log('Failed to process order', err);
      // Continues to next order, no error thrown
    }
  }
  return { success: true };  // Lies!
}

// Result: Some orders failed, but caller thinks all succeeded
```

**Solution: Explicit error handling strategy**

```
Implement processOrders(orders):
- Process each order
- On error: collect failed orders, don't stop processing
- Return: { processed: Order[], failed: { order: Order, error: string }[] }
- Let caller decide how to handle failures

DO NOT catch and ignore errors silently.
```

**Better implementation:**
```typescript
async function processOrders(orders: Order[]) {
  const processed: Order[] = [];
  const failed: { order: Order; error: string }[] = [];

  for (const order of orders) {
    try {
      await processOrder(order);
      processed.push(order);
    } catch (err) {
      failed.push({ order, error: err.message });
    }
  }

  return { processed, failed };
}
```

**Watch for:**
- Try/catch with only console.log
- Errors caught but not re-thrown or returned
- Success response when partial failure occurred
- Missing error details in response

### 9. Test Data Pollution

**Problem:** AI-generated tests use unrealistic data that passes tests but fails in production.

**Example bad test data:**
```typescript
it('creates user', async () => {
  const user = await createUser({
    email: 'test@test.com',
    name: 'Test User',
    age: 99
  });

  expect(user.id).toBeDefined();
});

// Production failure:
// Real user "María José García-López" with email "maria.jose@empresa.com"
// Name validation rejects special characters!
```

**Solution: Realistic test data**

```typescript
it('creates user with international characters', async () => {
  const user = await createUser({
    email: 'maria.jose@empresa.com',
    name: 'María José García-López',
    age: 34
  });

  expect(user.id).toBeDefined();
  expect(user.name).toBe('María José García-López');
});
```

**Require realistic test data:**
```
Generate tests for createUser.

Test data requirements:
- Real names (not "Test User", "John Doe", "foo bar")
- Real email domains (not test.com, example.com)
- International characters (María, 北京, Müller)
- Edge cases (very long names, special characters, numbers)

Examples of good test data:
- "Sarah Chen", "sarah.chen@company.com"
- "José García", "jose.garcia@startup.io"
- "李明", "liming@tech.cn"
```

### 10. Configuration Drift

**Problem:** Agent creates `.env.example` but doesn't update actual `.env`, or vice versa.

**Example drift:**
```bash
# .env.example (what agent updated)
DATABASE_URL=postgresql://localhost/myapp
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-here
NEW_FEATURE_FLAG=true  # Agent added this

# .env (what's actually used)
DATABASE_URL=postgresql://localhost/myapp
REDIS_URL=redis://localhost:6379
JWT_SECRET=prod-secret
# NEW_FEATURE_FLAG missing! Feature doesn't work.
```

**Solution: Sync config files**

```
Add NEW_FEATURE_FLAG to environment config.

Update BOTH files:
1. .env.example (with placeholder value)
2. .env (with actual value or prompt me for it)

After updating, verify they have the same keys:
```bash
diff <(grep '^[A-Z]' .env | cut -d= -f1 | sort) <(grep '^[A-Z]' .env.example | cut -d= -f1 | sort)
```

If diff shows missing keys, update both files.
```

**Automated sync check:**
```bash
# add to CI
npm run config-check

# package.json
{
  "scripts": {
    "config-check": "node scripts/check-env-sync.js"
  }
}

// scripts/check-env-sync.js
const fs = require('fs');

const env = fs.readFileSync('.env', 'utf8');
const example = fs.readFileSync('.env.example', 'utf8');

const envKeys = env.match(/^[A-Z_]+=/gm)?.map(k => k.slice(0, -1)) || [];
const exampleKeys = example.match(/^[A-Z_]+=/gm)?.map(k => k.slice(0, -1)) || [];

const missing = exampleKeys.filter(k => !envKeys.includes(k));
if (missing.length > 0) {
  console.error('Missing in .env:', missing);
  process.exit(1);
}
```

## Anti-Patterns

### 1. Trusting Agent Memory

**Bad:**
```
Session start:
  You: "Use TypeScript strict mode and Zod validation"
  Agent: "Got it"

2 hours later:
  Agent: *generates code with implicit any and no validation*
  You: "I told you to use strict mode!"
  Agent: "I don't recall that instruction"
```

**Why bad:** Context window is limited. Early instructions are forgotten.

**Fix:**
```
Create .claude/standards.md:

# Coding Standards
- TypeScript strict mode (no implicit any)
- Zod for all input validation
- Functions < 50 lines
- No classes, use functional components

Reference this file at start of each session:
"Follow the standards in .claude/standards.md"
```

### 2. No Verification After Agent Changes

**Bad:**
```
Agent: "I've updated the database schema"
You: "Great, thanks!"
[deploys to production]
[production crashes - migration broke]
```

**Why bad:** Agent might have made incorrect changes, broken migrations, or missed edge cases.

**Fix:**
```
Agent: "I've updated the database schema"
You: "Show me the diff"
[Review changes]
You: "Run the migration on a test database first"
[Verify it works]
You: "Run rollback test"
[Verify rollback works]
You: "Now deploy to production"
```

### 3. Accepting First Solution

**Bad:**
```
You: "How do I cache API responses?"
Agent: "Use an in-memory Map"
You: "Okay" [implements in-memory cache]
[Doesn't scale, memory leak in production]
```

**Why bad:** Agent gives first solution that pops up, not best solution.

**Fix:**
```
You: "How do I cache API responses? List 3 options with tradeoffs"
Agent:
  1. In-memory Map (fast, doesn't scale across servers, memory leak risk)
  2. Redis (scales, adds latency, requires infrastructure)
  3. CDN caching (fastest, limited control, only for public data)

You: "We have Redis already. Use option 2"
```

### 4. Not Constraining Output Size

**Bad:**
```
You: "Generate tests for UserService"
Agent: [generates 500 tests, 3000 lines, covers every possible permutation]
```

**Why bad:** Too many tests = slow CI, hard to maintain, diminishing returns.

**Fix:**
```
You: "Generate 10 critical tests for UserService"
- Happy path (1 test)
- Validation errors (3 tests)
- Permission errors (2 tests)
- Edge cases (4 tests)

Each test < 20 lines. Use realistic data.
```

### 5. Ignoring Agent Uncertainty

**Bad:**
```
Agent: "I think the issue might be in the database connection, possibly related to connection pooling, though it could also be a timeout issue"
You: "Fix it"
Agent: [makes random changes]
[Problem persists]
```

**Why bad:** Agent is guessing. Random changes waste time.

**Fix:**
```
Agent: "I think the issue might be..."
You: "You're uncertain. Let's diagnose first:"
  1. Add logging to connection pool
  2. Check timeout configuration
  3. Monitor connection count
  4. Review recent DB changes

[Gather data]
[Identify root cause]
[Make targeted fix]
```

## Trust Model Mismatch When Switching Tools

**Problem:** Different AI coding tools have opposite default trust models. Switching between them without adjusting expectations causes surprises.

| Tool | Default trust model | Isolation requires |
|------|--------------------|--------------------|
| Claude Code | Trust-first | Explicit permission boundaries |
| OpenCode | Trust-first | Explicit sandbox config |
| Cursor | Trust-first | No built-in sandboxing |
| **Codex CLI** | **Sandbox-first** | **Opting out of restrictions** |

Codex starts from a conservative sandbox posture. If a Codex task silently fails or
cannot reach an API, check sandbox mode and approval settings before debugging the code.

**Solution:**

Match your approval policy to the task, not to the tool's default:

```bash
# Codex: loosen when you need network or cross-dir writes
codex --sandbox danger-full-access "deploy to staging"

# Claude Code / OpenCode: tighten when running unreviewed tasks
# (use scoped /plan mode or restrict tool permissions in config)
```

When switching between tools in the same workflow, explicitly state the trust context in your prompt:
```
# Be explicit regardless of which tool you're using:
"Read-only: explain the auth flow without making changes."
"Full access needed: update the database migration and test it."
```

## Verification Checklist

After any agent-generated code:

- [ ] Run linter/formatter (verify code style)
- [ ] Run type checker (verify types are correct)
- [ ] Run tests (verify behavior is correct)
- [ ] Check for new dependencies (verify they exist on npm)
- [ ] Review diff (verify changes match request)
- [ ] Test locally (verify it works in dev)
- [ ] Check logs (verify no silent errors)
- [ ] Review config files (verify .env and .env.example match)
- [ ] Check bundle size (verify no bloat)
- [ ] Review security (verify no exposed secrets or vulnerabilities)

If any check fails: don't merge. Fix issues first.

AI agents are powerful but unreliable. Build guardrails. Verify everything. Design for failure.
