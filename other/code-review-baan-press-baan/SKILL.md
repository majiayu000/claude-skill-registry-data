---
name: code-review
description: Pre-merge code review skill for diffs, staged changes, single files, or pull requests. Emphasises naming honesty (does the name match what the code does?), simplicity, YAGNI, SOLID, DRY, Next.js 16 idioms, and Baan rule compliance. Use when asked to "review code", "review this diff", "review PR", "review the changes", or equivalent requests in any language.
---

# Code Review

Review a change set against Baan's coding rules and general software
engineering principles. Produce a structured report grouped by
severity. This skill is **read-only** — it never edits code.

## Scope arguments

| Argument | Target |
|----------|--------|
| (none) | `git diff HEAD` + staged changes |
| `staged` | Staged changes only (`git diff --staged`) |
| `HEAD` / `HEAD~N` | Last commit, or last N commits |
| `<path>` | A single file or directory |
| `pr <N>` | A GitHub PR (`gh pr diff <N>`) |

## Before reviewing

1. Fetch the diff with `git diff`, `git diff --staged`, `git show`,
   or `gh pr diff` as appropriate.
2. For each touched file, Read the file around the hunk for context —
   do not judge a line in isolation.
3. Identify which `.claude/rules/*.md` apply to each path
   (frontend / api / db / test / etc.).

## Review categories

Work through the eight categories below. Emit a finding for every
issue, tagged with its severity (see "Severity discipline" at the
end).

---

### 1. Naming honesty — top priority

The name must match what the code actually does. Name–behaviour drift
is the hardest defect for future readers to notice.

Flag:

- **Name vs. side effect mismatch** — e.g. `getX()` that writes,
  `validateX()` that mutates, `isY()` that does I/O.
- **Catch-all names** — `handleData`, `process`, `manage`, `utils`,
  `helper`. A name that could mean anything signals that the author
  did not yet know what the function is for.
- **Generic signatures** — `(options: Record<string, unknown>) =>
  unknown`. A function that "accepts anything and returns anything"
  cannot be reasoned about.
- **Booleans that do not express meaning** — `flag`, `done`, `ok`,
  `result`. A boolean name must read as a yes/no question:
  `isAuthenticated`, `shouldRetry`.
- **Plural-singular mismatch** — `getUser()` that returns an array;
  `users` that holds one record.
- **Reserved vocabulary** — see `.claude/rules/naming.md`. Reject
  identifiers that collide with Tailwind / Next.js / React / shadcn
  reserved terms (`prose`, `layout`, `page`, `ref`, `container`,
  …).

Rewrite suggestion format:

```ts
// Before
function getUser(id: string) {
    cache.set(id, ...);     // write hidden behind "get"
    return fetchUser(id);
}

// After — split responsibilities, rename each
function fetchUser(id: string) { ... }
function cacheUser(user: User) { ... }
```

---

### 2. Simplicity / YAGNI

Reject code that solves problems the project does not have yet.

Flag:

- **"Does anything" functions** — options bags with flags that
  change behaviour into mutually incompatible modes. Split into
  separate functions.
- **Unused option parameters** — if only one call site uses the
  option, inline the option and remove it.
- **Speculative extension points** — plugin interfaces, strategy
  classes, feature flags with no second consumer.
- **Abstraction on two call sites** — three similar call sites is
  still not duplication worth extracting. Wait for four or a clear
  generalisation.
- **Half-finished code behind a flag** — reject "landed but disabled"
  features.
- **Unnecessary indirection** — a wrapper that only forwards
  arguments.

Reference: `.claude/rules/coding-principles.md` §Simplicity First,
§YAGNI.

---

### 3. SOLID (pragmatic)

Apply SOLID where it pays for itself; do not invoke it to justify
abstraction YAGNI would reject.

- **SRP** — multiple reasons to change in one function / module.
  Example: a function that validates input, writes the DB, and sends
  a webhook should be three functions.
- **OCP** — growing `if/else if` dispatches keyed on a type
  discriminator. Consider a map or polymorphic handler when the
  chain is long enough to matter.
- **DIP** — a high-level module that imports a concrete infrastructure
  module directly. Prefer passing the dependency in, especially
  across the `lib/` boundary.
- Resist **LSP / ISP** nitpicks on TypeScript interfaces unless a
  real substitutability bug exists.

---

### 4. DRY (rule-backed)

The same datum must live in one place.

Flag:

- **Duplicated constants** — cookie names, timeouts, URL prefixes,
  rate-limit values, regex patterns. Example: if `60_000` appears in
  two files with the same meaning, extract to a named constant.
- **Duplicated business rules** — the same validation expressed in
  two places diverges on the next change.
- **Duplicated AI prompts** — system / user prompts must live in
  exactly one module.
- **Duplicated i18n keys or CSS tokens** — one source of truth per
  rule dictionary.

Reference: `.claude/rules/coding-principles.md` §DRY.

---

### 5. Next.js 16 idioms

- **`'use client'`** — present on files using React hooks, event
  handlers, or browser APIs; absent elsewhere. Flag both over- and
  under-use.
- **Server / client boundary** — `async` components only in Server
  Components; `useEffect` only in Client Components.
- **`route.ts` signature** — `export async function GET(request:
  NextRequest)` (or `POST`, etc.). Admin API routes must use
  `withAuth` unless listed in `skipAuthPaths`.
