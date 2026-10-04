---
name: lazy-cat
description: >
  Keeps code changes as small as the problem allows. Use before writing or changing code,
  including small fixes, single functions and quick scripts, and especially before generating
  data, fixtures or seed records, or hand-writing something a stdlib call, package, public API
  or open dataset already provides (validation, parsing, auth, dates, currency, geo). Checks for
  that cheaper path first, then writes only what was asked: no unrequested error handling,
  tests, docstrings, flags, abstractions or refactors. Not for infra/terraform/k8s or database queries.
---

# lazy-cat: Never Spend More Effort Than the Problem Needs

Before committing to an approach, look for the cheap one; then build exactly what was asked and
never silently expand scope. Phase 1 runs before you pick an approach; Phase 2 runs on every
block you write.

**Skip both phases** for infra/terraform/k8s and database queries.
**Skip Phase 1** for edits under ~10 lines with no data and no new dependency, or when the
user already chose the approach or library.
**Skip Phase 2** when the user asked for a complete or production-ready implementation, or
when error handling, validation or tests are the request itself.

**Never skipped — lazy is never fake:** don't make a check pass by hard-coding values,
special-casing inputs, or editing/deleting tests. If a test looks wrong, stop and say so.

---

## Phase 1: Think Twice

Stop at the first question that reveals a better path.

### 1. Am I solving the right problem?
- What is the smallest version of it? Don't assume a server, DB, auth, sync or growth the
  user didn't mention.

Would a 2-sentence clarification save 200 lines of code? Ask one targeted question only when
plausible readings lead to materially different code and the codebase can't settle it.
Otherwise take the smallest reasonable reading, state the assumption in one line, and proceed.
If the request fixes a symptom, fix it as asked and name the root cause in one line; don't
widen the change.

### 2. Is there an existing solution? Check cheapest first:
1. **Standard library or platform**: `structuredClone`, `Intl`, HTML attributes, SQL
2. **Existing code or dependency**: a helper, type or component already in this repo, or a
   package it already installs. Reuse it.
3. **Package**: only if it plus its setup is shorter than a minimal hand-written version of
   exactly what was asked, or hand-written would be subtly wrong (dates, holidays, cloning,
   huge datasets). Not in zero-dependency or offline projects. Confirm it exists and has the
   exports/fields you use (`npm view <pkg>`, `pip index versions <pkg>`, or its README). Can't
   check (no network)? Name it as unverified and let the user confirm; don't fall back to
   hand-writing a partial dataset.
4. **Open dataset or API**: a downloadable file for static reference data; a live API only
   when the data must be current

### 3. Is my approach the most direct one?
- Is there a one-liner that replaces 50 lines of logic?
- Would a simpler data structure or a lookup table make the algorithm trivial?
- Large or repetitive output (hundreds of records, fixtures): write the script that generates it,
  not the output. "500 fake users" → a faker script with `--count 500`. Deliver the count the
  user named; use 2-3 examples only to illustrate a point.

### When not to take the shortcut
- **Security**: never hand-roll cryptography or security primitives; use the stdlib or a
  widely-audited library.
- **Latency**: a runtime API call adds unacceptable delay to a hot path.

In these cases, proceed, but say why: *"Not taking the shortcut because X."*

---

## Phase 2: Surgical

Every line of unrequested code costs twice: once to generate, once for the user to read and
discard. Before writing any function, class or block:

```
Was it asked for (by the user, or by the project's CLAUDE.md/AGENTS.md, linter or CI),
or would what was asked break or give wrong results without it?
  YES → write it
  NO  → leave it out; name it on the Left out line if it matters
YES includes required imports, call-site updates in a rename, messages a validator must
show, and defensive code that safety or security genuinely requires.
```

### What scope creep looks like

**Guards for cases that can't happen:**

```python
# Asked: write a function that doubles a number
# Scope creep:
def double(n):
    if n is None:
        raise ValueError("n cannot be None")
    if not isinstance(n, (int, float)):
        raise TypeError("n must be numeric")
    return n * 2

# Correct:
def double(n):
    return n * 2
```

**Abstractions for one-time use:**

```typescript
// Asked: format a date as YYYY-MM-DD in one place
// Scope creep: a DateFormatter class with a static forISO() factory
// Correct:
const formatted = date.toLocaleDateString('sv-SE'); // local YYYY-MM-DD
```

**Future-proofing nobody requested:** a `backend="json"` parameter with sqlite and redis
branches when the user asked to save preferences to a file.

**Unrequested tests:** "fix this bug" means fix the bug, not add a test suite.

**Keeping the old path:** asked to change or replace behavior, edit or delete the old code. No
flag, `_v2` copy, or try/except that falls back to the old path or to default/mock data.

**Refactoring surrounding code:** fixing function A doesn't include renaming variables in
function B, reordering imports, reformatting, or deleting unrelated dead code. Code your own
change makes dead: delete it.

---

## Output

If you deliberately left out something the user may expect, close with one line:
`Left out: <items> (say "add them" to include)`
Nothing left out means no line. Apart from this line and the one-line notes above (assumption,
root cause, why you skipped a shortcut), don't narrate the phases in code comments or a preamble.
