---
name: port-feature
description: Bring a feature you already built in another of your own repos into this project. Reads the source feature end to end (screens, state, data, tests and the source's gotchas), maps it onto this project's architecture and conventions, lists what changes and what stays behind, ports the tests, then proves it works here. Never copies secrets, env values, or the other app's names, copy or branding. Use when the user says "bring X over from my other app", "port this feature", "reuse this from another repo", or "do it the way I did it in my other project".
---

# Port feature

A code port, not a copy. The feature already works somewhere else. The job is to
make it work here, the way this project does things, with the lessons the source
repo already paid for.

Not for ideas from apps the user does not own (use the reference-hunt skill), and
not for brand new features with no source.

## 0. Inputs

- **The feature**, in one sentence. Example: "the share sheet capture", "the
  onboarding flow", "the streak counter".
- **The source repo path.** If the user did not give one, ask for it. One question,
  then wait. Do not guess from folder names.

Read this project's rules file (`CLAUDE.md` or `AGENTS.md`) first. It is the
target. If there is none, read the code around where the feature will live and say
in the summary that conventions were inferred.

## 1. Reach the source

- **Local path:** read it directly. Read only. Never edit, commit or run installs
  in the source repo.
- **Not on this machine:** use whatever code search the session has (for example
  `gh search code --repo <owner>/<name> <symbol>`, or a connected GitHub tool), or
  a shallow read only clone into a scratch folder. If none of that works, ask the
  user to clone it locally. Do not rebuild the feature from memory or guesses.

## 2. Read the feature end to end

Before writing anything, trace the whole feature in the source and note:

- **Entry points:** screens, routes, deep links, notifications, share targets.
- **UI:** components, styling tokens, copy, images and other assets.
- **State and data:** stores, hooks, local storage keys, database tables,
  migrations, server endpoints, background jobs.
- **Dependencies:** each package and its exact version, config plugins, app config
  entries, native code, permissions.
- **Analytics and flags:** events fired, feature flags, paywall or premium checks.
- **Tests:** unit, component and end to end tests that cover it.
- **Gotchas:** search the source's rules file, decisions log and commit history
  for anything about this feature. These are the lessons you do not want to learn
  twice.

Keep a file list as you go. If the trace is getting long, the feature is bigger
than it looked; tell the user and offer to port it in slices.

## 3. Map it onto this project

Write a short port plan and show it to the user before coding. Three parts:

**Changes.** Each source piece and its home here. Translate, do not paste:

- Folder layout and routing (for example the source uses `app/`, this project
  uses `src/app/`).
- Theme, spacing and colour tokens; use this project's, not the source's.
- State and data: reuse this project's existing stores, services and helpers
  instead of porting the source's data layer. If the source calls a server and
  this project works on device (or the other way round), route through the local
  equivalent.
- Naming, exports, file idiom and test style from this project's conventions.
- Analytics events renamed to fit this project's event naming.

**Left behind.** Name each thing you are not bringing, and why:

- Secrets, API keys, DSNs, webhook URLs, env values, `.env` files. Never copy
  these. List the env var names this project will need and let the user fill them.
- The other app's name, bundle id, copy, screenshots, icons, brand colours and
  anything about its users or their data.
- Code the source needs only because of its own history (migrations from old
  versions, workarounds for bugs this project does not have).
- Parts of the feature the user did not ask for.

**Gotchas carried over.** Each relevant source gotcha, reworded for this project.

## 4. Check dependencies fit

For each package: `npm view <pkg>@<version> peerDependencies` and compare with
this project's Expo and React Native versions before installing. For Expo
packages prefer `npx expo install <pkg>` so the version matches the SDK. If the
source pins an old version, check whether the newer one changed its API.

Flag native modules early. They mean the app leaves Expo Go and needs a prebuild
and a development build. That is a step the user may have to run.

## 5. Build it

Port in this order, running the check command after each step:

1. Dependencies and config.
2. Data and state (or the wiring into existing stores).
3. Logic, with its unit tests ported alongside.
4. UI and navigation.
5. Analytics and flags.

Replace every piece of the other app's copy with copy written for this project.
If you do not know what it should say, leave a clear placeholder and list it in
the summary.

## 6. Port the tests

Bring the source's tests over and adapt them to this project's test setup. A test
that passed in the source and fails here is a finding, not a nuisance: either the
port is wrong or the assumption no longer holds. Fix the cause. Where the source
had no tests for a path that matters, add one.

## 7. Prove it works here

- Run the check command from the rules file Settings [`npm run check`, or lint,
  typecheck and tests]. It must be clean.
- Run the app and walk the feature's main path. Use a simulator or emulator if the
  session can drive one; otherwise say so plainly.
- Search the changed files for the source app's name, bundle id, domains and env
  values. Nothing should match.
- If the feature has a user facing surface, add an item to the release checklist
  (`RELEASE_TEST_CHECKLIST.md`) with the surface, steps and expected result.

## 8. Record it

- Add the carried over gotchas to this project's rules file **Gotchas**, dated.
- If the port added a subsystem, add one line to the rules file **Architecture**.
- If the project keeps a features doc, add the feature there.

## Summary

Finish with a short summary:

- What was ported and where it lives now.
- What changed in the translation, in a few lines.
- What was left behind and why.
- Env vars, native rebuilds or store setup the user has to do by hand.
- Copy placeholders still to write.

Good: "Ported the share sheet capture from your other app. Reused this app's
on device categoriser instead of the source's server call. Carried over the
gotcha about the share extension's bundle id suffix. Native module, so it needs a
development build. Two copy placeholders on the empty state."

Bad: "Copied the share feature over." No convention mapping, no gotchas, no
proof, and probably the other app's strings still inside.
