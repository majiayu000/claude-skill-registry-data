---
name: handoff
description: Compress the current Claude Code session into a portable markdown bundle the receiver can paste into a different session (same mac, different machine, claude.ai, future-you) and resume with zero context loss. Default receiver is ZOE (the cowork bot) via Bonfire - most handoffs are Zaal moving context to ZOE so it keeps following the thread, not to another CC terminal. Default voice - the receiver is already mid-work; the bundle leads with tasks to absorb into their existing todo list, decisions/git/in-flight/cold-start map are opt-in below. Lands as research/events/session-YYYY-MM-DD-<slug>/README.md in ZAO repos, ~/.zao/handoff/<slug>/ elsewhere. Pushes summary to Bonfire (required when receiver is ZOE, best-effort otherwise). DROPS INTO THE HANDOFF INBOX by default (zao-tracker handoff) so it appears in ZOE's /cockpit with NO paste - clipboard is now opt-in. Use when the user types /handoff, says "save my context", "summarize this session", "hand this off to another terminal", "move this work elsewhere", "back to the assistant", "back to ZOE".
allowed-tools: Read Write Edit Bash Skill
---

# /handoff - session handoff bundle

Compress this Claude Code session into a single paste-anywhere markdown bundle. Receiver pastes it into a new session and resumes.

Design doc: `research/dev-workflows/755-handoff-skill-design/README.md` (in ZAO repos).

## When to fire

- User types `/handoff`
- "save my context", "summarize this session", "hand off to another terminal"
- "move this work to my other laptop", "I want to pick this up later"
- About to /clear or /compact and want a portable artifact first
- Switching to claude.ai or a different agent and need to carry context

## The 5-section bundle (this is the output shape - do not deviate)

The bundle is **recursive-friendly**: the receiver pastes the whole thing into a fresh session and the model knows exactly what to do because of the receiver preamble at the top. The receiver can ALSO `/handoff` again later, chaining bundles. Each bundle's "Previous handoffs in chain" pointer keeps the lineage traceable.

**The `chain:` field has three accepted shapes** (pick the most accurate one):
- `chain: none` - first handoff for this thread of work
- `chain: <path-to-prior-bundle>` - sequential, this bundle resumes from the named one
- `chain: sibling:<path>` - parallel session, related to but not derived from the named bundle (e.g. two terminals working different facets of the same project)

**Skip transient overlays in Section E "Skills invoked"**. List discrete `/skill` invocations only - omit startup-hook overlays (`caveman:caveman`, `superpowers:using-superpowers`) and ambient session-config skills that are always-on. They are noise in the cold-start map.

**Always append an "Inline copy-paste block" at the very bottom of the bundle** - a one-line instruction the receiver can fire instantly without scrolling through the bundle to find the path:

```
## Inline copy-paste block (for fast receiver paste)

```
Ingest the bundle at <full-path-to-this-README> and follow receiver instructions at the top. <N> tasks to absorb.
```
```

That single line is what the receiver pastes when they just want to dispatch a fresh session pointed at the bundle.

**Always surface friction-source observations** in Section B (decisions / why). When the session hit a sandbox block, an ENOSPC, a flaky API, a permissions gate, etc - document it explicitly so the next session does not re-discover it. Friction-source surfacing is the highest-value thing the bundle does. If you skip it, future sessions waste cycles re-learning what you already know.

```markdown
# Session handoff - YYYY-MM-DD HH:MM
> from <source machine + branch> -> to <receiver, default "fresh CC terminal">
> doc: <path-to-this-bundle>
> chain: <previous-handoff-path-or-none>

## Receiver instructions (read me FIRST, then do exactly this)

You just received a handoff bundle. Do NOT start work yet. Do this:

1. Read ALL sections below (A through E) before responding to anything.
2. If section C has a diff, decide: apply it (`git apply diff.patch`) or note it for later.
3. Create TaskList entries from section A. These are the "to do" items.
4. Use section B as your "why" - do NOT re-litigate decisions captured there unless new info surfaces.
5. Use section D to know what's still running (background jobs, wakeups, subagents).
6. Use section E as your cold-start map for files, skills, memory state.
7. Once integrated, message back: "Ingested handoff <slug>. <N> tasks queued. Ready."
8. If you /handoff later, your new bundle's `chain:` field points BACK to this bundle's path so the chain is traceable.

## A. Tasks to absorb (paste these into your TODO list)
- [ ] <task 1> - <one-line context>
- [ ] <task 2> - <one-line context>
- [ ] <task 3> - <one-line context>

## B. Why - decisions + pivots + ruled-out paths
- <decision 1> because <reason>. Ruled out <alternative> because <reason>.
- <decision 2> ...

## C. Git state
- Branch: `<branch>` (ahead N, behind M, dirty K files)
- Push status: `<pushed | unpushed | merged>`
- Uncommitted diff (apply with `git apply` from repo root):
  ```diff
  <unified diff>
  ```
- Untracked files: `<list>`

## D. In-flight
- Background bash jobs: <task_id - description - status>
- Subagents pending: <agent_type - task>
- Scheduled wakeups: <delaySeconds - reason>
- Open AskUserQuestion: <yes/no>

## E. Cold-start map (read if you are confused)
- Files touched this session: <relative paths + brief note>
- Skills invoked: `<skill_name>` - <count> - <last result>
- Memory writes: `<memory_slug>` - <new | updated> - <one-line>
- Last-known mental model: <2-3 sentences>
- Open questions for the receiver: <items to clarify with the user>
```

