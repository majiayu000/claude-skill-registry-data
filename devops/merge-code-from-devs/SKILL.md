---
name: merge-code-from-devs
description: 'Quy trình nhập (merge) code từ nhánh developer (ví dụ: development-yen) vào nhánh chính (development) — THÔNG QUA SCRIPT AN TOÀN. Agent KHÔNG gọi lệnh git trực tiếp. Script tự: resolve đúng repo từ tên portal, kiểm tra trước (working tree sạch, đúng repo, không file xóa), tạo backup 2 bên (nguồn + đích), merge --no-ff, abort khi conflict, kiểm tra sau. Hỗ trợ kiến trúc 12 repo độc lập (1 Root + 1 Docker + 1 .github + 9 Portal).'
argument-hint: 'BẮT BUỘC 2 đầu vào: (1) repo portal: <tên-portal> (2) nhánh development-<tên>. VD: portal: kiemthu từ development-tuan'
---

# Merge Code Từ Developer Branch — SASUCO InvoiceEasy

> ⚠️ **TUYỆT ĐỐI KHÔNG tác động vào nhánh `main`** trong toàn bộ quy trình này.
> Chỉ làm việc với: `development` (nhánh nhận) và `development-<tên>` (nhánh nguồn).

> 🛑 **NGUYÊN TẮC CỐT LÕI (v2 — sau sự cố 13/08/2026):**
> **Agent KHÔNG gọi lệnh git trực tiếp.** Mọi thao tác git chạy qua **script** trong `scripts/`.
> Agent CHỈ: chạy script → đọc kết quả JSON → báo cáo → chờ user duyệt.
> Lý do: agent gọi git tay từng gây CWD sai repo → xóa file nested repos (sự cố 09/08 + 13/08).

> � **RÀNG BUỘC AGENT (bắt buộc tuyệt đối):**
> 1. **Chỉ được chạy script** (`node .../scripts/*.cjs`) và đọc output.
> 2. **KHÔNG được tự ý thực hiện bất kỳ lệnh git/khác nào** ngoài script (vd: `git merge`, `git checkout`, `git push`, `git reset`, `git stash`, sửa file repo...).
> 3. Khi script báo lỗi → chỉ **báo cáo lại cho user** kèm nội dung lỗi + gợi ý; KHÔNG tự sửa bằng lệnh tay.
> 4. Khi script yêu cầu xác nhận (exit 2 / `waiting-confirm`) → **DỪNG, báo user, chờ duyệt** rồi mới chạy lại với `--yes`.
> 5. Mọi kết quả đều lấy từ **JSON script xuất ra** — không tự suy đoán trạng thái git.

> 💡 **Nếu user gõ script trực tiếp (không qua skill) mà quên tham số:** script sẽ **hiển thị prompt hỏi nhập đầy đủ** `--portal`, `--branch`, `--target` (kèm danh sách giá trị hợp lệ). Khi chạy từ terminal thật (TTY), user nhập tay; khi agent chạy (không TTY), script báo lỗi yêu cầu truyền tham số.

> �📖 Tài liệu phân tích giải pháp đầy đủ: `docs/giai-phap-merge-an-toan-2026-08-13.md`

---

## B0 — Xác Định Repo Cần Merge (BẮT BUỘC ĐẦU TIÊN)

### 🎯 ĐẦU VÀO BẮT BUỘC (Hỏi user nếu thiếu)

| # | Đầu vào | Ví dụ |
|---|---------|-------|
| 1 | **Portal app cần merge** (nhánh nhận = `development` của repo đó) | `portal: kiemthu` / `portal: invoice` / `portal: ketoan` |
| 2 | **Lập trình viên nguồn** (nhánh nguồn = `development-<tên>`) | `development-yen` / `development-tuan` |

> ❌ Thiếu 1 trong 2 → **DỪNG và hỏi** (không đoán).

