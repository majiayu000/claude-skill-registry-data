---
name: mod-anything
description: Change or extend software or a device the user owns but whose source they don't control (a desktop app, a website, a game, a device protocol, a CLI) by the cheapest route that reaches the idea. The running original is the oracle, a journal and a stall breaker keep long runs honest, and every run ends in a field note for the next agent. Generalizes rehan-remade/universal-modder's mod-any-game method beyond games. USE WHEN the user wants an app or site to do something it doesn't, to add a feature or automation to a third-party app, to hook into or extend a desktop app, to reverse-engineer a device or file format they own, or to bridge two programs; or asks "can I mod X?", "mod any app", "make <app> do <thing>". NOT FOR code whose source you control (edit it), online games or services behind anti-cheat or anti-automation, bypassing DRM, licence, integrity or ownership checks, or anything the target's terms prohibit.
license: MIT
compatibility: Any agent that can read files and run shell commands. Scripts need Python 3.9+ (stdlib only). publish_check.py uses gitleaks 8.x when it is on PATH and says so when it is not. recon_macos_app.py needs macOS (it calls codesign). No network access needed.
metadata:
  version: "0.1.0"
  author: broomva
category: tooling
tier: D
---

# mod-anything

You are the modder. The user names a target they own and an idea in one sentence; you take it
to *working in the real target, with evidence*, by the cheapest route that reaches the idea.

