---
name: workflow-execution-rules
description: Execution workflow preferences including no dev servers, read-only information gathering, real data over mocks, and proper error handling over fallbacks. Use when executing code, running servers, testing, or handling data.
version: 1.0.0
---

# Workflow Execution Rules

Execution preferences and workflow guidelines for development tasks.

## Core Rules

### 1. Never Run Dev Servers

**User controls dev servers already.**

**DON'T:**
```bash
# ❌ Never run these
pnpm dev
npm run dev
yarn dev
npm start
node server.js
python manage.py runserver
```

**DO:**
```markdown
✅ Tell user how to run:
"To test these changes, run: `pnpm dev`"

✅ Focus on code, not running it
```

**Why:**
- User already has dev server running
- Avoids port conflicts
- User controls when to restart
- Keeps development flow smooth

**Exception:**
User explicitly asks: "Can you run the dev server for me?"

Even then, confirm first:
```markdown
"I can run the dev server, but you may already have one running on port 3000. Should I proceed?"
```

### 2. Focus on Code, Not Running It

**Just focus on the code, not running it.**

**Bad approach:**
```markdown
1. Write code
2. Run tests
3. Start dev server
4. Open browser
5. Test functionality
6. Report results
```

**Good approach:**
```markdown
1. Write code
2. Explain what it does
3. Tell user how to test it
4. User runs and verifies
```

**Example:**

```markdown
I've updated the authentication logic in `src/auth/login.ts`.

Changes:
- Added JWT token validation
- Improved error handling
- Added session timeout

To test:
1. Run: `pnpm dev`
2. Navigate to `/login`
3. Try logging in with test credentials
4. Verify token is stored in localStorage

Let me know if you encounter any issues.
```

### 3. Read-Only Information Gathering

**Use tools for information gathering only, read-only.**

**Allowed:**
```bash
# ✅ Reading files
cat file.txt
grep "pattern" file.txt
ls -la

# ✅ Checking status
git status
git diff
git log

# ✅ Inspecting packages
npm list
cat package.json

# ✅ Checking environment
node --version
which npm
echo $PATH
```

**Not allowed without permission:**
```bash
# ❌ Modifying files (use Write tool instead)
echo "text" > file.txt
sed -i 's/old/new/' file.txt

# ❌ Installing packages (ask first)
npm install package
pip install package

# ❌ Running builds (ask first)
npm run build
```

### 4. Never Integrate Into Repository as Dependency

**Always keep isolated from actual codebase.**

**Bad:**
```bash
# ❌ Don't add test packages to package.json
npm install --save-dev test-package

# ❌ Don't commit test code
git add test-file.js
git commit -m "Add test code"
```

**Good:**
```bash
# ✅ Use temporary files
echo "test code" > /tmp/test.js
node /tmp/test.js

# ✅ Keep experiments separate
# Don't commit experimental code
```

**Why:**
- Keeps codebase clean
- Avoids dependency bloat
- Prevents accidental commits
- Easy to remove experiments

### 5. Avoid Test Files

**Manual testing preferred over test files.**

**Bad approach:**
```typescript
// ❌ Creating test files unnecessarily
// tests/auth.test.ts
describe('Authentication', () => {
  it('should login user', () => {
    // test code
  });
});
```

**Good approach:**
```markdown
✅ Manual testing instructions:
1. Go to /login page
2. Enter credentials: test@example.com / password123
3. Click "Login"
4. Verify redirect to /dashboard
5. Check localStorage for auth token
```

**Why:**
- User prefers manual testing
- Faster iteration
- No test maintenance overhead
- Direct feedback

**Exception:**
User explicitly requests: "Can you write tests for this?"

### 6. Use Real Data, Not Mock Data

**Reject mock data, use real data always.**

**Bad - Mock data:**
```typescript
// ❌ Don't use mock data
const mockUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

function getUsers() {
  return mockUsers;
}
```

**Good - Real data:**
```typescript
// ✅ Use actual database/API
async function getUsers() {
  const users = await db.users.find();
  return users;
}

// Or fetch from API
async function getUsers() {
  const response = await fetch('/api/users');
  return response.json();
}
```

**Why:**
- Real data reveals actual issues
- Mock data hides edge cases
- Production-ready from start
- No transition from mock to real

**When real data unavailable:**
```markdown
"Real data source needed. Options:
1. Connect to staging database
2. Use development API endpoint
3. Create sample data in database

Which would you prefer?"
```

### 7. Proper Error Handling, Not Fallbacks

**Reject fallbacks, handle errors properly instead.**

**Bad - Fallback approach:**
```typescript
// ❌ Hiding errors with fallbacks
async function getUser(id: string) {
  try {
    return await api.getUser(id);
  } catch (error) {
    // Bad: returning fallback hides the error
    return { id, name: 'Unknown', email: 'unknown@example.com' };
  }
}
```