### 🚫 GIỚI HẠN PHẠM VI — CHỈ merge repo PORTAL app, CẤM TUYỆT ĐỐI mọi repo khác

> ⛔ **NGUYÊN TẮC CỐT LÕI: merge CHỈ được thực hiện giữa các branch trong repo PORTAL app**
> (thư mục `src/modules/<App>`). **CẤM tuyệt đối merge vào**:
> - ❌ **root** — `D:\JDX-SOUCRE-MAIN-FE-PORTAL\Jdx-portal-root`
> - ❌ **docker** — `D:\JDX-SOUCRE-MAIN-FE-PORTAL\Jdx-portal-root\Docker`
> - ❌ **agentskill** — `D:\JDX-SOUCRE-MAIN-FE-PORTAL\Jdx-portal-root\.github`
> - ❌ Bất kỳ thư mục/repo nào nằm NGOÀI `src/modules/`
>
> Lý do: các repo này quản lý cấu hình/deploy/skill toàn cục — merge sai sẽ lan tác động
> hoặc xóa file nested repos (sự cố 09/08 + 13/08/2026). Script **tự chặn cứng** ngay khi
> nhận `--portal root|docker|agentskill` hoặc path ngoài `src/modules/` (báo lỗi, exit 1).

### 🛡️ LỚP BẢO VỆ KỸ THUẬT — script tự kiểm tra TRƯỚC khi merge (tất cả đều BLOCK nếu sai)

| # | Lớp bảo vệ | Cơ chế | FAIL = |
|---|-----------|--------|--------|
| 1 | **Alias cấm** | `FORBIDDEN_MERGE_ALIASES` chặn ngay `root`/`docker`/`agentskill` khi nhận `--portal` | Dừng |
| 2 | **Phạm vi đường dẫn** | `resolveMergeRepoPath` yêu cầu repoPath nằm TRONG `src/modules/` (so sánh path chuẩn hóa) | Dừng |
| 3 | **show-toplevel khớp** | `git rev-parse --show-toplevel` phải bằng đúng thư mục repo mong muốn (chống CWD/alias sai) | Dừng |
| 4 | **Remote URL khớp** | `checkRemoteMatch` — origin URL phải chứa repo đúng của portal (vd `jdx-portal-kiemthu`). Chống **clone nhầm repo** vào thư mục portal | Dừng |
| 5 | **Validate branch** | `validateTargetBranch` + `validateSourceBranch` — đích phải `development*`, **nguồn phải `development-<tên>`**; cấm main/master, cấm merge chính nó | Dừng |

> ✅ **Chỉ cần 1 lớp FAIL → script DỪNG ngay, không merge.** Agent chỉ báo cáo kết quả JSON cho user.
> Lớp 4 là bổ sung mới (2026-08-13): ngăn trường hợp thư mục `src/modules/<App>` bị thay bằng clone của repo khác.

### Kiến trúc 12 repo độc lập

Dự án có **12 Git repo riêng biệt** (1 Root + 1 Docker + 1 `.github` + 9 Portal). Script resolve repo từ alias portal qua `PORTAL_MAP` — agent KHÔNG cần nhớ đường dẫn.

**✅ CHỈ 9 repo PORTAL app sau được merge (hợp lệ):**

| Alias (truyền `--portal`) | Thư mục git (so với root) |
|------|------------|
| `invoice` / `invoiceapp` | `src/modules/InvoiceApp/` |
| `admin` / `adminapp` | `src/modules/AdminApp/` |
| `partner` / `partnerapp` | `src/modules/PartnerApp/` |
| `sso` / `ssoapp` | `src/modules/SsoApp/` |
| `ketoan` / `ketoanapp` / `accounting` | `src/modules/KetoanApp/` |
| `crm` / `crmapp` | `src/modules/CrmApp/` |
| `taisan` / `taisanapp` | `src/modules/TaiSanApp/` |
| `kiemthu` / `kiemthuapp` | `src/modules/KiemThuApp/` |
| `baseindex` / `baseindexapp` | `src/modules/BaseIndexApp/` |