The method comes from [universal-modder](https://github.com/rehan-remade/universal-modder)
(MIT), whose `mod-any-game` skill shipped game mods and cross-game mashups. Nothing in it is
specific to games. This skill keeps its loop and generalizes it to apps, websites, devices and
CLIs. Every route is a rung on one ladder, and the rules come from the law's own line between
*studying* a program and *shipping* it.

## The loop

Run these steps in order. Steps 0, 2, 8 and 9 are not optional, even for a small mod.

In the commands, `$S` is this skill's folder (where this SKILL.md lives) and `<work>` is the
run's working folder. `modlog.py ...` is short for `python3 $S/scripts/modlog.py --dir <work> ...`.

`<work>` is a fresh folder outside every git repo (`mktemp -d`). The journal, the deny file
and the logged-in evidence all live there, and none of them should be one `git add` away from
a commit. `modlog.py init` refuses a folder inside a repo.

**0. Intake.**
- Get the target with its exact version, the idea in one sentence, and what *done* means. The
  default for done is: working in the real target, with a screenshot, log or dump as evidence.
- Check the envelope first (§Rules). If the target's terms forbid modification, or the idea
  needs a protection defeated, stop and say so. Check the terms of any companion app you
  will read too (a device's phone app is licensed software).
- Start the journal:
  `python3 $S/scripts/modlog.py --dir <work> init --target "<app> <version>" --idea "<one sentence>"`
- If the user names a domain rather than a target ("mod any app", "an editor"), run step 1
  first and start the journal once recon has picked the target. Record recon facts and the
  lab's restore path with `modlog.py log --text "..." [--evidence <file>]`; it needs no route.

**1. Recon.**
- Search the shipped field notes first: `grep -ril "<target>" $S/field-notes/`.
- If a recon adapter exists for the domain, run it: `python3 $S/scripts/recon_macos_app.py
  <App> --json` for macOS apps. Otherwise collect by hand: what the target is built on, which
  extension points it exposes, what protects it, and where its state lives.
- Record the version the target actually runs, not only the one its bundle declares. Obsidian's
  Info.plist said 1.8.4 while the app ran 1.13.7 downloaded into its profile.
- Domain knowledge is in `references/playbooks/` (macOS apps today).

**2. Pick the cheapest rung that reaches the idea** (§The ladder). Record the choice and the
reason *before* building:
`modlog.py route --rung 2 --name "VS Code extension API" --reason "sanctioned, covers hovers"`

**3. Lab.**
- Work in an isolated profile so the user's real state is never touched: `--user-data-dir`,
  a copy of the vault, a test device. The playbook lists the knobs per app family. For
  Chromium-based apps (Electron, Chrome, Arc), always add `--use-mock-keychain`.
- For a CLI, the lab is its config pointed into `<work>`: `GIT_CONFIG_GLOBAL`,
  `XDG_CONFIG_HOME`, or `HOME` for tools that read only that, plus synthetic input data.
- For a website, the lab is a fresh browser profile that the user logs into themselves.
  - A copied browser profile is never a lab: it carries cookies and saved logins. Never read
    cookies or tokens out of the user's real profile either.
  - A logged-in lab still holds the user's session: open a DevTools port on it only for the
    session, and close it after.
- Anything captured from real use stays in `<work>`: DOM dumps, logs and screenshots from a
  logged-in lab, traffic captures, device recordings. It carries the user's data and other
  people's, and a device capture can carry addresses, serials and keys. Evidence you publish
  comes from a fixture you wrote (a local page, synthetic entities, a hand-written frame), as
  in `examples/obsidian-kg-claims`.
- A lab that raises system UI on the user's screen is touching the user's environment: a
  keychain prompt, a permission dialog, a focus change. Stop it by exact PID and fix the lab
  before going on.
- A lab is not a sandbox. It shares the installed app, its updater, the user's macOS
  permissions and the user's file access.
  - Where the app allows it, turn auto-update off in the lab, and check whether the updater
    writes into the lab or into `/Applications`. Obsidian's writes into its profile. If it
    writes into `/Applications` and cannot be turned off, that is the user's environment:
    ask.
  - Code you load in the lab (a plugin, an injected script) runs with the user's own file
    access.
- Back up anything you will change, and write the restore path in the journal
  (`modlog.py log`).

**4. Read the source of truth.** Read the actual code, manifests, scripting dictionaries,
traffic or data. Your reading is a hypothesis; step 5 tests it.

**5. Vertical slice, verified in the running target.**
- Take one feature all the way through, then widen.
- The running original is the oracle; your reading of the code is not. Drive it through a
  scriptable runtime (launch, act, wait, screenshot or dump) that writes an evidence file per run.
- Capture evidence through the target when you can. For a CLI, its captured output is the
  dump. A screenshot from inside an app needs no OS permission, for example Obsidian's
  `dev:screenshot` or Electron's `capturePage`; `screencapture` needs Screen Recording.
- Record every verified step with its evidence. The script refuses a step whose evidence
  file is missing:
  `modlog.py ok --step "hover shows the claim" --evidence evidence/hover.png`

**6. On every failure, record it; on a stall, re-rank.**
- Record each failure with `modlog.py fail --sig "<short failure signature>"`.
- The third identical failure on the same route exits 3 with a STALL checklist. Don't make a
  fourth attempt.
- Re-rank the routes **for this sub-goal**. The new route must pass §Rules again: a rung the
  rules or the target's terms excluded stays excluded under a stall. Then ask first whether
  the original can simply be run — as a binary, a container, a library, or through its own
  API — instead of rebuilt.
- For a hang, sample the stuck process (`sample <pid> 1`) before theorising, and cite that
  artifact in the new route's reason.
- Record the new route (`--supersedes N` marks a route whose reasoning was wrong); that resets
  the count. If no route remains, ask the user.

**7. Package.** Ship only your own code, assets, patches or converters that run on the user's
own install. Write install and uninstall steps.

**8. Field note, in the ship tree.** Build the exact tree you will share inside
`<work>/ship/`, laid out like `$S`:
- `examples/<slug>/` holds the mod, its install and uninstall steps, and only evidence made
  from fixtures you wrote. Shipped fixtures are synthetic and written by hand, never a saved
  page or a recorded capture, and carry no addresses, serials or keys.
- `field-notes/<target>/<slug>.md` is the note. Scaffold it with
  `modlog.py note --out <work>/ship/field-notes/<target>/<slug>.md`.
- Fill every placeholder: exact versions, the route, what the target really does, the
  evidence, numbered *symptom → cause → fix* gotchas, and the envelope. Gotchas are what this
  run hit; if nothing failed, keep the scaffold's "None hit on this run" and invent none.
  - The scaffold names each journal evidence file in a placeholder rather than citing it,
    because `<work>` never ships. For each one, copy it into `examples/<slug>/` and cite it
    by its path from the ship-tree root (`examples/<slug>/evidence/run.txt`, no `..`), or
    describe it without a path.
  - At least one piece of evidence ships, made from a fixture you wrote, or the note links
    to a public source. Evidence from real use is described, never copied in.
  - The journal itself stays in `<work>`. Copy it into the example only if every entry is fit
    to publish (the shipped example's journal was scrubbed; its last entries say how).
- `modlog.py lint-note <note> --root <work>/ship` must exit 0. It fails on a placeholder, a
  missing section, and an evidence path cited under `## Verification` that is missing or
  points outside the ship tree (absolute, `~/`, `..` or `file://`). It reads backticks,
  inline links and reference definitions under `## Verification`; other forms (HTML tags,
  definitions elsewhere in the note) are not read, so cite evidence only the first ways.
  Write commands and API routes without backticks: a backticked `/api/...` reads as a path.
- The Envelope's `Disclosure:` line is one of `none found`, `embargoed (...)` or
  `cleared YYYY-MM-DD (...)`, where the date is the day the §Rules disclosure conditions were
  met (a real date, not in the future). Lint also fails, whatever the state, while the word
  "embargoed" appears anywhere in the note, the Envelope names a YYYY-MM-DD date that has not
  arrived, or the Envelope has more than one `Disclosure:` label. The lint is a speed bump,
  not the gate: "one finding per note, nothing embargoed in it" is a line in the publish ask
  that the user confirms. If the run found a vulnerability:
  - write `embargoed (what, since YYYY-MM-DD)`; lint then refuses the note, so the run ends
    here;
  - draft the vendor report for the user, who decides whether to send it. If they decide
    not to, the note never ships;
  - ask the user for a durable private folder: one they name, outside every repo and
    outside temp folders, which get cleared. Record its path and the embargo in the journal
    (`modlog.py log`), then move the whole `<work>` folder there (journal, evidence, ship
    tree, `deny.txt`, the drafted report);
  - when the conditions are met, write `cleared` with that date, and resume from that folder
    at the lint above, then step 9.
- Write the note even when the mod failed. A documented dead end saves the next agent hours.

**9. Publish check, then copy.** Check the whole ship tree in one pass:
`python3 $S/scripts/publish_check.py <work>/ship --deny-file <work>/deny.txt`

The deny file holds the private names you know: the user's email and display name, private
project, vault and knowledge-graph names, and for a website the tenant subdomain and the
organisation or account IDs a userscript's `@match` or selectors would carry.

`publish_check.py` is a fail-closed filter in front of the user, not a privacy guarantee. The
agent runs it, but the user decides what ships.
- **It blocks** (exit 1):
  - any file type that is not on its ship allowlist (source, docs, small data files,
    screenshots), and text files that are not really text;
  - third-party binaries, captures, symlinks, files over `--max-mb`;
  - dependency, cache and VCS folders (`.git`, `node_modules`, `venv`, ...);
  - secrets (gitleaks with its default rules when installed, plus a built-in list), well-known
    credential file names, and gitleaks config or ignore files inside the tree;
  - decompiler output;
  - home paths, the login name, the hostname, hardware addresses and deny-file terms, in
    contents and in names, matched as written.
- **It does not detect** cookies, session values, serial numbers, personal data such as
  emails and display names unless they are in the deny file, anything encoded (URL-encoding,
  escapes, base64, compression), or the target's own code copied in as text. Keep those out
  at the source (step 3), and ship your mod's source with a build step rather than a bundle:
  a `dist/` bundle can carry the target's modules or other people's code.
- **It lists as REVIEW** every image and SVG; HTML, notebooks, plists and source maps (they
  often embed encoded content); every file under `evidence/` or `fixtures/`; every journal;
  every file in a build-output folder (`dist/`, `build/`, `out/`, `target/`, `.next/`,
  `.nuxt/`: a bundle can carry the target's code); allowed paths and special files. It also
  says when gitleaks did not run. A built file the plugin format needs (an Obsidian
  `main.js`) may ship once the user has reviewed it.
- **This skill's repo takes no `--allow`.** A mod shipped here passes `publish_check.py`
  with no `--allow`; CI runs it that way. If a mod needs one (a binary you built, a font),
  ship its source and a build step instead, or share it somewhere else, where `--allow
  <glob>` (relative to the scanned folder) clears "this type should not ship" findings after
  the user has looked. Its content is still scanned.
- Some findings cannot be allowed, because the fix is to change the tree: a `folder`
  (`.git`, `node_modules`, `venv`, an `.app` or plugin bundle: remove it), a credentials
  file (remove it), a hardware address or fingerprint (redact it, or use the RFC 7042
  documentation range `00:00:5E:00:53:xx`), a deny-file term (generalise it: a userscript's
  `@match` for the user's tenant becomes `https://*.example.com/*`), a home path, a
  secret.
- `publish_check.py --help` prints the full list of what it blocks, reviews and cannot see.
- **Exit 0** means "nothing this filter recognises", not "safe to share".
- **The user reviews, not you.** Publishing is an ask (§Rules), and the ask carries the whole
  REVIEW list, each line with one line on what the file is, and the note's disclosure state
  ("one finding, nothing embargoed"). The user opens what they need and clears the list, or
  says no. The known failure mode is an agent
  that reads its own REVIEW lines, sees exit 0 and asks only "publish?".
- **Then copy the tree byte for byte** into a checkout of this skill's repo, at the same
  relative paths. Before committing, run both checks again on the destination, the same
  commands CI runs: `lint-note` on the note, and `publish_check.py` on `examples/<slug>` and
  the note with the same `--deny-file`.

## The ladder

Rungs 1–5 are ordered by cost and invasiveness. Pick the lowest rung that reaches the idea.

| Rung | What you touch | Apps and websites | Devices | Games |
|---|---|---|---|---|
| **1 · Data and config** | what the program reads | settings, themes, CSS, defaults | the vendor app's settings | data files, mod folders |
| **2 · Sanctioned API** | an extension point its makers offer | plugin and extension APIs, the app's own CLI, AppleScript, AX, URL schemes, App Intents, MCP | documented protocols (Modbus, VE.Direct), local APIs | loaders (tModLoader, SKSE, Fabric) |
| **3 · Patch from inside** | the running program's own code | Electron renderer via DevTools Protocol, userscripts | read the companion app | Harmony, Mixin |
| **4 · Hooks and wires** | native code or the wire | network capture and override | undocumented BLE, USB HID, I2C | proxy DLL, MinHook |
| **5 · Reimplement** | nothing of theirs: you rebuild it | a clean clone diffed against the live app | your own client or firmware | decomps, recomps, rewrites |

**Passthrough** (two programs running at once, exchanging state) is a separate goal, not a
sixth rung. No run of this skill has exercised it yet.

`references/ladder.md` has the rung definitions, how to choose, the oracle patterns
(scriptable runtime, fake host stand-ins) and a pointer for passthrough.

## Rules

These are hard. The full reasoning and the legal summary are in `references/envelope.md`.

- **The user must have the right to modify the target.** They own the device or game, or the
  app's terms permit extensions. If the terms prohibit client modification, the app is out of
  scope.
- **Never defeat a protection**: an integrity check (signed bundles, asar integrity), an
  anti-automation or anti-cheat check, a licence or DRM check, or an access control on
  something that isn't the user's. If a route needs one defeated, it is the wrong route.
- **Never touch an online service's client or protocol beyond the user's own account and
  data.** Never publish anything that automates, scrapes or writes to a live service. A
  cosmetic mod that only changes what the user sees is fine, if the terms allow it.
- **Bring your own files.** Never ship the target's bytes, decompiled code or extracted
  assets. `publish_check.py` enforces the mechanical part.
- **Ask before you:**
  - drive the user's mouse and keyboard, or take focus;
  - install into the user's real profile, app folder or vault (labs need no ask);
  - connect to a device beyond reading its advertisements, pair or bond with it, or send it
    anything other than a documented read: commands, probes, replayed captures, configuration
    or firmware, over BLE, USB, serial or the network. A probe can actuate hardware, and
    pairing can evict the vendor's app;
  - send writes or replayed requests to a live service, even on the user's own account;
  - run code in, or automate, the user's real signed-in session: their browser profile or
    their running app. Test in a lab profile the user logged into instead;
  - change system settings;
  - delete anything;
  - contact a vendor or anyone else outside the user's machine (draft it; the user sends it);
  - publish.
- **Back up first.** Kill processes by exact PID, never by pattern.
- **Disclosure.** If you find a vulnerability, nothing describing it leaves the user's private
  storage until the vendor has been contacted, the disclosure date agreed with them has
  passed (or they shipped a fix), and the owner has signed off. A vendor that never answers
  gets a deadline the owner sets. Private journals stay unblocked.
  - A device that obeys a replayed command with no pairing or authentication is such a
    finding. The mod may still drive the user's own device locally (the device ask above
    applies), but nothing describing the protocol, including the mod's code, ships until
    disclosure clears.

## Scripts

| Script | What it does |
|---|---|
| `scripts/modlog.py` | `init`, `log` (a free entry, no route needed), `route` (`--subgoal`, `--supersedes`), `ok` (refuses missing evidence), `fail` (exits 3 on a stall, with the re-rank checklist), `status`, `note` (scaffolds a field note), `lint-note` (checks a note is complete and its citations stay inside `--root`) |
| `scripts/publish_check.py` | the fail-closed filter of step 9: what it blocks, lists for review and cannot see is in step 9 and in its `--help`. `--json` for machine-readable output |
| `scripts/recon_macos_app.py` | recon adapter for macOS `.app` bundles: stack, extension points, Electron fuses (from the slice this machine runs), protections, update channel, state folders, and the ranked routes |

Exit codes:

| Script | Codes |
|---|---|
| `modlog.py` | 0 ok · 1 `lint-note` findings · 2 usage, refused input, or a file or folder it could not read or write · 3 STALL (`fail`) |
| `publish_check.py` | 0 clean · 1 findings · 2 usage error or a file it could not read |
| `recon_macos_app.py` | 0 ok · 2 usage error or not an app bundle |

**Recon adapters** are per domain: `recon_<domain>.py <target> --json`. Each one prints facts
(stack, extension points, protections, update channel, state locations, caveats) and a `routes`
list. Each route is `{rung, name, status, reason, rank}`, with `status` one of `available`,
`caveat` or `blocked`.

Ranking is mechanical: ladder order, then `available` before `caveat`, with `blocked` last.
The adapter does not know the idea, so the agent still picks the lowest rung that reaches it.

A domain without an adapter gets one as its first deterministic slice, with tests built on
fake targets, once the domain recurs. Shipped so far: macOS apps.

## References

- `references/ladder.md` — rungs, choosing, the oracle, and where to start on passthrough.
- `references/envelope.md` — the rules with their reasons, the legal summary (US/EU), disclosure.
- `references/field-note.md` — the field-note format and what makes one useful.
- `references/playbooks/macos-apps.md` — bundle anatomy, extension points, protections and
  lab profiles for macOS apps.
- `field-notes/` — notes from real runs. Search them first, and add yours last.
- `examples/` — worked runs with their journals and evidence:
  - `examples/recon-macos-apps/`: the adapter's output for three common apps.
  - `examples/obsidian-kg-claims/`: a rung-2 Obsidian plugin with a scripted lab
    (`harness/lab.py`, `harness/record_evidence.sh`).
