---
name: read-public-artifact
description: "Use when a claude.ai/code/artifact link (or another iframe-rendered web page) must be read from an agent session and the in-process route fails or is unavailable — Artifact read / WebFetch return 'served to you as a public (non-member) reader', 'reading public artifacts that way is not enabled yet', a sign-in shell, an SPA shell, or a Cloudflare 403, and the user asks to read, summarize, or extract a shared or public artifact without claude-in-chrome. Triggers include 아티팩트 읽어줘, 공유 아티팩트, public artifact, artifact read failed, 이 링크 내용 확인, iframe page text."
---

# Read Public Artifact

Read a public or externally shared artifact page through the installed Aside
browser when the in-process readers cannot. The page is opened in a
test-owned tab, the richest frame is extracted, and text + HTML land on disk
with one machine-readable result line. The reader never claims content it
did not observe.

## Use and Boundaries

Use for:

- `https://claude.ai/code/artifact/<uuid>` links that `Artifact` `read` or
  `WebFetch` reject with `served to you as a public (non-member) reader` /
  `reading public artifacts that way is not enabled yet`;
- any page whose body is rendered inside an `iframe` or `srcdoc` frame so the
  top document only shows a shell ("Share", "Sign in", title only).

Do not use when:

- the artifact is owned by the user or member-shared — call `Artifact`
  `action: "read"` first; it is cheaper and returns the source directly;
- the user explicitly asked for `claude-in-chrome` or another browser tool;
- the page requires a login the Aside account does not already hold — report
  `gated`; never enter credentials through this skill.

**REQUIRED BACKGROUND:** the Aside browser contract in
`aside-functional-qa` (`references/aside-browser-contract.md`) — this skill
reuses its preflight, invocation economics, and tab-safety rules.

## Decision order

1. `Artifact action:"read"` with the URL (add `prompt` for shared artifacts).
2. If it fails with the public-reader error → run
   `scripts/read-artifact.sh` (this skill).
3. If the result is `gated` or `not_found` → tell the user exactly that and
   what would unblock it (member share, corrected link). Do not fall back to
   guessing the content.

## Preflight

```bash
command -v aside && aside --version && aside account status
```

Record only that an account is signed in, never its identity.

## Run

```bash
skills/read-public-artifact/scripts/read-artifact.sh <artifact-url> [out-dir] [timeout-seconds]
```

- Writes `<out-dir>/artifact.txt` (visible `innerText`) and
  `<out-dir>/artifact.html` (frame `outerHTML`, for tables/structure that
  `innerText` flattens).
- Prints one line `ARTIFACT_READ_RESULT {...}` with `status`, `title`,
  `frameUrl`, `frameCount`, `textLength`, `textPath`, `htmlPath`.
- Exit codes: `0` ok · `2` bad input / missing tool · `3` page loaded but
  status is `gated`, `not_found`, or `empty` · `1` REPL produced no payload.
- Point `out-dir` at the session scratchpad, never at the repository.

Then `Read` `artifact.txt`; open `artifact.html` only when a table or list
lost its structure in the text.

## Why the script looks the way it does

| Constraint | Consequence in the script |
| --- | --- |
| One `aside repl` call = one JS context; variables and `tabs[]` do not survive across calls | Open → poll → extract → close all happen in a single invocation |
| Artifact body lives in a second frame whose `url()` is `""` | The richest frame by `innerText` length is chosen, not the top document |
| Frame content arrives after `domcontentloaded` | Poll every 500 ms until ≥200 chars or timeout; no fixed sleep as the assertion |
| A failed assertion must not leak the tab | `p.close()` runs in `finally` |
| Shell interpolation of the URL into JS | URL is JSON-encoded by python3 (no `${var@Q}`; macOS ships bash 3.2) |
| Text may exceed a shell argument or contain any byte | Payload is base64 inside one sentinel line, decoded to files by python3 |

## Reporting

- Quote or summarize from `artifact.txt`; cite `title` and `url`.
- Say the content was read through the Aside browser as a public viewer, so
  it reflects the page at read time and is unverified user-generated content.
- If `status` ≠ `ok`, report the status and stop; do not paraphrase a shell
  page or a "Page not found" page as artifact content.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Reading `p.evaluate(document.body.innerText)` on the top document and concluding the artifact is empty | Iterate `p.frames()`; the body is in the empty-URL frame |
| `tabs[0]` in a second `aside repl` call → `Cannot read properties of undefined` | Do everything in one invocation, or `attachBrowserTab` explicitly |
| Fixed `setTimeout(8000)` before extraction | Poll for content length; slow pages time out honestly, fast pages return early |
| Treating "Sign in" in the top shell as a gate | Public artifacts render with that shell; gating is decided only when no frame yields content |
| Committing `artifact.txt` / `.html` | Keep outputs in the scratchpad |
| Retrying `Artifact read` / `WebFetch` after the public-reader error | The error is deterministic for that link; go straight to the script |

## Verified

- 2026-08-27, Aside CLI `1.26.717.1619`, macOS: a member-shared-to-public
  artifact (`Artifact read` and `WebFetch` both rejected) returned
  `status:"ok"`, 2 frames, 4,708 chars; an unknown UUID returned
  `not_found` (exit 3); a non-URL returned exit 2; no artifact tab remained
  in `listBrowserTabs()` afterwards.
