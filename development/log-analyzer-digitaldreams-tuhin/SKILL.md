---
name: log-analyzer
description: >
  Laravel log file analyzer for expert-level bug diagnosis. Use this skill whenever the user mentions 'laravel.log', 'check the log', 'analyze logs', 'log file', 'there's an error in the log', or asks to diagnose, investigate, or fix a bug from a Laravel log file. Triggers on any mention of Laravel errors, exceptions, undefined variable errors, or stack traces from a Laravel application. This skill reads the log file, isolates actionable errors (ignoring INFO/DEBUG/routine logs), identifies the root cause by tracing into App-namespaced source files, inspects database table structure when model-related, and recommends a minimal, pattern-consistent fix. Always use this skill before attempting to diagnose any Laravel bug from a log.
---

# Laravel Log Analyzer Skill

You are an expert Laravel/PHP developer. Your job is to read a `laravel.log` file, isolate real errors, trace them to root cause through the application source, and produce a precise fix — following existing code patterns, never refactoring unnecessarily.

---

## Phase 1 — Read the Log File

When given a log file path (e.g. `storage/logs/laravel.log`), read it with:

```bash
cat /path/to/laravel.log
```

Or if the file is large, read only recent entries:
```bash
tail -n 300 /path/to/laravel.log
```

**Filter ruthlessly.** Only process entries at these log levels:
- `ERROR`
- `CRITICAL`
- `ALERT`
- `EMERGENCY`
- `WARNING` — only if it contains an exception class, stack trace, or undefined variable

**Completely ignore:**
- `INFO`, `DEBUG`, `NOTICE` level entries
- Routine Laravel messages: "Application booted", "Running scheduled task", "Queue worker", "Cache hit/miss", session activity, "Deprecation notice" (unless causing a crash)

Process **one log entry at a time**, starting from the most recent. Do not batch multiple errors together.

---

## Phase 2 — Classify the Error

For each qualifying error, determine its type:

### Type A — Undefined Variable / Property
```
ErrorException: Undefined variable: $someVar
ErrorException: Undefined array key "someKey"
ErrorException: Attempt to read property "x" on null
```

### Type B — Code Execution Exception
```
Illuminate\Database\QueryException
TypeError: Argument 1 passed to ...
BadMethodCallException
InvalidArgumentException
Error: Call to a member function on null
Symfony\Component\HttpKernel\Exception\*
```

### Type C — Model / Database Error
```
SQLSTATE[...] errors
Integrity constraint violation
Column not found
Field 'x' doesn't have a default value
```

**Skip and note (do not investigate):**
- `TokenMismatchException` — CSRF, not a code bug
- `AuthenticationException` — auth flow, not a code bug
- `NotFoundHttpException` on static assets (favicon, etc.)

---

## Phase 3 — Extract the Stack Trace

From the log entry, extract the full stack trace. Identify lines that reference files under the `App\` namespace (path typically starts with `app/`).

**Read these files. Ignore everything else:**
```
✅ app/Http/Controllers/...
✅ app/Services/...
✅ app/Repositories/...
✅ app/Models/...
✅ app/Jobs/...
✅ app/Listeners/...
✅ app/Traits/...
✅ app/Http/Requests/...

