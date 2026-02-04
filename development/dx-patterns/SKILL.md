---
name: dx-patterns
description: Design developer experiences that people love. Feedback loops, cognitive load, flow state, and ADHD-friendly patterns for tools and workflows.
triggers:
  - developer experience
  - dx patterns
  - developer productivity
  - adhd-friendly
  - cognitive load
  - workflow optimization
---

# Developer Experience (DX) Patterns

Build tools and systems that feel natural, reduce friction, and let developers reach flow state. Grounded in research and battle-tested in production.

## The DX Framework

Based on research by Greiler, Storey, and Noda, the **DX Framework** defines developer experience through three pillars:

### 1️⃣ Feedback Loops

**Definition:** How quickly developers know if something worked or failed.

**Good Feedback:**
- Tests run fast (< 5s for unit tests)
- Errors appear immediately (pre-commit hooks)
- Success is obvious (green checkmarks, clear output)
- Failures include actionable suggestions

**Bad Feedback:**
- Tests take 30s to run
- Errors appear only after CI fails
- Stack traces with no context
- "Something went wrong" with no solution

### 2️⃣ Cognitive Load

**Definition:** How much mental energy developers spend understanding your system.

**Reduce Cognitive Load:**
- Consistent patterns (same patterns everywhere)
- Clear naming (unambiguous function/variable names)
- Progressive disclosure (novice → expert paths)
- Visual hierarchy (important things stand out)
- Documentation that answers "why" not just "how"

**Increase Cognitive Load:**
- Hidden magic (implicit behavior)
- Inconsistent patterns (each tool different)
- Cryptic names (short abbreviations)
- Everything visible at once (no hierarchy)
- No documentation

### 3️⃣ Flow State

**Definition:** Developers' ability to maintain deep focus and productivity.

**Enable Flow:**
- Minimize context switching (related files nearby)
- Remove blockers (dependencies available)
- Clear next steps (obvious what to do)
- Intrinsic motivation (meaningful work)
- Mastery progression (skill growth visible)

**Block Flow:**
- Constant interruptions
- Broken dependencies
- Unclear requirements
- Busywork with no purpose
- No sense of progress

---

## DX Patterns in Practice

### Pattern 1: Progressive Disclosure

Show complexity gradually, not all at once.

#### ❌ Bad: Everything Visible

```
Usage: my-cli [options]

Options:
  --config FILE              Path to config file
  --verbose LEVEL            Verbosity level (0-3)
  --output FORMAT            Output format (md, json, html)
  --workers N                Number of worker threads
  --cache STRATEGY           Cache strategy (none, memory, disk)
  --socket-timeout MS        Socket timeout in ms
  --max-retries N            Maximum retries
  --backoff-multiplier N     Exponential backoff multiplier
  --log-level LEVEL          Logging level
  ... (20 more options)
```

**Result:** Overwhelming. Novice developers see too many options.

#### ✅ Good: Progressive Disclosure

```
Usage: my-cli [command] [options]

Commands:
  config       Show/edit configuration
  run          Execute the task
  help         Show help for a command

Basic options:
  --verbose    Show detailed output
  --help       Show this help

Examples:
  my-cli config              # Edit configuration
  my-cli run                 # Run with defaults
  my-cli run --verbose       # Run with details

Advanced:
  See 'my-cli help run' for all options
```

**Result:** Novice path is clear. Experts can discover advanced options.

### Pattern 2: Consistent Command Structure

Same patterns everywhere = lower cognitive load.

#### Structure: `command subcommand [args] [--flags]`

```bash
# File operations
git status
git add file.txt
git commit -m "message"
git push origin main

# CLI operations (same pattern!)
my-cli frontmatter get note.md
my-cli frontmatter set note.md key=value
my-cli frontmatter migrate note.md
my-cli frontmatter validate note.md
```

**Benefits:**
- Developers recognize the pattern (verb noun)
- Easy to guess next command
- Consistency reduces mental overhead

### Pattern 3: Clear Error Messages

Errors should include: what, why, how to fix.

#### ❌ Bad: Cryptic Error

```
Error: ENOENT
```

**Problem:** User has no idea what's wrong.

#### ✅ Good: Helpful Error

