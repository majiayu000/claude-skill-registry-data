---
name: semantius-admin
description: >-
  Orchestrates the Semantius pipeline (architect, analyst, modeler) and
  instance administration. Trigger when intent spans more than one skill, on a
  remote blueprint URL, or on "deploy this blueprint", "deploy these
  blueprints", "deploy all of these", "set up these systems", "build me a
  system and deploy it", "set up a CRM end-to-end", "clone the candidate-crm
  blueprint and deploy", "what's deployed in our instance?", "status of
  semantius", "audit this file" (naming no specific skill), "get started",
  "I'm new here, set this up", "turn on fast flow", "expert flow",
  "guided flow", or anything needing workspace artifacts
  inspected and routed to the right sub-skill. Also trigger on a deploy
  request with multiple URLs, paths, or a glob. Do NOT trigger when the user
  invokes one sub-skill directly (not "audit this spec with
  semantius-analyst", not "run the modeler"); let those through. Front door
  for end-to-end and ambiguous requests. Backing up, restoring, or moving
  modules or tables with their data between hosts is semantius-transfer, not
  this skill.
---

# Semantius Admin

## Execution context (mandatory, read before anything else)

**This skill is interactive and MUST run in the conversation the user is in.**

- Do NOT start this skill, or any of its stages, in an agent that another agent started to run on its own (a background worker, subagent, executor, or Task). Those agents cannot ask the user questions, so they cannot run this skill correctly. Running in the cloud is fine when the user is talking to that agent directly.
- Do NOT write a delegation prompt that tells another agent to run this skill, "build and deploy end to end", or "make the decisions yourself".
- If you cannot call a tool that asks the user a question and waits for the answer, STOP at once. Make no writes. Report back: "This skill is interactive and must be run in the user's conversation." Muse chat is the exception: there you ask in chat text and the tap picker, so do not stop; follow the question-format step of the shared preflight. For dot, OpenAI's personal assistant, and other similarly limited tools without a supported interactive question tool, do not stop: read `references/dot-questions.md`, ask questions in chat, and wait for the user's reply before continuing.
- An agent's general habit of delegating long or multi-step work does not apply here. This rule overrides it.

**What may be delegated:** only steps that ask nothing and change nothing the user has not confirmed.

The orchestrator for the three-skill Semantius pipeline plus administrative operations. Sits in front of `semantius-architect`, `semantius-analyst`, and `semantius-modeler`; routes composite operations to the right sequence of sub-skills; handles inspection and other instance-level admin tasks; backup and restore belong to `semantius-transfer`.

## Writing conventions

Every output this skill produces (chat, and the artifacts it writes) follows the shared writing conventions: US English spellings, no em-dashes, singular-subject confirmation prompts ("Looks good?"), no raw identifier leakage in user-facing prose, and plain domain language. They are the canonical set in [`references/writing-conventions.md`](./references/writing-conventions.md) and match the architect, analyst, and modeler so output reads consistently across the pipeline.

---

## Core invariants

A handful of rules govern this skill end-to-end. They are stated ONCE here; the sections below refer back with a short reminder ("single write gate", "copy, never move", "the plan is the task list") instead of re-explaining them.

- **Single write gate / informational plans.** The modeler's own pre-execute yes/no is the ONLY confirmation before a live-model write (in a fast run, the user's go-ahead in the design step takes its place, once for the whole build; [`references/fast-flow.md`](./references/fast-flow.md)). The admin never fires an up-front "Proceed?" gate; every plan it builds is informational (build the task list, then run). Creating tasks is never a pause. This suppresses the deploy *confirmation* only, never the scope *questions* (next rule).
- **Copy, never move.** A pre-existing artifact (especially one at the repo root) is COPIED up front into the convention folder (`semantius/blueprints/` or `semantius/specs/`); that copy becomes the working path and every edit targets it; the root original is read once and never moved, renamed, overwritten, edited, or deleted. The only files the admin relocates are ones it downloaded this run (`.tmp_admin/` into the convention folder). The Step 1.1 "Slug present in BOTH" compare-and-choose procedure and its widget are separate logic, not a restatement of this rule. Staging and copying are internal mechanics: never a task, never narrated.
- **Scope flags before the plan.** `customize` (blueprint), `review` (spec), and `deploy` (both) are resolved (inferred from intent, then asked only where ambiguous, Step 6.4) BEFORE the pipeline tasks are created. The flag questions are question-ledger tasks (`Q:`), and the pipeline tasks may be created only once `TaskList` shows no `Q:` task pending or in progress; that check is the gate. A bare "deploy this" still fires the customize question. Greenfield builds and catalog clones short-circuit: no scope questions, because the architect's Create pass IS the design and `deploy` is implied.
- **Internal mechanics never reach chat.** Preflight, the org probe, file staging, `curl` / `jq` / `yq` plumbing, stage transitions, run-ids, and skill-internal vocabulary go to the per-run diagnostic log, never to chat and never into a task subject. Task descriptions may hold working state (a one-line step summary, the flag values, the verbatim failure message); diagnostic detail stays in the log. The "surface / never-surface" lists, the narration-restraint rules, and the banned-vocabulary list in Output discipline below are the resident expression of this.
- **The plan is the task list.** The admin never renders a numbered plan in chat. It creates one task per plan line (Step 6.5 line shapes as subjects, chained in pipeline order with `blockedBy`) and emits ONE lead-in sentence in chat that names the steps by what they do, cues which step asks questions, and says which step writes to the live model (or that nothing is applied). Never a numbered list, never a code fence. Rules: [`references/task-tracking.md`](./references/task-tracking.md); wording and worked examples: [`references/plan-shapes.md`](./references/plan-shapes.md).
- **Never `WebFetch` for an artifact.** Fetch remote artifacts with `curl -s -L` only; `WebFetch` runs an HTML-to-markdown pass that silently strips YAML front-matter. `WebSearch` and `WebFetch` serve only the architect's and analyst's product lookups (architect SKILL.md, "Reference material").
- **`.tmp_admin/` is scratch and ephemeral.** The run folder persists after the run; the user manages cleanup.

---

## Output discipline (casual-user chat vs. internal diagnostic log)

Everything this skill prints to chat is read by a casual user who does not know the skill's internals. Internal mechanics (preflight guards, org probes, file staging, `yq` writes, stage/step transitions, skill-internal vocabulary) confuse and sometimes alarm them ("why is it talking about halting?"). Keep them out of chat entirely. When that detail is worth keeping for debugging, write it to the per-run diagnostic log instead.

**Surface to chat ONLY:**

- The download milestone: ONE result-shaped line per URL the user named, emitted when the fetch has validated (Step 2 / 6.1): *"Downloaded the Hiring Starter blueprint from semantius.com."* Display name (front-matter `system_name`) and host only; nothing about paths, folders, staging, or validation. It reports what happened, never what is about to happen or what machinery ran. Local sources get no milestone (the user named the file; the first question or the plan lead-in names the design within a step).
- The one-sentence plan lead-in (the plan itself is the task list; see the core invariant above).
- Questions the user must answer (`AskUserQuestion`: scope flags, sub-skill decisions).
- Results the user cares about: what's now live, where produced files landed, and any failure they must act on (with the failing sub-skill's verbatim message). In guided and expert flow this includes the architect's and the analyst's one-line close-outs naming the blueprint and spec files as each is written; only a fast run leaves file names out ([`references/fast-flow.md`](./references/fast-flow.md), 4.1).
- The close-out (Step 8).

**The task list is a sanctioned surface, not chat.** Task subjects follow the same plain-language bar as chat (Writing Convention 8: no internal vocabulary, no stage names, no raw slugs where a display name exists); task descriptions are working memory (flag values, one-line step summaries, verbatim failure messages) and may carry internal keys but never diagnostic detail. Task tool calls need no narration.

**Never surface to chat** (write to `$DIAG_LOG` instead):

- **The fact that any setup is happening at all.** Do not announce that you're running checks, preflight, or setup. **Never write the words "preflight" or "silent" in chat** — they name machinery the user doesn't know exists, and "silent" in particular reads as ominous. Your FIRST words to the user are the download milestone (only when the request named a URL), the first `AskUserQuestion`, or the plan lead-in; the tool-call rows ("Ran N commands") and the task list are the only other trace the setup is allowed to leave. Fetching a URL the user named is the first step of their request, not setup: its *result* gets the one milestone line; the fetch mechanics (`curl`, staging, validation, the copy into the convention folder) stay out of chat.
- Preflight: the org probe, the customizations-path computation, the toolchain (Bun / jq / yq) and CLI install checks. A *successful* tool install gets at most one plain line ("Installing jq..."); only a *firing* halt guard (a required tool could not be installed) produces a halt message.
- Internal transitions: "running preflight", "setting up the per-org customizations path", "assigning run id", phase announcements like "now inspecting the workspace".
- CLI / tool mechanics: command names, `.tmp_admin/` paths, `curl` / `jq` / `yq` invocations, staging locations.
- Skill-internal vocabulary: `customizations.yaml`, `run_id`, decision-path names, sub-skill mode names, raw flag tokens (never *"Inferred: customize=no, deploy=yes"*; the plan lead-in already states the resolved scope in plain words, and 6.4.3 lets the user correct it).
- Pipeline jargon: "reconcile", "reconciliation", "reconcile-then-apply", "normalization", "legacy location", "fact-sheet version". Checking the design against the live model is part of deploying, not a step of its own: in user prose say "deploy it", "build the spec", "the blueprint has N entities". The user never needs the internal stage names or the front-matter field labels.

Bash `description` fields obey the same rule (they render as "Ran <description>" in chat): neutral plain English ("Checking the workspace", "Reading the artifact"), never "Probe org", "yq check", "Append to customizations.yaml".

**Pipeline hand-offs are not narrated.** When the admin advances from one sub-skill to the next inside an item's pipeline (e.g. the analyst finishes the spec and the modeler is next), emit nothing in chat: the pipeline task going to `in_progress` (Step 6.7) is the trace. Do **not** add a transition sentence announcing the next phase or pre-explaining what it will do: no *"Now applying it to your live model"*, no *"The deploy step will show you what it creates and ask you to confirm"*. Each sub-skill narrates its own work and gates its own writes, so an admin-level preamble in front of it is redundant narration the user did not ask for. The task list plus the sub-skill's own output is the complete trace. The sub-skills' result lines are part of that output, not hand-off narration: in guided and expert flow, the architect's and the analyst's "Wrote `<path>`" close-outs are always sent.

