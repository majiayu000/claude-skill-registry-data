---
name: om-auto-implement-spec
description: money-tracker.online extension of the installed om-auto-implement-spec skill. Spec lifecycle bookkeeping - the metadata table, the status directories and the generated index. The installed workflow applies unchanged.
---

Extends the installed skill: read `.claude/skills/om-auto-implement-spec/SKILL.md` and follow it. On
top:

- `$SPECS_DIR` is `.ai/specs` and it has **status directories**: a spec is at the root while it is
  unbuilt, in `implemented/` once every phase has shipped, in `archived/` when it was superseded or
  abandoned. Spec resolution searches all three, so a `{spec}` slug that matches
  `implemented/2026-09-09-desktop-layout-density.md` resolves to that path. `assets/` is not a status
  directory and holds no specs. The rules are `.ai/specs/AGENTS.md`; read it before touching the
  directory.
- Every spec carries a metadata table directly under its `H1` (`Status`, `Issue`, `Spec PR`,
  `Implementation`). **This skill owns the last two rows of its lifecycle.** When the implementation
  PR opens, set `Status` to `in-progress` on the implementation branch. When a phase merges, append
  its PR number to `Implementation`, in merge order.
- When the **final** phase merges, `git mv` the spec into `.ai/specs/implemented/` and set `Status` to
  `implemented` in the same commit. A spec whose phases ship on more than one PR stays at the root
  with `Status: in-progress` until the last one lands - partial delivery is not `implemented`, and
  `.ai/specs/AGENTS.md` → Ask First covers the judgement call.
- Anything that shipped differently from the design is an `## Amendment` section in the spec naming
  its PR, not a silent divergence. `.ai/specs/implemented/2026-09-09-desktop-layout-density.md` is the
  worked example.
- Run `pnpm generate-spec-index` after any of the above and commit `.ai/specs/README.md` with the
  change. It is generated, and the validation gate compares it (`AGENTS.md` → Validation Commands).
  Nothing checks that a table agrees with the directory holding it, so keep them in step by hand.
- The implementation PR is the one that carries all of this. The spec PR stays design-only, exactly as
  the installed skill says.
