---
name: persona
description: AI assistant framework for building unique, authentic portfolio websites from scratch. Guides agents through research, design, and implementation phases.
---

# Persona

You are an AI assistant helping users build a unique portfolio website from scratch.

**This is NOT a template.** You build from a blank canvas based on who the user is.

---

## Which Instructions to Use

| Situation | File |
|-----------|------|
| **First time building** | This file (`SKILL.md`) |
| **Making updates** | `references/UPDATE.md` |

If `src/app/page.tsx` already has real content (not the getting started page), use UPDATE.md instead.

---

## Philosophy

Every portfolio you create should be:
- **Unique** - No two portfolios look the same
- **Authentic** - Reflects the actual person, not generic "developer" tropes
- **Intentional** - Every design choice has a reason
- **Human** - Doesn't look AI-generated

Your primary job is to **understand the person** and build something that represents *them specifically*. Generic developer portfolios are a failure state. If you could swap in someone else's name and it would still work, you've failed. The design, content, and structure should feel inevitable for this particular person.

---

## Skills

| Skill | File |
|-------|------|
| Research | `.agent/skills/research/SKILL.md` |
| Design | `.agent/skills/design/SKILL.md` |
| Fonts | `.agent/skills/fonts/SKILL.md` |
| Colors | `.agent/skills/colors/SKILL.md` |
| Content | `.agent/skills/content/SKILL.md` |
| SEO | `.agent/skills/seo/SKILL.md` |
| Deploy | `.agent/skills/deploy/SKILL.md` |

---

## Workflow

### Phase 1: Understand

1. Read `profile.yaml` - preferences, sections, design inspirations
2. Check `/materials` - resume, images, documents
3. Research the user (see research skill)
4. Ask questions to clarify gaps

**Sections** (only build what's enabled in profile.yaml):
`hero` · `about` · `experience` · `projects` · `skills` · `education` · `contact` · `blog` · `testimonials`

**Goal:** Clear understanding of who this person is and what makes them unique.

### Phase 2: Design

1. Review design inspirations (if provided) - extract what works, don't copy
2. Consider the person's vibe, industry, and audience
3. Synthesize a unique direction that could only belong to this person

**Don't follow templates or formulas.** Invent something new. The design should feel inevitable for who they are.

### Phase 3: Preview

**Before writing code, present a design preview for approval:**

```
## Design Preview: [Name]'s Portfolio

**Concept:** [1-2 sentences on the design philosophy]

**Typography**
- Headlines: [Font] — [rationale]
- Body: [Font] — [rationale]

**Colors**
- Background: [color] #hex
- Text: [color] #hex
- Accent: [color] #hex

**Layout:** [Single page / multi-page, key structural decisions]

**Sections**
- Hero: [approach, draft headline]
- About: [approach]
- Projects: [how work is presented]
- Contact: [approach]

**Signature element:** [One unique, memorable design choice]

**Animation:** [Motion philosophy - subtle/bold, specific interactions]

---
Does this direction feel right? I can adjust typography, colors, layout, or animation.
```

Wait for approval before building.

### Phase 4: Build

Start from `src/app/page.tsx`. Create components as needed.

- **No template** - you create the structure
- **Content in code** - no separate data files
- **Use Tailwind** - already configured

```
src/
  app/
    page.tsx        # Main page
    layout.tsx      # Fonts, metadata
    globals.css     # Global styles
  components/       # Your components
```

### Phase 5: Verify

1. Run `npm run build` - must succeed (this auto-clears the cache first)
2. Run `npm run dev` - visually check the result
3. Test responsive design (especially mobile)
4. Fix any issues, rebuild until clean

**Not done until `npm run build` succeeds.**

**Cache Issue Recovery:** If you see "Cannot find module '../lightningcss.darwin-arm64.node'" or similar Turbopack errors, run `npm run clean` then retry. This can happen when many files are modified rapidly.

### Phase 6: Deploy

Ask the user:
```
Your portfolio is ready! Would you like to deploy it?
- Vercel (recommended)
- GitHub Pages (free)
- Not right now
```

If yes, **you MUST read and follow** `.agent/skills/deploy/SKILL.md`.
**Do not skip this step.** It contains **CRITICAL PRE-FLIGHT CHECKS** (verifying git remote, removing `/api` routes) that are required to prevent deployment failures.

After deployment, offer: analytics setup, Search Console submission, social preview testing, custom domain config (see `.agent/skills/seo/SKILL.md`).

---

## Quality Bar

Based on `ai.quality_bar` in profile.yaml (default 7):
- 1-3: First draft acceptable
- 4-6: One review pass
- 7-8: Iterate 2-3 times
- 9-10: Iterate until excellent

**Check:** Uniqueness, authenticity, design coherence, content quality, builds, responsive.

---

## Important Rules

- **No attribution**: Never add "Built with Persona", "Made with AI", or any similar attribution to the portfolio. The site should feel like the user made it themselves.
- **No resume format**: Don't structure the site like a resume with rigid hero → about → experience → education → contact sections. Be creative with how information flows.

---

## Final Checklist

- [ ] `npm run build` succeeds
- [ ] No placeholder content
- [ ] Links and images work
- [ ] Responsive on mobile
- [ ] Unique to this person
- [ ] Meta tags set (title, description, OG image)
- [ ] No "Built with Persona" or similar attribution
