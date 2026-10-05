---
name: review
description: Clade coverage-driven project review — walks every VERIFY.md checkpoint, fixes failures in-session, converges when all pass. NOT the Claude Code built-in /review (single PR diff) — route PR reviews to /review-pr or the CC built-in.
when_to_use: "review everything, test all, full review, VERIFY.md, 全面测试, coverage review — NOT for post-iteration anchor checks in autonomous loops (use /verify), NOT for PR review (use /review-pr or the CC built-in /review)"
user_invocable: true
---

# Review Skill

Performs a systematic, coverage-driven review of the project by working through every checkpoint in `VERIFY.md`. Unlike a free-form code review, this skill tests specific scenarios end-to-end, fixes failures immediately, and only declares convergence when all checkpoints are ✅ or ⚠.

**Convergence condition**: all checkpoints in VERIFY.md are ✅ (pass) or ⚠ (known limitation). No ⬜ (untested) or ❌ (fail) remaining.