**🚫 CẤM TUYỆT ĐỐI (script từ chối exit 1 — kể cả khi user yêu cầu):**

| Alias | Thư mục git (so với root) |
|------|------------|
| `root` | `./` |
| `docker` | `Docker/` (chỉ 1 nhánh `master`) |
| `agentskill` | `.github/` |

> ⚠️ **Merge portal app → repo CHỈ nằm trong `src/modules/<App>`.** Script luôn chạy git với `cwd` chỉ định + kiểm tra `git rev-parse --show-toplevel` + **chặn phạm vi 2 lớp** (`FORBIDDEN_MERGE_ALIASES` + path nằm trong `src/modules/` ở cả `resolveRepoPath` lẫn `resolveMergeRepoPath`) + **kiểm tra remote URL** (`checkRemoteMatch`) — **không thể** lan sang root/docker/agentskill/portal khác kể cả khi terminal CWD sai hoặc thư mục bị clone nhầm repo.

---

## Quy Trình Tổng Quan (v2 — Script Tự Động)

> 🚀 **CÁCH NHANH:** Chạy **1 lệnh duy nhất `main-merge.cjs`** để tự động hoàn thành toàn bộ quy trình (pre-check → chờ duyệt → merge → post-check). Dùng 3 script bước rời khi cần tách kiểm soát từng giai đoạn.

```
B0: Xác định REPO (alias) + LẬP TRÌNH VIÊN nguồn — hỏi user nếu thiếu
B1: 🖥️ Chạy SCRIPT 0 — main-merge.cjs (điều phối) — KHÔNG --yes
    → Chỉ chạy pre-check → JSON { ok, errors, warnings } → exit 2 (chờ duyệt)
B2: Báo cáo kết quả pre-check cho user → 🛑 CHỜ DUYỆT
B3: 🖥️ Chạy LẠI main-merge.cjs --yes  (tự động: backup 2 bên + merge --no-ff + post-check)
    → JSON tổng hợp { backupsCreated, mergeCommit, ok, errors }
B4: Báo cáo tổng hợp → đóng task

─── HOẶC tách bước (khi cần kiểm soát từng giai đoạn) ───
B1: 🖥️ 1-check-pre-merge.cjs   (kiểm tra TRƯỚC)
B2: Báo cáo → 🛑 CHỜ DUYỆT
B3: 🖥️ 2-merge-safe.cjs        (backup 2 bên + merge --no-ff)
B4: 🖥️ 3-check-post-merge.cjs  (kiểm tra SAU)
```

> **Agent KHÔNG được:** gõ `git checkout/merge/push/reset/...` trong terminal. Mọi thứ script lo.

---

## B0.5 — SCRIPT 0: `main-merge.cjs` (Điều Phối — 1 Lệnh Hoàn Thành)

> Đây là **entry point chính** — 1 lệnh tự động chạy đủ quy trình. Không cần nhớ thứ tự 3 script.

```bash
# Bước 1 — chạy KHÔNG --yes (chỉ pre-check, DỪNG chờ duyệt, exit 2):
node .claude/skills/merge-code-from-devs/scripts/main-merge.cjs \
  --portal <alias> --branch <nguồn> [--target development]

# Bước 2 — sau khi user duyệt, chạy LẠI với --yes (merge + post-check, có thể thêm --push):
node .claude/skills/merge-code-from-devs/scripts/main-merge.cjs \
  --portal <alias> --branch <nguồn> [--target development] --yes [--push]
```

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|:---:|-------|
| `--portal <alias>` | ✅ | **CHỈ portal app** (`kiemthu` / `ketoan` / ...) — cấm `root`/`docker`/`agentskill` |
| `--branch <nguồn>` | ✅ | Nhánh dev nguồn (vd `development-tuan`) — **phải bắt đầu `development-`** (nhánh cá nhân); **cấm** `main`/`master`/`development` (nhánh chính)/branch lạ làm nguồn |
| `--target <đích>` | ❌ | Mặc định `development` — **phải bắt đầu `development*`**, cấm `main`/`master` |
| `--yes` | ❌ | Có thì chạy trọn (merge + post-check); thiếu thì chỉ pre-check rồi dừng — **bắt buộc cho cả `main-merge` lẫn `2-merge-safe`** |
| `--push` | ❌ | Có thì push `origin/<đích>` sau merge (mặc định KHÔNG push) |

