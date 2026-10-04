---
name: claude-md-progressive-disclosurer
description: Optimize CLAUDE.md files via progressive disclosure when rules are duplicated or repeatedly ignored.
---

### Multiple-entry principle (important!)

The same Level 2 resource can have **multiple entry points**, serving different lookup paths:

| Entry point | Location | Trigger scenario | User mindset |
|------|------|----------|----------|
| Reference index | Beginning | Hitting an error/problem | "Something broke - which doc do I check?" |
| "Read before changing code" | Middle | About to change code | "I'm about to change X - what should I watch out for?" |
| Reference trigger index | End | Locating in a long conversation | "That doc we mentioned earlier - which one was it?" |

**This is not duplication, it's multiple entry points.** Just like a book has a table of contents (by chapter), an index (by keyword), and a quick-reference card (by task).

---

## Optimization workflow

### Step 1: Back up

```bash
cp CLAUDE.md CLAUDE.md.bak.$(date +%Y%m%d_%H%M%S)
```

### Step 2: Classify content

Classify each section:

| Question | Yes | No |
|------|----|-----|
| Used frequently? | Level 1 | ↓ |
| Severe consequences if violated? | Level 1 | ↓ |
| Has a code pattern that needs to be copied directly? | Level 1, keep the pattern | ↓ |
| Has a clear trigger condition? | Level 2 + trigger condition | ↓ |
| Historical/reference material? | Level 2 | Consider deleting |

### Step 3: Create Reference files

Naming: `docs/references/{topic}-sop.md`

**Iron rule: move verbatim, no compression allowed**

When moving content to Level 2, you must **preserve the original content in full**. Do not "tidy it up while you're at it" during the move.

```
✅ Correct: move 100 lines untouched to Level 2 (100 lines → Level 2 100 lines)
❌ Wrong: "trim" 100 lines down to 60 and move to Level 2 (100 lines → Level 2 60 lines, 40 lines gone)
```

**Why**: compression = deletion in disguise. Content you deem "unimportant" and cut may be the key clue for some future debug session. The goal of optimization is to **change the location of information** (Level 1 → Level 2), not to **change whether the information exists**.

**How**:
1. Precisely copy the passage to be moved from the original CLAUDE.md
2. Paste it verbatim into the Level 2 file
3. You may add structure within Level 2 (headings, separators), but **do not trim, rewrite, or merge** the original content
4. If there genuinely is redundancy (the same passage appears multiple times in the original), keep one complete copy in Level 2 and add a note explaining the deduplication

### Step 4: Update Level 1

1. **Add the "Information-recording principle" at the top** (after the project overview, before the Reference index)
2. **Add the Reference index** (right after the information-recording principle)
3. Replace detailed content with the trigger-condition format
4. Keep code patterns and error diagnostics
5. **Add the "Read before changing code" table** (indexed by "what you want to change")
6. **Place another copy of the trigger index table at the end**

### Step 5: Verify (only complete when all three pass)

#### 5a. Referenced-file existence

