---
name: commit-local-push-server
description: 'Commit local sau khi hoàn thành + auto push theo ngưỡng. Dùng khi: hoàn thành feature/bug/refactor, tự tóm tắt và commit. Hỗ trợ kiến trúc 14 repo độc lập: 1 Root + .github + Docker + 11 Portal.'
argument-hint: 'mode: -f/-F | target: all|jpayapp|jgame|invoiceapp|ketoanapp|.github|docker'
---

# Commit & Push — Kiến Trúc Nested Repos

> Dự án có **14 Git repo độc lập** (1 Root + `.github` + `Docker` + 11 Portal). Mỗi repo có `.git` và branch riêng.

---

## ⚡ Chạy Bằng Script (Khuyến Nghị — Tiết Kiệm Token)

> Agent **chỉ chạy script và kiểm tra kết quả** — không gõ thủ công `cd` + `git add` + `git commit` + `git push`. Script tự phát hiện repo, kiểm tra branch, đếm commit, phát hiện + commit thay đổi, và push kèm pull đồng bộ.

```bash
# 1. KHÔ (mặc định): phát hiện thay đổi chưa commit + liệt kê file + đếm commit — KHÔNG thay đổi gì
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs

# 2. COMMIT: commit các repo có thay đổi chưa commit (message tùy chọn)
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs --commit -m "feat(invoice): mô tả"

# 3. PUSH: pull --rebase đồng bộ + push các repo ĐỦ ngưỡng
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs --push

# 4. PUSH FORCE: push LUÔN, KHÔNG cần đủ ngưỡng (alias: -f / -F / --force / --push-luon / --push-ngay)
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs --push --force

# 5. TARGET: chỉ xử lý repo theo tên (all | jpayapp | invoiceapp,ketoanapp | .github | docker)
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs --target jpayapp
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs -t invoiceapp
node .claude/skills/commit-local-push-server/scripts/push-all-repos.cjs jpayapp crmapp   # positional
```

**Script tự động:**
- Khám phá **14 repo** (root + `.github` + `Docker` + các module portal có `.git`)
- **Lọc theo target**: `all` (toàn bộ) hoặc tên cụ thể (`jpayapp`, `invoiceapp`, `ketoanapp`, `.github`, `docker`)
- **Phát hiện thay đổi chưa commit** + liệt kê file → agent dùng `get_errors` kiểm tra lỗi nhanh
- Kiểm tra branch; **chặn commit/pull/push nếu không ở `development`** (Docker: `master`)
- Đếm commit chưa push (`origin/<branch>..HEAD`)
- `--commit`: tự `git add -A` + `git commit`; `--push`: `pull --rebase` trước rồi push (tránh non-fast-forward); `--push --force`: push luôn không cần đủ ngưỡng
- Ngưỡng push: Root ≥ 5, còn lại (portal/`.github`/`Docker`) ≥ 3

### LUỒNG ĐẦY ĐỦ

1. Chạy **KHÔ** → script liệt kê repo có thay đổi chưa commit + các file.
2. Agent chạy **`get_errors`** trên các file đó để kiểm tra lỗi nhanh. Có lỗi → sửa hết.
3. Không lỗi → chạy **`--commit`** để commit.
4. Chạy **`--push`** (đủ ngưỡng) hoặc **`--push --force`** (push luôn, bỏ ngưỡng).

---

## 📚 Rules Chi Tiết (mở khi cần)

Chi tiết về ánh xạ repo, nhánh, commit, push, an toàn force-push đã tách vào `rules/`:

| File | Nội dung |
|------|----------|
| `rules/01-anh-xa-repo-va-nhanh.rule.md` | Bảng ánh xạ file → repo (14 repo), quy ước nhánh `development`/`master`, ngoại lệ Docker |
| `rules/02-commit-va-push.rule.md` | Format commit message, cách commit theo repo, ngưỡng push, pull đồng bộ trước push |
| `rules/03-an-toan-khi-push-forc.rule.md` | Khi nào dùng `--push --force`, điều kiện an toàn, luồng kiểm tra trước commit |

---

## Quy Tắc Cốt Lõi

- ✅ Chỉ commit trên `development` (Docker: `master`); KHÔNG commit trên `main`.
- ✅ Chạy `get_errors` trên file vừa sửa trước khi commit.
- ✅ Pull `--rebase` đồng bộ code mới nhất TRƯỚC khi push.
- ✅ Dùng script thay vì gõ git thủ công khi chỉ cần commit/push.