```
Error: Configuration file not found

Expected file: /Users/nathan/.config/my-tool/config.json

To create it, run:
  my-cli config --init

Or set the environment variable:
  export MY_TOOL_CONFIG=/path/to/config.json
```

**Result:** User knows exactly what to do.

### Pattern 4: Fast Feedback

Developers thrive on quick validation.

```bash
# ❌ Slow: User waits 30s after each command
$ my-cli build
  Building... (30 seconds)
  ✅ Done

# ✅ Fast: Instant feedback on changes
$ my-cli watch
  Watching for changes...
  ✅ Built (0.2s)
  ✅ Tests (0.8s)
  ✅ Linted (0.3s)
  Ready to go!
```

**Techniques:**
- Parallel execution (tests + lint simultaneously)
- Watch mode (rebuild on changes)
- Incremental builds (only changed files)
- Progress indicators (spinner, %)

---

## ADHD-Friendly Patterns

Cognitive load affects everyone, but patterns specifically help ADHD brains:

### 1. Minimal Context Switching

Keep related things together:
- Files for a feature in same directory
- Commands grouped by domain (git status, git add, git commit)
- Documentation next to code

**ADHD Impact:** Context switching is expensive. Minimize jumps between files.

### 2. Visible Progress

ADHD brains thrive on dopamine from progress signals:

```bash
# ✅ Good: Shows what's happening
$ bun test
✓ src/math.test.ts (3 tests) 45ms
✓ src/utils.test.ts (5 tests) 62ms
✓ src/cli.test.ts (8 tests) 125ms

All tests passed ✅ (16 tests, 232ms)

# ❌ Bad: No visibility
$ npm test
... (silent for 10 seconds)
PASS
```

### 3. Clear Entry Points

Make it obvious what to do next:

```bash
# Good README next steps
## Getting Started

1. Clone the repo
2. Run `bun install`
3. Run `bun run dev`
4. Open http://localhost:3000

Done! You're running now. Next steps:
- [ ] Read ARCHITECTURE.md
- [ ] Run `bun test` to see tests pass
- [ ] Check CONTRIBUTING.md for code style
```

### 4. Reduced Decision Paralysis

Provide good defaults instead of options:

```typescript
// ❌ Too many choices
const config = {
  cacheStrategy: "smart",      // Or "none", "memory", "disk"?
  workerCount: "auto",         // Or number?
  timeout: "adaptive",         // Or milliseconds?
  retryBackoff: "exponential", // Or linear?
};

// ✅ Smart defaults
const config = {
  cache: true,      // Works for 95% of cases
  workers: 4,       // Sensible default
  timeout: 30000,   // 30 seconds (standard)
};
```

### 5. Meaningful Status Indicators

Show not just progress, but context:

```bash
# ❌ Generic progress
[████████░░] 80%

# ✅ Meaningful progress
Building...
  ✓ Compiling TypeScript (2.3s)
  ✓ Bundling (1.1s)
  ⟳ Running tests (... 3s remaining)

Next: Linting (estimated 0.5s)
```

---

## Measurable DX: The Skill Matrix

Track developer growth and tool maturity:

### Developer Skill Levels

| Level | Knowledge | Speed | Independence |
|-------|-----------|-------|--------------|
| 1 Novice | Knows basics | Slow | Needs guidance |
| 2 Beginner | Understands patterns | Medium | Some independence |
| 3 Intermediate | Strong fundamentals | Fast | Self-sufficient |
| 4 Expert | Deep knowledge | Very fast | Mentors others |
| 5 Master | Innovates in domain | Instant | Shapes the field |

**Use case:** Help developers see their progression. "Moved from Level 2 (Beginner) to Level 3 (Intermediate)" is motivating.

### Tool Maturity Levels

| Level | API Stability | Documentation | Testing | Performance |
|-------|---------------|---------------|---------|-------------|
| Alpha | Unstable | Minimal | Partial | Unoptimized |
| Beta | Mostly stable | Good | Comprehensive | Optimized |
| Stable | Stable | Excellent | 90%+ coverage | Production-ready |
| Mature | Fixed | Complete | 95%+ coverage | Highly optimized |

**Use case:** Users know what they're getting. "This is a stable tool" vs. "This is an alpha experiment."

---

## Measuring DX: Key Metrics

### Time to First Success
How long until a new developer runs something successfully?

**Target:** < 10 minutes

