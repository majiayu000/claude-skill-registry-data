---
name: daily-standup-prep
category: scrum-sprint
description: >
  Generate a per-team standup report from recent Jira, GitLab, Confluence, and Git activity,
  written into the Obsidian vault. Use when the user says "daily standup prep", "standup
  report", "generate standup", "scrum prep", or invokes /daily-standup-prep.
codex-short-description: "Per-team standup report from Jira, GitLab, Confluence, and Git activity"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
  - Skill
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_get_issue
  - mcp__atlassian__jira_get_changelog
  - mcp__atlassian__jira_get_comments
  - mcp__atlassian__confluence_search
  - mcp__atlassian__confluence_get_page
  - mcp__gitlab-mcp__list_merge_requests
  - mcp__gitlab-mcp__mr_discussions
  - mcp__gitlab-mcp__list_pipelines
  - mcp__gitlab-mcp__get_pipeline
  - mcp__gitlab-mcp__list_group_projects
related-skills:
  - sprint-snapshot
  - clarity-council
loop-eligible: true
recurrence-hint: daily

compatibility: claude-code codex opencode
---
# Daily Standup Prep

Per-team standup report. Read-only across Jira, GitLab, Confluence, and Git. Writes one markdown file per team to the Obsidian vault.

This skill is a Claude Code port of `D:\powershell-scripting\src\bin\Get-Standup-Report.ps1` — same inputs, same template placeholders, same output path layout, same identity-matching rules. See [REFERENCE.md](REFERENCE.md) for the algorithm and per-section formatter contracts. See [EXAMPLES.md](EXAMPLES.md) for invocation parity with the PS script.

## Quick start

```text
/daily-standup-prep                                 → Pyrite, last 2 days, INC 25 / Sprint 1
/daily-standup-prep Onyx                            → single team
/daily-standup-prep Pyrite,Onyx --days 3 --inc 26   → multi-team, custom window
/daily-standup-prep --no-gitlab --no-confluence     → toggle sections off
```

## Parameters

| Param | Default | Maps to PS |
| :--- | :--- | :--- |
| `Teams` | `["Pyrite"]` | `-Teams` (string[]) |
| `DaysToLookBack` | `2` | `-DaysToLookBack` |
| `JQL` | auto-built | `-JQL` |
| `GitRepoPath` | `D:\paas\` | `-GitRepoPath` |
| `Inc` | `25` | `-Inc` |
| `Sprint` | `1` | `-Sprint` |
| `IncludeJiraIssues` / `IncludeGitCommits` / `IncludeGitLabActivity` / `IncludeConfluenceActivity` / `IncludeKanbanDiagram` / `IncludeStandupOrder` | all `true` | same |
| `IncludeSprintPulse` | `true` | new — runs Phase 4.5 (daily snapshot + council burndown/forecast/suggestions). Toggle off with `--no-sprint-pulse` |

JIRA base, Confluence base, GitLab base + group, vault root, and template path are all **resolved from memory** — never accept them as args. See *Config resolution* below.

## Config resolution (run once at the start of every invocation)

| Placeholder | Memory file | Default content / how to populate |
| :--- | :--- | :--- |
| `{{vault_root}}` | `reference_obsidian_vault.md` (`**Vault root:**` line) | `C:\Users\chris.adams\dev\gd-pkms\` — already populated |
| `{{jira_project}}` | `reference_jira_default_project.md` (`**Default Jira project key:**` line) | `PRJ` — already populated |
| `{{confluence_space}}` | `reference_confluence_default_space.md` | `PP` — already populated |
| `{{template_path}}` | derived | `{{vault_root}}\🗃Templates\Standup.md` (no separate memory) |
| `{{rosters_dir}}` | derived | `{{vault_root}}\Scrum Teams\_rosters\` |
| `{{output_root}}` | derived | `{{vault_root}}\Scrum Teams\` (per-team subfolder appended later) |

If a memory file is missing or its value is `<unset>`, **prompt once via `AskUserQuestion`** with the PS-script default as the recommended option, then write the answer back so the next run skips the prompt. Same pattern as `daily-briefing`.

## Roster bootstrap (first-run only)

The PS script reads `D:\powershell-scripting\src\bin\Teams\<Team>.csv`. We move ownership of those CSVs into the vault so the user maintains them in one place going forward.

For each team in the run:

1. Look for `{{rosters_dir}}\<Team>.csv` (case-insensitive). If present, use it.
2. If missing **and** `D:\powershell-scripting\src\bin\Teams\<Team>.csv` exists, prompt via `AskUserQuestion`:
   *"No roster found at `{{rosters_dir}}\<Team>.csv`. Copy from the powershell-scripting repo?"* — options: `Copy (recommended)`, `Use repo path this run only`, `Skip team`.
3. On `Copy`: `mkdir -p "{{rosters_dir}}"`, then copy the file. Tell the user the new path is the canonical location going forward.
4. If neither path exists, skip the team and warn — do not invent a roster.

CSV format is the same headerless layout the PS Team-Helpers module uses: `FullName,Email,Alias,Role,Flags`. Lines starting with `//` and blanks are ignored. `Alias` and `Flags` accept `;`-separated values. See [REFERENCE.md](REFERENCE.md#roster-csv-schema).

