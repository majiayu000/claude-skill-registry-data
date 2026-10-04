---
name: commit-message
description: >
  Build and create a git commit following this repository's established message
  format. Use when the user asks to "commit", "commit all changes", "commit and
  document", or similar. Also applicable when any agent (gemini-cli, codex,
  qwen, opencode, claude-code) needs to stage and commit a set of changes with
  a properly structured message.
version: 1.0.0
---

# Commit Message Skill

## Purpose

Stage all relevant changes and create a git commit whose message matches the
format already established in this repository: a conventional-commit subject
line followed by a structured body that groups changes by category.

This skill is intentionally written in plain, agent-agnostic language so it
can be followed by Claude Code, Gemini CLI, Codex, Qwen, opencode, or any
other LLM-based coding agent.

---

## Step 1 — Gather context

Run the following commands and keep their output in mind for the rest of the
process. Do not skip any of them.

```bash
# Learn the repo's commit message format and subject-line style
git log --oneline -10

# Identify every file that has changed since the last commit
git diff --stat HEAD

# See the full diff for changed files that need to be understood
git diff HEAD

# Confirm which branch you are on
git branch --show-current
```

---

## Step 2 — Determine the commit type

Inspect the nature of the changes and pick exactly one conventional-commit
type prefix that fits:

| Prefix   | Use when                                                        |
|----------|-----------------------------------------------------------------|
| `feat`   | A new feature or capability is added                           |
| `fix`    | A bug, warning, or incorrect behavior is corrected             |
| `chore`  | Build system, dependencies, CI, or tooling changes             |
| `refactor` | Code restructuring with no functional change                |
| `test`   | Tests added or updated                                         |
| `docs`   | Documentation only                                             |
| `perf`   | Performance improvements                                       |
| `style`  | Formatting/whitespace with no logic change                     |

If the changes span multiple types but share a single theme (e.g., fixing
many warnings across many files), use the dominant type (`fix`) and document
the breadth in the body.

---

## Step 3 — Write the subject line

Format: `<type>: <short imperative summary>`

Rules:
- 72 characters maximum.
- Imperative mood ("fix", "add", "remove" — not "fixed", "adds", "removes").
- No trailing period.
- Specific enough to distinguish this commit from adjacent commits in
  `git log --oneline`.

Examples from this repo:
```
fix: silence compiler warnings across GCC and Clang
fix: silence compiler warnings in RI pipeline
fix: clang warnings and thread linkage
chore: add project identity macros and use them
test: split teapot motion for raytrace and REYES
```

---

## Step 4 — Write the body

The body follows the subject line after **one blank line**. It must:

1. **Open with a one-sentence description** of the overall goal or motivation
   (the "why", not the "what").

2. **Group individual changes by category**, each group introduced with a
   short heading followed by bullet points. Category examples:
   - Warning class (e.g., `-Wsequence-point`, `-Wunused-result`)
   - Subsystem (e.g., `CMake / Clang alignment`, `Build system`)
   - Feature area (e.g., `Shader pipeline`, `Network layer`)