```bash
# Check that referenced files exist
grep -oh '`docs/references/[^`]*\.md`' CLAUDE.md | sed 's/`//g' | while read f; do
  test -f "$f" && echo "✓ $f" || echo "✗ MISSING: $f"
done
```

#### 5b. Content completeness (most critical)

For each section moved out of the original CLAUDE.md, check one by one:

1. **Restore the original file**: `git show HEAD:CLAUDE.md > /tmp/claude-md-original.md`
2. **Compare section by section**: for each `##` section in the original file, confirm its content exists in full in one of these places:
   - In the new CLAUDE.md (kept in Level 1)
   - In some Level 2 reference file (moved in full)

   **A helper script to quickly surface omissions**:

   ```bash
   # For each ## section heading in the original file, check whether it exists in the new file or a reference file
   grep '^## ' /tmp/claude-md-original.md | while read heading; do
     if grep -q "$heading" CLAUDE.md docs/references/*.md 2>/dev/null; then
       echo "✓ $heading"
     else
       echo "✗ NOT FOUND: $heading"
     fi
   done
   ```

   > ⚠️ This script **cannot replace manual section-by-section comparison** - it only checks whether section headings exist, not whether the content is complete. But it can quickly surface cases where **an entire section was omitted**, serving as a first screen before manual comparison.

3. **Flag every discrepancy**:
   - If a passage was shortened in the new file → **you must restore the trimmed parts**
   - If a passage exists in neither location → **you must restore it**
   - The only case where deletion is allowed: **the information already has an independent canonical source** (e.g. `docs/README.md` is already the canonical source for the doc index), and Level 1 has a clear pointer to it

**Do not use "intentional deletion" as a classification to mask information loss.** Every "intentional deletion" must state where the canonical source is. If you can't name one, it isn't "intentional deletion" - it's "omission".

#### 5c. Line-count audit prohibited

During verification, **do not count lines**. No `wc -l`. Do not compute "original X lines vs new Y lines". Those numbers distort your judgment.

The standard for verification is:
- Every piece of information has a home (Level 1, Level 2, or a canonical source)
- No information is lost
- Every Level 2 reference has a trigger condition

---

## Level 1 content classification

### 🔴 Absolutely must not move out

| Content type | Reason |
|---------|------|
| **Core commands** | Used frequently |
| **Iron rules / prohibitions** | Severe consequences if violated; must always be visible |
| **Code patterns** | The LLM needs to copy directly; avoid re-deriving |
| **Error diagnostics** | Complete symptom → cause → fix flow |
| **Directory map** | Helps the LLM locate files quickly |
| **Trigger index table** | Helps the LLM locate Level 2 in long conversations |

### 🟡 Keep a summary + trigger condition

| Content type | Level 1 | Level 2 |
|---------|---------|---------|
| SOP procedures | Trigger condition + key pitfalls | Full steps |
| Config examples | The 1-2 most common | Full config |
| API docs | Common method signatures | Full parameter descriptions |

### 🟢 Can be moved out entirely

| Content type | Reason |
|---------|------|
| Historical decision records | Accessed infrequently |
| Performance data | Reference material |
| Tech-debt list | Viewed on demand |
| Edge cases | Loaded only when there's a clear trigger condition |

---

## Reference formats (four)

### 1. Detailed format (important references in the body)

```markdown
**📖 When to read `docs/references/xxx-sop.md`**:
- [Specific error message, e.g. `ERR_DLOPEN_FAILED`]
- [Specific scenario, e.g. "when adding a new native module"]

> Contains: [keyword 1], [keyword 2], [code template].
```

### 2. Problem-trigger table (index at beginning/end)

```markdown
## Reference index (check here first when you hit a problem)

| Trigger scenario | Doc | Core content |
|----------|------|---------|
| `ERR_DLOPEN_FAILED` | `native-modules-sop.md` | ABI mechanism, lazy loading |
| `Cannot find module` after packaging | `vite-sop.md` | MODULES_TO_COPY |
```

### 3. Task-trigger table (read before changing code)

```markdown
## Read before changing code

| What you want to change | Read this first | Key pitfalls |
|-----------|---------|---------|
| Anything native-module related | `native-modules-sop.md` | Must lazy-load; electron-rebuild fails silently |
| Packaging config | `packaging-sop.md` | DMG contents must use the function form |
```

### 4. Inline format (short references)

```markdown
Full flow in `database-sop.md` (FTS5 escaping, health checks).
```

**Diversity principle**: don't use the same format for every reference.

---

## Four core principles

### Principle 1: Put the trigger index table at the beginning and end

**Reason**: LLM attention follows a U-shaped distribution - strong at the beginning and end, weak in the middle.

| Position | Purpose |
|------|------|
| **Beginning** | Establish global awareness at the start of the conversation: "which Level 2 resources are available" |
| **End** | Restate the reminder once the conversation has grown long: "which Level 2 should I read now" |

```markdown
<!-- Beginning of CLAUDE.md (after the project overview) -->
## Reference index

| Trigger scenario | Doc | Core content |
|---------|------|---------|
| ABI error | `native-modules-sop.md` | Lazy-loading pattern |
| Module missing after packaging | `vite-sop.md` | MODULES_TO_COPY |

... (body content) ...

<!-- End of CLAUDE.md (another copy) -->
## Reference trigger index

| Trigger scenario | Doc | Core content |
|---------|------|---------|
| ABI error | `native-modules-sop.md` | Lazy-loading pattern |
| Module missing after packaging | `vite-sop.md` | MODULES_TO_COPY |
```

### Principle 2: References must have a trigger condition

**Wrong**: `See native-modules-sop.md for details`

**Correct**:
```markdown
**📖 When to read `native-modules-sop.md`**:
- Hitting an `ERR_DLOPEN_FAILED` error
- Need to add a new native module

> Contains: ABI mechanism, lazy-loading pattern, manual fix commands
```

**Reason**: without a trigger condition, the LLM doesn't know when to go read it.

### Principle 3: Code patterns must stay in Level 1

**Wrong**: move the code example to Level 2, and have Level 1 only say "use the lazy-loading pattern".

**Correct**: Level 1 keeps the full copyable code:
```javascript
// ✅ Correct: lazy load, only load when needed
let _Database = null;
function getDatabase() {
  if (!_Database) {
    _Database = require("better-sqlite3");
  }
  return _Database;
}
```

**Reason**: the LLM needs to copy the code directly; once moved out, it has to re-derive it or read Level 2 every time.

---

## Information-volume check

### ✅ Correct information volume

| Check item | Passing standard |
|--------|---------|
| Everyday commands | No need to read Level 2 |
| Common errors | Has a complete diagnostic flow |
| Writing code | Has a copyable pattern |
| Specific problems | Knows which Level 2 to read |
| Trigger index | At the end of the doc, in table form |

### ❌ Signs of too little

- The LLM keeps asking the same question
- The LLM re-derives the code pattern every time
- The user has to keep reminding it of rules

### ❌ Signs of too much

- Large blocks of low-frequency detailed procedures in Level 1
- **Exactly identical content** in multiple places (note: multiple entry points pointing to the same resource ≠ duplication)
- Edge cases and common cases mixed together

---

## Project-level vs user-level

| Dimension | User-level | Project-level |
|------|--------|--------|
| Location | `~/.claude/CLAUDE.md` | `project/CLAUDE.md` |
| References | `~/.claude/references/` | `docs/references/` |
| Scope of information | Personal preferences, global rules | Project architecture, team conventions |

---

## Quick checklist

After optimization is done, **check every item** (do not skip):

### Information completeness (most important)
- [ ] **Every section of the original file has a home** - in the new Level 1, in Level 2, or with a clear canonical source
- [ ] **Level 2 file content is identical to the original** - not "trimmed" during the move
- [ ] **Nothing was silently deleted** - every deletion has user confirmation or a clear canonical source
- [ ] **At no stage did you count or mention line-count changes**

### Structural quality
- [ ] The "Information-recording principle" is at the top of the doc (prevents future bloat)
- [ ] The Reference index is at the top of the doc (entry point 1: check here when you hit a problem)
- [ ] The core command table is complete
- [ ] Iron rules / prohibitions have code examples
- [ ] Common errors have a complete diagnostic flow (symptom → cause → fix)
- [ ] Code patterns are directly copyable
- [ ] Directory map (feature → file)
- [ ] The "Read before changing code" table (entry point 2: indexed by "what you want to change")
- [ ] The Reference trigger index is at the end of the doc (entry point 3: restated after a long conversation)
- [ ] Every Level 2 reference has a trigger condition
- [ ] All referenced files exist
