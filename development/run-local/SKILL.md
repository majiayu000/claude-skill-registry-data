---
name: run-local
description: Run the product's Expo app and its API on this Mac, on an Android phone, an Android emulator or an iOS Simulator, in one command — the script checks what the Mac is missing, shows it all at once, installs it after one yes, starts the database and the API, launches the app (without rebuilding what is already installed), and when a step fails keeps the error so Claude can read it, propose the fix and try again. It also reports what is running, shows its logs and cleans native build state, as data Claude reads. Only for projects the profile marks `mobile`; macOS only for now. Use when the user says "run local", "correrlo local", "corré la app", "levantá el entorno local", "probalo en mi teléfono", "abrilo en el simulador", "no me anda el build", "run-local", after project-new's skeleton, or when the dashboard shows the local environment not set up.
---

# Run local — the app and its API on a phone, an emulator or a simulator

The work is done by `.keelokit/bin/run-local.sh`, which every Keelokit project carries (new or
adopted) and which runs without Claude and without the plugin: `bash .keelokit/bin/run-local.sh`
(`pnpm run run:local` in generated projects). This skill runs it, reads what it leaves behind when
something fails, and repairs. Solo macOS: on another system the script says so and stops.

Settings live in the `[local]` block of `.keelokit/profile.toml`; whatever it leaves out, the script
detects from the repo. Messages come in the project's language (`[dashboard] lang`).

**Never**, without the user's yes for that exact thing: kill a process, stop a container, delete or
regenerate `ios/` or `android/`, uninstall the app from a phone, edit a tracked native folder. Never
type, print or commit a credential, and never write values into an `.env` yourself: the script
copies `.env.example` into the gitignored `.env`; real keys are the user's.

## 1. See where it stands

No `.keelokit/` folder: the project isn't a Keelokit one yet, so there is no script to run. Say so and
offer `/keelokit:project-adopt` (it adds only `.keelokit/`, the script included); come back here after.

Read `[local]` in `.keelokit/profile.toml` and the profile's `traits`. No `mobile` trait: say there
is no app to run here and stop. Then:

- **No `[local]` block** (adopted repos, or a project from before this existed):
  `bash .keelokit/bin/run-local.sh detect` prints what the repo shows, as JSON, with the keys it is
  not sure of in `uncertain`. Show it in plain words (where the app is, how it installs, where the
  API and the database are) and ask only about the uncertain keys, once. With the user's yes, write
  the block (or let `run-local.sh doctor` write it) and tell them to correct by hand whatever is
  wrong. Two Expo apps: ask which. Never write a guess without showing it.
- **In an adopted repo** the script also creates `.local-dev/` (logs, `last-error.txt`) and adds it to
  `.gitignore`: ask before, once, and say what it is.
- **Block present:** `bash .keelokit/bin/run-local.sh doctor --check` says whether it is coherent
  (the app is where it says, the manager exists, the folders exist). Fix a wrong key with the user.

## 2. Diagnose, then run

Read the script's answers as data, not as text to scrape: `doctor --json`, `status --json`, `logs`
and the exit code. Exit codes: 0 done, 1 failed or something is missing, 2 usage, 3 stopped on
something only a person can do (Xcode, no phone, no emulator image), 4 a question was declined or
there was no terminal to answer it. `bash .keelokit/bin/run-local.sh <command> --help` says what each
command and flag does.

1. `bash .keelokit/bin/run-local.sh doctor --json` lists everything the Mac is missing at once and
   installs nothing:
   `{"exit":3,"ok":false,"messages":[{"level","text"}],"missing":[{"label","command"}],"blockers":["…"]}`.
   Show `missing` in plain words (Homebrew installs, an Android SDK, Node through nvm, a `sudo`
   prompt) and `blockers` as what is the user's to do: Xcode, a phone with USB debugging on, Expo Go
   on an Android phone.
