---
name: ui-redesign
description: Set up and manage a UI redesign experiment with three git worktree branches for modern minimal, bold creative, and classic refined design directions. Use when asked to run a UI redesign experiment, compare design approaches, or prototype multiple visual directions in parallel branches.
---

## Initial Setup

1. First, create 3 git worktree branches from the current main branch:
   - `ui-redesign-modern-minimal`
   - `ui-redesign-bold-creative`
   - `ui-redesign-classic-refined`

2. Set up the worktree structure:
   ```bash
   git worktree add ../project-modern-minimal ui-redesign-modern-minimal
   git worktree add ../project-bold-creative ui-redesign-bold-creative
   git worktree add ../project-classic-refined ui-redesign-classic-refined

Design Directions for Each Branch
Branch 1: Modern Minimal (ui-redesign-modern-minimal)
Work in ../project-modern-minimal

Design Philosophy: Clean, minimalist, lots of whitespace
Color Palette: Monochromatic with one accent color
Typography: Sans-serif, limited font weights
Components: Flat design, subtle shadows, micro-interactions
Focus: Maximum usability and clarity

Branch 2: Bold Creative (ui-redesign-bold-creative)
Work in ../project-bold-creative

Design Philosophy: Vibrant, experimental, attention-grabbing
Color Palette: Bold gradients, contrasting colors
Typography: Mix of fonts, creative text treatments
Components: 3D elements, animations, glassmorphism
Focus: Memorable user experience and visual impact

Branch 3: Classic Refined (ui-redesign-classic-refined)
Work in ../project-classic-refined

Design Philosophy: Timeless, professional, trustworthy
Color Palette: Traditional color schemes, navy/gold/cream
Typography: Serif fonts for headers, clean sans for body
Components: Card-based layouts, subtle borders, traditional patterns
Focus: Professional appearance and accessibility

Implementation Tasks for Each Branch
For each design direction, implement these changes:

Update the main color scheme and CSS variables
Redesign the homepage/landing page
Update the navigation menu style
Redesign at least 2 key components (buttons, cards, forms, etc.)
Create a style guide document showing the design system
Update any relevant documentation

Working Process

Start with branch 1, make all changes, commit with clear messages
Move to branch 2, repeat the process
Move to branch 3, complete the redesign
After all three are complete, create a comparison document

Final Deliverable
Create a COMPARISON.md file in the main branch that includes:

Screenshots of each design approach
Pros and cons of each approach
Performance metrics if applicable
Recommendation for which design to move forward with

Please proceed with this setup and implementation. Start by creating the worktree branches and confirming they're set up correctly, then begin with the Modern Minimal design.
