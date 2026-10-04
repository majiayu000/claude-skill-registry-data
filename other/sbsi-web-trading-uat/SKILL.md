---
name: sbsi-web-trading-uat
description: "Execute SBSI Web Trading (Maris Web / Core FLEX UAT at trading-uat.sbsi.vn) UAT test cases assigned to the current tester's PIC only — look up business rules first, drive the app via Claude in Chrome, verify results against the real order book, write a per-case report with evidence and UI/UX feedback, read test cases from and write clean Pass/Fail results back to the team's UAT Google Sheet (KỊCH BẢN KIỂM THỬ – Web Trading Online), and keep a local markdown tracker. Use when asked to run/continue SBSI Web Trading UAT tests, a TC_WEB_* test case, or anything about đặt lệnh, sổ lệnh, bảng giá, lô lẻ, sức mua, phong tỏa on trading-uat.sbsi.vn, or to update the UAT test sheet / tracker."
---

# SBSI Web Trading UAT execution

Claude Code version of the team's Web Trading UAT workflow. It merges the
original claude.ai `sbsi-web-trading-uat` skill (PIC scope + safety
rules; its MISO Dashboard sync is replaced by the UAT Google Sheet) with
the useful parts of the Antigravity `sbsi-web-trading-tester` skill (business-rule lookup, execution checks, evidence, report template,
UI/UX feedback). Browser driving is done with **Claude in Chrome**
(`mcp__claude-in-chrome__*` — invoke the `claude-in-chrome` skill first),
not Python/Playwright/CDP scripts.

Per-case flow:

```
0 Clarify → 1 Browser session → 2 Account & PIC → 3 Business-rule lookup
→ 4 Execute & capture evidence → 5 Report → 6 UI/UX feedback
→ 7 Local tracker + Google Sheet update (+ Jira defect only if asked)
```

## Step 0 — Clarify before acting (anti-hallucination, hard rule)

Never fill a gap with a plausible guess. If any item below is not stated
in the current chat, in the UAT sheet, or in a file you actually read this session,
**stop and ask the user** (one `AskUserQuestion` call can batch up to 4
questions) before continuing:

| Unknown | Ask, don't guess |
|---|---|
| Tester's PIC | "Bạn test với PIC nào (vd BaoDK)?" — the scope rule below depends on it |
| Which account / sub-account (`01` thường, `06` ký quỹ…) | Only use an account the user explicitly authorizes for that PIC |
| Which test case(s) | The exact Test ID(s), or "next `Untest` row of my PIC in the sheet" |
| Expected result | Take it from the sheet's column D. If it's ambiguous or empty, ask — never invent expected behavior |
| What to write in columns E/H when they already have content | Show the existing text and ask: keep, append, or replace |
| Test data (symbol, side, price, volume, order type) | If the case doesn't pin it down, propose values and get a yes before placing any order |
| Business rule (price band, lot size, fee, status name…) | Look it up (Step 3). If no source covers it, ask — say "chưa có nguồn xác nhận", don't state it as fact |
| Path to the HDSD folder / result file | Ask once per machine; don't assume `C:\Users\AD\...` or any other path from an old skill |
| Whether an ambiguous observation is Pass or Fail | Report what you saw, mark ⏳ Partial, and ask |
| Anything that changes shared state or leaves the machine (Jira, git, shared-account settings) | Ask first — see "Never do without the user's explicit go-ahead" |

Also, when reporting: separate **observed** (seen on screen this session)
from **inferred**, and never claim a screenshot, file, order or sync exists
unless a tool result in this session proved it.

## Scope — the tester's own test cases ONLY (hard rule, no exceptions)

Only ever execute, mark, or sync test cases whose **PIC Nghiệp vụ**
(column G of the UAT sheet) is the current tester's PIC (confirmed in
Step 0).
Known PICs: BaoDK, NgaMTQ, AnhLL, BachNT, LongNH, CuongNT — each owns
their own cases. Never touch, run, or change the status of another PIC's
test case, even if it looks trivial or nobody seems to be testing it.

Before acting on any test case:
1. Read its row from a fresh CSV export (Step 7b) and check column G.
2. If PIC ≠ your PIC, skip it entirely — do not open, test, mark, or sync.
3. When picking "what's next," filter the exported rows to your PIC first
   and work only within that list. Consecutive Test IDs are frequently
   owned by different testers, so never walk sequential IDs across the
   ~500-TC sheet.

If it's discovered mid-session that already-tested/synced cases weren't
yours, stop, flag it with the exact Test IDs and their real PIC, and ask
whether to revert those rows to `Untest`. If the user says not to revert,
leave them and narrow scope going forward.

## Key URLs & accounts

