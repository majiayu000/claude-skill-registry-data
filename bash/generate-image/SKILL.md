---
name: generate-image
description: Generate images with OpenAI GPT Image 2 via the Codex CLI, billed through the user's ChatGPT Plus subscription (no OpenAI API key, no per-image API cost). Use when the user asks to create, generate, or make an image, picture, illustration, icon, hero graphic, or concept art from a text prompt.
---

# Generate Image

Creates images via OpenAI GPT Image 2. Auth runs through the Codex CLI logged in
with a ChatGPT account, so generation is covered by the user's Plus subscription.
There is no OpenAI API key and no separate per-image API billing.

## Before you start

This Skill does not talk to OpenAI directly. It shells out to the **Codex CLI**,
and that CLI has to already be installed on this machine and already signed in
to a ChatGPT account with an active Plus subscription. Check with `codex --version`
and run `codex login` if it is not signed in. There is no API key to paste, and
no separate per-image charge; the images are billed to that subscription.

Without a signed-in Codex CLI nothing here works, and the script fails at the
first call rather than producing a file.

## Quick start

```bash
# from this Skill's own directory, wherever your agent installed it
./scripts/generate-image.sh "a shiba inu wearing sunglasses, studio photo"
```

Saves to the resolved output folder (see below) as a slugified PNG, e.g.
`assets/images/a-shiba-inu-wearing-sunglasses-studio-photo.png`.

## Workflow

1. Turn the user's request into a strong English prompt. **Follow the build
   order and levers in [PROMPTING.md](PROMPTING.md)** (scene → subject → details
   → invariants → use). Refine vague requests before calling; do not pass a bare
   one-liner when the asset matters.
2. Run the script with the prompt. Optionally pass `--out` and `--name`.
3. Report the saved path back to the user. For changes, iterate in small
   single-variable steps and restate the invariants (see PROMPTING.md).

## Output location

When `--out` is not given, the script resolves the folder automatically:

| Condition | Target folder |
|-----------|---------------|
| `./public/` exists (web/app initiative) | `./public/images/` |
| otherwise | `./assets/images/` (created if missing) |

This establishes a consistent `assets/images/` convention across projects while
respecting web projects, where images must live under `public/` to be served.

## Options

| Flag | Effect |
|------|--------|
| `--out <dir>` | Write into this directory instead of the resolved default |
| `--out <file>.png` | Write to this exact file path |
| `--name <basename>` | Use this basename instead of slugifying the prompt |

Existing files are never overwritten: the script appends `-2`, `-3`, ... instead.

## Deliverable naming

These outputs are work assets, so they get short functional names by default.
If an image is a stakeholder **deliverable**, pass an explicit
`--name` following the file-naming rule, e.g.
`--name "20260612_Hero Banner_v1"`.

## Requirements

- `codex` CLI installed (`brew install --cask codex`)
- Logged in with a ChatGPT account: `codex login` (Plus or higher; image
  generation is not available on Free)

The script checks both and fails with a clear message if either is missing.