3. **List files or modules affected** within each bullet, concisely. Prefer
   naming patterns over individual filenames when many files share the same
   fix (e.g., "brickmap.cpp, debug.cpp, texture.cpp" or "all fread() callers
   in the RI pipeline").

Body line width: 72 characters maximum (wrap prose, but keep code snippets on
one line even if longer).

---

## Step 5 — Stage files

Stage specific files by name. **Do not use `git add -A` or `git add .`**
unless you have verified that every untracked file in the working tree should
be committed.

Never stage:
- `.env` files or any file that may contain credentials or secrets
- Binary build artifacts (`*.o`, `*.a`, `*.so`, `*.dylib`)
- IDE workspace files (`.vscode/`, `.idea/`, `*.swp`)
- CMake build directory contents (`build/`, `CMakeCache.txt`, etc.)

Inspect `git status` and `git diff --stat HEAD` to identify exactly which
files belong to this commit.

---

## Step 6 — Create the commit

Use a HEREDOC to pass the message so multi-line formatting is preserved
exactly as written. Replace `<Agent Name>` and `<agent@email>` with the
appropriate attribution for the agent performing the commit.

```bash
git commit -m "$(cat <<'EOF'
<type>: <subject line>

<one-sentence motivation / overall goal>

<Category heading 1>:
  - <change description, files affected>
  - <change description, files affected>

<Category heading 2>:
  - <change description, files affected>
EOF
)"
```

---

## Step 7 — Verify

After the commit succeeds, run:

```bash
git log --oneline -3
```

Confirm the new commit appears at the top with the correct subject line and
that `git status` shows a clean working tree (or only intentionally unstaged
files).

---

## Complete example

This is the exact commit produced for the warning-fixes batch in this
repository. Use it as a reference for tone, level of detail, and grouping
structure:

```
fix: silence compiler warnings across GCC and Clang

Systematically eliminate all -Wall/-Wextra/-Wpedantic warnings produced
by GCC 13 on Linux and align Clang/AppleClang flag coverage to surface
the same diagnostics on macOS builds.

Warning categories addressed:

- -Wsequence-point / -Wunsequenced: fix *ptr++ = (*ptr) * k UB pattern
  in renderer.h, curves.cpp, bsplinePatchgrid.cpp, patches.cpp,
  subdivision.cpp; replace with local capture before increment

- -Wunused-result (fread): wrap all discarded fread() calls in if()
  checks with /* read error */ body across brickmap.cpp, debug.cpp,
  precomp.cpp, texture.cpp, texmake.cpp, fileResource.cpp,
  irradiance.cpp, remoteChannel.cpp, rendererNetwork.cpp, show.cpp,
  map.h (template — fixes all instantiation sites at once)

- -Wmaybe-uninitialized / -Wuninitialized: add = nullptr / = 0 / = {}
  initializers to variables in execute.cpp, executeMisc.cpp,
  shaderOpcodes.h, shaderFunctions.h, giFunctions.h, surface.cpp,
  linsys.cpp, occlusion.cpp, polygons.cpp, pointHierarchy.cpp,
  stochasticQuad.h

- -Wdeprecated-declarations: replace libtiff uint32/uint16 typedef
  aliases with uint32_t/uint16_t in texture.cpp and texmake.cpp

- -Wformat-truncation: resize buffers in sdr.y (tmp[]) and
  rendererFiles.cpp (tmp[OS_MAX_PATH_LENGTH+1])

- -Wimplicit-fallthrough: add __attribute__((fallthrough)) in fbx.cpp,
  pp1.c, pp2.c; fix sl.y null-pointer init

- -Wempty-body: wrap assert(FALSE) else-branches in braces in
  rendererDeclerations.cpp

- -Wsign-compare: cast fread return comparison to size_t in texture.cpp

- -Wsizeof-pointer-memaccess: replace sizeof(scratch) with
  ribOutScratchSize in ribOut.h; add extern declaration

- -Wunknown-pragmas: guard #pragma clang diagnostic in ri.cpp with
  #ifdef __clang__

- -Wunused-variable: move invBezier/dinvBezier from patchUtils.h into
  the single .cpp that uses each; fixes a real copy-paste bug in
  quadrics.cpp (Pstart written instead of Pend for motion blur)

CMake / Clang alignment (CMakeLists.txt, src/oshader/CMakeLists.txt):
  add -Wunused-but-set-variable, -Wunsequenced, -Wimplicit-fallthrough
  for Clang/AppleClang so the same diagnostic categories surface on
  macOS builds without loosening any existing flags
```

---

## Quick-reference checklist

Before running `git commit`, confirm:

- [ ] `git log --oneline -10` reviewed — subject style matches repo conventions
- [ ] Subject line ≤ 72 chars, imperative mood, correct `type:` prefix
- [ ] Body opens with a motivation sentence
- [ ] Changes grouped by category with bullet points
- [ ] No secrets, binaries, or build artifacts staged
- [ ] HEREDOC used to pass the message (preserves newlines)
