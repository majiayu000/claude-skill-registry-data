---
name: debugging-methodology
description: Scientific debugging methodology including hypothesis-driven debugging, bug reproduction, binary search debugging, stack trace analysis, logging strategies, and root cause analysis. Use when debugging errors, analyzing stack traces, investigating bugs, or troubleshooting performance issues.
---

# Debugging Methodology

This skill provides comprehensive guidance for systematically debugging issues using scientific methods and proven techniques.

## Scientific Debugging Method

### The Scientific Approach

**1. Observe**: Gather information about the bug
**2. Hypothesize**: Form theories about the cause
**3. Test**: Design experiments to test hypotheses
**4. Analyze**: Evaluate results
**5. Conclude**: Fix the bug or refine hypothesis

### Example: Debugging a Login Issue

```typescript
// Bug: Users cannot log in

// 1. OBSERVE
// - Error message: "Invalid credentials"
// - Happens for all users
// - Started after last deployment
// - Logs show: "bcrypt compare failed"

// 2. HYPOTHESIZE
// Hypothesis 1: Password comparison logic is broken
// Hypothesis 2: Database passwords corrupted
// Hypothesis 3: Bcrypt library updated with breaking change

// 3. TEST
// Test 1: Check if bcrypt library version changed
const packageLock = await fs.readFile('package-lock.json');
// Result: bcrypt upgraded from 5.0.0 to 6.0.0

// Test 2: Check bcrypt changelog
// Result: v6.0.0 changed default salt rounds

// Test 3: Verify password hashing
const testPassword = 'password123';
const oldHash = '$2b$10$...'; // From database
const newHash = await bcrypt.hash(testPassword, 10);
console.log(await bcrypt.compare(testPassword, oldHash)); // false
console.log(await bcrypt.compare(testPassword, newHash)); // true

// 4. ANALYZE
// Old hashes use $2b$ format, new version uses $2a$ format
// Incompatible hash formats

// 5. CONCLUDE
// Rollback bcrypt to 5.x or migrate all password hashes
```

## Reproducing Bugs Consistently

### Creating Minimal Reproduction

```typescript
// Original bug report: "App crashes when clicking submit"

// Step 1: Remove unrelated code
// ❌ BAD - Too much noise
function handleSubmit() {
  validateForm();
  checkPermissions();
  logAnalytics();
  sendToServer();
  updateUI();
  showNotification();
  // Which one causes the crash?
}

// ✅ GOOD - Minimal reproduction
function handleSubmit() {
  // Removed: validateForm, checkPermissions, logAnalytics, updateUI, showNotification
  // Bug still occurs with just:
  sendToServer();
  // Root cause: sendToServer crashes with undefined data
}
```

### Reproducing Race Conditions

```typescript
// Bug: Intermittent "Cannot read property of undefined"

// Make race condition reproducible with delays
async function fetchUserData() {
  const user = await fetchUser();
  // Add artificial delay to make race condition consistent
  await new Promise(resolve => setTimeout(resolve, 100));
  return user.profile; // Sometimes undefined
}

// Once reproducible, investigate:
// - Are multiple requests racing?
// - Is data being cleared too early?
// - Are promises resolving out of order?
```

### Creating Test Cases

```typescript
// Once bug is reproducible, create failing test
describe('Login', () => {
  test('should authenticate user with valid credentials', async () => {
    const user = await db.user.create({
      email: 'test@example.com',
      password: await bcrypt.hash('password123', 10),
    });

    const result = await login('test@example.com', 'password123');

    expect(result.success).toBe(true);
    expect(result.user.email).toBe('test@example.com');
  });
});
```

## Binary Search Debugging

### Finding the Breaking Commit

```bash
# Use git bisect to find the commit that introduced the bug

# Start bisect
git bisect start

# Mark current commit as bad (has the bug)
git bisect bad

# Mark a known good commit (before bug appeared)
git bisect good v1.2.0

# Git will checkout a commit in the middle
# Test if bug exists, then mark:
git bisect bad   # Bug exists in this commit
# or
git bisect good  # Bug doesn't exist in this commit

# Repeat until git identifies the breaking commit
# Git will output: "abc123 is the first bad commit"

# End bisect session
git bisect reset
```

### Automated Bisect