**The admin never duplicates a sub-skill's execution play-by-play.** The deploy, verification, and sample-data steps belong to the modeler sub-skill, which runs inline (Step 6.7) and narrates in ITS own restrained voice. While following the modeler's instructions, obey the modeler's "Narration restraint" rules and add no second layer of admin narration on top: no *"Matching step done"*, *"Confirming the artifact before applying"*, *"Seeding sample data now"*, *"Seven of eight tables confirm cleanly…"*, and no narration of a transient error and its self-correction (*"that ERR was a transient blip"*). Those are exactly the lines the modeler's "Narration restraint" section deletes; emitting extra admin-level narration reintroduces the noise that restraint exists to remove. If you are narrating what the deploy is doing as it happens beyond what the modeler's own rules permit, you are doing the modeler's job in the wrong voice; stop, and let the sub-skill's voice stand.

**Technical / DBA vocabulary is banned in admin chat too**, the same standard as the modeler's banned-token list. Keep these out of user-facing prose: `FK`, `orphan(s)`, `idempotent`, `non-destructive`, `NOT-NULL` and constraint talk, `junction`, `FK-dependency order`, `spec` / `blueprint` version numbers (`v5.2`, `blueprint v3.0`), and raw `snake_case` identifiers. Say "links between records", "safe to re-run", "the connecting records", "your live model" instead. The reader is a domain expert (HR director, operations lead), not a data modeler.

### Per-run diagnostic log

