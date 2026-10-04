---
name: verify-and-land
description: |
  Build the checked-out branch, launch that exact app, let the user confirm the
  fix is really there, then push and land it by the project's landing mode.
---

# Verify, then land

The gap this closes: a fix is committed, the user opens "the app", the fix is not
there — so they conclude it did not work. Usually it did. They were looking at a
**different build**: the copy in `/Applications` that Spotlight, the Dock and
Launchpad all open, or a `DerivedData` product from another branch. Nothing rebuilds
when the branch changes, because nothing ever does. Measured on one real project: the
installed copy was a month older than the branch build, and four other stale build
products were registered besides.

So this skill never asks the user to open the app. It **builds the branch they are
standing on, launches that exact bundle, proves on screen which one is running**, and
only then asks whether the fix is there. A yes lands the branch the way the project
has decided to land (Phase 7), without a second question unless the branch itself
changes how the project lands; a no keeps the branch open and says what to look at next.

Invoke with: `/superpowers-gstack:verify-and-land`

## Phase 0 — refuse early, and commit first

| Condition | Do this |
|---|---|
| Not a git repo | Refuse: "Not a git repository — there is no branch to verify or land." |
| No runnable app (Phase 2 finds none) | Refuse: "No app target found. This skill verifies something you can look at; for a library or CLI, run the tests instead." |
| Detached HEAD | Refuse landing later, so say now: give the work a branch first (`git switch -c <name>`), then re-run. |
| On the default branch | Build and launch normally, then skip Phase 7 — there is nothing to land. Say so once. |

**Uncommitted changes must be committed before the build.** Not a style preference:
the build compiles the working tree, but `git push` and every landing skill move
*commits*. Verify a dirty tree and land it and the user has approved something that
is not what shipped. Offer to commit — with a real message, per the repo's
convention — and only then build. If they decline, build anyway so they can look, but
**Phase 7 is blocked**: say plainly that landing would ship something other than what
they just saw.

## Phase 1 — name the change, so the user knows what to look at

```bash
DEFAULT_REF=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/||')
[ -z "$DEFAULT_REF" ] && for c in origin/main origin/master main master; do
  git rev-parse -q --verify "$c" >/dev/null && DEFAULT_REF=$c && break
done
BASE=$(git merge-base HEAD "$DEFAULT_REF")
git log --oneline "$BASE..HEAD"; git diff --stat "$BASE..HEAD"
```

Keep the *ref* that verified, not a stripped name — in a fresh clone `origin/main`
exists and `main` may not, and `merge-base` against a missing ref fails.

Turn the diff into **one sentence per observable change**, not files: "the sidebar
should keep its width when you resize the window" beats "3 commits touching
`SidebarView.swift`". A branch often carries more than one change — name each,
because the gate in Phase 6 asks about all of them: one yes must never quietly ship
three changes of which the user looked at one. If a change has no user-visible
effect — a refactor, a test — say so: looking is the wrong check for it; the tests
cover it and the gate covers the rest.

## Phase 2 — resolve the container, the scheme, and the destination

**Generate the project first if it is generated.** A `project.yml` is itself an
Apple-project signal: many repos commit only the spec and gitignore the
`.xcodeproj`, so listing schemes before generating finds nothing at all. If
`project.yml` exists and either no `.xcodeproj` is present or the spec (or anything
it includes) is newer, run `xcodegen generate` before anything else.

**Carry the container through every command.** A repo holding both a `.xcworkspace`
and a `.xcodeproj` makes bare `xcodebuild` ambiguous, and it will pick the wrong one
or fail:

```bash
if   ls *.xcworkspace >/dev/null 2>&1; then XC=(-workspace "$(ls -d *.xcworkspace | head -1)")
elif ls *.xcodeproj   >/dev/null 2>&1; then XC=(-project   "$(ls -d *.xcodeproj   | head -1)")
else XC=(); fi
xcodebuild "${XC[@]}" -list -json
```

Every later `xcodebuild` call takes `"${XC[@]}"`. One scheme is the answer; several,
ask once.

Split macOS from iOS by the scheme's own settings, never by guessing:

```bash
xcodebuild "${XC[@]}" -showBuildSettings -scheme "$SCHEME" -configuration Debug 2>/dev/null \
  | grep -E '^ +SUPPORTED_PLATFORMS '
```

`macosx` → macOS. `iphonesimulator` → iOS. Both → ask which one the fix is in.

