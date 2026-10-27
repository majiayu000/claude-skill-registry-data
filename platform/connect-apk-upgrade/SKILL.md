---
name: connect-apk-upgrade
description: >
  Upgrade the pinned Connect/CommCare APK end to end — release lookup,
  calibrate, flip every pin, activate, verify, roll back.
  Use when a new APK becomes ACE's default.
disable-model-invocation: true
---

# Connect APK Upgrade

Move ACE's pinned CommCare Android APK from one version to the next — the whole
transition, not just the constant. Manual, cross-opp, once per APK version.

**Why this skill exists.** Jonathan, 2026-09-05: *"We need to have a clear
process ACE does to bump and then make sure everything still works as expected
in the new version — we had a lot of gotchas last time we upgraded because I
didn't do an explicit update-version step."* The bump itself is one line. What
was missing was (a) an explicit enumeration of every place a version is pinned,
(b) proof the new version still navigates on a device, and (c) a checklist that
answers *"does everything still work"* afterwards. That is what this owns.

**This skill is a thin orchestrator.** It does not reimplement calibration
(`selector-map-calibrate`), reactive selector repair (`selector-map-heal`), or
version comparison (`lib/ccz-min-version.ts`). It sequences them and adds the
pin-flip + activation + verification they all omit.

## Inputs

| Source | Artifact | Used for |
|---|---|---|
| Operator | Target APK version (e.g. `2.64.0`) | everything downstream |
| Live | `github.com/dimagi/commcare-android` releases | does the release exist, and does an asset resolve |
| Static | `lib/apk-pin-sites.ts` (via its test) | the machine-discovered pin-site list |
| Static | `mcp/mobile/selectors/connect-<old>.yaml` | the map the new one is seeded from |
| Tool | `bin/ace-doctor` `selector_map_currency` | BEFORE/AFTER state |

## Products

- `mcp/mobile/selectors/connect-<new>.yaml` — a **live-calibrated** map (produced by `selector-map-calibrate`, not transcribed).
- `docs/mobile-calibration/connect-<new>-<date>.md` — the calibration report.
- `docs/mobile-atlas/connect-<new>.md` — the surface atlas for the new version.
- Every pin site flipped in ONE commit (§ Step 5).
- `ACE/_common/connect-screenshots/<new>/` (Drive) — the common training screenshot pool for the new version, produced by `common-screenshot-capture` (§ Step 7b).
- `docs/mobile-calibration/connect-<new>-upgrade-verification.md` — the § Verification checklist, filled in.

## Preconditions (restore, don't adapt)

Per CLAUDE.md § Phase preconditions are restored, not adapted:

1. **No `/ace:run` is in flight on this machine.** This skill runs
   `/ace:setup --force-env` and forces a full Claude Code restart — both of
   which a live run owns. Ask; do not probe-and-guess.
2. **A device is reachable and is yours to wipe.** `mobile_ensure_avd_running`
   cold-boots with `-wipe-data` every dispatch, so it kills whatever is
   running. **AVD contention is real** — as of 2026-09-05 `mobile_diagnose`
   reported 11 other live `ace-mobile` MCPs sharing 2 AVDs across 2 macOS
   accounts. **Serialise the calibration**, and read a dead-looking device as
   *probably a peer's*, not as broken.
3. **Never assume the adb port.** It is ALLOCATED (`mcp/mobile/port-allocator.ts`
   walks upward from 5037; 5038 was live on 2026-09-05). Ask `mobile_diagnose`
   for the port + serial. **Never probe with bare `adb`** — it starts a daemon
   on any port it is pointed at, so a port scan manufactures the servers it then
   reports. To find listeners by hand:
   `lsof -nP -iTCP -sTCP:LISTEN | awk '$1 ~ /^adb/ {print $9}'`.
