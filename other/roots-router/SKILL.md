---
name: roots-router
description: Use when you must decide which kivo-wise skill to open first, or in what order, for a task in a Roots-stack project (Sage theme, Acorn mu-plugin, Bedrock, Radicle) - "which skill", two skills seem to apply, the profile x intent map, the project-guidelines-first and native-first rules. When one skill clearly matches the task, open that skill instead. For detecting the profile use roots-triage.
license: MIT
compatibility: Filesystem agent with bash and node; project commands run through the runner named in the triage output, never on the host.
---

# Roots router

Entry point for every Roots-stack request: find the profile, pick one skill, apply the gates.

## When to use

- The session context names a Roots profile (`sage-theme`, `acorn-mu-plugin`, `radicle-app`) and the request is about code, configuration or commands in that project.
- The project has a `.roots-stack.json`, a `composer.json` requiring `roots/acorn`, `roots/bedrock` or `roots/radicle`, or a `.lando.yml` with `recipe: wordpress`.
- You are unsure which of the stack skills applies, or two of them seem to apply.
- Not for: plain WordPress sites without Acorn (classify them with `roots-triage` and fall back to the project's own guidelines), production operations, or generic PHP questions.

## Inputs required

- The triage JSON (`layout`, `apps[active].kind`, `apps[active].path`, `runtime.runners`, `warnings`) from the session context, or produced by `roots-triage`.
- The user's intent in their own words, including the identifiers they typed (`wire:model`, `lando rebuild`, `acf/validate_value`, ...).
- The project's guidelines file(s): `AGENTS.md`, `.ai/` or the rules folder the repository names.
- `references/routing.json` (profile descriptions, intent rows, `planned` list) and `references/keywords.json` (one keyword list per skill, used by the prompt router; `_triage` names symptom-first skills that win when several skills match).

## Procedure

1. **Read the project guidelines before anything else.** They win over every skill. Note the rules that constrain the answer (runner, language, branch names, forbidden actions).
2. **Fix the profile.** Take `apps[active].kind` from the triage JSON; `.roots-stack.json` overrides heuristics. If the context is missing, stale or contradicts the files you see, run `roots-triage` first. Map `acorn-theme` to `sage-theme` and `acorn-plugin` to `acorn-mu-plugin` for routing purposes.
3. **Classify the intent.** Match the identifiers in the request against the `intents` rows of `references/routing.json`. Exactly one row: open that skill. Several rows, or a row whose answer depends on the profile: read [references/decision-tree.md](references/decision-tree.md) (intent table, tie-breaks). None: use the lookup order below and answer from project guidelines and local source.
4. **Apply the native-first gate.** Before proposing validation, save flows, admin behaviour, endpoints, cron, caching or routing, name the native WordPress, ACF or Acorn mechanism and verify it in the local source (core directory from triage, ACF `includes/`, the app's `vendor/`). Custom code needs a verified gap and a written reason.
5. **Apply the lookup order for facts:** project guidelines, then local source, then the docs corpus when `.docs-brain.json` exists (`docs-brain` skill), then the web.
6. **Carry the runner.** Every command you suggest comes from `runtime.runners` (`wp`, `acorn`, `composer`, `node`, `test`, `lint`, `cache`, `logs`). In every skill, `{{runner.<key>}}` means that value: the session context lists it as `<key>=<command>` on the `runner:` line (for example `{{runner.acorn}}` is `lando wp acorn` in one project and `lando acorn` in another). A key that is absent means the project has no such command; say so instead of inventing one. When `runtime.runner` is `none`, say so and use bare commands with a warning.
7. **Open exactly one skill**, state the profile and the reason in one line, and let that skill chain to a second one only when its own procedure says so.

What differs per profile (details per row in the decision tree):

| Concern | sage-theme | acorn-mu-plugin | radicle-app |
|---|---|---|---|
| Base path | theme directory, inferred | plugin directory, must be explicit (`ACORN_BASEPATH` or `Application::configure(<path>)`) | repository root |
| Boot | `functions.php` at include time | main plugin file, usually `after_setup_theme` | root boot file under `public/content/mu-plugins/` |
| Blade views | theme `resources/views` | plugin `resources/views` through its own providers | root `resources/views` |
| Blocks | ACF Composer when installed | ACF Composer when installed | native `register_block_type` |
| Post types | Poet or `app/PostTypes` | Poet or `PostTypes` classes | `roots/acorn-post-types` (`config/post-types.php`) |
| Assets | theme `public/build`, `Vite::asset` | plugin `public/build`, plugin URL | `public/build` at the webroot |
| Namespace | `App\` | project-specific (triage `namespace`) | `App\` |
| Protected files | `.env*`, `wp-config.php` | the same plus the plugin's `.env` | `.env*`, `bedrock/environments/*.php`, `public/wp-config.php` |

## Verification

Done when all of these hold:

- One skill is named, with the profile and the reason, before any code or command is written.
- The profile came from `.roots-stack.json` or the triage JSON, not from the folder name alone.
- Every command uses the runner from the triage output; no host `wp`, `composer`, `php`, `yarn` or `npm`.
- Any proposed custom mechanism names the native one it replaces and where in the local source it was checked.
- Project guidelines were read and nothing in the answer contradicts them.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Two skills look equally right | Request mixes a symptom and a topic, or "create" and "explain" | Apply the tie-breaks in `references/decision-tree.md` section 4; symptom first, create before explain |
| Profile in the context does not match the files | Stale cached context, or the flag file points at another app | Run `roots-triage`; trust `.roots-stack.json` if present, otherwise propose writing it |
| Routing points at a skill that is not installed | The skill is in the `planned` list of `routing.json` (Phase 3 not shipped) | Say which skill would own it, follow the lookup order, keep the profile differences from the row; do not invent its procedure |
| Keyword hint fired for the wrong skill | `references/keywords.json` phrase overlaps the request by accident | Use the full `intents` rows instead; adjust the keyword list if the overlap repeats |
| Answer assumes a theme on a mu-plugin or Radicle project | Profile ignored | Re-read the profile table; base path, boot and asset URL differ per profile |
| Suggested `wp`/`composer` on the host | Runner not read from triage | Use `runtime.runners`; when `runner: none`, state the risk explicitly |
| Custom code proposed for something native | Native-first gate skipped | Name the native hook/API, verify it in the local source, keep custom code only for a proven gap |

## Escalation

- Triage cannot classify the project (`layout: unknown`, no apps): ask one question - theme, must-use plugin or repository root? - then write `.roots-stack.json` with `roots-triage`.
- The project guidelines contradict a skill: the guidelines win; report the conflict to the project maintainers instead of working around it.
- The intent is outside the stack (hosting, CI, design tools, business logic in another language): say so and stop routing; do not stretch a stack skill to cover it.