```
1. Clone repo (2 min)
2. Run setup (3 min)
3. Run first command (1 min)
4. See success output (instant)

Total: 6 minutes ✅
```

### Time to First Failure
How long until a developer knows when something breaks?

**Target:** < 5 seconds

```bash
$ bun test
  ✓ math.test.ts (3/3) ✅
  ✗ utils.test.ts (2/3) ❌

Failed: utils.test.ts:15 - expected 5 got 4
```

### Cognitive Load (Subjective)
Ask developers: "How easy is it to understand this tool?" (1-5 scale)

**Target:** 4.0+

---

## DX Patterns Checklist

### For Tools/CLIs

- [ ] Help text is clear and concise
- [ ] Error messages include solutions
- [ ] Common commands are documented
- [ ] First-time setup takes < 10 minutes
- [ ] Progress is visible (not silent)
- [ ] Defaults are sensible (not all options required)
- [ ] Commands follow consistent pattern
- [ ] Output is formatted (not raw text)

### For Documentation

- [ ] Quick start is first section
- [ ] "Why" explained, not just "how"
- [ ] Examples are copy-paste ready
- [ ] Visual hierarchy (headers, lists)
- [ ] Terms are defined (not jargon)
- [ ] Links to deeper topics
- [ ] Table of contents
- [ ] Search capability

### For Code Organization

- [ ] Related files grouped together
- [ ] File names are descriptive
- [ ] Directory structure makes sense
- [ ] No hidden dependencies
- [ ] Tests next to code
- [ ] Configuration centralized
- [ ] Comments explain "why"
- [ ] README in each directory

### For Workflows

- [ ] Next step is always obvious
- [ ] Feedback is immediate
- [ ] Context switching minimized
- [ ] Blockers are surfaced early
- [ ] Progress is visible
- [ ] Skill growth is measurable
- [ ] Small wins celebrated
- [ ] Flow state achievable

---

## Common DX Pitfalls

### ❌ Don't

- **Verbose error messages** — Users ignore walls of text
- **Silent failures** — No feedback = confusion
- **Hidden complexity** — "Magic" that only experts understand
- **Inconsistent patterns** — Different commands work differently
- **Missing documentation** — Users have to read code
- **No defaults** — Every setting requires configuration
- **Long setup time** — Users give up during onboarding
- **Slow feedback** — Tests take 5 minutes to run

### ✅ Do

- **Concise, actionable errors** — One problem, one solution
- **Instant feedback** — User knows immediately if it worked
- **Transparent behavior** — Users understand what's happening
- **Consistent patterns** — Similar commands work similarly
- **Excellent documentation** — Answer "why" and "how"
- **Smart defaults** — Works out of the box
- **Quick setup** — < 10 minutes to first success
- **Fast feedback** — Tests run in seconds, not minutes

---

## Related Skills

- **Bun Runtime Workflows** — Performance = better DX
- **Bun CLI Development** — Building tools with great DX
- **Documentation Patterns** — Critical for reducing cognitive load
- **Testing Patterns** — Fast feedback loops

---

## Resources

### Research
- **Greiler, Storey, Noda:** "An Actionable Framework for Understanding and Improving Developer Experience" (2024)
- **SFIA:** Global skills and competency framework for digital roles

### Practical Tools
- Feedback loops: Watch mode, hot reload, pre-commit hooks
- Cognitive load: Progressive disclosure UI, clear naming
- Flow state: Monorepos, fast builds, single tools

---

## FAQ

**Q: How do I measure DX improvements?**
A: Track time-to-first-success, error clarity, and user feedback. Survey developers quarterly.

**Q: Is fast startup time important for DX?**
A: Yes. Bun's 4x speed matters psychologically — faster feedback = better experience.

**Q: How much documentation is enough?**
A: Enough that novices succeed without asking for help. Usually: README + architecture + API docs.

**Q: Should I optimize for experts or novices?**
A: Novices. If experts struggle, the tool is too complex. If novices succeed, experts will find power-user features.

**Q: Is cognitive load the same for everyone?**
A: No. ADHD brains especially benefit from clear structure, visible progress, and minimal context switching.

---

**Last Updated:** 2025-12-05
**Status:** Reference Implementation
**Based On:** DX Framework (Greiler, Storey, Noda), SideQuest Marketplace patterns
