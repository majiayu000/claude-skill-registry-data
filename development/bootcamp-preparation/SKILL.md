---
name: bootcamp-preparation
description: 'Bootcamp preparation (first, mandatory module): choose Core vs Customized, select which modules to run, set verbosity and programming language, and initialize version control (git, no prompt). Use right after the onboarding WELCOME preface, before the entity-resolution primer / Module 1.'
---

# Bootcamp Preparation (first module, mandatory)

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Follow `../bootcamp-onboarding/ground-rules.md` throughout (👉 one-question-at-a-time,
MCP-first, file placement, checkpointing). This is the **first, mandatory module**. The
onboarding preface (`../bootcamp-onboarding/onboarding-flow.md`) hands off here after the WELCOME
banner, the overview, and the "any questions" step; this module consolidates the core setup in one
place: the Core-vs-Customized path choice, per-module selection, level of detail (verbosity),
programming language, and version control. (The software-integration and deployment-target
questions are asked in Module 1 Phase 2, not here, per INV-097.)

Bootcamp preparation is a **lightweight setup module**: it presents its own banner and closes with
a bootcamper-facing recap of the setup choices (INV-099), but is otherwise exempt from the
per-module completion apparatus (no journey map, no before/after framing, no
`docs/bootcamp_recap.md` section, and it is not added to `modules_completed`). It cannot show a
journey map yet — it is the module that *produces* the selection that drives the journey map from
the first content module onward. Do the administrative parts quietly (INV-012); ask the setup
questions one 👉 at a time.

Present the banner, then run the steps in order.

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧰🧰🧰  BOOTCAMP PREPARATION  🧰🧰🧰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## The module list (source of truth for selection and the journey map)

The bootcamp is this ordered sequence. "Required" modules are always included and cannot be
deselected; "Optional" modules are chosen in Customized mode. A module with **Requires** cannot
run unless its prerequisite is also included.

The **State token** column is the exact value to write into `selected_modules` and
`modules_completed`. Copy it; never derive a token from a display name.

| # | Module | Rule | State token | Maps to |
|---|---|---|---|---|
| 1 | Bootcamp preparation | Required | `bootcamp_preparation` | this module |
| 2 | Entity Resolution Concepts | Optional | `entity_resolution_concepts` | `module-00-entity-resolution-concepts` |
| 3 | Discover the Business Problem | Required | `business_problem` | `module-01-business-problem` |
| 4 | SDK setup | Required | `sdk_setup` | `module-02-sdk-setup` |
| 5 | System verification | Optional — Requires "SDK setup" | `system_verification` | `module-03-system-verification` |
| 6 | Truth Set visualization | Optional — Requires "System verification" | `truthset_visualization` | `module-03b-truthset-visualization` |
| 7 | Data collection | Required | `data_collection` | `module-04-data-collection` |
| 8 | Data Quality, Mapping, and Transformation | Required — Requires "Data collection" | `data_quality_mapping` | `module-05-data-quality-mapping` |
| 9 | Data processing | Required — Requires "Data Quality, Mapping, and Transformation" | `data_processing` | `module-06-data-processing` |
| 10 | Query, Visualize and Discover | Required — Requires "Data processing" | `query_visualize_discover` | `module-07-query-visualize-discover` |
| 11 | Bootcamp graduation | Required — Requires "Query, Visualize and Discover" | `graduation` | `graduation` |

Because **Bootcamp graduation is required** and it requires "Query, Visualize and Discover", which requires
"Data processing", which requires "Data Quality, Mapping, and Transformation", which requires "Data collection", that
whole downstream chain is always included. So the genuinely deselectable modules are exactly three:
**Entity Resolution Concepts**, **System verification**, and **Truth Set visualization** (and
deselecting System verification forces deselecting Truth Set visualization, which requires it).

## 0. Read the saved preferences first — honor them, do not ask (INV-133)

⛔ **Before Step 1, read `config/bootcamp_preferences.yaml` once.** Every capture question below is
governed by the same rule, and it applies to **all** of them:

