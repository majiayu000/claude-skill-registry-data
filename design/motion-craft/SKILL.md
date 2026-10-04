---
name: motion-craft
description: Implement professional web animations in a target repo against an approved design blueprint or an explicit motion direction. Use when asked to "add animations", "improve the motion", "make it feel alive", "implement the motion plan", or when dispatched by the upgrade-site skill. Plans by default; modifies code only on explicit implement authority. For broad visual/reference research, see design-dna instead.
user-invocable: true
argument-hint: "[target repo path and/or blueprint path, plus scope]"
compatibility: Designed for Claude Code. Requires git and a browser-verification tool (Playwright-compatible or gstack browse) for implement mode; plan mode works without a browser.
metadata:
  version: "1.0.0"
  author: augchan42
  schema-version: "1"
---

# Motion Craft

You implement animations against an approved blueprint or explicit direction.
You NEVER perform broad reference research — that is `design-dna`'s job.

## Authority mode

```text
mode =
  inherited from upgrade-site when dispatched
  else explicit implement request ("implement", "apply", "make the changes") → implement
  else plan
```

Plan mode writes only `docs/MOTION.md` sections and reports. Implement mode
may modify source, subject to Git safety below.

**Without a blueprint:** derive a target-native motion brief from the
existing site and its design documents. Do not research references.

## Target resolution

```text
target_repo = explicit path → current git root → cwd
```

Canonicalize; refuse `/` or `$HOME` as roots; all writes beneath the target;
state the resolved target up front.

## Step 1 — Target-policy discovery

This skill carries no project-specific policy. Before planning, read the
target's `AGENTS.md`, `CLAUDE.md`, `docs/DESIGN.md`, `docs/MOTION.md`, route
conventions, and package metadata. Identify high-volume generated templates
(programmatic/pSEO pages, per-item detail routes) and EXCLUDE them unless
explicitly included in scope. Record discovered policy at the top of your
plan output — i.e. in the response/report you give the user, not as
free-form prose added to the target's `docs/MOTION.md` (that file's content
outside the managed sections belongs to the project; see Step 4).

## Step 2 — Stack detection

Detect the animation library and version, its import convention, the CSS
framework, and the rendering model (server/client components, hydration).
Prefer stack-native techniques. Preserve the installed package's compatible
API — do not rewrite imports to a different entry point because a newer one
exists.

Never add a new animation dependency without asking. In a non-interactive
run, never add it at all: use the existing stack, CSS, or browser-native
APIs; otherwise record the item as **deferred** with the missing dependency
and rationale. The pipeline must not stall.

## Step 3 — Motion audit

What animates today, what is static, obvious jank (layout-affecting
transitions, unthrottled scroll handlers, missing reduced-motion handling).

## Step 4 — Choreography plan (upsert)

Write per-section specs into `<target_repo>/docs/MOTION.md` inside managed
sections — replace a matching section on re-run, never append a duplicate:

```markdown
<!-- inkstone:motion-craft:start section-id=homepage-hero -->
| Element/pattern | Trigger | Initial state | Final state | Scroll range/threshold | Duration | Delay/stagger | Easing | Scrubbed or discrete | Mobile variation | Reduced-motion fallback | Evidence | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
<!-- inkstone:motion-craft:end section-id=homepage-hero -->
```

If `docs/MOTION.md` does not exist yet, create it: a minimal top-level
heading (e.g. `# Motion`) followed by the managed section above — do not
invent additional unmanaged content.

Every data row must have exactly 13 cells matching the header. Never put a
literal `|` inside a cell (it silently shifts every later column); wrap
inline code or punctuation instead, and count cells before writing when a
row's content is long or generated programmatically.

Content outside managed sections belongs to the project — never touch it.

## Step 5 — Implement (implement mode only)

One section at a time, following `references/implementation-rules.md`
(client-boundary, property, bundle, accessibility, and i18n rules — read it
before writing any code).

### Git safety

1. Confirm the target is a git repository; refuse implement mode otherwise.
2. If the working tree is dirty with unrelated changes: stop and report.
3. Prefer a dedicated branch.
4. Commit per section only when the worktree was clean at start and that
   section's gates passed; otherwise leave changes uncommitted and provide a
   proposed commit breakdown.

## Step 6 — Verify

Every implemented section passes `references/verification-gates.md` before
you move to the next. Evidence goes to
`<target_repo>/.artifacts/site-upgrade/<run-id>/`.
