---
name: graduation
description: 'Bootcamp graduation: generate the recap PDF and a production-ready project. Use when the bootcamper finishes the last module (Module 7) and accepts the graduation offer, or says "graduate", "run graduation", or "finish the bootcamp".'
---

# Bootcamp graduation

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Bootcamp graduation turns a completed bootcamp into two things the bootcamper keeps: a
professional **recap PDF** and a clean **`production/` project** they can
build on. Bootcamp graduation is the required, terminal module of the bootcamp. Load this
skill when the bootcamper accepts the graduation offer after the last module
(Module 7), or asks to "graduate" / "run graduation".

Follow `../bootcamp-onboarding/ground-rules.md` throughout: `🛑`/`⛔` are internal
directives (never rendered); one 👉 question ends each yielding turn; keep all
files project-relative; all Markdown goes under `docs/`, all code under `src/`.

Bootcamp graduation is non-blocking: every artifact step warns-and-continues on failure,
and the recap guarantee at the end always produces a valid PDF. Steps that create
the `production/` project ask for confirmation before large or destructive
actions.

Bootcamp graduation is the terminal bookend module. Like every module it opens with the module-start
apparatus — journey map, before/after framing, a step overview, and an estimated time — adapted to
a terminal module (INV-102; see "Bootcamp graduation preface" below). Because no
next-module transition applies, it shows no `✅ Module complete` line and no transition question,
and it ends on the terminal END OF SENZING BOOTCAMP banner and its one `{{host.invoke_package_bootcamp}}` line
(INV-057). (Bootcamp graduation is NOT apparatus-exempt — contrast the exemptions for Bootcamp
preparation (INV-075) and Module 0 (INV-078).)

## Bootcamp graduation banner (show first, exactly once)

Display this banner verbatim as the FIRST output of graduation, before any step.
It bookends the bootcamp: the WELCOME banner marked the start, this marks the
finish. Show it at most once per graduation.

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓🎓🎓  BOOTCAMP GRADUATION  🎓🎓🎓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Bootcamp graduation preface (after the banner)

Like every module, graduation opens with the module-start apparatus (INV-029–032), adapted to a
terminal module — no next-module transition. Present these in order, right after the banner.
First read `config/bootcamp_preferences.yaml` (`selected_modules`)
and `config/bootcamp_progress.json` (`modules_completed`) to render the journey map. Honor the
active verbosity preset (INV-011/INV-012): suppress the explanatory parts under `minimal`, keep
them to one line under `concise`. Refer to modules by name, never number (INV-079).

1. **Journey map.** Render it in the shape `../bootcamp-onboarding/ground-rules.md` → "Module
   start banners and transitions" states once (INV-300), with every selected module marked ✅
   (all experienced) and **Bootcamp graduation** marked 🔄 as the current, final stage — nothing
   ⬜ after it.
2. **Before / After.** Before: every module is complete and your data is resolved, but your work
   still lives in the bootcamp workspace. After: you keep two things — a professional recap PDF
   (`docs/bootcamp_recap.pdf`) and a clean, production-ready `production/` project to build on.
3. **What we'll do.** A brief numbered overview of graduation's steps: (1) note anything that
   tripped us up this session, so the bootcamp itself improves, (2) look back at the decisions you
   made and how you got it built, then ask for your one-line takeaway and the one request you would
   give an AI assistant next time, (3) normalize the `docs/`
   Markdown and render the recap PDF keepsake, then offer an optional narrated 2-minute graduation
   video (`docs/bootcamp_recap.mp4`), (4) build the `production/` project, (5) create a
   silent revisit/resume bundle — a database backup plus a return guide — so you can come back
   later (INV-094), and (6) close with the END OF SENZING BOOTCAMP banner.
4. **Estimated time.** Give an honest, range-based estimate caveated per INV-096 — e.g.
   "⏱️ Roughly 5–15 minutes, depending on your workstation, the database backup size, and PDF
   rendering speed, plus a few minutes more if you choose the optional graduation video." If no
   meaningful estimate is possible, say "hard to estimate" rather than
   inventing a number. Suppress under `minimal`; one line under `concise`.

Bootcamp graduation is terminal, so it has no "what's next / next module" line and no `✅ Module complete`
transition — it ends on the END OF SENZING BOOTCAMP banner and its one `{{host.invoke_package_bootcamp}}` line
(INV-057). What the bootcamper carries forward is the recap PDF and the `production/` project.

## After the preface

Graduation asks nothing about the model or the reasoning effort, and says nothing about them: no
question, no gate and no statement, like every module
(`../bootcamp-onboarding/ground-rules.md` → "Working depth by stage", stated once there, INV-300).

**Where the flow resumes (INV-284).** Wherever ground-rules says to continue into "Step 1",
graduation runs the Pre-checks and then its first step, Step 0 — not graduation's own Step 1 — in
the same turn as the preface. The turn ends on the next single 👉 question, as ground-rules says.

## Pre-checks

Gather context before any step. Do this silently.

1. **Read preferences:** load `config/bootcamp_preferences.yaml` and extract, **by these exact key
   names**:

   | Key | Written by | Notes |
   |---|---|---|
   | `name` | Bootcamp preparation (detected, never asked — INV-134) | the certificate name; see pre-check 4 |
   | `programming_language` | Bootcamp preparation (INV-133) | **not** `language` |
   | `database_type` | SDK setup Step 7 | `sqlite` or `postgresql`, lowercase; **not** `database` |
   | `path` | Bootcamp preparation | `core`/`customized`; older sessions may store this as `track` |
   | `selected_modules` | Bootcamp preparation | drives the journey map (INV-076) |
   | `integration_targets` | Module 1 Phase 2 Step 10a (INV-097) | absent is normal — see pre-check 1a |
   | `deployment_target` / `cloud_provider` | Module 1 Phase 2 Step 10a (INV-097) | absent is normal; `cloud`/`container`/`local` name no platform — see pre-check 1a |

   The data-source registry is **`config/data_sources.yaml`**, its own file (INV-050) — not a
   preferences key.

   ⛔ **Use the names in that table verbatim.** They are the names the writing modules actually
   write, and a reader that invents its own is indistinguishable from a bootcamper who never
   answered: SDK setup says so in its own words — *"a different key name is the same failure as no
   key at all"*. Until 2026-07-29 this step read `language`, `database` and `data_sources`, which
   nothing has ever written, so every consumer below silently got nothing.

   **1a — what the Module 1 answers are for (INV-097).** `integration_targets` and
   `deployment_target`/`cloud_provider` are the bootcamper's own answers to two pinned 👉 questions
   asked in Module 1 Phase 2 Step 10a — what the resolved results must talk to, and where this is
   going to run. Module 7's step 4e acts on `integration_targets` earlier, through its exports;
   Bootcamp graduation is the last place they can still change anything, because the
   `production/` project **is** the thing being deployed: Step 3 stamps them into the container and
   environment templates, Step 4 into the README and the migration checklist's Deployment section,
   Step 5 into the graduation report.

   <a id="generic-deployment-target"></a>
   **A generic `deployment_target` names a category, not a platform.** `cloud`, `container` and
   `local` are what Step 10a records when the Bootcamper chose an option without naming a provider
   or platform; Step 10a's handling owns which answer records which value (INV-097, INV-300). Every
   step below that renders `deployment_target` renders a generic value as its category and says the
   platform was not stated: `cloud` → "cloud (provider not stated)", or the `cloud_provider` as
   stated when one is present; `container` → "container platform (not stated)"; `local` → "local or
   on-premises (not stated)". It never guesses a provider or platform (Step 3's "Stay declarative"
   rule). Every other value renders as that step already says.

   ⛔ **Never ask for them here.** They are asked once, in Module 1 (INV-006/INV-097), so **absent
   is normal, silent, and changes nothing**: every step below states its no-value behavior, and each
   simply stays generic.
   An empty value is the same as absent.
2. **Read progress:** load `config/bootcamp_progress.json` and extract `modules_completed`.
3. **Fallback — and distinguish a missing file from a missing key.** They are different failures
   and only one is the bootcamper's business:
   - **A file is missing or unparseable** → tell the bootcamper, then ask for the programming
     language and database type with one 👉 question at a time; use sensible defaults for the rest
     (path unknown, data sources none).
   - **A file is present but a key is absent** → do **not** announce it and do **not** ask. An
     absent `database_type` means SDK setup Step 7 did not record the choice — a **plugin defect**,
     not a bootcamper outcome — so note it internally so it surfaces in the Step 0 retrospective,
     exactly as Data collection does for the same key
     (`../module-04-data-collection/SKILL.md` → "8b. SQLite load-time warning"), and carry on with the
     value indeterminate. `integration_targets` and `deployment_target` are the exception: absent is
     **normal** and silent (see 1a).

   Either way graduation continues — nothing here blocks.
4. **Check the name is certificate-quality (INV-113).** `name` is auto-detected during Bootcamp
   preparation and never asked (INV-134), so it can be absent or unsuitable. **The governing test is
   the whole test:** treat it as **unusable** when it is missing, empty/whitespace, or **clearly not
   a person's display name**. The cases below are *examples* of that test, not an exhaustive list —
   a value that is plainly not a display name is unusable even if it matches none of them:

   - a known system/service account (`root`, `ubuntu`, `ec2-user`, `admin`, `runner`);
   - a value containing no letters;
   - an email address or `@handle`;
   - **a bare single-token handle** — one lowercase word with no space, e.g. `docktermj`, `jsmith42`,
     `mdockter`. This holds whether or not it matches the OS username: a handle is a handle either
     way, and requiring it to equal the OS username let one through onto a certificate.
   - **a name the recap PDF cannot print** — one written in a script the generator's built-in fonts
     do not carry (Chinese, Japanese, Korean, Cyrillic, Arabic, Hebrew, Greek, Devanagari, Thai …).
     The PDF is set in Latin-1 core fonts, so those characters are dropped rather than rendered, and
     `generate_recap_pdf.py` warns on stderr naming them (INV-143 forbids printing them as `?`, which
     it used to). Do **not** transliterate the name yourself — how it should be spelled in Latin
     script is the bootcamper's decision, which is exactly what the question below asks. Ask it, and
     record their answer; if they decline, the certificate reads "Bootcamper" and graduation
     continues (INV-113).

   Be conservative in the other direction: a plausible real name must **never** trigger the
   question, because asking someone their name right after correctly detecting it is its own defect
   (INV-006). A value containing a space and normal capitalization ("Ada Lovelace") is a display
   name; a single lowercase token is not.

   When it is unusable, ask this once, pinned verbatim (INV-056), **before** Step 1 renders the PDF:

   > 👉 **What name would you like printed on your Certificate of Completion?**

   Persist the answer **in both places**, or the certificate prints the value you just rejected:

   1. As `name` in `config/bootcamp_preferences.yaml`, so a re-render or a resumed session never
      asks again (INV-006). The generator reads this **first** for the certificate — it is the
      Bootcamper's answer, and it outranks anything detected earlier (INV-170).
   2. As the recap's `**Bootcamper:**` preamble line in `docs/bootcamp_recap.md`, written by
      **module-completion Step 2a, at the first module that appends a recap section** (INV-226 —
      a citation naming substeps MUST NOT omit the one that creates the artifact) — Entity
      Resolution Concepts when it is selected, otherwise Discover the Business Problem — from the
      `name` detected during Bootcamp preparation. (⚠️ Bootcamp preparation itself writes **no**
      recap: it is apparatus-exempt (INV-092) and writes only the two `config/` files. It detects
      the name; it does not put it in the recap.) Leaving the line unamended means
      the recap a reader opens still shows the rejected handle, and any re-render driven from the
      recap alone reproduces it. Amending a preamble meta line is not a rewrite of a completed
      module section, so the append-only rule (INV-085) does not forbid it.

      ⛔ **If the `**Bootcamper:**` line is absent, WRITE it — do not assume an edit target.** A
      recap whose header was never created has no line to amend, and passing over the amend without
      saying so is how the certificate ends up printing a placeholder. Write the full preamble if
      none exists,
      per `../bootcamp-onboarding/module-completion.md` Step 2a, above the first `## ` section; and
      note the recovery, because a header written at graduation means some module skipped 2a and
      that is worth knowing.

   ⛔ **Both, not either.** Preferences alone once printed `docktermj` on a signed certificate at
   exit 0 with 99% content retention and no warning, because the generator read only the recap line
   — the pre-check asked the question, the Bootcamper answered, and the answer was discarded
   (INV-170). The generator now prefers preferences and prints a `NOTE:` on stderr when the two
   disagree; treat that note as work still to do, not as confirmation.

   If the bootcamper declines or gives nothing usable, continue
   — graduation is non-blocking and the generator still renders a certificate, warning on stderr
   that it used the "Bootcamper" placeholder. **Never print a rejected system-account value** on the
   certificate or into the recap (INV-113); ask, and use the answer.

## Step 0: Session retrospective (self-observed feedback)

Run this **before** Step 1 renders the recap PDF. Every feedback entry the plugin has ever
collected exists because the *bootcamper* noticed something and said so. That sensor is blind to
the most valuable class of defect: **the kind that looks like it worked** — a wrong field name that
renders blank, a tool that behaves differently than documented, a workaround you applied so
smoothly nobody registered it as friction. This step is the plugin's second sensor, and it does not
depend on the bootcamper noticing anything.

Review **this session** for four categories:

- **False starts** — an approach you began and abandoned.
- **Errors** — commands, compiles, or tool calls that failed and had to be retried differently.
- **Course corrections** — a stated plan or hypothesis that measurement disproved.
- **Learnings** — anything you discovered about the environment, the SDK, or the MCP tools that is
  not in the plugin's documentation.

⛔ **The inclusion test is recurrence, not embarrassment: "would this happen to another
bootcamper?"** A one-off typo is noise. A documented tool that behaves differently than documented
is signal — file it. Do not soften a finding to look better, and do not manufacture findings to
look thorough; if the session genuinely produced none, write nothing and say so in one line.

⛔ **Sweep for these three; do not rely on remembering them.** The four categories above are
recalled from the session, and by graduation the session may have crossed one or more compaction
boundaries — so the most valuable findings are exactly the ones least likely to still be in context.
Go and look at what the project now contains:

1. **Withdrawn or changed mappings.** Compare the mapping you finished with against what you first
   proposed — `docs/data_source_evaluation.md`, the mapper code under `src/`, and the match-key
   audit's outcome in Data processing. A field you routed to payload after the audit, or a feature
   you stopped mapping two sources onto, is a reversal worth filing.
2. **Corrected scoring or accuracy code** you wrote, including any correction that *lowered* a
   number you had already reported. That one matters most: it means an earlier figure was wrong and
   something may have been decided on it.
3. **Abandoned proposals** — a change you recommended and then dropped after checking the Entity
   Specification or the MCP reference. Cheap when it happens, invisible afterwards.

**Do not re-file what is already there.** `../bootcamp-onboarding/ground-rules.md` → "Reversed
decisions: file them when they happen" means some of these are already in the file from during the
run. Read the existing entries first and skip any finding already recorded; add to an entry only if
you now have evidence it lacked. A reversal whose `steer_triggers` entry in
`config/bootcamp_progress.json` reads `filed: true` is already filed; one that reads `filed: false`
is not, so file it here.

For each finding, append a `## Improvement:` entry to
`docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md` using the **exact template** in
`../bootcamp-onboarding/feedback.md` Step 3 (append only — never rewrite the file), with:

- **`Source:` `self-observed (assistant retrospective)`** — not `bootcamper-reported` (INV-116).
  A maintainer must be able to tell the two apart; they deserve different weight.
- **`Module:`** the module where the friction occurred, even though you are filing at graduation.
- **`Routing:`** the Step 2b triage verdict (`plugin` | `mcp-server` | `both` | `host` | `unclear`, INV-248) with its
  one-line reason. Retrospective findings skew toward MCP-server issues — a tool behaving differently
  than documented is exactly the defect class a bootcamper cannot report — so triage each one rather
  than defaulting it to `plugin`.