> A setup preference already recorded in `config/bootcamp_preferences.yaml` MUST be honored, its
> capture question MUST NOT be asked, and the saved value MUST NEVER be overwritten with a
> recommended default (INV-133).

This is what lets a returning bootcamper settle a recurring choice permanently — put
`programming_language: Python` and `verbosity: {preset: minimal}` in the file before starting and
those two questions never appear again — without changing the default for anyone else. Asking
someone what they already told you is an INV-006 violation, and it is most galling on a second run.

| Preference | Question it suppresses | Honor when |
|---|---|---|
| `path` | Step 1 | `core`; or `customized` **and** a valid `selected_modules` list is also saved |
| `verbosity` | Step 3 | a recognized preset (`minimal`/`concise`/`standard`/`detailed`) |
| `programming_language` | Step 4 | any non-empty value |

- **`path: customized` with no `selected_modules`** is not honorable — the selection would be
  undefined. Ask Step 1 (and Step 2) in that case, and say why in one line.
- **An unrecognized or unreadable value is not honorable.** Fall through to the question rather than
  guessing what was meant.
- **Nothing here is a question.** Read the file quietly (INV-012) and hold each honored value for the
  Step 6 consolidated write, unchanged.
- **`name`, `os`/`arch` and `git_init` are detected, never asked** (INV-134/INV-061/INV-095), so they
  have no question to suppress — but a saved `name` is still honored rather than re-detected.

⛔ **State every honored value once in the Step 7 recap**, marked as coming from the saved file, so
the bootcamper can see what is in force and correct it. A silently-honored preference is
indistinguishable from a question you forgot to ask.

## 1. Choose the bootcamp path

⛔ Skip this step entirely when `path` is honorable per Step 0.

Present this pinned 👉 question, verbatim (INV-056), and end the turn on it:

> 👉 **Which bootcamp would you like? Reply with a number:**
>
> 1. **Core bootcamp** *(recommended)* — every module, in order, from preparation through graduation.
> 2. **Customized bootcamp** — you choose which optional modules to include (required modules are always in).

This is a ⛔ gate: wait for the real choice, do not assume one (INV-007).

- **Core** → **every** module is selected, in order — including all three deselectable ones.
  "Optional" describes what Customized may drop; it never means Core omits it. **Hold**
  `path: core` and this exact ordered list for the consolidated write in Step 6, then skip Step 2:

  ```yaml
  selected_modules:
    - bootcamp_preparation
    - entity_resolution_concepts
    - business_problem
    - sdk_setup
    - system_verification
    - truthset_visualization
    - data_collection
    - data_quality_mapping
    - data_processing
    - query_visualize_discover
    - graduation
  ```

  ⛔ Copy that list verbatim — all eleven tokens. Do **not** rebuild it by translating the module
  table's display names into tokens: that derivation is what silently dropped
  `entity_resolution_concepts` from a Core run, so the primer never appeared and the bootcamper was
  never told a module had been skipped (INV-014 permits only *requested* skips).
- **Customized** → go to Step 2.

**Handling each answer (INV-284).**

- **1, "Core bootcamp":** the **Core** item above, then Step 3.
- **2, "Customized bootcamp":** the **Customized** item above, so Step 2, then Step 3.

## 2. Select modules (Customized only)

Show the full module list above (as statements, so the bootcamper sees everything and what is
always included) — present only the module **names** and their required/optional status; do NOT
render the internal "#" or "Maps to" columns (catalog numbers and skill-directory names are
internal — INV-079/INV-012). Then end the turn on this single pinned 👉 question, verbatim (INV-056):

> 👉 **Which optional modules would you like to include? Reply with the numbers from the list below, comma-separated — reply "none" for just the required modules:**
>
> 1. **Entity Resolution Concepts** — a short primer on how entity resolution works.
> 2. **System verification** — end-to-end checks that Senzing works on your machine.
> 3. **Truth Set visualization** — an interactive web app of the resolved Truth Set (requires System verification).

