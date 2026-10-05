---
name: code-quality
description: >
  Use when improving or reviewing code quality, style, and dead-code hygiene —
  readability, naming, consistency with surrounding code, and removing unused
  code. Invoke whenever asked to "remove dead code", clean up, tidy, or
  de-duplicate, and load it as the standards behind any cleanup or review pass.
  Its core discipline is proving code is TRULY dead (no dynamic, reflective,
  cross-package, or convention-based use) before deleting anything. This is the
  knowledge/discipline skill — to actually RUN a review of the current diff use
  the /code-review command, and to apply reuse/simplification fixes use
  /simplify; pair either with the standards here.
---

# Code Quality

Goal: raise readability, consistency, and tidiness of the code, and remove dead
code — **without ever deleting something that is actually used.** When in doubt,
do not delete; flag it instead. A false-positive deletion (removing live code)
is far worse than leaving one dead function in place.

> **Who writes the code:** if implementation is delegated to another agent, this
> skill is the standard the reviewing agent holds the work to, not a licence to edit
> product code directly. A cleanup the reviewer wants goes to the implementer as a
> brief; the deletion bar below is what the returned diff is held to. (Fallback: if
> the implementer is unavailable, implement at the identical bar and flag it
> inline.) Who executes in this install: `LOCAL.md` beside this skill, when your
> copy keeps one — *Who writes the code*.

## Code quality & style

Match the code to its surroundings — the bar is "reads like the rest of this
file/module," not your personal preference. Naming, comment density, error
handling, and file layout all follow local idiom; don't introduce a style island.

- **Respect per-repo conventions over general taste.** A repo may, for example,
  ban comments entirely in some languages (extract a name instead), or keep
  framework decorators out of shared type libs. Read AGENTS.md, CLAUDE.md, and
  neighbouring code before imposing anything. (This install's standing conventions:
  `LOCAL.md` beside this skill, when your copy keeps one — *Per-repo conventions*.)
- **DRY with judgment — three strikes before a shared helper.** Two things that
  merely look alike today are not duplication.
- **No speculative construction in new code:** no abstractions for single-use
  code, no configurability or "flexibility" that wasn't requested, no error
  handling for scenarios that cannot occur. The refactor guidance below covers
  when structure earns its place; a first implementation defaults to none.
- **Clean up your own orphans — and only yours:** remove the imports, variables,
  and functions that YOUR change made unused. Pre-existing dead code stays in an
  unrelated diff — flag it for a separate pass under the deletion discipline
  below rather than bundling its removal.
- **Scope litmus: every changed line traces directly to the request.** A line you
  can't tie to the task belongs in a separate commit or not in the diff at all.
  (This and the two bullets above adapted 2026-08-27 from the Karpathy-derived
  `CLAUDE.md` template, `multica-ai/andrej-karpathy-skills`.)
- **Scope discipline:** a quality pass is behavior-preserving. If a cleanup
  changes behavior, surface it separately rather than smuggling it in.
- **Change sizing:** ~100 changed lines is good, ~300 acceptable for one logical
  change, ~1000 split it — stacked, by file group, horizontal (shared code first),
  or vertical slices. A ~1000-line *file* is itself an inspection signal. Whole-file
  deletions and automated refactors are exempt; there the reviewer checks intent.
- **Rule of 500:** a refactor touching >500 lines warrants a codemod, not hand edits.

### When a refactor is worth it

Propose the named move, not just the problem — and apply one test: **does this
reduce complexity or merely relocate it?** Count the concepts a reader must hold,
prefer the version where branches *disappear*, and prefer deleting an abstraction
to polishing it. Making a type boundary explicit so downstream branching vanishes
is usually the highest-value move available.

**The over-simplification traps** (these are the non-obvious half, and why
`/simplify` needs judgment rather than a rule):

- Inlining a helper that **named a concept** makes every call site worse.
- Merging two simple functions into one complex one is not simpler.
- Some abstractions exist for extensibility or testability — stripping them is a
  regression, not a cleanup. **Fewer lines ≠ simpler.**
- Litmus: would a new team member understand this faster than the original?

**Don't simplify** code you don't yet understand, code that is already clean,
performance-critical code where the simpler form is measurably slower, or a module
about to be rewritten.

## Dead code — the deletion discipline