❌ vendor/...         — NEVER read
❌ bootstrap/...      — skip
❌ public/index.php   — skip
```

Read the **primary error file first** (the file and line number where the exception was thrown). Then read files that **called** that file (the callers in the stack), working upward through `App\` files only.

```bash
# Example: read the file at the specific area of interest
sed -n '45,90p' app/Services/OrderService.php
```

Use `sed -n 'START,ENDp'` to read relevant sections rather than entire files where possible.

---

## Phase 4 — Contextual File Reading

After reading the error-origin files, if the root cause is still unclear, read the **files that interact with the erroring code**:

1. If the error is in a Controller → read the Service/Repository it calls
2. If the error is in a Service → read the Model it operates on
3. If the error is in a Model or involves a relationship → read the related Model(s)
4. If data is being passed from a Request → read the FormRequest class

Always read these in order: **caller → callee → model → migration/schema**.

---

## Phase 5 — Database Inspection (Model/Query Errors)

When the error involves saving, updating, querying, or relating Eloquent models, **always run a schema inspection query**.

```bash
php artisan tinker --execute="DB::select('DESCRIBE table_name');" 2>/dev/null
```

Or directly via MySQL if artisan isn't available:
```bash
mysql -u root -e "DESCRIBE database_name.table_name;"
```

Extract from the result:
- Column names and data types
- Nullable vs NOT NULL columns
- Default values
- Foreign key columns

Cross-check this against:
- `$fillable` in the Model
- `$casts` in the Model
- Any `$hidden` or `$guarded` that might block mass assignment
- The data being passed at the point of save/create/update

---

## Phase 6 — Diagnosis & Fix

Now synthesize everything into a diagnosis. Structure your response as:

### 🔴 Error
> Paste the single-line exception message from the log

### 📍 Location
> `app/Path/To/File.php` line N — what the code is doing there

### 🔎 Root Cause
> Explain in plain terms *why* this error occurs. Be specific: reference variable names, column names, method names from the actual code you read.

### ✅ Fix
Show the minimal code change needed. **Rules:**
- Follow the exact coding style already in that file (same variable naming, same indentation, same use of `$this->model` vs direct Model calls, same error handling pattern)
- Do not rename variables, extract methods, or restructure unless the bug literally cannot be fixed without doing so
- Show a before/after diff or clearly mark what line(s) to change
- If the fix touches a Blade view, match the existing Blade patterns in that file

### ⚠️ Do Not
> Briefly note anything that should NOT be changed (to prevent over-engineering)

---

## Worked Examples

### Example 1 — Undefined Variable in Blade (Type A)

**Log entry:**
```
[ERROR] ErrorException: Undefined variable $invoice in /app/resources/views/invoices/show.blade.php on line 12
#0 app/Http/Controllers/InvoiceController.php:34
```

**Process:**
1. Read `app/Http/Controllers/InvoiceController.php` around line 34
2. Notice the controller returns `view('invoices.show', ['invoices' => $invoice])` — typo, wrong key name
3. Read `resources/views/invoices/show.blade.php` — confirms it uses `$invoice`

**Fix:** Change `'invoices'` → `'invoice'` in the controller's return statement. Nothing else.

---

### Example 2 — Model Save Failure (Type C)

**Log entry:**
```
[ERROR] Illuminate\Database\QueryException: SQLSTATE[HY000]: General error: 1364 Field 'status' doesn't have a default value
  at app/Services/OrderService.php:58
  at app/Http/Controllers/OrderController.php:29
```

**Process:**
1. Read `app/Services/OrderService.php` lines ~50-70 — finds `Order::create($data)` where `$data` comes from the request
2. Read `app/Models/Order.php` — checks `$fillable`, sees `status` is listed
3. Run: `php artisan tinker --execute="DB::select('DESCRIBE orders');"`
4. Result shows `status` column is `NOT NULL` with no default
5. Read `app/Http/Controllers/OrderController.php` lines ~25-35 — confirms `status` is never set before calling the service

**Fix:** In `OrderController.php` (or `OrderService.php`, whichever is the pattern for setting defaults in this codebase), add `$data['status'] = $data['status'] ?? 'pending';` before the create call. Match whether the existing code sets defaults in the controller, service, or model `$attributes` property — don't invent a new pattern.

---

### Example 3 — Call to Member Function on Null (Type B)

**Log entry:**
```
[ERROR] Error: Call to a member function format() on null
  at app/Services/ReportService.php:91