- **`Upstream:`** for an `mcp-server`/`both` verdict, append the entry as `offer pending`: it is
  saved before the question is asked, so no outcome exists yet. Then offer the forward **once** per
  `../bootcamp-onboarding/feedback.md` Step 3c: show the exact message, strip anything identifying
  (INV-321), and send only on a yes. Batch the offer — one question covering all such findings, not
  one per finding, so the retrospective stays a single non-blocking step. The batch also covers
  entries already reading `offer pending` from the silent in-run append. The one answer replaces
  every `offer pending` value in the same turn, with the outcome Step 3c step 5 names (INV-281).
  On decline or failure, record it and continue; every entry is saved locally regardless (INV-015). ⚠️ **(INV-281) A session forbidden to
  send** — a maintainer `/dry-run` — still presents the offer, then records
  `submission blocked: <reason>`, **never** `offered, declined` (`feedback.md` Step 3c step 5): a
  yes that could not be acted on is not a refusal.
- The same **Context when reported** block, describing what *you* hit rather than what the
  bootcamper saw.

Then **verify it landed**: re-read the file and confirm each entry is present, exactly as
`../bootcamp-onboarding/feedback.md` Step 3b requires. An unwritten retrospective is worse than
none, because nobody is watching for it.

Constraints:

- **Non-blocking.** A retrospective that fails, finds nothing, or cannot review the session must
  never hold up graduation. Report and continue.
- **Not a gate.** Announce it in one line — "📝 Filed N self-observed notes to
  `docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md`." — and continue in the same turn. This is
  not a 👉 question, and the bootcamper is never asked to author or approve it.
- **No feedback-flow banners.** The entry/exit banners in `../bootcamp-onboarding/feedback.md`
  mark the boundary of the *bootcamper-driven* feedback flow (INV-074). This is a graduation step,
  not that flow — do not present them.
- **PII boundary.** Same rule as the recap (INV-322): no hostname, username, IP address, or other
  personal/host identifier. OS/architecture, plugin version, and model/effort are diagnostic
  context and are permitted — the line is personal/host identifiers, not environment facts.

## Step 0b: Hand over the ability (decisions, how it got built, next time)

Run this right after Step 0 and **before** Step 1 renders the recap PDF, so the PDF, the recap and
`docs/REVISIT_BOOTCAMP.md` all carry what it records. The rest of graduation hands over things: a
PDF and a `production/` project. This step hands over the ability: what the Bootcamper decided, how
they got it built with an AI assistant and the Senzing MCP server, and the one request that starts
their next build with no bootcamp script.

Read `docs/bootcamp_recap.md` first, and the checkpoint narrative Step 1a folds when one still
holds content, so nothing recorded is missed. Build two lists:

- **Decisions you made:** from each module's **Questions & Responses** (the record
  `../bootcamp-onboarding/module-completion.md` Step 2b writes). One line per answer that **chose
  something**: a menu choice, such as the record-volume range for the loading program, or an open
  answer that set a direction, such as the business problem or which sources to load. Prefix each
  line with the module's name.
- **How you got it built:** one line per module, `**{Module name}:** you asked for {…}; the AI built
  {…} with the Senzing MCP server.` Draw what was asked from that module's **Questions &
  Responses** and what was built from its **Actions Taken**. A module with neither adds no line.

⛔ **(INV-358) Readiness, teardown and consent gates are not decisions.** Leave out "ready to continue?",
"may I install…?", "tear down the container?" and every answer like them: it let the bootcamp
proceed and chose nothing about what was built.

⛔ **(INV-358) Both lists come from the recorded recap and nothing else.** Never invent a decision, a request
or a build step to fill a list, and never fill one from memory of the session. A list with no
supporting entries is left out: no heading, no "(none)".

**The takeaway turn.** Show both lists (statements, not questions), then end the turn on exactly one
👉 question (INV-251), pinned verbatim (INV-056):

> 👉 **In one line, what will you take away from this bootcamp?** (Reply "skip" to leave it out.)

Record the answer in the Bootcamper's words, as given: never reworded, summarized or completed. With
no takeaway ("skip", a pass, or nothing usable), the line is left out, never written as "N/A", as
`../bootcamp-onboarding/module-completion.md` already does for a module's takeaway.

**The "Next time" turn.** In the next turn, end on exactly one 👉 question (INV-251), pinned verbatim
(INV-056):

