---
name: meeting-notes
description: "Use when converting meeting transcripts, Clova Note exports, Slack huddle notes, speaker-labeled records, or AI summaries into Korean meeting minutes, Slack Canvas documents, action tables, Slack List registrations, or reusable meeting-minutes prompts."
---

# Meeting Notes

## Overview

Turn meeting transcripts, Clova Note exports, Slack huddle notes, and AI summaries into action-oriented Korean meeting minutes. Treat the input as raw evidence, then normalize names, technical terms, decisions, action items, unresolved questions, and audit evidence into Slack Canvas-ready Markdown.

## Core Rule

Do not produce a chronological transcript summary unless the user explicitly asks for one. Meeting minutes should preserve what matters after the meeting: decisions, owners, deadlines, risks, follow-up locations, and the evidence needed to audit corrections later.

Decision statements must be certain and attributable. 결정사항에는 불확실한 내용을 넣지 않는다. Put uncertain transcript-backed claims in `리스크/열린 질문` and in the correction appendix instead.

## Required Meeting Inputs

Before producing or creating meeting minutes, require both:

- A participant list from the user or source metadata. This participant list remains required metadata for the final Canvas and for speaker/owner correction; it is not the default Canvas access target.
- The meeting transcript text that will be preserved under `원문 전사본 전문`.

Input collection order is sequential. If either the participant list or transcript is missing, stop and ask for the missing input before drafting, creating, or indexing the meeting artifact, but ask in this order:

1. When no participant list is present, ask only for the participant list. Do not ask for the transcript in the same response.
2. After the participant list is provided, confirm the received participants, then ask for the meeting transcript text.
3. When both inputs are present, continue with the normal Meeting Notes workflow.

Do not infer the required participant metadata solely from generic speaker labels such as `참석자 1`; speaker labels can supplement the correction appendix, but they do not satisfy the required participant list. A final meeting Canvas must not be created from fallback placeholder content.

## Canvas UI/UX Principles

Slack Canvas is a fully formatted surface for information that does not fit in a normal message. Design meeting Canvases for scanning first, then audit depth.

Use these proven patterns:

- **Top status block UI:** after the title, add one short scope/status block. The syntax depends on the write path: Slack MCP Canvas-flavored Markdown may use `::: {.callout}` after read-back confirms it renders as a callout UI, but raw Slack Web API `canvases.create`/`canvases.edit` does not support that callout syntax and renders it literally. When using `.zshrc` token or `scripts/publish_meeting_canvas.py`, use a Web API-safe quote line such as `> 회의일 YYYY-MM-DD · 대상 #sample-platform-team · Source synthetic transcript · Follow-up 필요`.
- **Progressive disclosure:** put the answer first (`TL;DR`, decisions, actions), then topic detail, then follow-up, then uncertainty and appendix. Readers should understand the meeting without reaching the transcript.
- **Layer-cake headings:** headings must be meaningful on their own. A reader scanning only headings should see the meeting flow.
- **Chunk dense facts:** split long decision/action/risk lines into short nested bullets with labels. Do not pack decision, evidence, owner, impact, and status into one sentence.
- **Use tables only where comparison helps:** keep metadata as a compact two-column table with short cell values; avoid wide tables for decisions, risks, corrections, or meeting indexes because Slack Canvas tables expand to the longest cell and compress columns aggressively. If a metadata value is long, put a short summary in the table and move the detail to `### 메타데이터 메모`.
- **Use status blocks sparingly:** one scope/status block near the top, optional warning block only for high-impact caveats. Do not wrap normal body sections in callouts.
- **Prefer numerals and concrete labels:** counts, dates, owners, status, and tracker names should be visible without reading full prose.
- **Mirror source-specific UI when useful:** if a source Canvas or user-provided example has a clearer pattern, extract the pattern and adapt it, but do not copy irrelevant formatting.

## Slack Canvas UI Block Palette

Use Slack Canvas UI blocks intentionally. The default meeting-minutes pattern is not plain Markdown; it is a readable Canvas document composed from a small, verified block palette.

