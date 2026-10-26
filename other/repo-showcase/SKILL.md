---
name: repo-showcase
description: Make a repo public-facing on its working tree — README rewritten around outcome and demo, stale docs pruned, outdated claims fixed, secrets and private names found, GitHub metadata proposed — then hand off to /repo-scrub. Use for "showcase this repo", "polish the README for public", "prep for open-source or portfolio".
argument-hint: "[owner/repo] (default: current repo)"
---

Working tree only. History and visibility belong to `/repo-scrub`. **Gate**: every redaction, README rewrite, metadata change, commit, and push needs an explicit yes.

## 1. Ask (one batch, each with its default)

1. **Outcome**: what a stranger should do after reading (default: try it in under 5 minutes).
2. **Audience** (default: developers deciding whether to use or contribute).
3. **Emphasis**: the one thing worth a look (default: the latest merged feature or current headline claim, confirmed rather than invented).

"go" → defaults.

## 2. Doc inventory

Every tracked doc (`README*`, `docs/**`, `CONTRIBUTING*`, stray notes): table Path · keep / merge / delete · reason. Untracked docs are listed separately as `not shipped` and never rewritten or published. Act on rows only after a yes, echoed back.

## 3. Claims vs reality

Check every factual claim (languages, versions, install steps, commands, badges, "beta", architecture) against code, config and `git log`. Report `claim file:line` — `evidence file:line or SHA`. These feed §4 and the diff gate.

**License**: no `LICENSE*` file → flag it here and gate it. A license declared only in a manifest (`package.json` `license`, `pyproject.toml` `[project] license`, `Cargo.toml` `license`) is the user's stated pick: offer to add the matching `LICENSE` file (standard text, their name and year) and gate that. A `LICENSE` file that disagrees with the manifest → flag both `file:line`. Neither → offer the choice (name a few common ones); never pick one for them, and don't name a license in the README until they have.

## 4. README draft (lean)

1. One-line pitch. 2. Result: what using it produces. 3. Demo slot: `<!-- screenshot/GIF: paste path or URL -->` for the user to fill; media and metrics are never fabricated. 4. Quickstart, actually run: in a clean clone (`git clone . "$(mktemp -d)/x"`, `--recurse-submodules` when `.gitmodules` exists; flag a private submodule and a relative URL, which resolves against wherever the repo is cloned from; a working tree with an untracked `skilleddocs/` can break `pip install .`, see [TRACKING.md](../handoff-auto/TRACKING.md)), with every install landing in a temp dir: `npm install -g . --prefix <tmp>`, `pip install .` in a fresh venv, `go install ./...` with `GOBIN=<tmp>`, `cargo install --path . --root <tmp>`. Never a global or user-level install. A step that installs by registry name (`npm install -g <name>`, `pip install <name>`, `cargo install <name>`) runs only when the registry entry is this project: same name and its repository URL (`npm view <name> repository.url`, PyPI `project_urls`, crates.io `repository`) matches this repo's remote. Otherwise install from the clone instead and flag the README line: the name may belong to someone else. Report pass/fail with the output. A step whose toolchain is missing here (`command -v <tool>` fails) is not a failure: report `not run: <tool> missing`, keep the step as written, never drop it. A step that is itself wrong: fix it, or drop it on yes. 5. Architecture, only if the audience needs it. 6. Credits and license.

Draft only; the file changes at §7.

## 5. Secrets and private names

Tracked files: key/token/connection-string patterns (`gitleaks dir .` if installed), un-ignored `.env`. Personal names: grep for email addresses, then read comments and docs for person names, docs marked delete at §2 included; flag any that aren't authors (`git shortlog -sne`) or already public. Commit messages and identities: `git log --all --format='%an %ae %cn %ce%n%B' | grep -Eo '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]+' | sort -u` and `git log --all --format='%an <%ae>%n%cn <%ce>' | sort -u`; ask which are the owner's own and drop those; cite the rest by SHA. Report `file:line`; redact per item on yes (written at §7). Keep for §8 every personal string (name, email) redacted, removed with a deleted doc, or found only in history: the tree edit leaves it in every old commit. Non-owner identities: ask "rewrite in history" or "author identities stay", and keep the answer for §8. Secrets go by `file:line` only, never the value.

## 6. Metadata

Propose description, topics, homepage; `<o/r>` per the `next` skill's `BOARD.md`, Target repo section (fork → ask which repo first); show `gh repo edit <o/r> --description "…" --add-topic … --homepage …`; run on yes. No GitHub remote (`git remote -v` shows none, or a non-GitHub host) → print the command for later and skip.

## 7. Gate: diff, commit, push

Show the full README diff plus one line per doc change and redaction. Commit on yes from a separate worktree on a new branch based on the current one (note it first): `git worktree add "$(mktemp -d)/showcase" -b showcase/public <noted branch>`. Write each changed file there and `git rm` deleted docs there, never in the user's checkout, so their WIP and untracked files stay out and nothing needs switching back; stage only those paths (never `-A` or `.`), one logical change per commit (`docs: rewrite README for public release`), then `git worktree remove <path>`. A changed file that also holds user WIP → ask first: the worktree copy starts from the committed version, so the WIP stays out, but merging the branch will meet it. Push on a separate yes.

## 8. Hand off and record

Next step: `/repo-scrub` for the history scan and the visibility flip, kept separate on purpose. Merge (or push) `showcase/public` first, on a yes: repo-scrub scans pushed history, and its post-push reset would rebase an unmerged branch whose deleted docs conflict with the rewrite. Hand it every personal string kept at §5 (redacted, from deleted docs, message-only) and each non-owner identity with the user's answer; gitleaks has no rule for names or emails, so repo-scrub checks each with `git log -m -S`/`--grep` (`-m`: merge commits too), scrubs strings with a `literal:` rule and identities with a mailmap. Save inventory, claims, findings, and what was done to `skilleddocs/showcase/<local-date>.md`, uncommitted unless asked (and not counted among the files you commit in §7). Untracked → exclude `skilleddocs/` per [TRACKING.md](../handoff-auto/TRACKING.md) (it also covers the `pip install .` hazard).