- **`proxy.ts` response types** — `NextResponse.next` /
  `.rewrite` / `.redirect` must match intent. Rewrites preserve
  the URL; redirects change it.
- **`await request.json()` guards** — wrap in try/catch or validate
  shape; malformed JSON throws.
- **Rendering strategy** — `export const dynamic` /
  `generateStaticParams` must match the intent declared in the PR
  description.
- **`next/image`** — Baan ships with `images.unoptimized: true`, so
  a plain `<img>` with explicit width/height is acceptable. Flag
  only if the author clearly intended optimisation.

---

### 6. Baan rule compliance

For every finding, cite the specific rule file. Common hits:

| Violation | Rule file |
|-----------|-----------|
| Empty `catch {}` | `error-handling.md` §1 |
| Missing `console` prefix (`[ModuleName]`) | `error-handling.md` §2 |
| Admin API without `withAuth` | `security.md` §API Security |
| Direct `fs` outside whitelist | `settings-storage.md` |
| Japanese code comment | `coding-principles.md` §Language |
| Framework-reserved identifier | `naming.md` |
| Hardcoded UI text (no `t()`) | `i18n.md` |
| `await` inside a loop | `api-performance.md` |
| `page.tsx` / `layout.tsx` fetching without `ssrFetch` | `ssr-safety.md` |
| Rewriting an existing pipeline instead of feeding into it | `loose-coupling.md` |
| Raw SQL interpolation | `database.md` / `security.md` |
| Real HTTP in a unit test | `test-running.md` / `test-external-calls.md` |
| `.env.local` written by test code | `test-isolation.md` |

---

### 7. Comments

- **Why, not what** — a comment must explain a non-obvious intent,
  constraint, or trap. Restating what the next line does is noise.
- **No changelog comments** — `// Fix X:`, `// Add Y for Z`,
  `// Now we also handle …`. These belong in commit messages.
- **FIXME / HACK / TODO** — each has a distinct meaning (see
  `code-markers.md`). Reject markers without explanation. Reject
  TODO when FIXME is the correct marker.
- **Stale comments** — flag comments that contradict the code they
  annotate.

Reference: `.claude/rules/code-comments.md`,
`.claude/rules/code-markers.md`.

---

### 8. Test hygiene

- Unit tests must not make real HTTP calls.
- Unit tests must not write to `.env.local`.
- Playwright tests use port 3001 and read credentials from
  `.test-output/test-config.json`.
- No parallel `vitest` runs.
- No rate-limit or load testing inside the unit suite.

Reference: `.claude/rules/test-running.md`,
`.claude/rules/test-isolation.md`,
`.claude/rules/test-external-calls.md`.

---

## Severity discipline

| Severity | Meaning |
|----------|---------|
| 🔴 **Blocker** | Must fix before merge: broken build, security hole, public API contract break, data loss path, or a naming mismatch that will mislead every future reader. |
| 🟡 **Suggest** | Quality improvement, non-blocking. Refactor opportunities, DRY violations, better names where the current name is not actively wrong. |
| 💡 **Nitpick** | Subjective or stylistic. Early returns, formatting preferences, minor comment wording. |
| ✅ **Good** | Explicit positive notes when a tricky decision was handled well. Worth calling out — reviewers tend to only report problems, which skews the signal. |

One finding = one severity. Do not hedge.

Promote to Blocker only when the issue genuinely prevents merge.
Everything else is Suggest or Nitpick.

---

## Output format

```
## Code Review Report

Scope: <staged / HEAD / file.ts / PR #N>
Files reviewed: N

### Summary
| Verdict | Count |
|---------|-------|
| 🔴 Blocker | N  — must fix before merge |
| 🟡 Suggest | N  — quality, non-blocking |
| 💡 Nitpick | N  — subjective / optional |
| ✅ Good    | N  — positive notes |

### 🔴 Blockers

**[Short headline]** `path/to/file.ts:LINE`

Issue: one-paragraph description of what is wrong and why it blocks merge.

Fix:
\`\`\`ts
// rewrite example here
\`\`\`

Rule: `.claude/rules/<file>.md` §<section> (if applicable)

---

### 🟡 Suggestions

(same shape, cite file+line, show a rewrite where helpful)

### 💡 Nitpicks

(same shape, briefer)

### ✅ Strengths

- `path/to/file.ts:LINE` — what was done well and why it matters.

### Verdict

🟢 APPROVE / 🟡 APPROVE WITH SUGGESTIONS / 🔴 CHANGES REQUIRED

One-line rationale.
```

---

## Ground rules

- **Read-only.** Never edit code as part of a review. Report and
  wait for the user's direction.
- **Cite file and line on every finding.** No floating abstract
  criticism.
- **Prefer rewrite examples over prose.** A one-block "before /
  after" beats a paragraph of explanation.
- **One severity per finding.** No "Blocker or maybe Suggest".
- **Reference Baan rules explicitly** when a finding maps to one.
  `.claude/rules/<file>.md` path + section.
- **Verify before flagging.** If a pattern looks suspicious, Read
  the file to confirm the context — false positives erode trust.
- **Respect YAGNI vs. SOLID tension.** When proposing an
  abstraction, cite at least three current call sites or a concrete
  upcoming consumer. Otherwise demote the suggestion to a Nitpick or
  drop it.
- **Do not re-run `security-scan` work.** Vulnerability audits live
  in that skill; code review touches security only when the diff
  introduces a new risk.