> 🔴 **Ràng buộc branch (script tự chặn):** `--target main/master` ❌ | `--target` không bắt đầu `development` ❌ | `--branch main/master` ❌ | `--branch development` (nhánh chính) ❌ | `--branch` không bắt đầu `development-` (branch lạ) ❌ | `--branch` trùng `--target` ❌ (merge chính nó).

**Luồng bên trong (`main-merge.cjs`):**

```
[B1] PRE-CHECK   → resolve repo + show-toplevel khớp + fetch + working tree sạch
                   + branch tồn tại + không file xóa (D) → lỗi chặn = DỪNG ngay
[B2] CONFIRM     → không --yes: dừng (exit 2) để agent báo cáo, chờ user duyệt
[B3] MERGE-SAFE  → backup 2 bên IDEMPOTENT (chỉ tạo mới nếu CHƯA có backup cùng commit;
                   chạy lại nhiều lần sẽ DÙNG LẠI backup cũ, không tạo trùng)
                   + switch <đích> + merge --no-ff (conflict → abort, KHÔNG resolve)
[B4] POST-CHECK  → đúng branch + tree sạch + backup còn + mọi commit nguồn vào đích
```

**Exit code:** `0` = xong toàn bộ · `1` = lỗi chặn/abort · `2` = pre-check PASS, đang chờ duyệt (chạy lại với `--yes`).

---

## B1 — SCRIPT 1: Kiểm Tra TRƯỚC

```bash
node .claude/skills/merge-code-from-devs/scripts/1-check-pre-merge.cjs \
  --portal <alias> --branch <nguồn> [--target development]
```

**Script tự kiểm tra (mỗi mục FAIL đều chặn merge):**

| # | Kiểm tra | FAIL = |
|---|----------|--------|
| 1 | Portal hợp lệ + repo tồn tại + `.git` + repoPath nằm trong `src/modules/` | Dừng |
| 2 | `show-toplevel` khớp repo mong muốn | Dừng (chống sai repo) |
| 2b | **Remote URL khớp** — origin chứa repo đúng của portal (vd `jdx-portal-kiemthu`) | Dừng (chống clone nhầm repo) |
| 3 | Working tree sạch (không tracked M/D) | Dừng |
| 4 | Branch nguồn tồn tại (local/remote) | Dừng |
| 5 | Branch đích tồn tại | Dừng |
| 6 | Diff nguồn..đích KHÔNG có file xóa (D) | Dừng (chống mất code) |
| 7 | **🔴 Nguồn phải chứa MỌI commit của đích** (`git rev-list --count nguồn..đích` = 0) | **Dừng — BẮT BUỘC cập nhật nhánh nguồn trước** |
| 8 | **🔴 Branch hợp lệ** (`--target` ≠ main/master, bắt đầu `development*`; **nguồn phải bắt đầu `development-`** (vd `development-tuan`), cấm `main`/`master`/`development`/branch lạ) | Dừng |

**Exit code:** `0` = sẵn sàng · `1` = lỗi chặn · `2` = cảnh báo (báo user quyết định).

**Cảnh báo (KHÔNG chặn — chỉ báo user xác nhận):**
- Nhánh nguồn không có commit mới so với đích (merge sẽ tạo commit rỗng)
- Đã tồn tại nhánh backup (script sẽ dùng lại, không tạo trùng)

