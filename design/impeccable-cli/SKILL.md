---
name: impeccable-cli
description: Run the official `impeccable` CLI against HTML, CSS, JSX, TSX, Vue, Svelte, directories, or live URLs to catch deterministic UI anti-patterns before they ship, or use `impeccable live` to open the Visual Mode overlay on a page. Use when Codex needs a frontend design audit, CI-friendly JSON findings, fast local scans, or live in-browser anti-pattern triage.
---

# Impeccable CLI

Use this skill when the job is to run Impeccable on frontend code or a live page and turn the findings into direct UI fixes.

It fits especially well when the user wants to:

- audit a local app, component directory, or built site for AI-slop tells and other frontend anti-patterns
- scan a live URL before review or before reproducing the issues locally
- open the Visual Mode overlay so the flagged elements are visible in place
- collect JSON findings for CI, scripts, or a pre-commit hook
- separate what the CLI can prove from broader design critique that still needs human judgment

## Quick Start

Use the bundled wrappers when you want the official CLI without remembering whether it is installed globally:

```bash
bash skills/impeccable-cli/scripts/impeccable_detect.sh src/
bash skills/impeccable-cli/scripts/impeccable_detect.sh --json src/
bash skills/impeccable-cli/scripts/impeccable_detect.sh --fast app/components
bash skills/impeccable-cli/scripts/impeccable_detect.sh https://example.com
bash skills/impeccable-cli/scripts/impeccable_live.sh
bash skills/impeccable-cli/scripts/impeccable_live.sh --port=5199
```

The wrappers prefer a global `impeccable` binary and fall back to `npx`.

## Workflow

### Start With The Real Target

- Scan the exact path, directory, or live URL the user cares about.
- Prefer the smallest target that still reproduces the design problem. Start narrow, then widen the scan only when the issue spans the whole app.
- Use `detect` when the user wants a deterministic report, JSON output, CI wiring, or local source-path triage.
- Use `live` when the user wants the overlay on a real page so the flagged elements are visible in place.

### Pick The Right Mode

- Use the default mode when accuracy matters and the target is small enough to inspect normally.
- Use `--fast` for a cheap first pass when the repo is large or when the user wants a quick smoke test, then rerun without `--fast` before declaring the result final.
- Use `--json` whenever the findings need to feed another tool, a CI step, or a machine-readable report.
- Use `live` when a user is actively inspecting a page and wants the Visual Mode overlay instead of raw findings first.

### Triage Findings Like An Engineer

- Group findings by what the UI needs next, not just by rule name.
- Prioritize issues that affect readability, hierarchy, contrast, or obvious AI-generated layout tells.
- When the scan points to files or selectors, anchor the explanation there and suggest the smallest credible fix.
- If the user is shipping a component library or design system, turn repeated findings into one shared design rule instead of one-off cleanup.
- When the overlay is open, use it to confirm the element that actually triggered the rule before editing code.

### Keep The Boundary Honest

- The deterministic CLI catches only the rules it can prove from code or runtime structure.
- Do not claim coverage for LLM-only critique patterns unless the user separately asks for a broader design review.
- Respect the exit codes: `0` means no findings, `2` means anti-patterns were detected.
- Treat the output as evidence, not as a substitute for design judgment.
- Do not invent a Codex-native `/critique` command unless the current harness actually provides one.

## Integration Guidance

- For one-off audits, run the wrapper and summarize the highest-signal fixes first.
- For CI, prefer `--json` and fail or warn based on the CLI exit code.
- For pre-commit hooks, keep the target narrow so the hook stays fast enough to trust.
- When the user wants policy, turn repeated findings into a short repo rule set rather than pasting raw scan output everywhere.
- For live page debugging, start `impeccable live`, note the local server URL it prints, and use that overlay server to inject `detect.js` into the target page.
- If the user wants browser automation around the overlay workflow, pair this skill with [$playwright](/Users/arnav/.codex/skills/playwright/SKILL.md).

## Guardrails

- Do not invent unsupported upstream commands.
- Do not flatten every design issue into "AI slop"; some findings are normal quality and accessibility problems.
- If the target is a URL, do not pretend a source-file fix exists until you find the code path that produces the rendered issue.
- If contrast or typography findings remain after a patch, say so plainly instead of hand-waving them away.
- If `live` is aimed at a page the user did not ask about, stop and confirm the target instead of spraying overlay scripts across unrelated sites.

## Example Prompts

- `Use $impeccable-cli to scan this frontend app and tell me which findings are actually worth fixing first.`
- `Use $impeccable-cli to run a JSON scan on this directory and shape the result into a CI-friendly summary.`
- `Use $impeccable-cli to check this live URL, explain the highest-signal anti-patterns, and map them back to the components I should edit.`
- `Use $impeccable-cli to launch Visual Mode for this page and tell me which highlighted elements I should fix first.`

## Resources

- `scripts/impeccable_detect.sh`: local wrapper that runs `impeccable detect` directly or via `npx`
- `scripts/impeccable_live.sh`: local wrapper that runs `impeccable live`
- `references/cli-quick-reference.md`: concise command reference and operating notes
- `prototype/`: SwiftUI starter for a compact menu-bar scan panel