Apply the prerequisite rules when recording the selection:

- All Required modules are always included. Name them exactly as the module table above spells them
  — Bootcamp preparation, Discover the Business Problem, SDK setup, Data collection, **Data Quality,
  Mapping, and Transformation**, Data processing, **Query, Visualize and Discover**, Bootcamp
  graduation —
  never an abbreviation, since these names are what the bootcamper reads here and in every later
  journey map and transition question (INV-079).
- If the bootcamper chooses **Truth Set visualization** (3) without **System verification** (2),
  tell them Truth Set visualization requires System verification, and include System verification
  too (do not silently drop the choice; state what you included and why).
- "none" → include only the Required modules.

**Hold** `path: customized` and the resolved ordered `selected_modules` list for the consolidated
write in Step 6. Keep the list in module order so the journey map and transitions follow it.

**Handling each answer (INV-284).** Each number chosen adds its module to the held list, by the
prerequisite rules above; then Step 3.

- **1, "Entity Resolution Concepts":** added.
- **2, "System verification":** added.
- **3, "Truth Set visualization":** added, with System verification too when 2 was not chosen.

## 3. Level of detail (verbosity)

⛔ Skip this step entirely when `verbosity` is honorable per Step 0.

**Before asking, tell them the choice is not permanent** — that they can change it any time
("change verbosity", or "more code walkthroughs"). This has to come **first**: INV-251 requires the
👉 question to end the turn, so nothing can follow it, and a reassurance delivered after the answer
cannot inform the choice it was meant to inform.

> 👉 **How much detail would you like in the bootcamp output? Reply with a number:**
>
> 1. **minimal** — near-zero output: only questions, results, and required banners/summaries; no explanations, code walkthroughs, or step recaps. Best for experts who want to move fast.
> 2. **concise** — minimal explanations, brief recaps. Best for experienced developers.
> 3. **standard** *(recommended)* — balanced what-and-why, block-level code summaries.
> 4. **detailed** — full explanations, line-by-line walkthroughs, SDK internals.

Wait for the answer, then **hold** the chosen verbosity for the consolidated write in Step 6 — do
not write it now (INV-058: one setup write, not one per gate). Each preset maps its five
`categories` to a single level — `minimal` = 0, `concise` = 1, `standard` = 2, `detailed` = 3.
When persisted, the `verbosity` key will look like (here, `standard`):

```yaml
verbosity:
  preset: standard
  categories:
    explanations: 2
    code_walkthroughs: 2
    step_recaps: 2
    technical_details: 2
    code_execution_framing: 2
```

For `minimal`, every category is `0`. `minimal` reduces only *explanatory* output; it NEVER
suppresses required output — every 👉 question (INV-005), gate, module banner (INV-079),
end-of-module summary (INV-032), and the recap (INV-048) still appear.

This is not a ⛔ gate, but it is still a 👉 question the bootcamper answers (INV-007): wait for their
reply. If they explicitly decline to choose (e.g. "no preference", "you pick", "skip"), treat that
decline as choosing the recommended `standard` and say so — never assume a level before they have
replied. (The can-change-it-any-time reassurance belongs **before** the question, above — not here.)

**Handling each answer (INV-284).** Hold the preset as above, then Step 4 (Step 3a asks nothing).

- **1, "minimal":** every category `0`.
- **2, "concise":** every category `1`.
- **3, "standard":** every category `2`.
- **4, "detailed":** every category `3`.

## 3a. Model guidance — no question (retired)

⛔ **There is no model-guidance question and no `model_guidance` preference (INV-137).** Ask nothing
here and write nothing for it. The bootcamp never asks the bootcamper to change the model or the
reasoning effort: not here, not at a module start and not at graduation. The welcome names one
suitable model, once, and how carefully the guide works at each stage is set by instruction alone.
`../bootcamp-onboarding/ground-rules.md` → "Working depth by stage" is **authoritative**; do not
restate it here (INV-300).