**Pin the destination, then re-read the settings through it.** `BUILT_PRODUCTS_DIR`
is platform-specific (`Debug` vs `Debug-iphonesimulator`); read without a destination
it answers for the scheme's *default* platform, so the launch would look in a
directory nothing was written to — and the proof step would validate the wrong place.
For iOS, pin one simulator by UDID: `booted` is ambiguous with several up, and a
`name=` destination need not be the one that is booted.

```bash
# iOS only — choose exactly one device and use it for build, install and launch
UDID=$(xcrun simctl list devices booted -j | python3 -c 'import json,sys;d=json.load(sys.stdin)["devices"];print(next((x["udid"] for v in d.values() for x in v),""))')
[ -z "$UDID" ] && { UDID=$(xcrun simctl list devices available -j | python3 -c 'import json,sys;d=json.load(sys.stdin)["devices"];print(next((x["udid"] for v in d.values() for x in v if "iPhone" in x["name"]),""))'); xcrun simctl boot "$UDID"; }
DEST="platform=iOS Simulator,id=$UDID"      # macOS: DEST='platform=macOS'

eval "$(xcodebuild "${XC[@]}" -showBuildSettings -scheme "$SCHEME" -configuration Debug -destination "$DEST" 2>/dev/null \
  | awk -F' = ' '/^ +(BUILT_PRODUCTS_DIR|FULL_PRODUCT_NAME|PRODUCT_BUNDLE_IDENTIFIER|EXECUTABLE_NAME) /{gsub(/^ +/,"",$1); print $1"=\""$2"\""}')"
```

All four values are used below, and **the launch phase refuses to run without them**.

### Non-Xcode projects

- **SwiftPM with a GUI app bundle** — build with `swift build`, then treat the
  produced `.app` exactly as below. A plain **command-line** executable has no bundle,
  no `PRODUCT_BUNDLE_IDENTIFIER` and nothing to look at: do not force it through this
  flow. Run it once, show its output, and say that tests are the real check.
- **Web** — see Phase 6b.

## Phase 3 — the stale-app census (do not skip)

This is the phase that addresses the actual complaint. Before building, find every
bundle the user could plausibly be looking at:

```bash
# 1. What Spotlight, the Dock and `open -a` would actually start. Ask LaunchServices
#    BY BUNDLE ID — `path to application "<name>"` matches the *display* name, which
#    need not equal the executable name, and a silent miss defeats the census. Do not
#    probe with `open -Ra` either: it pops a Finder window as a side effect.
osascript -e "POSIX path of (path to application id \"$PRODUCT_BUNDLE_IDENTIFIER\")" 2>/dev/null
# 2. Build products lying around. Spotlight does not index DerivedData, so `mdfind`
#    finds none of these — glob the directory instead.
ls -d ~/Library/Developer/Xcode/DerivedData/*/Build/Products/*/"$FULL_PRODUCT_NAME" 2>/dev/null
# 3. Anything of this app already running, wherever it came from.
pgrep -fl "/Contents/MacOS/${EXECUTABLE_NAME}$" 2>/dev/null
```

Expect several — a project rebuilt under different DerivedData hashes accumulates
them. Report each with its build time (`date -r "<app>/Contents/MacOS/<exec>"`), then
say plainly: *"the one I am about to build and open is `<BUILT_PRODUCTS_DIR>/<name>`;
the copy in /Applications is from `<date>` and does not have this fix."* One sentence
— this is the misunderstanding that sends people hunting a bug that is not there. If
no other copy exists, say nothing; do not narrate an ambiguity that is absent.

## Phase 4 — build the branch that is checked out

Record the commit you are about to build: `VERIFIED_HEAD=$(git rev-parse HEAD)`. Phase 5
names it as the commit on screen, and a yes in Phase 6 is about this commit only.

```bash
xcodebuild "${XC[@]}" -scheme "$SCHEME" -configuration Debug -destination "$DEST" build
```

For iOS, `mcp__XcodeBuildMCP__build_run_sim` does build, install and launch in one
step — check availability with `ToolSearch` first, since these tools load on demand.
The CLI equivalent installs and launches **on the same UDID** that was built for:
`xcrun simctl install "$UDID" "$BUILT_PRODUCTS_DIR/$FULL_PRODUCT_NAME"` then
`xcrun simctl launch "$UDID" "$PRODUCT_BUNDLE_IDENTIFIER"`.

A failing build ends the skill here. Report the first real error, fix it if it is
within the current task, and never proceed to a launch that would show stale code.

A build can also exit 0 without leaving the product where the settings said it would
be. Check before launching — `open` on a missing path raises a macOS dialog that
explains nothing:

```bash
[ -d "$BUILT_PRODUCTS_DIR/$FULL_PRODUCT_NAME" ] || { echo "build succeeded but $FULL_PRODUCT_NAME is not in $BUILT_PRODUCTS_DIR"; exit 1; }
```