Section order is fixed: A is task-first because most receivers are mid-work and want the actionable item, not the backstory. B-E are opt-in.

## Phase 0 - Detect repo type

Run:
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/handoff-detect.sh
```

It prints one of:
- `zao` - cwd has `research/events/` and `community.config.ts` -> ZAO OS V1 repo
- `bcz` - cwd matches BCZ repos pattern
- `other-repo` - inside a git repo but not ZAO -> output goes to `<repo-root>/.handoffs/session-<slug>/`
- `no-repo` - not in a git repo -> output goes to `~/.zao/handoff/<slug>/`

Output path rule:
- `zao` -> `research/events/session-YYYY-MM-DD-<slug>/`
- `bcz` -> `<repo-root>/.handoffs/session-<slug>/` (or wherever the project keeps similar artifacts)
- `other-repo` or `no-repo` -> `~/.zao/handoff/session-<slug>/`

## Phase 1 - Gather state (mechanical, runs scripts)

### 1a. Git state
**SKIP this step if Phase 0 detected `no-repo`** - there is no git state to
gather, and `handoff-build.sh git` will hard-exit with an error outside a git
repo. Leave the bundle's git-state fields blank/omitted for a no-repo session.
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/handoff-build.sh git
```
Outputs to `/tmp/handoff-git-<pid>.txt` - branch, push status, dirty file count, unified diff (capped at 500 lines; full diff goes to a sidecar `diff.patch` if larger).

### 1b. Files touched + skills invoked + memory writes
You (the model) collect these from conversation memory. The harness does not expose a tool-call audit log, so you derive them from what you actually did this session.

Format:
- Files touched: every path you Wrote or Edited. Group by directory if many.
- Skills invoked: every `Skill` tool call by name + a one-line result note.
- Memory writes: paths under `~/.claude/projects/.../memory/` you created or edited.

### 1c. In-flight state
- Background bash jobs: review your conversation - any `run_in_background: true` Bash calls that have NOT been marked complete in a system-reminder.
- TaskList: include any tasks with status `pending` or `in_progress` (use TaskList tool if available, else recall from conversation).
- ScheduleWakeup: any pending wakeups + their fire-time + reason.
- Open AskUserQuestion: did you ask a question that has no answer yet?

## Phase 2 - Synthesize sections A + B + E (you the model write these)

These three sections are the high-value parts. Mechanical gathering can't write them - the model has to reflect on the conversation.

### Section A - Tasks to absorb (3-5 bullets, the receiver's next moves)

Sources:
- Open TaskList items (pending + in_progress)
- ScheduleWakeup prompts (literal "do this later" content)
- "TODO" / "next step" Zaal said explicitly
- Background bash jobs that haven't completed cleanly
- PRs / commits / pushes the conversation flagged but didn't execute

Voice: imperative, one-line, with a colon-prefix indicating effort if known. Examples:
- `[ ] Re-fire bonfire for the 7 May 19-23 meetings (5 min, run bash ~/.claude/skills/meeting/scripts/bonfire-episode.sh /tmp/meeting-bonfire-episodes.json)`
- `[ ] Write recap doc 754 (~30 min, transcript already at /tmp/meeting-<id>.txt)`
- `[ ] Decide PR strategy for doc 754 - same branch as M8 or its own?`

3-5 items. If more, pick the most-blocking ones. If fewer than 3 real items, that's fine - don't pad.

### Section B - Why (decisions, pivots, ruled-out paths)

This is the expensive-to-reconstruct part. Source: your conversation memory. Pull:
- Explicit decisions ("we picked X because Y")
- Pivots ("tried Z first, abandoned because W")
- Ruled-out alternatives ("considered Q but skipped because R")
- Surprising findings the receiver shouldn't have to re-discover

