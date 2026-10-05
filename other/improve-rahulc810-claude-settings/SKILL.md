---
name: improve
description: Scan the code against four architecture checks — layout, isolation, interface strength, extensibility — and propose specific fixes without applying them. Trigger on:- improve, review architecture, find improvements, refactor candidates, what's wrong with this module.
allowed-tools: Read, Grep, Glob, Bash
---

# Improve Architecture

Off the linear pipeline (`.specify/memory/constitution.md`) — reach for it when a file
keeps getting harder to touch. For a specific diff or plan use `/code-review`; to apply
routine cleanups use `/simplify`.

Good code comes down to four things. Check candidates against these, in order — each one tends to cause problems in the ones below it.

1. **Simple layout** — can you find things? Directory and file structure should map obviously to what's in them, no hunting.
2. **Isolation** — similar things live as separate, isolated workers, not entangled with each other. Shared code lives in one obvious shared place, not duplicated or reached-into.
3. **Strong interfaces** — a module's public surface fully covers what callers need, so nobody reaches into internals or leaks details out.
4. **Simple (not easy) to extend** — adding a new case fits the existing shape without special-casing or touching a pile of unrelated files. Simple means the extension is obvious and in one place, even if writing it takes real work.

Tests and performance aren't separate checks — they tend to follow once these four hold.

## When to use this

When a file keeps showing up in recent changes and each change to it feels harder than it should, or when asked directly to find refactoring opportunities. Skip this for a codebase small enough to hold in your head, or when nothing's actually hurting yet.

## Steps

1. **Find the hot spots.** If the user named a file or area, use that — skip inference. Otherwise, check `git log --oneline` over a reasonable stretch for files that keep recurring; that's where change pain is actually felt.

2. **Read the candidate against the four checks, in order.** Stop at the first one that's actually broken — a layout problem will often manifest as an interface problem downstream, so fix the upstream cause rather than patching the symptom.
   - Layout: does the structure make sense on its own, or do you need tribal knowledge to find things?
   - Isolation: does this module get entangled with siblings it shouldn't touch? Is shared logic actually shared, or copy-pasted / reached into?
   - Interfaces: do callers need to know internals to use this correctly? Does the interface leak more than it should?
   - Extensibility: pick a plausible next addition — does it fit in one obvious place, or does it require touching several files or adding special cases?

3. **Propose 1-2 concrete fixes, not a list of vague concerns.** Name the check it fails, what changes, and what gets simpler as a result. If you can't describe the fix concretely, keep reading — you don't have a real proposal yet.

4. **Let the user pick.** Present candidates plainly (file, which check fails, proposed fix) and stop. Don't refactor unprompted.

## What not to do

- Don't produce more than a couple of candidates — if everything looks broken, the scope was too wide; narrow it
- Don't refactor speculatively for code nobody's touched recently or complained about
- Don't chase tests or performance directly here — if the four checks hold and tests/performance are still bad, that's a different problem, not this skill