"Dead code" = code that can never be reached or referenced through ANY path.
Apparently-dead is not dead. Before deleting, you must actively rule out every
non-obvious form of use below. **The default answer to "is this safe to delete?"
is "prove it first."**

### Step 0 — establish a green baseline before touching anything

Run the relevant build / type-check / lint / tests FIRST and confirm they pass
(or note what's already red). Without a known-good baseline you can't tell
whether breakage came from your deletion or was pre-existing. Also rebuild any
workspace lib you depend on — stale `dist/` produces phantom type errors and
false "unused" signals (e.g. a shared types package `@acme/types` that resolves
from `dist`; this install's real cases are under *Shared workspace lib examples* in
`LOCAL.md` beside this skill, when your copy keeps one).

### Step 1 — search exhaustively, across the whole stack

A single-package grep is not enough in a monorepo. For each symbol:

- **Calibrate your detector first:** run the search/loop against a symbol you KNOW
  is used and confirm it reports references — a silently-broken search (e.g. zsh
  globbing `grep --include='*.ts'` into an error) makes *everything* look dead.
- Grep the **entire workspace**, not just the current package — shared libs
  (e.g. `@acme/types`) are consumed by other apps, frontends, and services.
- Search for the **bare name** AND for **string forms** of it (quoted, in arrays,
  in config). Dynamic dispatch hides references in strings.
- Search **other repos** that depend on this one when the symbol is exported
  from a published/shared package. An export with no in-repo use may still be
  another repo's public API.
- Check **tests, fixtures, mocks, seeds, migrations, config files, and non-code
  references** (HTML/template ids & classes, `data-*` attributes, i18n keys, SQL,
  CSS selectors) — not just `src/`.
- **Read the hits; don't trust counts.** Common identifiers (`Service`, `User`,
  `index`) produce substring false positives both ways — a high grep count can be
  noise, and a *type* can be reached transitively through another type with zero
  direct hits. Open the file and confirm the actual reference.
- **Distinguish a real reference from a mention.** A name appearing in a comment,
  a doc-string, a changelog, or a disabled/commented block is not a live call.
  Conversely, don't assume a commented block is dead (see intentional stubs below).

### Step 2 — rule out non-obvious "use"

Code is NOT dead if it is reached by any of these. Each is a way a symbol looks
unreferenced to a naive grep but is live at runtime:

- **Public/library API:** exported from a package others import. Unused *inside*
  the repo ≠ unused. Check `package.go`/`index.ts` barrels and the package's
  consumers before touching exports.
- **Dynamic / string-based references:** `import()`, `require(name)`,
  computed property access `obj[methodName]`, route tables, event names, DI
  tokens, job/queue names, GraphQL resolver maps, template strings.
- **Reflection & metaprogramming:** Go reflection + **struct tags**
  (`json:`/`db:`/`validate:` — the field is "unused" in Go but drives
  serialization); Rails metaprogramming (`send`, `method_missing`,
  `define_method`, `constantize`, callbacks, STI); decorators/annotations that
  register via reflection (NestJS providers, EntitySchema, DI).
- **Convention-based wiring:** framework auto-registration by file location or
  name (controllers, migrations, Rails autoload, Vue auto-imported components,
  Nest module scanning). The "caller" is the framework, not your code. Watch for
  routes/endpoints registered under **dotted/string names via mixins** (e.g. Rails
  Grape IPC routes registered through `self.included(base)` — no literal call
  site exists) and **runtime route registration** (routers that mount only routes
  matching a `meta`/auth predicate, so the route def looks statically unreferenced).
- **Intentional stubs & rebuild markers:** an empty component, a commented-out
  block with a "add back when we rebuild X" TODO, or a deliberately-omitted module
  registration may be a placeholder, not litter. Confirm intent (git log, the
  TODO, the user) before removing — deleting it loses the breadcrumb.
- **Pattern/contract-based config:** schemas that accept anything matching a
  pattern (e.g. a Joi rule that allows any `*_API_URL` env var) mean a value can be
  consumed without ever being named in code. "Undeclared" ≠ unused.
- **Serialization & external contracts:** fields read from / written to JSON,
  DB columns, API payloads, env vars, feature flags, CLI args. Removing a field
  that "nothing reads" can break a wire format or a stored record.
