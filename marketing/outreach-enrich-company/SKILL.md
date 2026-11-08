---
name: outreach-enrich-company
description: 'Adds fresh detail to a thin saved company profile and drafts messages to its people. Use when the user wants it filled out or messages written ("enrich a card", "draft messages from a card"). Not for companies with no card (use outreach-research).'
argument-hint: '"<path/to/company_card.md>" [channels:email|linkedin|both] [sender:<voice text or path>] [enrich:only|skip] [personality:off]'
allowed-tools: Agent, AskUserQuestion, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(cp *), Bash(rm *), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Outreach Enrich Company

## Overview

You are an orchestrator that takes a company card produced by `/outreach-research` and does two things, in this order:

1. **Deepen the dossier**. Fan out five specialist enrichment subagents in parallel — `outreach-news-finder`, `outreach-tech-analyst`, `outreach-growth-analyst`, `outreach-scanner`, `outreach-contact-finder` — each instructed to find data **not already in the card** (gap-filling, not duplicating). Their findings are merged into a new `## Deeper Intelligence` section appended to the card.
1. **Draft outreach letters**. Using the original card data plus the deeper intelligence as personalization fuel, draft one letter per named Key Contact via `expert-copywriter` — each subtly calibrated to the contact's inferred communication style (Social Styles, produced grounded-only by `outreach-personality-profiler`) — then mandatorily naturalize each via `expert-naturalizer`. The letters are appended as a `## Outreach Letters` section inside the card.

The whole pipeline is fully automatic — no approval gates, no mid-run prompts. The user invokes the skill, the skill enriches and writes letters, the card now holds them both.

## When to Use

Works on an existing company card (produced by `/outreach-research`, lives at `.mz/outreach/<run>/companies/<slug>.md`) to add richer company intelligence, outreach letters for its key contacts, or both.

### When NOT to use

- The user has only a company name or domain and no card — run `/outreach-research` first (single-company mode if they want only one).
- The user wants to discover companies first — use `/outreach-research`.
- The user only wants to record an action already taken on a card (an email sent, a call made) — use `/outreach-update-card`.
- The user wants recruiter contacts for a job application — use `/job-recruiter-info` in mz-job-outreach.
- The user wants general marketing copy (landing pages, announcements, social) — use `/copywrite` from mz-creative.
- The user wants letters written to a separate location than the card — this skill only writes back into the card.

## Input

- `$ARGUMENTS` — Required: an absolute or repo-relative path to a company card `.md` file. Two accepted shapes:
  - **Research baseline**: `.mz/outreach/<run>/companies/<slug>.md` — direct output of `/outreach-research`. First activation moves it to `active/`.
  - **Active**: `.mz/outreach/active/<YYYY-MM-DD>_<slug>.md` — a card already activated by this skill or `/outreach-update-card`. The date prefix is the last interaction date; this run updates it to today.
- Optional modifiers (case-insensitive, order-independent):
  - `channels:email|linkedin|both` — overrides per-contact channel auto-detection. Default: best channel per contact (email if known, else LinkedIn DM, else skip).
  - `sender:<inline text or path>` — overrides the sender voice. Inline text becomes the voice description; a path is read as a sender bio markdown file. Default: read `<run>/strategy.json` `sender_voice` field if present.
  - `enrich:only` — run the deep-enrichment phase and skip letter drafting (card gets `## Deeper Intelligence` but no `## Outreach Letters`).
  - `enrich:skip` — skip the deep-enrichment phase and draft letters directly from the existing card content only.
  - `brief:<run_name>` — pull the local business-climate dossier from an `outreach-brief` run; the combo matching the card's sector and location seeds the letters with regional-climate angles. Default: unset (company data only).
  - `personality:off` — disable reader-style calibration entirely (skip the Phase 3 profiling wave; letters use neutral structure). Default: on — role-based priorities always shape the leading angle, and footprint profiling runs automatically when a contact has a usable public profile.
  - Default (neither flag): both phases run.

If `$ARGUMENTS` is empty or no source can be resolved (see Source Resolution below), emit `STATUS: BLOCKED` with a clear message and stop.

## Argument Parsing

The `$ARGUMENTS` variables and the Source resolution rules (which derive `company_slug` and `source_path`) are in `${CLAUDE_SKILL_DIR}/references/argument-parsing.md`. Read it at Phase 0.

## Directory Structure

