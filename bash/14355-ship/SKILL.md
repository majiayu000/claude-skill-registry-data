---
name: ship
description: Release automation — commit squash, version bump, changelog, push, GitHub release. Works with any project.
---

<Purpose>
Squash WIP commits into meaningful units, bump versions, and push releases.
Works with xm marketplace plugins AND standalone projects.
Release documents (commit message, changelog entry, release notes) are written by `xm:write`.
Optimized for minimum turns: parallel discovery + single decision gate.
</Purpose>

<Use_When>
- User says "ship", "release", "ship it", "릴리스", "배포"
- User wants to clean up commit history before release
- User wants to bump versions and push
</Use_When>

<Do_Not_Use_When>
- Deploy to production servers (use CI/CD or /land-and-deploy)
- Create a PR without releasing (use git directly)
</Do_Not_Use_When>

## Wiring

```
after: x-review
suggests: x-humble
```

# x-ship — Release Automation

Commit squash + version bump + push. Works with any git project.

## Model Routing

| Step | Model | Reason |
|------|-------|--------|
| Step 0 (parallel discover) | **haiku** (Agent tool) | Pure git/script reads, no reasoning |
| Mode: status, dry-run | **haiku** (Agent tool) | Read-only display |
| Mode: squash (single) | **haiku** | Mechanical reset+commit |
| Step 1 (decision gate) | **session** (leader) | Squash strategy + bump type judgment — rides the model the user picked via /model |
| Step 2 (grouped squash) | **session** (leader) | LLM groups files by scope |
| Step 1 (documents via `xm:write`) | **session** (leader) | Quality writing matters for changelog and release notes |

For haiku-eligible steps, delegate via: `Agent tool: { model: "haiku", prompt: "Run: <bash>" }`. <!-- managed-model: writer -->

**Guardrail**: never haiku for grouped squash, bump-type decision, or release document authoring — these affect the published release.

## Output Style

### Korean output style (avoid AI-slop)

Universal (both modes) — these read as machine-generated in any register:
- Drop empty intensifiers ("매우 / 완벽하게 / 강력한 / 원활하게 / 혁신적인") unless they carry a specific, real claim.
- No forced rule-of-three or "~뿐만 아니라 ~까지" balance that adds no fact.
- No hedged non-conclusions ("결국 상황에 따라 다르다 / 균형이 필요하다"). End on a concrete fact, number, or next action.

Developer mode: terse and direct — lead with the result; state findings/actions without a 권고형 결말 pile-up ("~해야 한다" sentence after sentence).
Easy/normal mode: accessible Korean is the goal — polite guidance ("~해 보세요"), one line of context for non-experts. Keep commands, flags, paths, and proper nouns in English; on first use write a domain term as Korean(original), e.g. 결론(verdict). Still apply the universal rules; accessible ≠ padded or vague.

## CLI Invocation