```

**Process:**
1. Read `app/Services/ReportService.php` around line 91 — sees `$order->completed_at->format('Y-m-d')`
2. Run: `php artisan tinker --execute="DB::select('DESCRIBE orders');"`
3. Confirms `completed_at` is nullable
4. Look at how similar nullable date fields are handled elsewhere in the same file or model

**Fix:** Change to `$order->completed_at?->format('Y-m-d')` (null-safe operator) or `optional($order->completed_at)->format('Y-m-d')` — whichever pattern is already used in that file for similar null-safe access.

---

## Phase 7 — Submit the Fix

After diagnosis and fix are determined, **always check the environment before touching any file or branch.**

### Step 1 — Detect Environment

```bash
grep -E "^APP_ENV=" .env 2>/dev/null | cut -d= -f2 | tr -d '"'\''[:space:]'
```

If `.env` is not readable or `APP_ENV` is missing, **treat it as production. Do not assume local.**

| `APP_ENV` value | Action |
|---|---|
| `local` | → Option 1: Git branch + commit |
| `development` / `dev` | → Option 1: Git branch + commit |
| `staging` | → Option 2: Bug report `.md` file |
| `production` / `prod` | → Option 2: Bug report `.md` file |
| missing / unreadable | → Option 2: Bug report `.md` file |

---

### Option 1 — Git Branch & Commit (local/dev only)

**Step 1: Get current branch name**
```bash
git branch --show-current
```

**Step 2: Create bug branch from it**

Derive the branch name from the error. Use the pattern `bug/short-description-of-bug` — lowercase, hyphenated, max 5 words, no special characters.

Examples:
- `bug/undefined-invoice-variable-controller`
- `bug/order-status-missing-default`
- `bug/completed-at-null-report-service`

```bash
git checkout -b bug/your-derived-name
```

**Step 3: Apply the fix**

Make only the exact code change identified in Phase 6. Nothing else.

**Step 4: Stage and commit**

Stage only the files that were changed to fix the bug:
```bash
git add app/Path/To/ChangedFile.php
```

Write a commit message that follows this format:
```
fix: <what was wrong> in <ClassName>

<One sentence explaining root cause>
<One sentence explaining what was changed>
```

Example:
```
fix: undefined $invoice variable in InvoiceController

Controller passed 'invoices' key but view expected 'invoice'.
Corrected the key name in the return statement on line 34.
```

```bash
git commit -m "fix: ..."
```

Do **not** push. Do **not** open a PR. Just commit locally and report the branch name to the user.

---

### Option 2 — Bug Report File (staging/production/unknown)

**Never apply code changes directly on staging or production.**

Instead, create a markdown file at the project root:

```
bug-reports/YYYY-MM-DD-short-bug-name.md
```

Use today's date and the same short name you would have used for the branch.

Example: `bug-reports/2025-01-15-order-status-missing-default.md`

**Template:**

```markdown
# Bug Report: [Short title]

**Date:** YYYY-MM-DD  
**Environment:** production  
**Log File:** storage/logs/laravel.log  
**Severity:** [Critical / High / Medium] — based on whether it breaks core functionality

---

## Error

\```
[Exact exception message from the log]
\```

## Location

`app/Path/To/File.php` — line N

## Root Cause

[Plain-English explanation of why this happens. Name the specific variables, columns, or methods involved.]

## Files Investigated

- `app/Path/To/ErrorOriginFile.php`
- `app/Path/To/CallerFile.php`
- `app/Models/RelevantModel.php`

## Required Fix

**File:** `app/Path/To/File.php`  
**Line:** N

Before:
\```php
[original code]
\```

After:
\```php
[fixed code]
\```

## Notes for Developer

[Any caveats: e.g. "Confirm `status` default with product team before hardcoding 'pending'", or "Check if other callers of this method also omit this field"]

## Do Not

[What should NOT be changed or refactored while applying this fix]
```

After creating the file, tell the user: the file location, the severity, and whether they should action it immediately or can schedule it.

---

## Important Constraints

- **Never read vendor files.** If the only stack frames are in `vendor/`, report the last `App\` file in the stack and the line that called into vendor.
- **One error at a time.** Finish diagnosing and fixing one before moving to the next.
- **No refactoring.** If the fix requires changing 1 line, change 1 line. Do not "clean up while you're in there."
- **Match the existing pattern.** If the project uses Repositories, don't suggest Service-layer changes. If it uses direct Model calls in controllers, don't suggest injecting a Repository.
- **Always confirm the table structure** before diagnosing any database/model error. Do not guess column nullability or defaults.
