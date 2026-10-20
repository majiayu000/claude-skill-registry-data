---
name: iru-pr-review
description: Review an already-open pull request's changes by id, on whichever platform hosts the repository (GitHub, Bitbucket, Azure DevOps, or TFS) and whatever language(s)/framework(s) are in play — both detected via the `iru-explore` skill and used throughout instead of assuming GitHub/`gh` or generic checklist advice. Optionally takes the linked GitHub issue id or Jira key as a second argument (skipping auto-detection); otherwise looks for a reference in the PR title/body (e.g. "Closes #N" or a bare Jira key) and fetches that ticket for context on intent. Runs the `iru-explore` skill (grounded in the linked ticket when there is one) to understand the codebase's current architecture, conventions, and detected tech stack before judging the diff, so convention/architecture-drift findings are checked against the actual best practices for that stack (e.g. hexagonal architecture/DDD layering for a backend service, MVC/MVVM for a UI layer, unidirectional data flow for SwiftUI/Jetpack Compose) rather than a one-size-fits-all standard. When the `code-review` skill is available, delegates the correctness/reuse/simplification/efficiency analysis to it (via its `--comment` flag) rather than duplicating that logic, and layers on its own checks for ticket-intent alignment and codebase-convention drift; if `code-review` isn't available, runs the full review itself. Drafts its own findings and — after explicit confirmation — posts them as inline review comments on the pull request for manual follow-up. Invoke as `/iru-pr-review <pr-id> [ticket-id]`. Use when the user wants an actual PR reviewed and commented on, not a description generated (`iru-pr-description`).
model: opus
---

# PR Review

Review a specific, already-open pull request and leave the findings as review comments on it — this skill never
edits code itself. It is grounded in this repository's actual architecture and conventions, learned fresh via the
`iru-explore` skill, plus the originating ticket's intent when the PR links one (a GitHub issue or a Jira ticket).
Where the generic `code-review` skill is available, this skill prefers delegating to it for
correctness/reuse/simplification/efficiency findings (it already knows how to post inline PR comments) rather than
reimplementing that analysis, and focuses its own review on what `code-review` has no way to know: whether the
change matches the linked ticket's intent and whether it follows this codebase's own conventions. It works the
same way regardless of which platform hosts the repository, using that platform's own tooling instead of assuming
GitHub/`gh`.

## Step 1 — Resolve the PR id (required) and ticket id (optional)

A ticket id is optional but a PR id is not — there is nothing to review without it. When a ticket id is given (or
later detected in Step 4), it may refer to either a GitHub issue or a Jira ticket — a bare number/`#N` is a GitHub
issue, a key like `PROJ-123` is Jira — and Step 4 fetches it accordingly: `gh`/GitHub MCP tools for a GitHub
issue, or connected Jira MCP tools (`ToolSearch` "jira") for a Jira ticket.

- **PR id argument provided** (e.g. `/iru-pr-review 17`, or `/iru-pr-review 17 42` / `/iru-pr-review 17 PROJ-123` to also pass
  the ticket id explicitly): use it, go to Step 2. If a second argument is present, treat it as the linked ticket
  id and use it directly in Step 4 — skip that step's own detection since the caller (e.g. the `iru-issue` skill,
  which knows exactly which ticket a PR it just opened closes) already knows the relationship with certainty.
- **No PR id provided**: ask the user via `AskUserQuestion` for the pull request number. If they decline or give
  none, stop here entirely and tell them this skill requires a PR id (e.g. `/iru-pr-review 17`).

## Step 2 — Detect the repository host and available tooling

Determine which platform hosts this repository, so the right tool is used throughout instead of assuming
GitHub/`gh`:

- If `iru-explore` already ran earlier in this conversation, reuse the `Repository host: ...` line from its Tech
  stack report rather than re-detecting.