> **⚠ Call `xm build <command>` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`resolve_xmb()`) and variables (`XMB=…`) defined in one call do NOT persist to the next, so the following call fails with `command not found`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XMB_CLI=$(ls -d ~/.claude/plugins/cache/xm/{build,xm}/*/lib/x-build-cli.mjs 2>/dev/null | sort -V | tail -1)
> node "$XMB_CLI" release detect
> ```
>
> **Forbidden:** `XMB="node …"; $XMB release detect` — zsh expands `$XMB` as a SINGLE token, so it looks for a command literally named `node /path/x-build-cli.mjs` and fails. A path-only variable plus `node "$XMB_CLI"` is the working form.

**Mode detection (once, at the first CLI call):** run `xm build release detect`. If it succeeds, you are in **xmb mode** — use `xm build …` for every step below. If it fails (`command not found`, `Cannot find module`, or the fallback above also finds nothing), you are in **plain-git mode**: skip every `xm build` call and use the **Plain-Git Fallback** procedure (bottom of file).

Do NOT cache this in a shell variable — it will not survive to the next Bash call. Carry the decision in your own reasoning for the rest of the run.

## Project Mode Detection

Decide once, upfront. Cache the result for the rest of the run.

| Signal | Mode |
|--------|------|
| `.claude-plugin/marketplace.json` at repo root | marketplace (use `--plugins`) |
| Otherwise | standalone (use `--standalone` or plain-git) |

**`.xm/` is NOT a mode signal.** It is the data directory every xm tool writes into (panel runs,
review artifacts, traces) — a Rust or Go repo where someone once ran `/xm:review` has one. Keying
`marketplace` off it routes a non-plugin repo into `--plugins` versioning, which fits nothing there.
Same for `x-build/lib/`: that means "you are standing in the x-kit repo", not "this is a plugin
marketplace". Only the marketplace manifest decides.

### Version Source (standalone)

`release detect` reports the project type; do NOT assume `package.json`. What carries the version:

| Project | Version source | Tag |
|---------|----------------|-----|
| node | `package.json` `"version"` | `v<version>` (conventional) |
| rust | `Cargo.toml` `version` (workspace root or crate) | `v<version>` |
| python | `pyproject.toml` `version` | `v<version>` |
| go / no version file | **git tag only** — the tag IS the version | `v<version>`, required |

A repo with no `package.json` is not a repo that cannot be released. Resolve the version source
from the table before declaring a blocker.

## Routing

| Argument | Mode |
|----------|------|
| (empty) | interactive — quality gates (test + review) then auto |
| `auto` | auto — squash + bump + push, no gates |
| `status` | status — show commits since last release |
| `dry-run` | dry-run — preview plan |
| `squash` | squash only |
| `patch` / `minor` / `major` | manual bump (skip bump confirmation) |

## AskUserQuestion Dark-Theme Rule

Output ALL context as markdown BEFORE calling AskUserQuestion. The `question` field is invisible on dark terminals — put key info in `header` and option `label`/`description` instead.

---

## Step 0: Parallel Discover (single Bash call)

Always start here. Run all read-only probes in parallel. Reuse results downstream — never re-run `detect`/`diff-report`/`git log` for the same SHA.

```bash
# Single Bash invocation; all commands independent.
{
  echo "=== branch ==="; git rev-parse --abbrev-ref HEAD
  echo "=== status ==="; git status --short
  echo "=== ahead ==="; git log --oneline @{u}..HEAD 2>/dev/null || echo "(no upstream)"
  echo "=== last-tag ==="; git describe --tags --abbrev=0 2>/dev/null || echo "(none)"
  echo "=== mode-signal ==="; ls .claude-plugin/marketplace.json 2>/dev/null && echo "marketplace" || echo "standalone"
  echo "=== version-source ==="; ls package.json Cargo.toml pyproject.toml VERSION 2>/dev/null || echo "(git-tag only)"
  # Does CI fire on a TAG? If so, a pushed commit without a tag ships nothing.
  echo "=== ci-tag-trigger ==="; grep -rlE '^\s*tags:' .github/workflows/ 2>/dev/null || echo "(none)"
  # Step 4.5 input: does this repo already publish GitHub releases? Errors stay visible.
  echo "=== gh-releases ==="; gh release list --limit 1 2>&1 || echo "(gh failed — see above)"
  echo "=== detect ==="; xm build release detect 2>/dev/null || echo "(plain-git mode — xm build unavailable)"
  echo "=== diff-report ==="; xm build release diff-report 2>/dev/null || true
  echo "=== diff-stat ==="; git diff --stat HEAD~5..HEAD 2>/dev/null
} 2>&1
```

If no changes → "✅ 릴리스할 변경사항이 없습니다." Exit.

---

## Step 1: Plan + Conditional Gate

**Default behavior: proceed.** Invoking `/xm:ship` is implicit consent to ship. Show the plan as markdown, then **execute immediately unless a blocker is detected**.

Markdown preview (always shown) must include:
- Squash strategy (grouped vs single vs keep) with file→group mapping
- Bump type (patch/minor/major) with rationale from detect
- Drafted commit message, changelog entry, and release notes (from `xm:write`, below)
- Push target (`origin/<branch>`)
- GitHub release: will be created? (yes/no with the reason from the rule in Step 4.5)
- README update needed? (yes/no with reason)

### Release documents (xm:write)

Do not write the commit message, changelog entry, or release notes yourself. After the bump type
is decided, invoke the `xm:write` skill once with the Skill tool, requesting only the documents
this release needs:

```
Skill: xm:write
args: commit [changelog] [release] --for ship --range <last-tag-or-base>..HEAD --version <versions>
```

- `<versions>` — standalone: the new version (`1.5.0`). Marketplace: every bumped plugin as
  `name@version`, comma-separated (`x-build@3.13.1,xm@2.27.4`).

- `changelog` — only when `CHANGELOG.md` exists at the repo root.
- `release` — only when Step 4.5 will create a GitHub release.
- `--for ship` makes xm:write return text only: no questions, no file writes, and only read-only `gh` (`list` / `view`).

Show the returned text in the plan preview and reuse it verbatim in Steps 3.5, 4, and 4.5.

### Blocker Conditions (only these halt for AskUserQuestion)

| Blocker | Why it halts | Question |
|---------|--------------|----------|
| Bump type ambiguous (signals split between patch+minor or minor+major) | Wrong bump = wrong release semver | "1) patch  2) minor  3) major" |
| Breaking change detected (removed export, deleted command, signature change) | Major bump is irreversible after publish | "1) major  2) 변경 재검토" |
| Current branch is `main` or `master` | Direct push to main is rare and risky | "1) main에 push  2) feature 브랜치로 이동  3) 중단" |
| Pushed commits would be squashed (squash range crosses `@{u}`) | Force-push required, history rewrite | "1) 로컬만 squash  2) squash 생략  3) 중단" |
| Test gate failed (only when explicitly requested) | Shipping broken code | "1) 무시하고 계속  2) 중단" |
| Review verdict = Block (only when explicitly requested) | Critical findings | exit (no question — Block means block) |
| Working tree contains files outside change scope | Unintended WIP would be shipped | "1) 모두 포함  2) 의도한 파일만  3) 중단" |
| Version source unresolvable (no `package.json` / `Cargo.toml` / `pyproject.toml` / tag) | Bump 대상 미상 | "1) 버전 파일 지정  2) 태그로만 릴리스  3) 중단" |
| CI triggers on tags but the plan has no tag | 커밋만 푸시하면 릴리스 워크플로가 아예 안 돎 | "1) 태그 생성 후 푸시  2) 태그 없이 커밋만  3) 중단" |

### No Blocker → Proceed Silently

If none of the above apply, skip AskUserQuestion entirely. Print the plan, then immediately run Steps 2-5. Do **not** ask "진행할까요?" — the user already invoked /xm:ship.

Skip the entire gate (including blocker checks for test/review) in `auto` mode.

### Optional pre-gate quality checks (interactive only, opt-in)

If user explicitly requested test/review gates in their prompt:

```bash
xm build release test [--command "bun test"]   # only if requested
```

For review gate, invoke x-review with refs already collected in Step 0:
`/xm:review diff $LAST_TAG..HEAD --preset quick`

LGTM → proceed. Request Changes / Block → ask user before continuing.

### README / docs prose audit (always runs when README changes are staged)

When the plan says "README update needed? yes" or any `README*.md` / `docs/*.md` is staged for this release, run a one-shot prose audit before commit:

```bash
/xm:humanize audit README.md README.ko.md   # detect-only, no rewrite
```

Surface findings in the plan preview (pattern count + top 3 issues). Do NOT auto-rewrite — show the user and let them decide. This is the only allowed humanize call in the release flow; runtime/agent paths never invoke humanize automatically.

---

## Step 2: Squash (if planned)

**Default is `keep`.** Squash only when the history actually needs it — WIP markers (`wip`, `tmp`,
`fixup!`, `squash!`, `.`, `asdf`), or several commits that are obviously one unit split by mistake.
A history of atomic, conventional commits (`fix(x): …`, `feat(y): …`) is the OUTPUT of careful work;
flattening it destroys the bisect/blame trail the author just built. When in doubt, keep — the user
can always ask for a squash, but cannot un-squash after a push.

| History | Strategy |
|---------|----------|
| WIP markers / same-scope dupes | squash (grouped, one commit per scope) |
| Atomic conventional commits | **keep** — do not squash |
| Mixed | squash only the WIP run; keep the atomic ones |

For grouped squash:
```bash
xm build release squash --since <ref>
# Then re-commit in groups (LLM stages files per group)
```

For single squash:
```bash
xm build release squash
```

Plain-git: see fallback section.

**Verification**: `git diff $PRE_SQUASH HEAD` must be empty. If not, rollback.

---

## Step 3: Bump

| Mode | Command |
|------|---------|
| marketplace | `xm build release bump --<type> --plugins <list>` |
| standalone (with CLI) | `xm build release bump --<type> --standalone` |
| plain-git | edit `package.json`/`VERSION` directly |

Bump type rules:

| Change type | Bump |
|-------------|------|
| Bug fix, internal refactor | patch |
| New command/feature/export | minor |
| Breaking change (removed export) | major |
| Explicit in `$ARGUMENTS` | use that |

---

## Step 3.5: Changelog

Skip when there is no `CHANGELOG.md` at the repo root.

Edit the file directly (the bump already touched the tree; this rides the same commit):

1. Put the `xm:write` changelog entries under a new version section directly below
   `## [Unreleased]`, merged with whatever already sat under `[Unreleased]`. Copy the heading
   form from the latest existing version section, e.g. `## [<version>] - <YYYY-MM-DD>`.
   The version is the project version (standalone) or the new `xm` core version (marketplace —
   sections group the plugin bumps of one marketplace release). If a marketplace release does
   not bump `xm`, keep the entries under `[Unreleased]` and say so in the Step 5 output.
2. Leave `## [Unreleased]` in place and empty.

Tracked-file staging in Step 4 (`git add -u`, or the plain-git file list) picks it up. In
plain-git mode, add `CHANGELOG.md` to the staged files explicitly.

---

## Step 4: Commit + Tag + Push (single call)

Inline the README check here — no separate step. If plan said README update needed, stage README changes alongside the version bump.

```bash
xm build release commit --msg "release: ..." --tag v<version> --push
```

`--tag` creates an ANNOTATED tag and `--push` sends it with `--follow-tags`. Omit `--tag` only for
marketplace releases (versioned by `plugin.json`, no tag convention).

**A tag-versioned project is not released until the tag is pushed.** Release workflows keyed on
`on: push: tags: v*` (Step 0's `ci-tag-trigger`) never fire from a branch push — the commit lands,
CI stays silent, and the ship *looks* successful. If Step 0 found a tag trigger, or the version
source is git-tag-only, `--tag` is mandatory.

Plain-git:
```bash
# Stage the version file + the files this release actually touched — NEVER `git add -A`:
# .xm/ (panel runs, review artifacts, traces) and unrelated WIP would ride along into the release.
git add <version-file> <files-from-plan> && git commit -m "release: ..." \
  && git tag -a v<version> -m "release: v<version>" \
  && git push --follow-tags origin "$(git branch --show-current)"
```

Commit message: the `### commit` text `xm:write` returned in Step 1, verbatim. Its format and
rules (what changed, never the session's reasoning trail) live in `xm:write`.

---

## Step 4.5: GitHub Release

Create one only when ALL hold:
- a tag was created and pushed in Step 4 (marketplace releases without a tag get none)
- Step 0's `gh-releases` probe printed a release row — the repo already publishes GitHub
  releases and `gh` is authenticated. An error there means skip, not fail.

Otherwise skip, and state which condition failed in the Step 5 output.

Use the literal tag name Step 4 passed to `--tag` (or to `git tag -a`). Do not rediscover it
with `git tag --points-at HEAD`: a commit can carry several tags (monorepos tag each package),
and an empty result would still pass a `&&` chain. The `### release` block from `xm:write`
starts with `Title: <title>`; pass that line's value as the title and the rest as the notes.

```bash
TAG='<tag created in Step 4>'
git tag --points-at HEAD | grep -qxF "$TAG" || { echo "tag $TAG is not on HEAD" >&2; exit 1; }
TITLE=$(cat <<'EOF'
<value of the Title: line>
EOF
) && NOTES=$(mktemp) && cat > "$NOTES" <<'EOF'
<release notes without the Title: line>
EOF
gh release create "$TAG" --verify-tag --title "$TITLE" --notes-file "$NOTES"
```

`--verify-tag` aborts if the tag is not on the remote. If `gh release create` fails, the push
already landed: do not roll anything back. Report the error, print the notes, and give the exact
command to re-run with the literal tag name.

---

## Step 5: Trace (background) + Output (immediate)

Trace is fire-and-forget. Don't block the success message.

```bash
# run_in_background: true
xm build release trace --from {old} --to {new} --bump {type} \
  --test-passed {true|false} --review-verdict {LGTM|null}
```

Immediately print:
```
🚀 Shipped!

  Version: {old} → {new}
  Commit: {hash}
  Push: origin/{branch} ✅
  Release: {url} | skipped ({failed condition}) | ❌ {error}
```

---

## Mode: status

Run only the `=== detect ===` and `=== ahead ===` portions of Step 0. Display readable summary.

## Mode: dry-run

Run full Step 0, build the markdown plan from Step 1 (including the `xm:write` drafts), **do not** call AskUserQuestion, **do not** execute Steps 2-5.

## Mode: squash

Step 0 + Step 2 only. No bump, no push.

---

## Plain-Git Fallback (no x-build CLI available)

When mode detection (see CLI Invocation) landed on plain-git, replace CLI calls with:

| Step | Plain-git equivalent |
|------|---------------------|
| detect | `git log $(git describe --tags --abbrev=0)..HEAD --oneline` |
| diff-report | `git diff --stat $(git describe --tags --abbrev=0)..HEAD` |
| squash (single) | `git reset --soft $(git describe --tags --abbrev=0)` then `git commit` |
| squash (grouped) | `git reset --soft <ref>` then stage+commit per group |
| bump | edit the version source from the table above (`package.json` / `Cargo.toml` / `pyproject.toml`) |
| commit + push | `git add <version-file> <planned-files>` → `git commit` → `git tag -a v<ver>` → `git push --follow-tags` |
| trace | skip (no-op) |

Projects with no version file are versioned BY THE TAG — bump means `git tag -a v<next>`, not "skip
bump". Never `git add -A`: it sweeps `.xm/` artifacts and unrelated WIP into the release commit.

---

## Safety Rules

- **Squash local-only** — never squash pushed commits. Force push should not be needed.
- **No changes = no release**
- **Squash verification** — `git diff $PRE_SQUASH HEAD` must be empty
- **Not on main/develop = warn** (unless feature branch release intentional)
- **Rollback on failure** — save pre-squash HEAD, restore with `git reset --hard`
- **Push failure = keep commit** — instruct user to push manually
- **Reuse Step 0 results** — never re-run `detect`/`diff-report`/`git log` for the same SHA within one ship run

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "patch bump is safe, I'll use patch" | patch implies no behavior change. If behavior changed, bump minor. |
| "I'll squash later" | Squash before push or not at all. |
| "The user will confirm if they care" | Don't guess on irreversible operations. Ask before push. |
| "standalone project — can't ship without the CLI" | The Plain-Git Fallback delivers the same result. A missing CLI is not a blocker. |
| "re-running detect is safer" | Same SHA = same result. Reuse the Step 0 output; re-running just wastes a turn. |
| "confirming each step is safer" | Five step-confirms = five wasted turns. One plan preview + a single approval is safer — the full impact is visible at once. |
| "guess the CLI path and try it" | `xm build …` resolves the path internally. Guessing then failing is the worst pattern. |
| "I'll define `XMB` once and reuse it across steps" | The Bash tool starts a fresh shell every call — the variable is gone by the next step, and `XMB="node …"` breaks in zsh anyway (single-token expansion). Type `xm build …` each time. |
| "README update is a separate step" | Same transaction as the commit. Inline it in Step 4. |
| "`.xm/` is here, so this is a marketplace repo" | `.xm/` is the data dir every xm tool writes. Only `.claude-plugin/marketplace.json` means marketplace. |
| "no package.json → nothing to bump" | Check Cargo.toml / pyproject.toml / the tag. A version file is one of four possibilities, not a precondition. |
| "the commit is pushed, so it's released" | If CI triggers on `push: tags`, a branch push ships NOTHING. The tag is the release. |
| "squash makes the history cleaner" | Atomic conventional commits ARE the clean history. Squash WIP, keep the rest — you cannot un-squash after a push. |
| "`git add -A` is faster than listing files" | It commits `.xm/` artifacts and unrelated WIP into the release. Stage the plan's files. |
| "ship isn't done until I see trace results" | trace is for observability. Push success = ship done. Run trace in the background. |
| "ask for go-ahead every time, to be safe" | Invoking /xm:ship is the consent. Confirm only when a blocker fires — asking every time wastes the user's time and forces the same answer ("proceed"). |
| "the user might want to edit the commit message" | If they do, they will ask explicitly. Do not guess and prompt. |
| "I can write the commit message myself, it's one line" | Ship's documents come from one `xm:write` call so the commit, changelog, and release notes agree. Writing one inline breaks that and skips its evidence rules. |
| "create the GitHub release before pushing, it saves time" | The release points at a tag. Without the pushed tag `--verify-tag` fails, and without it `gh` creates the tag from the default branch's latest state — a release pointing at the wrong commit. |
| "this repo has no releases yet, I'll start them" | Starting GitHub releases is the maintainer's call. Create one only when the repo already publishes them. |

## Red Flags

- Entering Step 1 without Step 0 results → acting on missing information
- Running the same git command 2+ times → cached result not reused
- AskUserQuestion 3+ times (interactive mode) → decision gates scattered instead of batched
- Hardcoding the CLI path, or defining a `XMB` variable / shell helper to hold it → call `xm build …` directly; a fresh shell per Bash call discards both
- Waiting synchronously on trace → blocking on observability

## Verification

After ship:
- `git log -1 --format=%H` matches commit returned
- `git rev-parse @{u}` matches `git rev-parse HEAD` (push succeeded)
- Tag created AND pushed when the project is tag-versioned or CI triggers on tags:
  `git tag --points-at HEAD` is non-empty, and `git ls-remote --tags origin | grep <tag>` finds it.
  A local-only tag fires no workflow — that is a failed release, not a shipped one.
- GitHub release created when Step 4.5 applied: `gh release view '<tag created in Step 4>' --json tagName,name`
  returns that exact `tagName` and the title from `xm:write`. Never run it with an empty tag:
  `gh` then shows the latest release instead.
- `CHANGELOG.md` (when present) has the new version section and an empty `## [Unreleased]` in the release commit:
  `git show HEAD -- CHANGELOG.md`.