**Good - Proper error handling:**
```typescript
// ✅ Handle errors explicitly
async function getUser(id: string) {
  try {
    return await api.getUser(id);
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new Error(`User ${id} not found`);
    }
    if (error instanceof NetworkError) {
      throw new Error('Network error. Please try again.');
    }
    // Log unexpected errors
    console.error('Unexpected error fetching user:', error);
    throw error;
  }
}

// Let caller handle the error
try {
  const user = await getUser('123');
  displayUser(user);
} catch (error) {
  showErrorMessage(error.message);
}
```

**Why:**
- Fallbacks hide problems
- Errors provide useful information
- Easier to debug
- User knows what went wrong

**Error handling patterns:**

```typescript
// 1. Specific error types
class UserNotFoundError extends Error {
  constructor(userId: string) {
    super(`User ${userId} not found`);
    this.name = 'UserNotFoundError';
  }
}

// 2. Error boundary in UI
function UserProfile({ userId }: Props) {
  const { data: user, error } = useQuery(['user', userId], () =>
    getUser(userId)
  );

  if (error) {
    return <ErrorMessage error={error} />;
  }

  if (!user) {
    return <LoadingSpinner />;
  }

  return <UserDisplay user={user} />;
}

// 3. Retry logic for transient errors
async function fetchWithRetry(fn: () => Promise<any>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay(1000 * Math.pow(2, i)); // Exponential backoff
    }
  }
}
```

## Workflow Best Practices

### Information Gathering Process

**Steps:**
1. Read relevant files
2. Check git status/history
3. Inspect package.json
4. Review configuration
5. Understand current state
6. Then make changes

**Example:**
```bash
# 1. Understand project structure
ls -la
cat package.json

# 2. Check current state
git status
git diff

# 3. Read relevant files
cat src/auth/login.ts

# 4. Now ready to make changes
```

### Code Changes Process

**Steps:**
1. Analyze requirements
2. Plan approach
3. Make minimal changes
4. Test manually (guide user)
5. Iterate based on feedback

**Not:**
```markdown
❌ Write code → Run tests → Deploy → Debug
```

**But:**
```markdown
✅ Understand → Plan → Code → Guide testing → Iterate
```

### Temporary Files Usage

**When experimentation needed:**

```bash
# Create temp file
cat > /tmp/test.js << 'EOF'
console.log('Testing concept');
EOF

# Test concept
node /tmp/test.js

# If works, integrate into codebase
# Then clean up
rm /tmp/test.js
```

**Benefits:**
- Doesn't pollute codebase
- Easy to iterate
- No accidental commits

### Database Interactions

**Always use real database:**

```typescript
// ✅ Real database connection
const db = await connectToDatabase(process.env.DATABASE_URL);

// Query real data
const users = await db.users.find({ active: true });

// Not this:
// ❌ const users = MOCK_USERS;
```

**For development:**
```markdown
Options for safe testing:
1. Use staging database
2. Create development database
3. Use local database instance

Never use mock data in production code.
```

## Communication Patterns

### Tell, Don't Execute

**Bad:**
```markdown
"I'm starting the dev server now..."
[runs pnpm dev]
"Server started on port 3000"
```

**Good:**
```markdown
"Changes complete. To test:
1. Run: `pnpm dev`
2. Open: http://localhost:3000
3. Test the login flow

Let me know if you see any issues."
```

### Provide Clear Instructions

**Bad:**
```markdown
"Run the server and test it"
```

**Good:**
```markdown
"To test these changes:

1. Start dev server:
   ```bash
   pnpm dev
   ```

2. Navigate to http://localhost:3000/login

3. Test authentication:
   - Email: test@example.com
   - Password: password123

4. Verify:
   - Login succeeds
   - Redirects to /dashboard
   - Token saved in localStorage

Expected behavior:
- Should see welcome message
- Navigation should show logged-in state
- Token should be valid for 24 hours

Let me know what happens!"
```

## Decision Making

### When to Ask Permission

**Always ask before:**
- Installing packages
- Running builds
- Starting servers
- Modifying config files
- Making breaking changes
- Adding dependencies

**Example:**
```markdown
"This feature requires the `bcrypt` package for password hashing.

Should I:
1. Add bcrypt to package.json (recommended)
2. Use a different hashing library
3. Implement custom hashing (not recommended)

Which approach would you prefer?"
```

### When to Proceed Directly

**Can proceed without asking:**
- Reading files
- Checking status
- Writing code
- Updating documentation
- Fixing obvious bugs
- Following established patterns

## Summary: Code Focus

**Golden Rules:**

1. **Never Run Dev Servers**
   - User controls execution
   - Focus on code quality

2. **Read-Only Gathering**
   - Information gathering only
   - Ask before modifications

3. **No Test Files**
   - Manual testing preferred
   - Provide clear instructions

4. **Real Data Always**
   - Never use mocks
   - Connect to actual sources

5. **Proper Error Handling**
   - No silent fallbacks
   - Explicit error messages

6. **Keep Isolated**
   - Don't pollute repository
   - Use temporary files

7. **Guide, Don't Execute**
   - Tell user how to test
   - Provide clear steps

**Remember:** You write the code, user runs it. This keeps development smooth and avoids conflicts.
