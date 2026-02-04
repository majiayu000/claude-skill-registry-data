---
name: figma-to-react
version: 0.9.27
description: Convert Figma designs to pixel-perfect React components with Tailwind CSS.
license: MIT
compatibility: Requires Figma MCP server (mcp__figma__*). React + Tailwind CSS project. Uses oxlint for fast linting.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch TodoWrite AskUserQuestion mcp__plugin_figma_figma__get_metadata mcp__plugin_figma_figma__get_screenshot mcp__plugin_figma_figma__get_design_context mcp__plugin_figma_figma-desktop__get_metadata mcp__plugin_figma_figma-desktop__get_screenshot mcp__plugin_figma_figma-desktop__get_design_context mcp__figma__get_metadata mcp__figma__get_screenshot mcp__figma__get_design_context
---

# Figma to React

Convert Figma designs to pixel-perfect React components with Tailwind CSS.

## Workflow

The workflow is a **status-driven loop**. Always check status before and after each step:

```
LOOP:
  1. Run: $SKILL_DIR/scripts/status.sh
  2. Read the step file for current_step (e.g., step-4b-validate-dimensions.md)
  3. Execute that step's instructions
  4. Go to step 1 (until step 8 complete)
```

### Step Reference

Create a TodoWrite list with these steps (Glob to find each file):

```
1. Setup - step-1-setup.md
2. Detect structure - step-2-detect-structure.md
3. Confirm config - step-3-confirm-config.md
3b. Create preview route - step-3b-preview-route.md
4. Generate screens (parallel) - step-4-generation.md
4b. Validate dimensions - step-4b-validate-dimensions.md
5. Import tokens - step-5-import-tokens.md
6. Validate screens (parallel) - step-6-validation.md
7. Rename assets - step-7-rename-assets.md
8. Disarm hook - step-8-disarm-hook.md
```

### Pre-flight Checks

Each step file has a pre-flight check. If status.sh says you're on step 4b but you're trying to execute step 5:
1. **STOP** - don't execute step 5
2. Update TodoWrite to uncheck wrongly-completed steps
3. Read the correct step file (step 4b)

This prevents skipping steps, which was a common failure mode.

## Recovery After Compaction

If context is compacted, run `$SKILL_DIR/scripts/status.sh` to see exactly where you are.
The script infers state from /tmp files - no context needed.

**State files used by status.sh:**
- `/tmp/figma-to-react/capture-active` - Skill is active
- `/tmp/figma-to-react/config.json` - Config with screens/screenNames mapping
- `/tmp/figma-to-react/steps/4b/*.json` - Dimension validation results
- `/tmp/figma-to-react/steps/4b/user-decisions.json` - User decisions on missing dims
- `/tmp/figma-to-react/steps/5/complete.json` - Token import done
- `/tmp/figma-to-react/validation/*/result.json` - Visual validation results
- `/tmp/figma-to-react/steps/7/complete.json` - Asset rename done