The run's file layout (state, card snapshot, enrichment, briefs, profiles, drafts, card lifecycle) and the `task_name` and `<run_dir>` rules are in `${CLAUDE_SKILL_DIR}/references/directory-structure.md`. Read it at Phase 0.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                             | Agent(s)                                                                                                                  | Details                               |
| --- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| 0   | Setup + card validation           | — (orchestrator)                                                                                                          | `phases/parse_card.md`                |
| 1   | Parse card + light web enrichment | — (orchestrator + WebSearch)                                                                                              | `phases/parse_card.md`                |
| 2   | Deep enrichment via subagents     | `outreach-news-finder`, `outreach-tech-analyst`, `outreach-growth-analyst`, `outreach-scanner`, `outreach-contact-finder` | `phases/deep_enrichment.md`           |
| 3   | Reader profiling + draft letters  | `outreach-personality-profiler`, `expert-copywriter`                                                                      | `phases/draft_letters.md`             |
| 4   | Naturalize letters                | `expert-naturalizer`                                                                                                      | `phases/naturalize_and_finalize.md`   |
| 5   | Rewrite card (deeper + letters)   | — (orchestrator, Read + Write)                                                                                            | `phases/naturalize_and_finalize.md`   |
| 6   | Verification summary              | — (orchestrator)                                                                                                          | `verification-summary.md` (reference) |

Read `phases/parse_card.md` when you reach Phase 0, `phases/deep_enrichment.md` when you reach Phase 2, `phases/draft_letters.md` when you reach Phase 3, and `phases/naturalize_and_finalize.md` when you reach Phase 4 (or Phase 5 when `enrich_mode == "only"`). If `enrich_mode == "only"`, Phases 3 and 4 are skipped; Phase 5 still runs to append the `## Deeper Intelligence` section. If `enrich_mode == "skip"`, Phase 2 is skipped; Phase 5 only appends the `## Outreach Letters` section.

### Phase 0: Setup + card validation

Run from `phases/parse_card.md`; read it at the start of Phase 0.

### Phase 1: Parse card + light web enrichment

Run from `phases/parse_card.md`, which Phase 0 already loaded.

### Phase 6: Verification summary

After Phase 5 completes, emit the visible block defined in `${CLAUDE_SKILL_DIR}/references/verification-summary.md`, which also lists when `STATUS` is `DONE_WITH_CONCERNS`.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Red Flags

- You drafted a letter referencing a personalization hook that came from your own background knowledge rather than the card, the light-pass enrichment, or the Phase 2 deeper intelligence.
- You wrote a letter that names a product, customer, metric, or date not in the contact's `verified_entities` list (which now includes Phase 2 findings).
- You asserted a Social Style for a contact without a citable public-footprint cue. With no evidence the profiler must fall back to role-based priorities — never guess a style from the title alone.
- A letter named or alluded to the recipient's inferred personality or communication style. The reader calibration must stay invisible in the text.
- You skipped the naturalize pass for any draft. The naturalize pass is mandatory.
- You wrote the letters or the deeper intelligence to a separate file outside the card. Both outputs must be appended inside the card.
- You used a copywriter, naturalizer, or enrichment artifact without first checking that it exists on disk.
- You exceeded 6 concurrent agent dispatches in a single wave (Phase 2 uses 5 subagents; that fits in one wave).
- You dispatched an enrichment subagent without first reading its existing-card-data block from `card_parsed.json`. Subagents must be told what is ALREADY known so they can hunt for gaps, not duplicate findings.
- You added a `## Outreach Letters` or `## Deeper Intelligence` section to the card without first removing the prior version (re-runs must replace, not duplicate).
- You modified the card's earlier sections (Overview, Key Contacts, Outreach Recommendation, etc.) — only the new `## Deeper Intelligence` + `## Outreach Letters` sections and their trailing footer lines are this skill's outputs.
- You wrote the rebuilt card back to `source_path` instead of `target_path = <PROJECT_ROOT>/.mz/outreach/active/<today>_<company_slug>.md`. The card must end this run at the active path with today's date prefix.
- You preserved the source file at its research-baseline or stale-active location after Phase 5 completed (a successful run leaves exactly one card for the slug, at `target_path`).
- You left multiple active files for the same slug behind — only today's-dated file should remain.
- You discarded the `## Interaction History` section (if present below the prior `## Outreach Letters` section). Interaction history is owned by `/outreach-update-card` and must be preserved verbatim.

## Verification

Before emitting `STATUS: DONE`, confirm:

1. The card now lives at `target_path = <PROJECT_ROOT>/.mz/outreach/active/<today>_<company_slug>.md`.
1. If `source_path != target_path`, the source file no longer exists.
1. `<PROJECT_ROOT>/.mz/outreach/active/` contains exactly one file matching `*_<company_slug>.md`.
1. If `enrich_mode != "skip"`, the card at `target_path` contains a `## Deeper Intelligence` section with at least one populated subsection.
1. If `enrich_mode != "only"`, the card at `target_path` contains a `## Outreach Letters` section. Every non-skipped (contact, channel) pair produced one letter under that section. Each email letter shows a `**Subject**:` line; every letter opens with a salutation and closes with a voice-adaptive gratitude sign-off (`Thanks,` / `Best regards,` / `Sincerely,`) plus the sender's first name. No letter body contains em-dashes, en-dashes, curly quotes, or the ellipsis character. When `personality_mode != "off"`, each letter carries a `*Reader calibration: ...*` provenance line and no letter names or alludes to the inferred trait. The `## Naturalization report` block does not appear under any letter in the final card.
1. The card retains its original `*Generated: <date> | Sources: <list>*` footer above the new sections.
1. New footers sit at the bottom of each new section: `*Deeper intelligence: <date> | subagents: <N> | failed: <M>*` and `*Letters generated: <date> | naturalized: yes | light queries: <K> | reverted: <R>*`.
1. Section order on the card is: original sections → `## Deeper Intelligence` (if present) → `## Outreach Letters` (if present) → `## Interaction History` (if it existed before).

## References

- `${CLAUDE_SKILL_DIR}/references/argument-parsing.md`: the `$ARGUMENTS` variables and the Source resolution rules that turn `user_path` into `company_slug` and `source_path`. Read it in full at Phase 0.
- `${CLAUDE_SKILL_DIR}/references/directory-structure.md`: where state, the card snapshot, enrichment artifacts, briefs, profiles and drafts live, the card lifecycle, and the `task_name` and `<run_dir>` rules. Read it in full at Phase 0.
- `${CLAUDE_SKILL_DIR}/references/verification-summary.md`: the final verification block and the `STATUS` rule. Read it in full at Phase 6.

## Resume Support

Before creating anything in Phase 0, run the resume check in `phases/parse_card.md` (section Resume Support); it maps the `Phase` value in `state.md` to the phase to resume from.

## Error Handling

- User path missing or no source can be resolved (user path does not exist AND no matching active card found) → `STATUS: BLOCKED`. Surface the failing check.
- `strategy.json` missing → fall back to default sender voice; final STATUS becomes `DONE_WITH_CONCERNS`; the verification block names the absence.
- Light-pass cap hit (6 calls) → drop the lowest-priority queries; record the drop in `state.md` and the final footer.
- One enrichment subagent in Phase 2 returns `BLOCKED` or `NEEDS_CONTEXT` → continue the wave for other subagents; mark the corresponding subsection as `unavailable` in the `## Deeper Intelligence` block; final STATUS becomes `DONE_WITH_CONCERNS`. Do not auto-retry.
- All five enrichment subagents fail → still emit the `## Deeper Intelligence` section with each subsection marked `unavailable: <reason>` so the failure is visible in the card; downgrade STATUS to `DONE_WITH_CONCERNS`.
- One `expert-copywriter` dispatch returns `BLOCKED` or `NEEDS_CONTEXT` → continue the wave for other contacts; mark this contact `failed_draft` in `state.md`; the contact appears as `### Skipped: <Name> — <reason>` under the card section; final STATUS becomes `DONE_WITH_CONCERNS`. Do not auto-retry — the failure reason must surface to the user.
- One `expert-naturalizer` dispatch over-shortens a draft (post-validation finds word count outside channel budget by >5% or subject line drifted) → restore the pre-naturalize snapshot; mark `naturalize_reverted` in `state.md`; the pre-naturalize draft is what gets appended; final STATUS becomes `DONE_WITH_CONCERNS`.
- Card has no Key Contacts at all AND `enrich_mode != "only"` → `STATUS: BLOCKED` with message "card has no Key Contacts — re-run /outreach-research or hand-edit the card first, or run with enrich:only to skip letters."
- Any agent run more than once with `NEEDS_CONTEXT` → escalate via `AskUserQuestion` with the agent's stated missing piece. Otherwise no user prompts.
- Source-file deletion fails during Phase 5 cleanup (permission, file vanished, fs error) → do not fail the run; log `relocation_cleanup_failed: <reason>` in `state.md`; downgrade final STATUS to `DONE_WITH_CONCERNS`. The card content at `target_path` is canonical regardless; the user can clean up the stale source manually.
- `.mz/outreach/active/` is unwritable (permission, read-only mount) → `STATUS: BLOCKED`. The skill cannot complete without writing the activated card.
- Never fabricate contacts, hooks, news items, metrics, or any other content. Incomplete output is better than fabricated content.
