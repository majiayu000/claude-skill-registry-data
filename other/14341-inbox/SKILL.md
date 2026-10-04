---
name: inbox
description: Receiving side of /xm:toss — list, take, resolve, or drop cross-project bug reports that landed in this project's .xm/inbox/. Use when the user asks to check the inbox, "받은 편지함 봐줘", "what did other projects toss at us", or wants to start/finish/dismiss a specific handed-off item.
model: haiku
---

# x-inbox — Cross-Project Inbox

## Overview

The receiving side of `/xm:toss`: `.xm/inbox/<id>.json` holds bug reports other
registered projects tossed at this one. `/xm:inbox` lists them, marks one as being
worked on (`take`), marks verified work complete (`resolve`), or dismisses one
that isn't relevant (`drop`). Every read
opportunistically archives resolved items older than 30 days locally (no network) —
neither this nor anything else in this CLI ever discards an unresolved item.

**The CLI itself makes zero network calls.** It cannot query mem-mesh pin state and
cannot recreate an expired pin — that requires an MCP session, which only you (the
skill, running inside Claude Code) have. Re-notifying an item whose pin already expired
is therefore something YOU do, using `mcp__mem-mesh__pin_get` / `mcp__mem-mesh__pin_add`
plus `xm inbox record --scope inbox` — see step 5 below.

## When to Use

- "받은 편지함 봐줘" / "what's in the inbox" / "show what other projects tossed at us"
- Starting work and want to check for cross-project reports before diving in
- "이거 처리할게" / "I'll work on this one" → `take <id>` (marks in-progress, returns
  the full repro/fix body to act on)
- "수정 끝났어" / "done" → `resolve <id>` after implementation and verification
- "이건 아니다" / "not relevant, drop it" → `drop <id>`

## Do NOT Use When

- You want to SEND a report to another project — that is `/xm:toss`.
- You want to turn a taken item into a tracked x-build task — `take` only returns the
  item's content; promoting it into a task/later item is a separate manual step
  (x-build tasks have no field that holds why/repro/fix_direction verbatim).

## CLI Invocation

> **⚠ Call `xm inbox <command>` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xinbox()`) defined in one call do NOT persist to the next, causing `command not found: xinbox`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XINBOX_CLI=$(ls -d ~/.claude/plugins/cache/xm/xm/*/lib/x-inbox-cli.mjs 2>/dev/null | sort -V | tail -1)
> node "$XINBOX_CLI" <command> [args]
> ```
>
> **Forbidden:** `XINBOX="node ..."; $XINBOX list` — zsh treats the quoted string as a single command and fails.

## Core Process