4. **A Learn-NOT-complete opportunity** for the Learn-dependent states. Learn
   completion is one-way per `(test user, opportunity)` and is server-side — a
   device wipe does NOT reset it (jjackson/ace#568). Consuming one to "diagnose"
   costs a fresh `/ace:run`.

## Process

### Step 0 — Record the BEFORE state

Do this first; the rollback and the verification both diff against it.

```bash
bin/ace-doctor            # capture the whole selector_map_currency block
```

Record `apk_version`, `pin`, `code_default`, `newest_map`, `rows_verified`,
`rows_unverified`, `unresolved_selectors`. Then record the live device's
version, so "what we were on" is a measurement rather than a memory:

```bash
# serial + adb port come from mobile_diagnose — do NOT assume 5037
adb -s <serial> shell dumpsys package org.commcare.dalvik | grep versionName
```

### Step 1 — Prove the release resolves to a downloadable asset

**Before editing any pin.** Dimagi has renamed the release asset at least three
times, and `mcp/mobile/client.ts` probes the three known conventions in order:

| APK | Asset name |
|---|---|
| 2.62.0 | `app-commcare-release.apk` |
| 2.63.0 / 2.63.1 | `commcare-<v>-release.apk` |
| 2.63.2 | `commcare-<v>.apk` |
| 2.64.0 | `app-commcare-release.apk` — **reverted to the 2.62.0 form** |

**The naming is per-release and NON-MONOTONIC. Do not infer it from the
version.** This table used to end `| 2.63.2+ | commcare-<v>.apk |`, which
implied newest-convention-always-wins. Measured 2026-09-06, that is false —
2.64.0 went back to the oldest form, and resolves only on the THIRD candidate:

```bash
B=https://github.com/dimagi/commcare-android/releases/download/commcare_2.64.0
curl -o /dev/null -w '%{http_code}\n' -L $B/commcare-2.64.0.apk          # 404
curl -o /dev/null -w '%{http_code}\n' -L $B/commcare-2.64.0-release.apk  # 404
curl -o /dev/null -w '%{http_code}\n' -L $B/app-commcare-release.apk     # 200
```

So every convention stays in the probe list forever; a cleanup that drops
"legacy" forms would break the CURRENT pin. *Enforced:*
`test/mcp/mobile/apk-asset-conventions.test.ts`.

The 2.63.2 form was missing from that probe list until 2026-07-25, so pinning a
**published** release failed with `APK_DOWNLOAD_FAILED`. A pin whose asset does
not resolve is indistinguishable from a network fault at the point it bites.

```bash
gh release view "commcare_<new>" -R dimagi/commcare-android \
  --json isDraft,isPrerelease,assets \
  --jq '{isDraft, isPrerelease, assets: [.assets[].name]}'
```

Halt unless ALL of:

- the tag exists (a 404 here is the whole finding — do not proceed),
- **at least one asset name ends in `.apk`.** This is the real test, and it is
  strictly stronger than "is it published".
- at least one `.apk` asset matches one of the conventions above.

**Do NOT gate on `isDraft` alone.** This step used to say *"a draft release has
no assets — `mcp/mobile-server.ts` records 2.63.3 as exactly this: a GitHub
draft."* Re-checked 2026-09-06, that is **false**:

```bash
$ gh release view commcare_2.63.3 -R dimagi/commcare-android \
    --json isDraft,isPrerelease,assets
{"isDraft":false,"isPrerelease":false,"assets":["app-lts-release.aab"]}
```

2.63.3 is *published*; its only asset is an `.aab` (an App Bundle, which
`adb install` cannot take). So it is still unpinnable — for a different reason
than the one recorded. Anyone re-deriving the old rule would read
`isDraft: false` and pin it. **The `.apk`-asset check catches both cases; the
draft check catches neither reliably.**

If no asset matches any known convention, Dimagi renamed it again: add the new
form to the `candidateUrls` list in `mcp/mobile/client.ts` **in this PR**, with
a row in `OBSERVED_CONVENTIONS` in the test above, before continuing.

### Step 1b — Diff the two APKs' RESOURCE TABLES, before any device time

**This is the step that catches the class Step 2 is structurally blind to.**
Everything downstream hunts changed *selectors*: a rename, a removal, a value
that drifted. But an APK can rename nothing this map uses and still break every
recipe — by ADDING A SCREEN. 2.64.0 is the proof. Zero id drift across the whole
map, and registration still stranded, because a new PersonalID email step was
inserted mid-flow (ace#2029). **"No id drift" is not "no flow drift."**

Two `comm`s over the two resource tables name the change in one command, for
free, before an emulator is booted:

```bash
AAPT=~/Library/Android/sdk/build-tools/35.0.0/aapt2   # any recent build-tools
ids() { "$AAPT" dump resources "$1" \
          | awk '$1=="resource" && $3 ~ /^id\// {sub(/^id\//,"",$3); print $3}' \
          | sort -u; }

# mktemp, never a predictable /tmp name — ace#1046: on a multi-user Mac the
# write can EACCES while the follow-up read succeeds against another
# account's stale file, and the diff is then plausible and wrong.
OLD=$(mktemp "${TMPDIR:-/tmp}/ace-ids-XXXXXX.txt")
NEW=$(mktemp "${TMPDIR:-/tmp}/ace-ids-XXXXXX.txt")
ids "$TMPDIR/ace-mobile-apk-cache/commcare-<old>.apk" > "$OLD"
ids "$TMPDIR/ace-mobile-apk-cache/commcare-<new>.apk" > "$NEW"

comm -13 "$OLD" "$NEW"    # ADDED in <new>   <- the new surfaces
comm -23 "$OLD" "$NEW"    # REMOVED in <new> <- what may break
```

Commit both lists next to the walk's ui-dumps (`docs/mobile-atlas/evidence/
connect-<new>/resource-ids-<v>.txt`) — every "this id is 2.64.0-only" claim in
the map cites them, and a claim whose evidence lives in `$TMPDIR` is not cited.

(The APKs land in that cache the moment Step 2.0 downloads them; `client.ts`
caches by version, so both are usually already there.)

Read the ADDED set for **clusters**, not individuals. On 2.64.0 it named the
whole change outright before anyone touched a device:

```
personalid_email_skip_button, personalid_email_continue_button, email_text_value,
personalid_email_verify_button, personalid_email_resend_button, otp_code_view,
action_personalid_backupcode_to_personalid_email      <- the nav graph says it too
```

`action_*` entries are Navigation-component destinations, so they hand you the
transition *by name* — `backupcode -> email` is a flow change stated in the
resource table.

Then, for every cluster, ask the question the selector diff cannot: **does a
recipe walk through where this was inserted?** Write the answer down. A new
cluster on a surface no recipe visits is a note; one inserted mid-registration
is `blocks-e2e`.

Also diff the REMOVED set against the map you are about to seed — a row whose id
is gone in `<new>` must not be carried over as if it still resolved.

### Step 2.0 — Get the new APK ONTO the device, and verify it landed

**Do this before Step 2, not after Step 5.** Nothing else in this skill installs
the APK, and calibrating the old one is silent: the bootstrap reports success and
the branch says `<new>` while the device runs `<old>`.

The reason is the ordering trap Step 7 describes, seen from the other end.
`mobile_ensure_avd_running` installs the version named by
`ACE_CONNECT_APK_VERSION` **in the INSTALLED `.env`**, which the live MCP
subprocess read **at its own startup**. Editing `DEFAULT_APK_VERSION` in the repo
changes nothing about a device walk in this session. So swap it out of band:

```bash
# serial + adb port from mobile_diagnose — never assume 5037
export ANDROID_ADB_SERVER_PORT=<port>
adb -s <serial> uninstall org.commcare.dalvik
adb -s <serial> install -r "$TMPDIR/ace-mobile-apk-cache/commcare-<new>.apk"

# VERIFY — this line is part of the step, not a courtesy
adb -s <serial> shell dumpsys package org.commcare.dalvik | grep versionName
```

If the cache has no `commcare-<new>.apk` yet, one `mobile_ensure_avd_running`
downloads it (that also exercises Step 1's asset resolution end to end).

**Re-enable Google Play Services first, and use the command that exists.**
`mobile_ensure_avd_running` deliberately leaves GMS **disabled** so in-app
face capture falls back to ManualMode. `PersonalIdActivity` then declines to
render, showing an *"Enable Google Play services"* AlertDialog with a single
ENABLE button — which reads as broken registration rather than a device setting.
**Observed, not predicted:** repro in the 2.64.0 walk, 2026-09-06, ace#1997 —
`docs/mobile-calibration/connect-2.64.0-2026-09-06.md` finding 2.

```bash
adb -s <serial> shell pm enable com.google.android.gms
```

`pm enable-user` **does not exist** (`Unknown command`); only `disable-user`
does. The pair is asymmetric, and `mcp/mobile/backends/avd.ts` already uses it
correctly — copy from there, not from muscle memory.

### Step 2 — Seed the new map and calibrate it against a live device

1. Copy `mcp/mobile/selectors/connect-<old>.yaml` →
   `connect-<new>.yaml`, set its `apk_version:` to `<new>`, and mark every row
   `unverified: true`.

   **The copy is a SCAFFOLD, never a shipped answer.** The 2.63.0 map was
   copied unverified from 2.62.0 and shipped as a permanent placeholder; the
   drift was only found when a device walk burned wall-clock
   (jjackson/ace#591/#593). CLAUDE.md § close the loop to the source of truth:
   selector values are **device truth**. Do not transcribe from a sibling
   version, and do not back-copy a newly calibrated row into an older map to
   make a test pass.

2. **Run `selector-map-calibrate` against `<new>`.** It owns Steps 0–7: the
   cold-boot, the 10-state walk, the ui-dump harvest, `scripts/probe-atlas-drift.ts`,
   the map reconciliation, the recipe migration off raw resource-ids, and the
   on-device re-run. Do not reimplement any of it here.

   Serialise it (§ Preconditions 2). Its Step 6 — re-running each migrated
   recipe on-device — is the non-negotiable one.

   **This delegation is UNEXERCISED as of 2026-09-06.** The 2.64.0 calibration
   was hand-driven (`adb shell uiautomator dump` per surface) because a dump per
   surface was what the harvest needed. `selector-map-calibrate` may well work;
   nobody has shown that it does. Treat a failure inside it as a finding about
   the delegation, file it, and fall back to the hand-driven loop rather than
   abandoning the calibration — `docs/mobile-calibration/connect-2.64.0-2026-09-06.md`
   is a worked example of the manual path and its output shape.

3. Its product is `docs/mobile-calibration/connect-<new>-<date>.md`. If it
   records residual gaps, they are carried into § Verification, not dropped.

### Step 2b — Cover the version-upgrade prompt (dimagi-internal/ace#1998)

**This screen appears exactly during a version transition, which is why it is
this skill's job and not calibration's.** When CommCare's minimum exceeds the
installed APK it interposes a soft gate instead of launching the app, and there
is no selector coverage for it. Live ui-dump, APK 2.63.2:

```
org.commcare.dalvik:id/prompt_title
  "The application requires CommCare version 2.64.0. You are currently running 2.63.2."
org.commcare.dalvik:id/action_button    "UPDATE COMMCARE VIA THE PLAY STORE"
org.commcare.dalvik:id/do_later_button  "I'LL UPDATE LATER"     <-- dismisses it
```

Today the claim recipe falls through to its `nsv_home_screen` assertion and
captures the failure under `claim-START-HANDOFF-WEDGED-issue629` — a label for
a **different** class (#629 is the INERT `btn_start` handoff, where the launch
never fired; here the launch worked and CommCare deliberately gated it).

During an upgrade, add:

1. Rows in `connect-<new>.yaml`: `commcare-version-prompt-title`,
   `commcare-version-update-later` (`.../do_later_button`),
   `commcare-version-update-now` (`.../action_button`).
2. A guarded `runFlow when visible: <version-prompt-title>` in
   `connect-claim-opp.yaml`, `learn-launch.yaml` and `deliver-launch.yaml`,
   ahead of the `nsv_home_screen` assertion, that **captures under its own
   label and fails** — see the next paragraph.
3. Its own capture label, so the two causes are never conflated again. In
   `connect-claim-opp.yaml` the `...issue629` capture must ALSO become guarded
   on `notVisible: <version-prompt-title>`; adding the new branch without
   excluding the old one leaves both reachable on the same screen.

**RECOGNISE the gate; do NOT dismiss it.** This step originally said the branch
should *tap `do_later_button`*. Implemented 2026-09-06 (ace#1998) as
recognise-and-fail instead, deliberately:

- That `do_later_button` **exists** is recorded device evidence. What
  dismissing it then **permits** is not — no ACE run has observed the
  post-dismiss state. "The gate is soft, so a walk need not die here" is an
  inference from the button's presence, not an observation, and encoding it
  is the mirror image of the thing CLAUDE.md § *a guard that PREDICTS another
  system's rejection must cite a reproducer* forbids.
- If dismissing *does* let the walk proceed, it proceeds on a runtime the CCZ
  itself declares unsupported — and Phase 6 then mints screenshots, QA
  verdicts and a training deck from it. **False green is worse than a clean
  halt.** That is the CLAUDE.md "correctness-skip" footgun: reading one
  system's signal and declining to act on a transition a later step depends on.
- The gate is the authoritative signal that the pin is wrong. Auto-dismissing
  suppresses the single loudest correct message in the system.

Revisit ONLY with an on-device observation of the post-dismiss state. Until
then the remedy is the pin (ace#1997), and the value delivered here is that
the failure is **named correctly** — which was the whole of ace#1998's
complaint.

**Evidence class for this step.** The selector VALUES are device truth (take
them from a real ui-dump; the ace#1998 body carries one for 2.63.2). Which
branch a guard selects and how a capture is NAMED are static structure — a
unit test over the recipe YAML is complete evidence for those, and
`test/mcp/mobile/version-gate-recognition.test.ts` is that test. If you extend
this to *tap* anything, the tap is device truth again: stage it via
`ACE_MOBILE_STATIC_RECIPES_DIR=<repo>/mcp/mobile/recipes/static` plus a full
Claude Code restart (`playbook/integrations/mobile-integration.md § Validating
a palette fix pre-merge`) — a palette staged *next to* the recipe is shadowed
by the palette dir and silently unused. If you cannot reach a device, merge
with the residual **named in the PR** (CLAUDE.md § the device gate is a
PREFERENCE), and say exactly what would falsify it.

Note this is a **mitigation**. The root cause of the gate is the CCZ-vs-APK
mismatch in dimagi-internal/ace#1997.

### Step 3 — Prove every static recipe still navigates

Calibration re-runs the recipes it *migrated*. An upgrade must clear all of
them, because a recipe that touched no migrated row can still break on a
surface the new APK reshaped.

For every file in `mcp/mobile/recipes/static/`:

1. `mobile_validate_recipe` with `apkVersion: <new>` — lint must stay clean
   (watch `runFlow-guard-scope-mismatch`).
2. `mobile_resolve_selectors` with `apkVersion: <new>` — no unresolved
   `${SELECTOR:...}` placeholders.
3. **Run it on-device** as part of at least one full journey (registration →
   claim → Learn → Deliver). A statically-resolved recipe that was never re-run
   is still a guess about whether the recipe *acts* correctly — substitution
   into nested `below:` / `when:` positions has bitten us (jjackson/ace#663).

Record per recipe: `validated` / `resolved` / `ran-on-device` / `not-reached
(reason)`. "Not reached" is an honest residual; a silent omission is not.

### Step 4 — Add the atlas entry

Write `docs/mobile-atlas/connect-<new>.md` from the calibration walk's dumps.
`test/mcp/mobile/static-palette-health.test.ts` keys the expected atlas filename
off `DEFAULT_APK_VERSION`, so Step 5 goes red without it — by design.

### Step 5 — Flip every pin, atomically, in one commit

**Enumerate from a live scan, never from memory.** `lib/apk-pin-sites.ts`
discovers the sites; `test/lib/apk-pin-sites.test.ts` fails if a site exists
that this checklist does not name, and fails if any `pin` disagrees with any
other. That test is the reason this list cannot rot — a fourth pin site in a
new syntax trips its `suspect` scan.

```bash
npx vitest run test/lib/apk-pin-sites.test.ts   # the enumeration, machine-checked
```

**`pin` — MUST all flip together:**

| Site | Form |
|---|---|
| `mcp/mobile/client.ts` | `export const DEFAULT_APK_VERSION = '<v>'` |
| `mcp/mobile-server.ts` | `apkVersion: z.string().default('<v>')` — **twice** (`mobile_validate_recipe`, `mobile_resolve_selectors`) |
| `mcp/mobile/recipe-resolver.ts` | `prepareRecipeForMaestro`'s `apkVersion` default parameter |
| `scripts/probe-atlas-drift.ts` | `process.env.ACE_CONNECT_APK_VERSION \|\| '<v>'` |

**`doc-claim` — prose that asserts what the default IS; flips or it lies:**

| Site | Claim |
|---|---|
| `CLAUDE.md` | `(default APK <v>)` in the `ace-mobile` bullet |
| `playbook/integrations/mobile-integration.md` | `ACE_CONNECT_APK_VERSION` `(default <v>)` |

**`doc-example` — review, may legitimately lag** (illustrative manifest
snippets whose real value is read from the device at capture time):
`skills/connect-baseline-screenshots/SKILL.md`,
`skills/common-screenshot-capture/SKILL.md`. Only the *prose snippets* in those
two files may lag. The *pool they produce* may not: it is a family member,
listed in the next paragraph.

**Version-keyed artifact FAMILIES — an upgrade ADDS a member, never rewrites
one:** `mcp/mobile/selectors/` (`connect-<v>.yaml`, each declaring its own
`apk_version:`), `docs/mobile-atlas/` (`connect-<v>.md`),
`templates/training-deck/_common/composites/` (`connect-<v>.yaml`, the composited
pool frames' spec, § Step 7b), and the **Drive**
common screenshot pool `ACE/_common/connect-screenshots/<v>/` (`manifest.yaml`
+ PNGs). Training decks and FLW guides resolve that pool by the pinned version,
so a pin flip without a matching pool leaves every `ref: _common/platform-setup`
slide and every common-navigation guide step with nothing to show. The pool is
not in git, so the pin-site test cannot see it. § Step 7b produces it, and
`bin/ace-doctor`'s `common_screenshot_pool` probe fails while it is missing.
That is how 2.64.0 shipped with no pool for six weeks: the pool was listed only
as a `doc-example` (dimagi-internal/ace#3060).

**`vault` — flips by hand, outside git:** `ACE_CONNECT_APK_VERSION=<v>` in
ACE's Canopy vault on canopy-web (agent `ace`, Settings → Credentials). It is
what every machine's and runner's `.env` is written from, so a repo-only flip
leaves every install on the old version. Set it after the PR lands, then Step 7.
The pin-site test cannot see it.

**Never sed the whole repo.** `2.63.2` → `2.64.0` across the tree rewrites the
historical maps, the atlas for older versions, and every CHANGELOG entry.

### Step 6 — Ship

`npm test` + `npx tsc --noEmit` green, then follow `skills/shipping`
(bump → PR → arm auto-merge → **wait** → verify it landed). VERSION collisions
are expected — `bash scripts/version-bump.sh --rebase-first` then
`git push --force-with-lease`.

State the evidence class in the PR body: which parts are device-validated
(selector map, the #1998 branch, the recipe runs) and which are static (the pin
flip, the pin-site test).

### Step 7 — Activate, in this order

The order is the whole point, and reversing it fails silently.

1. **Set `ACE_CONNECT_APK_VERSION=<v>` in ACE's Canopy vault, then
   `/ace:setup --force-env`** (it runs `canopy agent env --plugin ace` and keeps
   local-only keys like `ACE_WEB_PAT_TOKEN`). `/ace:update` does **not** touch
   the installed `.env`, so the machine stays pinned to the old version until
   this runs.
2. **Then quit and reopen Claude Code — a full process restart.** Every MCP
   server calls `dotenvConfig()` at module top level and consumes the result at
   import, so a subprocess spawned *before* the `.env` write holds the old value
   for its whole life (ace#880: the connect MCP came up at 21:17:09, `.env` was
   written at 21:17:54, and the registry read the stale value with a correct
   parser). `/reload-plugins` reloads skills/agents/commands/hooks and does
   **not** respawn MCP subprocesses.
3. **Confirm the running subprocess, not the version files.** `VERSION` and
   `installed_plugins.json` are on-disk facts a live session can have rewritten
   *after* spawning its children:

   ```bash
   ps -eo ppid,command | awk -v c="$PPID" '$1==c' | grep -o "0\.13\.[0-9]*"
   cat ~/.claude/plugins/cache/ace/ace/<dir-from-above>/VERSION
   ```

   The directory NAME can lie (it comes from `plugin.json`, the contents from
   the marketplace clone's HEAD); the `VERSION` file inside it is authoritative.

4. **Recipes do not hot-patch their way out of this.** `mcp/mobile/recipes/*.yaml`
   are re-read per call — but from **the version directory the subprocess was
   LAUNCHED from**, not the newest on disk. Patching the newest cache dir after
   an update does nothing, with no symptom. Measured: a device walk ran against
   recipes 15 versions stale, five of them changed (ace#1500).

### Step 7b — Produce `<new>`'s common screenshot pool

Run `common-screenshot-capture` against the device that now runs `<new>`. It
writes `ACE/_common/connect-screenshots/<new>/`. This step is required. The
previous version's pool is not a substitute: a deck that reads it shows the old
UI captioned as the current one, and a deck that finds no pool at all degrades to
prose without saying so.

- **Bar:** every alias that was `source: live` in `<old>`'s manifest is `source:
  live` in `<new>`'s, or has a named reason in the manifest `note`. Quarantined
  aliases (`sync-button`, ace#1832) and template assets (the PersonalID
  completion screens, ace#873) stay as they are.
- **Distinctness:** Step 5.5 of that skill (`classifyPoolDistinctness`) must pass
  before anything is published as `live`.
- **Opp-agnostic frames:** `connect-home` and `claim-opp` always show a real
  program, so they are published **composited**: the new version's real capture
  with only the opp strings replaced (`common-screenshot-capture` § Step 5.4).
  Add `templates/training-deck/_common/composites/connect-<new>.yaml`. Its
  coverage check refuses any string the new APK added until a rule accounts for
  it.
- If the device leg cannot run this session, say so in the verification
  checklist (row C6) and leave the upgrade's tracking issue open. Do not mark the
  upgrade done.

### Step 8 — Verify (§ Verification checklist)

Run the checklist below and write it to
`docs/mobile-calibration/connect-<new>-upgrade-verification.md`. This is the
half the operator says was missing: the artifact that answers *"does everything
still work in the new version."*

## Verification checklist

Each line names what it ASSERTS, so a green tick is a claim someone can check.

**A. The pin actually took**

| # | Assert | How |
|---|---|---|
| A1 | `bin/ace-doctor` `selector_map_currency` is `pass`, and `pin` == `code_default` == `newest_map` == `<new>` | `bin/ace-doctor` |
| A2 | The residual names exactly which rows are `unverified` and why (`rows_unverified: 0` is the ideal, not the bar — see below) | doctor block |
| A3 | `unresolved_selectors: []` | doctor block |
| A4 | `env_freshness` names no stale pid | doctor block |
| A5 | The live MCP subprocess runs the merged version | the `$PPID` + inner-`VERSION` read in Step 7.3 |
| A6 | The device actually runs `<new>` | `dumpsys package org.commcare.dalvik \| grep versionName` |
| A7 | Every `pin` site agrees and no unclassified pin site exists | `npx vitest run test/lib/apk-pin-sites.test.ts` |

**A2 in full, because the strict reading is not reachable in one pass.** A
calibration walk can only verify the surfaces it can REACH, and most of the
unreached ones need a fresh `/ace:run` opportunity: Learn completion is one-way
per `(test user, opportunity)` (#568), so the Learn assessment, the Deliver
download gate and the case list cannot be harvested off a borrowed opp. The
2.64.0 pass ended at 46 verified / 45 unverified for exactly that reason, and
demanding zero would have meant either blocking the upgrade or laundering rows —
the failure mode this skill exists to prevent.

So the NAMED-RESIDUAL form is the bar, and `rows_unverified: 0` is the thing to
converge toward on the next walk. `bin/ace-doctor` already agrees: its
`selector_map_currency` probe PASSES with unverified rows and emits an `info`
(`bin/ace-doctor:2964-2966`); only UNRESOLVED selectors warn. Nothing downstream
requires zero. What is not optional is the naming — list the rows, and for each
one the surface and why it was not reached.
**B. The device still works**

| # | Assert | How |
|---|---|---|
| B1 | A cold boot reaches the precondition (registered demo user at Connect home) | `mobile_ensure_avd_running` |
| B2 | The APK downloads — the asset convention resolved | no `APK_DOWNLOAD_FAILED` in the boot log |
| B3 | Registration incl. the camera/photo surface completes | the cold-boot registration recipes |
| B4 | Claim → Learn → Deliver walks end-to-end on one journey | `mobile_run_recipe` per Step 3 |
| B5 | Every static recipe is `validated` + `resolved` + `ran-on-device` or has a named reason | Step 3's per-recipe table |
| B6 | The version-upgrade prompt branch — **see the caveat below; usually NOT verifiable in this session** | Step 2b |

**B6 in full: this one is structurally unverifiable during the very upgrade
that fixes it.** The version-upgrade prompt fires only on version SKEW — the
live 2.63.2 capture read *"The application requires CommCare version 2.64.0. You
are currently running 2.63.2."* Installing `<new>` removes the precondition, so
by the time you reach the checklist the screen cannot be made to appear. Tested,
not assumed, on 2.64.0: a fresh CCZ install on a wiped device went straight to
`StandardHomeActivity`, and

```
$ grep -l "prompt_title\|do_later_button" docs/mobile-atlas/evidence/connect-2.64.0/*.xml
(no matches)
```

Two consequences, and Step 2b's "validate the branch on-device in this session"
must be read against them:

1. **Capture the rows from the OLD version's failure dump BEFORE the pins flip**
   — that is the only window in which the surface exists. Do it in Step 0.
2. **Then mark B6 `unverifiable-post-upgrade` and ship the dismissal branch as
   DEFENCE for the next skew,** flagged `unverified` in the map. That is an
   honest residual, not a skipped check. Re-manufacturing the skew (downgrading
   the APK under a CCZ that requires the new one) to satisfy a tick costs a
   device walk and proves something the next upgrade will re-prove for free.

**C. The rest of ACE still agrees with the new pin**

| # | Assert | How |
|---|---|---|
| C1 | `npm test` green | `npm test` |
| C2 | `npx tsc --noEmit` clean | `npx tsc --noEmit` |
| C3 | The atlas for `<new>` exists (the palette-health ratchet keys on it) | `docs/mobile-atlas/connect-<new>.md` |
| C4 | **`app-release-qa`'s CCZ min-version check changed disposition** — see below | re-read `lib/ccz-min-version.ts`'s severity table |
| C5 | The calibration report's residual gaps are carried forward, not dropped | `docs/mobile-calibration/connect-<new>-<date>.md` |
| C6 | The common screenshot pool for `<new>` exists in Drive, and every alias that was live in `<old>` is live (or has a named reason) and distinct | `bin/ace-doctor` `common_screenshot_pool` is `pass`, plus the pool's `verdict.yaml` from § Step 7b |

**C4 in full, because completing this skill CHANGES another check's behaviour.**
`lib/ccz-min-version.ts` compares a released CCZ's `profile.ccpr` minimum
against the pinned APK, and its severity keys on whether a remedy is *reachable*:

- `required <= pinned` → `ok`.
- `required > pinned`, **a selector map covering `required` exists** → `blocker`.
- `required > pinned`, **no such map** → `warn`.

So the moment this skill lands `connect-<new>.yaml`, every run whose CCZ requires
`<= <new>` flips `ok`, and any run still requiring MORE than the pin flips
`warn` → **`blocker`**, because repinning is now something an operator can
actually do. That is intended: the check gets sharper as coverage lands. Say so
in the PR, and expect Phase 3 to start halting on mismatches it previously only
warned about.

## Rollback — if the new version is bad

The upgrade is designed to be reversible because the old map is never deleted.

1. **Stop before blaming the APK.** Read `failureForensics.screenshotPath` +
   `.uiDumpPath` on any recipe failure first
   (`playbook/integrations/mobile-integration.md § Failure forensics`); a
   `-FAILURE.xml` element tree distinguishes "wrong selector" from "wrong
   screen" in one step. And if something that WORKED now fails, run
   `upstream-regression-triage` before concluding the APK is at fault.
2. **Fast, machine-local revert (no PR):** set
   `ACE_CONNECT_APK_VERSION=<old>` in the installed `.env`, then **restart
   Claude Code** (Step 7 order applies in reverse too). The old map is still on
   disk, so this is a complete rollback of runtime behaviour. Expect
   `selector_map_currency` to report `fail` with *"pin is stale (behind code
   default)"* — that is the pin doing its job, and it is the signal that a repo
   rollback is still owed.
3. **Repo revert:** revert the Step 5 commit (all pins move back together —
   which is why they shipped together). **Keep `connect-<new>.yaml` and the
   atlas**: they are live-measured evidence and cost a device walk. Deleting
   them throws away the only calibration you have and re-enters the
   transcribed-map class the next time someone tries.
4. **File what you learned** against `dimagi-internal/ace` with the run/repro,
   labelled `blocks-e2e` if a run cannot complete. Search first, in its own
   Bash call. Self-heal it if the fix is bounded.

## Related skills

- `selector-map-calibrate` — the live-device state walk this skill delegates Step 2 to. Systematic, per-APK-version, manual.
- `selector-map-heal` — narrow, reactive, additive-only repair from ONE failure dump. Not an upgrade path; it never flips a pin.
- `upstream-regression-triage` — when a path that worked now fails and ACE's own code is unchanged.
- `shipping` — the bump → PR → wait → merge → verify mechanics for Step 6.

## Failure modes

- **Pinning a version whose asset does not resolve.** `APK_DOWNLOAD_FAILED` on a
  published release, because Dimagi renamed the asset again (the 2.63.2 case).
  Step 1 is the guard, and it gates on an `.apk` ASSET, not on `isDraft` —
  2.63.3 is published but ships only an `.aab` (verified 2026-09-06), so a
  draft-only check would have waved it through.
- **Transcribing the map from the sibling version.** The 2.63.0 placeholder
  problem (#591/#593). The copy is a scaffold; calibration is the answer.
- **Reading "zero selector drift" as "nothing to do".** An APK that renames
  nothing can still insert a whole SCREEN into a flow every recipe walks —
  2.64.0's PersonalID email step (ace#2029) did exactly that, and it is invisible
  to a selector-centric check by construction. Step 1b's resource-table `comm` is
  the guard, and it costs one command.
- **Calibrating the OLD APK.** Nothing but Step 2.0 installs the new one, and
  `mobile_ensure_avd_running` installs whatever the INSTALLED `.env` says. The
  bootstrap reports success either way; the branch says `<new>` and the device
  runs `<old>`.
- **Assuming the release asset name progresses.** It does not: 2.64.0 reverted to
  2.62.0's `app-commcare-release.apk`. Read it off the release (Step 1).
- **Flipping some pins and not others.** `mobile_resolve_selectors` then reads a
  different map than the runtime loads, and the disagreement is invisible until
  a device walk. Step 5 + `test/lib/apk-pin-sites.test.ts` are the guard.
- **Comparing versions as strings.** `'2.64.0' < '2.9.0'` and `'2.63.10' <
  '2.63.9'`. Use `compareVersionTriples` from `lib/ccz-min-version.ts`; never
  write a third comparator.
- **Restarting before `/ace:setup --force-env`.** The MCP children re-read the
  OLD `.env`, and nothing surfaces it except `env_freshness` (ace#880).
- **Hot-patching the newest plugin-cache dir.** A live subprocess re-reads
  recipes from the directory it was LAUNCHED from; the patch is faithfully
  ignored (ace#1500).
- **Consuming the Learn precondition to "diagnose".** One-way per
  `(test user, opportunity)`; the only restore is a fresh `/ace:run` (#568).
- **Treating a peer's AVD as a dead device.** Many concurrent `ace-mobile` MCPs
  share few AVDs; the adb port is allocated, not fixed. Ask `mobile_diagnose`.

## Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-16 | **The Drive common screenshot pool is now a version-keyed family member (dimagi-internal/ace#3060).** 2.64.0 shipped with no `ACE/_common/connect-screenshots/2.64.0/`. The skill listed the two screenshot skills only as `doc-example` ("may legitimately lag"), and the families list named only the git-side families. Nothing failed, so `_common/platform-setup` decks could not render and the tekzal/20261013-2314 FLW guide fell back to prose. Added the pool to Products and Families, a new § Step 7b that produces it, and checklist row C6, which is gated by doctor's `common_screenshot_pool`. | ACE team |
| 2026-09-06 | First execution (2.64.0), and everything it produced. **Premise errors the skill would have propagated:** the asset-convention table implied newest-wins (2.64.0 REVERTED to the 2.62.0 name — measured, now a 4th row + `test/mcp/mobile/apk-asset-conventions.test.ts`); Step 1 gated on `isDraft` (2.63.3 is published with an `.aab`-only asset, so the real test is "has an `.apk` asset"); Step 2b prescribed TAPPING `do_later_button` (changed to recognise-and-fail — the button's existence is recorded evidence, what dismissing permits is not, and a dismissed gate risks false-green Phase 6 artifacts), and the `...issue629` capture was split so both causes cannot be reachable on one screen. **Steps the first execution found MISSING:** **Step 1b** (resource-table `comm` diff — the only step that can see an ADDED screen, which is what 2.64.0 actually shipped: zero id drift, one new registration surface, ace#2029) and **Step 2.0** (install the new APK on the device + verify, before calibrating — nothing else did, and `mobile_ensure_avd_running` installs whatever the INSTALLED `.env` says; includes the `pm enable` GMS note, since `pm enable-user` does not exist). **Checklist rows reframed:** **A2** (`rows_unverified: 0` is unreachable in one pass and not required by doctor — the named residual is the bar) and **B6** (structurally unverifiable during the upgrade that removes the version skew; capture it in the NEXT upgrade's Step 0). Recorded that the `selector-map-calibrate` delegation is still unexercised. Full review: `docs/mobile-calibration/connect-2.64.0-2026-09-06.md`; filled-in checklist: `docs/mobile-calibration/connect-2.64.0-upgrade-verification.md`. | ACE team |
| 2026-09-05 | Initial version. Authored because the previous APK upgrade had no explicit update-version step, so pin sites were missed and nothing verified the new version end-to-end. Orchestrates `selector-map-calibrate`; adds the pin flip, the ace#1998 version-prompt coverage, the activation ORDER, the verification checklist, and rollback. Pin-site enumeration is machine-discovered by `lib/apk-pin-sites.ts` + `test/lib/apk-pin-sites.test.ts`, so this checklist cannot silently rot. | ACE team |
