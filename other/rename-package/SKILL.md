---
name: rename-package
description: Rename an Emacs package's files, features and API, with explicitly scoped repository, Elpaca and configuration updates. Use for an actual package rename, not ordinary prose cleanup or unrelated file/repository renames.
---

# Rename an Emacs package

Keep package, repository and runtime identities consistent across the requested
rename. A review or plan stays read-only; a source rename does not by itself
authorize publication, trust migration, source-checkout relocation or live
package removal. Do not execute this workflow while auditing the skill.

## Establish the rename contract

Separate the identities that happen to share a name: Elpaca registry ID, checkout
label, main library, provided features, public API prefix, remote repository,
manual outputs and local checkout path. Record exact OLD → NEW mappings and
which layers the user requested. A library-only rename leaves the surviving
package's other identities intact. Preserve an explicitly requested scope.

Use `dotfiles-context` and `elisp-conventions` before source edits. Resolve an
Elpaca-managed package with `bin/elpaca-package-resolve`/`elpaca-package-path`;
keep the registry's actual source, ID and evidence label. Do not infer
`sources/<name>` from a profile string or choose a build tree found by
`locate-library`. Unmanaged repositories retain their named checkout. Dotfiles
and extras belong in the canonical dotfiles tree, never its Elpaca mirror.
Resolve the named dotfiles helpers from that canonical root, not relative to
the package repository or current shell directory.

Inspect applicable repository instructions, worktree/index, branch/upstream,
remote identity, active writers and relevant visited/unsaved buffers. Record
the baseline HEAD and unrelated staged/unstaged work in each affected repo.
Read remote values without disclosing embedded credentials. Do not silently
save, revert or relocate a user's modified buffer. If package identity or
ownership remains ambiguous, resolve it before writing.

Inventory destination conflicts before edits, including untracked files,
symlinks, case-only names on case-insensitive filesystems, existing features,
public symbols and local checkout directories. Do not overwrite, merge into
or adopt an existing different target. A GitHub lookup failure is not proof
that a new name is available. A redirect may identify the same already-renamed
repository; compare repository identity before calling it a collision.

## Plan exact edits and verification

Build a bounded replacement map over the relevant tracked source and owned
configuration references. Include applicable:

- Library filenames, `provide`/`require`, autoload targets, package headers,
  `Package-Requires`, declared main/library paths and packaging recipes.
- Public/private symbols, custom groups and variables, keymaps, hooks, advice,
  mode names, integration callers and tests. Check computed symbol names and
  quoted strings as well as literal symbols.
- Manual references and actual export declarations, README badges/links,
  build/test scripts and CI paths. Derive generated Texinfo/Info filenames from
  their declarations; do not assume `old.texi` or a single test feature exists.
- Explicitly selected environment variables, generated data paths and external
  API consumers. Preserve user data and explain any compatibility boundary.

Search for candidates; do not replace every substring. For `agents` → `agent`,
an actual `agents-codex-handoff` API reference may change, while `subagents`,
`AGENTS.md` and prose about agents remain intact. Treat matches in historical
logs, old profiles, vendored code and unrelated projects as outside scope unless
requested. Keep intended legacy/compatibility references classified so a zero
search count is not the acceptance criterion.

Choose a compatibility policy from the request and existing package contract.
Do not introduce aliases as a hidden fix for failed tests, or remove an existing
transition layer merely to make the old name disappear. If compatibility would
materially change an otherwise ambiguous request, ask before selecting it.

Before making the old main library disappear, establish how the renamed source
will be tested and how the commit guard will bind that evidence. The standard
batch runner resolves the current registry ID and expects its main library;
a new name not yet in the registry, or a renamed main file under an old ID,
may be unsupported. Read `elisp-conventions/references/testing.md`. Use the
owning project's reviewed clean check for the proposed tree and diagnose a
missing evidence route; do not relabel another package's receipt, test an old
build, create a placeholder old library or disable a guard.

## Edit, test and commit source

Rename only the verified tracked paths, using literal quoted arguments and
`--` where supported. `git mv` stages changes: inspect any pre-existing staged
hunks in the same files first and preserve their separation. On case-only
renames, use a unique absent intermediate path if needed, verify both steps and
retain a recovery record if interrupted. Do not use force to overwrite a
destination.

Make the scoped content edits and update the applicable manual using the
package's existing documentation workflow. Run fresh source-based compilation
and focused ERT plus required project checks in a separate batch Emacs; follow
the conventions' source-first and stale-compiled-code rules. Do not run tests
through live `emacsclient`, add every profile build ahead of source or assume
an unqualified `emacs --batch` starts an isolated environment.

Test actual renamed commands/APIs, dependency requires, autoloads and consumers,
not just syntax. Verify both the new contract and any intended legacy behavior.
Record exactly which checks are blocked rather than calling an unregistered
package tested through another ID.

Review the full diff and only the rename-owned index content, preserving
unrelated hunks. Commit each verified logical change under the owning repo's
policy. Never use `git add -A` or broad commit path selection as a substitute
for isolating ownership. Keep package and dotfiles commits individually
identified; they are not one transaction.