| Block | Use For | Meeting-Minutes Rule |
|---|---|---|
| Callout/status quote | Scope, status, high-impact caveat | Use one top status block before metadata. Use MCP `::: {.callout}` only on the MCP path; use `>` quote syntax on raw Web API paths. |
| 2-column vertical table | Metadata fields | Use `Field` / `Value`; do not make metadata a wide horizontal table. |
| Narrow table | Short comparisons | Use only for metadata-like comparisons that genuinely scan better as rows. Avoid action/risk/correction mega-tables. |
| Checklist bullets | Action items | Use `- [ ]` with owner, deliverable, due date, and tracker in one scannable line. |
| Heading hierarchy | Section scanning | Use only `#`, `##`, `###`. Make headings meaningful without reading body text. |
| Slack emoji codes in headings | Visual anchors | Use sparingly for major sections only, such as `:dart:` or `:white_check_mark:`. Do not decorate every bullet. |
| Layout columns | Short side-by-side summaries | Optional only for dashboard-style summaries. Do not put tables, callouts, or transcript/code blocks inside layouts. |
| Horizontal rule | Separate execution area from audit appendix | Use one top-level `---` before `보정 및 원문 부록` when the Canvas is long. Do not put dividers between every section. |
| Block quote | Short verbatim evidence | Use only for a short source quote that clarifies a decision. Do not use block quotes for normal summary text. |
| Code block | Verbatim transcript | Use a top-level `text` code block only for `원문 전사본 전문`. |
| Links and Slack references | Trackers, source, channel, people | Prefer labeled links. Use Slack Canvas reference syntax only when IDs are known. |

Default meeting Canvas UI recipe:

1. Title.
2. Top status block with date/target/source/status.
3. 2-column metadata table.
4. TL;DR as 2-4 bullets or short sentences.
5. Decisions as bold titled bullets with separated fields.
6. Actions as checklist bullets.
7. Topic discussion with `###` sections.
8. Follow-up and risks near the appendix.
9. One divider, then correction maps and verbatim transcript.

## Canvas UI Pattern Examples

Detailed snippets live in `references/canvas-ui-examples.md`; load that file only when drafting or debugging a Canvas body. Do not overfit the UI proof Canvas; it was used only to verify which Slack blocks survive read-back. Apply the patterns to the meeting's content density and user goal.

- Status block: use `::: {.callout}` only for MCP Canvas creation after read-back confirms it renders; use `> 회의일 ...` for raw Slack Web API writes.
- Metadata table: use `|Field|Value|` as the two-column vertical metadata table for the team's current Canvas convention. Keep each value short enough to fit narrow Canvas widths; long participant lists, source details, access notes, and tracker links belong in `### 메타데이터 메모`.
- TL;DR bullets: use 2-4 bullets for multi-topic meetings.
- Action checklist: use checklist bullets under `## 액션 보드`.
- Short evidence quote: use only a short quote that clarifies a decision.
- Audit divider: use one `---` before the correction appendix.
- Transcript block: preserve the transcript in a top-level `text` code fence marker such as ```` ```text ````; do not put transcript/code blocks inside layout columns.
- Layout columns: only for short dashboard-style summaries. Do not use them in the default meeting minutes body because tables, callouts, and transcript/code blocks are not supported inside layouts.

## Canvas Anti-Patterns

Reject these outputs before they reach Slack:

- Do not use one dense paragraph for TL;DR in multi-topic meetings. Use 2-4 bullets so a reader can scan the outcome.
- Do not use tables for decisions, actions, risks, or corrections by default. Use titled bullets and checklists; tables are only for metadata or short comparisons.
- Do not put long values into the metadata table. Slack Canvas table width follows the longest cell, so `Participants`, `Source`, `Tracking`, and `Access` must be summaries such as `플랫폼담당 외 4명`, `붙여넣은 화자분리 전사본`, `Slack List / issue tracker / 런북`, and `#sample-platform-team`; put exact long detail below in `### 메타데이터 메모`.
- Do not put callouts, tables, or code blocks inside layout columns. Slack Canvas does not support those nested combinations reliably.
- Do not create a skeleton Canvas and stop there. If a fallback skeleton is created, it must be followed by section updates until the full readable meeting Canvas is present.
- Do not hide uncertainty in decisions. Keep uncertain speaker mappings, term mappings, policy details, and architecture assumptions in `리스크/열린 질문` or the correction appendix.
- Do not put meeting-index maintenance inside the meeting Canvas. The Canvas is for meeting content; Slack List binding happens separately as an automatic existing-List registration for published meeting Canvases, with manual handoff only after verified API/permission failure.
- Do not replace the verbatim transcript with representative excerpts unless a hard Slack/API limit forces a degraded output and the output is explicitly labeled `원문 전사본 발췌`.

