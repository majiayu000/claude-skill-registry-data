---
name: reviewing-cpp
description: Reviews C++ desktop code for memory safety, framework anti-patterns, build system issues, and thread safety. Use when reviewing C++ GUI code quality or when the user asks for code review.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob
  argument-hint: [file-or-directory]
  stability: stable
  content-hash: sha256:5d7b41a7e11ef261a0eac761368c2b26933bf811211574dce8d6f5969c11b430
---

# Review Context

- Changed files: !`git diff --name-only HEAD~1 2>/dev/null || echo "No recent commits"`
- Staged files: !`git diff --staged --name-only`

## C++ Desktop Code Review

**Scope**: $ARGUMENTS

Delivers **focused, streamlined** C++ desktop code reviews matching stated task
requirements exactly. No over-analysis.

## Workflow

1. **Read task requirements** to understand expected scope
2. **Detect framework** (wxWidgets / GTK3 / Qt) from includes and CMakeLists.txt
3. **Match review depth** to task complexity (single file vs multi-module)
4. **Validate requirements** — does implementation match task scope exactly?
5. **Issue focused feedback** with specific file paths and line numbers

## Review Strategy

**Simple Tasks (single file/widget)**: Memory safety, framework correctness,
requirements match

**Complex Tasks (multi-module)**: Above plus architecture, ownership graph,
event flow, thread safety

**Always**: Check CMakeLists.txt, check for raw pointer leaks

## Review Checklist

**Memory Safety**:

- [ ] No raw `new` without matching `delete` (prefer smart pointers)
- [ ] No dangling pointers to destroyed widgets
- [ ] RAII used for all resource acquisition (files, sockets, handles)
- [ ] No `reinterpret_cast` without safety justification
- [ ] Container access bounds-checked where needed (`at()` vs `[]`)

**Framework Anti-Patterns**:

- [ ] wxWidgets: no manual delete of child windows (parent owns them)
- [ ] GTK3: all `g_object_unref` / `g_free` calls present
- [ ] Qt: no `delete` on QObject children (parent-child ownership)
- [ ] No blocking calls in GUI event loop (use async/worker threads)
- [ ] Event handlers do not throw exceptions across framework boundaries

**Build System (CMakeLists.txt)**:

- [ ] Target-based commands (no `include_directories()`, `link_libraries()`)
- [ ] `find_package()` with imported targets, not raw variables
- [ ] Minimum CMake version specified
- [ ] No hardcoded paths or platform assumptions without conditionals

**Thread Safety**:

- [ ] GUI updates only from main thread
- [ ] Worker threads use framework-specific dispatch (wxWidgets: `CallAfter`, Qt: `QMetaObject::invokeMethod`, GTK: `g_idle_add`)
- [ ] Shared data protected by mutex or atomic operations
- [ ] No data races between event handlers and background threads

**Code Quality**:

- [ ] Follows project patterns in `src/` and `include/`
- [ ] Const-correctness on methods and parameters
- [ ] Forward declarations used to minimize header coupling
- [ ] GUI logic separated from business logic

## Output Standards

**Simple Tasks**: CRITICAL issues only, clear approval when requirements met
**Complex Tasks**: CRITICAL/WARNINGS/SUGGESTIONS with specific fixes
**All reviews**: Concise, actionable, no unnecessary complexity analysis
