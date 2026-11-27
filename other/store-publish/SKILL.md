---
name: store-publish
description: "Ship a web game as a website, a signed APK download and a Google Play release, repeatedly, by workflow. Use when yskills says APK, Play Store, Google Play or 'push the game to the store'."
---

# Store publish: website, APK, Google Play

Written 2026-10-12 for yskills' goal: keep shipping small games to the Play Store for experience.
A fresh project Claude reads this file once and does everything marked **Claude**. Research
behind it: `/mnt/project-files/claude-setup/research/stores-automation.md` (its [U] facts stay
unverified until a Learnings line says otherwise). Money and review rules for paid apps: `store`.
Marker **[U]** = not tested yet; the first real run confirms or fixes it, then Learnings records it.

## What you get

| Output | How | Status |
|---|---|---|
| 1. Website | `publish` skill (new-project workflow), the game's web build | covered |
| 2. Signed APK, downloadable from the website | tag `v1.2.3` runs `android-release.yml`, APK on a GitHub Release, website links `releases/latest/download/<name>.apk` | build tested in CI (`store-publish-test`), release and link [U] |
| 3. Google Play, repeatedly | same workflow uploads the AAB to the internal track with the Play Developer API | [U] until the first real upload |
| Steam, App Store | not now: Steam via `game-3d` + research file §4, App Store via `store` + research file §3 | later |

## Decisions (do not re-decide)

| Question | Choice | Why |
|---|---|---|
| Wrapper | Capacitor, game files bundled in the app | one build gives APK and AAB, works offline; a TWA is only a browser tab on your website and needs `assetlinks.json` |
| Play upload | `r0adkll/upload-google-play` pinned by SHA | one step, no Gradle or Ruby changes; Gradle Play Publisher and fastlane `supply` need more setup |
| Signing | one upload keystore for all games, kept on the laptop, base64 in each app repo's Actions secrets | Play App Signing re-signs for Play, so a lost upload key can be reset; the website APK key cannot |
| Signing step | `sign-android.sh` (`apksigner`, `jarsigner`) as its own workflow step after an unsigned build | npm, the web build and Gradle run with no secrets; the keystore never touches project files |
| Who may sign | only a commit that is on `main` (the workflow checks it) | a tag or manual run from a branch cannot get keys |
| Version | tag `vX.Y.Z`; `versionCode = X*10000 + Y*100 + Z` | Play needs a code that only grows; no counter to keep |
| Application id | `studio.yverse.<name without dashes>` | permanent once on Play: choose it once, in `capacitor.config.json` |
| APK hosting | GitHub Release of the app repo, no new service | needs a **public** repo (below) |
| Tracks | internal first, closed test next, production only after yskills presses it | production needs Google's 14-day closed test (12 testers) on new personal accounts |

**Secrets exception:** `docs/USING.md` (The world) says projects keep no secrets in GitHub. The signing key and the
Play service account cannot live anywhere else, because the APK is built in Actions. They live only
in the app repo's Actions secrets (names below), are set from the laptop, and are never printed.
One keystore is shared by all games, so one leak exposes all of them: keep the laptop file private and
rotate only on yskills' word (rotating a secret is an ask-first item).

## Can do / only yskills / cannot

| Claude can | Only yskills | Nobody can |
|---|---|---|
| Wrap the web game, set the app id, icons, version | Play developer account (ID check, $25) | Skip Google's review (hours to days) |
| Build, sign, publish the APK and the website download page | Create each app in Play Console, Data safety, content rating (Claude drafts answers) | Skip the 12 testers x 14 days before production |
| Generate the keystore and set repo secrets (laptop route) | Service account JSON once (hands step 3) | Upload the first app version by API [U] |
| Upload the AAB to internal, closed or production tracks | Press "Apply for production", add testers' emails | Test on a real phone (yskills installs and says what happened) |
| Write listing text, release notes, screenshots | Make the repo public (a card first) | |

## The guide (a fresh project Claude follows this)

1. **Web game live.** `publish` skill, `docs/USING.md` (Deploy a page). The game must run from static
   files in a folder (`dist` or `www`): Vite or Phaser build, no server routes the game needs offline.
2. **Decide the id and visibility.** `appId` = `studio.yverse.<name>`. Release downloads work for
   anonymous visitors only if the repo is public. A web game's code is public in the browser anyway,
   so the recommended answer is public. Put it in your reply as `Card:` "Make `<name>` repo public so
   the APK can be downloaded?" (recommend yes) and wait for the tap (outward-facing).
   Private repo instead: a Worker route that streams the release asset with a read-only token
   secret [U]; no tap needed, it is a new secret, not a rotation.
3. **Wrap.** In the app repo: `npm i @capacitor/core @capacitor/android` and `npm i -D @capacitor/cli`,
   add `capacitor.config.json` (see `templates/game/`: `appId`, `appName`, `webDir`), run
   `npx cap add android` and commit the `android/` folder (not its `build` folders; `.gitignore` in
   the template). Icons: `@capacitor/assets`.
4. **Copy the templates.** `templates/build-android.sh` and `templates/sign-android.sh` to `scripts/`,
   `templates/android-release.yml` to `.github/workflows/android-release.yml`; replace `CHANGE_ME` in
   the workflow with the app id. `WEB_BUILD_CMD` (env of the build step) overrides `npm run build`.