1. **먼저 mem-mesh에서 수신 항목을 materialize합니다.** `search`에는 현재 `tags`
   필터가 없으므로 `query="inbox"` 같은 넓은 검색으로 수신함을 판단하면 안 됩니다.
   `pin_list`에서 `status`를 생략하면 모든 상태를 반환한다고 가정하지 마십시오.
   현재 서버는 기본 상태를 선택할 수 있어 새 `in_progress` delivery pin이 빠질 수 있습니다.
   다음 세 호출을 각각 실행하고, 반환된 `pins`를 `id`로 중복 제거해 하나의 배열로
   합칩니다. `limit`은 각 호출에서 반드시 10 이하로 둡니다.

   - `mcp__mem-mesh__pin_list(project_id=<id>, tags=["inbox"], status="open", limit=10)`
   - `mcp__mem-mesh__pin_list(project_id=<id>, tags=["inbox"], status="in_progress", limit=10)`
   - `mcp__mem-mesh__pin_list(project_id=<id>, tags=["inbox"], status="completed", limit=10)`

   그 결과를 파일로 저장한 뒤 **`xm inbox reconcile`에 먹여 무엇을 해야 하는지 판정합니다.**
   눈으로 대조하지 마십시오 — 이 명령이 pin 쪽과 원장 쪽 양방향 drift를 모두 계산합니다.
   ```bash
   # pin_list 결과(전체 envelope 또는 pins 배열)를 파일에 기록한 뒤
   xm inbox reconcile --pins-file <path> --json
   ```
   출력의 action별로:
   - `materialize` — pin은 살아 있는데 로컬 원장에 항목이 없습니다. 아래 3단계로 가져옵니다.
   - `renotify` — 미종결 항목의 pin이 죽었습니다(목록에 없거나 `completed`). 7번 절차를 따릅니다.
   - `unmappable` — toss id 없는 구 포맷 pin입니다. 추측하지 말고 pin id와 title을 보여 준 뒤
     발신 측에 재전달을 요청합니다.
   - `none` — 할 일 없음.

   세 호출 중 하나라도 `count == limit`이면 목록이 잘렸을 수 있으므로 `--partial`을
   붙입니다. 그러면 "목록에 없음"을 pin이 죽었다는 증거로 쓰지 않아 잘못된 재알림을
   막습니다. 세 결과를 합치지 않았거나 상태 하나라도 조회하지 못했을 때도
   `--partial`을 붙입니다.

   새 toss pin의 `content`는 `<toss id> — <title>` 형식입니다. `materialize` 대상의 toss id로
   `mcp__mem-mesh__search(query=<toss id>, project_id=<현재 프로젝트의 mem-mesh id>,
   limit=10)`을 호출하고, **같은 `id`를 가진 JSON 본문**만 고릅니다. 그 결과의
   `content`를 아래 명령으로 materialize합니다. **memory 본문은 파일로 먼저 쓰고
   `--content-file`로 넘깁니다** — 본문은 repro 명령과 캡처된 출력을 품은 JSON 문서라,
   셸 인자로 넘기면 중첩 escape를 손으로 다시 맞춰야 하고 한 글자만 어긋나도 repro가
   조용히 손상됩니다.
   ```bash
   # memory content를 그대로 파일에 기록한 뒤
   xm inbox materialize --content-file <path> --memory-id <memory id> --pin-id <pin id> --json
   ```
   `--content <json>` 인라인 형태도 여전히 동작하며, 둘 다 주면 인라인이 이깁니다.
   기존 pin처럼 toss id가 없는 항목은 title 또는 일반어로 추측 검색하지 않습니다. pin id와
   title을 보여 주고 발신 측에 재전달을 요청합니다. 이 CLI는 네트워크를 호출하지 않고
   **현재 cwd의** `.xm/inbox/<id>.json`에만 기록합니다. 따라서 materialize 명령은 반드시
   수신 프로젝트를 cwd로 하여 실행하고, 발신 프로젝트 경로·outbox·다른 checkout을 인자로
   넘기지 않습니다. malformed JSON이나 `to_project`가 현재 프로젝트와 다른 항목은 거부하고,
   이미 같은 id가 있으면 로컬 상태를 바꾸지 않습니다.
   MCP 검색을 할 수 없으면 그 사실을 밝히고 기존 로컬 원장만 조회합니다.
2. **`xm inbox list`** — materialize 뒤에 실행합니다. Prints unresolved items first, then
   in-progress, then resolved, then dismissed; add `--json` when you need to act on fields programmatically.
3. **Address items by `id` only**, never by a remembered list position — re-run `list`
   if unsure, since the sort order and the opportunistic archive sweep can shift between
   calls.
4. **`xm inbox take <id>`** when starting work on one: relay the full returned body
   (why / repro command+output / fix direction) to the user, or use it directly as the
   starting point for a fix — don't re-derive it from scratch. `take` writes
   `status: "in_progress"`; it never claims completion.