- **Build-conditional code:** Go build tags, `NODE_ENV`/env-gated branches,
  platform-specific files, feature-flag-gated paths. Off in your config ≠ dead.
- **Framework lifecycle hooks:** callbacks/handlers invoked by the framework
  (`after_commit`, lifecycle methods, signal handlers, scheduled jobs).
- **Tests-only but intentional:** test helpers, factories, fixtures. Used only
  by tests is still used.

### Step 3 — lean on tooling, then verify

Tools find candidates; they do not authorize deletion.

- Use the language's own unused-code detectors as a *first pass*: TS
  `noUnusedLocals`/`tsc`, ESLint/oxlint `no-unused-vars`, `ts-prune`/`knip` for
  exports, `staticcheck`/`go vet`/`deadcode` for Go, Ruby `debride`/coverage for
  Rails. For languages with no good detector (e.g. R/Shiny), the first pass is a
  disciplined project-wide grep instead.
- **Configure the tool's real entry points before trusting it.** Detectors infer
  reachability from declared entrypoints; a non-obvious one (a TS module loaded by
  a plain `server.js`, a CLI script, a dynamically-imported route) makes everything
  it pulls in look "unused." Most knip/ts-prune false positives trace to this.
- Treat their output as **candidates**, then apply Steps 1–2 to each. These
  tools routinely miss reflection, string dispatch, cross-repo use, and
  framework wiring — and over-report behind bad entrypoints.
- **Peel orphans iteratively, not in one shot.** A deletion orphans whatever the
  deleted code referenced (DTOs → sub-DTOs → validators). Re-run detection after
  each deletion pass and repeat until a pass finds nothing new; keep any file
  that retains a single non-spec, non-self reference.
- After deleting, **build + run the test suite + boot the affected path**. A
  green compile is necessary, not sufficient — exercise the code path (or a
  live stack) when the use could be dynamic. Report what you verified.
- **Don't infer "dead/broken" from stale data.** An empty table or zero-result
  query in a dev snapshot can be old data, not a dead code path — reproduce live
  before concluding the code is unused.

### Prefer the smallest safe reduction

Removing the whole symbol is the last resort, not the first. Scale the cut to what
you can actually prove is unreachable:

- An **unused export** that's still used internally → drop the `export` keyword,
  keep the symbol.
- A **dead barrel re-export** where the underlying thing is imported directly →
  remove the re-export line, keep the component/module.
- Only delete the entire definition when nothing anywhere — in any repo, by any
  mechanism above — reaches it.

### Step 4 — when uncertain, don't delete