```bash
# Create test script that exits 0 (pass) or 1 (fail)
# test.sh
#!/bin/bash
npm test 2>&1 | grep -q "Login test failed"
if [ $? -eq 0 ]; then
  exit 1  # Bug found
else
  exit 0  # Bug not found
fi

# Run automated bisect
git bisect start HEAD v1.2.0
git bisect run ./test.sh

# Git will automatically find the breaking commit
```

### Binary Search in Code

```typescript
// Bug: Function returns wrong result for large arrays

function processArray(arr: number[]): number {
  // 100 lines of code
  // Which line causes the bug?
}

// Binary search approach:
// 1. Comment out second half
function processArray(arr: number[]): number {
  // Lines 1-50
  // Lines 51-100 (commented out)
}
// If bug disappears: Bug is in lines 51-100
// If bug persists: Bug is in lines 1-50

// 2. Repeat on the problematic half
// Continue until you isolate the buggy line
```

## Stack Trace Analysis

### Reading Stack Traces

```
Error: Cannot read property 'name' of undefined
    at getUserName (/app/src/user.ts:42:20)
    at formatUserProfile (/app/src/profile.ts:15:25)
    at handleRequest (/app/src/api.ts:89:30)
    at Layer.handle [as handle_request] (/app/node_modules/express/lib/router/layer.js:95:5)
```

**Analysis**:
1. **Error type**: TypeError - trying to access property on undefined
2. **Error message**: "Cannot read property 'name' of undefined"
3. **Origin**: `getUserName` function at line 42
4. **Call chain**: api.ts → profile.ts → user.ts
5. **Root cause location**: user.ts:42

### Investigating the Stack Trace

```typescript
// user.ts:42
function getUserName(userId: string): string {
  const user = cache.get(userId);
  return user.name; // ← Line 42: user is undefined
}

// Why is user undefined?
// 1. Check cache.get implementation
// 2. Check if userId is valid
// 3. Check if user exists in cache

// Add defensive check:
function getUserName(userId: string): string {
  const user = cache.get(userId);
  if (!user) {
    throw new Error(`User not found in cache: ${userId}`);
  }
  return user.name;
}
```

### Source Maps for Production

```javascript
// Enable source maps in production
// webpack.config.js
module.exports = {
  devtool: 'source-map',
  // This generates .map files for production debugging
};

// View original TypeScript code in production errors
// Instead of:
//   at r (/app/bundle.js:1:23456)
// You see:
//   at getUserName (/app/src/user.ts:42:20)
```

## Logging Strategies

### Strategic Log Placement

```typescript
// ✅ GOOD - Log at key decision points
async function processOrder(order: Order) {
  logger.info('Processing order', { orderId: order.id, items: order.items.length });

  try {
    // Log before critical operations
    logger.debug('Validating order', { orderId: order.id });
    await validateOrder(order);

    logger.debug('Processing payment', { orderId: order.id, amount: order.total });
    const payment = await processPayment(order);

    logger.info('Order processed successfully', {
      orderId: order.id,
      paymentId: payment.id,
      duration: Date.now() - startTime,
    });

    return payment;
  } catch (error) {
    // Log errors with context
    logger.error('Order processing failed', {
      orderId: order.id,
      error: error.message,
      stack: error.stack,
    });
    throw error;
  }
}
```

### Structured Logging

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'order-service',
    version: process.env.APP_VERSION,
  },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Output:
// {
//   "timestamp": "2025-10-16T10:30:00.000Z",
//   "level": "error",
//   "message": "Order processing failed",
//   "orderId": "order_123",
//   "error": "Payment declined",
//   "service": "order-service",
//   "version": "1.2.3"
// }
```

### Log Levels

```typescript
// Use appropriate log levels
logger.debug('Detailed debug information');  // Development only
logger.info('Normal operation');              // Informational
logger.warn('Warning but not an error');      // Potential issues
logger.error('Error occurred');               // Errors that need attention
logger.fatal('Critical failure');             // System-wide failures

// Set log level by environment
const logLevel = {
  development: 'debug',
  staging: 'info',
  production: 'warn',
}[process.env.NODE_ENV];
```

## Debugging Tools

### Using Debuggers

```typescript
// Set breakpoints in VS Code
function calculateTotal(items: Item[]): number {
  let total = 0;
  for (const item of items) {
    debugger; // Execution pauses here
    total += item.price * item.quantity;
  }
  return total;
}

