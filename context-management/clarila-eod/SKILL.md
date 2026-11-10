---
name: clarila-eod
description: "Write HeyAmara end-of-day reports, Discord EODs, standups, or daily updates from verified work evidence. Supports requested dates and separate, connected reports for consecutive days. Produces one near-limit Discord Nitro message per day in the user's lowercase voice. Not for session handoffs, generic weekly or quarterly summaries, single PR lookups, or standalone news."
metadata:
  version: "1.1"
---

# EOD - HeyAmara Daily Report

Write as the user. Default to HeyAmara work only, one separate Discord message
per requested day, and useful detail close to Nitro's 4,000-character limit.
Discord is a paste destination only; never read it as a source or send the
report without explicit authorization.

## Defaults Established by the User

- Include only HeyAmara work and directly related dependencies. Exclude other
  products, including Nook/Cove, unrelated teaching, and personal activity.
- Report the user's own implementation, investigation, testing, releases, and
  issue closures. Exclude other people's PRs that the user only reviewed or
  approved. Their merge does not become the user's delivery.
- Use lowercase, plain language, clear outcomes, and verifiable evidence.
  Make the work convincing through specifics, not hype or invented impact.
- No AI-news section by default. Work on HeyAmara's AI chat remains relevant.
- No clock times, elapsed-time descriptions, or activity labels such as
  "today", "yesterday", "morning", "afternoon", "evening", or "overnight".
  Use the date heading and the required
  "tomorrow" heading to identify the report and its next steps.
- Allow useful sections such as "released:", "done:", "verified:", and
  "issues i closed:". Bullets and short paragraphs are allowed.
- Each day has its own "tomorrow" section. Connect consecutive reports:
  the earlier day's next steps lead into the following day's actual progress.
  Carry unfinished work forward without claiming completion.
- Aim as close to 4,000 characters as the verified evidence allows. For detailed
  reports, target 3,950-4,000 total characters per message, including full URLs,
  Markdown, whitespace, and any copied code fences. Include remaining useful
  verified details before finalizing. Never exceed 4,000, pad, repeat facts, or
  invent work to fill the allowance. An explicitly requested quick report may
  be short.
- Explicit user changes to scope, format, or length override these defaults.

## Modes and Dates

| Request | Behavior |
|---|---|
| "write my eod", "standup", "wrap up today" | Report the current client-local day. |
| "eod for monday and tuesday" | Resolve the requested dates and write one separate report for each. |
| "eod quick" | Use sessions, conversation, local git, GitHub, and memory; skip mail/calendar. |
| "eod sources" | Diagnose source coverage and gaps; do not compose the EOD. |
| "eod rewrite" | Improve supplied notes; verify their GitHub and delivery claims. |

A request for separate daily EODs across a week is supported. A generic weekly
or quarterly narrative is outside this skill.

Use the conversation's date/timezone ahead of the execution host. Set EOD_TZ
to the user's timezone and EOD_DATE to each report's YYYY-MM-DD date before
running collectors. An explicit user timezone takes precedence. Query each
local day as an inclusive start and exclusive next-day start; midnight work
belongs to its local day. Times stay in working notes, not the EOD prose.

## Gather and Verify

Read only the references needed for the selected mode:

| Reference | Use |
|---|---|
| [sources](references/sources.md) | Collection, scope filtering, merge rules |
| [agent sessions](references/source-codex.md) | Available Codex/ChatGPT and Claude records |
| [local git](references/source-local-git.md) | Own commits, worktrees, uncommitted changes |
| [GitHub](references/source-github.md) | PR ownership, closure actors, current state and checks |
| [mail/calendar](references/source-mail-calendar.md) | HeyAmara release and team context |
| [memory](references/source-memory.md) | Locate prior decisions, then verify them |
| [composition](references/composition.md) | Sections, readability, continuity, character budget |
| [example](references/example.md) | Connected daily reports |
| [working notes](references/working-notes.md) | Evidence records and output files |
| [optional news](references/source-ai-news.md) | Only when the user explicitly requests news |

Collect available sources independently, then filter to HeyAmara and the
requested dates before drafting. Recover relevant sessions that span midnight;
deduplicate handoffs, subagent summaries, and copied transcripts.

GitHub is the authority for current PR/issue state. Verify authored PRs and
every referenced issue. A claim that the user closed an issue requires the
closure actor and local closure date, not merely a closed badge, assignment,
notification, or related merge. When requested, list all personal closures
once, with repository, number, short description, and disposition. Distinguish
new fixes, verified existing fixes, and unresolved issues tracked upstream.

Check relevant EAS builds, submissions, OTA updates, store availability,
Sentry incidents, CI, and deployment records when available. Keep these states
distinct: local, committed, pushed, checks passed, build finished, submitted,
available to testers, deployed, and device/provider verified. Record unavailable
sources and uncertain evidence; never imply live verification that did not occur.

## Compose and Deliver

Use a "released:" section when actual delivery is verified. Include the mobile
version, build number, destination, and relevant OTA/deployment details. Do not
put merely prepared fixes or completed cloud builds there.

In "done:", explain the problem, resulting behavior, and practical value.
Put substantial test evidence in "verified:" when it improves scanning.
State the purpose of UI work and whether it is local or released. Avoid
implementation detail that does not help readers understand the contribution.

Use "tomorrow" for concrete next steps and continuing work. A plan supplied
for the day following Tuesday belongs in Tuesday's "tomorrow" section; do not
turn it into a separate Wednesday EOD unless requested.

Use masked Markdown links for work references. Count their complete URLs,
not just visible labels. Save one file per date, plus a fenced bundle if useful,
and run:

```bash
EOD_SKILL_DIR="${EOD_SKILL_DIR:-$HOME/.agents/skills/clarila-eod}"
EOD_DATE=2026-10-12 EOD_TZ=Asia/Jakarta "$EOD_SKILL_DIR/scripts/eod-date.sh" --json
"$EOD_SKILL_DIR/scripts/eod-lint.sh" work/eod/2026-10-12.txt
"$EOD_SKILL_DIR/scripts/eod-lint.sh" work/eod/messages.txt
```

The linter validates each message independently. Verify semantic ownership,
release claims, project relevance, and day-to-day continuity against the sources.

For normal report modes, deliver only one copyable txt block per day in date
order. Never combine several days into one Discord message. Do not add a
preamble, closing notes, or source-gathering narration to the copyable reports.

## Configuration and Validation

For substantive work, follow the current owner's [pinned poteto-mode workflow](../clarila/references/pstack.md) and its actual applicable procedures. A delegated report stage stays within that owner and scope. The explicit report source, voice, date, length and copyable-output requirements above remain the owner's format contract; procedural defaults do not add engineering publication or unrelated work.

Defaults can be overridden for a different explicitly requested scope:
EOD_GH_ORG defaults to Hey-Amara; EOD_DEV_ROOT defaults to
$HOME/Developer/heyamara. Extra collector owners or folders are candidate
sources, not automatic permission to include unrelated projects.

Validate changes with the tests under tests/ and the skill-creator validator.
Routing cases live in evals/evals.json; update them when discovery behavior changes.
