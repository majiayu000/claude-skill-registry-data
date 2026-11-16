---
name: tdd-evidence
description: >
  Use when you need to prove test results with a signed receipt from yana-rt
  evidence run — not just text. Required for all Rust guard/evidence modules
  in Yana AI, and any claim "tests passed" that must be verifiable.
  Triggers on: yana-rt evidence run, signed receipt, viết test trước,
  evidence run, proof of test.
triggers:
  - yana-rt evidence run
  - yana-rt evidence
  - signed receipt
  - viết test trước
  - evidence run
  - proof of test
  - YANA-EVIDENCE
  - receipt đính kèm
source: >
  Adapted from design.md/.agents/skills/tdd (MIT, google/design.md).
  Extended for Rust runtime, multi-language, and Yana AI evidence provenance.
---

# Red-Green-Refactor (TDD) Skill

Mọi feature mới, bug fix, hay module guard đều đi qua đúng 3 phase này —
không bỏ qua, không đảo thứ tự.

---

## The Three-Phase Cycle

### Phase 1: RED — Establish Failure

Chứng minh feature chưa tồn tại và test của bạn là hợp lệ.

1. **Viết đúng 1 test** cho một behavior nhỏ nhất có thể.
2. **Chạy và xác nhận FAIL** — lỗi phải do logic chưa có, không phải do
   config sai hay syntax error.
3. **Ghi lại expected failure message** — nếu test fail vì lý do sai,
   fix test trước, không phải code.

**Rust:**
```rust
#[test]
fn verify_receipt_rejects_wrong_key() {
    // RED: hàm verify_receipt chưa tồn tại
    assert_eq!(
        verify_receipt("wrong-key", "ok\n", "YANA-EVIDENCE v1 0 aabb ccdd"),
        Err("signature invalid — not produced by this runtime")
    );
}
```
```
error[E0425]: cannot find function `verify_receipt` in this scope
```

**TypeScript:**
```typescript
import { describe, it, expect } from 'vitest';
import { blastRadius } from './blast_radius';

describe('blastRadius', () => {
  it('blocks find -delete', () => {
    expect(blastRadius('find . -delete')).toBe('blocked');
    // Fails: Cannot find module './blast_radius'
  });
});
```

**Python:**
```python
def test_protected_hit_blocks_absolute_path():
    # RED: hàm chưa tồn tại
    assert protected_hit('/workspaces/Yana-AI/core/rules/x.md') == True
```

---

### Phase 2: GREEN — Minimal Pass

Làm test pass bằng code **đơn giản nhất có thể**. Không build for the future.

1. **Minimal implementation** — chỉ đủ để test pass, không thêm gì khác.
2. **Chạy toàn bộ test suite** — tất cả phải green, không chỉ test mới.
3. **Evidence bắt buộc** — capture output bằng `yana-rt evidence run`:

```bash
# Rust
yana-rt evidence run cargo test verify_receipt_rejects_wrong_key

# TypeScript
yana-rt evidence run npx vitest run --reporter=verbose

# Python
yana-rt evidence run pytest tests/ -v
```

Output sẽ kèm receipt `YANA-EVIDENCE v1 ...` — đây là proof of work thật,
không phải text bịa. Paste receipt này khi báo cáo "tests passed".

---

### Phase 3: REFACTOR — Clean Up

Cải thiện code trong khi giữ nguyên green state.

1. **Clean up**: naming, bỏ duplication, type safety.
2. **Chạy test sau MỖI thay đổi** — nếu đỏ, revert ngay.
3. **Không thêm feature mới** trong phase này.

```rust
// Sau refactor: rõ ràng hơn, vẫn pass
pub fn verify_receipt(key: &str, body: &str, receipt: &str) -> Result<i32, &'static str> {
    let parts: Vec<&str> = receipt.split_whitespace().collect();
    if parts.len() != 5 { return Err("malformed receipt"); }
    // ... proper implementation
}
```

---

## Core Rules

### 1. Không "horizontal splurging"
Viết nhiều test cùng lúc là sai. Loop bắt buộc:
```
Write 1 Test → See RED → Write minimal fix → See GREEN → Refactor → Repeat
```

### 2. Không sửa test để pass
Nếu test phải đổi, đó là vì **requirement đổi** — không phải vì code khó viết.
Sửa test để pass implementation = phá vỡ toàn bộ giá trị của TDD.

### 3. Evidence trước khi claim "done"
Không được nói "tests passed" nếu không có signed receipt từ
`yana-rt evidence run`. Text không có receipt = claim không có proof.

### 4. Với Rust — test trong module, không file riêng
```rust
// Trong cùng file với implementation
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_name() { ... }
}
```

### 5. File size rule vẫn áp dụng
Ngay cả khi viết test, mỗi file ≤ 300 dòng. Nếu test file phình to,
tách theo nhóm behavior, không nhét hết vào một file.

---

## Quick Reference

| Phase | Rust | TypeScript | Python |
|-------|------|------------|--------|
| Run 1 test | `cargo test test_name` | `npx vitest run -t "test name"` | `pytest tests/test_x.py::test_name` |
| Run all | `cargo test` | `npx vitest run` | `pytest` |
| With evidence | `yana-rt evidence run cargo test` | `yana-rt evidence run npx vitest run` | `yana-rt evidence run pytest` |
| Watch mode | `cargo watch -x test` | `npx vitest` | `pytest-watch` |

---

## Checklist trước khi đóng task

- [ ] Mỗi behavior mới có ít nhất 1 test
- [ ] Tất cả test green (evidence receipt đính kèm)
- [ ] Không test nào bị sửa để pass code mới
- [ ] File ≤ 300 dòng
- [ ] Không còn `todo!()` hay `unimplemented!()` trong production path