**Agent đọc JSON → báo cáo user:**
```
✅ Pre-check PASS: repo đúng (show-toplevel khớp, remote jdx-portal-kiemthu khớp),
   working tree sạch, nguồn development-tuan có 90 commits mới, không file xóa.
⚠️ WARN: đã có 2 nhánh backup — script sẽ dùng lại backup cùng commit, không tạo trùng.
👉 Có merge không? (yes/no)
```

---

## B2 — 🛑 CHỜ USER DUYỆT (BẮT BUỘC)

> KHÔNG chạy 2-merge-safe khi chưa có xác nhận `yes`. Lỗi chặn (exit 1) → tuyệt đối không merge.

---

## B3 — SCRIPT 2: Merge An Toàn (Backup 2 Bên)

```bash
# KHÔNG --yes → chỉ pre-check rồi DỪNG (exit 2, chờ duyệt) — KHÔNG merge
node .claude/skills/merge-code-from-devs/scripts/2-merge-safe.cjs \
  --portal <alias> --branch <nguồn> [--target development]

# Có --yes → thực hiện merge thật
node .claude/skills/merge-code-from-devs/scripts/2-merge-safe.cjs \
  --portal <alias> --branch <nguồn> [--target development] --yes [--push]
```

> 🔴 **Bắt buộc `--yes`** — nếu chạy `2-merge-safe` trực tiếp không có `--yes`, script chỉ chạy pre-check rồi DỪNG (exit 2). Không có cơ chế "merge ngầm".

**Script tự thực hiện (an toàn tuyệt đối):**

```
1. Resolve repo từ alias → verify .git + show-toplevel khớp + validate branch (chặn main/lạ/trùng)
2. Chạy lại pre-check (lỗi chặn → ABORT ngay) — không --yes: DỪNG chờ duyệt (exit 2)
3. git fetch origin (lỗi mạng → WARN, không chặn)
4. Đảm bảo branch nguồn local
5. TẠO BACKUP 2 BÊN IDEMPOTENT (git branch — không đổi working tree):
     backup/<nguồn>-<ts>   backup/<đích>-<ts>   (dùng lại nếu đã có cùng commit)
6. git switch <đích>
7. git merge <nguồn> --no-ff --no-edit
   → FAIL/CONFLICT: git merge --abort → báo lỗi (KHÔNG resolve thủ công)
8. [--push] git push origin <đích>   (mặc định KHÔNG push)
```

**Exit code:** `0` = merge thành công · `1` = lỗi (đã abort, working tree nguyên trạng).

**Agent đọc JSON → báo cáo:**
```
✅ Merge thành công: backup/development-tuan-20260813-153000, backup/development-20260813-153000
   Merge commit: abc1234
```

---

## B4 — SCRIPT 3: Kiểm Tra SAU

```bash
node .claude/skills/merge-code-from-devs/scripts/3-check-post-merge.cjs \
  --portal <alias> [--target development] [--source <nguồn>]
```

**Script tự kiểm tra:**
1. Remote URL khớp repo portal mong đợi (chống kiểm tra nhầm repo)
2. Branch hiện tại — **CHỈ CẢNH BÁO** nếu không ở đích (vì `main-merge`/`2-merge-safe` tự quay về branch gốc sau merge — không còn là lỗi chặn)
3. Working tree sạch sau merge
4. Nhánh backup tồn tại
5. `git log <đích>..<nguồn>` rỗng → mọi commit nguồn đã vào đích (bắt buộc truyền `--source <nguồn>`)
6. HEAD là merge commit hợp lệ

**Exit code:** `0` = đạt · `1` = có vấn đề (báo user, dùng backup khôi phục).

---

## B5 — Báo Cáo & Đóng Task