## Workflow (per team)

Loop the steps below for each team in `Teams`. Each iteration is independent — one file per team, matching the PS script's `$teamsToProcess | ForEach-Object` block.

```text
Per-team progress:
- [ ] Phase 1: Resolve config + load roster
- [ ] Phase 2: Compute window + auto-build JQL
- [ ] Phase 3: Gather data (Jira, Git, GitLab, Confluence) — parallel
- [ ] Phase 4: Match activity to team members + flag HasActivity
- [ ] Phase 4.5: Sprint pulse — daily snapshot + council (burndown / forecast / suggestions)
- [ ] Phase 5: Render section markdown + Mermaid kanban + talking order
- [ ] Phase 6: Substitute template placeholders + write to vault
- [ ] Phase 7: Console summary
```

### Phase 1 — Config + roster

Resolve every `{{placeholder}}` per the table above. Load the roster CSV into a list of `{FullName, FirstName, LastName, JiraName, Email, Alias[], DisplayFirstName, Role, Flags[]}` records — derive `JiraName = "{Last}, {First}"` and `DisplayFirstName = Alias[0] ?? FirstName`. Tag each member with `HasActivity = false` and empty `Issues / Commits / GitLabActivities / ConfluenceActivities` lists.

### Phase 2 — Window + JQL

- `activity_since` = midnight (Pittsburgh local) `DaysToLookBack` days ago.
- `since_iso` = `YYYY-MM-DDTHH:mm:ssZ` for GitLab/Confluence cutoffs.
- `since_date` = `YYYY-MM-DD` for `git log --since`.
- If `JQL` arg is empty: build `project = {{jira_project}} AND updated >= startOfDay(-{N}d)` where `N = DaysToLookBack`.

State the chosen window in one short sentence: *"Gathering Pyrite standup for window 2026-05-11 → 2026-05-13 (2-day lookback)."*

### Phase 3 — Gather data (parallel)

Issue these MCP/Bash calls in a single response when section toggles allow:

- **Jira issues** (`IncludeJiraIssues` or `IncludeKanbanDiagram`): `jira_search(jql=<jql>, fields="summary,status,assignee,issuetype,updated")` with pagination to a sane cap. For each result, follow up with `jira_get_changelog` and `jira_get_comments` only when the issue's `updated` is within the window — skip the fetch otherwise to save tokens.
- **Jira kanban** (`IncludeKanbanDiagram` only): second `jira_search` with `project = {{jira_project}} AND sprint in openSprints() AND labels in ({lowercase team names})`. Capture `key, summary, status, assignee.displayName, issuetype.name`.
- **GitLab MRs + discussions** (`IncludeGitLabActivity`):
  1. `list_group_projects(group_id="{{gitlab.XXXX}}")` to get all project IDs in the group (subgroups included).
  2. For each project: `list_merge_requests(project_id, updated_after=<since_iso>, per_page=100)`.
  3. For each MR: `mr_discussions(project_id, merge_request_iid)` capped at 100 notes.
- **GitLab pipelines** (`IncludeGitLabActivity`): for each project, `list_pipelines(project_id, updated_after=<since_iso>, per_page=100)`. For each, `get_pipeline(project_id, pipeline_id)` to read the triggering user.
- **Confluence pages** (`IncludeConfluenceActivity`): `confluence_search(cql="lastModified >= '{since_date}' AND space = {{confluence_space}}")`. For each, `confluence_get_page(page_id, expand="history.lastUpdated,version,space,body.view")`.
- **Git commits** (`IncludeGitCommits`): Bash sequence — confirm `{{git_repo}}\.git` exists; `git -C "{{git_repo}}" fetch --all`; `git -C "{{git_repo}}" log --all --since="{since_date}" --pretty=format:"%H|%an|%ae|%aI|%s"`. Parse pipe-delimited lines.