2. `bash .keelokit/bin/run-local.sh status --json` says what already runs, so nothing is started
   twice or killed by surprise (`api.owned` false means another project's API holds the port: the
   script will offer its next free port, or stop and ask; never reuse it): `api`, `database.services`, `metro`, `android.devices` (phones and
   emulators, with `kind`), `ios.booted`, and `ports` with the pid and the process that holds each.
3. Ask before launching, with the multiple-choice question tool: at most three short questions, only
   the ones that apply, the last answers as defaults. Run in a terminal by the user, the script asks
   the same questions itself; run by you, it must never have to, so map every answer to a flag:
   - **Target**: a connected phone, which emulator (or a new one), the iOS simulator, only Metro, or
     only the API and database. `android --phone` or `android --emulator` (`--device <AVD|serial|model>`
     picks a specific one; `--new-avd` makes an emulator); `ios`; `metro`; `backend`. Ask it only when
     there is a real choice (`status --json`: a phone in `android.devices` and an emulator possible).
     One at a time; the script shuts other simulators down.
   - **Seed**, only when the project has a seed (`api_seed` in `detect`): "Load the seed data?" with
     the recommendation: the script says "the database looks empty" when it can tell (through
     `docker compose exec <db> psql`) and otherwise "can't tell if it already has data". Always the
     user's own yes: `--seed` or `--no-seed`. `--yes` alone never seeds.
   - **Rebuild or fast relaunch**, only when the app is already installed on the target and its
     native inputs are unchanged since the last install (the script prints "no native build: …" when
     that is so): default fast, `--no-build`; the other answer is `--rebuild`. Without that
     situation do not ask: it builds.
4. After the user accepts the list and the answers, run the target with `--yes` and the flags (`--yes`
   never waits on a menu: it takes the remembered or first simulator, phone or emulator and says
   which; without `--yes` and without a terminal it exits 4 after 20 seconds, so a menu is never a
   hang): `bash .keelokit/bin/run-local.sh <target> --yes --phone --no-seed`. Metro keeps running in
   it (the script gives it an input that never ends when there is no terminal, so it survives being
   run in the background): run it where the user can see it, or in the background and read `logs`.
   If it reports "Metro exited on its own" (exit 1), the app is installed but has no Metro: read the
   log and run it again.

**It does not rebuild what is already there.** The first run builds the native app (10–20 minutes:
say so). A later `android` or `ios` finds the app installed on the target and the native inputs
unchanged since the last successful install, and only starts Metro and opens the app; it prints
which path it took and why. `--rebuild` builds anyway (after a native dependency or config change the
script does it by itself), `--no-build` refuses to build and fails if the app is not installed.

**A known iOS behaviour.** Opening the app by its link makes iOS show a system dialog, Open in "<app>"?,
that someone must tap in the simulator, every time; Android has no such prompt. The script says so and
opens the link; tell the user to tap Open. Launching the app first was tried on hardware and does not
help: the dev launcher opens but does not reconnect to Metro by itself.

**Android targets.** One phone connected: it is used. Several: the user chooses, and it is remembered
(`--device <serial|model>` overrides). Wireless: `pair` walks through it and asks for the pairing
address, lets adb ask for the code, then the connect address: never type or keep the code yourself.
No phone: the script offers an emulator. If there is no emulator it offers to create one, and says
that the system image is a 1–2 GB download: relay that, and only run with `--yes` after the user
accepted the download. `--new-avd` creates a new emulator with an 8 GB data partition (an installed
image is reused, no download). On `INSTALL_FAILED_INSUFFICIENT_STORAGE` the script offers, each with its
own yes: uninstall the app and retry, a new emulator, or a cold boot with `-wipe-data`, which erases
that emulator's apps and data: name the emulator and get that yes yourself; with `--yes` it exits 3
listing the options and picks none. An emulator needs hardware acceleration (HVF on macOS); if it complains, say
so plainly and suggest a phone.

