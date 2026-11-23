---
name: project-development-playbook
description: Use when implementing IdeaGo tasks that need branch, stack, and verification guidance.
---
# Project Development Playbook

This legacy skill is a thin Trellis pointer.

Read these files before editing:

1. `.trellis/spec/README.md`
2. `.trellis/spec/shared/index.md`
3. `.trellis/spec/backend/index.md` for backend work
4. `.trellis/spec/frontend/index.md` for frontend work
5. `.trellis/spec/shared/verification.md` before completion

Key branch rule: `main` must stay anonymous and personal-deployment friendly.
Do not add hosted auth, Supabase, Stripe, LinuxDo, profile, quota, admin, or
billing requirements unless the task explicitly targets both branches.
