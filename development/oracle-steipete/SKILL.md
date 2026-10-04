---
description: Use when you want a second-model review through the `@steipete/oracle` CLI by bundling a prompt with a tightly scoped set of repo files. Use for debugging, refactor review, design critique, prompt validation, or cross-checking a tricky conclusion. Supports GPT-5.5 Pro/GPT-5.5 browser runs with standard or extended thinking.
metadata:
    hermes:
        command_priority: 420
    targets:
        - antigravity
name: oracle_steipete
---
# Oracle CLI

Oracle bundles your prompt plus selected files into one external-model request. Treat the answer as a strong second opinion, not ground truth: verify it against the repo and tests before acting.

Current reference checked: `@steipete/oracle` npm `0.9.0` and upstream `steipete/oracle` main docs as of 2026-05-03. The npm help may lag the README for brand-new browser flags; upstream documents GPT-5.5 Pro/GPT-5.5 and `--browser-thinking-time`.

## Default recommendation

Use browser mode with GPT-5.5 Pro and extended thinking when Kosta asks for Oracle and the question is hard enough to justify the wait:

```bash
npx -y @steipete/oracle \
  --engine browser \
  --model gpt-5.5-pro \
  --browser-thinking-time extended \
  -p "<task>" \
  --file "src/**"
```

Use standard thinking for faster/cheaper-ish browser passes where you mostly want a sanity check:

```bash
npx -y @steipete/oracle \
  --engine browser \
  --model gpt-5.5-pro \
  --browser-thinking-time standard \
  -p "<task>" \
  --file "src/**"
```

If Kosta explicitly wants non-Pro GPT-5.5, use `--model gpt-5.5` with the same `--browser-thinking-time standard|extended` choice.

## Pick standard vs extended

- **standard**: quick second pass, small bug, prompt review, API-shape check, or when the attached file set is already very narrow.
- **extended**: architecture, merge conflict review, subtle debugging, multi-file refactor, release-readiness, security/reliability review, or anything where a shallow answer would waste more time than the slower run.

Default to **extended** for ambiguous “ask Oracle” requests. Say which mode you picked in the prompt slug or short preface.

## Golden path

1. Pick the smallest file set that still contains the truth. Include entrypoints, failing tests, configs, and nearby docs; exclude secrets and generated output.
2. Preview first:

```bash
npx -y @steipete/oracle --dry-run summary --files-report \
  -p "<task>" \
  --file "src/**" --file "!**/*.snap"
```

3. Run browser GPT-5.5 Pro with `standard` or `extended` thinking.
4. If the run detaches or times out, reattach. Do **not** immediately re-run the same prompt.

## Useful commands

Show help:

```bash
npx -y @steipete/oracle --help
npx -y @steipete/oracle --help --verbose
npx -y @steipete/oracle --debug-help
```

Preview full bundle without sending:

```bash
npx -y @steipete/oracle --dry-run full \
  -p "<task>" \
  --file "src/**"
```

Manual paste fallback:

```bash
npx -y @steipete/oracle --render --copy \
  -p "<task>" \
  --file "src/**"
```

Session recovery:

```bash
npx -y @steipete/oracle status --hours 72 --limit 50
npx -y @steipete/oracle session <session-id> --render
```

## Attaching files

`--file` accepts files, directories, and globs. Pass it multiple times; comma-separated paths also work.

Examples:

```bash
--file "src/**"
--file src/index.ts
--file docs --file README.md
--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"
```

Important behavior:

- Default ignored dirs include `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, and `tmp` unless explicitly passed.
- Glob expansion honors `.gitignore`.
- Symlinks are not followed by default.
- Dotfiles are filtered unless the pattern includes a dot-segment, e.g. `--file ".github/**"`.
- Files over the default 1 MB cap are rejected unless `ORACLE_MAX_FILE_SIZE_BYTES` or `~/.oracle/config.json` raises `maxFileSizeBytes`.

## Prompt template

Oracle starts with no project memory. A good prompt includes:

- Project briefing: stack, target OS/toolchain, services, build/test commands.
- File map: which attached paths matter and what role each file plays.
- Exact question, prior attempts, and verbatim errors.
- Constraints: APIs not to change, compatibility, performance, style, rollout risk.
- Desired output: patch plan, risk list, test plan, alternatives, or final recommendation.

For long investigations, write a self-contained prompt that can be restored later: 6–30 sentences of context, concrete repro steps, exact errors, and all required files.

## Engine rules

- Browser mode is the normal path for GPT-5.5 Pro without API keys.
- API mode incurs usage cost; get explicit user consent before starting API runs unless Kosta explicitly requested an API run.
- Auto engine selection uses API when `OPENAI_API_KEY` is set, otherwise browser, so pass `--engine browser` when you mean ChatGPT browser automation.
- Browser model selection can be controlled with `--browser-model-strategy select|current|ignore`. Use `current` when the browser is already on the exact desired ChatGPT model.
- `~/.oracle/config.json` can set defaults such as `model: "gpt-5.5-pro"` and `browser.thinkingTime: "extended"`, but CLI flags win.

## Safety

Do not attach secrets by default: `.env`, private keys, tokens, cookie databases, credential exports, and auth logs. Redact aggressively. Prefer fewer files plus a clearer prompt over whole-repo dumps.