## Default Slack Target

- 기본 대상 채널: `#sample-platform-team`.
- Default artifact: create the individual meeting Canvas for `#sample-platform-team`, grant workspace-wide view access, and register the meeting in the existing Slack List using that List's current convention.
- Slack List registration is automatic for published meeting Canvases. Inspect the existing List convention first, then create/update exactly one row through the verified Web API path. Use Slack's built-in `이름` field for the meeting title and do not create a duplicate index List. Manual handoff is a fallback only when API/tool permission is actually unavailable after verification.
- 다른 채널 can be used when the user names one. Treat the named channel as a channel override for the meeting Canvas.
- When drafting only, write the target as metadata and do not claim a Canvas was created.
- After a Canvas is created and read back, register or update the existing Slack List row, then report the List row/item ID separately. If List registration is blocked by verified API/permission limits, provide a manual index-binding handoff instead. This handoff is not part of the Canvas body unless the user explicitly asks for it.

Do not claim to have created, shared, pinned, attached, or updated a Slack Canvas unless a Slack tool call or user confirmation proves it. If only drafting text, call it Canvas-ready content.

## Participant Access Grant

Meeting canvases are created with default "invited people only" access, so a freshly created Canvas can be creator-only until sharing is applied. The default sharing policy is **워크스페이스 공개 채널 구성원 열람**: give the Canvas public channel based `read` access so anyone in the workspace who can use that public channel visibility path can view it.

- Use `#sample-platform-team` as the default public-channel sharing target unless the user names another channel. The API call needs Slack channel IDs, so set `CANVAS_ACCESS_CHANNEL_IDS` (comma-separated `C...` IDs) before using the Web API helper.
- Granting access needs the Slack Web API `canvases.access.set` with `channel_ids` and `access_level: read`. Access level defaults to `read`; use `write` only when the user asks for collaborative editing.
- Do not pass `channel_ids` and `user_ids` together. Slack rejects mixed target types in one `canvases.access.set` call. Use `channel_ids` for the default workspace visibility path.
- The participant list remains required metadata: include it in the Canvas metadata, use it for owner/speaker correction, and record unresolved or ambiguous participant/speaker mappings in `참석자/화자 보정`. Do not silently convert generic speaker labels to real people.
- Use participant `user_ids` only when the user explicitly asks for restricted participant-only sharing or the public-channel target cannot be provided. In that restricted mode, only auto-resolve users on a single unambiguous match; on no match or multiple matches (동명이인), do not guess.
- The current MCP surface has no `canvases.access.set` tool. Create/read the Canvas via MCP when available, but run the access grant through the Web API path in `scripts/publish_meeting_canvas.py`. Requires a token with `canvases:write` and `lists:write` for the default published artifact (plus `users:read` only for restricted participant lookup); Lists/Canvas are paid-plan features.

## Local Background

Before resolving terms, services, participants, or speaker labels, check for `skills/meeting-notes/background.local.md`. That file is gitignored on purpose; use `skills/meeting-notes/background.local.example.md` as the tracked template and keep team-specific names, service names, and private operating context out of `SKILL.md`.