- App under test: https://trading-uat.sbsi.vn/priceboard ("Maris Web").
- UAT test sheet (source of test cases AND where results go):
  https://docs.google.com/spreadsheets/d/1h7OFH0E7nySstbyY9ffyMYw350vT1hX_j0yX5hYmoBM/edit?gid=581688525#gid=581688525
  — tab "KỊCH BẢN KIỂM THỬ", Web Trading Online (Maris Web), `TC_WEB_*`.
  Layout in Step 7b.
- The MISO Dashboard is **no longer** the place to record results. Don't
  write to it.
- Authorized account per PIC — **only these are authorized**:
  - BaoDK → **088C024014** (Claude may type the account number).
  - Any other PIC → ask the user for their authorized account. Don't reuse
    one from this list for a different PIC.
- Do **NOT** use 088C096969, or any account number seen in the sheet's test-case
  notes/sample data, or the accounts listed in the old Antigravity
  `uat_accounts.json` (088C115858, 088C000922, 088C030413). Use one only
  if the user explicitly authorizes it in the current chat.
- This skill deliberately stores **no passwords, PINs, or OTPs**.

## Credential-entry rule (hard rule, no exceptions)

Claude must **never type into a password, PIN, or OTP field** — not the
real value, and not a deliberately wrong one for a negative test. The
platform's safety classifier blocks this ("Credential Leakage" / "Security
Weaken"). For any step that needs a password/PIN/OTP (correct OR wrong),
stop, ask the user to type it into the browser, then continue. Never work
around this. The PIN-confirm popup of an order is therefore always a
hand-off point.

## Step 1 — Browser session (Claude in Chrome)

1. Invoke the `claude-in-chrome` skill, load its tools in one `ToolSearch`
   call, then `tabs_context_mcp`.
2. Reuse the user's logged-in Chrome session. If there's no
   `trading-uat.sbsi.vn` tab, open a new tab to it — don't reload an
   existing tab that holds state the user is working with.
3. If not logged in, type the account number, then hand off for the
   password (credential rule).

## Step 2 — Account & sub-account

Confirm on screen (header account badge + sub-account dropdown) that the
active account and sub-account match what Step 0 settled. If they differ,
switch via the UI (native `<select>` → `find` + `form_input`) or ask.

## Step 3 — Business-rule lookup before acting

Before judging a result, find the rule it's judged against:

1. The sheet row's own steps (column C) and expected result (column D) —
   primary source.
2. `references/trading-rules.md` — price bands, price steps, lot sizes,
   order statuses, buying-power formulas. Marked **unverified**: confirm
   against HDSD/current regulation before citing a number as the reason
   for a Fail.
3. The team's HDSD folder, if the user has one on this machine (path
   confirmed in Step 0). Relevant subfolders in the original setup:
   `02_SBSI_Web_App` (screen analyses, order edge-case matrices, BRD lưu
   lệnh, `dataset_web_standard.json`), `01_FLEX_BackOffice` (FLEX order
   accounting, sub-account `01`/`06` blocking), `09_UAT_Testing` (previous
   UAT findings — check for known regressions). Read PDF/xlsx with the
   `pdf`/`xlsx` skills. If the folder isn't available, say so and ask
   rather than citing a document you haven't read.

## Step 4 — Execute & capture evidence

Execution rules:
- **Anti-warrant**: when typing a stock symbol, pick the suggestion whose
  first token equals the symbol exactly; reject `C<symbol>…` covered
  warrants and anything labelled "Chứng quyền".
- **Price within band**: read the live Trần/Sàn/TC for the symbol from the
  screen and check the input price is inside the band and on a valid price
  step (unless the case is a negative test of exactly that).
- **Units**: Maris shows prices ÷1,000 (20,950đ is entered as `20.95`).
- **Verify in the real order book**: an order case is Pass only when the
  order row actually appears in Sổ lệnh (Trong ngày) with the expected
  status (`Chờ gửi` / `Chờ khớp` / …). A success toast alone is not proof.
- **Clean up** orders you placed (cancel) if the case or the user expects
  it, and note it in the tracker — cancelling needs the PIN hand-off too.
- UI selector hints from the old skill are in
  `references/selector-hints.json` — **unverified**, use them only for
  read-only `javascript_tool` queries and confirm with `find`/`read_page`.

Evidence — for order-placing cases take a separate screenshot at each of
these 4 checkpoints (never reuse one image for two checkpoints):
1. Order form (symbol, price, volume, order type visible)
2. Confirm popup (before the user types the PIN)
3. Order book row
4. Asset / buying power after the order

Other cases: one screenshot per verified expectation. If the session can't
save screenshots to disk, say so in the report and describe what each one
showed. Never write a file path to an image that doesn't exist. Use
`gif_creator` if the user wants a recording of a multi-step flow.

## Step 5 — Per-case report