If you cannot prove a symbol is dead, **leave it and report it** as a candidate
with what you found (where you looked, why it's ambiguous), rather than removing
it. Group confirmed-dead deletions into their own atomic commit, separate from
quality refactors, so they're easy to review and revert.

### Consumer-bounded removal (when the user names the complete consumer set)

The reason removing an exported/public symbol (an API endpoint, a library export)
is normally unsafe is a *single* unknown: **we don't know everyone who calls it.**
So a published endpoint with no in-repo use is still presumed live (Step 2). When
the **user explicitly tells you the complete, authoritative set of consumers**,
that unknown is gone — and only then may you treat cross-consumer absence as proof
of death. Use this mode ONLY on the user's explicit instruction; never assume a
consumer set yourself.

When instructed, treat the named consumers as ground truth:

- **Make the consumer set explicit in your report** ("user states the only consumer
  of `orders-api` is `web-app`"). The whole removal rests on this claim — surface it
  so the user can correct it before anything is deleted.
- **Search every named consumer exhaustively** for the endpoint/symbol, applying
  Step 1 (bare name + string forms: URL paths, route constants, service-method
  names, generated clients) and Step 2 (dynamic/string dispatch, config). The path
  may be assembled (`base + '/v1/' + resource`), so grep for path fragments, not
  just whole strings.
- **An endpoint absent from all named consumers is confirmed dead** — remove it,
  even though it's "public." Present in any consumer → live; keep it.
- **Re-confirm the boundary still holds** before deleting: verify no *other*
  in-repo or sibling app has quietly started consuming it (a new service, a cron, a
  test harness). The user's claim covers known consumers; a quick workspace grep
  guards against a new one. If you find a consumer the user didn't name, stop and
  report — the boundary was wrong.
- **Migration ordering matters.** When old endpoints are being superseded by new
  ones (e.g. `v1` → `v2`), only remove the old endpoint after its consumer has been
  cut over to the replacement *and* that cutover is merged/verified — otherwise you
  delete something still live in the current consumer revision. Sequence:
  add new → migrate consumer → confirm no consumer references old → remove old.

Worked example (hypothetical): the user states **the only consumer of a service
`orders-api` is `web-app`.** Once an old orders-api list endpoint has been replaced
by a new versioned one and web-app is moved onto the new version, diff orders-api's
exposed endpoints against web-app's usage to identify the now-orphaned old
endpoints, and remove them as confirmed-dead. (This install's standing consumer
set, stated by the user: `LOCAL.md` beside this skill, when your copy keeps one —
*Standing consumer set*.)

## Verify a flagged issue before acting on it

Whether a finding comes from a tool, a review subagent, another reviewer, or your own first
read — **confirm it against the exact code before you change anything.** Automated and AI
reviewers over-report; acting blindly churns or breaks correct code.

- **Read the precise code path** the finding names. Many "bugs" dissolve on reading (the
  framework already does the thing, the value is already neutralized upstream, the branch is
  unreachable).
- **For any runtime/DB/ORM/serialization claim, confirm empirically, not from memory of how the
  framework "should" behave.** Print the generated SQL, run a rolled-back transaction, write a
  10-line throwaway script, or repro the path. Empirical proof is cheaper and more certain than
  arguing internals.
- **Blast-radius grep before "fixing" a shared convention.** If the flagged pattern is the
  house convention across many call sites, a local "fix" is a behavior change across all of
  them — surface it as a decision, don't smuggle it into a cleanup.
- **Scope the fix to the real defect.** Reading the exact code often shrinks a fix from a wide
  signature change to a one-line clamp (and sometimes proves there's nothing to fix).
- Then stack the **verified** fixes as small, concern-scoped commits/PRs.

## Fix at the right layer, at the right scope

- **The same bug twice means the fix is at the wrong LAYER.** A second instance of a bug
  you already fixed is not bad luck and not a missed case — it is evidence the first fix
  sat above the level where the defect actually lives. Before patching instance two, go
  find the layer where one change covers both.
- **A bug's blast radius is a scope decision, not a technical one.** How far a fix should
  reach — this call site, this module, every consumer — is a judgment about risk and
  ownership that belongs to the person who owns the change, not something the stack trace
  decides. Surface it as a choice rather than quietly picking the widest or narrowest.
- **Review the FIX as adversarially as the original code.** Patches reintroduce their own
  bug class: the author is now reasoning about a narrow, freshly-understood slice and is at
  their least suspicious. A fix deserves the same "how does this break?" pass the defect
  got.
- **Before calling code "too clever," find out WHAT FORCES IT.** Non-obvious code is
  sometimes load-bearing — a workaround for a framework bug, an ordering constraint, a
  performance floor. Simplifying without finding the forcing constraint reintroduces the
  problem the cleverness was solving. If nothing forces it, then simplify.
- **Extract the shared base rather than re-declaring the fields** when two types drift
  into near-duplicates; and **don't make one function serve two registers** — a label
  helper stretched to cover two audiences reads wrong in both.

> **Reviewing a delegate's diff:** a code-writing agent **reaches for the weakest passing
> assertion**, and arguing about it is slower than settling it empirically — mutate the
> subject and see whether the assertion actually catches it. See [tdd-skill](../tdd-skill/SKILL.md)'s mutation
> rails; the standard here is that the returned diff meets the same bar as your own.

## Reporting review findings

- **Label every finding by severity:** **Critical** (blocks — security, data
  loss, broken functionality) / *(no prefix)* = Required / **Optional/Consider**
  (worth doing, not required) / **Nit** (author may ignore) / **FYI**. Without
  labels authors treat all feedback as mandatory.
- **Lead by leverage:** correctness & security first, then structural
  regressions and missed simplifications, then the rest. A few high-conviction
  comments beat a long list — if you have one structural problem and ten nits,
  the structural problem IS the review.
- **Approve when the change definitely improves overall code health**, even if
  imperfect; don't block because it isn't how you'd have written it. Exit: all
  Critical resolved; every Required resolved or explicitly deferred with a filed
  follow-up (per the open-followups habit — no deferred cleanup without one).
- **Review the tests first** — they reveal intent and coverage before you read
  the implementation.

## Posting a review to a PR on the user's behalf

Adopted 2026-09-04 from a real PR review, where a long top-level comment was
rewritten into inline threads over three rounds. The findings did not change; the
delivery did, and it came out roughly a third the length. (The originating PR:
`LOCAL.md` beside this skill, when your copy keeps one — *Posting reviews: the
originating PR*.)

- **Anchor every finding as an inline comment on the lines it concerns**, not as
  one top-level essay. `start_line`/`line` + `side: RIGHT` against the head SHA.
  The anchor carries the file and line, so the comment carries only the problem —
  that alone removes most of the scaffolding a top-level review needs.
- **Comment only on what needs work.** No "fixed since last time" recap, no
  "checked and fine" inventory, no praise. When a prior review had blockers, one
  line in the review body saying they cleared is the whole allowance.
- **Only genuinely file-less items go in the review body** — missing ticket, plan
  doc not updated, a verification that spanned repos.
- **One to three sentences per comment.** Mechanism, then consequence, then the
  fix. No bullet lists inside a comment, no hedging preamble.
- **Never change the review state unasked.** Post with `event: COMMENT` so an
  existing CHANGES_REQUESTED (or a clean slate) stays as it is; changing it is
  the user's call, made explicitly.
- **Draft in-session and get approval before posting.** The user revises wording;
  posting happens on an explicit go, not on your read of "this looks ready."
- **Mechanically:** one `gh api repos/<owner>/<repo>/pulls/<n>/reviews --method
  POST --input <file>` call with a `comments` array. Validate the JSON and
  confirm every anchor's exact line span against the head SHA first
  (`git show <ref>:<path> | sed -n '<a>,<b>p'`) — one bad span rejects the entire
  review, not just that comment.
- **Verify across repo boundaries before asserting or asking.** On that PR an open
  question ("does the sibling service validate the hash?") and a standing nit both
  dissolved once the sibling repo was actually read. A question you could have
  answered yourself costs the author a round-trip; see a cross-skill principles
  file, if you keep one, on unverified claims reaching people other than the user.

## Dependency upgrades

- **Read the changelog, not the version number** — a "patch" can carry a
  behavior change; for a major, read the migration notes.
- **One dependency per change** — a bulk bump hides which package broke the build.
- **Verify a green suite before AND after.** Thin coverage around the dep is
  itself the finding — add a test first.
- **Review the lockfile diff, not just the manifest**, and never hand-edit the
  lockfile.
- **Pre-add gate:** does the existing stack already solve it / size / maintenance
  / audit / license.

## Output when asked to "remove dead code"

1. List candidates found (tooling + manual search).
2. For each: verdict — **confirmed dead** (with the search evidence) /
   **live** (with the use you found) / **uncertain** (flag, don't delete).
3. Delete only the confirmed set; keep it in a dedicated commit.
4. State what you ran to verify (build, tests, live boot) and what's unverified.

## Before you call this done

- Every deletion has evidence attached (where you searched, what you ruled out) —
  not just a tool's say-so.
- Anything you couldn't prove dead is flagged, not deleted.
- Build + tests + lint are green, and you exercised (or live-booted) any path
  whose use could be dynamic.
- Deletions sit in their own commit, separate from quality refactors.
- No behavior changed — or the behavior change is called out explicitly.
- New durable traps/conventions from this pass are captured in `LEARNINGS.md`
  beside this skill, when your copy keeps one.

## Related skills

- [deprecation-and-migration](../deprecation-and-migration/SKILL.md): removing something that still has consumers is a migration, not a cleanup.
- [security-and-hardening](../security-and-hardening/SKILL.md): its dependency-intake checklist runs alongside the pre-add gate here.

## Capturing learnings (session-handoff protocol)

Accumulate durable, project-specific quality knowledge in `LEARNINGS.md` beside this
skill, when your copy keeps one:
style conventions adopted, dead-code false-positive traps hit in THIS codebase
(specific reflection/dynamic-dispatch patterns), which detectors work per stack,
and cross-repo consumer relationships worth remembering. On handoff / "update
skills" / after a cleanup: dedupe, merge, tag by stack/project, extract the
general principle. Read it before quality or dead-code work.
