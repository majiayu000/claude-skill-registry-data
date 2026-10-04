---
name: sdd-rfc
description: Quản lý RFC để sửa CONSTITUTION.md hoặc thay đổi kiến trúc lớn
user-invocable: true
---

# SDD RFC Manager (`/sdd-rfc`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PROPOSED`, `APPROVED`, `PENDING HUMAN REVIEW`), RFC identifiers (`RFC-XXX`), rule codes, file paths, and CLI commands are language-invariant.

Dùng khi cần đề xuất thay đổi/bổ sung quy tắc trong `CONSTITUTION.md` thuộc Layer 1 Hard Rules hoặc Layer 2 Architectural Constraints sau khi template đã phát hành. Một explicit Human authorization cho một đợt phát hành template không tạo quyền mặc định cho Agent sửa Constitution.

## Tham số

- `--title=<short-title>`: Tiêu đề ngắn, ví dụ `soft-delete-policy` hoặc `jwt-expiry-standard`.
- `--approve=<rfc-number>`: Chỉ Tech Lead/Human Director được dùng để phê duyệt RFC và đồng bộ Constitution.

## Quy trình

1. **Tạo RFC**
   - Không truyền `--approve`: tạo `.sdd/rfcs/RFC-XXX-<title>.md`, đánh số liên tục `RFC-001`, `RFC-002`, ... và status ban đầu `PROPOSED`.
2. **Điền template RFC**
   - Bắt buộc có `Motivation`, `Proposed Change`, `Risk Assessment` và `Migration Plan`.
   - Quy tắc mới dùng code `SEC-XX`, `DATA-XX`, `ARCH-XX` hoặc `ENG-XX` khi phù hợp.
3. **Phê duyệt và đồng bộ**
   - Chỉ RFC đã `APPROVED` bởi Tech Lead/Human Director mới được đồng bộ vào `CONSTITUTION.md`.
   - Bump patch/minor version của Constitution theo semantic impact.

## AI Recommendation và Human Final Review

Sau khi soạn hoặc đánh giá RFC, tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm motivation, alternative, security/architecture impact, migration risk và disposition đề xuất. Lưu trong RFC hoặc `.sdd/reviews/rfc-<number>.md` với `PENDING HUMAN REVIEW`. Chỉ Tech Lead/Human Director được ủy quyền có thể approve RFC và thay đổi Constitution; Agent không tự approve.

## Hướng dẫn sử dụng
- **Khi dùng:** Propose or authorizedly approve a Constitution Layer 1/2 or major architecture change.
- **Không dùng:** Không dùng để approve feature artifacts, patch source directly, or substitute `/sdd-review` for RFC approval.
- **Input:** `--title` creates a proposal; `--approve=<RFC-XXX>` is restricted to authorized Tech Lead/Human Director; reject missing migration/risk evidence.
- **Điều kiện trước:** Constitution and existing RFC sequence are readable; approval authority must be explicit and persisted by project governance.
- **Evidence:** RFC file with motivation/change/risk/migration, recommendation block, status and Constitution version impact.
- **Dừng khi:** Missing authority, conflicting rule, incomplete migration/risk, invalid RFC ID or attempted direct Constitution write.
- **Human quyết định:** Authorized Tech Lead/Human Director approves RFC; Agent never self-approves or treats template authorization as ongoing authority.
- **Lệnh tiếp theo:** `/sdd-rfc --approve=<rfc-number>` only when authorized; then follow the RFC's persisted sync action.
- **Ví dụ:** `/sdd-rfc --title=soft-delete-policy` creates `PROPOSED` RFC without changing `CONSTITUTION.md`.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Nêu RFC ID/status, Constitution/migration impact, evidence và review target. RFC `PROPOSED` là `Human decision required`; chỉ Tech Lead/Human Director được ủy quyền mới có thể chạy `/sdd-rfc --approve=<rfc-number>`. Thiếu authority, motivation/risk/migration hoặc conflicting rule là `BLOCKED`; không dùng `/sdd-review` để thay route approve RFC.