Use `references/report-template.md`. Result is **PASS / FAIL / BLOCKED /
SKIPPED**, based only on what you observed. Save it next to the local
tracker (ask for the folder once) as `test_report_<TestID>.md`, unless the
user says the tracker row alone is enough.

## Step 6 — UI/UX feedback

Add a short feedback section to the report, based only on what you
actually interacted with in this case:
- **Friction & flow**: unnecessary steps/clicks, missing autofocus, Enter
  not submitting.
- **Visual hierarchy & contrast**: price colors follow the Vietnam
  convention (see `.claude/rules/design-system.md` → `Text.Price.*`),
  number readability.
- **Feedback & error handling**: error messages clear to a retail
  investor, or raw technical codes?
- **Performance**: PIN popup latency, delay before the new row appears in
  Sổ lệnh (state the observed time, don't estimate).

Split into **Quick-wins** and **Strategic improvements**. Skip the section
for a case with nothing to observe, and don't pad it.

## Step 7a — Local result file (tracker)

A markdown file with per-module tables (`| Test ID | Scenario | Status |
Notes |`, legend ✅ Pass · ❌ Fail · ⏳ Blocked/Partial · ⚪ Not run ·
⏭️ Skipped). Default path `~/Documents/SBSI_WebTrading_UAT_TestResults.md`.
Confirm the path with the user the first time, then edit it directly with
Edit/Write.

Update it immediately after **every** test case, including Blocked/
Skipped/Partial ones with a clear reason. Never batch updates, so progress
survives a context loss. Entries already logged for other PICs don't need
to be stripped out — just don't add more.

(claude.ai / Cowork only: edit a cloud working copy, then push it to the
user's machine via `mcp__remote-devices__device_commit_files` after every
case. If the device bridge is unavailable, tell the user their computer
isn't reachable.)

## Step 7b — UAT Google Sheet: read test cases, write results

**Layout** (tab gid `581688525`; header rows 10–11, data from row 12;
section rows such as "Phân hệ …" / "UC01: …" have no Test ID in column A):

| Col | Header | Who writes |
|---|---|---|
| A | Mã trường hợp kiểm thử (`TC_WEB_UCxx_nnn`) | never |
| B / C / D | Mục đích / Các bước thực hiện / Kết quả mong muốn | never — test definition |
| E | Kết quả thực tế | Claude, observed result only |
| F | Kết quả hiện tại — `Pass` / `Fail` / `Untest` / `Pending` / `Cancel` | Claude, `Pass`/`Fail` only |
| G | PIC Nghiệp vụ | never |
| H | Ghi chú | Claude, short note: date, account/sub-account, evidence/report file |

Rows 4–8 (P / F / PE / chưa thực hiện / tổng) are summary counters.
Never edit them.

**Read** (no login needed while the sheet is link-readable). Finding
cases costs one script call. Don't spend time or tokens on it any other
way:

```bash
S=.claude/skills/sbsi-web-trading-uat/scripts/uat-sheet.ts
bun $S --pic BaoDK --status Untest --brief --limit 10   # 1) pick: one short line per case
bun $S --id TC_WEB_UC24_105                             # 2) full detail for the ONE case you'll run now
```

- Always list with `--brief` (sheetRow, id, status, purpose). For 28 cases
  that's ~3 KB instead of ~16 KB of full JSON. Add `--limit` when you only
  need the next few. The header line still shows the total match count.
- Pull full detail (steps/expected/actual/note) with `--id` only for the
  case you're about to execute. Never dump the whole list in full.
- Other useful filters: `--status Pending` / `--status Fail` (re-test),
  `--pic` + no status (overview). Use the section order (sheetRow) to batch
  related cases, e.g. all logged-out cases or one UC, in one browser pass.
- Never search the sheet through Chrome, `WebFetch`, or by reading the
  CSV yourself. The script is the only search path.

The script fails loudly if the export isn't reachable, the column layout
moved, or an `--id` doesn't match exactly one row. On failure, stop and
tell the user. Don't guess row numbers or read the sheet some other way
without their OK.

**Write** — only a **clean ✅ Pass or ❌ Fail** whose column G is
confirmed to be your PIC. Never write Partial/Blocked/Skipped results.
Record those only in the local tracker, and ask the user before setting
`Pending`/`Cancel`. Never write another PIC's row. One case at a time:
1. Re-run the script with `--id <TestID>` **right before writing**. Rows
   shift when someone inserts a line. Take `sheetRow` from this fresh read
   only, and confirm `pic` is yours. If E or H already has content, show it
   and ask: keep, append, or replace (Step 0).
2. In Chrome (the user's Google account must have edit access), open the
   sheet URL. Go to the cell via the **Name box**: `find` "Name box",
   click it, type `F<sheetRow>`, then Enter. Check that the Name box shows
   that address and the row's column A shows the Test ID (screenshot or
   `get_page_text`) before typing anything.
3. Type the value, then Enter. Status is exactly `Pass` or `Fail`, matching
   the sheet's dropdown values. Fill E and H the same way, one cell at a
   time. Don't paste multi-cell ranges. Don't use `javascript_tool` to
   write.
4. Verify: re-run `--id <TestID>` and confirm F/E/H now hold exactly what
   you typed, and that rows 4–5 moved by exactly one. The export can lag a
   few seconds; re-read, don't assume. If it doesn't match, stop and
   re-check before the next case. Never chain writes without verifying.

Why: the old MISO flow once marked the wrong row Pass because the target
row wasn't pinned down first. Separately, cases owned by LongNH (UC04–UC09)
were run and partly synced by mistake. Always re-read, then verify the PIC
and the row, then write.

Never sort, filter-in-place (use a filter *view* if needed), delete, or
insert rows/columns in the shared sheet. Other testers work in it at the
same time.

## Step 7c — Jira defect (optional, ask first)

For a ❌ Fail, offer to file a defect. Don't create one automatically.
Only on a yes: follow `.claude/rules/jira.md` / the `jira-workflow` skill
(verify site + project first, nothing is hardcoded). Include Test ID,
steps, expected vs actual, and the evidence descriptions/files.

## Guest / logged-out test cases

Batch your own logged-out cases: log out via the account switcher ("Đăng
xuất tất cả tài khoản"), run all of them in one pass, then log back in once
(pausing for the user's password).

## Known environment quirks & gaps

- Claude in Chrome flakiness ("Cannot access a chrome-extension://..." on
  screenshot/click/javascript_tool while `get_page_text`/`find`/`navigate`
  still work) is transient instability, not anti-automation (no
  debugger/webdriver detection in the JS bundle). Just retry.
- A "Không thể tải về dữ liệu... Khoảng thời gian không hợp lệ" toast on
  the UAT price feed is usually leftover state (stale date range) or a
  feed hiccup, not necessarily a bug in the feature under test.
- Guest mode has been observed both ways: earlier, no price data /
  "Không tìm thấy kết quả". On 2026-09-14 it showed full live data. Always
  re-verify it against the specific test's expectation. Never silently
  overwrite a recorded sheet result when behavior contradicts it; ask.
- Native `<select>`: `find` + `form_input`, never visual click (the OS popup
  isn't in CDP screenshots). Some (e.g. login's "Phiên đăng nhập kết thúc
  sau") aren't in the accessibility tree at all. Don't guess their options
  from a screenshot. Mark them unverifiable or ask the user.
- Validation is inconsistent across flows (e.g. duplicate-name check works
  on create but not on rename). Treat that as a real Fail. Confirm by
  re-running with fully correct data.
- Known data gaps — mark ⏭️ Skipped with the reason, never fabricate:
  - UC56 "Đăng ký Dịch vụ SMS" not in the Tiện ích menu.
  - UC03 / anything needing a Môi giới (broker) account: none available.
  - UC57 margin sub-account registration needs a real CCCD photo.
  - UC19 account list needs a second authorized logged-in account.
  - UC58 needs a margin sub-account + configured financial products; the
    Tiểu khoản dropdown only shows the empty placeholder.
  - Preconditions Claude can't create (e.g. an unread notification for a
    badge-count test).

## Never do without the user's explicit go-ahead

- "Success" cases that **change shared account state**: reset/change login
  password, PIN, transaction password, 2FA method. Skip with a note and ask,
  and run them last if approved.
- Deliberately triggering lockout (10 wrong logins) or the 5-attempt
  captcha.
- Flipping a recorded sheet result (Pass↔Fail), or overwriting existing
  text in columns E/H. Confirm first, citing what changed.
- Testing, marking, or syncing another PIC's test case.
- Creating a Jira issue, committing/pushing, or writing to any shared
  store other than the local tracker and columns E/F/H of your own rows
  in the UAT sheet.

## Deliberately not ported from the Antigravity skill

- Python/Playwright/CDP scripts (`sbsi_browser.py`, `run_testcase.py`,
  per-case `execute_*`/`run_case_*`): replaced by Claude in Chrome.
- `sbsi_sync_portal.py` 5-tier sync (dataset mirrors, HTML dashboards,
  `extract-legacy.mjs`, Cloudflare KV, auto squash-merge to `main`): it
  lives in another repo and auto-merges, which conflicts with this repo's
  draft-PR rule. Results go to the UAT Google Sheet (Step 7b) instead. Ask the
  user before touching that pipeline.
- `uat_accounts.json` with plaintext PINs/OTPs: conflicts with the
  credential rule.
- The "2-minute SLA": not realistic with hand-offs for PINs. Correctness
  comes first.
