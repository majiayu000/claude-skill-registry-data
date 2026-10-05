---
name: drupal-planner.theme
description: "Plan Drupal themes — base theme, component strategy (SDC/traditional), CSS methodology, responsive design."
---

# Drupal Theme Planner

## Overview

drupal-planner.theme designs Drupal theme architectures before the first line of Twig or CSS is written. It produces specifications for base theme selection, component architecture (SDC vs traditional), CSS methodology, preprocess function strategy, template organization, asset library management, accessibility patterns, and responsive design — all grounded in Drupal theme layer conventions.

This is a focused sub-planner of `/drupal-planner` and the companion planner to `drupal-theme-critic`. The planner designs FOR everything the critic checks.

## Use_When

- User says "plan the theme", "design the frontend", "choose a base theme", "plan the component architecture"
- User needs to decide: SDC vs traditional templates vs Pattern Lab vs Storybook
- User is designing CSS architecture (BEM, SMACSS, utility-first, hybrid)
- User is planning preprocess function strategy or asset library organization
- User needs to plan responsive design, accessibility, or performance for the theme layer
- User has drupal-theme-critic REVISE findings to address

## Do_Not_Use_When

- User needs full feature planning — use `/drupal-planner`
- User wants to review an existing theme — use `drupal-theme-critic`
- User is focused on content model or entity architecture — use `/drupal-planner.content-model`
- User is writing CSS/Twig code — use their development workflow

## Companion_Skills

- `drupal-theme-critic`: Review the theme after implementation (this planner designs for what the critic checks)
- `drupal-planner`: Full Drupal implementation planning (routes here for theme phase)
- `a11y-planner`: Accessibility design (for deep-dive on ARIA patterns, focus management)
- `drupal-critic`: Review the full implementation after coding

## Steps

1. **Identify scope**: What theme architecture is being designed?
2. **Detect context**: Drupal version (10, 11, CMS), existing theme, base theme candidates, design system requirements
3. **Route to agent**: Delegate to the drupal-theme-planner agent
   - `Agent(subagent_type="drupal-planner", model="opus", prompt=<theme_planning_prompt>)`
4. **Return the plan**: Present theme architecture specification

## Tool_Usage

- Use Read to examine existing theme structure, .info.yml, .theme files, templates, CSS
- Use Grep to find preprocess functions, template files, CSS methodology patterns, library definitions
- Use Bash to check Drupal version, base theme, StarterKit usage
- Write the plan to `docs/plans/`
