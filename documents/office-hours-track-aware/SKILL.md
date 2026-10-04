---
name: office-hours-track-aware
description: Wraps gstack /office-hours. Runs the session, infers native vs web, writes .gstack/track, moves the design doc into docs/ and publishes it before approval.
allowed-tools: Bash, Read, Write, Edit, Grep, AskUserQuestion, Skill, Artifact
---

# /superpowers-gstack:office-hours-track-aware

Wraps gstack's `/office-hours`: runs it to completion, infers native vs web, declares the
track once per project, moves the design doc into the repo, and lets the user read the
doc before being asked to approve it.

## Phase 0 — Setup

Derive the project slug with gstack's helper and read any existing track marker:

```bash
eval "$(~/.claude/skills/gstack/bin/gstack-slug 2>/dev/null)"
[ -z "${SLUG:-}" ] && SLUG="$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")"
{ [ -z "$SLUG" ] || [ "$SLUG" = "/" ]; } && { echo "FATAL: could not derive SLUG" >&2; exit 1; }
mkdir -p .gstack
EXISTING_TRACK=$(tr -d '[:space:]' < .gstack/track 2>/dev/null || true)
case "$EXISTING_TRACK" in ''|ios|macos|both) ;; *) echo "BLOCKED — invalid .gstack/track value '$EXISTING_TRACK' (expected ios, macos or both)" >&2; exit 2 ;; esac
echo "SLUG=$SLUG EXISTING_TRACK=${EXISTING_TRACK:-none}"
```

## Phase 1 — Run upstream office-hours

Before invoking it, drop a timestamp marker so the doc *this* run produces can be told
apart from anything else that changes on disk meanwhile (another session, a formatter, a
handoff write):

```bash
mkdir -p .gstack && touch .gstack/.office-hours-start
```

Invoke it through the Skill tool and let it run its normal flow (product context, forcing
questions or builder mode, design doc). A skill invoking a skill is fine.

```
Skill(skill="office-hours")
```

gstack writes the design doc under `~/.gstack/projects/$SLUG/` by default. Locate the one
written after the marker that carries design-doc frontmatter, and relocate it into the
repo's `docs/`, never overwriting an earlier doc:

```bash
CANDIDATES=$(find ~/.gstack/projects/"$SLUG" . -maxdepth 3 -type f -name '*.md' -newer .gstack/.office-hours-start \
  ! -path '*/node_modules/*' ! -path '*/.git/*' -exec grep -lE '^(type: design-doc|status: DRAFT)' {} + 2>/dev/null)
rm -f .gstack/.office-hours-start
COUNT=$(printf '%s\n' "$CANDIDATES" | grep -c . || true)
[ "$COUNT" -eq 0 ] && { echo "No design doc found — did office-hours write one?" >&2; exit 1; }
[ "$COUNT" -gt 1 ] && { echo "Several new design docs:"; printf '%s\n' "$CANDIDATES"; echo "Ask which one before moving anything." >&2; exit 1; }
RECENT_MD="$CANDIDATES"
case "$RECENT_MD" in
  "$HOME/.gstack/projects/"*)
    mkdir -p docs
    TARGET="docs/$(basename "$RECENT_MD")"
    [ -e "$TARGET" ] && TARGET="docs/$(basename "${RECENT_MD%.md}")-$(date +%Y%m%d-%H%M%S).md"
    mv "$RECENT_MD" "$TARGET" && RECENT_MD="$TARGET" ;;
esac
echo "DESIGN_DOC=$RECENT_MD"
```

## Phase 2 — Infer track

Read the doc and count native vs web signals (case-insensitive, word-boundary).
Native: SwiftUI, UIKit, AppKit, Swift, iOS, iPadOS, macOS, watchOS, tvOS, visionOS, Xcode,
App Store, TestFlight, Mac app, iPhone app, iPad app. Web: Next.js, React, Vue, Svelte,
Angular, Node.js, Express, Django, Rails, Flask, web app, dashboard, landing page, npm,
pnpm, Vercel, Netlify. Native only → `native`; web only → `web`; both → `ambiguous`;
neither → `unknown`, treated as web.

## Phase 3 — Platform question

Skip entirely when `EXISTING_TRACK` is set, or when the track is `web` / `unknown` (no
marker is written, matching gstack's default). Otherwise ask once with AskUserQuestion;
for `ambiguous`, first say that mixed signals were found and confirm it is a native project.

> Which platform does this project ship to first — iOS, macOS, or both?
> One-time project decision; it steers generated Package.swift platforms and design
> defaults. Re-run later to change it.

Write the answer (`ios`, `macos` or `both`): `echo "$CHOICE" > .gstack/track`. Report
`Track set: <value>`, or `Track already set: <value> (no change)` when skipped.

## Phase 4 — Let the user read, then approve

Before asking anything, publish the design doc as a page: load the `artifact-design`
skill, write an HTML rendering of `$RECENT_MD` to a scratch file, and publish it with the
Artifact tool so the user has a link to read. If the Artifact tool is unavailable, print
the path to `$RECENT_MD` and continue.

Then ask with AskUserQuestion:

> Read the design doc? Approve — it holds. Revise — something must change. Restart — the
> premise was wrong.

- **Revise** → ask what to change, edit the markdown, republish the same artifact, ask again.
- **Restart** → back up the doc (`mv "$RECENT_MD" "$RECENT_MD.bak"`) and re-run from Phase 1.
- **Approve** → continue.

## Phase 5 — Mark approved and suggest the next step

```bash
grep -q '^status: DRAFT$' "$RECENT_MD" || { echo "no 'status: DRAFT' line to approve in $RECENT_MD" >&2; exit 1; }
sed -i.bak 's/^status: DRAFT$/status: APPROVED/' "$RECENT_MD" && rm -f "$RECENT_MD.bak"
grep -q '^status: APPROVED$' "$RECENT_MD" || { echo "approval write failed" >&2; exit 1; }
```

Republish the artifact so the page shows the new status, then print:

```
Design doc approved: <path>
Track: <ios|macos|both>  (or "web/unknown — no marker written")

Next:
- native → /superpowers-gstack:swiftui-design-consultation
- web    → /design-consultation (gstack)
```

Re-runs are idempotent: an existing `.gstack/track` is kept, office-hours runs fresh and
writes a new doc, and relocation never overwrites an earlier doc.
`/superpowers-gstack:adapt` emits a CLAUDE.md rule preferring this wrapper when
the user types `/office-hours`.