Internal mechanics go to a per-run diagnostic log, never to chat. The admin samples the run-id ONCE at the top of Preflight (`RUN_ID="run-$(date -u +%Y%m%d-%H%M%S)"`) and never re-samples it; every stage writes `.tmp_admin/<run_id>/diag-<role>.log` into that one folder (`diag-admin.log`, `diag-architect.log`, ...). The logs are best-effort (a failed write never blocks the run), diagnostics only (NOT a decision log — that is `customizations.yaml` plus git; a fast run's `auto-picks.md` is a per-run diagnostic, not a policy record, `references/fast-flow.md`), and never named in chat except the run-folder path on a failed run (Step 6.8). Full mechanics — the `log_diag` helper, the per-role file-naming table, and the log rules — are in [`references/output-discipline.md`](./references/output-discipline.md).

---

## Task tracking (resident summary; rules in `references/task-tracking.md`)

The admin uses the harness task tools (`TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet`) for two things. Full mechanics, the response sequence, and the wording rules are the canonical text in [`references/task-tracking.md`](./references/task-tracking.md); this section only says what the admin's tasks are.

**Pipeline tasks (the plan).** After Step 1.1 / 1.3 have resolved and every scope-flag question is answered, create one task per plan line, in pipeline order, subjects from the Step 6.5 line-shape table verbatim (they carry the slug or display name, which is how the final report identifies items). No prefix. Then chain them: every pipeline task after the first gets `addBlockedBy: [<the previous pipeline task's id>]`, continuous across items, so the order is in the list itself, not in numbering. Sub-skills point their own stage tasks at the pipeline task with `addBlocks`, so a pipeline task shows as blocked until its sub-skill's stages are done. Admin-only operations (Step 5, including Get started) create no tasks. Sub-skills create their own `Design › / Match › / Apply ›` stage tasks when they enter; the admin never creates, edits, or completes those. When a sub-skill's output artifact is verified, the admin sets its pipeline task `completed` with the one-line summary in the description; on failure the task stays `in_progress` with the verbatim message.

**Ledger stage: scope flags (Step 6.4).** Every flag question that inference leaves at `?` becomes a `Q:` task (subject = `Q: ` + the exact 6.4 question wording, one question object per flag, up to four per `AskUserQuestion` call). These `Q:` tasks precede the pipeline tasks, so they have no stage task to block; the gate is the rule itself: the pipeline tasks may be created only when `TaskList` shows no `Q:` task pending or in progress. Standalone (no ledger task, unchanged): the Step 0 clarifying question, the 1.1 collision widget, the 1.3 match widget and its follow-ups, "audit both, no name". 1.1 and 1.3 always resolve before the flag ledger starts.

---

## Preflight (runs before Step 0, every invocation)

**Preflight produces no chat output** (see Output discipline above). Do not announce it; never write the words "preflight" or "silent" to the user. Sample `$RUN_ID` and set up `$DIAG_LOG` (`diag-admin.log`) first, then run the four shared preflight checks with NO chat narration, writing their results to the log. The only user-facing output is a halt message (a required tool could not be installed) or a setup action the user must see (installing a required tool, getting the CLI on PATH, naming the host, or opening the sign-in link). On all-pass with every tool already installed and the CLI authenticated, say nothing and let your first user-facing line be the download milestone (URL requests only), the first question, or the plan. The `$RUN_ID` sampled here is the one reused by Step 6.2 — never re-sample it.

**Run the shared preflight: [`references/preflight.md`](./references/preflight.md).** The canonical checks live there as the single source of truth shared by the admin and all three sub-skills:

1. **Stay in the repo root** (never `cd`; the CLI reads `.env` from cwd).
2. **Install the supporting toolchain (Bun, jq, yq)** — auto-install any missing tool, package-manager-first with a static-binary fallback, on Windows / macOS / Linux, including the mikefarah-yq footgun guard.
3. **Ensure the `semantius` CLI is installed and authenticated** — one `getCurrentUser` probe folds the install check, the auth check, and the org / `ui_baseurl` read; install the CLI if missing (or call it by full path when it is installed but not yet on PATH); with no host or a failed sign-in, sign the user in with `semantius use <host>` in the background, relaying the link.
4. **Compute the customizations file path** (`CUSTOMIZATIONS_FILE="semantius/${org}/customizations.yaml"`).

The admin runs all four as part of an orchestrated run; it then passes the resolved `org`, `ui_baseurl`, and `CUSTOMIZATIONS_FILE` to each sub-skill via the Step 7.3 `Run context:` block, so the sub-skills skip the checks rather than repeat them. Read the reference file for the full per-check procedure, install matrix, and exit-handling tables; do not duplicate that detail here.

---

## Step 0: Identify the request type

The first thing this skill does is classify what the user is asking for. The downstream plan depends on this.

Six request types, in roughly priority order:

| Type | Trigger phrases | Pipeline |
|---|---|---|
| **Get started / onboarding** | "get started", "I'm new here, set this up", "what can I build?" | admin-only (Step 5.5): run preflight (install check) → verify the connection by querying the database → count deployed modules → point to the blueprint catalog |
| **End-to-end build** | "build me a CRM and deploy", "set up an ATS end-to-end", "I need a helpdesk live in our instance" | architect → analyst → modeler |
| **Clone-and-deploy** | "clone the candidate-crm blueprint and deploy", "use ats-candidate-crm as a starting point and deploy", "deploy a copy of the X blueprint" | architect (Catalog-Clone) → analyst → modeler. Copying live tables or a live module *with their data* to another host is a transfer, not a clone-and-deploy: route to `semantius-transfer` |
| **Deploy existing artifact** | "deploy this blueprint", "deploy https://...md", "deploy the file in my workspace" | (fetch if URL) → analyst (if blueprint) → modeler |
| **Inspect / audit / status** | "what's deployed?", "status of semantius", "audit this file" | admin-only (no sub-skill chain), or routes to the right Audit mode |
| **Admin operation** | "list modules", "check the connection", "rotate API key" | admin-only (operates directly via use-semantius). Backup and restore route to `semantius-transfer` |

If the request is ambiguous, ask one clarifying question via `AskUserQuestion`. Do not guess.

---

## Step 1: Inspect the workspace

**Gate: does the request already name an exact, unambiguous source?** A URL, or an exact file path, resolves the source completely — there is nothing left to discover about *where the artifact is*. In that case do NOT run a general workspace inventory. Instead:

1. Derive the candidate slug from the named source (the URL/file's own filename: `it-ops-starter-semantic-blueprint.md` → `it-ops-starter`; `related_modules`/other metadata is not needed for this, just the filename stem).
2. Run ONE targeted **exact-filename** existence check against the convention folders only — `test -f semantius/blueprints/<slug>-semantic-blueprint.md` / `semantius/specs/<slug>-semantic-spec.md`. **Exact filename, never a glob, never a substring/prefix/suffix match.** A file is either named `it-ops-starter-semantic-blueprint.md` and is the artifact, or it is named anything else (`v0-it-ops-starter-semantic-blueprint.md`, `it-ops-starter-v2-semantic-blueprint.md`, `my-it-ops-starter-semantic-blueprint.md`) and is **not a match** — full stop, it does not get read, opened, `cmp`'d, or mentioned. A blueprint's name is its filename; `*<slug>*` glob matching treats "contains the slug as a substring" as "is the artifact," which is exactly backwards — it pulls in prefixed/suffixed variants nobody named and burns a read-and-compare cycle on each one. If the exact-name file is absent, that's a miss: proceed to Step 2 (fetch the named URL) or build fresh, same as if the workspace were empty. Do not fall back to searching for "something close."
3. Do **not** run the workspace-root scan at all for a named-source request. Root-level placement is a concern for artifacts nobody named explicitly; it has no bearing on a request that already says exactly what to fetch and deploy. If the user separately mentions a root-level file by name, that's a *named* source too and step 2's exact-filename check (pointed at root instead) covers it — still not a scan, still exact-match only.

**Only when the request does NOT name an explicit source** (status checks, "what's deployed", a bare "deploy this" with nothing else in the workspace to disambiguate, onboarding) does a general inventory make sense, because there IS something to discover — which artifact, if any, the vague request could mean:

```bash
# Primary location (the convention): semantius/blueprints/ and semantius/specs/
find semantius/blueprints semantius/specs -maxdepth 1 -name '*.md' 2>/dev/null

# Workspace-root locations: blueprints/specs sitting at the workspace root.
# Still scope this to any slug hints the request text does contain (e.g. "the ATS
# blueprint" → scope to *ats*), never a blanket `*-semantic-blueprint.md` glob —
# that pulls every unrelated file at the repo root into consideration for zero
# benefit. Only fall back to the fully unscoped glob when the request truly gives
# no slug hint at all (rare: "what's sitting in my workspace root?").
find . -maxdepth 1 -name '*-semantic-blueprint.md' -o -name '*-semantic-spec.md' 2>/dev/null
```

### 1.1 Locate artifacts in place, and COPY (never move) the deployed artifact into the convention folder

Copy, never move: the skill reads artifacts wherever they are and **copies** (never moves) the deployed artifact into the convention folder. The mechanics for every deploy:

- **Copy up front, with `cp`, before any edit.** As soon as a root-level artifact is resolved for this run, copy it into `semantius/blueprints/` or `semantius/specs/` (created on demand with `mkdir -p`) *immediately*, before the customize / extend / rebuild pass or the analyst runs. The convention-folder copy becomes the **working path**: every edit targets it, so it still matches exactly what was deployed; the root original is read once and never modified (editing it is a bug).
- **Existing differing convention copy:** if a convention copy of this slug already exists and differs from the root, resolve via the "Slug present in BOTH" widget below *first*, then make the chosen version the working copy. Never blind-overwrite.
- If the resolved artifact already lives in the convention folder, it is already the working path; nothing to copy.

The ban is specifically on **moving and deleting** files the skill did not create (a filename pattern is NOT proof of ownership). A non-destructive copy of the single artifact this run deploys is required and expected; never scan-and-move or scan-and-delete pre-existing files.

**Slug present in BOTH root and the convention folder.** Pick which copy to *read* for this request. Never move or overwrite either file as a result.

- **Unrelated file** (not part of this request): leave both copies untouched, log to `$DIAG_LOG`, say nothing in chat. Do not pick a winner, do not mention it. The failure mode to avoid: announcing a `real-estate-agent` collision while the user asked to deploy `hiring-starter`, then admitting "(this is unrelated to your request)". If it's unrelated, it does not belong in chat at all.
- **The artifact being deployed**: the two copies may differ, and reading the wrong one is a real risk, so do NOT silently pick. Compare them with `cmp -s`:
  - **Byte-identical**: no ambiguity. Read the convention-folder copy, log to `$DIAG_LOG`, continue without asking.
  - **Different**: fire the collision widget below and let the user choose which to read. This applies equally to blueprints (root vs `semantius/blueprints/`) and specs (root vs `semantius/specs/`).

**Collision widget** (only when the deployed artifact's two copies differ):

- question: *"There are two different copies of `<slug>`, one in the workspace root and one in the convention folder. Which should I use for this deploy?"*
- header: `"Which copy"`
- options:
  1. `"Convention-folder copy (Recommended)"` — *"Use the copy in the convention folder (the standard location). Last changed `<date>`."*
  2. `"Root-folder copy"` — *"Use the root-level copy instead. It stays exactly where it is; nothing is moved or overwritten. Last changed `<date>`."*

Surface each copy's last-changed date in the option descriptions so the user can tell which is newer. Whichever the user picks, read that copy and leave BOTH files exactly where they are. This disambiguation is a one-off, NOT standing policy; do not write it to `customizations.yaml`, a future collision asks again.

After 1.1, blueprints and specs are read wherever they live (convention folder or repo root); nothing has been moved. Step 1.2 (workspace summary) reads from both locations.

### 1.2 Workspace summary

A slug may live in the convention folder, at the repo root, or both; the skill reads it wherever it is and never moves it (per 1.1). When the same slug appears in both locations, prefer the convention-folder copy as a defensive fallback for the summary, unless the user picked the root copy via the 1.1 collision widget.

For each candidate file, read **only the front-matter** (the first 30 lines is enough). Extract:

- `artifact` (`semantic-blueprint` vs `semantic-spec`)
- `version` (blueprints and specs; the file format version, `"3.x"`)
- `system_slug`
- `reconciled_at` and `source_blueprint` (specs only)

Build a workspace summary:

```
Workspace artifacts:
  semantius/blueprints/
    - ats-candidate-crm-semantic-blueprint.md  (artifact: semantic-blueprint, version: "3.1", slug: ats-candidate-crm)
  semantius/specs/
    - ats-candidate-crm-semantic-spec.md       (artifact: semantic-spec, version: "3.1", slug: ats-candidate-crm, reconciled 2026-05-25)
```

If the request mentions a URL, plan to fetch it first (Step 2).

If the request mentions a specific file by path or name, prefer that over auto-discovery. **When the location the user names doesn't match where the file actually is** (e.g. they say "from the root folder" but the only match lives in `semantius/blueprints/`), just use the unambiguous match silently. Do NOT narrate a paragraph explaining the discrepancy; the user named the artifact, not the path, and a location correction is housekeeping for `$DIAG_LOG`. Surface a one-line clarification only if there are genuinely two candidates and you had to pick.

The workspace summary itself is internal: it goes to `$DIAG_LOG`, not chat. The user does not need a front-matter dump (`version`, entity counts, "reconciled" dates) before the plan. Lead the chat with the plan, not with an inventory. **Exception: 1.3 below.** When an existing workspace artifact matches the user's request, that match MUST be surfaced before the plan is built. The "no inventory dump" rule covers unrelated artifacts; it does NOT cover a slug-match on the thing the user just asked for.

### 1.3 Match check: surface pre-existing artifacts that could satisfy the request

Before constructing any plan, the admin checks whether the workspace already contains a blueprint or spec that could satisfy the user's request. If it does, the admin MUST tell the user and let them choose between deploying the existing artifact, starting over, or auditing it first. Silently building a new blueprint when a matching one already exists, or silently routing the deploy through an existing spec the user didn't know about, is the failure mode this section closes.

**Exception: exact-source bypass — skip the widget entirely.** The widget above exists to resolve *ambiguity* about which artifact the user meant. There is no ambiguity, and the widget must NOT fire, when both of the following hold:

1. The request names an exact, unambiguous source: a URL, or an exact file path/name. (Inferred matches from slug/keyword similarity, per the "What counts as a match" tests below, do NOT qualify — those are exactly the ambiguous case the widget is for.)
2. The workspace already has a blueprint or spec for that source, and it is confirmed **byte-identical** to the named source (fetch it — Step 2 — and `cmp -s` it against the workspace copy per Step 1.1's comparison) or, for a spec, the workspace spec's `source_blueprint` reconciles a byte-identical blueprint and was reconciled **on or after** that blueprint's current content.

When both hold, there is nothing to decide: the workspace artifact *is* the thing the user asked for, byte-for-byte, already reconciled. Log the match to `$DIAG_LOG` and go straight to the plan (deploy the existing spec through the modeler if one is current; otherwise blueprint → analyst → modeler). Asking "what do you want to do?" about a file that is a verified exact match of what was explicitly requested is not resolving ambiguity, it's manufacturing it, and it wastes the user's time. If the fetched source differs even slightly from the workspace copy, the exception does not apply, fall through to the normal match-check widget (the difference is real ambiguity: did the user want the update applied, or did they mean to keep what's there?).

**What counts as a match.** Walk every blueprint and spec in the Step 1.2 workspace summary and apply the following tests against the user's request text:

1. **Slug match.** Derive a candidate slug from the user's request (e.g. "roadmap planner" → `roadmap`; "ATS for our recruiting team" → `ats`, `recruiting`, `ats-candidate-crm`). Any artifact whose `system_slug` equals a candidate slug, or whose `system_slug` is a substring/superstring of one, is a match candidate.
2. **System-name match.** Any artifact whose `system_name` (case-insensitive, ignoring filler words like "and", "the", "for") shares two or more content words with the user's request is a match candidate. Example: request "product roadmap planner" matches `system_name: Product Roadmap` on both `product` and `roadmap`.
3. **Tagline / description match.** Any artifact whose `tagline` shares a notable verb phrase with the request (request "collect ideas and defects, prioritize them" vs tagline "Capture ideas and defects, prioritize them, and build a release plan") is a match candidate.

A request can produce zero, one, or many match candidates. **All must be surfaced, none silently picked.**

**What to do on a match.** Fire `AskUserQuestion` BEFORE any sub-skill is invoked and BEFORE the plan is built. The question shape:

- **question**: *"I found `<file>` in your workspace that looks like it already covers your request (slug `<slug>`, `<system_name>`). What do you want to do?"*
- **header**: `"Existing artifact"`
- **multiSelect**: `false`
- **options** (in this order):
  1. label `"Deploy the existing <blueprint|spec> (Recommended)"`, description: *"Use `<file>` as-is. Skip building a new one. Pipeline: <analyst → modeler for a blueprint match; modeler for a spec match>."*
  2. label `"Audit / review the existing artifact first"`, description: *"Run an audit pass on `<file>` so you can see what's in it before deciding. No writes to your semantic model."*
  3. label `"Start over (build new)"`, description: *"Ignore `<file>` and build a fresh design from scratch. You'll be asked where to move the existing file so it isn't accidentally re-used (the admin never deletes a file it didn't create)."*
  4. label `"Cancel"`, description: *"Stop without doing anything."*

**Multiple match candidates.** When the workspace has more than one matching artifact (e.g. both a blueprint and a spec for the same slug, or two distinct slugs that both could be what the user meant), enumerate them in the question body and let the user pick which one to act on (`AskUserQuestion`, `multiSelect: false`, one option per candidate plus "Start over" and "Cancel"). The tool accepts 2 to 4 options per question, so list **at most 2 candidates** as options (the two whose slug or system name match the request most closely); when there are more, name every candidate in the question body and end it with *"Type the file name of another candidate if it isn't listed."* (the tool adds its own free-text slot; never list an "Other" option). Once the user has picked a candidate, the single-match widget above fires for that file (deploy / audit / start over / cancel). Never silently pick "the newer one" or "the one that matches more closely" — picking is the user's decision.

**On option 3 (Start over).** Fire a follow-up `AskUserQuestion` (`multiSelect: false`, 2 options) asking where to move the pre-existing artifact: `"Move it to semantius/archive/ (Recommended)"` or `"Leave it in place; I'll give the new build a different slug"`. A different folder is written into the tool's free-text slot, not listed as an option. The admin never deletes pre-existing files (per the rules at the bottom of this SKILL); it can only move them, and only with explicit user direction.

**On option 1 / 2.** Skip Step 0's classification result and route directly to the appropriate pipeline (deploy through Step 6 for option 1; architect Audit or analyst Audit for option 2). The user's choice here overrides whatever Step 0 originally classified the request as.

**Run this check between inspection and planning, never after the plan is built**, so the plan is built from the user's informed choice. A match check fired after planning is too late: the plan's narrative already contradicts what's about to happen.

**The "no inventory dump" rule still holds for unrelated artifacts.** A workspace cluttered with old blueprints from prior unrelated work does NOT trigger this widget. Only artifacts whose slug, system_name, or tagline matches the current request surface here. Everything else stays internal per Step 1.2.

---

## Step 2: Fetch remote artifacts (only when input is a URL)

When the user gives an `http(s)://` URL, fetch it before any other step using the canonical fetch-validate-place procedure in **Step 6.1**: `curl -s -L` into `.tmp_admin/<run_id>/incoming/`, validate the first 30 lines parse as front-matter with a known `artifact:` value, then move to `semantius/blueprints/<system_slug>-semantic-blueprint.md` or `semantius/specs/<system_slug>-semantic-spec.md` (folders created on demand). Never `WebFetch`.

On any fetch failure (curl non-zero exit, empty file, no front-matter, unknown `artifact:` value), halt and report the failure verbatim; do not guess. The `semantius/` folder at the workspace root is the committed home for these artifacts (distinct from the plugin install, which lives in the user's Claude Code plugin folder, not their project repo).

**On success, emit the download milestone** (Output discipline): one line per URL, as soon as its front-matter has validated, naming the design by its `system_name` and the source host, e.g. *"Downloaded the Hiring Starter blueprint from semantius.com."* (for a spec: *"Downloaded the Hiring Starter spec from semantius.com."*). That line is this step's ONLY chat output; where the file landed, the staging folder, and the validation are `$DIAG_LOG` material. Do not pre-announce the fetch ("Fetching the blueprint...") and do not add a second line when the file was already present and byte-identical (Step 1.3 bypass): the milestone still reads "Downloaded ...", because it was.

---

## Step 3: Plan the pipeline

Given the request type from Step 0 and the workspace state from Step 1/2, decide which sub-skill(s) to invoke and in what order.

### Decision table

| Request type | Workspace state | Plan |
|---|---|---|
| End-to-end build | Empty workspace | `architect (Create-Greenfield)` → analyst → modeler. **No scope-flag questions fire** (no `customize`, no `review`, no `deploy` ask): the architect's interactive Create pass IS the design, and `deploy` is implied by the build request (in expert flow, only once the user answers yes to the architect's close-out "Deploy it now?"; a no ends the run after the design). The created blueprint becomes Step 6's item; the modeler's own pre-write yes/no is the single gate (in a fast run, the go-ahead in the design step). See "Greenfield and clone builds skip scope flags" below and Pattern 4. |
| End-to-end build | Blueprint present, no spec | **First run Step 1.3 match check.** If the blueprint matches the request, the user's choice at 1.3 routes the run (deploy / audit / start-over). If 1.3 found no match (the workspace blueprint is unrelated), hand off to Step 6 with the workspace blueprint as the only item ONLY when the user's request is explicitly about that blueprint; otherwise treat as Empty workspace. **Never silently use a workspace blueprint the user didn't reference.** |
| End-to-end build | Spec present | **First run Step 1.3 match check.** If the spec matches the request, the user's choice at 1.3 routes the run (deploy / audit / start-over). If 1.3 found no match (unrelated spec), treat as Empty workspace and run greenfield architect. **Never silently use a workspace spec the user didn't reference.** |
| Clone-and-deploy | Empty workspace | `architect (Create-Catalog-Clone)` → analyst → modeler. Like greenfield, the architect creates the artifact, so **no scope-flag questions fire**; `deploy` is implied. The cloned blueprint becomes Step 6's item. |
| **Deploy existing** | **Any (1 or N blueprints/specs)** | **Hand off to Step 6.** This is the universal deploy path regardless of how many items. Scope flags (`customize` / `review`, plus `deploy`) are resolved FIRST per "Resolve scope flags BEFORE presenting the plan" below (inference in 6.4.1, asked when ambiguous), so a bare "deploy this" still fires the customize question before anything runs. |
| Audit | Blueprint named | `architect (Audit)` on the blueprint (does NOT route through Step 6). |
| Audit | Spec named | `analyst (Audit)` on the spec (does NOT route through Step 6). |
| Audit | Both, no name | Ask which to audit (`AskUserQuestion`, `multiSelect: false`, 3 options: the blueprint, the spec, both one after the other). |
| Status | n/a | Admin-only (Step 5). |
| Admin (status, list, health) | n/a | Admin-only (Step 5). Backup and restore: `semantius-transfer`. |

**Why everything-deploy routes through Step 6:** one item or many, the pipeline is the same. Step 6 has the customize/deploy flag plumbing, the customizations-file handoff, the unified report. Greenfield builds and catalog clones also route through Step 6 for the analyst → modeler half and the unified report, but they carry NO `customize` / `review` / `deploy` questions: the architect's Create pass already covered design and `deploy` is implied (see "Greenfield and clone builds skip scope flags"). The only request types that bypass Step 6 are pure-architect operations (Audit on a blueprint), pure-analyst operations (Audit on a spec), and admin-only operations (status, backup, health). Anything that ends in writes to the live semantic model goes through Step 6.

### Resolve scope flags before presenting the plan

Scope flags are resolved before the pipeline tasks are created (scope flags before the plan). They are routing decisions, not confirmations: `customize=yes` makes a blueprint architect → analyst → modeler, `customize=no` makes it analyst → modeler, so a plan cannot be correct until they are resolved. Greenfield builds and catalog clones short-circuit (no scope question fires; the bug guard: "create a task list" must NEVER produce *"Deploy the task-list design as designed, or edit it first?"*). For an existing artifact (a workspace file, a Step 1.3 match, or a URL fetched in Step 2):

- **Single identified artifact** (one named file, one fetched URL, one Step 1.3 match): resolve its flags HERE, before the pipeline tasks are created. The front-matter (`system_name`) is in hand, so the question wording is fully formed.
- **Multi-source / glob** (items only enumerated in Step 6.1): resolve each item's flags in Step 6.4, still before that item's pipeline tasks are created in Step 6.6.

Use the inference-then-ask procedure in Step 6.4 (intent table 6.4.1, exact wording 6.4, procedure 6.4.2); do not re-derive it here. These are scope questions, not the deploy confirmation, so the single-write-gate rule never suppresses them: a bare "deploy this" leaves `customize` at `?` and MUST fire the customize question. The flag questions run through the question ledger (Task tracking above): `TaskList` must show no open `Q:` task before any pipeline task exists.

### Interaction flow switch (no question)

The interaction flow is a persisted switch, `.interaction_flow` in `$CUSTOMIZATIONS_FILE`: `guided`, `expert`, or `fast` (the default when nothing is saved; rules: [`references/interaction-flow.md`](./references/interaction-flow.md)). Handle it here, before any sub-skill starts:

1. If the request says "expert flow", "guided flow", or "fast flow", write `.interaction_flow` (`expert` / `guided` / `fast`) with the usual provenance comment (`references/customizations-protocol.md` 7.5, step 4a) and narrate the one line from interaction-flow.md section 2.
2. Otherwise, if `.interaction_flow` is `expert`, narrate once: *"Running in expert flow."*
3. **Decide the flow for this run** and pass it to every sub-skill as `Interaction flow:` (Step 7.3):
   - Rebuild: `expert`, whatever the switch says; narrate nothing.
   - Switch `expert` or `guided`: the switch value.
   - Switch `fast` or not set, new build (`Architect mode: create`): `fast`; but `guided` for this build only when the request asks to be guided (`references/interaction-flow.md`, section 2), narrating once *"Using guided flow for this one."* and writing nothing.
   - Switch `fast` or not set, any other run (it starts from an existing design): `guided`; only when the switch is saved as `fast`, narrate once *"Fast flow covers new builds only; this run uses guided flow."*

It is not a scope flag: no `Q:` task, no widget.

### Fast flow

In a fast run, read [`references/fast-flow.md`](./references/fast-flow.md) now and again after a context reset. The design step ends with one go-ahead question; after a yes, no sub-skill asks anything until the modeler's closing sample-data question, because the user approved the whole build at once, every further stop breaks that promise, and the closing summary is their review. When the user answers the go-ahead, write the marker into your pipeline tasks' descriptions (`fast: go-ahead given` / `fast: guided flow for this build`; `references/fast-flow.md`, section 3). Before entering the analyst, and again before the modeler, read the marker in your pipeline task's description (`TaskGet`): `fast: go-ahead given` means pass `Interaction flow: fast`; `fast: guided flow for this build` (the user chose "Ask me along the way") means pass `guided`.

**Exit check (fast flow).** Before the modeler's closing message goes out, scan the closing block of the assembled draft (the lines after the `---`) and **count**, per the modeler's Closing Contract:

- **Absolute URLs:** none outside the Open link, `[Open <System Name> in Semantius →](<ui_baseurl>/<module_slug>)`, and the spec download line. The download line's link form is the environment's, so the gate doesn't judge it.
- **Link targets:** the Open link's URL is exactly `<ui_baseurl>/<module_slug>` (the `ui_baseurl` read at setup), and its text names the System Name. The download line hands over the deployed spec, `<system_slug>-semantic-spec.md` (the `Input artifact:` file, after Stage 5b), and no other file. Check both in the response that logs `fast: close-out verified`.
- **File download links:** exactly 1 in a fast run, exactly 0 in guided or expert flow. 2 or more fails, whatever the extra files are.
- **The sample-data question:** present and unanswered, unless the user already answered it.

A failure is not a wording problem to be smoothed over. Delete an extra line, correct a line whose target is wrong, add a missing one (the Open link, the spec download line in a fast run, the sample-data question unless it was answered), re-scan, then send. The count is the gate; presence alone is not. Write `log_diag "fast: close-out verified"` in the response before the closing message (the one that completes the Verify task), because the closing message has no tool call after its text.

### Presenting the plan

By this point the scope flags are resolved, so the plan reflects them and shows the right number of steps. **Pipeline flows (build, clone, deploy) do NOT build-and-run their plan here** — they hand off to Step 6, which creates the pipeline tasks in Step 6.6 after Step 6.4 resolves each item's flags. Step 3 builds a runnable plan only for flows that bypass Step 6 (audit, admin). Never build a deploy plan and jump straight to entering a sub-skill from Step 3: that skips Step 6.4.

The plan is the task list: create one task per plan line, then emit the one-sentence lead-in in chat (single write gate: no up-front Proceed? widget; the modeler asks its own yes/no). The plan-line authoring rules, the four plan patterns (read-only / write-bound / network-fetch / greenfield), and the worked multi-item examples are in [`references/plan-shapes.md`](./references/plan-shapes.md). The canonical write-bound shape is two tasks plus one sentence:

- Task: `Match ats-candidate-crm against your live semantic model and write the spec.`
- Task: `Apply ats-candidate-crm to your live semantic model.`
- Chat: *"Here is the plan. The matching step asks you a few merge / reuse questions and writes nothing; the apply step updates your live model after it shows you what changes and you say yes."*

Then run the pipeline; the modeler is the single write gate. If the user wants to change scope or stop after seeing the plan, they say so in chat; re-resolve the flags (Step 6.4), set the obsolete pipeline tasks `deleted` and create the new ones, or stop cleanly ("Cancelled. No changes made."). Nothing has run, and the modeler still gates every write, so no unintended write can slip through.

---

## Step 4: Execute the pipeline

For each step in the plan, run the corresponding sub-skill **inline in the main thread** (load and follow its `SKILL.md` in this same conversation context) so its `AskUserQuestion` prompts reach the user directly.

**All three pipeline sub-skills are interactive, so all three run inline.** The architect's customize pass is an interactive edit loop only the user ends; the analyst fires the merge / reuse / promote / collision questions during reconciliation; the modeler asks its pre-execute yes/no before every write. **Never spawn an interactive sub-skill as an Agent-tool subagent:** a subagent runs in an isolated context and cannot conduct these dialogs, so its questions would never reach the user and the pipeline would stall or guess. Reserve the Agent tool for genuinely non-interactive helper work only — none of the architect / analyst / modeler pipeline steps qualify.

### Sub-skill invocation pattern

For each step:

1. **Pre-flight**: confirm the input artifact exists at the expected path, then set the step's pipeline task `in_progress`.
2. **Invoke inline**: establish the run context (Step 7.3) in the conversation, then enter the sub-skill in this same context and follow its `SKILL.md`. Let its `AskUserQuestion` prompts surface to the user; answer nothing on the user's behalf (in a fast run after the go-ahead, the sub-skill itself picks each answer by its own rules and logs it; the admin still decides nothing). The sub-skill creates and drives its own stage tasks; the admin does not touch them. The sub-skill produces its output artifact.
3. **Verify**: confirm the expected output artifact appeared in the workspace at the expected path.
4. **Record**: set the pipeline task `completed` with a one-line summary (output path, key metrics) in its description. Nothing in chat; the final report (Step 6.8) or the close-out (Step 8, for audit runs that bypass Step 6) is where the summary reaches the user.

If any sub-skill halts, surfaces an error, or asks the user a question the admin can't answer on its behalf, **stop the pipeline at that point** and surface the sub-skill's last message verbatim. The admin does not try to recover or guess. (In a fast run after the go-ahead the sub-skills ask nothing, so only a halt or an error stops the pipeline.)

### Common sub-skill triggers (so the admin invokes them correctly)

| Sub-skill | Invoke when | Input artifact | Output artifact |
|---|---|---|---|
| `semantius-architect` | Building a new blueprint, cloning a catalog blueprint, or auditing/extending/rebuilding an existing blueprint | (none, or `<slug>-semantic-blueprint.md` for Audit/Extend/Rebuild/Customize modes) | `<slug>-semantic-blueprint.md` |
| `semantius-analyst` | Reconciling a blueprint against live catalog into a deployable spec | `<slug>-semantic-blueprint.md` | `<slug>-semantic-spec.md` |
| `semantius-modeler` | Deploying a reconciled spec | `<slug>-semantic-spec.md` | (live catalog mutations) |

### Versioned input gates

Each sub-skill enforces its own version contract on input. The admin trusts those gates — it does not pre-check versions. If a sub-skill rejects input as a version mismatch, surface the rejection message verbatim.

---

## Step 5: Admin-only operations

Operations that don't involve the architect / analyst / modeler chain. The admin executes these directly via `use-semantius` (CLI patterns) without spawning sub-skill agents. Full procedures (the exact Status output template, the listing wrappers, and the health probe) live in [`references/admin-operations.md`](./references/admin-operations.md); load it when running one of these.

| Operation | Trigger | What it does |
|---|---|---|
| **Status** (5.1) | "what's deployed?", "status of semantius" | Show workspace artifacts and live modules (entity / permission counts, last deploy). Read-only. |
| **Backup** (5.2) | "back up the catalog", "snapshot module X", "restore this backup" | Not run here: route to `semantius-transfer`, which exports to a restorable file with the CLI's `export_module` and restores with `import_module`. |
| **Listing** (5.3) | "list modules / entities / permissions / users / roles" | Convenience read wrappers producing readable tables. Read-only. |
| **Health** (5.4) | "check the connection" | `semantius whoami` and `semantius ping`, read a known built-in, report OK / FAIL. |

Get started (5.5) stays resident below: it is a top-level request type (Step 0) with its own onboarding flow.

### 5.5 Get started (onboarding)

**Get started** — the front door for someone new to the platform. It makes sure the tooling is in place, verifies the connection by querying the live database, reports how much is already deployed, and points to https://app.semantius.com (sign up, or access the dashboard) and the blueprint catalog so the user can stand up a data platform tailored to them. Safe to run anytime; triggered by "get started", "I'm new here, set this up", and the like (no external command required).

Flow:

1. **Run the shared preflight** ([`references/preflight.md`](./references/preflight.md)). This is the install check: it installs the `semantius` CLI, Bun, jq, and yq if any are missing (Windows / macOS / Linux), and settles the connection (asking which host when none is configured, then starting the sign-in and giving the user the link to open). On success the active `org` and `ui_baseurl` are in hand. If a guard halts (a tool could not be installed, the user has not signed in yet), surface that and stop; a user who has no instance yet signs up at https://app.semantius.com, which gives them their instance address — there is nothing to get started against until the platform is reachable.
2. **Verify the connection by querying the database.** Confirm the catalog actually reads back, not just that the CLI authenticated:

   ```bash
   semantius call crud read_entity --single '{"filters": "table_name=eq.users"}'   # a known built-in must read back
   semantius call crud read_module '{}'                                            # the deployed modules
   ```

   If either errors, surface the verbatim error and stop: the platform is reachable but the catalog is not queryable, which the user must resolve before anything else.
3. **Count the deployed modules.** From the `read_module` result, count the custom data modules: those carry a non-empty `domain_code` column (the deploy pipeline's marker), distinct from platform built-ins. That count is the "your data platform so far" number.
4. **Report, and point to the catalog.** Use human language, never raw slugs:
   - **Nothing deployed yet (no custom modules):** *"You're connected to `<org>`, but no custom data modules are live yet. Semantius is built around customizable blueprints — pre-designed data models you tailor into a hyper-customized data platform — and I can deploy one for you. Your dashboard is at https://app.semantius.com."*
   - **Some modules already deployed:** *"You're connected to `<org>` with N data module(s) live: <plain-English names>. Every system in the catalog is a customizable blueprint you can tailor into a hyper-customized data platform. Your dashboard is at https://app.semantius.com, and just ask me for a full status anytime."*
5. **Offer the next step, don't force it.** One short line: ask me to deploy a catalog blueprint, build a new system from an idea, or show a full status. Then wait.

Read-only against the catalog. The only writes are the tool installs and the sign-in with its host pin (`semantius use`, after the user names the host), which the user authorized by asking to get started.

---

## Step 6: Pipeline execution

A deploy request accepts one source or many. Two URLs, three local paths, a glob like `./blueprints/*.md`, or any mix. The admin walks the same checklist regardless of how many items it received.

Decisions the user makes inside one item (cross-module collisions, host-master picks, missing-owner choices) are recorded in `semantius/<org>/customizations.yaml` as standing policy, so later items in the run — and every future run — auto-resolve without re-asking. Avoiding duplicate prompts is the whole point.

### 6.1 Resolve sources

Walk the deploy sources named in the request left-to-right (when invoked as a plugin command they arrive as the command arguments; standalone, read them from the user's message). Each source is one of:

- `http(s)://...` URL: download via `curl -s -L` (never `WebFetch`). Land in `.tmp_admin/run-<id>/incoming/<derived-filename>.md` for validation; on success, move to the workspace artifact folder (`semantius/blueprints/<system_slug>-semantic-blueprint.md` or `semantius/specs/<system_slug>-semantic-spec.md`) and emit the one download milestone line per Step 2 (*"Downloaded the Hiring Starter blueprint from semantius.com."*), the only chat output the fetch produces.
- Local file path: accept both the convention folders (`semantius/blueprints/<file>`, `semantius/specs/<file>`) and bare workspace-root paths. A root-only artifact is **copied into the convention folder up front per Step 1.1's copy rule, before any sub-skill runs**, and the convention-folder copy becomes the resolved working path for the rest of the run; the root original is read once and then never edited. (copy, never move; never edit the root.)
- Glob pattern: expand against the workspace. Sensible glob shapes include `semantius/blueprints/*.md`, `semantius/specs/*.md`, or `./*.md` for the workspace root. Order is whatever the shell returns; user can re-order by listing sources explicitly.

Build a flat list of resolved file paths (validated, final locations). Validate each one:

- Exists and is readable.
- First 30 lines parse as YAML front-matter.
- Has an `artifact:` key with a value the admin knows (`semantic-blueprint` or `semantic-spec`).

On any failure (curl non-zero, missing file, malformed front-matter, unknown `artifact:` value), halt with a plain-English error naming the failing source. Do not fall back, do not skip the offender silently.

Create the artifact folders if they don't exist yet: `mkdir -p semantius/blueprints semantius/specs`.

### 6.2 Reuse the run-id

`$RUN_ID` was already sampled once in Preflight (it is the single timestamp for the whole invocation). Reuse it here; do NOT call `date` again — a second sample would split downloads and diagnostics across two differently-named folders.

```bash
# RUN_ID comes from Preflight. Same folder already holds diag-admin.log.
RUN_DIR=".tmp_admin/$RUN_ID"
mkdir -p "$RUN_DIR/incoming"
```

The folder stays on disk after the run completes; the next run gets its own folder. The user manages cleanup. The run folder holds incoming downloads (`incoming/`) and the per-agent diagnostic logs (`diag-<agent>.log`, per the Output discipline section), plus, in a fast run, `auto-picks.md` (the per-run list of what was picked for the user; [`references/fast-flow.md`](./references/fast-flow.md), section 5). No decision log: persisted decisions live in `$CUSTOMIZATIONS_FILE` (per-org, committed) per Step 7.

### 6.3 Inspect each artifact

For each resolved path, read only the first 30 lines and extract:

- `artifact` (`semantic-blueprint` vs `semantic-spec`)
- `system_slug`
- `system_name` (the human display name; from front-matter, or the top-level `# <name>` heading). Needed for the close-out's plain-English link text (Step 6.8 / Step 8); in user-facing prose, lead with this, never the raw slug.
- `naming_mode` (present → greenfield blueprint; absent → catalog-clone blueprint; not applicable for specs)

The full file goes to the sub-skill by path reference. Do not read the body into admin context.

### 6.4 Resolve scope flags (infer from intent first, then ask remaining)

**Greenfield and clone items skip 6.4 entirely.** When the item is a blueprint this run's architect just created (a greenfield build or a catalog clone), scope flags do NOT apply: the Create pass was the interactive design, `deploy` is implied, and `customize` / `review` are N/A. Route such items straight to analyst → modeler (Step 6.5) without asking anything. In expert flow the architect's close-out asks "Deploy it now?"; on a no the run ends after the design, the analyst and modeler tasks stay `pending`, and Step 8 closes out. Resolve scope flags ONLY for artifacts that pre-existed the run (a workspace file or a URL fetched in Step 2).

**Ordering (hard rule) for pre-existing artifacts: scope flags are resolved BEFORE the pipeline tasks are created in 6.6.** For a single identified pre-existing artifact this already happened in Step 3 ("Resolve scope flags BEFORE presenting the plan"); re-read those resolved values here and validate they fit the item's artifact type (a blueprint takes `customize` + `deploy`; a spec takes `review` + `deploy`). For items first enumerated in Step 6.1 (multi-source / glob), resolve them here. These are routing / scope questions, NOT the deploy confirmation, so the "no up-front gate" rule does not suppress them: a bare "deploy this" leaves `customize` at `?` and MUST fire the customize `AskUserQuestion` before the plan and before any sub-skill is entered. The mechanical form of this rule: the flag questions are `Q:` ledger tasks, and 6.6 may not create a pipeline task while `TaskList` shows a `Q:` task pending or in progress.

Up to three flags apply per item. Which two are in play depends on the artifact type:

| Flag | Applies to | Default | What it decides |
|---|---|---|---|
| `customize` | blueprint inputs | `no` | Whether to edit the design (entities, relationships) before it is built and applied, or deploy it as designed. |
| `review` | spec inputs | `no` | Whether to review the spec against the live model for drift before applying, or apply directly. |
| `deploy` | both | `yes` | Whether to apply the result to the live model, or stop at a dry run (build only). |

**Exact wording when a flag must be asked.** When inference (6.4.1) leaves a flag ambiguous and the procedure (6.4.2) fires `AskUserQuestion`, use the wording below verbatim, putting the design's display name (its `system_name`, e.g. "Hiring Starter") wherever `<system_name>` appears. Two rules keep these prompts clear, because an option labeled only "Deploy as-is" with no impact line is the vague prompt this block exists to prevent:

1. **Every option description states the concrete downstream impact:** what runs next, and what does (or does not) get written to the live model. The label names the choice; the description spells out what happens.
2. **"As designed" and "directly" refer to the artifact's *content*, never to file handling.** Copying the source artifact into `semantius/blueprints/` is automatic and is never a user choice (Step 1.1). Never word an option so it reads as "use the file I found" or "should I copy it"; that conflates the design decision with the copy rule and is exactly the ambiguity being removed.

`customize` (blueprint inputs), header `Edit design?`:
- question: *"Deploy the `<system_name>` design as designed, or edit it first? Editing opens an interactive pass to add or remove entities and adjust relationships before anything is built. Deploying as designed leaves the entity list and relationships exactly as written."*
- option 1 (default): label `Deploy as designed (Recommended)`, description *"Use the design unchanged and deploy it. No entities or relationships are edited."*
- option 2: label `Edit the design first`, description *"Open an interactive editing pass first (add or remove entities, change relationships). When you say you are done, I match the edited design against your live model and apply it."*

`review` (spec inputs), header `Review spec?`:
- question: *"Apply the `<system_name>` spec directly, or review it against your live model first? Reviewing shows what would change (drift) before anything is written; it does not modify your model."*
- option 1 (default): label `Apply directly (Recommended)`, description *"Skip the review and hand the spec to the apply step. The apply step still shows its own summary and asks before it writes anything."*
- option 2: label `Review against the live model first`, description *"Compare the spec to the current state of your live model and surface any drift. Read-only; nothing is written until you choose to continue."*

`deploy` (both), header `Apply?`:
- question: *"Apply the result to your live model at the end, or stop short for a dry run?"*
- option 1 (default): label `Apply to your live model (Recommended)`, description *"Run the full pipeline and write the result to your live model. The apply step shows a summary and asks before writing."*
- option 2: label `Dry run (build only)`, description *"Build the spec but do not touch your live model. You get the spec file to inspect; nothing is written."*

Blueprint inputs resolve `customize` + `deploy`; spec inputs resolve `review` + `deploy`. Never both `customize` and `review` on the same item. (The access level (`access_scope`) is **not** an admin scope flag: the architect decides the access level in its permission step. The admin neither detects it nor asks about it.)

**A blueprint without an access level always goes through Customize.** Before resolving `customize` for a blueprint item, read the working copy's frontmatter: `yq --front-matter=extract '.access_scope' <working copy>`. When it is empty (`null`), set `customize = yes` without asking (the `customize` question above is skipped for that item, also after "deploy as is" or "just deploy"): architect Customize's first step decides the access level and stamps it before the analyst runs. Resolve `deploy` as usual.

**Inference happens BEFORE asking.** Scan the user's request for intent verbs and pre-fill the flags. Only fire `AskUserQuestion` for flags that remain genuinely ambiguous. The rule of thumb: only explicit opt-out phrases ("deploy as is", "just deploy", "deploy unchanged") let us skip the edit-first ask; bare deploy verbs always ASK.

#### 6.4.1 Intent → flag inference table

The table has two halves, one per artifact type. Pick the half matching the current item's `artifact:` value and walk it top-to-bottom; first match wins.

**Blueprint inputs** (artifact is `semantic-blueprint`):

| Phrase pattern in the user's request | `customize` | `deploy` | Notes |
|---|---|---|---|
| "build me a X", "create a X", "I need a X", "set up a X end-to-end" (greenfield: no pre-existing artifact; the architect creates it this run) | N/A | `yes` | Greenfield build. The architect's interactive Create pass IS the design, so there is no `customize` question. `deploy` implied; modeler is the write gate. Skip 6.4 for this item (greenfield short-circuit above). |
| "deploy as is", "just deploy", "deploy unchanged", "deploy verbatim", "deploy straight", "deploy without changes" | `no` | `yes` | Explicit opt-out of customization. Skip both asks. |
| "deploy this", "deploy that", "deploy these", "deploy all of these", "push this", "apply this", "make it real", "implement this", "set up in semantius" | `?` (ask, default no) | `yes` | Deploy verb without an as-is qualifier. Skip the deploy ask; ASK the customize question. |
| "create spec(s) for", "reconcile this", "match this against the live model", "what would change if", "analyze this blueprint", "dry run", "plan only", "just generate the spec", "check against semantius" | `no` | `no` | Analyst-only intent. Both flags inferred; skip both asks. |
| "customize this first", "let me edit the entities", "tweak before deploying", "review and adjust", "audit and update" (on a blueprint) | `yes` | (still ask) | Customize is explicit; user might just want to customize and stop, or customize then deploy. Ask deploy. |
| "customize and deploy", "edit then push", "tweak and apply", "review and deploy this" | `yes` | `yes` | Both explicit. No asks. |
| "customize this" (no deploy verb anywhere) | `yes` | `no` (Recommended) | Lean no but confirm once. |
| Ambiguous: bare URL with no verb, "set this up", "use this blueprint" | `?` (ask) | `?` (ask) | Fall back to the defaults via `AskUserQuestion`. |

**Spec inputs** (artifact is `semantic-spec`):

| Phrase pattern in the user's request | `review` | `deploy` | Notes |
|---|---|---|---|
| "deploy the spec as is", "just deploy the spec", "deploy spec unchanged", "directly deploy", "deploy without review" | `no` | `yes` | Explicit opt-out of review. Skip both asks. |
| "deploy the spec", "deploy this", "push the spec", "apply this", "make it real", "implement this" | `?` (ask, default no) | `yes` | Deploy verb without an as-is qualifier. Skip the deploy ask; ASK the review question. |
| "review the spec and deploy", "audit then deploy", "check the spec then push" | `yes` | `yes` | Both explicit. No asks. |
| "review the spec", "audit the spec", "check the spec", "look at the spec first" (no deploy verb) | `yes` | `no` | Review-only intent. Both flags inferred; skip both asks. |
| Ambiguous: bare URL with no verb, "set this up", "use this spec" | `?` (ask) | `?` (ask) | Fall back to the defaults via `AskUserQuestion`. |

The classification is lenient on `deploy` (favor inferring) and strict on `customize` / `review` (favor asking unless the prompt explicitly opts out). One false positive on the edit-first flag silently skips a step the user wanted; a needless ask is cheap by comparison.

#### 6.4.2 Procedure

0. **Greenfield / clone short-circuit.** If the item is a blueprint this run's architect created (greenfield build or catalog clone), STOP: scope flags are N/A, `deploy` is implied (in expert flow, by a yes to the architect's "Deploy it now?"), route it straight to analyst → modeler. Do not run the steps below for it.
0a. **Blueprint without an access level.** For a blueprint item run `yq --front-matter=extract '.access_scope' <working copy>`; `null` → `customize = yes` (forced: no `Q:` task and no question, also after "deploy as is" or "just deploy"), then resolve only `deploy` below.
1. Read the user's full request text (the message that triggered the run).
2. For each item, pick the half of the table (blueprint or spec) matching the artifact, then walk it top-to-bottom; first match wins.
3. For every flag that remains `?` after inference, ask it through the question ledger (`references/task-tracking.md`, Pattern B): one `Q:` task per flag whose subject is `Q: ` + that flag's exact 6.4 question wording, then batches of up to four question objects per `AskUserQuestion` call, each question carrying its 6.4 header, both options with their impact-explicit descriptions, and the default option marked Recommended. One question object per flag, never two flags merged into one question. The answer is recorded on the item (in the pipeline task's description once it exists) and the `Q:` task set `completed`. `TaskList` clean of `Q:` tasks is the precondition for 6.6.
4. Inferred flags are NOT narrated (no *"Inferred: customize=no, deploy=yes."*): raw flag tokens are internal vocabulary. The resolved scope reaches the user through the plan lead-in, which names the steps and says which one writes to the live model, and 6.4.3 covers a correction. The flag values go into the pipeline tasks' descriptions and `$DIAG_LOG`.

#### 6.4.3 Changing scope before the run

There is no up-front confirmation gate to pick "change" from. If the user asks to change scope after seeing the plan (in chat), re-resolve the in-play flags for the run, set the obsolete pipeline tasks `deleted`, and create the new ones. The intent inference doesn't run again on an explicit correction (the user is overriding it).

### 6.5 Build the checklist

For each item, derive its pipeline by artifact type and the **already-resolved** flags (Step 3 / 6.4 resolved them before this point; 6.5 only reads them, it never asks or re-resolves). **Each sub-skill in an item's pipeline is its OWN task; do NOT collapse multiple sub-skills into one task.** A blueprint with customize=yes and deploy=yes is three tasks, not one.

**Pipeline per item:**

| Input artifact | edit-first flag | deploy | Pipeline (each step = one task) |
|---|---|---|---|
| `semantic-blueprint` | `customize=no` | `yes` | analyst Reconcile → modeler |
| `semantic-blueprint` | `customize=no` | `no` | analyst Reconcile |
| `semantic-blueprint` | `customize=yes` | `yes` | architect Customize → analyst Reconcile → modeler |
| `semantic-blueprint` | `customize=yes` | `no` | architect Customize → analyst Reconcile |
| `semantic-blueprint` without `access_scope` | `customize=yes` (forced, never asked; 6.4) | `yes` / `no` | as the two `customize=yes` rows above |
| `semantic-spec` | `review=no` | `yes` | modeler |
| `semantic-spec` | `review=no` | `no` | refuse this item (nothing to do — narrate one line and skip) |
| `semantic-spec` | `review=yes` | `yes` | analyst Review → modeler |
| `semantic-spec` | `review=yes` | `no` | analyst Review |

The plan is the task list: one `TaskCreate` per pipeline step, in item order, subject from the table below using each file's `system_slug` (or filename if slug is missing), per the plan-line authoring rules in [`references/plan-shapes.md`](./references/plan-shapes.md) (action-first, "your semantic model", filenames surfaced in the close-out not the subject). The plan is informational (single write gate: no confirmation widget at the end; creating tasks is not a pause).

**Per-sub-skill task subjects:**

| Sub-skill | Task subject |
|---|---|
| architect Create (greenfield) | `"Design the data model for your <system>, mapping out its entities and how they relate (interactive)."` |
| architect Catalog-Clone | `"Clone the \`<source>\` design as a starting point (interactive)."` |
| architect Customize | `"Review and edit \`<slug>\`."` |
| analyst Reconcile (from a blueprint) | `"Match \`<slug>\` against your live semantic model and write the spec."` |
| analyst Review (from a spec) | `"Review \`<slug>\` against your live semantic model."` |
| modeler | `"Apply \`<slug>\` to your live semantic model."` |

For multi-item runs, create item one's tasks, then item two's, and so on, and chain every task after the first with `addBlockedBy: [<previous pipeline task id>]` (one chain across all items; that is the order, and the reason numbering is never used: ids interleave with the sub-skills' own stage tasks and with `Q:` tasks). Each subject stands alone; don't compress repeated phrases.

Worked examples for every flag combination (multi-item analyst → modeler, dry-run, customize, direct spec deploy, review-then-deploy) are in [`references/plan-shapes.md`](./references/plan-shapes.md). The modeler shows its own summary and asks a final yes/no before writing each item.

**Lead-in sentence rule:** the one chat sentence that accompanies the tasks tells the user which step asks questions and what gets written, naming steps by what they do (never by number). If any task is a modeler apply: *"Here is the plan. The matching step asks you a few merge / reuse questions and writes nothing; the apply step updates your live model after it shows you what changes and you say yes."* If no apply task exists: *"Here is the plan. The matching step asks you a few merge / reuse questions; nothing is applied to your semantic model, and the spec is written to `semantius/specs/`."* Drop the matching clause when no analyst step exists; add *"The editing step is interactive and ends when you say you are done."* when an architect step exists. A fast-flow new build uses the fast-flow lead-in instead (`references/plan-shapes.md`, Pattern 4, fast-flow variant).

**Spec + `deploy=no` + `review=no` is refused.** If an item resolves to that combination, narrate one line — *"`<slug>` is a spec with deploy=no and review=no; nothing would happen. Skipping."* — and drop the item from the run before creating any task.

### 6.6 Present the plan and run

Precondition: `TaskList` shows no `Q:` task pending or in progress (every scope flag answered). Then create the pipeline tasks per 6.5 and chain them (`TaskCreate` all, then `TaskUpdate ... addBlockedBy` on each after the first, in the same response), emit the lead-in sentence, and run (single write gate: no up-front confirmation widget, one item or many). In a fast run each pipeline task's description starts with the marker `fast: awaiting go-ahead` (`references/fast-flow.md`, section 2).

- **Run includes writes** (`deploy=yes` for any item): each item's modeler step shows its own plan summary and asks a final yes/no before it writes — one modeler confirmation per deploying item, fired when that item's spec is ready. In a fast run the go-ahead in the design step is that confirmation, and the modeler does not ask again.
- **Read-only run** (`deploy=no`): create the tasks, emit the lead-in, run.
- **Changing scope or cancelling:** if the user asks to change scope or stop after seeing the plan, re-resolve the flags (6.4), set the obsolete tasks `deleted` and create the new ones, or stop cleanly. No widget needed; nothing has run yet and the modeler still gates every write.

If a URL fetch happened in 6.1, print the URLs and run the fetch first (it writes nothing to the live model and is never a task), then continue.

### 6.7 Execute item by item

Iterate the resolved list in user-given order. Trust the order; do not topologically sort. Cycles are user error.

For each item:

**Precondition (hard gate):** this item's scope flags are already resolved (Step 3 / Step 6.4) and its pipeline tasks created (Step 6.6). If `customize` (blueprint) or `review` (spec) is still unresolved, STOP and resolve it first; never enter the item's first sub-skill with an unresolved scope flag. Never jump from the Step 3 plan straight to entering the analyst while skipping the customize question.

1. Set the item's first pipeline task `in_progress`. No chat line: the task status is the trace. Do not double-narrate what the sub-skill itself will narrate, and do not add a transition sentence between sub-skills (no *"Now applying it to your live model..."*, no pre-explaining the deploy step), see "Pipeline hand-offs are not narrated" in Output discipline.
2. Establish the run context per Step 7.3's schema (stated in the conversation, not prepended to an Agent-tool call):
   - Always: `Run context:`, `Customizations file:`, `Interaction flow:` (the flow for this run, Step 3 "Interaction flow switch"; before the analyst and the modeler of a fast run, re-read the pipeline task marker first).
   - Architect invocation: add `Architect mode:` (one of `create | catalog-clone | audit | extend | customize | rebuild`) and `Input artifact:` — this MUST be the **convention-folder working copy** (`semantius/blueprints/<file>`) resolved in Step 6.1, never the repo-root path. The architect edits the artifact it is handed in place, so handing it the root path is what causes the root file to be mutated; hand it the copy. Derive mode from the resolved flags (table in Step 7.3).
   - Analyst invocation: add `Analyst mode:` (`reconcile` for normal deploys; `audit` / `extend` / `rebuild` for other routes) and `Input artifact:` (the convention-folder working copy, never the root).
   - Modeler invocation: add `Input artifact:` (spec path) and `Deploy flag:` (`yes`/`no` per the resolved deploy choice).
3. Enter the first sub-skill in the pipeline **inline in the main thread** (Step 4 invocation pattern): state the run context from step 2, then follow the sub-skill's `SKILL.md` in this same context so its `AskUserQuestion` prompts reach the user. Do NOT spawn it as an Agent-tool subagent.
4. On sub-skill success, close the step before opening the next (**hand-off gate**): set the finished pipeline task `completed` (one-line summary in its description); only when the `TaskUpdate` result reads `completed`, set the next one `in_progress` and advance. Never set a pipeline task `in_progress` while the one before it is still `in_progress`; this holds in a fast run too, where the hand-off has no pause. The design step's task completes when the blueprint is written and the architect's consistency check has exited clean, not when the matching step starts. If the harness refuses the update because one of the sub-skill's stage tasks is still open, the sub-skill has not finished: return to it, never advance past it. **🛑 Exception (interactive customize gate).** When the step that just completed was the **architect in `customize` mode**, do NOT auto-advance to the analyst the moment an edit lands. The customize step is an interactive LOOP that only the user ends (architect Step C5); a single edit landing is NOT proof the user is finished. The mechanical check: `TaskList` must show the architect's `Design › Edit the design with you` task `completed` (the architect sets it so only when the user answers its own C5 "done?" question). While that task is `in_progress`, the customize pass is still open: wait for the architect's question and the user's answer; do not ask a second admin-level "ready to continue?" question. Advance to the analyst ONLY after that task is `completed`.
5. On sub-skill failure: halt the run. The failing pipeline task stays `in_progress` with `halted: <verbatim message>` in its description; the remaining pipeline tasks stay `pending`. Carry on to Step 6.8 (which renders ✗ / ⏸ from those statuses).
6. When the item's pipeline completes: the convention-folder working copy was already created **up front** (Step 6.1 / Step 1.1) and every edit this run targeted it, so it already matches exactly what was deployed — no post-hoc copy from the root is needed (and copying *from* the root here would be wrong, since the root was deliberately left unedited). Just confirm the convention copy exists (a defensive `cp` from the root is acceptable *only* if the convention copy is somehow absent, e.g. a direct deploy that skipped Step 6.1's resolve). Then advance to the next item.

`customizations.yaml` accumulates across items and across runs; later items consult it before firing their own `AskUserQuestion`s. This is the only cross-item awareness the analyst gets. No multi-item-aware analyst logic exists.

**Tool-call description discipline (same as analyst / architect).** Every Bash call the admin fires during setup and execution has a user-facing `description` field that renders as "Ran <description>" in chat. Don't leak internal vocabulary:

- ❌ Wrong: `"Create run folder and customizations file"`, `"Append to customizations.yaml"`, `"Mkdir tmp_admin"`, `"Fetch URL into staging"`, `"yq insert at .collisions"`.
- ✅ Right: `"Setting up the run"`, `"Downloading the blueprint"`, `"Reading the artifact"`, `"Saving your choice"`, `"Checking earlier choices"`. Neutral plain English, no yq / .tmp_admin / customizations.yaml references.

Similarly for chat narration: when the run folder is created, narrate at most one short sentence — *"Setting up the customize pass on `<slug>`..."* — and skip mentioning the `.tmp_admin/run-<id>/` path. The user doesn't need the scratch staging location; if they want it for debugging, the final report (Step 6.8) surfaces it.

### 6.8 Final report

After the last item (or on halt). **End-of-run check first:** `TaskList`; no pipeline task may be `in_progress` without `halted:` in its description when the report renders. Settle any such task by its true state: its output verified (Step 4 "Verify") → `completed` with the one-line summary; not verified → append `halted: <what is missing>`, so it reports ✗. Then render as markdown prose, never code-fenced. Item status comes from the **admin pipeline tasks** (`TaskList`): every task of an item `completed` → ✓; a task `in_progress` with `halted:` → ✗ (quote its message); an item whose tasks are all still `pending` → ⏸. The sub-skills' own stage tasks are not consulted.

> **2 of 3 items applied to your semantic model.**
>
> - ✓ **HCM Core** is live (23 entities, 9 permissions). [Open HCM Core in Semantius →](<ui_baseurl>/hcm-core)
> - ✗ **ATS Candidate CRM** failed during the matching step: *<verbatim message from analyst>*.
> - ⏸ **ITSM Helpdesk** skipped.
>
> Files written to `semantius/specs/`. Customizations saved to `semantius/<org>/customizations.yaml` (7 new entries). Re-running is safe: items already applied won't be duplicated, and the run picks up where it stopped once you've resolved the failure. Diagnostic detail is in `.tmp_admin/<run_id>/` (one `diag-<agent>.log` per agent) if you need it for support.

A halted fast run adds one line after the halt: *"Before it stopped, I decided N things for you; they're listed in the run folder."* (N = the lines in `auto-picks.md`; [`references/fast-flow.md`](./references/fast-flow.md), section 6.)

**Every ✓ item carries a clickable browser link**, the same call-to-action the modeler's Closing Contract mandates (see [`semantius-modeler` → "Closing Contract: clean and sticky"](../semantius-modeler/SKILL.md)): `[Open <System Name> in Semantius →](<ui_baseurl>/<module_slug>)`. `ui_baseurl` was read once in Preflight from `getCurrentUser` (e.g. `https://tests.semantius.app`); the link text is the human **System Name** (read in Step 6.3), the URL path is the lowercase `module_slug`. Lead each line with the bold System Name, never the bare slug. **Never substitute a developer slash command for this link** in an end-user close-out: a slash command assumes a live Claude Code session with the plugin installed under an exact name (which a standalone install does not have), and it shows a drift report rather than the user's data. Slash commands are developer/admin affordances, not the deploy call-to-action.

For an all-✓ run, drop the "Re-run" and diagnostic-log lines and replace with the usual close-out language from Step 8. The run-folder path is surfaced ONLY when a run fails; never mention it on a clean run.

---

## Step 7: Customization protocol

The authoritative reference for how the admin and sub-skills share standing policy across runs. The architect and analyst SKILLs point at this section.

### 7.1 Why every answer is policy

The architect and analyst never ask the same question twice. Every Stage 3 / authoring-stage answer is written to `semantius/<org>/customizations.yaml` as standing policy *before* the spec or catalog change proceeds. Re-runs of the same blueprint, sibling blueprints that reference the same entity, and brand-new blueprints that share a concept all auto-resolve from this single file.

There is no "just this run" alternative, no follow-up "remember it?" widget, no opt-out. Decisions are policy unconditionally. (A default applied to a question skipped in guided flow, or a pick made in a fast run after the go-ahead, is not a decision: nothing is written; see `references/customizations-protocol.md` 7.6.) The customer's escape hatch is git: revert the line in `customizations.yaml`, re-deploy. Git is the audit log; the file itself carries provenance via trailing comments (`# decided <YYYY-MM-DD> during <blueprint_slug> deploy`).

The only widgets that never write are explicit-cancel options ("Stop, I want to think about it"). On cancel, nothing changes in the file.

### 7.2 File location and creation

```bash
CUSTOMIZATIONS_FILE="semantius/${org}/customizations.yaml"
```

Computed during Preflight (above). Per-org, folder-scoped: the folder name IS the org, so the file body never carries an `org:` field (a duplicate field would drift; the folder path cannot). The folder is created lazily; the file is created the first time a widget answer needs to be written, with `version: "1.0"` as the only initial content. Subsequent writes use `yq -i` for surgical updates that preserve hand-edits and comments.

If the file does not exist when a sub-skill starts, the consultation pattern (7.4) reads `null` for every lookup and falls through to firing the widget; write-on-answer then creates the file.

### 7.3 Run context (admin → sub-skill, inline)

Because sub-skills run **inline in the main thread** (Step 4), there is no Agent-tool input to prepend a header to. Instead the admin states this fixed run context in the conversation immediately before it enters the sub-skill, and the sub-skill reads it from there as it begins. The first two lines apply to every invocation; additional lines are conditional on the sub-skill and the operation being performed.

The `run_id` is also how each sub-skill finds its diagnostic-log folder: it writes `.tmp_admin/<run_id>/diag-<its-own-role>.log` (per the Output discipline section), reusing the admin's single run-id instead of sampling its own timestamp. No separate `Diagnostics:` line is needed; the run-id carries it.

```
Run context: run_id=run-20260527-143012
Customizations file: /abs/path/to/semantius/<org>/customizations.yaml
Interaction flow: guided                                          (every sub-skill; one of: guided | expert | fast; the flow for THIS run, Step 3)
Architect mode: customize                                       (architect only; one of: create | catalog-clone | audit | extend | customize | rebuild)
Analyst mode: reconcile                                         (analyst only; one of: reconcile | audit | extend | rebuild)
Input artifact: semantius/blueprints/<slug>-semantic-blueprint.md   (when an existing file is being operated on)
Customize flag: yes                                             (architect only when relevant; the resolved customize choice)
Deploy flag: yes                                                (modeler only when relevant)

<then the actual sub-skill input — a short plain-English instruction or the user's verbatim intent>
```

**Required lines per sub-skill:**

| Sub-skill | Required header lines | Notes |
|---|---|---|
| `semantius-architect` | `Run context`, `Customizations file`, `Interaction flow`, `Architect mode`, `Input artifact` (if file exists) | The `Architect mode` line is the canonical mode signal — see Step 0 of architect SKILL.md. Without this line, the architect falls back to natural-language detection (and may misclassify). |
| `semantius-analyst` | `Run context`, `Customizations file`, `Interaction flow`, `Analyst mode`, `Input artifact` | Same logic: explicit mode beats inference. |
| `semantius-modeler` | `Run context`, `Interaction flow`, `Input artifact` (the spec path), `Deploy flag` | The modeler does not consult policy (specs already carry every decision). `Interaction flow: fast` is how it knows the go-ahead already confirmed the write. |

**Mapping resolved flags to sub-skill modes — blueprint inputs:**

| `customize` | `deploy` | Architect mode | Analyst mode | Modeler invoked? |
|---|---|---|---|---|
| `no` | `yes` | (skip architect) | `reconcile` | yes |
| `no` | `no` | (skip architect) | `reconcile` | no |
| `yes` | `yes` | `customize` | `reconcile` | yes |
| `yes` | `no` | `customize` | `reconcile` | no |
| `yes` (forced: the blueprint has no `access_scope`) | `yes` / `no` | `customize` (its first step decides the access level) | `reconcile` | per `deploy` |

**Mapping resolved flags to sub-skill modes — spec inputs:**

| `review` | `deploy` | Architect mode | Analyst mode | Modeler invoked? |
|---|---|---|---|---|
| `no` | `yes` | (skip) | (skip) | yes |
| `no` | `no` | (skip) | (skip) | item refused per Step 6.5 — nothing to do |
| `yes` | `yes` | (skip) | `audit` | yes |
| `yes` | `no` | (skip) | `audit` | no |

For end-to-end build flows starting from scratch, set `Architect mode: create`. For clone-and-deploy flows, set `Architect mode: catalog-clone`.

The sub-skill exports `CUSTOMIZATIONS_FILE` from the second line and proceeds. Direct invocations (no admin orchestration) compute the same path themselves at their own Step 0.

### 7.4–7.6 Registry, consultation pattern, and what is NOT written

The operational detail lives in [`references/customizations-protocol.md`](./references/customizations-protocol.md):

- **7.4 Decision-key → yq path registry** — every Stage 3 / authoring-stage widget's `$CUSTOMIZATIONS_FILE` path and value shape. It is the single source of truth for paths; the architect and analyst cite specific rows (e.g. the "Optional entity verdict" row) but never invent new ones.
- **7.5 Consultation pattern (sub-skill side)** — policy lookup → cache-miss `AskUserQuestion` → atomic write-on-answer with a provenance comment, plus the yq footguns (`lineComment` vs `headComment` on mappings), the one-line cache-hit narration, and the write-on-ask discipline (the skill that fires the prompt is the skill that writes the entry).
- **7.6 What is NOT written** — the modeler's pre-execute y/n, free-text "Other" answers, explicit-cancel selections, and any decision inside the modeler.

---

## Step 8: Close-out

After successful execution:

- **Pipeline runs**: state what's now live, where the produced files landed, and give the user a way **into the product**: the same clickable browser link the final report uses (Step 6.8, never a developer slash command). Lead with the **System Name**, not the raw slug; surface file paths here, not in the plan line (in a fast run, leave out where the files are saved). Example (single item): *"Done. **ATS Candidate CRM** is live in your semantic model (6 entities, 7 permissions). [Open ATS Candidate CRM in Semantius →](<ui_baseurl>/ats-candidate-crm). The spec is saved under `semantius/specs/`."* For multi-item runs, use the Step 6.8 per-item link list.
- **Admin-only runs**: state what was produced (list output, status report, health result) and stop.

After unsuccessful execution:

- Surface the failing sub-skill's last message verbatim.
- Suggest the recovery path from `../../docs/architecture.md` § 6 (Failure Modes).
- Never try to "fix" the failure by chaining additional sub-skills.

---

## Routing for natural-language requests (without slash commands)

Every phrasing maps to one of the six request types in Step 0 (whose table carries the trigger phrases and the pipeline for each); the Step 3 decision table then refines by workspace state. A few mappings worth calling out:

- A URL deploy is *fetch → analyst → modeler*; a workspace blueprint is *analyst → modeler*; "deploy the spec" skips the analyst (*modeler* only).
- "Set up X from scratch" is an end-to-end build unless a catalog blueprint named X exists, in which case it is a clone.
- "Audit this file" routes by artifact type to the architect's or analyst's Audit mode (it does not go through Step 6).
- Status, list, and health are admin-only (Step 5).
- Importing a data file (CSV) into a single entity, existing or new, is not admin territory and not a pipeline deploy: route to the `semantius-importer` skill.
- Moving, backing up or restoring modules or tables, with or without their data, is a transfer: route to the `semantius-transfer` skill.

When a phrasing is ambiguous, ask one clarifying question (Step 0); do not guess.

---

## Things the admin must NEVER do

- **Re-decide what a sub-skill decided.** If analyst chose `reuse-from <module>.<entity>` for some entity, the admin does not second-guess. The spec is the source of truth.
- **Skip the analyst when deploying a blueprint.** The modeler refuses to consume blueprints directly; routing a blueprint straight to the modeler is a bug. Always go via analyst.
- **Delete catalog records.** Same `delete_*` ban as the other three skills.
- **Move, rename, overwrite, edit, or delete a workspace file it did not create this run.** Pre-existing files, especially anything at the repo root, are off-limits — this explicitly includes **editing them in place**. A customize / extend / rebuild pass must run against the convention-folder working copy made up front (Step 6.1 / Step 1.1), never the root original. The ONLY files the admin may relocate are ones it downloaded this run (`.tmp_admin/` to the convention folder). Matching a `*-semantic-blueprint.md` / `*-semantic-spec.md` filename pattern is NOT proof of ownership. See Step 1.1.
- **Auto-recover from a sub-skill failure.** Surface the failure; let the user choose the next step.
- **Modify built-in tables silently.** Additive fields are allowed; replacement is not.
- **Write an `org:` field inside `customizations.yaml`.** The folder name is the org; a duplicate field would drift, the folder path cannot.
- **Create a `history.jsonl` (or any decision log file).** Git on `customizations.yaml` is the audit trail. Provenance comments inside the file carry per-entry dates. (The per-run `$DIAG_LOG` is NOT a decision log — it's scratch, ephemeral diagnostics, never a source of truth. Allowed. The task list and the no-task-tool fallback checklist file are the same class: they track open questions and progress; answers live only in `customizations.yaml` and the artifacts. Allowed. The fast-flow `auto-picks.md` in the run folder is allowed: a per-run diagnostic, not a policy record; [`references/fast-flow.md`](./references/fast-flow.md), section 5.)
- **Surface internal mechanics in chat.** Preflight guards, org probes, CLI/`yq` plumbing, stage transitions, and skill-internal vocabulary go to `$DIAG_LOG`, never to the user. See the Output discipline section.