```markdown
## 📋 BÁO CÁO MERGE — {Tên repo} `{nguồn}` → `{đích}`

| Bước | Kết quả |
|------|---------|
| Pre-check | ✅ PASS (hoặc ⚠️ WARN N) |
| Backup | `backup/{nguồn}-{ts}`, `backup/{đích}-{ts}` |
| Merge | ✅ commit `{hash}` (hoặc ❌ abort — conflict) |
| Post-check | ✅ PASS |
| Push | ✅/❌ (--push) |
```

- Lỗi chặn (pre-check FAIL / merge abort) → báo user hướng khắc phục, **không tự ý merge**
- Thành công + user duyệt → có thể `--push`

---

## Quy Tắc Vàng

| ✅ ĐƯỢC | ❌ KHÔNG ĐƯỢC |
|---------|--------------|
| Chạy script trong `scripts/` + đọc JSON | **Gọi lệnh git trực tiếp trong terminal** |
| Chỉ chạy script, nhận kết quả, báo cáo user | **Tự ý thực hiện bất kỳ lệnh khác** (git/script/sửa file repo) ngoài script |
| Hỏi đủ 2 đầu vào: portal app + dev nguồn | Merge khi thiếu thông tin (đoán mò) |
| Truyền `--portal` đúng alias 1 trong **9 portal app** | **Merge vào root / docker / agentskill / repo khác** — script chặn (exit 1); agent không được hỏi, đề xuất, hay làm theo nếu user yêu cầu merge repo cấm |
| `--target` bắt đầu bằng `development` (vd `development`) | **`--target main/master`** hoặc target lạ (script chặn) |
| `--branch` là nhánh cá nhân `development-<tên>` (vd `development-tuan`) | **`--branch main/master`**, **`--branch development`** (nhánh chính), branch lạ, hoặc **`--branch` trùng `--target`** (script chặn) |
| Chạy trên đúng repo portal (remote khớp, show-toplevel khớp) | Merge khi repo sai / remote lạ / clone nhầm repo (script chặn) |
| Đọc kết quả `1-check-pre-merge` → chờ user duyệt | Tự merge khi chưa xác nhận |
| Để script tạo backup 2 bên | Tự tạo/xóa backup thủ công |
| Merge `--no-ff` (script tự) | `--squash` / `--ff-only` |
| Conflict → script abort (báo user) | Agent tự resolve conflict / `git checkout --ours/--theirs` |
| Kiểm tra post-merge trước khi báo thành công | Bỏ qua post-check, báo "xong" vội |
| Chỉ merge repo được chỉ định (script cô lập) | Merge lan sang repo khác |

> 🛡️ **Script KHÔNG chứa lệnh xóa/reset commit** (`git reset`, `git branch -D`, `git push --force`, `git clean`). Backup tạo ra không bị script xóa — giữ làm phao cứu sinh.
>
> 🧑‍💻 **User chạy trực tiếp:** nếu quên tham số, script hiển thị prompt nhập đầy đủ `--portal` / `--branch` / `--target` kèm danh sách hợp lệ — gõ giá trị rồi Enter để tiếp tục.

## Xử Lý Sự Cố

| Tình huống | Cách xử lý |
|-----------|-----------|
| `1-check-pre-merge` FAIL "SAI REPO" | Báo user, chạy lại với `--portal` đúng |
| `1-check-pre-merge` FAIL "working tree bẩn" | Báo user commit/stash trước |
| `1-check-pre-merge` FAIL "file xóa (D)" | BLOCK — nhánh nguồn đi sau, cần cập nhật nguồn trước |
| `1-check-pre-merge` FAIL "THIẾU N commit của đích" | **BLOCK — BẮT BUỘC nhánh nguồn phải merge `development` vào rồi push TRƯỚC, sau đó mới merge lại** |
| `2-merge-safe` abort (conflict) | Báo user, dùng backup hoặc cập nhật nguồn trước khi merge lại |
| `3-check-post-merge` FAIL | Báo user, hướng dẫn khôi phục từ `backup/*` |
| Script lỗi runtime | Báo user kèm log — không tự sửa script trừ khi được yêu cầu |