## Phase 5 — launch that exact bundle, and prove it

**Refuse to run this phase with an unset variable.** The first line is not
decoration: an empty `$EXECUTABLE_NAME` would turn the fallback below into
`pkill -f "/Contents/MacOS/"`, which matches every bundled process on the machine —
`loginwindow` included — and would log the user out. Measured, not theorised.

```bash
: "${EXECUTABLE_NAME:?resolve build settings in Phase 2 first}" \
  "${PRODUCT_BUNDLE_IDENTIFIER:?resolve build settings in Phase 2 first}" \
  "${BUILT_PRODUCTS_DIR:?resolve build settings in Phase 2 first}"
```

Quit any running instance — otherwise macOS activates the copy already up, very often
the wrong one — and **wait for it to actually exit**, because both quit paths return
before the process does:

```bash
if pgrep -f "/Contents/MacOS/${EXECUTABLE_NAME}$" >/dev/null; then
  osascript -e "tell application id \"$PRODUCT_BUNDLE_IDENTIFIER\" to quit" 2>/dev/null \
    || pkill -f "/Contents/MacOS/${EXECUTABLE_NAME}$"
  for _ in $(seq 1 20); do
    pgrep -f "/Contents/MacOS/${EXECUTABLE_NAME}$" >/dev/null || break; sleep 0.25
  done
fi
open "$BUILT_PRODUCTS_DIR/$FULL_PRODUCT_NAME"
```

Then **prove** what came up rather than assuming — and wait for it, since a cold start
with signature validation takes well over a second. Match on the **full executable
path**, not a process name, so a helper or another copy cannot answer for it:

```bash
WANT="$BUILT_PRODUCTS_DIR/$FULL_PRODUCT_NAME/Contents/MacOS/$EXECUTABLE_NAME"
PID=""
for _ in $(seq 1 40); do
  PID=$(pgrep -n "$EXECUTABLE_NAME" 2>/dev/null || true)
  [ -n "$PID" ] && [ "$(ps -o comm= -p "$PID" 2>/dev/null)" = "$WANT" ] && break
  PID=""; sleep 0.25
done
[ -n "$PID" ] && echo "on screen: $(ps -o comm= -p "$PID")" || echo "the branch build did not come up within 10s"
```

Match by **string equality on the full path**, not by a pattern: `pgrep -f` treats
its argument as a regular expression, and a bundle path is not one — a `+` or `(`
anywhere in it would quietly stop the proof from ever matching.

If nothing appeared, that is a launch failure — **not** a verdict on the fix. Report
it and stop. If a different copy is running instead, quit it, wait, and relaunch.

**iOS needs its own proof**, for the same reason: the simulator may still hold an
older install of the same bundle id, and `launch` will happily start that one.

```bash
xcrun simctl get_app_container "$UDID" "$PRODUCT_BUNDLE_IDENTIFIER" app
stat -f '%Sm' "$(xcrun simctl get_app_container "$UDID" "$PRODUCT_BUNDLE_IDENTIFIER" app)"
```

The timestamp must be from this run. If it is older the install did not take:
`xcrun simctl uninstall "$UDID" "$PRODUCT_BUNDLE_IDENTIFIER"`, install again.

Report one line: which branch, which bundle path, and which commit is on screen.

## Phase 6 — the human gate

The user is the instrument; a person looking is the entire point. Ask with
`AskUserQuestion`, naming the behaviour from Phase 1:

- **Yes, it works** — asked per observable change when there are several; only when
  all of them hold → Phase 7. Phase 7 then lands without asking again, so settle now
  what a yes does, and say it in this option:
  - Name `VERIFIED_HEAD`, recorded in Phase 4 before the build: the commit the user is
    looking at. Do not re-read `HEAD` here; a commit made since the build is not on screen.
  - Read the landing mode (the rule in Phase 7, step 2) and name what follows: `solo` —
    push, then land on the default branch through `/superpowers-gstack:land`; `pr` —
    push, then open a pull request through `/ship`; no valid line — push, then `land`
    asks once how this project lands. With no remote configured, say that nothing is
    pushed and the landing stays on this machine. If `/review` has not run on this
    branch in this session, say that a yes lands code no review has seen (`land`
    assumes one has).
  - When Phase 0 skipped or blocked Phase 7 (the default branch, a detached HEAD, or
    uncommitted changes the user declined to commit), say instead that a yes lands
    nothing.
- **No, it still behaves the old way** → stay on the branch, land nothing. Say what
  you would check next and offer `/investigate`.
