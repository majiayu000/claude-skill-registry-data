---
name: compare
description: Compare a field of candidates (tools, frameworks, services, products) and recommend one, from a one-round brief through gated, per-candidate research and a refuting verifier to a compact verdict in chat. --quick answers inline.
disable-model-invocation: true
argument-hint: "<candidates or field> [--quick]"
---

The arguments name the field: candidates ("Next.js vs SvelteKit"), a category ("git clients to replace Sublime Merge"), or both, plus anything already known about the purpose or requirements. This skill ends in a recommendation. It changes no code and writes no files outside `/tmp`.

## Brief

One round, never a follow-up. Four slots; skip a slot the arguments or context already answer, and give every remaining one a recommended answer drawn from the repo, the user's instructions and memories, and their environment.

- **Purpose:** what the choice is for: the project, the workload, the pain that started it.
- **Incumbent and seeds:** what's used today, and any candidates the user named.
- **Must-haves:** pass/fail requirements, at most 4. Draft them from the arguments ("X is a requirement"), from what the incumbent does that the user relies on or the pains they name, from environment constraints in their instructions (package availability, platforms, ToS), and from their memories. Tag each with where it came from.
- **Priorities:** what to weigh among the survivors, in order. Seed them from the defaults below for the field's kind.

Asking the round:

- Only must-haves the user confirms become gates; unconfirmed ones drop to priorities.
- Use the harness's question tool (pi `ask_user_question`, Claude `AskUserQuestion`) when every slot is a short pick, otherwise markdown with a `> **Recommended:**` line under each.

Default priorities, starting points rather than fixed columns:

- **Software tool or library:** fit for the purpose, critical mass (stars, contributors, downloads, dependents), maintenance (release cadence, recent commits, bus factor), licence and forkability, platforms and packaging, cost in context or resources where agents use it.
- **Hosted service or subscription:** what the limits really are in use, price at the user's volume, ToS (custom clients, agents), data retention and jurisdiction, lock-in and export.
- **Physical product:** local availability and price with shipping, compatibility with what they own, reviews from long-term owners. If the user is in Denmark and `../pricerunner/SKILL.md` exists beside this skill's directory, get prices by reading it and running its script; it's user-invoked only, so it can't be invoked as a skill.

## Sweep

Build the field.

- The incumbent is always a candidate: "keep X" is a legitimate verdict.
- Add "build our own" only when the scope makes it plausible (a plugin, a script, a fork of a candidate), never for a framework or a product category.
- With seeded candidates, sweep inline: a few searches for what else exists in the category, recent newcomers included.
- With an open field, give the sweep to one fresh subagent that returns a deduplicated list with a one-line description and a link each.
- Candidates the user adds at any point join the field, deduplicated against it.

## Gate

- Check each candidate against the confirmed must-haves only.
- Drop a candidate only on a clear fail with a source, and record the reason in one line.
- A must-have that can't be checked from what's quickly available leaves the candidate in, marked unverified on that row.
- At most 5 finalists. If more pass, list them with a one-line case each and ask the user which to cut; never cut silently.

## Research

- Print one line naming the agents about to start, e.g. "4 researchers (GitComet, SourceGit, SmartGit, Sublime Merge), then 1 verifier".
- Start one fresh subagent per finalist (not a fork), in parallel. Each sees its own candidate and never the others, so the order of the field and the first-named option can't sway it.
- Without a subagent tool, research them one after another inline, finishing each before reading about the next.

Every researcher gets the same criteria sheet: purpose, confirmed must-haves, priorities in order, today's date, and these rules:

- Answer every row of the sheet. A row without evidence is "unknown", not a guess, and not left out.
- Every claim carries a source link and an as-of date. Prefer the strongest source: the code or the published package (tarball, release asset) over docs, docs over README claims, README claims over third-party write-ups. Mark claims that rest only on a README or marketing page "claimed".
- Don't trust prior knowledge for anything that changes: prices, limits, versions, maintenance status, licences. Look it up.
- When docs and what users report disagree (issue trackers, forums, changelogs), report both.
- Measure what can be measured cheaply in a sandbox under `/tmp`: install it with a one-off package command, time a run, count tokens, run a handful of benchmark queries. Measure the thing the claim is about, not a proxy for it. A number that wasn't measured is "claimed", with the command that would measure it.
- Return the sheet filled in, the candidate's strongest case and its worst problem for this purpose, each in a sentence.

## Verify

Give one fresh subagent the criteria sheet, the filled sheets and what the user has said in this session about any candidate. It tries to refute every cell:

- Does the cited source exist, and does it say that, as of when?
- Does each measurement measure what its claim says?
- Do the candidates have comparable evidence on each row? Flag a row where one candidate has a source code reference and another a README line.
- Where a cell contradicts something the user said, flag it as a conflict ("docs say X; you said Y; users report Z"). Never resolve it in the docs' favour.

It returns each cell as confirmed, refuted (with the correction) or unverified. Then:

- Apply the corrections and mark unverified cells.
- Carry every conflict into the report for the user to settle.
- Overrule the verifier only with evidence, and say so.

## Report

In chat, compact enough to read in one go:

```markdown
## <verdict in one sentence: pick, keep, build, or wait>

<2–3 sentences on why, naming the decisive rows.>

1. **<candidate>**: <why it ranks here, one line>
2. …

|                | <candidate>                  | <candidate>                             | …          |
| -------------- | ---------------------------- | --------------------------------------- | ---------- |
| Must-have gaps | none                         | <gate rows it fails or couldn't verify> |            |
| <priority row> | ✓ <short claim> ([src](url)) | partial: <claim>                        | unverified |

### <candidate>

<One paragraph each: strongest case, worst problem, anything measured.>

**Dropped at the gate:** <candidate>: <failed must-have, source> · …

**Conflicts to settle:** <docs vs your claim vs user reports, if any>

**Flip if:** <if X matters more than Y, pick Z> · …
```

- Rows are ordered by priority, at most about 10.
- Cells are ✓, ✗, partial or unverified plus a short claim and its source.
- No numeric scores or weights: argue the ranking in prose and let the flip lines carry the trade-offs.
- Keep the researchers' full findings in context. When the user asks to expand on a candidate or a row, answer from them before searching again.
- End with what the user needs to act on: one line offering to publish the report as a page or document, and one line naming the next step (build it, or `/grill-me` on adopting the pick).

## --quick

For when the user is only slightly curious. No subagents, no verifier, no file.

- Ask nothing, unless one unknown (usually the purpose) could flip the verdict; then ask that single question first.
- Open with one line stating the assumed purpose and must-haves, so the user can object.
- Search inline; give every claim a source and an as-of date, and the same "don't trust prior knowledge" rule applies.
- Answer with the verdict, a table of at most 6 rows and the flip lines, then end with `Deeper: /compare <field>`.
- A deep run that follows in the same session starts its brief from these assumptions as the recommended answers.