Voice: declarative, past-tense, named-with-reason. Example:
- "Picked single-file markdown bundle (not multi-file split) because the receiver shouldn't need to know which file to grab first - friction kills the use case."
- "Decided NOT to wrap everything-claude-code:save-session - it's generic, ZAO needs Bonfire push + cowork tracker hooks that don't fit a wrapper."

5-10 items typical. Skip the obvious; capture the non-obvious.

### Section E - Cold-start map

| Sub-field | How to fill |
|-----------|-------------|
| Files touched | List from Phase 1b. Group by topic if many. |
| Skills invoked | List from Phase 1b. |
| Memory writes | List from Phase 1b. |
| Last-known mental model | 2-3 sentences. "We are mid-X. Just finished Y. Next step is Z." |
| Open questions | Items the receiver should clarify with the user before resuming. Empty is fine. |

## Phase 3 - Confirm with the user

Show the user the draft section A + B inline (NOT the whole bundle - too long). Ask:

> Section A draft (the tasks the receiver will absorb):
> - [ ] ...
> - [ ] ...
> Section B headline (the decisions you'll explain):
> - ...
>
> Receiver context (where is this going?):
> - [x] ZOE / cowork bot, via Bonfire (default)
> - [ ] Another CC session on this mac
> - [ ] CC on a different machine
> - [ ] claude.ai or a different agent
> - [ ] Future-you, weeks later
>
> Slug for the doc folder (default: `<auto-picked from section A>`): _______
> Targets to fire:
> - [x] Write the bundle doc
> - [x] DROP INTO THE HANDOFF INBOX (default) - `zao-tracker handoff` so it appears in ZOE's /cockpit with NO paste (Phase 7)
> - [x] Bonfire push (required when receiver is ZOE, best-effort otherwise)
> - [ ] Auto-clipboard for paste (opt-in now - only if Zaal wants a paste-ready copy for himself; the inbox is the delivery path)
> - [ ] Cowork tracker rows for EACH section A task (opt-in - the inbox drop is one summary row; check this to also file each task)

Wait for confirmation. Edit Section A based on feedback before writing.

**Default-receiver rule:** unless Zaal says otherwise, assume the receiver is ZOE via Bonfire - most `/handoff` invocations are "move this back to the assistant" rather than a same-mac CC-to-CC handoff. When receiver = ZOE:
- Bonfire push (Phase 6) is REQUIRED, not best-effort - if it fails (no key, network error), surface that failure to Zaal explicitly rather than silently reporting success. This is the actual delivery mechanism for a ZOE handoff, not a nice-to-have.
- One Bonfire episode per Section A task (not just one summary episode) so ZOE's queries can surface individual open items, not just a paragraph blob.
- The local bundle file (`~/.zao/handoff/session-<date>-<slug>/README.md` for no-repo sessions) still gets written as the durable human-readable record, but the clipboard auto-copy is lower priority for a ZOE handoff than for a same-mac receiver - skip asking about it unless Zaal also wants a paste-ready copy for himself.
- Still ask the Phase 3 confirmation question every time (don't skip confirmation just because ZOE is the default) - Zaal said "most of the times," not "always," so a same-mac or different-machine receiver is still a real, live option he may pick.

## Phase 4 - Write the bundle

Write the bundle to the path Phase 0 picked. Use the 5-section template verbatim (the structure in the "The 5-section bundle" section above).

**For a CLOUD / different-machine receiver, add two extra sections above Section A** (they are noise for same-mac handoffs, so skip them there):
1. **"Repos to use (START HERE)"** - the exact primary repo the receiver clones (owner/name + git URL + the branch/validate/PR conventions), plus one line naming any secondary/reference repos. Rule of thumb: "if unsure which repo, it is <primary>."
2. **"Capability boundary (cloud vs terminal)"** - a boot self-check (`~/.zao/zao.env` for secrets, `~/.claude/skills` for the brain, `gh auth status`, `$DISPLAY` for GUI) + the escalation rule: when a task needs local secrets, browser/GUI, the clipboard skill, locally-authed MCP, Zaal's real accounts, onchain writes, or a non-repo local file, the cloud session STOPS and asks Zaal to run that step in a mac terminal (or do it himself) rather than silently failing or faking it - and continues with everything it CAN do. This is what lets a cloud session know its own lane.

If the unified diff is over 500 lines:
- Write a one-line-per-file summary inline in Section C
- Write the full diff to `<path>/diff.patch` as a sidecar
- Note in Section C: "Full diff at diff.patch (apply with `git apply diff.patch`)"

Sidecar files (only when relevant):
- `diff.patch` - if uncommitted diff is large
- `inflight.json` - if background jobs are running (raw state for debugging)
- `transcript.md` - if this session was processing a meeting (link to the source)

## Phase 5 - Secret + PII scan

Before writing, scan the bundle markdown for secrets + PII. Use the regex set from `.claude/rules/secret-hygiene.md` (project-local if available, else the patterns inlined below):

Secret patterns (HIGH severity):
- `sk-ant-[A-Za-z0-9_-]{20,}` (Anthropic key)
- `ghp_[A-Za-z0-9]{36}` (GitHub PAT)
- `sk-(proj-|cp-)?[A-Za-z0-9_-]{30,}` (OpenAI key)
- `-----BEGIN ([A-Z]+ )?PRIVATE KEY-----` (PEM)
- `0x[0-9a-fA-F]{64}` (private key / hash)
- `[0-9]{9,12}:[A-Za-z0-9_-]{30,}` (Telegram bot token)
- `AKIA[0-9A-Z]{16}` (AWS key)

PII patterns (per `.claude/rules/pii-hygiene.md`, in ZAO repos):
- third-party emails outside the public ZAO allowlist
- US phone numbers
- street addresses
- third-party Telegram handles

If any HIT, abort the write. Print to chat: `[handoff] ABORT - secret/PII match: <pattern>. Redact + re-run.` Do NOT auto-redact - that risks leaving partial leaks.

## Phase 6 - Bonfire (required when receiver is ZOE, best-effort otherwise)

Build the episodes JSON at a **session-specific tmp path** so parallel sessions never collide and the Write tool never errors on stale files:

```bash
EPISODES_JSON="/tmp/handoff-bonfire-episodes-${slug}-$$.json"
```

Pattern: `/tmp/handoff-bonfire-episodes-<slug>-<pid>.json`. The PID makes it unique per invocation; the slug makes it human-readable when scanning `/tmp`. NEVER hardcode `/tmp/handoff-bonfire-episodes.json` - that path is a collision trap (the Write tool refuses to overwrite a stale file from a prior session and you waste a turn on `rm -f` + retry).

Same pattern applies to any other tmp file this skill writes: append `-<slug>-$$` so each invocation gets its own filename.

Contents:

```json
{
  "episodes": [
    {"name": "session:<date>:summary", "body": "<one paragraph: what was worked on, key decisions, where it ended>", "source_tag": "handoff:<slug>"},
    {"name": "session:<date>:task-1", "body": "From the <date> session, <action title>. Context: <one-line>.", "source_tag": "handoff:<slug>"}
  ]
}
```

One summary episode + one per section-A task. Run:
```bash
bash ~/.claude/skills/meeting/scripts/bonfire-episode.sh "$EPISODES_JSON"
```

The `bonfire-episode.sh` script handles all env loading + secret-scanning + best-effort posting (post doc 754, it reads `~/.zao/zao.env` correctly). If env is missing it prints "skipped (no key)" and exits 0.

## Phase 7 - Auto-clipboard (BOOT-CLIPBOARD format - least clicks)

Zaal's standing rule: least clicks always. Do NOT dump the whole bundle markdown to the clipboard. Emit a minimal, two-block BOOT clipboard the receiver can act on without reading or scrolling. Use the `clipboard-emit.sh` helper directly with exactly two `<pre>` blocks (each gets its own one-click Copy button):

1. **The repo (its own labeled spot)** - the exact repo the receiver opens, as a copyable clone URL. If the work spans multiple repos, this is the PRIMARY one only; name secondary/reference repos in one line of prose, not as copy blocks.
2. **The one paste for the terminal** - a single self-contained block that does the whole boot: clone the repo, cd in, read the bundle, follow it. One copy, one paste, done. Example shape:
   `Clone <primary-repo-git-url> and cd into it, then read <bundle-path-relative-to-repo-root> and follow the receiver instructions at the top. <one-line mode + task count>.`

```bash
cat <<'BODY' | bash ~/.claude/skills/clipboard/bin/clipboard-emit.sh "Cloud terminal boot - <slug>" "cloud-boot-<slug>"
<h2>1. The repo</h2>
<primary-repo owner/name>
<pre><primary-repo git clone URL></pre>
<h2>2. Paste this into the terminal</h2>
<pre><the one self-contained clone+read+follow line></pre>
BODY
```

**Cloud-receiver rule (overrides "never commit the bundle"):** if the receiver is a cloud terminal / different machine (i.e. it will NOT have Zaal's local filesystem), the bundle MUST be reachable from a clone - so commit it into the primary repo (a `.handoffs/` path is fine; PR + merge) BEFORE writing the clipboard, and make the paste-block path RELATIVE to the repo root (not the absolute mac path). For same-mac receivers, keep it local/uncommitted and the absolute path is fine.

The full bundle still lives at its path for anyone who wants to read it; the clipboard is just the fast boot.

## Phase 7.5 - Drop into the handoff INBOX (DEFAULT delivery - no paste)

This is the step that means Zaal never has to paste a handoff into ZOE. Every
handoff registers itself in the shared inbox that ZOE's `/cockpit` reads, so it
shows up as a HANDOFFS lane item automatically.

Run (best-effort; falls back to clipboard if it fails):

```bash
# one summary row per handoff - legacy_source "handoff:<slug>" is what the
# cockpit HANDOFFS lane (bot/src/cockpit/adapters.ts partitionHandoffs) reads.
~/bin/zao-tracker handoff "<slug>" "<one-line: what this handoff is + the top task>"
```

- The `<slug>` matches the bundle folder slug. The summary should lead with the single most important task to pick up.
- On success: report `[OK] Inbox - dropped into ZOE /cockpit (no paste needed)`.
- If `zao-tracker` is unavailable (env not loaded, network): fall back to the clipboard-for-paste path and say so - do NOT silently drop the handoff.
- This REPLACES manual paste as the default. The clipboard is now opt-in (only when Zaal wants a copy for himself).
- The receiver flow: Zaal (or any terminal) runs `/cockpit`, sees the handoff in the HANDOFFS lane with its slug + top task, and picks it up. No copy-paste.

## Phase 8 - Report

```
[OK] Bundle -> research/events/session-YYYY-MM-DD-<slug>/README.md
[OK] Inbox -> dropped into ZOE /cockpit HANDOFFS lane (no paste needed)
[OK] Diff -> diff.patch sidecar (NN lines)
[--] Bonfire - skipped (no key)  |  [OK] Bonfire - N episodes posted
[--] Clipboard - opt-in (skipped)  |  [OK] Clipboard - ready to paste from ~/.zao/clipboard/session-<slug>.html
[OK] Or copy-paste this whole block into a fresh CC terminal:

<bundle markdown inline>
```

End with the actual bundle inline (last) so the user can long-press-copy it directly from the terminal if they don't want to open the clipboard page.

## Hard rules

- **Default voice: receiver is mid-work.** Section A is "tasks to absorb into your TODO list", not "things you need to know." Tone is "add these to your list" not "here's the situation."
- **Never include the full conversation transcript** in the bundle. Section B's job is to compress it. Section E's "mental model" is 2-3 sentences max.
- **Never auto-write decisions without confirming Section A with the user first.** Skip this only on `--auto` flag (for chained workflows).
- **Never push to remote git** as part of `/handoff` - EXCEPT the Phase-7 cloud-receiver case, where the bundle must be committed + pushed so a cloud clone can read it (see Phase 7). For same-mac/local receivers, never push.
- **Never commit the bundle to git for same-mac receivers.** Bundles are draft artifacts. The ONLY exception is a cloud/different-machine receiver that needs the bundle reachable from a clone (Phase 7 cloud rule).
- **No emojis. No em dashes.** Use hyphens. Per global feedback rules.

## Anti-patterns

- Do NOT wrap `everything-claude-code:save-session`. Native build per doc 755 decision #6.
- Do NOT write the bundle as multiple files for "easier reading" - the spec is single-file. Sidecars are only for the diff + inflight raw state, not for splitting the bundle itself.
- Do NOT post the FULL conversation to Bonfire. Only summary + section-A tasks.
- Do NOT include section-A items the user pushed back on - if they edited the draft, write what they confirmed.

## Receiver flow (for documentation; not part of this skill)

Receiver gets the bundle. Two paste flows:
1. **Same-mac fast path**: open a new CC terminal, type `/handoff-resume <path-to-bundle-README>` (v2 skill, not yet shipped).
2. **Manual path (v1)**: open any chat surface, paste the bundle. The receiving model reads it, integrates section A into TaskList, and reads B-E as it works.

## Scripts

- `scripts/handoff-detect.sh` - print repo type (zao/bcz/other-repo/no-repo) + suggested output path
- `scripts/handoff-build.sh git` - emit git state + diff to a tmp file
- (v2) `scripts/handoff-bonfire.sh` - thin wrapper that builds the episodes JSON + calls bonfire-episode.sh

## References

- `references/bundle-template.md` - the exact 5-section markdown template (copy-paste-able)
- Doc 755 (in ZAO OS V1) - design spec
- Doc 754 (in ZAO OS V1) - Bonfire push unblock that makes Phase 6 work
- Doc 717 (in ZAO OS V1) - upstream architecture context
