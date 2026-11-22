---
name: ponytail
description: "YAGNI-first code-minimalism ladder — before writing code, check in order: does this need to exist? already in the codebase? stdlib? native platform feature? installed dependency? one line? Cuts unnecessary code/tokens while never trading away validation, error handling, security, or accessibility. Triggers on: 'ponytail mode', 'write minimal code', 'don't over-engineer this', 'yagni', 'is there already something for this', 'use native instead of a library', 'keep this simple', 'fewest lines possible', 'lazy senior dev mode'."
origin: DietrichGebert/ponytail (MIT)
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.41.0"
allowed-tools: Read, Grep, Glob
---

# Ponytail — The YAGNI Ladder
# Source: DietrichGebert/ponytail (MIT)
# Tier: TIER 3 — PRODUCTIVITY

Before writing code, walk this ladder — stop at the first rung that holds:

```
1. Does this need to exist?    → no: skip it (YAGNI)
2. Already in this codebase?   → reuse it, don't rewrite
3. Stdlib does it?             → use it
4. Native platform feature?    → use it
5. Installed dependency?       → use it
6. One line?                   → one line
7. Only then: the minimum that actually works
```

The ladder runs **after** understanding the problem, not instead of it — read the code
the change touches, trace the real flow, then pick a rung. Lazy about the solution,
never about reading the problem first.

**Lazy, not negligent**: trust-boundary validation, data-loss handling, security, and
accessibility are never on the chopping block. A date-picker request becomes
`<input type="date">` (the browser already has one) — a permission check does NOT
become "skip it, probably fine."

**Do NOT use for:** overriding `golden-principles.md` #3 (TDD — tests still come
first, this ladder governs implementation size, not whether tests exist), or as
license to skip the validation/error-handling requirements in `code-quality-gate-
law.md` — those are exactly the things this skill explicitly refuses to cut.

---

## Relationship to `caveman` (already in this repo)

Different axis, easy to conflate — check both when the trigger phrase is ambiguous:

```
caveman   → compresses PROSE (agent's own chat responses), ~75% token cut via
            terse fragments, no articles/filler. Governs how the agent TALKS.
ponytail  → compresses CODE (what the agent writes to files), governs what the
            agent BUILDS. Independently measured: -54% LOC, -22% tokens, -20%
            cost, -27% time vs. no-skill baseline on real agentic coding
            sessions (12 tasks, FastAPI+React repo, Haiku 4.5, n=4) — and the
            only one of the two that stays at 100% safety score under
            adversarial testing (a bare "write fewer tokens" prompt without
            this ladder's guardrails drops to 95%).
```

They compose — using both together is not a conflict, "caveman mode" style replies
about "ponytail mode" minimal code are independent settings.

Note: `JuliusBrussee/caveman` (a *different* origin repo, also named "caveman", also
benchmarked in ponytail's own README) was evaluated for this ingestion queue and
skipped as a functional duplicate of this repo's existing `caveman` skill (sourced
from `mattpocock/skills` instead) — same trigger phrases, same terse-prose mechanism.

---

## Example — before/after

```
Request: "add a date picker"

❌ Without the ladder: installs flatpickr, writes a wrapper component,
   adds a stylesheet, starts a discussion about timezone handling.

✅ With the ladder (rung 4 — native platform feature):
   <input type="date">
```

```
Request: "parse this CSV string"

Ladder walk:
  1. Needs to exist? Yes (real requirement).
  2. Already in this codebase? Check first — grep for an existing CSV parser.
  3. Stdlib? Python's csv module / Node has none built-in → skip.
  4. Native platform? N/A for this case.
  5. Installed dependency? Check package.json/requirements — if csv-parse or
     pandas is already a dependency, use it. Don't add a new one.
  6. One line? Only if the format is trivial (no quoting/escaping) — real CSV
     needs a real parser, this is where "one line" fails safety and the
     ladder correctly stops before it.
  7. Minimum that works: use the existing or stdlib parser, nothing hand-rolled.
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu skip validation/error-handling/security/accessibility với lý do "ponytail mode"
   — đây chính là ranh giới skill này tuyên bố KHÔNG BAO GIỜ cắt
❌ FAIL nếu chọn rung 6 (one-liner) cho input cần escaping/quoting/edge-case thật sự
   (vd CSV parsing thật) — one-liner đúng nghĩa "lazy" chỉ khi input đơn giản thật
❌ FAIL nếu bỏ qua bước đọc code trước khi áp ladder — ladder chạy SAU khi hiểu vấn đề
❌ FAIL nếu conflate với `caveman` skill (khác trục: prose vs code, xem bảng trên)
✅ PASS khi: mỗi rung được cân nhắc theo thứ tự, dừng ở rung đầu tiên hợp lệ, và
   an toàn/validation không bị đánh đổi lấy ít dòng code hơn
```

## See also

- `caveman` — compresses agent prose, not code; different axis, see comparison table above
- `code-quality-gate-law.md` — the validation/error-handling/type-safety floor this skill never cuts below
- `golden-principles.md` #5 (small files/functions) and #12 (surgical changes) — this ladder is a specific, benchmarked technique toward the same goal those principles state generally