## Publication, only when requested

Renaming the hosted repository and pushing commits are separate externally
visible actions. Obtain any missing authority before that action, not after it
has published unrelated commits. Use the configured GitHub service-access tools,
not a hard-coded account or branch.

Before a hosted rename, verify the source repository's stable identity, owner,
permissions and target availability. Consider GitHub Pages and published Actions:
[GitHub's rename documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)
does not promise redirects for those consumers. Do not create a replacement
repository, archive one, or change integrations outside the requested scope.

After the authorized rename, verify the returned repository identity/name. Update
only the selected local remote URLs, preserving transport, host, fetch/push URL
distinctions and unrelated remotes. If hosted rename was not authorized, keep
working remote URLs and publication links on the existing repository; a source
package name does not require the remote name to match.

If pushing was requested, resolve the actual destination ref and inspect the
entire outgoing commit range, including commits that predate this task. Ask for
scope only if that range includes unapproved work. Verify the selected source
SHA and remote tip, push the exact intended ref without force, and read back its
SHA. Do not hard-code `main`, push all branches/tags or rewrite history.
Use `post-push-ci` only after an authorized push or for an explicitly selected
commit. A temporarily absent run is not proof that no workflow was triggered;
respect the observer's bounded policy and report uncertainty.

## Local checkout and configuration

A filesystem checkout move is independent of a hosted rename. Perform it only
when requested and when active editors, builds, watchers and registry consumers
can remain consistent. An Elpaca registry object can retain absolute paths after
a shell move; changing `origin` or tangling a recipe does not repair that state.

Inspect the Git layout, linked worktrees and submodules before a directory move.
Use the supported [Git worktree operation](https://git-scm.com/docs/git-worktree)
for a linked worktree where eligible; it cannot move the main worktree or a
linked worktree containing submodules. For other layouts, establish the supported
move/repair procedure first. Refuse an existing target, preserve .git
indirections and verify HEAD, status, index and worktree connections afterwards.
Never nest the source inside an existing destination through an unchecked
`mv SOURCE TARGET` or rename a canonical dotfiles root as a package side effect.

Update selected dotfiles references in canonical `emacs/config.org`, extras and
owned documentation; leave previous profiles and unrelated configuration alone.
Follow `dotfiles-context` for paired artifacts and profile-aware tangling,
including its unsaved-buffer preflight. Generated profile init files are not
canonical sources. A successful tangle does not activate the new recipe.

Treat `emacs/lockfile.el` as generated package-manager state. Use its owning
workflow and verified resolved recipe/source revision if an update is required;
do not insert an assumed pushed SHA or regenerate unrelated lock entries.
Preserve valid old repository URLs when publication was excluded.

Session/history relocation is not a raw path replacement or incidental trust
edit. If requested, use each runtime's `move-session-log` workflow, or
`migrate-profile` for an actual profile-wide operation, with its offline and
recovery requirements. Leave trust/settings unchanged unless separately
authorized. Never rewrite `codex/config.toml` trust tables as a consequence
of a source filename or checkout rename.

## Activate and verify the requested runtime

Live activation needs a verified intended Emacs process/profile and the scope
to change that package's running state. Read the conventions' live-verification
reference. Inspect the installed Elpaca recipe/registration mechanism before
reconciling registry ID, source path, main feature and dependencies. A new
`elpaca` declaration may install another checkout; do not assume it reuses the
renamed source, or clone an unrequested repository to make a check pass.

Do not blindly enqueue `elpaca` plus an unbounded `elpaca-wait`. Use the
bounded rebuild/live-verification helpers only when they support the identified
new registry/source layout, and observe any existing rebuild before launching
another. Do not pass a guessed new name to the helper or bypass it with
`load-file`. If safe in-session registration/activation is unsupported, preserve
the committed source and report activation pending. Do not restart, signal or
switch Emacs profiles without explicit authority.

Already-loaded old definitions, hooks, timers, advice and keymaps do not
disappear when their file or build directory is renamed. Use the package's
supported lifecycle teardown/transition only within the requested activation;
do not force-unload dependencies or use destructive `deleted:PACKAGE`
verification for a library rename inside a surviving package.

After the committed rebuild, verify the new registry/source identity and loaded
code provenance, then exercise the renamed user-visible command through
`end-to-end`. A `locate-library` or `fboundp` result alone is insufficient.
Check intended absence or compatibility of old features and active callbacks,
not merely whether an old library remains on disk. Keep other profiles intact.

Only trash an exact inspected generated old build when cleanup is authorized,
it is no longer in use and the new runtime is verified. Preserve source trees,
user data and unrelated builds. Report partial state if a later phase fails;
do not automatically undo a hosted rename, restore over newer edits or delete
sources to make the filesystem look complete.

Report the completed scope, actual commits and any requested publication/runtime
result. Name remaining activation, compatibility, relocation or CI gaps only
where they change the outcome; do not describe an entirely local rename as
published or fully active.
