---
name: agents-md
description: "When the user explicitly asks to create or repair repository agent instructions — build a minimal AGENTS.md."
disable-model-invocation: true
---

# AGENTS.md

Build the smallest useful always-loaded map of the repository, not a generated handbook.

1. **Inspect before proposing.** Target the repository root unless the user names a package or subtree. Inspect the path type and content of `AGENTS.md` before proposing any change. A directory at that path is a blocker. Read symlink targets for evidence, but never write through a symlink. Then read the README, manifests, lockfiles, scripts, CI configuration, linked docs, and nested instruction files needed to establish current truth; do not infer commands or conventions from ecosystem defaults.
2. **Resolve the edit.** Present the proposed keep, move, and remove set and get approval. Show contradictions between the instruction file and the repository, and ask which intent wins. Preserve confirmed project constraints; remove stale, redundant, obvious, vague, or unenforceable guidance. Other instruction files are outside this skill's write scope.
3. **Keep a recovery path.** Before replacing a regular `AGENTS.md`, check its Git status. A tracked, clean file needs no backup. Copy any untracked, ignored, staged, or unstaged regular file to the adjacent `<name>.bak` first; never overwrite an existing backup. For a symlink, remove only the link entry after approval, never its target.
4. **Write one canonical source.** Create a regular root `AGENTS.md`: purpose, stable ownership boundaries, important verified commands, non-obvious constraints, and conditional pointers. Keep essential rules visible; a map is not just a list of links. Describe capabilities and agreed domain terms, not an exhaustive file tree or skill catalog. Use this repository's facts, not the author's harness layout or personal workflow.
5. **Disclose progressively.** Each pointer says when to read its target and what it answers. Route growing, maintaining, updating, and fixing the project to existing owners: README, focused docs, source, scripts or CI. Keep portable technique separate from repository facts. Move detailed guidance only to a maintained destination; create a doc when real content needs an owner, not to fill a template. No mandatory glossary, tracker, memory tree or sibling skill installation. Use nested `AGENTS.md` files only for real package scopes, without repeating root rules.
6. **Validate.** Re-read `AGENTS.md`. Verify every linked local file and heading exists, every named command comes from repository truth, scoped rules have one owner, and no symlink was followed for writing. Walk representative change, update and bug-fix tasks from the map to the actual guidance; an existing but irrelevant target is a broken pointer too. Static checks prove navigation and structure, not that a model follows the instructions.

Deliver: files created or changed, backups created, guidance kept/moved/removed, unresolved contradictions, and validation performed.