If any external system fails to respond, log a warning and continue with empty results for that section — never fabricate. If `IncludeKanbanDiagram` is on but Jira fails, render `_No kanban data — Jira unavailable._` rather than skipping the placeholder.

### Phase 4 — Match activity to team members

Use the cascading 8-strategy matcher described in [REFERENCE.md](REFERENCE.md#identity-matching-cascade). For every activity record, attempt to match by `(email, displayName, username)` — Jira gives email + displayName; GitLab gives email + name + username; Confluence gives email + displayName; Git gives email + author name only.

Filter rules:

- **Jira issue inclusion** — keep an issue iff its assignee matches a team member **OR** any comment/changelog entry within the window was authored by a team member. (Direct port of the PS `$isAssignedToTeamMember -or $hasRecentActivity` filter.)
- **Git/GitLab/Confluence inclusion** — keep an activity iff its author matches a team member.
- Set `member.HasActivity = true` for any matched member, and append the activity to the member's `Issues / Commits / GitLabActivities / ConfluenceActivities` lists for the talking-order/per-member sections.

### Phase 4.5 — Sprint pulse (daily snapshot + council)

Skip if `IncludeSprintPulse` is off (substitute empty strings for the three pulse placeholders).
Otherwise follow [PULSE.md](PULSE.md): run `sprint-snapshot --phase daily`, read the sprint's
`_snapshots.jsonl`, and have `clarity-council` (infographics-expert + statistics-expert + scrum-master)
produce `{{burndown_chart}}` (burn-up chart per the contract there), `{{forecast_note}}`, and
`{{scrum_suggestions}}`. Never fabricate trend data; on snapshot failure render the unavailable note.

### Phase 5 — Render sections

Each placeholder in the template gets a string built from the matched data. Formatter contracts (exact markdown shape) live in [REFERENCE.md](REFERENCE.md#section-formatters):

- `{{talking_order}}` — randomized active members (`✅`) first, inactive (`🧽`) last. Each line `- [ ] [[@First Last]] - ✅` (or `🧽`). Multi-team runs append ` (TeamName)` after the wikilink. If `IncludeStandupOrder` is off, leave the placeholder empty.
- `{{jira_state}}` — Mermaid `flowchart` with five status columns (Blocked / Ready / In Progress / In Review / Done). Spec in [REFERENCE.md](REFERENCE.md#mermaid-kanban-spec). If `IncludeKanbanDiagram` is off, empty.
- `{{jira_issues}}` — per-issue blocks with `### KEY - Summary`, type/status/assignee line, then a bulleted activity log of `(date) WHO / WHAT / WHY` plus `text` code fences for details.
- `{{git_updates}}` — per-member blocks `### [[@First Last]]` then `- (date) `hash7` - message` lines, sorted desc by date.
- `{{gitlab_updates}}` — three subsections (`## Merge Request Activity`, `## Comment Activity`, `## Pipeline Activity`) only if non-empty; otherwise the placeholder line `_No GitLab activity found in the specified time period._`.
- `{{confluence_updates}}` — per-page blocks with title + space tag, type/last-modified/author line, link, and a content snippet (first 200 chars of stripped HTML in a `text` code fence).

### Phase 6 — Substitute and write

1. `Read` `{{template_path}}`. The template is the user's master Standup template — never modify it.
2. Replace placeholders **in this exact set** (matches the PS `ConvertTo-TemplateMarkdown` function plus the three Phase 4.5 additions): `{{date}}`, `{{team}}`, `{{sprint}}`, `{{increment}}`, `{{talking_order}}`, `{{jira_state}}`, `{{jira_issues}}`, `{{git_updates}}`, `{{confluence_updates}}`, `{{gitlab_updates}}`, `{{burndown_chart}}`, `{{forecast_note}}`, `{{scrum_suggestions}}`. Date format `YYYY-MM-DD` (Pittsburgh local). Team name written **TitleCase** (first char upper, rest lower) to match the PS `$formattedTeam` line. The three pulse placeholders are no-ops if the user's template doesn't reference them — the substitution still runs cleanly. Note this once when a template lacks them so the user knows to add them if they want the pulse rendered (e.g. under a `## Sprint Pulse` heading containing `{{burndown_chart}}`, then `### Forecast` `{{forecast_note}}`, then `### Suggestions` `{{scrum_suggestions}}`).
3. Compute output path: `{{vault_root}}\Scrum Teams\<TeamTitleCase>\Scrum 📅\INC {Inc}\Sprint {Sprint}\YYYY-MM-DD.md` — note the `📅` emoji is preserved literally; forward slashes work fine in bash on Windows.
4. `mkdir -p` the parent directory.
5. **Never overwrite silently.** If the file exists, `Read` it, then `AskUserQuestion`: `Overwrite` / `Append as ## Re-run HH:MM section` / `Skip save`.
6. `Write` the file. Print the saved path back as a clickable markdown link.

**Sibling-skill delegation in Phase 4.5 / Phase 6:**

- The daily snapshot is **always delegated to `sprint-snapshot` via `Skill`** with `--phase "daily"`. Never reimplement Jira sprint fetching inline — `sprint-snapshot` owns the JQL, identity matching, capacity math, and the JSONL trend schema. If its phase derivation logic doesn't recognize `daily`, pass it through as an explicit `--phase` override (the skill already supports arbitrary phase strings via that flag).
- The pulse council is **always delegated to `clarity-council` via `Skill`** with personas pinned to `infographics-expert + statistics-expert + scrum-master`. Do not author burndown SVG/Mermaid, forecast paragraphs, or suggestions inline — let each persona produce its own artifact under its own constraints.

- If extending the template with new Obsidian Flavored Markdown constructs (callouts, embeds, dataview, block IDs, frontmatter properties beyond `Increment/Sprint/Date`), invoke **`obsidian-markdown`** via `Skill` rather than authoring the syntax inline — it's the canonical reference and stays in sync with vault conventions.
- For **wikilink target verification** (the `[[@First Last]]` rule in talking_order / git_updates), prefer delegating the lookup to **`obsidian-vault`** if the run will need to verify many person notes — its search is more efficient than repeated `Glob` calls. For a single team run (≤15 lookups) the inline `Glob` is fine.
- If the user later wants a **dashboard `.base` file** that aggregates team standups (e.g. "all standups for Pyrite this sprint"), invoke **`obsidian-bases`** rather than hand-authoring the YAML.
- For **CLI-driven vault inspection** (e.g. checking note frontmatter, running a vault-wide property query before deciding whether to overwrite), invoke **`obsidian-cli`** — it has direct property/task access that `Read`+`Glob` cannot replicate cheaply.

### Phase 7 — Console summary

Print a brief block per team (matches the PS `=== REPORT GENERATION SUMMARY ===` block):

```
=== <Team> standup report ===
Team members loaded: N
Jira issues included: N (of M scanned)
Git commits matched: N
GitLab activities matched: N
Confluence activities matched: N
Sprint pulse: snapshot=<ok|failed|skipped> · trend rows=N · council=<ok|failed|skipped>
Saved: <markdown link>
```

## Rules

- **Read-only across Jira, GitLab, Confluence.** Never transition issues, post comments, approve MRs, edit pages, or modify any external state.
- **Read-only on the Git repo.** `fetch` and `log` only — never checkout, pull, or merge.
- **No vault writes outside `Scrum Teams/`.** The template at `🗃Templates/Standup.md` is read-only too.
- **Never overwrite an existing standup file silently.** Always confirm via `AskUserQuestion`.
- **Confirm before persisting to memory.** When populating an `<unset>` value (GitLab base URL, etc.), use the PS-script default as the recommended option but let the user override before writing.
- **Wikilinks for team members only when the vault person note exists.** Use `Glob("{{vault_root}}/🤼 Team/**/@*.md")` to verify before writing `[[@First Last]]`. If the vault has no canonical note for a roster member, render plain text — don't pollute the graph with broken links.
- **TitleCase team names in output.** `pyrite` → `Pyrite` (first char upper, rest lower) — matches the PS `$formattedTeam` line so vault paths and frontmatter stay consistent.
- **Pittsburgh local time.** All `Date` columns and the filename use America/New_York. The `git log` `%aI` and ISO timestamps from Jira/GitLab/Confluence are converted before display.
- **Section toggle semantics match the PS script.** Skipping a section (e.g., `--no-gitlab`) means: don't gather, don't fetch, and substitute an empty string for the placeholder — the template still resolves cleanly.
- **No fabricated data.** If an MCP fails, surface the failure in the console summary and put a `_<system> unavailable_` note in the corresponding section. Do not invent.
- **Sprint pulse is delegated, never inlined.** The `daily` snapshot must come from `sprint-snapshot` and the burndown/forecast/suggestions must come from `clarity-council`'s three pinned personas. Do not author burndown charts, forecasts, or scrum-master suggestions inline — that bypasses the persona constraints (infographics-expert's chartjunk rules, statistics-expert's confidence-band requirement, etc.) that make these artifacts trustworthy.
- **Burndown trend data is read-only and append-only.** Phase 4.5 reads `_snapshots.jsonl` to feed the chart but never edits past rows. Past `daily.canvas` / `daily.md` are allowed to be overwritten — the trend record lives in the JSONL.

## Edge cases

- **No team members loaded** — warn and skip the team. Don't render an empty report (matches PS `if ($teamMembers.Count -eq 0)` guard).
- **Roster CSV missing for one of N teams** — process the others; warn for the missing one.
- **Vault `🤼 Team` folder doesn't have a `@First Last.md` note for a roster member** — render plain `First Last` instead of a wikilink in `{{talking_order}}` and `{{git_updates}}`.
- **Git repo not present at `{{git_repo}}`** — skip git commit collection silently; render an empty `{{git_updates}}` section.
- **Jira sprint label missing** for the team (kanban query returns 0) — render `_No <Team> items found in current sprint._` for `{{jira_state}}`.
- **GitLab group returns 0 projects** — surface a warning; the user may have lost group membership. Render `_No GitLab activity found in the specified time period._`.
- **Re-run on the same day** — same overwrite/append/skip prompt as `daily-briefing`.
- **Multi-team run, partial failure** — generate reports for the teams that succeeded; surface per-team status in the final summary block.
- **Sprint pulse with no prior snapshots** — first daily run of a sprint will only have one trend row after Step 1 writes it. Render the burndown as a single point with a one-line caption (e.g. `_First daily snapshot of Sprint N — trend will fill in over coming days._`) and let the statistics-expert flag the data as too sparse to forecast.
- **Sprint config note missing** — `sprint-snapshot` will prompt to create one. If the user declines, skip the entire pulse phase rather than half-rendering it.

## Related skills

This skill writes into and reads from the user's Obsidian vault. When any vault-related extension or refinement is needed, **delegate to the relevant `obsidian-*` skill via `Skill`** rather than reimplementing — they are the canonical references for vault conventions and stay in sync with Obsidian feature changes.

| Skill | Use it for |
| :--- | :--- |
| `daily-briefing` | Personal (Outlook-driven) morning prep. Sibling skill — both can run on the same morning. Same `{{vault_root}}` resolution pattern. |
| `sprint-snapshot` | **Owns the daily snapshot in Phase 4.5.** Always invoke via `Skill` with `--phase "daily"`; never reimplement Jira sprint fetching, identity matching, or the JSONL trend schema inline. The `_snapshots.jsonl` it writes is the burndown's data source. |
| `clarity-council` | **Owns the pulse council in Phase 4.5.** Always invoke with the three pinned personas (`infographics-expert`, `statistics-expert`, `scrum-master`). Lets each persona enforce its own constraints on the burndown chart, forecast, and suggestions. |
| `issue-suggest-component` | Pattern reference for memory-driven default Jira project + bulk `AskUserQuestion` pacing if the multi-team loop ever grows beyond a handful of teams. |
| `issue-feature-breakdown` | Pattern reference for Jira+Confluence context-gathering depth. |
| `obsidian-markdown` | **Canonical reference for Obsidian Flavored Markdown.** Consult before extending the standup template with new constructs (callouts, embeds, dataview, block IDs, frontmatter properties). |
| `obsidian-vault` | Use for batch wikilink target verification, vault-wide note discovery, and managing the standup index notes. Prefer over repeated `Glob` calls when the run needs >15 lookups. |
| `obsidian-cli` | Use for property/task queries, frontmatter inspection, and any CLI-driven vault operation that `Read` + `Glob` cannot do cheaply. |
| `obsidian-bases` | Use when the user wants a dashboard `.base` file (e.g. "show me all standups for Pyrite this sprint", "which team members had no activity in the last 5 standups"). Don't hand-author `.base` YAML. |
| `obsidian-canvas` | Use if the user wants a visual board summarizing the standup (e.g. a sprint-overview canvas with linked standup notes as nodes). |

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Activity is mapped to the correct roster member from the CSV
- The Mermaid kanban renders and reflects the gathered Jira/GitLab state
- Sources cover the requested N-day window across Jira, GitLab, Confluence, and Git
- One file per team is written to the vault

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/daily-standup-prep.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
