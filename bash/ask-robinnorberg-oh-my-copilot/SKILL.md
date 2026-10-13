---
name: ask
description: Process-first advisor routing for Claude, Codex, Gemini, Antigravity, Grok, or Cursor via `omc ask`, with artifact capture and no raw CLI assembly
---

# Ask

Use OMC's canonical advisor skill to route a prompt through the local Claude, Codex, Gemini, Antigravity, Grok, or Cursor CLI and persist the result as an ask artifact.

## Usage

```bash
/oh-my-copilot:ask <claude|codex|gemini|antigravity|grok|cursor> <question or task>
```

Examples:

```bash
/oh-my-copilot:ask codex "review this patch from a security perspective"
/oh-my-copilot:ask gemini "suggest UX improvements for this flow"
/oh-my-copilot:ask antigravity "suggest UX improvements for this flow"
/oh-my-copilot:ask claude "draft an implementation plan for issue #123"
/oh-my-copilot:ask cursor "apply this implementation plan"
```

## Routing

**Required execution path — always use this command:**

```bash
omc ask {{ARGUMENTS}}
```

**Do NOT manually construct raw provider CLI commands.** Never run `codex`, `claude`, `gemini`, `agy`, `grok`, or `cursor-agent` directly to fulfill this skill. The `omc ask` wrapper handles correct flag selection, artifact persistence, and provider-version compatibility automatically. Manually assembling provider CLI flags will produce incorrect or outdated invocations.

## Requirements

- The selected local CLI must be installed and authenticated.
- Verify availability with the matching command:

```bash
claude --version
codex --version
gemini --version
agy --version
grok --version
cursor-agent --version
```

- **Antigravity CLI install** (Google's successor to the Gemini CLI): install the `agy`
  binary per the [official Antigravity instructions](https://antigravity.google) (inspect
  any installer before running it). Verify: `agy --version`
  > **Platform note:** `omc ask antigravity` runs on macOS, Linux and Windows. On Windows the advisor spawns `agy` without a shell so the prompt reaches it as a single argv value (`agy` cannot read the prompt from stdin); a run that hangs or exits with no output is reported as a failure (google-antigravity/antigravity-cli#76).
- **Gemini CLI** remains supported for enterprise/API-key use cases.

## Artifacts

`omc ask` writes artifacts to:

```text
.omg/artifacts/ask/<provider>-<slug>-<timestamp>.md
```

Task: {{ARGUMENTS}}