// Or use VS Code launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Tests",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Node.js Built-in Debugger

```bash
# Start Node with inspector
node --inspect index.js

# Open Chrome DevTools
# Navigate to: chrome://inspect
# Click "inspect" on your Node.js process

# Or use Node's built-in debugger
node inspect index.js
> cont  # Continue
> next  # Step over
> step  # Step into
> out   # Step out
> repl  # Enter REPL to inspect variables
```

### Memory Profiling

```typescript
// Detect memory leaks
import v8 from 'v8';
import fs from 'fs';

// Take heap snapshot
function takeHeapSnapshot(filename: string) {
  const snapshot = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${snapshot}`);
}

// Compare snapshots to find leaks
takeHeapSnapshot('before.heapsnapshot');
// ... run code that might leak
takeHeapSnapshot('after.heapsnapshot');

// Analyze in Chrome DevTools:
// 1. Open DevTools → Memory tab
// 2. Load snapshot
// 3. Compare snapshots
// 4. Look for objects that grew significantly
```

## Performance Profiling

### CPU Profiling

```typescript
// Profile function execution time
console.time('processLargeArray');
processLargeArray(data);
console.timeEnd('processLargeArray');
// Output: processLargeArray: 1234.567ms

// More detailed profiling
import { performance } from 'perf_hooks';

const start = performance.now();
processLargeArray(data);
const end = performance.now();
console.log(`Execution time: ${end - start}ms`);
```

### Node.js Profiler

```bash
# Generate CPU profile
node --prof index.js

# Process profile data
node --prof-process isolate-0x*.log > profile.txt

# Analyze profile.txt to find slow functions
```

### Chrome DevTools Performance

```typescript
// Add performance marks
performance.mark('start-data-processing');
processData(data);
performance.mark('end-data-processing');

performance.measure(
  'data-processing',
  'start-data-processing',
  'end-data-processing'
);

const measure = performance.getEntriesByName('data-processing')[0];
console.log(`Data processing took ${measure.duration}ms`);
```

## Network Debugging

### HTTP Request Logging

```typescript
import axios from 'axios';

// Add request/response interceptors
axios.interceptors.request.use(
  (config) => {
    console.log('Request:', {
      method: config.method,
      url: config.url,
      headers: config.headers,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    console.log('Response:', {
      status: response.status,
      headers: response.headers,
      data: response.data,
    });
    return response;
  },
  (error) => {
    console.error('Response error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    });
    return Promise.reject(error);
  }
);
```

### Debugging CORS Issues

```typescript
// Enable detailed CORS logging
import cors from 'cors';

const corsOptions = {
  origin: (origin, callback) => {
    console.log('CORS request from origin:', origin);

    const allowedOrigins = ['https://app.example.com'];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      console.log('CORS blocked:', origin);
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
};

app.use(cors(corsOptions));
```

## Race Condition Detection

### Using Promises Correctly

```typescript
// ❌ BAD - Race condition
let userData = null;

async function loadUser() {
  userData = await fetchUser(); // Takes 100ms
}

async function displayUser() {
  console.log(userData.name); // May be null if loadUser not finished
}

loadUser();
displayUser(); // Race condition!

// ✅ GOOD - Wait for promise
async function main() {
  await loadUser();
  await displayUser(); // userData guaranteed to be loaded
}
```

### Detecting Concurrent Modifications

```typescript
// Detect race conditions with version numbers
interface Document {
  id: string;
  content: string;
  version: number;
}

async function updateDocument(doc: Document) {
  // Read current version
  const current = await db.document.findUnique({
    where: { id: doc.id },
  });

  // Check if version matches
  if (current.version !== doc.version) {
    throw new Error('Document was modified by another user');
  }

  // Update with incremented version
  await db.document.update({
    where: { id: doc.id, version: doc.version },
    data: {
      content: doc.content,
      version: doc.version + 1,
    },
  });
}
```

## Common Bug Patterns

### Off-by-One Errors

```typescript
// ❌ BAD - Off by one
const arr = [1, 2, 3, 4, 5];
for (let i = 0; i <= arr.length; i++) {
  console.log(arr[i]); // Last iteration: undefined
}

// ✅ GOOD
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);
}
```

### Null/Undefined Issues

```typescript
// ❌ BAD - No null check
function getUserName(user: User): string {
  return user.profile.name; // Crashes if user or profile is null
}

// ✅ GOOD - Defensive checks
function getUserName(user: User | null): string {
  if (!user) {
    return 'Unknown';
  }
  if (!user.profile) {
    return 'No profile';
  }
  return user.profile.name;
}

// ✅ BETTER - Optional chaining
function getUserName(user: User | null): string {
  return user?.profile?.name ?? 'Unknown';
}
```

### Async/Await Pitfalls

```typescript
// ❌ BAD - Forgot await
async function getUser(id: string) {
  const user = fetchUser(id); // Missing await!
  return user.name; // user is a Promise, not the actual user
}

// ✅ GOOD
async function getUser(id: string) {
  const user = await fetchUser(id);
  return user.name;
}

// ❌ BAD - Sequential when parallel is possible
async function loadData() {
  const users = await fetchUsers();    // 1 second
  const posts = await fetchPosts();    // 1 second
  const comments = await fetchComments(); // 1 second
  // Total: 3 seconds
}

// ✅ GOOD - Parallel execution
async function loadData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
  ]);
  // Total: 1 second
}
```

## Root Cause Analysis (5 Whys)

### The 5 Whys Technique

```
Problem: Application crashed in production