Use local background as high-confidence correction candidates for product names, team rosters, explicitly listed aliases, confirmed roles, and domain terms. Product and service names from local background are preferred over phonetically similar unknown terms when the meeting context matches the product/service domain; for example, if local background lists `{product}`, then a matching transcript variant should resolve to `{product} staging`, not to an invented project name. If the local background explicitly gives an alias such as `{alias}: {name}`, apply that alias consistently in decisions, actions, topic summaries, and correction maps. Standalone Korean honorific-like words may be name misrecognitions when they phonetically match exactly one roster member; for example, `프로님` can resolve to `{sample_name} 님` when `{sample_name}` is in the local roster or alias list. But `{name} 프로님` should be treated as a title/honorific, not as the alias target, unless the local background explicitly says otherwise. If the local background confirms a role such as `{name}: 팀리더`, do not write `{name} 팀리더 추정`; write the confirmed role directly. Do not silently convert a generic speaker label such as `참석자 N` to a real name from the roster alone. A real-name speaker mapping still needs transcript evidence, user-provided context, an explicit alias entry, a unique phonetic roster match for a standalone name-like expression, or a clear meeting role; otherwise write it as `{이름} 추정` or keep `참석자 N` and record the uncertainty in `참석자/화자 보정`.

## Workflow

1. Identify the requested output: full minutes, Slack Canvas meeting doc with existing Slack List registration, Slack recap, action table, or prompt.
2. Confirm required inputs before drafting or writing:
   - If no participant list is present, ask only for the participant list and stop.
   - If a participant list is present but the transcript is missing, confirm the received participants, ask for the meeting transcript text, and stop.
   - If both participant list and transcript are present, continue with the normal Meeting Notes workflow.
3. Resolve Canvas target:
   - Use `#sample-platform-team` by default.
   - Apply a user-provided 채널 override when present.
   - Record target channel, access assumption, source, and last-updated metadata in the output.
   - Use the required participant list as Canvas metadata and correction evidence; use the public-channel target for the default workspace access grant.
4. Read optional local background, then read the transcript and build correction maps:
   - technical terms
   - uncertain words or sentences
   - participants and speaker labels
5. Extract outcomes before narrative:
   - TL;DR
   - decisions
   - action items
   - risks/open questions
   - follow-up checks
6. Render the meeting in reader order: executive summary, decisions, actions, topic discussion, follow-up checks, then risks/open questions immediately before the correction appendix.
7. Group discussion by topic, not by timestamp, unless exact timeline matters.
8. Produce the requested Korean artifact. When creating an individual meeting Canvas, return the verified List binding values and row/item ID separately after read-back verification.
9. Grant Canvas access through the workspace public-channel visibility path by default (see `Participant Access Grant`). Report unresolved or ambiguous participant/speaker mappings instead of guessing.
10. Preserve the full transcript verbatim in the audit appendix unless the user explicitly excludes it. Only redact security-sensitive strings.

## Canvas Naming Rules

Always title individual meeting canvases with this exact pattern:

```text
YYYY-MM-DD [Topic] Title
```

Examples:

```text
2026-06-24 [배포] release/stg 배포 회고
2026-06-25 [테스트품질] 2468 parent 정리 회의
```

Use short topic labels such as `배포`, `테스트품질`, `장애`, `온보딩`, `AI`, `인프라`, `정책`, `리뷰`. If unclear, use `[확인필요]`.

Before calling Slack `create_canvas`, sanitize the API title separately from the human-readable title:

- Avoid literal `&` in the `title` parameter. Use `and`, `및`, or remove the ampersand. For example, send `Sample Platform R and R 및 이벤트 파이프라인 온보딩` as the Slack API title instead of `Sample Platform R&R 및 이벤트 파이프라인 온보딩`.
- Preserve the canonical human-readable title in the Canvas body, metadata, and Slack List row when needed.
- If `create_canvas` returns `Invalid text passed`, retry once with a sanitized title before assuming the body Markdown is invalid.

## Slack List Registration

The default published artifact is not complete until both surfaces are done:

- Create/read back the individual meeting Canvas.
- Grant workspace-wide public-channel access through the target public channel.
- Inspect the existing Slack List convention.
- Create or update one Slack List row with the verified Canvas URL.
- Read back or otherwise verify the row/item ID.

After a successful Canvas create/read-back and List registration, report this separate binding summary in the final response or Slack recap, not inside the Canvas body:

```markdown
Slack List 등록 값
- 이름: {meeting title}
- Date: YYYY-MM-DD
- Topic: {Topic}
- Status: {Draft/Follow-up 필요/완료/확인 필요}
- Counts: 결정 N / 액션 N / 질문 N
- Meeting Canvas: {Canvas URL}
```

Rules:

- Do not skip Slack List registration for a published meeting Canvas. If List tooling or permission fails, verify the failure and report the blocker; only then provide the manual handoff fallback.
- Read/inspect the existing List fields and row convention first; preserve its field names, date format, status values, and title convention.
- Store the Canvas link in the List as the workspace docs URL: `https://{workspace}.slack.com/docs/{team_id}/{canvas_id}`. Do not hard-code a real workspace or team ID. Do not store `https://slack.com/canvas/{canvas_id}` in the List; that fallback can open the wrong surface or fail to match the team's existing List convention. If needed, call Slack `auth.test` to derive the workspace URL and team ID before creating or updating the row.
- Do not create an index Canvas as a substitute for the List.
- Do not put an index row preview in the meeting Canvas body by default.
- If the source has no explicit meeting date and the user did not provide one, set the List `Date` to the same value as `Last updated`.
- Use Slack's built-in List `이름` field as the meeting title, following the existing convention of `[Topic] 제목` without the `YYYY-MM-DD` prefix because `Date` lives in its own column. Do not create/delete/rename List fields unless the user explicitly asks for field administration.

## Meeting Canvas Template

Use this exact structure for every individual meeting Canvas. Keep section names and field order stable so the team can scan every meeting the same way:

````markdown
# YYYY-MM-DD [Topic] Title

> 회의일 YYYY-MM-DD · 대상 #sample-platform-team or {channel override} · Source {source} · Status {Draft/Follow-up 필요/완료/확인 필요}