**Other things it asks.** The seed (`api_seed`) writes to the database: it is offered once, never
silent, and `seed` runs it by name. `[local] services` (redis, mailpit...) start and stop with the
database. Node and the JDK come from the project; a Node from nvm is used for the run only, and
installing one is in `missing`, so it is the user's yes.

With Expo Go and `--yes`, the script answers Expo's "Install the recommended Expo Go?" with yes: it
downloads Expo Go from Expo and installs or updates it on the target, so only pass `--yes` once the user
has accepted that. If the prompt could not be answered it exits 3 and says so.

The script chooses between Expo Go and a development build (`client` in `[local]`: `auto`,
`expo-go`, `dev-client`) and says which and why. In a simulator build it can remove capabilities a
simulator can't run (Sign in with Apple, associated domains, push) from the generated `ios/`: it
shows the list and asks once. It never does it to a git-tracked `ios/` or for a phone; for a phone
without a developer certificate, explain what is missing and stop.

## 3. When it fails

The failed step's log tail is in `.local-dev/last-error.txt`; read the rest with
`bash .keelokit/bin/run-local.sh logs [step]` (newest first; a step name gives its last 100 lines).
The script already repairs a few known causes once (listed in `REPAIRS`, the first block of the
script: a different signature on the phone, port 8081 or 5554 taken, Gradle out of memory,
CocoaPods' index, an emulator lock file, a missing Google services file). For the rest:

1. Read `last-error.txt`, then the log around the first real error, not the last line.
2. Say in one sentence what broke and **propose** the fix. Wait for the yes if it kills a process,
   stops a container, removes something or reinstalls native folders. Otherwise apply it.
3. Run the same target again. After **two** repairs of the same run, stop: say what was tried and
   what is left, and don't keep going.
4. If a failure repeats across projects, suggest adding a line to `REPAIRS` and a `repair_<action>`
   function in the template's `run-local.sh`. A local edit to the project's copy is overwritten by
   `/keelokit:harness-upgrade`.

Disk and stale native state: `bash .keelokit/bin/run-local.sh clean` lists, group by group, what it
would delete with sizes (build caches, this project's Xcode DerivedData, the generated `android/` and
`ios/`, the logs) and asks per group. It never touches anything git tracks or anything outside the
project. Offer it when a build fails in a way a fresh native folder would fix, and tell the user the
next build takes 10–20 minutes again. Never delete those folders any other way.

## 4. After it

Show the test accounts in the summary, from `bash .keelokit/bin/run-local.sh users --json`
(`{"source","accounts":[{"line"}]}`: raw lines from the project's own docs, README section or seed log,
never parsed or invented; `source: null` means none were found, so say how to add `users_file` in
`[local]`). They are local development credentials: show them, never write them anywhere, never read
`.env` files. The script also prints a short "Test users" block when a launch starts and after the seed.

If the app opened and reached the API, say so and how to stop it
(`bash .keelokit/bin/run-local.sh stop` asks before stopping the API, the containers and an emulator;
the data stays). If `[local]` was just written, refresh the dashboard (`/keelokit:project-dashboard`),
which shows "Local environment: ready".

## What is tested and what is not

Tested with simulated commands: detection on many project shapes (pnpm, npm, yarn classic and berry,
bun, turborepo, nx, lerna), the coherence check, the diagnosis, the questions before anything is
killed, stopped, deleted or edited, the decision to rebuild or not, the choice of Android target, how
an emulator image and device are created and booted, status, logs and clean. The script this one grew
from launched an app on the iOS simulator, on an Intel Mac with Xcode 26, and on a Samsung Galaxy S20
over USB. **Never run on real hardware by me:** the emulator, wireless debugging, Expo Go on a phone,
the fingerprint through `@expo/fingerprint`, opening the dev client by its link, Apple Silicon. Say so
when it matters, and read the failure instead of assuming the path works.