- **Something else broke** → same: land nothing, investigate.

**End your message at this question.** Do not pre-run the landing steps and do not
describe them as though they had happened.

### Phase 6b — the web track, briefly

Record `VERIFIED_HEAD=$(git rev-parse HEAD)` first, as Phase 4 does. Then start the
project's dev script **and keep its PID**. A ready port does not prove the
server is yours: an older one from another branch or worktree may already own it, in
which case the new process exits and the readiness probe succeeds against stale code
— the same bug as the stale bundle, wearing a different hat. Check that the process
you started is still alive before trusting the port, and if the port was taken, say
so and use a free one. Then the same gate, unchanged. Skip Phase 3 — a dev server
serves the working tree, so no stale-bundle ambiguity exists.

## Phase 7 — land it

Landing has two halves and they are not the same: **pushing is backup, landing is
completion.** Do both, in that order. The yes in Phase 6 is the one human review; Phase 7
adds no question of its own when the project has already decided how it lands.

0. **Check that the yes still applies.** A yes covers the build the user saw and the
   landing they were told about, nothing else. If `git rev-parse HEAD` is no longer
   `VERIFIED_HEAD`, or the landing mode now reads differently from what the Phase 6
   option said, land nothing and say what changed. A new commit means a new build: go
   back to Phase 4. A changed mode only invalidates the announcement: go back to Phase 6
   and ask again with the mode as it now reads.
1. **Push first**, so the verified work exists in more than one place whatever is
   decided next. Pass the branch as a quoted argument — refs may legally contain
   `$( )`, `;` and `&`:
   ```bash
   branch=$(git symbolic-ref --short HEAD)
   git rev-parse -q --verify "@{upstream}" >/dev/null \
     && git push \
     || git push -u origin -- "$branch"
   ```
   If the push fails, land nothing: report the error and stop, so landing never runs
   without the backup the Phase 6 option promised. With no remote configured there is
   nothing to push: say plainly that the work stays on this machine, then go on.
2. **Then land it by the project's landing mode.** Read the `Landing mode:` line the way
   `land` does: the exact line `Landing mode: solo` or `Landing mode: pr` in the
   `CLAUDE.md` at the root of this worktree (`git rev-parse --show-toplevel`), a real line
   outside fenced code blocks. Compare it with the same line on the default branch
   (`git show "$DEFAULT_REF":CLAUDE.md`, the ref from Phase 1). When `CLAUDE.md` is a
   symlink, that prints only the link's target path: read the target the same way
   (`git show "$DEFAULT_REF":AGENTS.md` for a link to `AGENTS.md`), as `land` does.
   - **The branch changes the landing mode** (the two differ) → land nothing
     automatically: a branch must not set the policy it is landed under. Ask once with
     `AskUserQuestion` which mode holds, naming both values, and end your message at it.
     Act on the answer as `land`'s exit-14 row says: it is the same stop, made by `land`
     itself when it is invoked on such a branch.
   - **`solo`** → invoke `/superpowers-gstack:land` for this worktree, from its root, with
     no further question.
   - **`pr`** → invoke `/ship` inside this worktree, with no further question from this
     skill. `/ship` may ask its own questions about the pull request; those are not a
     second ask of the landing.
   - **No valid line** (missing, only inside a code block, or both values) → invoke
     `/superpowers-gstack:land` anyway. Its exit-2 row owns this question: it asks the
     user once (solo or pull request? or, with both values, which one holds) and records
     the answer. Do not ask it here as well.

   When `land` stops with an exit code, follow `land`'s own exit-code table: it is the
   authority on the next step. Add no menu of your own on top of it, and never offer
   `/superpowers:finishing-a-development-branch` from this skill: it merges without the
   project's pre-merge gate, which is why `land` stops at exit 8 when `wt` is not
   installed instead of falling back to it.

**If the branch is checked out in a worktree**, run `/ship` and `/superpowers-gstack:land`
from that worktree's root: a branch cannot be checked out twice, and `git checkout` fails
outright elsewhere (`git worktree list` gives the path). The landing skills move the
default branch themselves; do not hand-roll a merge.

After `land` exits 0, follow its `remaining` field: it prints the cleanup commands in the
order git needs them (the worktree first, then the branch).

## What this skill is not

- Not a test run. Tests answer "did I break something else"; this answers "is the
  thing I fixed actually fixed". `/ship` runs the tests on the way to a PR.
- Not UI automation. `/superpowers-gstack:e2e-route` owns automated E2E; this is the
  one case where a human eye is the point.
- Not a release. It builds Debug and launches locally; shipping to users is
  `/land-and-deploy`.
