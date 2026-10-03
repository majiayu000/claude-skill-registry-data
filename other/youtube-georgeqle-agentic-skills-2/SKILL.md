---
name: youtube
description: Intent-based router and play composer for youtube-ops skills — classifies what the user needs and recommends a single skill or queues a multi-step play for /exec
type: router
version: v0.4
argument-hint: "[natural language] | --health <channel> | --concept \"<idea>\" [--channel <slug>] | --launch <unlisted-video-url> | --intel <video-urls...> | --meta <channel> | --status"
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json` `enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# YouTube — Intent Router & Play Composer

Invoke as `/youtube`.

Entry point for the `youtube-ops` pack. Classifies the user's intent and either recommends a single skill or composes a multi-step "play" written to `tasks/todo.md` for `/exec` to drive.

This skill does not produce research artifacts or alignment pages. It is a routing and planning layer over the 15 standalone youtube-ops skills (plus `youtube-format-research` from the `remotion` pack when installed).

## Modes

### Mode A — Intent Router (default)

When invoked with natural language and no flags, classify the user's intent against the table below. Recommend 1–3 skills inline with a one-sentence rationale per skill. Do not write files. If the intent maps cleanly to a play (Modes B–E) or the meta route (Mode G), suggest the corresponding flag instead.

| Intent | Signal Words | Routes To |
|--------|-------------|-----------|
| Channel health | "audit", "how is my channel", channel URL | `/youtube-channel-audit` or suggest `--health` play |
| Video diagnosis | "why did this video", single video URL | `/youtube-video-audit` |
| Prelaunch review | "unlisted", "pre-release", "prelaunch", "ready to publish", "needs editing", "launch strategy", single unlisted video URL | `/youtube-video-prelaunch-audit` |
| Video understanding | "watch this", "summarize", external URL | `/youtube-vid-research` |
| Concept validation | "should I make", "video idea" | `/youtube-concept-research` or suggest `--concept` play |
| Competitive analysis | "why did their video", "competitor" | `/youtube-competitive-research` |
| Derivative slate planning | "clips", "Shorts from this video", "derivative cuts", "repurpose long video", "publish sequence" | `/youtube-derivative-cuts` |
| Packaging | "title", "thumbnail", "CTR" | `/youtube-title-thumbnail-audit` |
| Description/SEO | "description", "tags", "metadata" | `/youtube-description-optimizer` |
| Search opportunity | "search", "keywords", "ranking" | `/youtube-search-positioning` |
| Cadence | "cadence", "how often", "schedule" | `/youtube-cadence-diagnosis` |
| Peer comparison | "compare", "benchmark", "peers" | `/youtube-peer-benchmark` |
| Meta research | "current meta", "what is working now", "find opportunities for @channel", "breakout patterns", "exploit", "avoid", "counter-position" | `/youtube-meta-research` or suggest `--meta` |
| Portfolio | "portfolio", "content mix" | `/youtube-portfolio` |
| General audit | "full audit", "everything" | `/youtube-audit` |
| Format/production | "format", "editing", "pacing" | `/youtube-format-research` (remotion pack) |

When routing to `youtube-format-research`, verify the `remotion` pack is enabled in `.agents/project.json` `enabled_packs`. If not, note that `npx skillpacks install remotion` is required first.

### Mode B — Channel Health Play (`--health <channel>`)

Queue a 5-step channel health audit play to `tasks/todo.md`:

1. `/youtube-channel-audit <channel> --count 20`
2. `/youtube-portfolio`
3. `/youtube-peer-benchmark <channel>`
4. `/youtube-cadence-diagnosis <channel>`
5. `/youtube-title-thumbnail-audit <channel>`

### Mode C — Pre-Production Play (`--concept "<idea>" [--channel <slug>]`)

Queue a concept validation play to `tasks/todo.md`:

1. `/youtube-concept-research "<idea>" [--channel <slug>]`
2. `/youtube-competitive-research` (using comparables surfaced in step 1)
3. `/youtube-search-positioning`
4. `/youtube-format-research` (only if `remotion` pack is enabled — mark optional if missing)

### Mode D — Video Launch Play (`--launch <unlisted-video-url>`)

Queue a launch preparation play for an unlisted or scheduled video to `tasks/todo.md`. If the video is already public and the user asks why it performed a certain way, recommend `/youtube-video-audit` instead.

1. `/youtube-video-prelaunch-audit <video-url>`
2. `/youtube-title-thumbnail-audit`
3. `/youtube-description-optimizer <video-url> --mode draft`

### Mode E — Competitive Intel Play (`--intel <video-urls...>`)

Queue a competitive analysis play to `tasks/todo.md`:

1. `/youtube-vid-research <video-urls>`
2. `/youtube-competitive-research <video-urls>`
3. `/youtube-format-research` (only if `remotion` pack is enabled — mark optional if missing)

### Mode F — Status (`--status`)

Read-only scan of `research/youtube/` artifacts. Report:

- Which research files exist and their last-modified dates
- Staleness (files older than 30 days)
- Coverage gaps (which skills have never produced output)
- Any active working packets in `research/youtube/_working/`

Do not write files in this mode.

### Mode G — Meta Research (`--meta <channel>`)

Recommend `/youtube-meta-research <channel>` for current public YouTube meta analysis around the target channel. Use this when the user asks what is working now, what the channel should exploit or avoid, which breakout patterns matter, or how to counter-position against visible peer/search surfaces.

If the user explicitly asks to queue a meta research play, use the Play Approval Gate before writing to `tasks/todo.md`:

1. `/youtube-meta-research <channel>`
2. `/youtube-search-positioning <channel>` (optional follow-up when the meta report identifies query-dependent opportunities)
3. `/content-programming` (only if `creator-foundation` is enabled; otherwise note that `npx skillpacks install creator-foundation` is required first)

## Play Approval Gate

Before writing a play to `tasks/todo.md`:

1. **Check for existing work.** Read `tasks/todo.md`. If it contains unfinished items (unchecked checkboxes), warn the user and ask whether to append, replace, or abort. Do not silently overwrite existing plans.
2. **Present the play.** Show the numbered steps with skill names and arguments. Note any optional steps and their prerequisites (e.g., remotion pack).
3. **Write on approval.** Write the play to `tasks/todo.md` as a checklist. Include a header line identifying the play type and timestamp. Each step is a `- [ ]` item with the full skill invocation command.

After writing the play, recommend the approved task artifact route to begin execution.

## Play Format for `tasks/todo.md`

```markdown
## YouTube Play: {Play Type} — {timestamp}

- [ ] Step 1: `/<skill-name> <args>`
- [ ] Step 2: `/<skill-name> <args>`
...
```

## Approved Artifact Handoff

After an approved play write or any direct artifact mutation:

- List every created or updated synthesized artifact path, including `tasks/todo.md` when a play was written.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only routing artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.

## Intent-Aware Routing

Before applying the default next-step routing or writing a queued play, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, prelaunch review, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, owner-analytics export, or post-publication video audit work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Next-Step Routing

When Mode A recommends skills without writing files, the recommended next step is the selected youtube-ops skill or pack installation command shown in the routing response.

After Mode B-E or an explicitly queued Mode G play writes an approved play to `tasks/todo.md`, recommend `Recommended next route: approved task artifact` to begin execution. If play writing is blocked by existing unfinished tasks, the next step is the user's append, replace, or abort decision.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