5. **`xm inbox resolve <id> --summary "..." --verification "..." --json`** only after the implementation and relevant verification
   have completed. `done` is an alias. Both flags are **required** and the command
   refuses the transition without them — a receipt is the only thing the sender ever
   sees, so one claiming "resolved" with no evidence closes the report against a fix
   that may not exist. `--verification` must name the concrete check you actually ran
   (command and its result, or the files/lines you confirmed); restating the summary
   is not verification. This writes the terminal `status: "resolved"`,
   creates an immutable receipt (terminal state, time, summary and verification evidence),
   and returns `mcp_calls`. Then, in order:
   - Call `mcp__mem-mesh__add` with `mcp_calls.add` **verbatim**, and record the
     returned memory id with `xm inbox receipt record <id> --memory-id <id>`.
   - If `mcp_calls.pin_complete` is present, call `mcp__mem-mesh__pin_complete` with it.
     The delivery pin otherwise stays `in_progress` forever and every later session
     start announces a report that is already closed.

   If MCP delivery fails or is unavailable, the terminal receipt remains locally `pending`;
   do not claim the sender was notified. Use `xm inbox receipt retry <id> --json` in a
   later MCP-capable session to obtain the same payload (including `pin_complete`), and
   `receipt status <id>` to report the local transport state.
6. **`xm inbox drop <id> --summary "..." --json`** when it doesn't need action.
   `--summary` is required — say why this project is not acting on the report — but
   verification is not, since nothing was fixed. It follows the same receipt-delivery
   and `pin_complete` process as resolve. If it's ambiguous whether an
   item is relevant, confirm with the user before dropping — treat the drop as final in
   conversation even though dismissed items remain recoverable in the archive on disk.
7. **Re-notify a dead pin yourself, when relevant.** For any `delivered`/`in_progress`
   item (plus legacy `actioned` items)
   whose `mem_mesh.pin_id` is set (visible via `xm inbox list --json`):
   - Call `mcp__mem-mesh__pin_get(pin_id)` yourself.
   - If it comes back not-found, OR `status: "completed"` (mem-mesh's 7-day auto-close —
     never a real user action on a delivery pin), the pin is dead: call
     `mcp__mem-mesh__pin_add(content="<item id> — <item title>", project_id=<this project's mem-mesh id>,
     tags=["inbox"])` to recreate it, then persist the new id:
     ```bash
     xm inbox record <id> --pin-id <new pin id> --scope inbox --json
     ```
   - If the pin is still `in_progress`, or the item is `resolved`/`dismissed`, do nothing — this
     matches `ledger.mjs`'s `reconcile()` rules exactly (dead pin + unresolved item →
     renotify; anything else → no action).
   - **If you have no MCP tools available at all** (plain shell, no Claude Code MCP
     session), skip this step entirely and say so — don't guess at pin state or claim
     re-notification happened.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll remember item #2 from the last list and take() it later." | Lists are re-sorted (unresolved-first) and re-swept (archive) on every call — position 2 can point at a different item next time. Always address by `id`. |