This step number is kept so the surrounding step numbering and every cross-reference to Steps 4-7
stay stable. Skip straight from Step 3 to Step 4.

(A previous design asked the bootcamper to choose between `advisory`, `off` and `prompt` and
persisted the answer. That question is retired. Do **not** reintroduce it, and do not honor a
stale `model_guidance` key left in an old preferences file.)

## 4. Programming language selection (gate)

⛔ Skip the **programming-language question** when `programming_language` is honorable per Step 0.
Platform detection and name detection below still run either way — they are detections, not
questions.

- **Detect the platform first (do not ask).** Determine the OS and architecture from the
  environment/system context (else run `uname`/`systeminfo`), and state it in one line
  ("Detected macOS on Apple Silicon"). Hold the detected `os`/`arch` for the Step 6 consolidated
  write so Module 2 can reuse it instead of re-asking (INV-061). ⚠️ **The Linux distribution is
  neither of those, and nothing here detects or holds one.** `os`/`arch` is all this step persists;
  the choice between `linux_apt` and `linux_yum` belongs to rule 5 of the numbered list under
  "Routing rules (apply in order)" in `../module-02-sdk-setup/SKILL.md`, which reads
  `/etc/os-release` on the Linux branch when it needs the answer — cite it rather than restating
  its criterion here (INV-300). **Only if detection is genuinely unavailable or ambiguous**, ask
  this pinned fallback question, verbatim (INV-056), and hold the answer:

  👉 **Which operating system and processor architecture are you using? Reply with a number:**

  1. Linux (x86-64)
  2. Linux (ARM64)
  3. macOS (Apple Silicon)
  4. macOS (Intel)
  5. Windows (x86-64)

  *(Internal: end the turn on this single 👉 question and wait — INV-251.)*

  **Handling each answer (INV-284).** Hold the answer as `os`/`arch` for the Step 6 write, as a
  detected platform is held, then go on with the rest of this step.

  - **1, "Linux (x86-64)":** held.
  - **2, "Linux (ARM64)":** held.
  - **3, "macOS (Apple Silicon)":** held.
  - **4, "macOS (Intel)":** held.
  - **5, "Windows (x86-64)":** held.

- **Detect the bootcamper's name silently (do not ask).** Best-effort: read a display name from
  `git config user.name` (else the environment). If found, hold it as `name` for the Step 6
  consolidated write so the recap and graduation report can address the bootcamper by name; if
  none is available, leave `name` unset. Never ask for it and never block on it.
- Call **`get_capabilities`** on the Senzing MCP server for the supported programming languages.
  It is the tool that carries the full set, and it is the **only** source of the options offered
  here: Python, Java and C# official, Rust and TypeScript/Node.js community-maintained wrappers
  (re-verified 2026-11-19, server 1.46.1). Do **not** route this lookup to `sdk_guide`, and do
  **not** filter the set by platform. `sdk_guide(topic='install', platform=…)` returns install
  commands, env vars, paths and gotchas, and with no `platform` it returns the platform decision
  tree rather than a language one — `needs_input.parameter` is `platform`, offering five operating
  systems. Its reply differs by platform:
  - **`macos_arm` and `windows`:** the `gotchas` list the programming languages supported there —
    *"Java and C# (official), Rust and TypeScript (community)"* — and send Python to Docker or WSL2,
    because the Python SDK is supported on Linux only. That is the `get_capabilities` set narrowed
    by Python alone, for that one reason.
  - **`linux_apt`, `linux_yum` and `docker`:** the reply carries no language list.

  (Every platform and the no-platform call re-checked live, same server and date.)
  <!-- MCP-NEGATIVE: sdk_guide(topic='install', platform='linux_apt', 'linux_yum' or 'docker') — returns no language list — owner: get_capabilities carries the language set (routing negative — the fact exists, go there) — server 1.46.1, 2026-11-19 -->
  So the set is the same on every platform except for **where Python runs**, and that one
  platform↔language constraint the server states — the Python SDK is supported on Linux only, with
  Docker or WSL2 as the route on macOS/Windows — is carried in the annotation rules below and in
  Module 2's routing, which is where it belongs. Python stays among the options on macOS and
  Windows, annotated with its cost and the server's routes.