Why? Memory leak caused out-of-memory error
  Why? Array of user sessions kept growing
    Why? Sessions weren't being cleaned up
      Why? Cleanup function wasn't being called
        Why? Event listener for cleanup was never registered
          Root Cause: Missing initialization code in new deployment script
```

### RCA Template

```markdown
## Root Cause Analysis

**Date**: 2025-10-16
**Incident**: API downtime (30 minutes)

### Timeline
- 10:00 - Deployment started
- 10:15 - First error reports
- 10:20 - Incident declared
- 10:25 - Rollback initiated
- 10:30 - Service restored

### Impact
- 500 users affected
- 10% of API requests failed
- $5,000 estimated revenue loss

### Root Cause
Database connection pool exhausted due to missing connection cleanup in new feature code.

### 5 Whys
1. Why did the API fail? → Database connections exhausted
2. Why were connections exhausted? → Connections not returned to pool
3. Why weren't connections returned? → Missing finally block in new code
4. Why was the finally block missing? → Code review missed it
5. Why did code review miss it? → No automated check for connection cleanup

### Immediate Actions Taken
- Rolled back deployment
- Manually closed leaked connections
- Service restored

### Preventive Measures
1. Add linter rule to detect missing finally blocks
2. Add integration test for connection cleanup
3. Update code review checklist
4. Add monitoring for connection pool usage

### Lessons Learned
- Need better monitoring of connection pool metrics
- Database connection patterns should be abstracted
- Code review process needs improvement
```

## Debugging Checklist

**Before Debugging**:
- [ ] Can you reproduce the bug consistently?
- [ ] Do you have a minimal reproduction case?
- [ ] Have you checked recent changes (git log)?
- [ ] Have you read error messages carefully?
- [ ] Have you checked logs?

**During Debugging**:
- [ ] Are you using scientific method (hypothesis-driven)?
- [ ] Have you added strategic logging?
- [ ] Are you using a debugger effectively?
- [ ] Have you isolated the problem area?
- [ ] Have you considered race conditions?

**After Fixing**:
- [ ] Does the fix address root cause (not just symptoms)?
- [ ] Have you added tests to prevent regression?
- [ ] Have you documented the fix?
- [ ] Have you conducted root cause analysis?
- [ ] Have you shared learnings with team?

## When to Use This Skill

Use this skill when:
- Debugging production issues
- Investigating bug reports
- Analyzing error logs
- Troubleshooting performance problems
- Finding memory leaks
- Resolving race conditions
- Conducting post-mortems
- Training team on debugging
- Improving debugging processes
- Setting up debugging tools

---

**Remember**: Debugging is detective work. Be systematic, stay curious, and always document what you learn. The bug you fix today will teach you how to prevent similar bugs tomorrow.
