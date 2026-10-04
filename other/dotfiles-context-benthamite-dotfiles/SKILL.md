---
name: dotfiles-context
description: Route changes to emacs/config.org, dotfiles extras, Elpaca-managed package checkouts, and paired Claude/Codex configuration. Use to prepare external-package fixes, choose the canonical edit location, tangle the active Emacs profile, or run paired-config checks; not for read-only or unrelated dotfiles work.
user-invocable: false
---

# Dotfiles and package routing

Use this context to choose the correct source tree and verification path. If the
task changes Emacs Lisp, also use `elisp-conventions` for coding, batch-test,
rebuild, and live-verification rules.

Before adding or changing agent-facing guidance, read the canonical
[instruction placement policy](../../../agents/instruction-placement.org),
including its permission boundary for `AGENTS.md` and `CLAUDE.md`.

## Canonical sources

- `~/My Drive/dotfiles/` is the canonical dotfiles source. It is the intentional
  exception to the rule that development repositories do not live under the
  Drive sync root.
- The active profile's `elpaca/sources/dotfiles/` checkout (or its registry's
  legacy equivalent) is a read-only mirror. Do not edit it, even if an edit guard
  does not fire. Commit-time synchronization supplies its canonical changes.
- Extras belong in canonical `emacs/extras/`, not the runtime mirror. The helper
  recognizes their package IDs and returns that directory.
- For other Elpaca-managed packages, use the source directory reported by the
  live package registry. It is usually `elpaca/sources/<package>/`; a legacy
  registry may report `elpaca/repos/<package>/`. Do not choose between profiles
  or directories by scanning for whichever checkout happens to exist.

Resolve package paths with the deterministic helper instead of guessing a
profile or using `locate-library` or `symbol-file`:

```bash
~/My\ Drive/dotfiles/bin/elpaca-package-path PACKAGE [relative-path]
```

The helper returns the canonical dotfiles root for `dotfiles`, the canonical
extras directory for an extras ID, and the live registry's source for standalone
packages. Confirm success and repository identity; an unavailable or ambiguous
registry is unresolved, not permission to guess a path or edit a build tree.
Keep any supplied relative path within the resolved source directory. For an
ordinary standalone repository outside Elpaca, retain the user's named checkout;
this routing rule does not move every repository into an Emacs profile.

Pushing is a separate sharing step; it is not required to update the local
dotfiles mirror. The commit hook's intended sync is not proof that the mirror
or loaded code reached that commit: observe the relevant completion evidence.

## Workflow

1. Resolve the canonical source and applicable repository instructions before
   editing. Inspect working tree/index and relevant unsaved buffers. Preserve
   other work, including unrelated hunks in a file you also need to change.
2. For `.el` changes, follow `elisp-conventions` after choosing the layout.
3. For `emacs/config.org`, read
   [references/config-org.md](references/config-org.md), complete its live
   source/profile and buffer preflight, then use the profile-aware command below.
4. For paired Claude/Codex configuration or skill changes, inspect the pairing
   manifest and update the canonical tracked counterparts. Preserve documented
   unpaired artifacts and runtime-specific metadata, paths and implementation
   differences; semantic parity does not require identical bytes. Do not edit
   generated shims or plugin caches as substitutes for their maintained source.

After an authorized `emacs/config.org` change, once preflight is satisfied, tangle
the intended running profile with:

```bash
emacsclient -e '(init-build-profile (file-name-directory user-init-file))'
```

Do not use `org-babel-tangle-file` directly. It does not know the active profile
and can write to the wrong target.

If the running server/profile cannot be verified, preserve the source edit and
report activation as pending. Do not start, switch or restart Emacs to conceal
the gap. A successful tangle generates files; it does not reload configuration
or prove an Elpaca recipe, checkout or package changed in the running session.

When a fix belongs to an externally maintained package, read
[references/upstream-pr-pins.md](references/upstream-pr-pins.md) before editing,
even when the user has not mentioned a PR. Prepare the upstream contribution
and local retention plan within the requested scope; publication requires
explicit authorization. Also use that reference for an existing upstream PR
whose Elpaca change must remain active locally. Diagnosis-only requests stay
read-only, and an explicit local-only request excludes PR preparation.

If an authorized committed package change needs an explicit rebuild and an
observable completion point, use the bounded helper and target the package,
not the aggregate `dotfiles` source. Observe any already-started commit-hook
rebuild first rather than launching a competing one:

```bash
~/My\ Drive/dotfiles/claude/bin/elpaca-rebuild-wait PACKAGE
```

## Verification

- Confirm the intended source/profile and generated output after a tangle;
  distinguish that from separately authorized live activation and behavior.
- Follow `elisp-conventions` for every Emacs Lisp change.
- Run `~/My\ Drive/dotfiles/bin/ai-config-sync audit` after paired
  Claude/Codex changes.
- If a tracked public skill name or catalog description changed, run
  `~/My\ Drive/dotfiles/bin/docs-audit generate` and then
  `~/My\ Drive/dotfiles/bin/docs-audit audit`. Inspect the generated diff and
  preserve concurrent catalog edits; a generator can update more than your row.
- Inspect `git status --short` before completion so unrelated concurrent edits
  remain separate.
- Commit logical owned changes under repository policy. Path selection alone
  does not isolate unrelated hunks in the same file. Report unresolved routing,
  sync or activation gaps without treating a configured path as a verified one.