| "Inbox is empty, something's broken." | An empty inbox is a normal, valid state — say so; don't assume the CLI or mem-mesh is malfunctioning. |
| "`search(query=\"inbox\")`가 비었으니 새 수신함도 비었다." | `search`는 `tags` 필터가 없고 넓은 질의는 랭킹에서 밀린다. 먼저 `pin_list(tags=[\"inbox\"], limit=10)`으로 알림을 찾고 toss id로 정확히 검색한다. |
| "`pin_list(tags=[\"inbox\"])` 한 번이면 모든 상태가 나온다." | `status` 생략 시 서버 기본 상태만 반환될 수 있다. `open`, `in_progress`, `completed`를 각각 조회해 합쳐야 신규 delivery pin을 놓치지 않는다. |
| "I compared the pin list against `list`'s output by eye — same count, so nothing is missing." | Counting agrees even when a pin points at an id the ledger never had. `reconcile` diffs both directions by id; eyeballing missed exactly this for five days (`toss-20260721-666aa5a0`, taken 07-21, local file gone by 07-26, pin still `in_progress`). Run the command. |
| "list didn't print anything about pins, so they must all still be fine." | `list` never checks pin state (t11 — no network in the CLI). Silence from `list` says nothing about pin health; you have to actually call `pin_get` yourself to know. |
| "The memory body is short enough — I'll just paste it into `--content '...'`." | Bodies embed a repro command and its captured output, both of which routinely contain quotes, backslashes and newlines. Re-quoting them by hand corrupts the repro with no error — nothing validates the repro against its source. Write the body to a file and use `--content-file`. |
| "take() gave me the item, I'll now `later promote` it to keep the body." | `later promote` has no field for why/repro/fix_direction — the body does not survive that trip. Use the returned item content directly instead. |
| "The fix is obvious, I'll put 'fixed' in --verification and move on." | `--verification` is the sender's only evidence that this project checked anything. A restatement of the summary is what let 5 x-kit items sit marked done while only 2 were actually fixed. Name the command you ran and its result, or the file:line you confirmed. |
| "I resolved it and delivered the receipt — the pin will sort itself out." | Nothing closes a delivery pin but you. Left open it reads as an unhandled report at every future session start. If `mcp_calls.pin_complete` is in the output, call `mcp__mem-mesh__pin_complete` with it. |
| "take means the issue is done." | `take` means work started. Only `resolve` is terminal, and only after the fix and checks complete. |
| "I'll drop an item I'm not sure about, just to clean up the list." | Drop is for items that genuinely don't need action. When unsure, leave it `delivered` (or `take` it) and ask the user rather than guessing it away. |
| "No MCP tools here, I'll just tell the user the inbox looks fine." | The listed items are accurate (local files), but you silently skipped pin re-notification. Say explicitly that you couldn't check/renew pin state — don't imply you did. |
| "I recreated the pin via pin_add but that's the whole job, no need to persist it." | Without `xm inbox record --scope inbox`, the new pin id only lives in your chat output — the next session's ledger still points at the dead pin id and would recreate ANOTHER one. Always record it. |
| "The item is old, I'll delete the file myself." | Only the CLI's own opportunistic `archiveExpired()` sweep (run before every read) may relocate terminal items, and only after 30 days. Manual deletion bypasses the recoverable archive path entirely. |

## Red Flags

- You referenced an inbox item by list position instead of `id`.
- You decided what to materialize or renotify by reading the pin list yourself instead of running `xm inbox reconcile`.
- You used a generic memory search instead of an inbox pin's toss id to materialize a delivery.
- You dropped an item without the user's confirmation when its relevance was unclear.
- You called `resolve` before implementation and verification completed.
- You passed a `--verification` that restates the summary instead of naming a check you ran.
- You delivered a terminal receipt but skipped the `mcp_calls.pin_complete` call it returned.
- You treated a terminal local state as proof that the sender received its receipt.
- You claimed pin re-notification happened without actually calling `pin_get`/`pin_add`.
- You called `pin_add` to renotify but never ran `xm inbox record --scope inbox` afterward.
- You had no MCP tools available and didn't tell the user re-notification was skipped.
- You edited or deleted a `.xm/inbox/*.json` file directly instead of going through `take`/`drop`/`record`.

## Verification

- Every item referenced by `id`, matching what `list` printed.
- `take`'s full body (why/repro/fix) was relayed or acted on, not summarized away.
- Completed work was closed with `resolve`, while unfinished work remained `in_progress`.
- For resolve/drop, `mcp_calls.pin_complete` was called when present, so no closed item leaves an open pin.
- For resolve/drop, the receipt MCP call was delivered verbatim and its memory id recorded;
  otherwise the pending transport state was stated plainly and left retryable.
- Any pin re-notification you performed was via real `pin_get`/`pin_add` MCP calls, followed by `xm inbox record --scope inbox` — never assumed or skipped silently.
- If no MCP tools were available, that limitation was stated plainly, not glossed over.
- No direct file edits under `.xm/inbox/` — only via the CLI subcommands.
