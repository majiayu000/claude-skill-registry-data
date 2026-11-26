---
name: gsap-new
description: Orchestrate new GSAP work for new pages, new sections, or greenfield animation systems. Use when the user wants to add animations where there is no established motion implementation yet. Create or update .gsap artifacts, interview only when required, generate the animation specification and implementation plan, then apply implementation.
---

# GSAP New

Use this workflow for new pages, new sections, and greenfield animation work.

## Sequence

1. Read existing `.gsap` artifacts if present.
2. Inspect the real page/component files.
3. Run internal discovery/bootstrap helpers if artifacts are missing.
4. Let the script detect framework, packages, routes, likely sections, and visual signals first.
5. Interview only for missing decisions.
6. Update `.gsap/animation-spec.md` and `.gsap/pages/<page>.animation.md`.
7. Generate or refresh `.gsap/animation-plan.md`, `.gsap/tasks/<page>.tasks.md`, and `.gsap/phases/<page>/*.md`.
8. Split the work into phases so each phase owns one major section only.
9. Implement only the active phase unless the user explicitly asks for more.
10. Update statuses in the page, plan, tasks, and phase artifacts.

## Internal Helper

Use:

```bash
python scripts/gsap_workflow.py gsap-new --path "<project>" --page "<page>"
```

This command should scaffold artifacts, inspect the project structure, detect framework/packages, generate discovery questions, and prepare workflow state. It is the only public helper command for this mode.

## Interview Policy

Ask only for missing data:

- motion personality
- density
- scroll behavior
- section-level recipe choice
- mobile downgrade rules
- reduced-motion fallback

If the artifacts already contain these answers, continue without re-interviewing.

## Implementation Output

Before finishing, ensure:

- `.gsap/pages/<page>.animation.md` reflects actual status
- `.gsap/animation-plan.md` reflects the latest section order and recipes
- `.gsap/tasks/<page>.tasks.md` reflects the phase queue
- `.gsap/phases/<page>/` contains one file per major section phase
- implementation follows current code, not generic examples
