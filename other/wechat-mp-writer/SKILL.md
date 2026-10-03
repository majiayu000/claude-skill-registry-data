---
name: wechat-mp-writer
description: Project-level workflow for turning GitHub repositories, URLs, local product materials, or markdown drafts into WeChat Official Account articles and draft-box submissions. Use when the user asks to write, adapt, illustrate, verify, or publish a WeChat/公众号 article, especially from a GitHub repo or existing technical/product material.
---

# WeChat MP Writer

Use this skill as the project orchestrator. It adapts the Hermes workflow to Codex and this repository.

## Local Resources

- Project workflow: `docs/github-to-wechat-codex-workflow.md`
- Content agent: `docs/content-agent/workflow.md` and `docs/content-agent/agent-prompt.md`
- Setup check: `tools/github-to-wechat/check-config.ps1`
- GitHub intake: `tools/github-to-wechat/fetch-github-repo.ps1`
- URL intake: `tools/github-to-wechat/url-to-markdown.ps1`
- Publish wrapper: `tools/github-to-wechat/publish-markdown-to-wechat.ps1`
- Project Skill configs: `.baoyu-skills/*/EXTEND.md`
- Visual direction: `wechat-visual-director`

## Workflow

1. Run or mentally apply setup checks.
   - If publishing is requested, run `tools/github-to-wechat/check-config.ps1`.
   - If only writing is requested, do not block on the SSH key.
   - Never print API keys or tokens.
2. Intake source material.
   - For GitHub repositories, use `fetch-github-repo.ps1` to save repo metadata, README, and a source ledger.
   - For generic pages, use `url-to-markdown.ps1`.
   - For local files, list the provided files and cite paths.
3. Establish evidence.
   - Label claims as verified, reasonable inference, unverified, or do-not-publish.
   - If evidence is insufficient, provide known facts, candidate hypotheses, verification paths, and temporary safe wording only.
4. Draft the article.
   - Follow the project content agent workflow.
   - Use `wechat-title-strategist` before locking the article title.
   - Keep the visible line: concrete pain -> product solution -> AI/technical judgment.
   - Avoid traffic-first writing, generic AI-tool review tone, invented adoption claims, and unverified business impact.
5. Plan visuals before generating.
   - Use `wechat-visual-director` before any image-generation Skill.
   - Use `baoyu-cover-image` only for the cover.
   - Use `baoyu-article-illustrator` for body visuals.
   - Prefer real screenshots for UI, CLI, repository evidence, and product states.
   - Use Codex native image generation when available; do not route image work through another computer's Codex CLI.
   - Save final prompts before generating images.
6. Publish only when the user wants a real WeChat draft.
   - Publish markdown, not pre-rendered HTML with base64 images.
   - Use remote-api via project config.
   - Personal subscription accounts can create drafts but require manual publish in WeChat backend.

## Visual Direction

Do not make every image from the same cover template.

- Architecture or workflow: flowchart/framework.
- Business mechanism: editorial infographic/comparison.
- Release or project history: timeline.
- Product contrast: comparison matrix.
- Workplace pain: scene illustration.
- UI or repository proof: real screenshot.

Use mobile-readable body images, usually `3:4` or `4:3`. Use `2.35:1` for covers.

## Publishing Rules

- Use `.baoyu-skills/.env` for credentials and keep it ignored.
- Use `baoyu-post-to-wechat` through `tools/github-to-wechat/publish-markdown-to-wechat.ps1`.
- Keep ordinary external links as bottom citations unless the user explicitly says otherwise.
- Do not use `--no-cite` by default.
- Do not claim publishing succeeded unless the command actually creates a draft and returns success.