- Always say "**programming language**", never the bare word "language" (avoids confusion with
  spoken languages).
- Present the MCP-returned options as a **numbered list**, rendered **directly beneath the 👉
  question, as part of it** — the same shape Steps 1–3 use, and required by
  `../bootcamp-onboarding/ground-rules.md` → the 👉 protocol. These options cannot be pinned,
  because they come from the server at runtime; that changes whether the text is fixed, never where
  it goes. The question says "reply with a number", so the numbers must follow it (INV-224).

  ⛔ **Sort the two kinds of prose in this step by where they belong, because it mixes them.**
  - **Platform-wide statements are informational → BEFORE the 👉**, with the detected-platform
    line. The Linux sentence is one: it says the same thing about every option, so it is a fact
    about the platform, not an annotation on a choice.
  - **Per-option annotations belong ON their option**, inside the numbered list — never hoisted
    above the question, where they separate the numbers from the instruction to use them.

  Annotate an option **only where the Module 2 routing rules actually distinguish it** — that is,
  where the platform forces a language into a container — so the trade-off is visible at the
  decision point. The rules are the numbered list under "Routing rules (apply in order)" in
  `../module-02-sdk-setup/SKILL.md`; the ordinals below index that list, so re-check them there
  rather than trusting the numbers if that list is ever edited. All four platform cases:
  - **macOS Apple Silicon:** per-option — "Python — runs via Docker (the SDK is Linux-only);
    Java / C# — native." (routing rules 1 and 3)
  - **macOS Intel:** platform-wide — every language runs via Docker; there is no native Intel-Mac
    install. (rule 2) Say it once, above the 👉.
  - **Windows:** per-option — for Python, name the **cost**, not just the mechanism: choosing it
    here means installing and running a Linux environment (Docker Desktop **or** WSL2), which needs
    administrator rights and, for WSL2, a reboot. Other languages need Scoop, else Docker.
    (rules 1 and 4)
  - ⛔ **On Windows and macOS the Python annotation states the price, not the routing.** "Runs via
    Docker" is true and is not what the choice needs: it names a mechanism where the Bootcamper needs
    to know they are agreeing to a system-level install. A Bootcamper who picks Python here and meets
    that two modules later, at SDK setup, has paid for a reversible decision at the one point where
    reversing it was free — reported 2026-08-18 by a Windows 11 Bootcamper who lost the time to a
    WSL2 install and a reboot mid-bootcamp.
  - ⛔ **Relay every environment route the server returns, not just Docker.** Take them from
    `sdk_guide(topic='install', platform=<detected>, language='python')` at gate time rather than
    from this file (INV-080): on **server 1.33.0, 2026-08-21** its `compatibility_notes` give **two**
    — *"Pick a different environment — use Docker or WSL2 to run Python inside a Linux container"* —
    alongside two language alternatives (*"Java and C# are officially supported on macOS and
    Windows; Rust and TypeScript are community-supported on all platforms"*). The Bootcamper above
    chose WSL2, which is the server's own second option and which this gate did not offer.
    ⚠️ **On macOS, suppress the WSL2 half:** the `platform='macos_arm'` response carries the same
    sentence, and WSL2 does not exist on macOS. Reported upstream as a bug 2026-08-21; until it is
    corrected, do not relay that clause on a Mac.
  - **Linux:** platform-wide — the rules distinguish nothing per language, so all supported
    languages install natively via the platform's package manager (rule 5). Say that once above the
    👉 rather than annotating each option with the same thing, and do **not** invent per-language
    install detail to fill the space.

  ⛔ **Do not manufacture an annotation the routing rules do not support.** Those rules
  (`../module-02-sdk-setup/SKILL.md`, "Determine Platform") resolve a *platform*, not per-language
  install mechanics, so on Linux there is genuinely nothing to differentiate. Precise install
  commands come from `sdk_guide(topic='install', platform=…, language=…)` in Module 2, at the point
  they are needed — not from memory here (INV-080). If the MCP server flags a language as
  discouraged or unsupported on the platform, relay that and suggest alternatives.

  The resulting shape (Linux, where the platform statement is platform-wide). The question line is
  written once, below — this is its position, not a second copy of it:

  ```text
  Detected platform: Linux (apt). All supported programming languages install natively
  via the platform's package manager.

  <the pinned 👉 question below, verbatim>

  1. Python — official SDK
  2. Java — official SDK
  … (one line per language `get_capabilities` returned, in its order)
  ```

  On macOS Apple Silicon and Windows the same shape holds, with the routing note on the option it
  applies to — on Windows, `1. Python — needs a Linux environment: Docker Desktop or WSL2 (admin rights; WSL2 also a reboot)`, and on macOS the same without the WSL2 half — and nothing platform-wide
  hoisted above except the detected-platform line.

  👉 **Which programming language would you like to use for the bootcamp? Reply with a number:**

  **Handling each answer (INV-284).** The options come from `get_capabilities` at runtime.

  - **Each number:** that programming language; hold it as below, then Step 5.

- This is a ⛔ gate whose wording is pinned — present the 👉 question above verbatim (INV-056); wait for the bootcamper's real choice. Do NOT assume or say "I'll go with X."
- **Hold** the chosen programming language for the Step 6 consolidated write (do not write it now).

## 5. Initialize version control (automatic, no prompt)

Do this quietly (administrative, not narrated — **no 👉 question**, INV-095). Check whether the
working directory is already a git repository. `git` behaves identically on Linux, macOS, and
Windows; rely on the command's **exit status**, not a shell-specific stderr redirect:

```bash
git rev-parse --is-inside-work-tree
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

- **Already a repo** (command succeeds / prints `true`): **hold** `git_init: existing`.
- **Not a repo** (command fails / non-zero exit): run `git init` automatically as a quiet
  administrative action and **hold** `git_init: true`. Do not ask.
- **`git` not installed** (command not found): skip initialization, **hold**
  `git_init: unavailable`, and continue — never block on version control.

`git init` is an action (run it now when applicable), but the `git_init` value is **held** for the
single consolidated write below — no separate write (INV-058).

## 6. Consolidated preference write (once, quietly)

Persist all setup choices collected in Steps 1-5 to
`config/bootcamp_preferences.yaml` in a **single** write (INV-058) — `path` (`core`/`customized`),
`selected_modules`, `verbosity`, the programming language, the detected `name` (if any), the
detected `os`/`arch`, and the `git_init` outcome. **No `model_guidance` key** — that preference is
retired (INV-137). (The software-integration and deployment-target answers are
NOT collected here — they are asked in Module 1 Phase 2 and persisted there, per INV-097.) (`path`
replaces the old `track` preference; downstream readers — graduation, the recap header — read
`path`.) This is the only setup write of this module; the gates only held their answers, so the
bootcamper sees one diff instead of one per gate (INV-012). Do not narrate this administrative
write.

```yaml
path: core            # or: customized
selected_modules:     # ordered; drives the journey map and transitions
  - bootcamp_preparation
  - entity_resolution_concepts   # always in Core; omitted only if Customized drops it
  - business_problem
  - sdk_setup
  - system_verification          # always in Core; omitted only if Customized drops it
  - truthset_visualization       # always in Core; omitted only if Customized drops it
  - data_collection
  - data_quality_mapping
  - data_processing
  - query_visualize_discover
  - graduation
```

⛔ **Before handing off, verify the list you are about to write** (internal self-check, not
bootcamper-facing). When `path: core`, confirm `selected_modules` holds all eleven tokens from
Step 1 in that order; when `path: customized`, confirm it holds the eight Required tokens plus
exactly the optional ones resolved in Step 2, in module order. If a module is missing, correct it
**now** — after the handoff in Step 7 the next module has already started and the omission is
invisible.

Also set `current_module` in `config/bootcamp_progress.json` to the first content module (a single
batched write, INV-012). This write sets no other key. The module selection is kept in one file,
`config/bootcamp_preferences.yaml`, which the consolidated write above has already written and
which module completion and the journey map read (INV-442).

## 7. Recap the setup and hand off to the first selected content module

**First, recap the setup choices to the bootcamper** (INV-099): read them back from the
consolidated write as a concise, lightly-highlighted summary — analogous to a per-module recap, but
Bootcamp preparation stays apparatus-exempt, so this is a bootcamper-facing recap **only**: it is
NOT added to `modules_completed` and NOT written as a `docs/bootcamp_recap.md` section (INV-092).
Respect the active verbosity preset — shorten under `concise`, and keep it to a single line under
`minimal`.

Every line states the value **in force**, whether it came from a question this run or from the
saved file (INV-133). Append ` — from your saved preferences` to any line whose question Step 0
suppressed, so an honored preference is visible rather than looking like a question you skipped:

```text
✅ Bootcamp preparation complete
────────────────────────────────
• Path: Core (all modules) — or Customized (selected modules)
• Modules: {ordered selected module names, separated by "; "}
• Detail level: {verbosity}{ — from your saved preferences}
• Programming language: {programming language}{ — from your saved preferences}
• Version control: {git initialized | existing repo | git unavailable}
→ Next: {first content module name}
```

⛔ **Two details in that template are load-bearing; do not "tidy" either one.**

- **The module list is separated by semicolons, not commas.** Two display names contain internal
  commas — *Data Quality, Mapping, and Transformation* and *Query, Visualize and Discover* — so a
  comma-separated Core list reads as **fourteen** modules instead of eleven. This is the same reason
  `generate_recap_pdf.py`'s `--check --expect-modules` takes a semicolon-separated list. The names
  themselves must stay verbatim (INV-079), so the separator is the only place this can be fixed.
- **The label is "Programming language", never the bare "Language"** — the rule stated in Step 4
  above, and it applies to every bootcamper-facing line, not only to the question.

⛔ **Under `minimal`, the six lines COLLAPSE to one — they are not dropped.** The one-line budget and
the per-line provenance marker collide exactly when they matter most: a returning bootcamper who
pre-seeded `path`, `verbosity` and `programming_language` needs all three marked, and has one line to
put them on. Merge with `; ` and attach each marker **inline to its value**, per
`../bootcamp-onboarding/ground-rules.md` → Verbosity. The module list compresses to a count, since
the names were just given in the preface; a count is not a module number, so INV-079 is unaffected.
This exact shape:

```text
✅ Bootcamp preparation complete — Path: Core (all 11 modules) — from your saved preferences; Detail level: minimal — from your saved preferences; Programming language: Java — from your saved preferences; Version control: git initialized. → Next: Entity Resolution Concepts
```

Nothing here is optional under `minimal`: the values in force, their provenance markers, and the
next-module pointer are all required output, and `minimal` reduces only *explanatory* output.

When Step 0 honored anything, close the recap with one line telling them how to change it: "Edit
`config/bootcamp_preferences.yaml` to change any saved choice, or just tell me."

Then hand off to the first module in `selected_modules` after `bootcamp_preparation`:

- If **Entity Resolution Concepts** is selected → invoke `module-00-entity-resolution-concepts`
  (it runs the primer directly; its skip/keep gate has been retired — inclusion is driven by this
  selection).
- Otherwise → invoke `module-01-business-problem` to begin Module 1 — **Discover the Business Problem** (name it to the bootcamper, never "Module 1").

The selected numbered modules then run in order per `selected_modules`, each ending with the
standard module completion process in `../bootcamp-onboarding/module-completion.md`, and the
journey map (per `ground-rules.md`) shows only the selected modules.