5. **Keystore and secrets (laptop route).** One RC session on the laptop (`start_rc_session`, folder
   `repos` of `STUDIO_ROOT`). Needs a JDK (`winget install EclipseAdoptium.Temurin.21.JDK`)
   and `gh` as `yskills-claude`. This step is the exception to "no project has secrets in GitHub" (docs/USING.md, The world): keys live in this game repo's
   Actions secrets, nowhere else, never printed, and the one shared keystore means one leak exposes all games.
   First game only; later games reuse the file:
   ```powershell
   mkdir $env:USERPROFILE\keystores
   $pw = -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 24 | % {[char]$_})
   keytool -genkeypair -keystore $env:USERPROFILE\keystores\yverse-upload.jks -alias upload -keyalg RSA -keysize 2048 -validity 10000 -storepass $pw -keypass $pw -dname "CN=yverse-studio"
   $pw | Out-File -NoNewline $env:USERPROFILE\keystores\yverse-upload.pw
   ```
   Per game (never echo the values; the password file stays outside every repo):
   ```powershell
   $r = "yverse-studio/<name>"; $d = "$env:USERPROFILE\keystores"
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("$d\yverse-upload.jks")) | gh secret set ANDROID_KEYSTORE_BASE64 -R $r
   Get-Content -Raw "$d\yverse-upload.pw" | gh secret set ANDROID_KEYSTORE_PASSWORD -R $r
   Get-Content -Raw "$d\yverse-upload.pw" | gh secret set ANDROID_KEY_PASSWORD -R $r
   "upload" | gh secret set ANDROID_KEY_ALIAS -R $r
   ```
6. **First APK.** Open a size-M PR with steps 3 and 4; the gate runs it. After merge: `git tag v0.1.0 && git push origin v0.1.0`
   (if a cloud thread cannot push tags, dispatch `android-release` with `version` 0.1.0 instead [U]). Check the run with `actions_get`, and that the Release holds `<name>.apk`.
7. **Website download.** Add a section "Android" to the game's page: button to
   `https://github.com/yverse-studio/<name>/releases/latest/download/<name>.apk`, the SHA-256 from
   `<name>.apk.sha256`, and a two-line install hint (German first: "Download, öffnen, 'Aus dieser Quelle
   installieren' erlauben"). Playing in the browser stays the first button. Legal pages as always (`legal`).
   Android may warn about unknown apps; the page says so. From 2027 Google also wants sideloaded apps
   registered by a verified developer (research file, Google Play "Gotcha 2026") [U].
8. **Google Play, once per game (hands steps 1 and 2 first).** Upload the AAB from the first run
   (run artifact `android-0.1.0`; yskills downloads it from the run page) by hand to Testing > Internal testing > Create new release [U]. After that every tag uploads automatically.
9. **Service account (hands step 3, once), then secret per game** (same exception as step 5:
   the Play key lives only in this game repo's Actions secrets, never printed): `PLAY_SERVICE_ACCOUNT_JSON` from the
   JSON file on the laptop: `Get-Content -Raw <file> | gh secret set PLAY_SERVICE_ACCOUNT_JSON -R $r`.
10. **Release again.** New tag `v0.2.0` builds, releases and uploads to `internal`; yskills installs
    from the Play link on the phone. For a closed test or production dispatch the workflow with `play` true
    and `track` alpha or production, or press promote in Play Console (production is always yskills' button).
    First upload of a never-published app may need `status: draft` [U].
11. **After each run**, append to Learnings if anything surprised you (below), and say `Done:` with the links.

## Hands steps for yskills (one at a time, Claude re-sends the one needed)

1. Why: only you can pay and prove who you are (about 25 min, then a wait). Open
   https://play.google.com/console/signup, choose "Personal", fill name, address, phone, pay $25, upload ID.
2. Why: each game needs its own entry (5 min per game). In Play Console press "Create app", name, language
   German, "Game", "Free", tick the declarations; leave "Play App Signing" on. Claude sends the name and
   the answers for Data safety and content rating (Play Console > Policy and programs > App content).
3. Why: Claude needs a robot login (about 12 min, once). Open
   https://console.cloud.google.com/apis/library/androidpublisher.googleapis.com and press "Enable";
   open https://console.cloud.google.com/iam-admin/serviceaccounts, "Create service account", name
   `play-publisher`, then its "Keys" tab, "Add key", "Create new key", JSON. In Play Console >
   "Users and permissions" > "Invite new users", paste the service account's email, role "Release Manager"
   (the older "Setup > API access" page may exist instead) [U]. Save the JSON on the laptop as
   `%USERPROFILE%\keystores\play-service-account.json`. Never paste it in chat.
4. Why: Google's rule for new personal accounts. Testing > Closed testing > add 12 testers' emails, send
   the opt-in link, keep them 14 days. Start early. Then Dashboard > "Apply for production" (5 min).

## Untested (as of this PR)

Built and signed in CI: APK, AAB, version code, signature. **Not yet run against real accounts:** Release
upload on a tag, the public download link, the Play upload step and its `status`/`track` inputs, the
first-upload-by-hand rule, the service-account role, `gh secret set` from the laptop, tag push from a
cloud thread. Mark each Learnings line with what you actually saw.

## Learnings

Every project that hits a problem or a surprise with this pipeline appends one dated line here, in the
same turn it fixes the problem: open a size-S PR against `yverse-studio/claude-setup` that only edits
this section (`add_repo` claude-setup first), format
`- YYYY-MM-DD <project>: what went wrong -> what fixed it (tested | assumed)`. If the fix changes a step
above, edit that step too. Friction with the skill itself is also a `loop:setup` issue (`operator`).

- 2026-10-12 (template): nothing run against real accounts yet; see Untested.