> 👉 **What's the first thing you'd ask an AI assistant with the Senzing MCP server to build next, on your own data?** (Name the data or domain. Reply "skip" and I'll draft one from your data.)

- **They state it:** record it in their words, as given.
- **They pass:** offer **one** draft request drawn from their data, their business problem in
  `docs/business_problem.md` and their sources in `config/data_sources.yaml`, naming their own data
  or domain. Offering it is a statement, not a question: show it in one line and continue.

⛔ **(INV-358) The guide's draft is labeled as the guide's, wherever it is recorded.** Record it as
`**The guide's draft (you passed):** {the draft}`, never as their words: in the recap, in
`docs/REVISIT_BOOTCAMP.md` and in the closing announcement.

Then continue to Step 1 in the same turn. Step 1a folds both lists, the takeaway and the "Next time"
request into the recap, and Step 6c carries all four into `docs/REVISIT_BOOTCAMP.md`. The closing
announcement repeats only the "Next time" request (INV-358).

**On a re-run of graduation**, a takeaway or "Next time" request the recap's handover block already
records is not asked again (INV-006); the two lists are rebuilt from the recap as it now stands.

Non-blocking like every graduation step: if the recap cannot be read, leave both lists out, still
ask the two questions, and continue.

## Step 1: Finalize the recap and render the recap PDF

The recap is the crown-jewel deliverable. Produce it before the `production/`
project so the recap PDF always exists.

A finished-recap sample ships with the plugin (INV-065) at
`{{host.docs_dir}}/examples/bootcamp_recap.example.pdf` (skill-relative
fallback: `{{host.docs_relative}}/examples/bootcamp_recap.example.pdf`). You may point the
bootcamper to it so they see what theirs is about to look like — a non-blocking
statement, never a 👉 question or gate, and it adds no turn.

### 1a. Reconcile the recap

Confirm `docs/bootcamp_recap.md` has a name-based `## {Module name}` section for **every** module
in `modules_completed` — match by module **name**, not a catalog number. Iterate the full
`modules_completed` list in its recorded (experienced) order and, for any completed module with no
matching section, append one now from the module's artifacts and progress data, following
`../bootcamp-onboarding/module-completion.md` (append only, never rewrite existing sections, never
re-sort into catalog order). The module flow records each module it completes — including
`entity_resolution_concepts` (Module 0, when it ran — INV-092) and both `system_verification` and
`truthset_visualization` when the Truth Set visualization ran (each self-recording with its own
`modules_completed` entry and recap section, INV-086/INV-087/INV-092) —
so this reconcile is normally a **no-op**; its job is to **recover** a section missing because a
module was interrupted before its completion step ran (e.g. synthesize a missing
`truthset_visualization` section from its artifacts). If `docs/bootcamp_recap.md` does not exist at
all, reconstruct it from `config/bootcamp_progress.json` and the files each module produced.

**Backfill the End-of-Module Summary blocks (before rendering).** Every module section's
**End-of-Module Summary** must carry three labeled blocks — `**What you accomplished:**`,
`**Files produced:**`, `**Why it matters:**` (INV-103; the "Bootcamper's takeaway" line stays
optional). Check each section and add any that is absent, drawn from that module's own recorded
content: **Actions Taken** and the section's own prose say what was accomplished, the paths it names
(plus the files the module actually produced) give **Files produced**, and the module's own
**Before/After** line gives **Why it matters**, taken from its own `SKILL.md` (for example
`../module-04-data-collection/SKILL.md`), or, for Truth Set visualization, the one at its module
start in `../module-03b-truthset-visualization/phase1-visualization.md`. Entity Resolution Concepts
has no Before/After line, so its **Why it matters** comes from what the primer covered, as
`../bootcamp-onboarding/module-completion.md` Step 2c composes it. Where the summary is already
there as an unlabeled paragraph, keep the paragraph and add the labeled blocks — adding the labels a
subsection was always required to carry is not a prose rewrite (INV-085), and the run this was
found in had summaries whose three blocks were simply absent.

**Write each block in its required shape.** `**What you accomplished:**` and `**Files produced:**`
are **lists**: put the label on its own line and one bullet per accomplishment, and one bullet per
file with a short "— what it is" gloss. `**Why it matters:**` is **prose**: it stays inline after its
label. This is the shape `../bootcamp-onboarding/module-completion.md` prescribes and the shape
`{{host.docs_dir}}/examples/bootcamp_recap.example.md` (skill-relative fallback:
`{{host.docs_relative}}/examples/bootcamp_recap.example.md`, INV-252) shows. It is not cosmetic: the PDF renders bullets as
bullets and inline text as one wrapped paragraph, so a list written inline — the comma-joined run of
paths being the usual way it happens — reaches the keepsake as a paragraph and cannot be recovered
later. The shape chosen here is the shape the bootcamper keeps.

⛔ **Never invent content to fill a label.** If a module's own record does not support a block, write
what is true — "(no files — {reason})" for a module that produced none — or leave that one block out
and let the generator mark it "(not recorded)". A keepsake that overstates what the bootcamper did is
worse than one that shows a gap (INV-157's principle: never fabricate to fill a field). Like every
graduation step this is non-blocking: warn and continue.

`--check` (Step 1b) reports these gaps per module, so run it after this backfill and re-render if it
still finds any — the PDF renders every absent block as "(not recorded)" rather than dropping it, so
a gap is visible on the page but should not survive to the bootcamper's copy.

**Stamp the completion date.** Ensure the recap header carries a `**Completed:** {today's date, ISO
8601}` line (add it directly under the `**Started:**` line if absent; leave an existing one intact).
This is the date the Certificate of Completion shows (INV-100), distinct from `**Started:**` — so a
bootcamp spanning multiple days shows the graduation date, not the start date. The renderer prefers
this `Completed` date and falls back to `Started` when it is absent.

**Record the run environment (recap-only).** Ensure the recap header carries the plugin version and
a run-environment provenance block, so the keepsake records which plugin version produced the run
and the hardware/software it ran on. Add these header meta lines (in the preamble, above the first
`## ` section) when absent, idempotently — leave existing lines intact:

- `**Plugin version:**` — from the plugin manifest (should already be present from the recap
  header; add it here if the header predates that field). Resolve the manifest exactly as
  `../bootcamp-onboarding/onboarding-flow.md` step 0 specifies —
  `{{host.plugin_root}}/{{host.manifest_path}}`, else
  `<this-skill-dir>/../../{{host.manifest_path}}`, else "Unknown" — and ⛔ never by searching
  the filesystem, which on a machine carrying two plugin checkouts records the wrong version in
  the keepsake (INV-252). Record the version only, never the path it resolved from: an absolute
  path carries a username and this block is PII-free (INV-322).
- `**Operating system:**` — OS + architecture, reused from the detected/persisted values in
  `config/bootcamp_preferences.yaml` (INV-061), e.g. `Ubuntu 24.04 (x86_64)`.
- `**Python version:**` — the `python3 --version` of the environment.
- `**Language runtime:**` — the bootcamper's chosen-language runtime and version (for a Python
  bootcamp, the same Python).
- `**Senzing SDK:**` — the `sdk_version` recorded in `config/bootcamp_progress.json` by SDK setup
  (Module 2 Step 4, marked by `sdk_version_measured_at`): the installed SDK's own report from
  `SzProduct.get_version()`, `VERSION` only (e.g. `4.4.1`). The Senzing MCP server is remote and
  cannot know what is installed here, so it is not the source for this line. (INV-329) If `sdk_version` is
  absent (an older progress file, or Step 4 skipped), record "Unknown" and continue: do not re-run
  the version call, and do not fill it from the package manager or the MCP server.
- `**Database:**` — the database backend (e.g. SQLite, or PostgreSQL when chosen).

The renderer renders `Plugin version` on the cover and the `Operating system` / `Python version` /
`Language runtime` / `Senzing SDK` / `Database` lines as a distinct **Run environment** block (use
exactly those key names so the renderer groups them). This block is written to `docs/bootcamp_recap.md`
and the PDF only — it is **never** shown in the bootcamp output (INV-012) — and MUST NOT contain a
hostname, username, IP address, or any other personal/host identifier (INV-322). Like every
graduation step it warns-and-continues: if a value cannot be gathered, record "Unknown" and proceed.

If an in-progress recap checkpoint at `docs/progress/recap_checkpoint.md` still holds a
**narrative** (a module interrupted before completion), fold its content into that module's
`## {Module name}` section (append only), then remove the
`<!-- RECAP-CHECKPOINT:START -->` … `<!-- RECAP-CHECKPOINT:END -->` block from
`docs/bootcamp_recap.md` and clear the checkpoint. This ensures the recap carries any
narrative captured from an interrupted module and the PDF renders clean, completed
sections.

⚠️ **The file existing is not evidence a module was interrupted.** `checkpoint-tick.py`
creates it as an empty scaffold of HTML comments while the bootcamp runs, so the normal
state at graduation is "present and unfilled". Fold only when there is real content
**between** the `START` and `END` markers; a scaffold-only checkpoint is nothing to fold
and nothing to report.

**Backfill orphaned screenshots (before rendering).** Scan `docs/visualizations/*.png`. For any PNG
**not already referenced** by an `![...](...)` image line in `docs/bootcamp_recap.md`, embed it into
the matching `## {Module name}` section's **Actions Taken** — **all** of them, not a "best" few: each
capture is a distinct tab (INV-122), so a count cap deletes unique content, and this backfill is the
safety net for captures whose embed step was missed. Map each PNG to
its module by the visualization it came from: match the PNG's base name against the `<name>.html`
referenced in a module's recap section (e.g. `truthset_verification-*` → Truth Set visualization;
`results_visualization-*` (Module 7's single interactive visualization app),
`due_diligence_results-*`, or any other `<name>-*` → the module whose section references
`<name>.html` (older recaps may carry `multi_source_results-*` from before the consolidation; the
general `<name>-*` rule still maps them)). If a PNG matches no section, place it in the nearest preceding module section. This
is a **safety net** for captures whose embed step was skipped mid-bootcamp
(`../bootcamp-onboarding/module-completion.md` makes the embed a required step, but this guarantees
the recap PDF still shows captured screenshots if one was missed). Append-only and **idempotent** —
never rewrite a completed section's prose (INV-085), never add a reference that already exists, and
skip any image that is missing or unreadable. Like every graduation step it is
non-blocking: if it is uncertain, warn and continue — never block the PDF on a screenshot.

Captures are named `<name>-<tab-slug>.png` (see
`../module-03b-truthset-visualization/visualization-api-reference.md` → "Tab identifiers and
deep-linking"), so the **tab slug gives the caption**: use the tab's display name rather than
inventing a description. A backfilled caption must never assert content that was not confirmed by
opening the image.

One tab needs more than its slug. A **Search / Probe** capture taken from the static snapshot has an
inert search box (the snapshot has no engine), and a bare "Search / Probe" caption on an empty search
box implies a result set that was never captured — the defect INV-123 forbids. When the image opened
shows an empty or inactive search state, say so in the caption. This matters here and not only at
capture time because a backfill runs precisely when the capture step's own caption never happened.

⛔ **Insert in the app's tab order, not in filename-discovery order.** That same tab table's row
order is the embedding order. Backfilling by directory scan is what produced a recap whose images
ran Entity Graph → Cross-Source → Search/Probe → Merge Statistics → Match Keys → Feature Scores —
append order, against an app whose tabs run left to right in a different sequence. Ordering the
image lines within a section is not a prose rewrite: the append-only rule (INV-085) protects the
section's **narrative**, and these lines are the backfill's own output.

**Verify the screenshots the recap actually carries (warn, never block).** Three checks, each
best-effort and each non-blocking (INV-129) — the backfill above only maps PNGs that *exist*, so
none of these are covered by it:

1. **A visualization section carrying fewer images than were captured.** For each completed module
   whose recap section references a `docs/visualizations/*.html` artifact, compare the count of
   `![...](...)` lines in that section against how many tabs were actually captured for it. Warn on
   any **shortfall**, not only on zero.

   Get the captured count from an external source, never from the recap:
   - **Preferred — the capture manifest.** `capture_screenshots.py` writes
     `docs/visualizations/<name>-tabs.json` recording `captured` (one entry per PNG written),
     `not_present`, `not_applicable` and `failed`. A `not_applicable` tab is **not** a shortfall:
     the app suppresses a tab whose data does not exist (Cross-Source with one data source,
     Match Keys and Feature Scores with no multi-record entities), so it was never on screen and
     is correctly absent from the recap. `generate_recap_pdf.py`'s `--check` already reads it and fails on a
     shortfall, naming the missing tab slugs; if `--check` reported
     `SKIPPED: tab-coverage check`, no manifest was found and this check has **not** run — say so
     rather than treating it as passed (INV-163).

     ⚠️ **`--check` also reports a manifest that *undercounts*** — one recording fewer captured tabs
     than there are `<name>-*.png` files beside it — as `the manifest undercounts`. Read that as the
     coverage check above having measured against too small a denominator, not as a missing image.
     The usual cause is a **targeted re-capture**: re-running capture for one tab used to rewrite the
     manifest from scratch, leaving `captured_count: 1` where six tabs had been captured, after which
     coverage passed on a 1-of-1 denominator and would have passed just as cheerfully with five of
     the six images lost. `write_manifest` now merges instead of replacing, so this should not recur;
     the count against the PNGs is what notices if that merge is ever bypassed. Fix the manifest (or
     re-run the full capture) and re-check rather than reading the coverage line as a pass.
   - **Fallback — the PNGs on disk.** Count `docs/visualizations/<name>-*.png` for that
     visualization's base name and compare against the section's image lines.

   ⛔ **(INV-271) The manifest check is PER-NAME, and its denominator is the manifests that exist — so ask
   separately whether a manifest is MISSING (INV-193, INV-265).** "Did every captured tab reach the
   recap?" is answered for each manifest found; it cannot answer "should there have been another
   manifest?" A module that captured nothing contributes no manifest, no denominator, and no
   shortfall the check can see, and the `SKIPPED: tab-coverage check` branch fires only when **no**
   manifest exists at all — so with one present it stays silent.

   **The expected-visualization denominator closes it, and it does not come from the manifests.**
   `--check` derives the set of **expected visualizations** from `modules_completed` in
   `config/bootcamp_progress.json`, mapped to the visualization each producing module is specified to
   build — `truthset_verification` for the Truth Set module, `results_visualization` for Module 7 —
   and reports, by name, any expected visualization with no manifest:

   ```text
   SKIPPED: tab-coverage check for 'results_visualization' — the 'query_visualize_discover'
   module ran (it is in modules_completed) … Coverage for it has NOT been measured — this is
   not a pass …
   ```

   When that fires, `--check` **withholds the coverage figure entirely** and prints
   `Tab coverage NOT reported: N expected visualization(s) have no manifest` instead. Relay that as
   an **unrun** check naming the visualization and the module that owed it — never as a pass, and
   never alongside a coverage percentage.

   ⚠️ **This is why it matters, in the artifact that leaves with them.** On a 2026-08-25 run the
   check reported *"6 of 6 captured tabs reached the recap"* — a clean pass — while the entire
   Module 7 application, built over the Bootcamper's **own** resolved data, had been captured not at
   all. The recap PDF illustrated the bootcamp with six pictures of the demo Truth Set, and the
   Bootcamper's cross-source entities and fraud leads appeared only as prose. The sentence was true
   of the manifests that existed and false of the bootcamp.

   ⛔ **(INV-271) Offer the remedy — it is cheap while the artifacts are still on disk.** Re-start the app and
   re-run the capture against it with the bundled tool,
   `python3 "{{host.scripts_dir}}/capture_screenshots.py" --url http://localhost:<port> --name <name>`
   (INV-185; skill-relative fallback `{{host.scripts_relative}}/capture_screenshots.py`, INV-252), then
   re-embed via the backfill path, rather than proceeding with a recap that pictures the sample
   dataset in place of the Bootcamper's results.

   ⚠️ **None of this is blocking.** The recap PDF is produced unconditionally (INV-048) and a missing
   manifest does **not** fail `--check`; the requirement is that graduation **states** the shortfall,
   not that it refuses to graduate. Do not re-state Module 7's capture instruction either — it is
   already explicit, and a fourth copy is the state-it-once violation (INV-183, INV-300). What was missing was
   the silence afterward, and that is what this closes.

   ⛔ **Do not use the generator's `embedded N of M images` figure for this.** Its denominator is
   the count of `![](…)` links in the recap it is measuring, so a section that embedded four of six
   captured tabs reports `embedded 4 of 4 images` — a perfect score against an incomplete set. It
   answers "did every link render", never "did every tab arrive". A prior session cited
   `embedded 12 of 12` to a Bootcamper as proof the screenshots were complete while they were
   asking about exactly this; it was right only by luck of the input.

   Zero remains the worst case and is still covered: it shipped a Truth Set visualization section
   with no screenshots at all — no PNG existed, so the backfill found nothing to backfill and said
   nothing.
2. **Duplicate images within one section.** If two embedded images in the same section are
   byte-identical, or have identical pixel dimensions and were written within the same second, warn:
   that is the signature of capturing one tab repeatedly rather than one image per tab.
3. **Captions that cannot be checked.** If an embedded filename carries no recognized tab slug, warn
   that its caption cannot be verified against a tab and should be confirmed by opening the image.

**Fold the Bootcamper's notes into the recap (after reconcile, before normalize and render).**
If `docs/bootcamp_notes.md` exists and carries at least one `### ` note, append its notes to
`docs/bootcamp_recap.md` **after the last module section**, fenced exactly like this
(INV-258):

```markdown
<!-- BOOTCAMP-NOTES:START -->
## Notes, Ideas and Questions

{the note entries, in capture order, exactly as written in docs/bootcamp_notes.md}
<!-- BOOTCAMP-NOTES:END -->
```

⛔ **The fence is what makes this safe, not the heading text.** Every `## ` heading in the recap
is parsed as a module, so a notes section recognized by its *title* would be one renamed module
away from being mis-parsed — and a Bootcamper's private note one heading away from being printed
on their Certificate of Completion (INV-100). The generator lifts this block out **before** module
parsing begins, so nothing inside it can become a module.

- **Append-only and idempotent (INV-085).** Re-running graduation must not duplicate the section:
  if the fence is already present, replace its contents rather than appending a second block. It
  never touches a module section.
- ⛔ **With no notes, write nothing** — no fence, no heading, no "(none)" page. An empty notes
  section on a keepsake is worse than an absent one.
- **`docs/bootcamp_notes.md` itself survives graduation intact.** The fold copies; it never moves,
  empties or deletes the bootcamper's notes file.

**Fold the handover into the recap (after the notes fold, before normalize and render).** Write
Step 0b's two lists, the takeaway and the "Next time" request into `docs/bootcamp_recap.md` **after
the notes block** (after the last module section when there are no notes), fenced exactly like this:

```markdown
<!-- BOOTCAMP-HANDOVER:START -->
## What You Take With You

### Decisions you made

- {Module name}: {the decision, as recorded in that module's Questions & Responses}

### How you got it built

- **{Module name}:** you asked for {…}; the AI built {…} with the Senzing MCP server.

### Your takeaway

{the Bootcamper's one line, as given}

### Next time

{their request, as given, or: **The guide's draft (you passed):** {the draft}}
<!-- BOOTCAMP-HANDOVER:END -->
```

⛔ **(INV-258) The fence keeps the handover out of the modules, not its heading.** The generator
lifts this block with its own lifter before module parsing, as it lifts the notes fence, and prints
it as its own page after the notes and before the Certificate of Completion. `--check` never counts
it as a module.

- **Replace, never append (INV-085).** If the fence is already present, replace its contents; never
  write a second block. `--check` fails on a recap that carries two. It never touches a module
  section.
- **Leave out what is absent.** A list with no entries, a passed takeaway, or a missing request is
  left out with its `### ` heading. ⛔ **When all four are absent, write no fence (INV-258)**: no
  heading and no "(none)" page, as the notes fold does; remove a fence an earlier run left.

**Normalize the Markdown (once, before rendering).** Now — after reconcile, the notes fold and the
handover fold, and **before** the Step 1b render — make a single best-effort CommonMark pass over
`docs/*.md`, including `docs/bootcamp_recap.md`. Scope it to top-level `docs/*.md` only: **never recurse into
`docs/feedback/`, and never rewrite, empty, or delete the bootcamper's feedback file**
(`docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md` must survive graduation intact — INV-015).
During the bootcamp these files were written plain (see
`../bootcamp-onboarding/ground-rules.md` → "Markdown files"); this is where they get prettified.
**Run the bundled normalizer** rather than reformatting by hand — it enforces the house rules and,
more importantly, enforces the content guard below in code:

```bash
python3 "{{host.scripts_dir}}/normalize_docs_markdown.py"
# or, if {{host.plugin_root_var}} is unset: python3 {{host.scripts_fallback}}/normalize_docs_markdown.py
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

It applies blank lines around headings (MD022), fenced blocks (MD031) and lists (MD032); a language
on every fenced block (MD040); and `**Label:**` colon spacing (a space after the colon, none
before). It globs top-level `docs/*.md` only and never recurses, so the feedback file is
structurally out of reach.

⛔ **The pass is purely cosmetic, and that is checked, not assumed.** It must never reorder, remove,
or rewrite the prose of a completed `## {Module name}` section, nor drop any of its four subsections
(Information Shared, Questions & Responses, Actions Taken, End-of-Module Summary). The normalizer
fingerprints each file's non-whitespace content line by line before and after and **restores the
original** if the result does not carry every source line forward — the one permitted change being an
opening fence gaining an info string. This matters because the pass runs *immediately before* the
render: a cosmetic step that dropped prose would produce a valid, prettier, **shorter** recap, and the
generator's content-retention figure (INV-110) is computed against the normalized file, so it would
report success against already-damaged input.

If the normalizer reports a file left as written, that is a normalizer bug — say so and continue with
the file unformatted; never hand-edit the prose to make formatting pass. Like every graduation step
this is non-blocking: if it fails or is unavailable, warn, leave the content as written, and continue
— a formatting issue is never a reason to skip the PDF.

⛔ **(INV-166) Relay the normalizer's mojibake warning; never repair it.** For a file whose lines
look like UTF-8 text read as Windows-1252 and written back, the normalizer writes
`<path>: WARNING: N line(s) look like Windows-1252 mojibake …` to stderr and still exits 0, so a
zero exit is not a clean result. Read its stderr. For each such line, tell the Bootcamper in one
plain sentence which file and lines look double-encoded, and that rewriting them from the UTF-8
source fixes them
(`../bootcamp-onboarding/ground-rules.md` → "Windows and PowerShell"). Do not edit the file to
repair it: a repair is a content change, and the pass changes formatting only (INV-110). The
warning is a statement, not a 👉 question, and the step continues.

### 1b. Render the PDF

Generate `docs/bootcamp_recap.pdf` with the bundled generator. It always produces
a valid PDF (a professionally designed one when `fpdf2` is installed, a plainer
stdlib-rendered one otherwise), so a missing `fpdf2` is never a reason to skip.

**Prefer the professionally designed renderer.** Before rendering, check whether
`fpdf2` is importable (`python3 -c "import fpdf"`). If it is not, offer to install it
so the designed renderer is used (a cover page, a table of contents with page
numbers, color-coded per-module sections, and page footers — INV-048, the recap PDF
should look professional). Install it **robustly**, never with a bare `pip`:

- **Prefer a project-local virtualenv.** This sidesteps PEP 668
  "externally-managed-environment" Python (common on macOS/Homebrew and many Linux
  distros) and never touches the global/system Python:

  ```bash
  # Linux/macOS:
  python3 -m venv data/temp/recap-venv
  data/temp/recap-venv/bin/python -m pip install fpdf2
  # Windows:
  python3 -m venv data/temp/recap-venv
  data/temp/recap-venv/Scripts/python -m pip install fpdf2
  ```

  Guide-run; unverified on Windows: no test runs it
  there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

  Then run the generator with **that venv's** Python (below) so it imports `fpdf2`.
- **Never call bare `pip`** — a stale shim on PATH may point at a deleted
  interpreter. Always go through an explicit interpreter: `python3 -m pip`, on
  Windows too. `--user` / `--break-system-packages` are last-resort
  opt-ins only, never the default.
- **Degrade gracefully.** If the bootcamper declines, or venv creation / the install
  fails (offline, no `ensurepip`, etc.), proceed with the stdlib fallback — it still
  produces a valid, complete PDF, so this never blocks graduation.

(Rasterizing pages to PNG to check the layout is **not** a maintainer-only aid — it is part of
verifying the render, below. `poppler`'s `pdftoppm` is the tool to reach for; `pymupdf` also works
where it happens to be installed. Neither is required — but a check that does not run MUST be
reported as skipped rather than degrading silently, per "Say what you could not verify" below.)

Locate and run the bundled script (it ships with this plugin). Use the venv's Python
if you created one above; otherwise `python3`:

```bash
# fpdf2 already importable, or using the stdlib fallback:
python3 "{{host.scripts_dir}}/generate_recap_pdf.py"
# Or, when you installed fpdf2 into the project-local venv above (Linux/macOS):
data/temp/recap-venv/bin/python "{{host.scripts_dir}}/generate_recap_pdf.py"
# Windows:
data/temp/recap-venv/Scripts/python "{{host.scripts_dir}}/generate_recap_pdf.py"
```

Guide-run; unverified on Windows: no test runs it
there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

If `{{host.plugin_root}}` is not set in the current context, resolve the script
relative to this skill's directory instead (this skill lives at
`skills/graduation/`, so the generator is in `{{host.scripts_relative}}/`, counted from there):

```bash
python3 {{host.scripts_fallback}}/generate_recap_pdf.py
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

The script reads `docs/bootcamp_recap.md` and writes `docs/bootcamp_recap.pdf`.

- **Success** is a `PDF generated:` line on stdout with exit 0. Only then tell the bootcamper: "📄 Recap PDF generated at `docs/bootcamp_recap.pdf`." Never claim success without that line. That line also reports how much of the recap reached the PDF (e.g. `rendered 25201 of 25467 source characters (99%)`); if it is well below 100%, content is being dropped — check the recap's structure before handing the PDF over. When the recap references screenshots it additionally reports `embedded N of M images` — **read this, and do not treat the retention figure as covering it.** Retention counts characters, so a PDF that lost every screenshot still reports ~99%; `embedded 0 of 6` is the only line that says so. Any shortfall means an image path did not resolve, and the generator names each one on stderr as `skipped image (not found): …` with the directories it searched.
- **Image paths in the recap are relative to `docs/bootcamp_recap.md`, and the generator resolves them that way.** Write them exactly as Step 1a says — `![alt](visualizations/<file>.png)` — which is what a Markdown reader of the recap needs, and what the PDF now needs too. Do **not** "fix" a path to `docs/visualizations/...` to suit the PDF: that breaks the Markdown recap (it resolves to `docs/docs/...`) and is no longer necessary. Equally, do not `cd docs` before rendering to make images appear; if images are missing, the path or the file is wrong, not the working directory.
- **`WARNING: … some sections are incomplete` with exit 0** means the recap was recognizable but a section is missing a subsection. The PDF was still written and is still valid — backfill per 1a and re-render if you can, but this never blocks graduation.
- **`ERROR: refusing to render …` with a non-zero exit means NO PDF was written.** The generator refuses when the input is not a bootcamp recap (no `## {Module name}` sections, or no section carrying its `### ` subsections) or when most of the content would be dropped — because an empty-looking-but-valid PDF is worse than none. Do **not** announce a PDF. Say plainly that the recap PDF could not be generated and why, then fix the cause: confirm `docs/bootcamp_recap.md` really is the recap (not some other Markdown file) and that its sections carry the four subsections, then re-render. If it cannot be fixed, fall back to the inline render below — never leave graduation with the bootcamper believing a PDF exists when it does not.
- **Content check (required after every render, non-blocking):** run the script with `--check --expect-modules "<semicolon-separated display names of the modules reconciled in Step 1a>"` — this confirms each present section carries the four required subsections, that every **End-of-Module Summary** carries its three labeled blocks (What you accomplished / Files produced / Why it matters — backfill per 1a if it reports any missing), flags any `![](…)` image target that resolves to no file (reported as `embedded image not found: …`, so a lost screenshot surfaces here rather than in the finished PDF), **and** flags any completed module missing its section entirely. Separate the names with **semicolons**, not commas, since some names contain commas (e.g. "Query, Visualize and Discover" and "Data Quality, Mapping, and Transformation" — the latter contains two). (The names are the same ones Step 1a ensured have sections, so pass them directly; whole-module presence is primarily guaranteed by that reconcile.) If it reports gaps, backfill per 1a and re-render. A gap never blocks graduation.

  ⚠️ **This is no longer the first time `--check` runs, and its findings should normally be empty.**
  `../bootcamp-onboarding/module-completion.md` Step 2c runs the same check after every module's
  append, so a structural fault — most importantly a subsection written as a bold label rather than
  an `###` heading, which renders identically to a human and drops the whole section from the PDF —
  is caught at the module that wrote it. A finding **here** therefore means something Step 2c could
  not see: a section damaged after its module closed, a module whose Step 2c check could not run, or
  a whole-file property (image targets, tab coverage, `--expect-modules`) that only exists at
  graduation. Treat a structural finding at this point as a signal worth reading, not routine.
- **If the bundled script cannot be located or run:** do not stop. Generate the PDF inline instead: parse `docs/bootcamp_recap.md` and render a cover page plus one page per module (each with Information Shared, Questions & Responses, Actions Taken, End-of-Module Summary) using `fpdf2` if importable, else a minimal valid PDF. On either path, draw every End-of-Module Summary's three labeled blocks — What you accomplished, Files produced, Why it matters — and mark one the recap does not carry as `(not recorded)` rather than omitting it or inventing its content (INV-157). The recap Markdown at `docs/bootcamp_recap.md` is always the source of truth, so content is never lost.

⛔ **Verify the artifact, not the exit code.** A `PDF generated:` line, a zero exit, and a high
retention percentage are all necessary and all demonstrably insufficient: in one session four separate
steps reported success while producing wrong output — three screenshots of the same tab with two
invented captions, a certificate footer whose glyphs were sliced in half by the page border, an entire
match-key table drawn off the page, and bullet lists whose item boundaries were invisible. None raised
an error and two reached a signed keepsake. The retention figure *cannot* catch off-page content,
because the text is in the content stream and merely positioned outside the page box.

So inspect the rendered artifact. Each check below is **best-effort and non-blocking** — run what the
toolchain supports, warn on what it finds, and never block graduation on a verification step
(INV-129, INV-052/INV-066). None of these is a 👉 question; this is agent-side apparatus, not
bootcamper-facing output (INV-012).

- **Rasterize before trusting text extraction.** `pdftoppm -r 100 -png -f N -l N <pdf> <prefix>` the
  certificate page and any page whose layout changed, and **look at the image**. Text extraction
  reports a border-clipped string as present and correct; only the raster shows the glyphs cut in
  half.
- **Probe positively for content you know is there.** `pdftotext` the output and grep for a
  distinctive string from the source — a table header, a match-key pattern, the cover subtitle in
  full. A count of **0** is the finding. This is the only check that catches content rendered outside
  the page box.
- **Count unique image XObjects, not `/Subtype /Image` occurrences.** References are counted more than
  once, so the naive grep reported 12 for 10 images. Reach for these in order, and use the first
  available: (1) the generator's own `embedded N of M images` line, which needs no tool at all and is
  the count the renderer actually achieved; (2) **Pillow**, which `fpdf2` already pulls in — so when
  you created the project-local venv above it is *already importable in that same interpreter*, and
  opening the embedded images there gives an honest count and their dimensions with **no new
  dependency**; (3) `pdfimages -list <pdf>` where poppler exists; (4) the `/Subtype /Image` grep,
  **which overcounts** — if you fall back to it, label the number as approximate and say so.
- ⛔ **`embedded N of M images` measures references, not tab coverage — never cite it as evidence
  that every tab is present.** Its denominator is the number of `![](…)` links in the recap being
  rendered, so it is derived from the same file as its numerator: if only four of six captured tabs
  were ever embedded, the line reads `embedded 4 of 4 images`. It is structurally incapable of
  detecting the very incompleteness a Bootcamper asking "are all the tabs here?" is describing, and
  a prior session cited `embedded 12 of 12` as proof of completeness while being asked exactly that
  — correct by luck of the input, not by measurement. The count that *can* answer it is the
  generator's separate `N of M captured tabs reached the recap`, whose denominator comes from
  `capture_screenshots.py`'s `<name>-tabs.json` manifest; when `--check` prints
  `SKIPPED: tab-coverage check`, no manifest was found and the question is **unanswered** rather
  than answered yes (INV-163).
- **Open every captured PNG before writing its caption** (INV-123, and
  `../bootcamp-onboarding/module-completion.md` → "Capturing visualization screenshots").
- **Re-run `--check --expect-modules "…"` after every render**, semicolon-separated — two module
  display names contain commas.
- **When you replace text, confirm both directions:** the new string is present **and** the old one is
  gone. Decompress the content streams rather than assuming the replacement landed.

⚠️ **A caution learned the hard way:** verify your verification. A regex-based content-stream reader
using strict `zlib.decompress` silently drops any stream whose slice is off by a few bytes, which
looks exactly like a lost page. Cross-check a suspicious "missing content" result with a second,
independent tool (`pdftotext`) before concluding the artifact is broken — the reader is the likelier
culprit.

**Toolchain these assume, and what it looks like per platform.** Every check above is doable with
plain headless Chrome and poppler, which is why nothing here — or in the screenshot capture path — is
designed around a heavier dependency. Probe for a tool before using it and skip the check when it is
missing; **never install one to satisfy a verification step** (INV-129) — that includes poppler, so do
not offer `scoop install poppler` / `brew install poppler` / `apt install poppler-utils` to make a
check pass.

- **Linux:** poppler is usually present (`pdftoppm` / `pdftotext` / `pdfinfo` / `pdfimages`),
  so the full check set normally runs. One field machine had `fpdf2`, headless Chrome and poppler, and
  did **not** have Playwright, Selenium, or PyMuPDF.
- **macOS: poppler is NOT part of the base system.** macOS ships none of the four binaries, and you
  **must never install them** to make a check pass (INV-129) — they arrive only via an explicit
  `brew install poppler`, which a Bootcamper has no reason to have run.
  Observed 2026-07-31 on macOS 26.5.2 (Apple Silicon) **with Homebrew installed and in active use for
  the Senzing SDK itself**: all four absent, poppler not installed as a formula. Do **not** group
  macOS with Linux here — the habitual pairing for Unix-like tooling is wrong for poppler, which is a
  Linux distribution package rather than a macOS system component.
- **Windows: poppler is typically absent.** On one Windows 11 workstation only `pdftotext` resolved —
  `pdftoppm`, `pdfinfo` and `pdfimages` were all missing. That is the normal Windows case, not a
  broken setup.
- **So the missing-poppler path is the expected case on both macOS and Windows**, and it removes
  exactly the two checks text extraction cannot substitute for: the page raster and the honest image
  count.

  ⚠️ **Do not fall back on `pdftotext` without probing for it.** On Windows it was the one binary
  that resolved, so earlier guidance said to "keep the positive `pdftotext` probe" — on macOS it is
  missing along with the other three, so that advice is not actionable there. Probe, then use it or
  record it as skipped.

  What needs **no** new dependency on either platform, so the reduced set is actionable rather than
  merely reduced:

  - **Pillow**, which `fpdf2` already requires (`fpdf2` 2.8.5 declares `Pillow>=8.3.2` — verified
    2026-07-31), so when you created the project-local venv above it is *already importable in that
    same interpreter*. This is the honest image count and their dimensions.
  - **The generator's own success line**, which needs no tool at all: `embedded N of M images` is the
    count the renderer achieved, and `N of M captured tabs reached the recap` is the coverage figure.
    Keep them distinct — the first cannot answer the coverage question (see the ⛔ above), and the
    second is absent when no capture manifest exists.

  **Report the page raster as not verified** — do not imply the layout was checked (INV-163).

⛔ **Say what you could not verify.** Any check skipped for a missing tool MUST be recorded as skipped,
naming the check and the tool, and the closing announcement MUST state which verification steps did
not run. "Verified" that silently means "verified except for the two strongest checks" is the same
class of overstatement this section exists to prevent: a keepsake whose layout nobody could inspect is
acceptable, one described as verified when its layout was never inspected is not. A skipped check
still never blocks graduation (INV-163, INV-052/INV-066), and this stays agent-side apparatus rather
than bootcamper-facing output (INV-012).

⚠️ **Spend a reduced check set on what only it can catch.** When tools are missing, prioritize: the
positive `pdftotext` content probe (the only check that catches content positioned outside the page
box) and the image count (which catches silently-dropped screenshots — the failure that shipped a
recap with 2 images where 8 were expected, detectable *only* by counting). The page raster is the one
genuinely tool-gated check; its absence is the thing to announce.

### 1c. Offer the graduation video (optional)

The recap PDF now exists, so the video can reuse its certificate's name and date. The video is
optional. It is built from the B-roll each module saved (`../bootcamp-onboarding/module-completion.md`
Step 2e) and rendered by the bundled renderer, `generate_recap_video.py` (resolved under **Render it**
below), which writes `docs/bootcamp_recap.mp4`.

⛔ **(INV-340) The video never blocks graduation.** Every failure below, whether a declined install, a
failed install, an invalid storyboard or a failed render, skips the video with a one-line message
naming what failed, and graduation continues to Step 2.

**The offer.** When Step 1b is done, end the turn on this pinned question. Ask it once per graduation
(INV-006, INV-056):

> 👉 **Would you like a narrated 2-minute graduation video of your bootcamp?** (Saved to `docs/bootcamp_recap.mp4`; reply no to skip.)

- **No:** continue straight to Step 2 in the same reply turn.
- **Yes:** continue below.

⛔ **(INV-340) On no, write no video file at all:** no `docs/video/storyboard.json` and no
`docs/bootcamp_recap.mp4`. The storyboard is written only after a yes.

**Model quality.** There is no model question and no model statement here. Write the narration on
whatever the bootcamper is running and say nothing about it (see "After the preface").

#### Write the storyboard

Write `docs/video/storyboard.json` in the renderer's format. Run the renderer with `--schema` to print
every scene type and its fields; the example below shows the shape. `video.bootcamper` is the name the
certificate prints (INV-100; pre-check 4: `name` in `config/bootcamp_preferences.yaml`, else the recap's
`**Bootcamper:**` line, else "Bootcamper"), and `video.graduation_date` is the recap's `**Completed:**`
date that Step 1a stamped. Set `video.title` to "Senzing Agentic AI Bootcamp". Use the bootcamper's
name in the narration where it fits: the Intro, the business problem and the certificate.

**Where each scene comes from.** Scenes run in the order the bootcamper experienced the bootcamp:
the Intro, then Bootcamp preparation, then each module in `modules_completed` order, then the ending.

- **The Intro** always opens the video, on every path. It is one `title_card` built from the
  `video` object alone, and writes no B-roll entry:
  - `"_module": "intro"`, the one `_module` tag that is not a module's state token;
  - `module`: "Senzing Agentic AI Bootcamp";
  - `highlight`: "[Name] · [Date]";
  - `narration`: "This is [Name]'s Senzing Agentic AI Bootcamp, [Date]."

  `[Name]` is `video.bootcamper`, so the Intro shows exactly the name the certificate shows, the
  "Bootcamper" fallback included. `[Date]` is `video.graduation_date`, the recap's `**Completed:**`
  date, written out in words as the certificate prints it, `Month D, YYYY` (e.g. "October 1,
  2026"). The Intro carries the bootcamper's own name and the date, as the certificate does, and no
  record value.
- **Bootcamp preparation** always comes from `config/bootcamp_preferences.yaml`: the path, the selected
  modules and the `programming_language`, as one `title_card`. That module writes no B-roll entry
  (#298).
- **Every other module** comes from its entry in `docs/video/broll.json`, keyed by its state token.
  Its name-free `images` (see "Only name-free screenshots" below) become `image` scenes, its
  `facts` become the scenes in the table below, and its `highlight` becomes the narration, or a
  `title_card` highlight when it has nothing on screen.
- **A bootcamp with no `broll.json`** (it started on an older plugin version), or a module with no
  entry in it: build that module's scenes from its `## {Module name}` section in
  `docs/bootcamp_recap.md` and the screenshots under `docs/visualizations/` that section embeds.
  Write the image paths as `docs/visualizations/<file>.png`, relative to the project root, not the
  recap's `visualizations/…`. Use only the name-free ones among them, by the same rule.

**The five animated scenes.** Each of these modules is required, so each has a scene:

| Module | Scene type | Built from |
|---|---|---|
| Discover the Business Problem | `title_card` | the problem the bootcamper described (the entry's `highlight`), elaborated in the narration |
| Data collection | `counter` | the characteristics of their data: `facts.sources`, records per source |
| Data Quality, Mapping, and Transformation | `mapping` | `facts.mappings`, one scene per source, at most 8 fields each |
| Data processing | `loading` | the loading of their data: `facts.records_loaded` and `facts.entities_resolved` |
| Query, Visualize and Discover | `entity_merge`, then `counter` and `image` scenes | what was found: records, entities and sources, then `facts.statistics` and the name-free results screenshots |

When a module's figures are missing, draw its scene as a `title_card` with its highlight. Never
invent a number to fill a scene (INV-157's principle: never fabricate to fill a field).

⛔ **(INV-340) Aggregates only: no raw record values anywhere in the storyboard.** A scene may show counts,
source names, field and attribute names, and statistics. It may not show a name, an address, a phone
number, an identifier or any other value from the bootcamper's records, in any field, the narration and
captions included. `broll.json`'s text fields hold only aggregates (INV-341), but its `images` name
every screenshot the module produced, and a screenshot can show record values. So images pass the
name-free rule below before they go in. The recap may quote records (an entity the bootcamper
searched for, say), so on the fallback path lift only its aggregates. The video is a keepsake the
bootcamper is encouraged to share.

⛔ **(INV-340) Only name-free screenshots go in the video.** An image becomes an `image` scene only
when its file name is `<name>-<slug>.png` with `<slug>` one of the three name-free tab slugs below
(`capture_screenshots.py` `TABS` names them). Every other image is left out of the storyboard.

| Image | Tab | In the video |
|---|---|---|
| `<name>-match-keys.png` | Match Keys | yes: name-free |
| `<name>-feature-scores.png` | Feature Scores | yes: name-free |
| `<name>-cross-source.png` | Cross-Source | yes: name-free |
| `<name>-merge-statistics.png` | Merge Statistics | no: its "Largest resolved entities" list shows entity names and IDs |
| `<name>-search-probe.png` | Search / Probe | no: it shows the names that were searched |
| `<name>-entity-graph.png` | Entity Graph | no: a capture keeps the entity-name node labels whenever the graph has 40 nodes or fewer |
| `<name>.png`, a single-page capture such as `data_quality_assessment.png` or the mapping summary | none | no: a model-authored page can carry sample values |
| any other name, including the reserved `relationship-network` and `record-merges` slugs | any other | no: not on the allow-list |

- **The allow-list is the only way in.** A name that matches none of the three slugs is left out,
  so a new or renamed tab stays out until it is added to this table.
- **One rule for every image.** It applies to the Truth Set's images (`truthset_verification-…`)
  as to the bootcamper's own, and on the fallback path to the screenshots under
  `docs/visualizations/` the recap embeds.
- **A module left with no image** gets no `image` scene. Draw it as a module with nothing on
  screen: its `facts` scenes, or a `title_card` with its highlight, in the same seconds.
- **Nothing is cropped or edited.** A left-out image stays on disk and in the recap PDF.

**The ending (INV-340).** The last two scenes are always the `certificate`, then the `tag_line` with the text
**"Resolved: [Name], Senzing Bootcamp graduate."**, where `[Name]` is `video.bootcamper`. The renderer
sets it centered, "Resolved:" above the name and "Senzing Bootcamp graduate." on a line of its own.

**The time budget (INV-340).** The planned length is **2:00**. Each module gets this share of it:

| Module | State token | Share | Seconds (every module taken) |
|---|---|---|---|
| Intro | `intro` | 3% | 3.6 |
| Bootcamp preparation | `bootcamp_preparation` | 3% | 3.6 |
| Entity Resolution Concepts | `entity_resolution_concepts` | 4% | 4.8 |
| Discover the Business Problem | `business_problem` | 15% | 18.0 |
| SDK setup | `sdk_setup` | 3% | 3.6 |
| System verification | `system_verification` | 3% | 3.6 |
| Truth Set visualization | `truthset_visualization` | 10% | 12.0 |
| Data collection | `data_collection` | 10% | 12.0 |
| Data Quality, Mapping, and Transformation | `data_quality_mapping` | 10% | 12.0 |
| Data processing | `data_processing` | 5% | 6.0 |
| Query, Visualize and Discover | `query_visualize_discover` | 30% | 36.0 |
| You graduated! | `graduation` | 4% | 4.8 |

Intro, Bootcamp preparation and You graduated! always count, whichever optional modules were
skipped. Every other module counts only when it is in
`modules_completed`. Leave out the modules the bootcamper did not take (the optional modules skipped
on a Customized path), and scale the shares of the rest back up to 100%:

`seconds = 120 × share ÷ (sum of the shares that count)`

Round each module to one decimal, and give any rounding remainder to Query, Visualize and Discover so
the total is exactly 120. For example, a Customized path that skipped Entity Resolution Concepts,
System verification and Truth Set visualization counts 83%:

| Module | Seconds (83% counted) |
|---|---|
| Intro | 4.3 |
| Bootcamp preparation | 4.3 |
| Discover the Business Problem | 21.7 |
| SDK setup | 4.3 |
| Data collection | 14.5 |
| Data Quality, Mapping, and Transformation | 14.5 |
| Data processing | 7.2 |
| Query, Visualize and Discover | 43.4 |
| You graduated! | 5.8 |

A module's seconds may be split across several scenes; the scene durations for a module add up to
its seconds, and You graduated!'s seconds are shared between the certificate and the tag line. Tag
each scene with its module's state token in a `_module` key (the Intro with `intro`). The renderer ignores keys that begin
with `_`, and the tag tells you which module a scene belongs to when you re-time it below. The
renderer lengthens a scene whose narration runs past its planned duration, so keep each narration
to about 2.5 words for every second of its scene after the first. The Intro's line usually runs a
little past its 3.6 seconds; the renderer lengthens it and reports it, and the total stays inside
the tolerance below.

A storyboard for a Core bootcamp, with every module taken:

```json
{
  "video": {"bootcamper": "Ada Lovelace", "graduation_date": "2026-09-30", "title": "Senzing Agentic AI Bootcamp"},
  "scenes": [
    {"_module": "intro", "type": "title_card", "duration": 3.6, "module": "Senzing Agentic AI Bootcamp", "highlight": "Ada Lovelace · September 30, 2026", "narration": "This is Ada Lovelace's Senzing Agentic AI Bootcamp, September 30, 2026."},
    {"_module": "bootcamp_preparation", "type": "title_card", "duration": 3.6, "module": "Bootcamp preparation", "highlight": "Core path, 11 modules, Python", "narration": "Ada chose Core: eleven modules, in Python."},
    {"_module": "entity_resolution_concepts", "type": "title_card", "duration": 4.8, "module": "Entity Resolution Concepts", "highlight": "How records become entities", "narration": "First: records that describe one thing become one entity."},
    {"_module": "business_problem", "type": "title_card", "duration": 18, "module": "Discover the Business Problem", "highlight": "One customer view across two systems", "narration": "Then Ada's own problem. The same customers sat in two systems, under different spellings and addresses, and nobody could say how many customers there really were. That was the question to answer."},
    {"_module": "sdk_setup", "type": "title_card", "duration": 3.6, "module": "SDK setup", "narration": "The Senzing SDK went in."},
    {"_module": "system_verification", "type": "title_card", "duration": 3.6, "module": "System verification", "narration": "Its system check passed."},
    {"_module": "truthset_visualization", "type": "image", "duration": 6, "image": "docs/visualizations/truthset_verification-match-keys.png", "heading": "Truth Set: match keys", "narration": "A practice run on the Truth Set showed resolution at work."},
    {"_module": "truthset_visualization", "type": "image", "duration": 6, "image": "docs/visualizations/truthset_verification-cross-source.png", "heading": "Truth Set: cross-source overlap", "narration": "And how its sources overlapped."},
    {"_module": "data_collection", "type": "counter", "duration": 12, "title": "Records per source", "items": [{"label": "CUSTOMERS", "value": 1200}, {"label": "VENDORS", "value": 340}], "narration": "Then Ada's own data: two sources, twelve hundred customer records and three hundred forty vendor records."},
    {"_module": "data_quality_mapping", "type": "mapping", "duration": 6, "source": "CUSTOMERS", "fields": [{"from": "last_nm", "to": "NAME_LAST"}, {"from": "street", "to": "ADDR_LINE1"}], "narration": "Each field was mapped to a Senzing attribute."},
    {"_module": "data_quality_mapping", "type": "mapping", "duration": 6, "source": "VENDORS", "fields": [{"from": "vendor_name", "to": "NAME_ORG"}, {"from": "addr1", "to": "ADDR_LINE1"}], "narration": "Vendors too, names and addresses alike."},
    {"_module": "data_processing", "type": "loading", "duration": 6, "records": 1540, "entities": 1310, "narration": "All 1,540 records loaded into 1,310 entities."},
    {"_module": "query_visualize_discover", "type": "entity_merge", "duration": 12, "records": 1540, "entities": 1310, "sources": ["CUSTOMERS", "VENDORS"], "narration": "Here is what Senzing found. Records from both sources came together as the entities they really are."},
    {"_module": "query_visualize_discover", "type": "counter", "duration": 12, "title": "What Senzing found", "items": [{"label": "Entities in both sources", "value": 118}, {"label": "Entities with several records", "value": 190}], "narration": "One hundred eighteen entities appear in both sources, the overlap nobody could see before."},
    {"_module": "query_visualize_discover", "type": "image", "duration": 12, "image": "docs/visualizations/results_visualization-cross-source.png", "heading": "Your sources, side by side", "narration": "Every one of them is in Ada's own results app."},
    {"_module": "graduation", "type": "certificate", "duration": 2.0, "narration": "Congratulations, Ada."},
    {"_module": "graduation", "type": "tag_line", "duration": 2.8, "text": "Resolved: Ada Lovelace, Senzing Bootcamp graduate.", "narration": "Resolved: Ada Lovelace, Senzing Bootcamp graduate."}
  ]
}
```

#### Offer the Piper voice

The renderer narrates with a local Piper neural voice, `en_US-ljspeech-high`, whenever the Python
that runs it can find `piper` and the voice sits in `data/temp/piper-voices/`. Otherwise it uses the
computer's built-in voice. Piper is set up when both hold:

- `data/temp/recap-venv/` exists and its Python can find `piper`:
  `<venv python> -c "import importlib.util, sys; sys.exit(importlib.util.find_spec('piper') is None)"`
  exits 0. Here `<venv python>` is `data/temp/recap-venv/bin/python` (Windows:
  `data/temp/recap-venv/Scripts/python`).
- The voice is in `data/temp/piper-voices/`: `en_US-ljspeech-high.onnx` and its
  `en_US-ljspeech-high.onnx.json` both exist.

When Piper is set up, make no offer, and run `--check` and the render below with the venv's Python.

**The offer.** When Piper is not set up, end the turn on this pinned question, after the storyboard is
written and before the first render. Ask it once per graduation (INV-006, INV-056):

> 👉 **May I install the Piper neural voice so the narration sounds natural?** It downloads about 200 MB into this project: `piper-tts` (GPL-3.0, runs on your machine) into `data/temp/recap-venv/`, and the public-domain `en_US-ljspeech-high` voice into `data/temp/piper-voices/`. (Reply no to narrate with your computer's built-in voice, which sounds noticeably more robotic.)

When the venv will also get Pillow or `imageio-ffmpeg` (the next paragraph says when), the question
names them after `data/temp/recap-venv/`: "…into `data/temp/recap-venv/` along with Pillow and
`imageio-ffmpeg`, which rendering needs, and the public-domain `en_US-ljspeech-high` voice…". Name
only the one the venv will get when it gets one ("along with Pillow, which rendering needs," or "along
with `imageio-ffmpeg`, which rendering needs,"). Every other word stays the same.

**On yes,** install into the project only (INV-066), skipping each step that is already satisfied:

1. Create `data/temp/recap-venv/` with `python3 -m venv data/temp/recap-venv`, on Windows too, if
   it does not exist.
2. Run **one** `python -m pip install` with the venv's Python, installing `piper-tts` when the venv
   cannot find `piper`, plus Pillow when the venv's Python cannot `import PIL`, plus
   `imageio-ffmpeg` when there is no ffmpeg on `PATH`.
3. Download the voice by the route `piper-tts` documents, when it is not in
   `data/temp/piper-voices/` yet.

```bash
# Linux/macOS (add Pillow and imageio-ffmpeg to the same command when they are missing):
python3 -m venv data/temp/recap-venv    # only if it does not exist yet
data/temp/recap-venv/bin/python -m pip install piper-tts
data/temp/recap-venv/bin/python -m piper.download_voices en_US-ljspeech-high --data-dir data/temp/piper-voices
# Windows:
python3 -m venv data/temp/recap-venv    # only if it does not exist yet
data/temp/recap-venv/Scripts/python -m pip install piper-tts
data/temp/recap-venv/Scripts/python -m piper.download_voices en_US-ljspeech-high --data-dir data/temp/piper-voices
```

Guide-run; unverified on Windows: no test runs it
there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

When every step succeeds, **run `--check` and the render below with the venv's Python** from then on.
The venv now has Pillow and, without an ffmpeg on `PATH`, `imageio-ffmpeg`, so the exit-2 install
offer cannot follow a successful install.

**On no, or on any failure** (creating the venv, the `pip` install or the download), render with
the interpreter Step 1b used, as before, and the renderer narrates with the computer's built-in voice.
Graduation continues (INV-340), and the exit-2 install offer still applies to that render.

⛔ **(INV-066, INV-340) Never run `sudo`, a bare `pip`, or an install outside `data/temp/recap-venv/` and
`data/temp/piper-voices/`.**

#### Render it

Check the storyboard, then render it. Use the venv's Python when Piper is set up (above), otherwise the
same interpreter Step 1b used (the project-local virtualenv's Python when Step 1b created one,
otherwise `python3`). Pass no `--voice-model`: the renderer finds the voice at its default path,
`data/temp/piper-voices/en_US-ljspeech-high.onnx`.

```bash
python3 "{{host.scripts_dir}}/generate_recap_video.py" --check
python3 "{{host.scripts_dir}}/generate_recap_video.py"
# or, if {{host.plugin_root_var}} is unset: python3 {{host.scripts_fallback}}/generate_recap_video.py
# With Piper set up (Linux/macOS; Windows: data/temp/recap-venv/Scripts/python):
data/temp/recap-venv/bin/python "{{host.scripts_dir}}/generate_recap_video.py" --check
data/temp/recap-venv/bin/python "{{host.scripts_dir}}/generate_recap_video.py"
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

⛔ **(INV-340) Graduation never passes `--no-voice`, to `--check` or to the render.** The flag is an
opt-out for tests and manual renders, and the renderer prints a `WARNING:` line whenever it is passed.
The `--no-voice` row under "When the video has no voice" is the defensive case only.

**`--check` also checks the plan against `config/bootcamp_progress.json`.** It prints an `INVALID:`
line for each token in `modules_completed`, and for `intro`, `bootcamp_preparation` and `graduation`,
that no scene's `_module` names, and one for a planned total outside the renderer's tolerance
(`TARGET_SECONDS` ± `TOLERANCE_SECONDS` in `generate_recap_video.py`). Then it exits 1 with no
`VOICE:` line: add the missing module's scenes from the time budget above, or re-time the scenes, and
run it again, as exit 1 below says. A `SKIPPED:` line means the progress file held no readable
`modules_completed` list, so coverage went unchecked; it never blocks.

**Read `--check`'s `VOICE:` line before you render.** On a valid storyboard `--check` prints one
`VOICE:` line after `Storyboard valid`, naming the voice this interpreter would narrate with:
`VOICE: Piper (en_US-ljspeech-high)`, `VOICE: platform engine <name> (Piper is out: …)` or
`VOICE: none (…)`. When it names a voice other than Piper, a line pointing at "Offer the Piper voice"
follows it. When the `VOICE:` line names a voice other than Piper and the Piper offer has not been
made in this graduation, make the offer now, ending the turn on it, and do not render. When the
bootcamper already declined it, or its install failed, render without asking again (INV-006,
INV-056).

The renderer reads `docs/video/storyboard.json` and writes `docs/bootcamp_recap.mp4`. Act on its exit
code:

- **0, rendered.** It prints `Video generated:`, a `Duration:` line, a `Voice:` line and a `Music:`
  line. Go on to "Verify the video" below.
- **1, invalid storyboard.** Each `INVALID:` line names the field at fault. Fix those fields and run
  it again. If it is still invalid, skip the video.
- **2, a capability is missing.** No usable ffmpeg, or no Pillow; the `ERROR:` line says which. Make
  the install offer below.
- **3, the render failed.** Skip the video.

⛔ **(INV-340) Keep the storyboard whenever it was written.** Skipping the video leaves
`docs/video/storyboard.json` in place, so the video can be rendered later by running the renderer
again. The skip message says so, for example: "🎬 I couldn't render the graduation video (ffmpeg is
missing). Its storyboard is saved at `docs/video/storyboard.json`, so it can be rendered later." Then
continue to Step 2.

**The install offer (exit 2).** Offer it once (INV-006, INV-340), pinned:

> 👉 **Rendering the video needs ffmpeg. May I install `imageio-ffmpeg` into this project's virtualenv?** (Reply no to skip the video; its storyboard is kept so you can render it later.)

When Pillow is missing as well, name it in the same question: "Rendering the video needs ffmpeg and
Pillow. May I install `imageio-ffmpeg` and Pillow into this project's virtualenv?", with the same
answer hint. Pillow is missing when the virtualenv does not exist yet or its Python cannot run
`import PIL`. When ffmpeg is on `PATH` and only Pillow is missing, the question names Pillow alone.

On yes, install into the project-local virtualenv (INV-066). Step 1b's `fpdf2` install may have created
it already:

```bash
# Linux/macOS (add Pillow when it is missing):
python3 -m venv data/temp/recap-venv    # only if it does not exist yet
data/temp/recap-venv/bin/python -m pip install imageio-ffmpeg
data/temp/recap-venv/bin/python "{{host.scripts_dir}}/generate_recap_video.py"
# Windows:
python3 -m venv data/temp/recap-venv    # only if it does not exist yet
data/temp/recap-venv/Scripts/python -m pip install imageio-ffmpeg
data/temp/recap-venv/Scripts/python "{{host.scripts_dir}}/generate_recap_video.py"
```

Guide-run; unverified on Windows: no test runs it
there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

On no, or when the venv or the install fails, skip the video and keep the storyboard.

#### Verify the video

⛔ **Verify the rendered video, not the exit code (INV-129, INV-340).** Each check is best-effort and
non-blocking. A check that cannot run is recorded as skipped, naming the check (INV-163). Use the
ffmpeg the render used: `ffmpeg` on `PATH`, or the `imageio-ffmpeg` binary, whose path
`<venv python> -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` prints. Use
`ffprobe` where it exists. ⛔ **Never install a tool only to run a check (INV-129).**

1. **Duration: within the renderer's tolerance**, `TARGET_SECONDS` ± `TOLERANCE_SECONDS` in
   `generate_recap_video.py`, both bounds included. The render prints an `OUT OF TOLERANCE:` line
   after `Duration:` when its length falls outside it. Read it from the file (`ffprobe`, or the
   `Duration:` line `ffmpeg -i docs/bootcamp_recap.mp4` prints), not only from the renderer's own
   line.
2. **Frames.** Extract one frame at the midpoint of each scene, including the certificate and the
   tag line, and look at each one. For example, after creating `data/temp/video-check/`:
   `ffmpeg -ss <seconds> -i docs/bootcamp_recap.mp4 -frames:v 1 data/temp/video-check/scene-<n>.png`.
   Work the midpoints out from the planned durations, lengthened as the renderer's `OVERRUN:` lines
   report. Confirm that each frame shows its scene, that the certificate carries the right name and
   that the tag line reads "Resolved: [Name], Senzing Bootcamp graduate.".
3. **Audio.** Read the renderer's `Voice:` and `Music:` lines. There is an audio stream whenever
   either one is present: a `Voice:` line naming an engine (`Voice: <engine> (<n> of <m> scenes
   narrated)`), or `Music: yes`. Then the file carries an audio stream (`ffprobe`, or the `Audio:`
   stream line of `ffmpeg -i`). `Voice: none (…)` names why no voice spoke (`--no-voice`, `no speech
   engine found`, or `<engine> voiced no scene`): the captions carry the narration, and that is not a
   failure. Only with `Voice: none (…)` and `Music: off (storyboard)` together is there no audio
   stream.

**Out of tolerance.** When the render prints `OUT OF TOLERANCE:`, or the file's duration falls outside
the same tolerance, shorten the narration (a video that runs long) or lengthen it (a video that runs
short), starting with the scenes the `OVERRUN:` lines name, and re-render **once**. If it is still
outside, keep the video and say so, with its duration.

Tell the bootcamper in one line, naming the voice from the renderer's `Voice:` line: the engine it
names, for example "🎬 Your graduation video is at `docs/bootcamp_recap.mp4` (2:03), narrated by Piper
(en_US-ljspeech-high).". When the `Voice:` line is `Voice: none (…)`, that line only notes there is
no voice: "🎬 Your graduation video is at `docs/bootcamp_recap.mp4` (2:03), with no voice." Keep the
reason and any guidance for the closing announcement (below). Name any check that did not run, and
continue to Step 2.

#### When the video has no voice

Read the reason in the renderer's `Voice: none (…)` line (#339) and keep it, with the `Music:` line,
for the closing announcement, which is where the bootcamper hears it. There are three cases:

| `Voice:` line | What the closing announcement adds |
|---|---|
| `Voice: none (no speech engine found)` | the platform's speech engine, its install hint and the re-render command, below |
| `Voice: none (<engine> voiced no scene)` | names `<engine>` and says it could not voice the narration; no install hint, because the engine is installed |
| `Voice: none (--no-voice)` | nothing about installing; graduation never passes `--no-voice`, so this case is defensive |

A `Voice:` line that names an engine means the video has a voice, even when some scenes went
unvoiced: none of this applies, and the renderer's per-scene notes on stderr cover the rest.

This guidance is about the platform's speech engine only. Piper is a separate, opt-in voice, offered
once before the render ("Offer the Piper voice" above). When the bootcamper declined it, or its
install or its narration failed, the renderer fell back to the platform engine, so
`Voice: none (no speech engine found)` still means no platform engine was found. Give the platform
guidance below, and do not offer Piper again.

**The platform's speech engine (no speech engine found).** State it in one sentence:

- **Linux, WSL included:** the voice comes from `espeak-ng`. Read `ID` and `ID_LIKE` in
  `/etc/os-release` (a plain file; reading it installs nothing) and take the first row whose names
  appear in `ID`, then in `ID_LIKE`:

  | `ID` / `ID_LIKE` names | Install hint |
  |---|---|
  | `debian`, `ubuntu` | `sudo apt install espeak-ng` |
  | `fedora`, `rhel`, `centos` | `sudo dnf install espeak-ng` |
  | `arch` | `sudo pacman -S espeak-ng` |
  | `suse`, or a name starting `opensuse` | `sudo zypper install espeak-ng` |
  | none of these, or no `/etc/os-release` | install `espeak-ng` with your package manager |

- **macOS:** `say` is built in to macOS, so not finding it is unusual; say so. Give
  `brew install espeak-ng` as the fallback, because the renderer tries `espeak-ng` after `say`.
- **Windows:** the voice uses System.Speech, which comes with Windows PowerShell 5.1
  (`powershell.exe`). PowerShell 7 (`pwsh`) alone cannot load it, which is what the renderer's
  "not loadable" means; say so. There is no install command to give.

⛔ **(INV-066, INV-340) The install hint is the bootcamper's to run.** Never run `sudo` or a system
package manager (`apt`, `dnf`, `pacman`, `zypper`, `brew`) for it, and never install the engine for
them.

**The re-render command (no speech engine found).** The storyboard is kept, so once the engine is
installed the same command renders the video again with a voice. Write it out with resolved
absolute paths, so it runs as-is in the bootcamper's own terminal. `{{host.plugin_root}}` is unset
there, so never write it, a `<this-skill-dir>` placeholder or a relative path into the command.
Resolve three paths:

- **The interpreter Step 1c rendered with:** the project-local virtualenv's Python under the project
  root (`<project>/data/temp/recap-venv/bin/python`; on Windows
  `<project>\data\temp\recap-venv\Scripts\python.exe`), or else the absolute path of `python3`
  (`command -v python3`).
- **The renderer:** the absolute path that `{{host.scripts_dir}}/generate_recap_video.py`
  expands to in your shell (or the skill-relative fallback, resolved).
- **The project root:** the absolute path of the bootcamper's project.

The renderer's defaults are relative to the current directory, so pass the storyboard, the output and
the project root explicitly, and the command works from any directory. Use the platform's shell
syntax:

- **Linux and macOS** (POSIX, single-quoted):
  `'<interpreter>' '<renderer>' --storyboard '<project>/docs/video/storyboard.json' --output '<project>/docs/bootcamp_recap.mp4' --project-root '<project>'`
- **Windows** (PowerShell, double-quoted, through the `&` call operator):
  `& "<interpreter>" "<renderer>" --storyboard "<project>\docs\video\storyboard.json" --output "<project>\docs\bootcamp_recap.mp4" --project-root "<project>"`

⛔ **(INV-340) This guidance is a statement, never a question, and it never blocks graduation.**
It changes nothing about Step 1c's outcome: the video was produced, and graduation continues to
Step 2.

## Step 2: Build the production project

If `production/` already exists, pin this 👉 question verbatim (neutral lead + numbered list):

👉 **`production/` already exists — how should I proceed? Reply with a number:**

1. **Overwrite** — replace the existing `production/` contents.
2. **Merge** — keep existing files and add or update the generated ones.
3. **Abort** — leave `production/` untouched and write the graduation report to `docs/` instead.

Wait for the answer. On abort, skip to the graduation report noting the abort.

**Handling each answer (INV-284).**

- **1, "Overwrite":** replace the existing contents by the copy below, then Step 3.
- **2, "Merge":** keep the existing files and add or update them by the copy below, then Step 3.
- **3, "Abort":** leave `production/` untouched and skip to Step 5, the graduation report, noting
  the abort. Nothing under `production/` is written or normalized after an Abort: Step 5 writes
  the report to `docs/GRADUATION_REPORT.md`, and Step 5a is skipped.

Create `production/` and copy production-relevant files (skip any source that
does not exist; on a copy failure, log and continue):

| Source | Destination | Notes |
|--------|-------------|-------|
| `src/transform/**` | `production/src/transform/` | Mapping/transform code |
| `src/load/**` | `production/src/load/` | Loading code |
| `src/query/**` | `production/src/query/` | Query/discovery code |
| `src/utils/**` | `production/src/utils/` | Shared helpers |
| `data/senzing-ready/**` | `production/data/senzing-ready/` | Senzing-ready data |
| `data/exports/**` | `production/data/exports/` | Module 7 step 4e's exports for the named systems |
| `config/data_sources.yaml` | `production/config/data_sources.yaml` | Data-source registry, written as a projection (below), not copied whole |
| `requirements.txt` / `pom.xml` / `Cargo.toml` / `package.json` / `*.csproj` | `production/` | Root dependency manifest. Only Python's `requirements.txt` sits at the root: C#, Rust and TypeScript manifests travel inside their program folders, which the `src/**` rows copy unchanged |
| `nuget.config` | `production/nuget.config` | C#'s project-local package source (SDK setup), so the copied programs restore `Senzing.Sdk` as they did here |

**The `src/**` rows copy source, never build output.** Skip every `classes/`, `target/`, `dist/`,
`node_modules/`, `bin/` and `obj/` folder under them, wherever it sits: those are what the build
and init commands in `../bootcamp-onboarding/ground-rules.md` → "Building and running a program"
write (Java's `<dir>/classes`, Rust's shared `<dir>/target`, TypeScript's `<dir>/<name>/dist` and
`node_modules/`, C#'s `bin/` and `obj/`). Each program folder keeps its manifest and source, and the
copied project rebuilds them from `production/` with that section's commands.

⛔ **Every destination above keeps the source's path relative to the project root, and
`data/senzing-ready/` and `data/exports/` in particular.** (INV-186) The code in `src/load/**` is copied **verbatim** and reads its
input from `data/senzing-ready/` (INV-084 — `../module-06-data-processing/phaseA-build-loading.md`
step "Mapped sources"), so flattening the data to `production/data/` hands the bootcamper a project
whose loader points at a directory that does not exist. Copy the tree, do not rewrite the code: the
loader is theirs, and a path edited by graduation is a change they never saw made.
`data/exports/` is the same rule in the other direction: the `src/query/**` row above carries
Module 7 step 4e's export program unchanged (`../module-07-query-visualize-discover/phase2b-discover.md`,
step 4e item 8), and that program **writes** to `data/exports/<system>/`, so its output tree has to
arrive at the same project-relative path or the copied program writes where nothing expects it.

⛔ **(INV-186) `config/data_sources.yaml` is written to `production/config/data_sources.yaml` as a
projection, never copied whole, and never left out.** The multi-source orchestrator in `src/load/**`
reads each source's registry entry when it runs (`../module-06-data-processing/phaseC-multi-source.md`
step 17, INV-320), so without the registry at that path the copied loader stops at its first lookup.
The projection describes what production loads, not what the evaluation loaded:

- **Keep only:** `version`, the `sources:` mapping with its keys as the registry has them, and per
  source `name`, `file_path` and `format`.
- **Strip:** every other field, including `load_subset:`, `sample:`, `quality_score`,
  `quality_intent`, `provenance`, `validation_status`, `validation_checks`, `mapping_status`,
  `load_status`, `record_count`, `expected_record_count`, `truncated` (as
  [the truncated-source rule](../module-04-data-collection/SKILL.md#truncated-cord-source) defines), `file_size_bytes` and the timestamps.
- **Sources:** every source whose `file_path` is non-null, fast-pathed sources included (their
  `data/raw/` input is disclosed as the paragraph on fast-pathed sources below says). Omit a source
  whose `file_path` is null, such as a documented-location-only source. Omit a source whose
  `mapping_status` is `skipped` too: it has no mapper, so production has nothing to load it with,
  and Step 4's README names it (INV-363; [what `skipped` means](../module-04-data-collection/SKILL.md#mapping-status-values)).
- **Why `load_subset:` goes:** it is the evaluation's limit. An `overlap_preserving` block names a
  subset file under the excluded `data/subsets/` (below), and a `first_n` block's `limit` is the
  evaluation's license or SQLite cap. A source with no block loads its whole registry `file_path`
  (step 17), which is what production loads. `sample:` goes for the same reason: its file is under
  the excluded `data/samples/`.
- **Merge** regenerates the projection, as it does every generated file. A missing registry is
  skipped like any other missing source; a write failure is logged and the step continues.

Create `production/database/.gitkeep` as an empty placeholder (never copy the
eval database itself).

**Exclude (never copy):** `config/bootcamp_progress.json`,
`config/bootcamp_preferences.yaml`, `docs/bootcamp_recap.md`, `docs/bootcamp_notes.md`,
`data/samples/`, `data/raw/`, `data/subsets/`, `data/backups/`, `logs/`, `backups/`, and
`docs/feedback/`.

`data/subsets/` is excluded because a subset is the evaluation's license-capped or volume-capped
slice (Module 6), not the data production loads. `data/backups/` is excluded because it holds
Module 6's pre-load copies of the evaluation repository, which production does not restore.

⛔ **`docs/bootcamp_notes.md` is a bootcamp artifact, not production content** — exactly as
`docs/bootcamp_recap.md` and `docs/feedback/` are. It holds the bootcamper's own ideas and
reminders about learning the tool; it has no place in a project they hand to their team.

⛔ **`data/raw/` is excluded, so a CORD fast-pathed source's input is not carried over.** A
fast-pathed source loads straight from `data/raw/` with no mapping (INV-040/INV-041), so its loader
arrives in `production/` with no input file — deliberately, since raw source data is the
bootcamper's to place, not graduation's to copy. Name each such source in the Step 5 graduation
report's **files-excluded** table and in `production/README.md` → Configuration, saying where its
input has to be supplied (INV-187). An excluded input the handover never mentions is indistinguishable from a
broken project.

<a id="mapped-source-raw-input"></a>
**A mapped source's raw input is not carried over either.** Each mapped source's `transform_[name]`
arrives in `production/src/transform/` and takes the file it transforms as a run argument
(`../module-05-data-quality-mapping/phase2-data-mapping.md` step 13), and that file is the source's
file in the excluded `data/raw/`, as the source's lineage document,
`docs/mapping/transformation_lineage_[name].md`, names it. Name each such source in the Step 5
graduation report's **files-excluded** table and in `production/README.md` → Configuration, saying
that the reader supplies that input as the transform's argument (INV-187). A source Module 5
fast-pathed has no transform, so the paragraph above is its only disclosure; a `skipped` source has
no transform either, and gets no line.

<a id="scan-the-copied-code"></a>
**(INV-401) Scan the copied code for paths this step left behind.** Generated programs never read such a
path at runtime ([the rule](../module-06-data-processing/phaseA-build-loading.md#no-runtime-reads-of-uncopied-paths)),
and this scan names any read that slipped through. After the copy, on Overwrite and Merge alike,
run the bundled scanner from the project root:

```bash
python3 "{{host.scripts_dir}}/scan_uncopied_paths.py"
# or, if {{host.plugin_root_var}} is unset: python3 {{host.scripts_fallback}}/scan_uncopied_paths.py
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

It searches the text of every file under `production/src/`, in any language, for a
project-relative path that exists in the project but not in `production/`, which is everything
above leaves behind, and prints one `<file>: <path>` line per hit. **Each line becomes one `- [ ]`
item in the Data section of Step 4's `production/MIGRATION_CHECKLIST.md`**, naming the file and the
path it reads, and saying that `production/` has no such path, so the program needs it supplied or
rewritten to take it from the environment. No line, no item. A text search cannot tell a read from
a write or a comment, so the item says the file names the path and leaves the Bootcamper to check
which. If the scanner cannot run, log it, add no item, and continue: the scan only adds items.

Present a short, one-line statement of what was copied, what was excluded, and the directories
created, then continue directly to Step 3 — generate the production configuration files
automatically. Do not gate this behind a 👉 question (one fewer low-stakes confirmation).

## Step 3: Production configuration files

Generate these in `production/`, parameterized by `programming_language` and `database_type` from
pre-checks. Use placeholder values only, never real secrets:

- **`.env.example`:** `SENZING_ENGINE_CONFIGURATION_JSON`, `DATABASE_URL`,
  `LOG_LEVEL` with safe example values and comments. ⛔ **(INV-208) The license goes in the engine
  config's `PIPELINE` section, inside the `SENZING_ENGINE_CONFIGURATION_JSON` value —
  `LICENSESTRINGBASE64` (an inline Base64 key, preferred) or `LICENSEFILE` (the path to an
  existing `.lic`) — matching Data collection's wiring; show both as a comment there.** That is the route
  `sdk_guide(topic='load', language=…, record_count=<above the default limit>)` names in its
  `compatibility_notes` (INV-080). Add no license environment variable to the key list, and never
  `SENZING_LICENSE_PATH` — a confabulation that shipped here for a time and no MCP tool
  returns. This file is one the bootcamper carries into production, where an unread variable
  licenses nothing and fails as a capacity error far from its cause.
- **`docker-compose.yml`:** SQLite (single service + volume mount) or PostgreSQL (app + db service with a health check), per `database_type`.

**Where `deployment_target`/`cloud_provider` is known, say so in both files** (INV-097): a header
comment naming the intended target — e.g. `# Target: AWS (ECS/Fargate)`, `# Target: Kubernetes`,
`# Target: on-premises`, or for a generic value `# Target: ` and its
[pre-check 1a rendering](#generic-deployment-target) — and, in `.env.example`, a comment on the
values that platform will supply differently (a managed-database `DATABASE_URL`, a secret-manager
reference instead of a literal).
⛔ Stay declarative: name the target and stop. Do **not** invent provider-specific resources,
credentials, ARNs, or account identifiers — placeholder values only, as above, and a wrong
infrastructure guess in a handed-over project is worse than a generic one. When the value is absent
the files are exactly as they were before this paragraph.

- **`.gitignore`:** language-appropriate, always including `.env`, `.env.production`, `*.db`, `*.sqlite`, `__pycache__/`, `node_modules/`, `target/`, `classes/`, `bin/`, `obj/`, `build/`, `dist/`, `*.log`.

## Step 4: Production README and migration checklist

- **`production/README.md`:** parameterized by `programming_language`, `database_type`, and the data sources from `config/data_sources.yaml`. Use no bootcamp language (no "bootcamp", "module", "track", or "bootcamper"). Sections: Project Overview, Prerequisites, Installation, Configuration, Usage, Project Structure. Show it to the bootcamper and apply any requested revisions.
  - **Usage gives each copied program's build and run commands.** One entry per program under
    `production/src/`, with its build and run commands as `../bootcamp-onboarding/ground-rules.md` →
    "Building and running a program" gives them for `programming_language`, with that program's
    `<dir>` and `<name>`, run from `production/`, where every program keeps its project-relative
    path. For Java, say that the run needs the Senzing SDK jar and `<dir>/classes` on the classpath:
    the launcher `../module-02-sdk-setup/SKILL.md` → "The launch environment" sets up is not copied.
  - **Configuration names the registry.** Say that `config/data_sources.yaml` is the registry the
    loader reads, holding each source's `file_path` and `format` (the Step 2 projection). Then name
    each source the evaluation loaded as a subset (one whose bootcamp registry entry has a
    `load_subset:` block), and say that production loads its whole `file_path`. No source was loaded
    as a subset → omit that sentence.
  - **Configuration names each source that is not mapped.** (INV-363) For each source whose bootcamp registry
    entry has `mapping_status: skipped`, which Step 2's projection leaves out
    ([what `skipped` means](../module-04-data-collection/SKILL.md#mapping-status-values)), say that it is not mapped, so
    the registry does not list it and the loader does not load it, and that its mapping was stopped
    after the mapping validator rejected it without a usable reason. No such source → omit that
    sentence.
  - **Configuration names each transform's raw input.** (INV-187) For each mapped source, name its
    file in `data/raw/` as the input the reader supplies as `transform_[name]`'s input argument, as
    Step 2's [mapped-source paragraph](#mapped-source-raw-input) says. No mapped source → omit that
    sentence.
  - **Where `integration_targets` is known** (INV-097), name those systems in **Project Overview** as what the resolved entities are meant to feed, and in **Configuration** as the integration points a reader will need to wire up — the resolved data exists to reach them, so a README that never mentions them describes half the job. Absent → omit; never write "none" or a placeholder.
- **`production/MIGRATION_CHECKLIST.md`:** `- [ ]` checkboxes under six sections (Database, Security, Licensing, Performance, Data, Deployment). Because the bootcamp does not include dedicated performance/security/monitoring/deployment modules, add a note at the top: "⚠️ Some production topics (performance, security, monitoring, deployment) are not covered in depth during the bootcamp: complete these items before deploying," and mark those items with ⚠️.
  - **(INV-421) The Database section MUST carry the production-database item** — ⚠️ *"SQLite is an
    evaluation and starter database: before deploying, move to a supported production database.
    Senzing's documentation recommends PostgreSQL for anything beyond evaluation. If
    `docker-compose.yml` or `.env.example` points at SQLite, this starter is not ready to deploy
    unchanged."*
    Ship it whatever `database_type` is: a PostgreSQL project confirms it and ticks the box. It
    asks for a migration the team carries out; graduation changes no template and migrates no
    data. Do **not** say SQLite cannot run in production: the documentation's wording is a
    recommendation, *"For anything beyond evaluation, use PostgreSQL"*, from the SQLite
    performance answer that `search_docs(query='SQLite evaluation PostgreSQL production database
    recommendation')` ranks first.
  - **The Performance section MUST carry the DEFAULT-flags item** — ⚠️ *"Replace `*_DEFAULT_FLAGS`
    composites in `production/src/`, **including the export call**, with the explicit `SZ_*` flags
    whose output your code actually consumes. On the export call a replacement can drop output
    with no error: hand-assembling `SZ_ENTITY_INCLUDE_*` members has been observed to drop
    `RELATED_ENTITIES` entirely. Before you adopt a replacement there, export with it and confirm
    that every field and relationship your code reads is still present. Until you have, keep the
    current flags and leave this item unchecked."*
    ⛔ **(INV-287) Ship the exception with the item, never the item alone.** Here the exception
    is a qualification, not an exemption. The bare instruction points at the one call where
    following it blindly silently loses every relationship (`../module-06-data-processing/phaseD-validation.md`), and a checklist a
    Bootcamper works through unattended is exactly where an unqualified rule does that damage.
    The export call is not exempt: `SZ_EXPORT_DEFAULT_FLAGS` is itself a composite whose members
    include `SZ_ENTITY_DEFAULT_FLAGS` (`get_sdk_reference(topic='flags',
    filter='SZ_EXPORT_DEFAULT_FLAGS')`, MCP server 1.46.0, 2026-11-10), so the caution below
    covers it as much as any other call. Name no explicit export flag set in the item: none has
    been verified to carry everything a given project consumes, so the item asks the team to
    verify their own.
    Give the reason, because it is what makes the item non-obvious: the server states
    that DEFAULT composites are for getting started and exploration rather than production, that
    their **membership may change between Senzing versions**, and that pinned code can therefore
    *"silently change what it returns after an upgrade — no error is raised"*; they also over-fetch,
    costing engine work and response size (`get_sdk_reference(topic='flags', …)` top-level
    `caution`, MCP server 1.32.9, 2026-08-12; re-confirmed word for word on 1.46.0, 2026-11-10).
    This matters here specifically because `src/query/**` is copied into `production/src/`
    verbatim, so the bootcamp's exploration-shaped flag choice becomes their shipped code. The bootcamp is right to teach the composites
    (`../module-07-query-visualize-discover/phase1-query-visualize.md` relays the same caution) —
    this checklist is where the production correction belongs.
  - **The Data section carries Step 2's scan items**, one per line [the scan](#scan-the-copied-code) printed.
  - **The Deployment section is where `deployment_target`/`cloud_provider` lands** (INV-097): name the stated target in its heading or first item, and make its checkboxes the ones that target actually needs (a cloud target → managed database, secret storage, image registry, network egress to nothing external; Kubernetes → manifests/Helm, resource limits, liveness probes; on-premises → host provisioning, backup schedule). ⛔ Still ⚠️-marked and still not covered in depth by the bootcamp — naming the target makes the list *relevant*, not authoritative, and it must not read as a deployment guide the bootcamp did not give. Absent → the generic six-section list exactly as before.
    - **A generic value** is named by its [pre-check 1a rendering](#generic-deployment-target)
      and takes its category's checkboxes: `cloud` the cloud list, `container` a container list
      naming no orchestrator-specific tooling (image build and registry, resource limits, health
      checks), `local` the on-premises list.

Write every `production/*.md` deliverable — this README, the migration checklist, and the
Step 5 `GRADUATION_REPORT.md` — as **plain, functional Markdown**, exactly as the bootcamp's own
docs were written (`../bootcamp-onboarding/ground-rules.md` → "Markdown files"). Do **not**
hand-format them to the house rules: **Step 5a runs the normalizer over `production/`** and does it
in code, with a content guard. Structure still matters and is not deferred — the sections listed
above, the `- [ ]` checkboxes, and the tables are content, not formatting.

## Step 5: Graduation report

Always generate `production/GRADUATION_REPORT.md`, even if earlier steps had
errors, except after Step 2's Abort, when it goes to `docs/GRADUATION_REPORT.md` instead.

**After an Abort.** Step 2 promised to leave `production/` untouched, so write the report to
`docs/GRADUATION_REPORT.md`, record the abort in it, and skip Step 5a. Leave an earlier
`production/GRADUATION_REPORT.md` as it is. Step 1a's pass over `docs/*.md` has already run and
Step 5a does not run, so hand-format this report to the house rules as Step 6c's
`docs/REVISIT_BOOTCAMP.md` is (MD022/MD031/MD032 blank lines, MD040 fenced-block languages,
`**Label:**` colon spacing). Its files-generated table lists only what this run wrote.

Include: completion timestamp, bootcamp path (Core/Customized) and the modules completed,
`programming_language`, `database_type`, a files-generated table (it lists
`production/config/data_sources.yaml`, the Step 2 registry projection, with the other generated
files), a files-excluded table, and
next steps (fill in secrets, obtain a production license, work through the
checklist, configure CI/CD, test with production data). Record the Module 1 answers too when
present — the intended `deployment_target`/`cloud_provider` and the `integration_targets`
(INV-097) — so the handover states what the project was aimed at; omit either line when absent.
Record the value as stored; for a generic value, add its
[pre-check 1a rendering](#generic-deployment-target), which says the platform was not stated.
If any step failed, add a
"⚠️ Issues Encountered" section naming what failed and what was skipped.

## Step 5a: Normalize the production Markdown (once, after the files exist)

**Skip this step after Step 2's Abort.** Nothing under `production/` was written, and Step 5 put
the report in `docs/`, so there is nothing here to normalize and `production/` stays untouched.

`production/` now holds its Markdown deliverables, written plain. Make the same single
best-effort CommonMark pass over them that Step 1a made over `docs/*.md` — INV-060 requires the
pass over **both** sets, and the `production/` half is why this step exists:

```bash
python3 "{{host.scripts_dir}}/normalize_docs_markdown.py" --docs-dir production
# or, if {{host.plugin_root_var}} is unset: python3 {{host.scripts_fallback}}/normalize_docs_markdown.py --docs-dir production
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

It applies the same rules as in Step 1a and globs top-level `production/*.md` only, never
recursing — so nothing under `production/src/`, `production/config/` or a copied `docs/` subtree is
touched.

⛔ **Same content guard, same non-blocking contract as Step 1a.** The normalizer fingerprints each
file's non-whitespace content before and after and **restores the original** if any source line
would be lost, so a cosmetic pass can never silently shorten a handover document. If it reports a
file left as written, that is a normalizer bug — say so and continue with the file unformatted;
never hand-edit prose to make formatting pass. If the script fails or is unavailable, warn, leave
the content as written, and continue.

⛔ **Run it after Step 5, not before.** `production/` does not exist at Step 1a and its Markdown is
not finished until `GRADUATION_REPORT.md` is written, so an earlier pass would normalize nothing —
which is precisely how this half of INV-060 went unbuilt from 2026-07-16 to 2026-07-29.

`docs/REVISIT_BOOTCAMP.md` is written later still (Step 6c) and so is covered by **neither** pass;
Step 6c states its own formatting rule.

## Step 5b: Render the two keepsake documents as styled PDFs

The bootcamp already treats "rendered as a styled PDF" as the signal that a document is a
keepsake rather than a working file. Two more qualify, and the renderer that makes them is
already bundled:

- **`docs/business_problem.md`** — the document a stakeholder is most likely to be shown.
- **`docs/data_source_evaluation.md`** — the engine-verified readiness findings and the
  unmapped-field audit with its rejected-field rationale; the reference a team returns to when
  someone asks "why wasn't field X mapped?".

Render each with the bundled general renderer, resolved the same way as every other bundled
script and never as a bare `scripts/…` path (INV-185):

```bash
python3 "{{host.scripts_dir}}/generate_document_pdf.py" \
    --input docs/business_problem.md --output docs/business_problem.pdf \
    --require-sections "<this document's own H2 headings, semicolon-separated>" \
    --subtitle "The problem this bootcamp set out to solve"
# or, if {{host.plugin_root_var}} is unset: python3 {{host.scripts_fallback}}/generate_document_pdf.py …
```

Guide-run; unverified on Windows: no test runs it there ([guide-run blocks](../bootcamp-onboarding/ground-rules.md#guide-run-blocks)).

⛔ **Pass `--subtitle`.** The cover's subtitle defaults to the discoveries line, "What Senzing
found in your data" — true of the discoveries document and wrong on either of these. It is the
one part of the layout engine that is not document-agnostic, and it is the first thing a
stakeholder reads. For `data_source_evaluation.md`, something like "How ready your sources were,
and what was left unmapped".

⛔ **Read each document's actual H2 headings and pass those.** Bootcampers word these documents
differently, so there is no fixed list to hard-code — which is the whole reason the renderer took
a `--require-sections` parameter instead of a constant. Omitting the flag applies the *discoveries*
defaults and the document is refused; `--no-section-check` is the fallback when a document has no
stable headings, and it is weaker, because the section check is what catches a document that
silently lost its structure.

⚠️ **Neither flag relaxes the content-retention floor** (INV-110). If a render is refused for
retention rather than sections, the document genuinely would not survive the pass — say so and
leave it unrendered rather than reaching for `--no-section-check`.

⛔ **Verify each PDF, do not trust the `PDF generated:` line** (INV-129). Two positive probes per
file, both required:

1. **Extract text from the written file** and confirm real content appears — fpdf2 compresses its
   content streams, so decompress before searching, or a raw byte search reports a false negative.
2. **Count pages** (`/Type /Page` objects, or `pdfinfo` where poppler exists — which on macOS and
   Windows it usually does not; see Step 1b). At least one, and a one-page PDF from a multi-section
   document is a signal to look at the text probe again rather than to pass it.

A zero exit and a plausibly-sized file are both necessary and neither is sufficient.

**Non-blocking, like every graduation step**: if a document is absent, refused, or fails
verification, warn on stderr, say which PDF was not produced, and continue. Name the ones that
succeeded in the closing summary alongside the recap PDF; never turn a failure into a 👉 question
or a to-do for the bootcamper.

Character handling is unchanged from the discoveries path — the renderer reports any character it
had to drop (INV-143/INV-159). This step must not become a route that bypasses that report: if it
names dropped characters, repeat them in the warning rather than only in the PDF.

⚠️ **One exception, and it needs no action: the generated-scenario marker's ROBOT FACE.** When
`docs/business_problem.md` carries `> 🤖 Bootcamp-generated business case` — Module 1 Step 11
writes it on every run that accepts the Business Case Offer, which is the common Core path — the
emoji cannot be set in the PDF's Latin-1 core fonts and is dropped from that line. **That loss is
expected and harmless.** The marker is a machine-readable flag for the plugin's own branches
(Module 4, Module 6 Phase C and Module 6 Phase D), every one of which reads it from
the **Markdown**; nothing reads it from the PDF. So do not substitute a name, do not add an ASCII
description, and above all do not edit the marker out of the Markdown to quiet the renderer —
several shipped files and the recap renderer match that exact string, and changing it breaks them
silently.

⛔ **This exemption is the marker line and nothing else (INV-266).** The renderer suppresses only the tally
entry whose passage *is* that line; a ROBOT FACE anywhere else in the document, and every other
unrenderable character, still warns and still needs the warning's own guidance. If the warning
names a dropped character and you cannot place it on the marker line, treat it as a real finding.

## Step 6: Save the revisit/resume bundle

Silently preserve everything a returning bootcamper needs to pick the bootcamp back up — so
"graduated" becomes a genuine save point. Like every graduation step this is **non-blocking**
(warn-and-continue on any failure) and administrative in spirit (no narration beyond a short
closing summary). The bundle lives **outside `production/`**, under the reserved top-level
`backups/revisit/` directory, so Step 2's "never copy the eval database into `production/`" rule
is preserved (INV-094).

If `backups/revisit/` already exists from a prior graduation, pin this 👉 question verbatim before
overwriting it (neutral lead + numbered list, INV-051/INV-056); otherwise create it silently:

👉 **A revisit bundle already exists — how should I proceed? Reply with a number:**

1. **Overwrite** — replace the previous revisit bundle.
2. **Keep** — leave the existing bundle untouched and skip this step.

**Handling each answer (INV-284).**

- **1, "Overwrite":** run 6a–6c into `backups/revisit/`, then Step 7.
- **2, "Keep":** leave the bundle untouched, skip 6a–6c, and continue to Step 7.

### 6a. Database backup

⛔ **Follow `database-backup.md` — it is the one implementation of this procedure, and behavior here
is unchanged by the factoring.** It carries the `database_type` lookup, the do-not-guess rule for an
indeterminate value, both engine branches, the warn-and-continue rule, and the restore commands Step
6c records in the return guide. INV-094 requires exactly one of its two branches to have run.

The second caller is `../bootcamp-onboarding/packaging.md`: the `transfer` package profile needs a
database backup, and when `backups/revisit/` does not exist yet it runs **that same file's**
procedure rather than growing a second SQLite-vs-PostgreSQL branch.

### 6b. RESUME_STATE manifest

Snapshot the resume-critical state into `backups/revisit/state/` (copy each if it exists):
`config/bootcamp_progress.json`, `config/bootcamp_preferences.yaml`, `config/data_sources.yaml`,
`config/engine_config.json`, and `docs/mapping/`. Then write
`backups/revisit/RESUME_STATE.json` — a manifest indexing what was saved: the bootcamp path and
`modules_completed`, `programming_language` and `database_type` (the pre-check key names), the
business problem and data
sources, the relative path of each snapshotted file, the database backup path and its restore
command, the recap PDF (`docs/bootcamp_recap.pdf`), and any visualization snapshots under
`docs/visualizations/`. Use only project-relative paths.

Do not snapshot `config/license.json`. It is the SDK's `get_license` response, measured from the
license installed on the machine, so a copy restores nothing a resumed bootcamp needs, and it
names the license's customer, contract and billing terms. Record it in `RESUME_STATE.json` as
regenerated on restore, never as a snapshotted path, with the key
`"regenerated_on_restore": [{"path": "config/license.json", "by": "Module 4 Step 8a sub-step 7"}]`.

### 6c. Return guide

Write `docs/REVISIT_BOOTCAMP.md` (Markdown under `docs/`, per INV-017). ⛔ **This is the one
deliverable you always hand-format** to the house rules (MD022/MD031/MD032 blank lines, MD040 fenced-block
languages, `**Label:**` colon spacing): it is written *after* both normalization passes — Step 1a's
over `docs/*.md` and Step 5a's over `production/*.md` — so no pass will reach it. Re-running Step 1a
here is deliberately **not** the answer: it would re-touch `docs/bootcamp_recap.md`, which the recap
PDF was already rendered from in Step 1b, leaving the keepsake and its source subtly out of step.
(After Step 2's Abort, Step 5's `docs/GRADUATION_REPORT.md` is hand-formatted too, for the same
reason.) Cover:

- **Quick start when you return** — a short command list at the very top (re-source the env, restore
  the database, re-init the engine, re-run a query and the visualization).
- **What you accomplished** — per completed module, drawn from the recap.
- **Decisions you made** and **How you got it built** — the two lists from Step 0b, exactly as
  Step 1a folded them into the recap's handover block. A list with no entries is left out here
  too.
- **Your takeaway** — the one line from Step 0b, in the Bootcamper's words, as Step 1a folded it.
  A passed takeaway is left out, never written as "N/A".
- **Next time** — the request from Step 0b, in the Bootcamper's words, or labeled as the guide's
  draft when it is one: the place to start when they come back with a new source, with no script.
- **Your business problem and data sources** — from `docs/business_problem.md` /
  `config/data_sources.yaml`.
- **Restore the database** — the exact SQLite copy-back or PostgreSQL `pg_restore -d` / `psql -f`
  command recorded in Step 6a, as `database-backup.md` → "Restore" writes it: never a `<` or `>`
  redirection, which Windows PowerShell 5.1 rejects or re-encodes.
- **Re-initialize and re-run** — how to re-run the project env script created in Module 2
  (`source src/scripts/senzing-env.sh` on Linux/macOS, `. .\src\scripts\senzing-env.ps1` on Windows,
  dot-sourced in the PowerShell window that runs the programs; the Windows form is unverified on
  Windows PowerShell 5.1 here, INV-163) and re-init the engine, then re-run the loader, queries, and
  visualization.
- **License** — where the license lives, as Data collection Step 8a sub-step 5 wired it: a Base64
  key inline in `config/engine_config.json` (`LICENSESTRINGBASE64`), a `.lic` file at
  `licenses/g2.lic` (`LICENSEFILE`), else the built-in evaluation license; and any expiry. On
  return, re-measure the license by Module 4 Step 8a sub-step 7, which re-creates
  `config/license.json` from the license installed on that machine; the bundle does not carry it.
- **Where things are** — point at `backups/revisit/` (state + database backup), the recap PDF, and
  `docs/visualizations/`. Name `data/exports/` too when Module 7 step 4e exported for a system, and
  say that `production/data/exports/` holds the same tree, since the copied export program writes
  there (INV-186). Name `docs/bootcamp_recap.mp4` too when Step 1c produced it (INV-340). When Step 1c
  wrote a storyboard but skipped the video, say that `docs/video/storyboard.json` is kept so the
  video can be rendered later with the bundled renderer, `generate_recap_video.py`.

Then present a one-line summary of what the bundle saved and where, and continue to Step 7.

## Step 7: Feedback reminder

If `docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md` exists and contains at
least one real feedback entry, remind the bootcamper it is there, as statements:

- name its path, `docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md`;
- say the file stays on this machine, and that moving it anywhere is their own action, as
  `../bootcamp-onboarding/packaging.md` says of the archive (INV-135);
- say that any MCP-server finding in it was already offered upstream through
  `../bootcamp-onboarding/feedback.md` → "Step 3c: Offer to forward an MCP-server issue upstream",
  the only upstream path (INV-249).

This step makes no offer and asks no question. An entry still reading `offer pending` here gets no
offer either: Step 0's batch replaces every such value in its own turn (INV-281), so a leftover one
means that batch did not run, and the entry stays on this machine as it is. If they ask you to send
a `plugin`, `host` or `unclear` entry somewhere, it stays on this machine too: name the path so
they can move it themselves.

Otherwise, add one line: "Say \"bootcamp feedback\" anytime if you'd like to share your experience."

## Mandatory closing step: guaranteed recap and announcement

This runs exactly once, after the report, before graduation is reported finished.

1. **Guarantee the recap PDF exists.** Confirm `docs/bootcamp_recap.pdf` exists and is non-empty. If it is missing, re-run Step 1b (or the inline fallback) once so a valid PDF exists before you announce it. Never announce an artifact you have not confirmed exists at its path.
2. **Emit one closing announcement** naming only the artifacts confirmed to exist. State that the recap PDF at `docs/bootcamp_recap.pdf` opens with a summary page and then walks through every completed module, capturing that module's Information Shared, Questions & Responses, Actions Taken, and End-of-Module Summary, and that the source lives at `docs/bootcamp_recap.md`. Name the `production/` project and its `GRADUATION_REPORT.md` and `MIGRATION_CHECKLIST.md`; after Step 2's Abort, name `docs/GRADUATION_REPORT.md` instead and none of `production/`'s files, since this run wrote none. Frame the PDF as a keepsake to revisit and share with their team.

   **Add exactly one line** offering `{{host.invoke_package_bootcamp}}`, which gathers the recap, the keepsake
   documents, the visualizations and `production/` into a single zip under `backups/packages/` they
   can archive, move to another machine, or hand to a colleague.

   ⛔ **That line is a statement, not a question, and it names no output path (INV-251).** No new 👉
   gate belongs here — the single closing question is untouched — and graduation does **not** run the
   packager, so there is no archive yet whose path could be named. (`tests/test_graduation_announces_what_it_produces.py`
   requires a path to be announced when a graduation bash block writes one; this design deliberately
   writes none.)

   **State that from here there is no script, and repeat the "Next time" request.** Close the
   announcement with both, as statements: that from here there is no script, and that they direct
   an AI assistant with the Senzing MCP server themselves; then the request Step 0b recorded,
   quoted as recorded, saying it is the guide's draft when it is one.

   ⛔ **(INV-251) Neither sentence is a question, and neither adds a 👉.** The turn still ends on
   the unchanged closing question in item 3. When Step 0b recorded no request, state only that
   there is no script.

   **Also name the two keepsake documents Step 5b rendered — each only if it exists:**
   `docs/business_problem.pdf` (the problem this bootcamp set out to solve — the document a
   stakeholder is most likely to be shown) and `docs/data_source_evaluation.pdf` (how ready each
   source was and what was left unmapped — the reference for "why wasn't field X mapped?"). Step 5b
   is **non-blocking**, so either can legitimately be absent: an absent or refused PDF is simply not
   named, by item 1's rule that you never announce an artifact you have not confirmed exists. This
   step is the **only** place these two reach the bootcamper — graduation is terminal, so a PDF
   unnamed here is one they never learn they have.

   **(INV-340) Also name the graduation video, `docs/bootcamp_recap.mp4`, only if Step 1c produced it:** a
   2-minute video of their bootcamp, to keep and share. When its duration stayed outside the
   renderer's tolerance (Step 1c, "Verify the video") after the one re-render, say so here, with its
   duration. When a video check did not run, say which, in the same plain sentence as the PDF note
   below (INV-163).

   ⛔ **(INV-340) Call the video narrated only when the renderer's `Voice:` line named an engine.**
   With `Voice: none (…)`, call it a 2-minute graduation video "with captions and music, no voice",
   or "with captions, no voice" when the renderer printed `Music: off (storyboard)`. The same
   sentence then carries, once, what Step 1c's "When the video has no voice" gives for its case:
   for `no speech engine found`, the platform's speech engine, its install hint and the re-render
   command; for `<engine> voiced no scene`, the engine that could not voice the narration, with no
   install hint; for `--no-voice`, nothing more. It is a statement, not a question (INV-340).

   **If any Step 1b verification check was skipped for a missing tool, say so here in one plain sentence** — name what was not checked, not the tool names. On Windows this is the common case (poppler is typically absent, so the page raster could not run). One sentence is enough: *"One note: I verified the PDF's contents but couldn't check its page layout on this machine, so if anything looks visually off, tell me and I'll re-render."* Never describe the keepsake as verified when a check did not run — and never turn this into a 👉 question or a to-do for the bootcamper.

Example (list only what exists):

> 🎓 **Here's your bootcamp recap.** Your complete recap is at `docs/bootcamp_recap.pdf`: a shareable PDF that opens with a summary and then walks through every module you completed, capturing the Information Shared, Questions & Responses, Actions Taken, and End-of-Module Summary for each. Your production project is ready in `production/`: start with `production/GRADUATION_REPORT.md` and work through `production/MIGRATION_CHECKLIST.md`. Two more keepsakes are alongside the recap: `docs/business_problem.pdf`, the problem you set out to solve, and `docs/data_source_evaluation.pdf`, how ready your sources were and what was left unmapped. And your narrated 2-minute graduation video is at `docs/bootcamp_recap.mp4`. From here there is no script: you direct an AI assistant with the Senzing MCP server yourself. Next time, start with your own request: "Help me map and load our vendor master file into Senzing and find the vendors that are also customers."

When the video has no voice because no speech engine was found, its sentence reads like this instead
(Ubuntu, with music; the paths are illustrative):

> And your 2-minute graduation video, with captions and music, no voice, is at `docs/bootcamp_recap.mp4`: no speech engine was found, and on Ubuntu the voice comes from `espeak-ng`, which you can install with `sudo apt install espeak-ng`; then run `'/home/ada/projects/my-bootcamp/data/temp/recap-venv/bin/python' '/opt/plugins/senzing-bootcamp/scripts/generate_recap_video.py' --storyboard '/home/ada/projects/my-bootcamp/docs/video/storyboard.json' --output '/home/ada/projects/my-bootcamp/docs/bootcamp_recap.mp4' --project-root '/home/ada/projects/my-bootcamp'` to render it again with a voice.

3. **End on the single closing question (INV-251).** The announcement carries no 👉. After it, end the graduation turn with exactly one 👉 question:

> 👉 **Is there anything else you would like to explore?**

Then stop and wait. This is the single closing question for the whole bootcamp.

4. **Terminal banner — only after the bootcamper declines.** Handle the reply to the closing question:

   - **Wants to keep exploring** (asks a question, names a topic, or otherwise continues): help them, then offer the closing question again when they are ready. Do **not** show the terminal banner yet — it must never pre-empt continued exploration.
   - **Declines** ("no", "I'm done", "that's all", "nothing else"): the bootcamp is complete. Do these two things, in order:
     1. **Stand down the closing-question nudge and record completion, silently.** Set a top-level `bootcamp_complete: true` key in `config/bootcamp_preferences.yaml` (a single minimal edit; do not narrate it). In the same step, write `config/bootcamp_progress.json`: set `bootcamp_complete: true`, `completed_at` to the current time in ISO 8601, `current_module: "graduation"` and `current_step: null`, and append `graduation` to `modules_completed` if it is absent, keeping every other key as it is. Make both writes on the normal path and after Step 2's Abort alike. Where a hook runs it, `{{host.scripts_relative}}/stop-nudge.py` reads the flag and will not nudge for a closing 👉 question once the bootcamp is over — so the terminal banner, which ends the turn with no 👉, is not re-opened. Session start and `{{host.invoke_start_bootcamp}}` read either file's flag as a finished bootcamp (`../bootcamp-onboarding/SKILL.md` step 2), so the progress file never presents the last module as current.
     2. **Render the terminal banner, verbatim, exactly once, then the one `{{host.invoke_package_bootcamp}}` line below it, verbatim.** The banner bookends the WELCOME banner that opened the bootcamp (start) and the BOOTCAMP GRADUATION banner (finish) with a clear end-of-bootcamp marker; the line reminds the bootcamper how to keep or share what they built.

     ```text
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     🎓🎓🎓  END OF SENZING BOOTCAMP  🎓🎓🎓
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ```

<!-- host:only claude -->
     Run `{{host.invoke_package_bootcamp}}` anytime to bundle your bootcamp results into one zip you can archive, move to another machine, or share with others.
<!-- host:end -->
<!-- host:except claude -->
     Say {{host.invoke_package_bootcamp}} anytime to bundle your bootcamp results into one zip you can archive, move to another machine, or share with others.
<!-- host:end -->

     That line is the final output. Show it as a plain line right after the banner's fence, never inside it. No 👉 question follows it, and nothing else does; the turn simply ends. It is a statement, not a question, and it names no archive path, because graduation runs no packager and no archive exists yet (INV-251). Show it on the normal path and after Step 2's Abort alike, and under every verbosity preset, including `minimal`, exactly like the banner.

     Show this banner and its line at most **once** per bootcamp, and never while exploration is still continuing.