- Otherwise, detect it directly — the same way `iru-explore`'s own Step 2 does: get the remote URL (`git remote
  get-url origin`, falling back to `git remote -v` or whichever remote the current branch tracks) and match it
  against known patterns:
  - `github.com` (or a GitHub Enterprise Server domain) → **GitHub**. Tooling: the `gh` CLI, or GitHub MCP tools
    (`ToolSearch` "github").
  - `bitbucket.org` (cloud), or a self-hosted domain with a `/scm/<project>/<repo>.git` path (Bitbucket
    Server/Data Center) → **Bitbucket**. Tooling: search for Bitbucket MCP tools first (`ToolSearch` "bitbucket"),
    otherwise the Bitbucket REST API.
  - `dev.azure.com` or `<org>.visualstudio.com` → **Azure DevOps (cloud)**. Tooling: `az repos` (the Azure CLI
    with the `azure-devops` extension) if installed, or Azure DevOps MCP tools (`ToolSearch` "azure devops").
  - A self-hosted domain with a `/tfs/` path segment, or bare `_git` in the path without a `dev.azure.com`/
    `visualstudio.com` domain → **Azure DevOps Server / TFS**. Same tooling family as Azure DevOps, but confirm
    the collection URL and API version before assuming parity.
  - If the URL doesn't clearly match any of these, ask the user (`AskUserQuestion`) which platform it is rather
    than guessing.
- If there's no remote configured at all, tell the user a PR can't be reviewed without a hosted remote, and stop.

Record the detected host — every later step's "use the host's tool" instruction refers back to this.

## Step 3 — Fetch the pull request

Use the tool matching the host detected in Step 2 to get the PR's metadata, diff, and any comments/reviews
already left on it:

- **GitHub**:
  ```bash
  gh repo view --json owner,name -q '.owner.login + "/" + .name'
  gh pr view <pr-id> --json number,title,body,url,state,baseRefName,headRefName,headRefOid,additions,deletions,files,commits
  gh pr diff <pr-id>
  gh api repos/<owner>/<repo>/pulls/<pr-id>/comments
  ```
  If `gh` is not installed/authenticated, search for GitHub MCP tools instead (`ToolSearch` "github pull
  request") and use those to fetch the same information.
- **Bitbucket**: Bitbucket MCP tools if connected, otherwise the REST API — `GET
  /2.0/repositories/<workspace>/<repo>/pullrequests/<pr-id>` for metadata, `GET .../diff` for the diff, and `GET
  .../comments` for existing comments (Cloud paths shown; substitute the Server/Data Center equivalents on a
  self-hosted instance).
- **Azure DevOps / TFS**: `az repos pr show --id <pr-id>` for metadata, the pull request iterations/changes REST
  endpoint (or `az repos pr show`'s linked commits) for the diff, and the pull request threads REST endpoint for
  existing comments — or Azure DevOps MCP tools if connected.

If the PR can't be fetched by any means, tell the user and stop.

If the PR is already merged or closed, tell the user and ask (`AskUserQuestion`) whether to continue anyway (e.g.
a post-hoc review) or stop — don't assume either way.

Read the full diff, not just the file list or a stat summary — the review must be grounded in the actual changes.
Note the existing comments/reviews so Step 7 doesn't re-raise points already made.

## Step 4 — Find a linked ticket, if any

If Step 1 already received an explicit ticket id, skip detection and use it directly — it may be either a GitHub
issue ID or a Jira key; if its type isn't already obvious from context, detect it the same way `iru-explore`'s Step 1
does (a Jira key pattern like `PROJ-123` vs. a bare number/`#N`).

Otherwise, look for a reference in the PR title or body:
- GitHub issue patterns: `Closes #N`, `Fixes #N`, `Resolves #N`, or a bare `#N` mention.
- Jira patterns: a bare Jira key mention (e.g. `PROJ-123`) anywhere in the title/body — teams commonly include
  these via commit-message/PR conventions or smart-commit links.

Either way, once a ticket id is known, fetch it — but unlike `iru-explore`/`iru-issue` (which ground a broader
exploration or file a new ticket and so want the full comment thread), Step 7 below only checks the diff against
the ticket's stated intent, so there's no need to pull the comment history by default:
- **GitHub issue**: `gh issue view <ticket-id> --json number,title,body,labels,state,url` (or GitHub MCP tools if
  `gh` is unavailable). Only add `comments` to the fetch if the title/body alone leaves genuine ambiguity about
  scope or acceptance criteria that a comment thread would likely resolve.
- **Jira ticket**: search for connected Jira MCP tools (`ToolSearch` "jira issue" or "jira ticket") and fetch its
  summary/description/labels/status — same reasoning, skip comments unless the description alone is ambiguous.

If no reference is found/provided, or the ticket can't be fetched, continue without one — this skill works fine
on a PR with no linked ticket, it just loses that piece of intent context.

