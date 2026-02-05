---
name: focus-ai-brand
description: Apply Focus.AI brand guidelines to documents, presentations, websites, and other materials. Supports two sub-brands - Focus.AI Client (services, proposals, client work) and Focus.AI Labs (research, experiments, public content). Use when creating branded materials, applying visual identity, or generating content that needs to follow Focus.AI style. Trigger on "focus.ai style", "focus brand", "labs style", or requests for branded Focus.AI materials.
---

# Focus.AI Brand System

This skill applies Focus.AI brand guidelines to create consistent, on-brand materials across two sub-brands.

## Required Reading

**IMPORTANT**: Before creating any branded material, you MUST read the appropriate design system files:

### For ALL Brand Work
First, read the shared foundations:
```
Read: focus-ai-brand/THEFOCUS_DESIGN_SYSTEM.md
```

### Then, Based on Context

**For Client Materials** (proposals, case studies, client work, service pages):
```
Read: focus-ai-brand/THEFOCUS_CLIENT_DESIGN_SYSTEM.md
```

**For Labs Materials** (research, experiments, blog posts, open source):
```
Read: focus-ai-brand/THEFOCUS_LABS_DESIGN_SYSTEM.md
```

## Brand Selection Guide

| Context | Brand | Design System File |
|---------|-------|-------------------|
| Client proposals | Client | THEFOCUS_CLIENT_DESIGN_SYSTEM.md |
| Case studies | Client | THEFOCUS_CLIENT_DESIGN_SYSTEM.md |
| Service pages | Client | THEFOCUS_CLIENT_DESIGN_SYSTEM.md |
| Product marketing | Client | THEFOCUS_CLIENT_DESIGN_SYSTEM.md |
| Conference analysis | Labs | THEFOCUS_LABS_DESIGN_SYSTEM.md |
| Research reports | Labs | THEFOCUS_LABS_DESIGN_SYSTEM.md |
| Experiments | Labs | THEFOCUS_LABS_DESIGN_SYSTEM.md |
| Technical blog posts | Labs | THEFOCUS_LABS_DESIGN_SYSTEM.md |
| Open source projects | Labs | THEFOCUS_LABS_DESIGN_SYSTEM.md |

**Rule of thumb**: Client work or selling services → Client brand. Sharing learnings or exploring → Labs brand.

## Quick Difference Summary

| Aspect | Client | Labs |
|--------|--------|------|
| **Aesthetic** | Magazine / editorial | Bell Labs / RAND Corporation |
| **Primary accent** | Petrol `#0e3b46` | Rand-Blue `#0055aa` |
| **Secondary accent** | Vermilion `#c3471d` | Alert-Red `#d93025` |
| **Voice** | Confident, professional, clear | Curious, wry, generous |

## Workflow

1. **Determine brand**: Client work → Client brand. Research/sharing → Labs brand.
2. **Read foundations**: Load `THEFOCUS_DESIGN_SYSTEM.md`
3. **Read brand specifics**: Load the appropriate brand file (Client or Labs)
4. **Apply guidelines**: Follow typography, colors, layout, and voice from the loaded files
5. **Verify**: Check against the quality checklist in the design system files

## Assets

- `assets/fonts/` — Font files (use Inter + Courier Prime for new work)
- `assets/examples/` — HTML implementation examples