## 메타데이터
|Field|Value|
|  ---  |  ---  |
| Date | YYYY-MM-DD |
| Topic | {배포/테스트품질/장애/온보딩/AI/인프라/정책/리뷰/확인필요} |
| Status | {Draft / Follow-up 필요 / 완료 / 확인 필요} |
| Owner | {짧은 owner 또는 미정} |
| Participants | {짧은 요약. 예: 플랫폼담당 외 4명} |
| Source | {짧은 source. 예: 붙여넣은 화자분리 전사본} |
| Slack thread | {링크 또는 미정} |
| Tracking | {짧은 tracker 요약. 예: Slack List / GitLab / 런북} |
| Access | {#sample-platform-team / channel override / restricted / 미정} |
| Last updated | YYYY-MM-DD |

### 메타데이터 메모
- 회의일이 source에 없으면 `Date`는 `Last updated`와 같은 값을 사용한다.
- 긴 참석자 전체 명단, source URL, Slack thread, GitLab/문서 링크, 접근권한 상세는 이 섹션에 bullet로 둔다.

## TL;DR
- {회의 결론 또는 방향성.}
- {우선순위 또는 실행 흐름.}
- {주요 follow-up 또는 리스크.}

## 결정사항
- **{짧은 결정 제목}**
  - 내용: {확정된 결정}
  - 근거: {timestamp/source}
  - 영향: {영향 범위}
  - 결정자/동의자: {이름 또는 미정}
  - 상태: 확정

## 액션 보드
- [ ] {담당}: {산출물 중심 작업}. 기한: {날짜/미정}. Tracking: {Slack/GitLab/문서 링크 또는 미정}.

## 주제별 논의
### {주제}
- 배경: {왜 논의했는가}
- 논점: {주요 내용}
- 정리: {현재 상태}

## 후속 확인
- {확인할 것}. 담당: {이름/미정}. 확인 위치: {Slack/GitLab/문서/미정}. 기한: {날짜/미정}.

## 리스크/열린 질문
- **{리스크 또는 질문 제목}**
  - 내용: {불명확한 점}
  - 확인 담당: {이름/미정}
  - 확인 방법: {확인 경로}
  - 상태: 확인 필요

---

## 보정 및 원문 부록

### 용어 보정
- `{오인식 표현}` -> `{정확한 표현}`. 근거: {문맥/링크/사용자 보정}. 신뢰도: {높음/중간/낮음}. 확인 방법: {확인 경로}.

### 불확실 단어/문장 보정
- `{불확실한 표현}` -> `{추정 또는 확인 필요}`. 근거: {문맥}. 신뢰도: 낮음. 확인 방법: {누구에게/어디서 확인}.

### 참석자/화자 보정
- `{참석자 1}` -> `{이름 또는 확인 필요}`. 근거: {사용자 제공/문맥}. 신뢰도: {높음/중간/낮음}. 확인 방법: {확인 경로}.

### 원문 전사본 전문
```text
[00:00] Speaker 1: {원문 발화}
[00:15] Speaker 2: {원문 발화}
```
````

The full transcript must remain a verbatim block with visible speaker/timestamp context. 표로 넣지 않는다. Do not summarize, normalize, translate, or replace the pasted transcript under `원문 전사본 전문`.

## Quality Rules

- Add the top status block before metadata. It should fit on one line when possible and contain only scope/status facts: date or period, target channel, source/basis, status, and exclusions if any. Use `::: {.callout}` only for Slack MCP Canvas-flavored Markdown; use `>` quote syntax for raw Slack Web API writes because the Web API Markdown support does not include callout blocks.
- Use the default UI recipe unless the user asks for a different Canvas style. A passable meeting Canvas should visibly use at least these UI affordances: top status block, 2-column metadata table, checklist action board, layer-cake headings, and a transcript code block. Long Canvases should also use one top-level divider before the audit appendix.
- Keep the metadata table narrow. The `Field`/`Value` table is allowed only for short values; long cells make Slack Canvas render a wide, hard-to-read table. Use summaries in the table and move detail to `### 메타데이터 메모`. A publish path should reject metadata rows that would exceed the width guard rather than posting a wide table.
- Put `TL;DR`, `결정사항`, and `액션 보드` above detailed discussion.
- Render `TL;DR` as 2-4 bullets when there are multiple independent takeaways. Use short paragraphs only when the meeting has a single clear outcome.
- Render `결정사항` as scannable multi-line bullets with separate `내용`, `근거`, `영향`, `결정자/동의자`, and `상태` fields. A long one-line decision that packs all fields into one sentence is a readability failure on Slack Canvas.
- Render `리스크/열린 질문` after `후속 확인` and immediately before `보정 및 원문 부록`. This keeps executable meeting flow above and uncertainty/audit material together near the appendix.
- Render every risk/open-question item as a titled multi-line bullet with separated `내용`, `확인 담당`, `확인 방법`, and `상태` fields. A one-line risk that packs all fields into one sentence is a Slack Canvas readability failure.
- Optimize for the actual Slack Canvas reading surface, not only Markdown validity. The meeting Canvas body should not include a meeting-index row by default. Provide verified Slack List row values outside the Canvas after the Canvas URL is known. Any table over 5 columns is a quality failure unless the user explicitly asks for export-oriented tabular data.
- A created or read-back meeting Canvas must not retain placeholder cells such as `미정`, `생성 후 인덱스 참조`, or `{Canvas 링크}` for the Canvas URL after the Canvas URL exists.
- Do not use layout columns for the default meeting minutes body. Layouts are useful for short dashboard summaries, but Slack Canvas does not support tables or callouts inside layouts, and long meeting minutes need predictable vertical scanning.
- Keep actions as checklist bullets so they remain readable on narrow Canvas widths.
- If an action is long-term tracking 대상, keep the meeting-time checklist item in Canvas and put the live tracker in `Tracking` as a Slack/GitLab/문서 링크.
- Use one accountable owner when possible. If the transcript implies a team owner but not a person, write `미정` and add an open question.
- If local background and meeting role identify a team lead owner for a follow-up or risk, use the confirmed role in executable fields. Do not leave team-lead-owned follow-ups as `참석자 1` while separately naming a confirmed team lead elsewhere. Speaker mapping can stay uncertain in the appendix, but owner/decision fields should use the best confirmed role.
- Prefer deliverables over vague verbs: `검토한다` is weak; `GitLab 이슈 본문에 검증 체크리스트를 추가한다` is strong.
- Include a due date only when the transcript states or clearly implies one. Otherwise use `미정`.
- Correction maps must contain the fields `원문 표현`, `보정 표현`, `근거`, `신뢰도`, `확인 방법`, but render them as bullets in Slack Canvas unless the list is short enough for a 5-column table to stay readable.
- If a mapping table approaches Slack Canvas's 300 cells limit, split it into sections such as `용어 보정 1`, `용어 보정 2`, `불확실 단어/문장 보정 1`. The 300-cell limit is not enough by itself; rendered readability still fails when the table is too wide.
- Preserve general meeting statements by default. Redact only security-sensitive raw strings such as secret/token/password/API key/private key values with `[민감정보 생략]`.
- Do not paste uncertain transcript-backed claims into `결정사항`; put them in `리스크/열린 질문` and the appendix.
- If Canvas update noise matters, mention that workspace/admin Canvas update-message settings may need review before bulk appendix or transcript updates.

## Slack Canvas Write Path

When using Slack tools, prefer direct Canvas creation after the Markdown is structurally validated:

1. Sanitize the Slack API title, especially by removing or replacing literal `&`, then create the complete Canvas in one `create_canvas` call when the body follows Slack Canvas formatting rules and contains the final readable structure.
2. Read the created Canvas back to verify rendered section order, the 2-column metadata table, absence of index-row sections, multi-line decision bullets, checklist actions, topic discussion, follow-up checks, risks/open questions, correction bullets, and transcript appendix.
3. If direct creation fails with `Invalid text passed`, retry once with a sanitized title if the first title contained punctuation such as `&`. If the sanitized title still fails or the failure is clearly a body formatting/length error, fall back to a skeleton Canvas. Read the created Canvas to capture section IDs, and then append or replace complete sections.

Do not leave the skeleton as the final artifact. A Canvas with only a 1-2 line summary or 2-3 actions is a failed forward-test for a long planning meeting. In live Slack verification, a full long meeting body with verbatim transcript returned `canvas_creation_failed: Invalid text passed`, while the skeleton-create plus section-replace path accepted complete readable sections. Therefore, direct create is the preferred path, and skeleton+replace is a verified fallback for long transcript bodies.

When replacing a header section ID, remember that Slack preserves the targeted header and replaces only that header's body content. The replacement body must not repeat the same heading. For example, replacing the `### 원문 전사본 전문` section should send only the transcript code block, not another `### 원문 전사본 전문` line. After each targeted replace, read the Canvas back and reject adjacent duplicate headings such as `### 원문 전사본 전문` repeated twice.

Do not repair a Slack Canvas metadata table through raw Web API cell-by-cell edits. Slack `canvases.sections.lookup` only identifies sections by headers or non-empty text, and raw table edits can leave unaddressable empty rows such as `|||` below metadata. If a metadata table is wrong or too wide after publish, either use an exact full-canvas `replace` only when the complete source Markdown/transcript is available, or create a clean replacement Canvas and update the existing Slack List row to the new Canvas URL. Never declare a Canvas ready while read-back still contains literal `::: {.callout}`, duplicate metadata tables, wide metadata cells, `|||` blank table rows, or placeholder Canvas/List fields.

For the meeting index, use tools/API by default after the Canvas is verified. First inspect the existing List convention, then create/update exactly one row and verify the resulting row/item ID. Return the List binding values with `이름`, `Date`, `Topic`, `Status`, `Counts`, and `Meeting Canvas`. Avoid destructive full-canvas replace unless the user explicitly asks for a full rewrite, the existing Canvas is already corrupted and must be repaired, or the just-created test Canvas is visibly wrong and must be corrected.

For List row repair, Slack `slackLists.items.update` uses `cells`, and each cell must include its own `row_id`; do not pass `row_id` as a top-level field. After updating the `meeting_canvas` cell, read the List row back and reject it unless `originalUrl` is the workspace docs URL pattern above.

## Forward Quality Rubric

Use a rubric before calling a meeting-minutes output good enough. Treat the first run as the baseline score and keep improving until the current output meets the pass line.

- Baseline: record the first output's baseline score before edits. A weak but structurally valid first pass is expected to be around 25-70/100.
- Pass line: a reusable meeting Canvas must score at least 92/100 before it is treated as ready for `#sample-platform-team`.
- Do not fabricate meeting dates from the transcript. If the source has no explicit meeting date and the user did not provide one, set `Date` to the same value as `Last updated`. Do not add a separate open question just to confirm the meeting date unless the user asks for calendar reconciliation.
- 실명이 전사본만으로 확정되지 않으면 speaker labels remain uncertain. Use `참석자 1(팀 리드 추정)` or similar wording, then put the exact mapping in `참석자/화자 보정`.
- 용어 보정 후보를 먼저 작성, then use only high-confidence corrected terms in decisions/actions. Low-confidence terms stay in `불확실 단어/문장 보정` and open questions.
- Verbatim full transcript handling: if the user provides transcript text, `원문 전사본 전문` must contain that pasted transcript verbatim in one top-level `text` code block, preserving speaker labels, timestamps, wording, omissions, order, and line breaks as much as the Canvas surface allows. Do not summarize, normalize, translate, or substitute representative blocks under `원문 전사본 전문`.
- The pasted transcript must appear exactly once. Do not append the transcript once during skeleton creation and then append or replace it again during section repair. Before declaring a Canvas ready, compare the `원문 전사본 전문` section against the source transcript by marker count or hash: the transcript start marker, transcript end marker, and full transcript body must each occur once.
- If a hard Slack/API limit prevents inserting the complete transcript after trying the skeleton-create plus targeted section update path, do not label the appendix `원문 전사본 전문`. Rename it to `원문 전사본 발췌`, state that the full source is linked in `Source`, and include the exact source location. This is a degraded output and must be called out before treating the Canvas as ready.
- A passable output must create/read back the meeting Canvas, register it in the existing Slack List, and provide separate List binding values that use Slack's built-in `이름` field as the title plus the verified row/item ID. The Canvas body itself should focus on meeting content, not index maintenance.
- A passable created/read-back output must not contain Canvas URL placeholders such as `미정`, `{Canvas 링크}`, or `생성 후 인덱스 참조` after the Canvas URL exists.
- A passable output must not leave known team-lead follow-ups or risks as `참석자 1` when local background and meeting role evidence identify the owner as `{sample_team_lead} 팀리더`.
- A passable output must render risks/open questions as separated fields, not dense one-line records containing `확인 담당`, `확인 방법`, and `상태` in the same bullet.
- A passable output must contain exactly one `### 원문 전사본 전문` heading and one top-level `text` transcript code block under it. Duplicate adjacent transcript headings are a Slack Canvas write-path failure.
- A passable output must include a compact top status block before metadata. For MCP Canvas creation this may be `::: {.callout}` only when read-back confirms it renders as callout UI. For raw Slack Web API creation or repair, it must be a `>` quote line; visible literal `::: {.callout}` is a failed Canvas.
- A passable output must keep the metadata table narrow: no long participant/source/tracking/access cells, no duplicate metadata tables, and no malformed read-back rows such as `|||`, `||Value|`, or `|Date||`. Put long detail in `### 메타데이터 메모`.
- A passable output must follow the Canvas UI recipe: top status block, vertical metadata table, TL;DR bullets for multi-topic meetings, multi-line decision bullets, checklist actions, meaningful `###` topic headings, one divider before the audit appendix, correction bullets, and a transcript code block.
- A passable output must keep section order coherent for readers: `TL;DR` -> `결정사항` -> `액션 보드` -> `주제별 논의` -> `후속 확인` -> `리스크/열린 질문` -> `보정 및 원문 부록`.
- A passable output must show care for readability: decisions use multi-line bullets, not one dense sentence containing decision, evidence, impact, owner, and status.
- A passable output must not contain one 12-column index table, a secondary index detail table, or any table wider than 5 columns for Slack Canvas. Preserve detail fields in the meeting Canvas metadata and Slack List registration values, not in an index table embedded in the Canvas.
- A passable output must have enough substance for the input length. For a 30+ minute planning transcript, `TL;DR` plus sections must cover the major topics; a two-line meeting summary is a failed output.
- Re-run `python3 scripts/meeting_notes_quality_rubric.py` after prompt/skill changes when this repo's fixture is available.

## Slack Recap

Use this when the user asks for a channel message to accompany the Canvas:

```markdown
회의록 Canvas입니다: {Canvas 링크}

- 대상 채널: #sample-platform-team or {channel override}
- 핵심 결론: {1문장}
- 결정사항:
  - {결정}
- 액션 아이템:
  - {담당}: {할 일} ({기한})
- 확인 필요:
  - {열린 질문}
```