## Step 5 — Explore the codebase

The review must be grounded in how this codebase is actually structured, not just the diff in isolation.

- **Check first**: if this conversation already explored the codebase (or this same ticket) recently, reuse that
  instead of repeating it.
- **Otherwise**, invoke the `iru-explore` skill: `Skill({skill: "iru-explore", args: "<ticket-id>"})` if Step 4 found a
  ticket, or `Skill({skill: "iru-explore"})` with no argument otherwise. Wait for it to finish before continuing.

`iru-explore` detects and reports (in its "Tech stack" summary) the repository host (used in Step 2 above), plus the
programming language(s) and framework(s) actually in play — per module, if the repo has more than one stack. Use
that detected language/framework list to ground Step 7's convention check in the right architectural best
practices for the stack at hand, rather than a generic checklist — e.g. hexagonal architecture/ports-and-adapters
or DDD layering conventions for a Java/Spring or .NET/ASP.NET Core backend, MVC or MVVM for a web/desktop UI
layer, MVVM/unidirectional data flow for SwiftUI or Jetpack Compose, or whatever architectural style this
specific codebase already follows for its detected stack.

From the exploration, note in particular: the architectural patterns and abstractions the changed files should be
consistent with, any contributor conventions documented in `CLAUDE.md`/`README`/`AGENTS.md` (naming, error
handling, validation, documentation requirements, etc.), and the language/tooling in play (so Step 7 can apply
the right idioms and check for the right lint/static-analysis config — e.g. Checkstyle/PMD/SpotBugs rules for
Java, ESLint / Prettier / Biome (`eslint.config.*`, `.prettierrc*`, `biome.json`) plus `tsconfig.json` (strictness
flags) for JS/TS, Detekt / ktlint / Android Lint (`detekt.yml`, `.editorconfig` ktlint rules, `lint.xml`,
`lintOptions`/`lint {}` in Gradle) for Kotlin/Android, PHPStan / Psalm / PHPCS / Pint / PHP-CS-Fixer
(`phpstan.neon*`, `psalm.xml`, `phpcs.xml*`, `pint.json`, `.php-cs-fixer.dist.php`) for PHP, Ruff / mypy
(`[tool.ruff]`/`[tool.mypy]` in `pyproject.toml`, `ruff.toml`/`.ruff.toml`, `mypy.ini`/`setup.cfg`, the
`[tool.django-stubs]`/pydantic mypy plugins) plus `[tool.pytest.ini_options]` markers for Python, SwiftLint /
swift-format (`.swiftlint.yml`, `.swift-format`) for Swift, clippy / rustfmt / cargo-deny (`[lints]` in
`Cargo.toml`, `clippy.toml`, `rustfmt.toml`, `deny.toml`) for Rust, golangci-lint (`.golangci.yml`, v1 vs v2 config) for
Go, and so on — and for a command-line tool, whether the change keeps its stdout/stderr, `--json` schema and exit-code
contract intact — read any such config found rather than assuming defaults).

## Step 6 — Delegate to the `code-review` skill when available

Check the currently available skills (listed in this session) for `code-review`. It already knows how to find
correctness bugs and reuse/simplification/efficiency cleanups and how to post them as inline PR comments — don't
reimplement that analysis if it's available.

- **If `code-review` is not available**: skip this step entirely and cover correctness, security, test coverage,
  and simplification/reuse/efficiency yourself in Step 7 alongside the ticket-intent and convention checks.
- **If `code-review` is available**: it reviews "the current diff", so it needs the PR's changes checked out
  locally first:
  1. Capture the current branch (`git branch --show-current`) so it can be restored afterward, and run `git
     status` first per this repository's safety conventions — if there are uncommitted changes, stash them
     (`git stash push -u`) rather than checking out over them.
  2. Check out the PR's source branch, using the tool matching the host detected in Step 2:
     - **GitHub**: `gh pr checkout <pr-id>`.
     - **Bitbucket / Azure DevOps / TFS**: no equivalent single-command checkout — use the source branch name
       already captured in Step 3's metadata directly: `git fetch origin <source-branch-name> && git checkout
       <source-branch-name>`.
  3. Tell the user this skill is about to invoke `code-review` with `--comment`, which posts its findings to the
     PR directly and immediately (it does not stop for a separate confirmation) — get explicit confirmation
     before proceeding, since Step 8's confirmation gate only covers this skill's own findings, not
     `code-review`'s.
  4. Invoke it: `Skill({skill: "code-review", args: "high --comment"})` (use `high` effort for a thorough pass;
     drop to `medium` if the user wants a lighter review). Wait for it to finish.
  5. Restore the original branch (`git checkout <original-branch>`, and `git stash pop` if a stash was created in
     step 1).
- Note what `code-review` found (or that it wasn't available) for Step 9's report.

## Step 7 — Review for ticket intent and convention drift

This step always runs, regardless of whether Step 6 delegated — `code-review` has no visibility into the linked
ticket or this repository's specific conventions, so this is this skill's own irreplaceable contribution. If Step
6 was skipped (no `code-review` available), also cover correctness, security, and test coverage here, per the
full list below.

For every changed hunk in the Step 3 diff, evaluate it against the linked ticket's intent (if any, from Step 4)
and the codebase's own architecture and conventions (from Step 5). Look for:

1. **Ticket-intent mismatch** — the change doesn't actually satisfy what the linked ticket asked for, addresses
   only part of it, or introduces behavior the ticket didn't request.
2. **Convention/architecture drift** — code that doesn't follow the patterns Step 5 identified (e.g. bypassing an
   existing abstraction, inconsistent validation/error-handling style, missing required documentation like
   Javadoc where this repo's conventions mandate it), *and* code that violates the established architectural
   style for the language/framework Step 5 detected — e.g. business logic leaking into a controller/adapter in a
   hexagonal-architecture backend, a domain entity reaching into infrastructure in a DDD codebase, a
   view/ViewModel violating MVC/MVVM separation (state mutation in the view, business logic in the view layer),
   or a Compose/SwiftUI screen breaking unidirectional data flow. Judge this against how the codebase *actually*
   applies that pattern (from Step 5), not an idealized textbook version of it.
3. **Stack-specific pitfalls** — framework traps a generic correctness pass tends to miss, for whichever stacks
   Step 5 detected (only the ones actually in play), e.g.:
   - **Kotlin + Spring Boot**: Spring/JPA classes relying on the `kotlin-spring` (all-open) and `kotlin-jpa`
     (no-arg) compiler plugins — a final `@Configuration`/`@Transactional` class or an entity without them breaks
     proxies/lazy loading silently; `data class` JPA entities (`equals`/`hashCode` over mutable, generated-id
     state); `@Transactional` on `suspend fun` without a reactive transaction manager, or a coroutine launched
     (`GlobalScope.launch`, a new scope) inside a transaction, losing the transaction context; `block()`/blocking
     I/O on an event-loop thread; self-invocation bypassing `@Transactional`/`@Cacheable`.
   - **Quarkus**: build-time CDI rules — beans looked up dynamically without `@Unremovable`, private injection
     points (reflection, warnings), beans lacking a bean-defining annotation; `@Transactional` on the
     entity/repository instead of the calling service/resource, or writes outside a transaction; blocking calls
     in a `Uni`/`Multi` pipeline or a non-`@Blocking` reactive endpoint (event loop); reflection-based code
     (Jackson on non-registered classes, `Class.forName`) without `@RegisterForReflection` when native builds are
     used; Kotlin classes missing the all-open/no-arg configuration Quarkus doesn't add automatically.
   - **PHP**: missing `declare(strict_types=1);` where the codebase uses it; mass assignment (`$guarded = []`,
     `$request->all()` into `create()`/`fill()` instead of validated/`safe()` data); N+1 queries (missing
     `with()`/eager loading in loops); unescaped output (`{!! !!}`, `echo $var`) and raw SQL built from input.
     **WordPress**: missing nonce verification (`check_admin_referer`/`wp_verify_nonce`) and capability checks
     (`current_user_can`) on state-changing handlers, AJAX/REST endpoints (`permission_callback`), unprepared
     `$wpdb` queries (no `$wpdb->prepare`), input not sanitized (`sanitize_*`, `wp_unslash`) and output not
     escaped late (`esc_html`/`esc_attr`/`esc_url`/`wp_kses`), unprefixed globals/functions. **PrestaShop**:
     hooks registered in `install()` without matching `registerHook`/uninstall cleanup, `Tools::getValue()` input
     used without validation/casting (`(int)`, `Validate::is*`), SQL through `Db::getInstance()` without `pSQL()`/
     `bqSQL()`/`(int)` escaping, missing `$this->trans()`/admin token checks.
   - **NestJS**: DTOs imported with `import type` (erases the class — `ValidationPipe` silently skips
     validation); global pipes/guards/interceptors/filters registered via `app.useGlobal*()` in `main.ts` instead
     of `APP_PIPE`/`APP_GUARD`/... providers (not applied in tests, not overridable), or registered from more than
     one module; `REQUEST`-scoped providers bubbling scope up the injection chain, or per-request state kept on a
     singleton; providers not exported/imported where used; ESM relative imports with the `.js` extension
     "fixed" away.
   - **FastAPI**: blocking I/O (sync DB driver, `requests`, `time.sleep`) inside an `async def` path operation or
     dependency (use `def` to run it in the threadpool, or an async client); request/response bodies as raw
     `dict` instead of Pydantic models, or a `response_model`/return type that leaks fields (the table model
     instead of `XPublic`, password hashes); an `AsyncSession` shared across requests/tasks instead of a
     per-request `Depends` yield dependency; `@app.on_event` instead of `lifespan`; settings read from
     `os.environ` ad hoc instead of the `pydantic-settings` dependency; tests hitting real services instead of
     `app.dependency_overrides`; an Alembic migration missing for a model change.
   - **Django**: N+1 queries (missing `select_related`/`prefetch_related`, no `assertNumQueries`); a model change
     without its migration (or a hand-edited applied one); multi-write services without `@transaction.atomic`,
     or side effects (emails, tasks) not deferred with `transaction.on_commit`; business logic in signals,
     views or serializers instead of services; raw SQL / `.extra()` / `RawSQL` built from input; DRF viewsets
     without explicit `permission_classes`/queryset scoping to the requesting user, or serializers with
     `fields = "__all__"`; settings with a default `SECRET_KEY`/`DEBUG = True` outside local/test; references
     to `auth.User` instead of `settings.AUTH_USER_MODEL`/`get_user_model()`.
   - **Next.js**: server/client boundary — `'use client'` placed too high, hooks or browser APIs in Server
     Components, non-serializable props crossing the boundary, server-only modules (secrets, DB) importable from
     client code (no `server-only`); Server Actions without authentication/authorization and input validation
     inside the action itself (they are public POST endpoints); caching semantics that don't match the project's
     Next major version / `cacheComponents` setting (e.g. assuming `fetch` is cached by default on 15+, sync
     `params`/`cookies()` on 15+/16, one-argument `revalidateTag` on 16, runtime data read inside `'use cache'`);
     secrets exposed through `NEXT_PUBLIC_*` env vars.

   - **User interfaces (any stack — web, Android, Apple, React Native, KMP, Windows, terminal UIs)**: a screen or
     component built as one monolith instead of composed components; subclassing a screen/component to tweak it
     instead of composing; presentational components that fetch data, navigate or read global state; events
     leaking raw framework event objects, or two-way binding on collections/domain objects; a data-driven or long
     list, grid, carousel, pop-up list or tab strip built eagerly instead of on the platform's virtualizing/
     recycling container (`RecyclerView`/`ListAdapter`+`DiffUtil`, `LazyColumn` with `key`, SwiftUI `List`,
     `UICollectionView` diffable data source, `FlatList` with `keyExtractor`, a web virtualizer, a WPF virtualizing
     `ListView`), index keys, or selection state kept in recycled item views; hard-coded user-visible strings or
     left/right instead of start/end; missing accessible names/alt text, contrast or touch-target problems; a new
     or changed screen/component without UI tests covering its states, events, left-to-right and right-to-left,
     light and dark, its `.ui-screenshots/` captures and the accessibility check at the repository's
     `.ui-quality.yml` level; a UI change that leaves the Antora `ui/` pages and `images/ui/` screenshots stale
     (suggest `/iru-update-docs`).

If Step 6 didn't run, also look for, using general best practices for the language in use:

4. **Correctness bugs** — logic errors, edge cases the code doesn't handle, incorrect assumptions, concurrency
   issues, resource leaks.
5. **Security issues** — anything resembling the OWASP top 10 (injection, unsafe deserialization, missing input
   validation at boundaries, secrets in code, etc.) relevant to the language/framework in play.
6. **Test coverage** — new/changed behavior without a corresponding test, or tests that don't actually exercise
   the edge cases the change introduces.
7. **Simplification/reuse/efficiency** — real, non-cosmetic opportunities: duplicated logic that already exists
   elsewhere in the codebase, unnecessary complexity, obvious inefficiencies. Skip nitpicks and pure style
   preferences that aren't backed by a documented convention.

For each finding, record: the file path, the line number *as it appears in the new version of the file in this
diff* (needed for inline comments in Step 9 — pick a line that is actually part of a diff hunk), a one-sentence
summary of the problem, and a concrete suggested fix. Skip anything that duplicates a point already made in the
existing comments/reviews gathered in Step 3, or that `code-review` already posted in Step 6.

If the diff is large, it's fine to work through it file by file rather than holding the whole thing in view at
once — but every changed file must be considered, not just a sample.

## Step 8 — Draft the review and confirm before posting

Posting comments on a pull request is a visible, shared-state action — never do it without explicit confirmation.

1. Present the drafted findings to the user: grouped by file, each with its line, summary, and suggested fix, plus
   a short overall summary sentence or two for the review body.
2. Ask the user (`AskUserQuestion`) whether to post these as review comments on the PR, and if so, confirm the
   scope (e.g. they may want to drop some findings first).
3. If they decline: stop here — the drafted findings are the deliverable, available for them to act on manually.

## Step 9 — Post the review

Only reached after explicit confirmation. Use plain comments only — never use any host's "approve" or "request
changes"/vote capability here; these are suggestions for the user to judge, not a verdict. The exact mechanism
depends on the host detected in Step 2:

- **GitHub**: bundle every confirmed finding into a single pull request review (one review event, multiple inline
  comments) rather than posting each as a separate top-level comment — this mirrors how a human reviewer leaves a
  batch of inline notes plus a summary, and avoids spamming notifications. Write the payload to a file in the
  scratchpad directory, e.g.:
  ```json
  {
    "commit_id": "<headRefOid from Step 3>",
    "event": "COMMENT",
    "body": "<one- or two-sentence overall summary>",
    "comments": [
      { "path": "<file>", "line": <line>, "side": "RIGHT", "body": "<summary + suggested fix>" }
    ]
  }
  ```
  Then submit it:
  ```bash
  gh api repos/<owner>/<repo>/pulls/<pr-id>/reviews --method POST --input <path-to-json-file>
  ```
  Always use `event: "COMMENT"` — never `REQUEST_CHANGES` or `APPROVE`.
- **Bitbucket**: there is no single batched "review" object like GitHub's — post one inline comment per finding
  (via Bitbucket MCP tools if connected, otherwise `POST
  /2.0/repositories/<workspace>/<repo>/pullrequests/<pr-id>/comments` per comment, each with an `inline: {path,
  to: <line>}` block and the summary + fix as `content.raw`), plus one additional top-level comment (no `inline`
  field) carrying the overall summary.
- **Azure DevOps / TFS**: post one comment thread per finding via the pull request threads REST endpoint (`POST
  .../pullrequests/<pr-id>/threads`, each with a `threadContext` naming the file path and the right-side line
  range, and a `comments` array with the summary + fix), plus one additional thread with no `threadContext` for
  the overall summary — or Azure DevOps MCP tools if connected.

If posting on a specific line fails because the host requires it to be part of the diff (GitHub, Bitbucket, and
Azure DevOps all enforce this for inline comments), retry that specific comment on the nearest valid line within
the same hunk, or fall back to including it in the overall summary text with an explicit `file:line` reference
rather than dropping it silently.

## Step 10 — Report

Summarize for the user: the PR reviewed and its linked ticket (if any); whether `code-review` was available and
delegated to (and what it found), or that this skill covered the full scope itself; how many of its own findings
were raised and in which files; and the outcome — a link to the posted review, or, if they declined to post, a
reminder that the draft from Step 8 is the deliverable. Obtain the link via whichever host tooling was used in
Step 9: `gh pr view <pr-id> --json url -q .url` for GitHub; the PR's web link already captured in Step 3's
metadata for Bitbucket; or `az repos pr show --id <pr-id> --query "_links.web.href" -o tsv` (or the URL already
captured in Step 3) for Azure DevOps/TFS.
