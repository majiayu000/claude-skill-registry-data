---
name: setup-deploy
preamble-tier: 2
version: 1.0.0
description: |
  为 /land-and-deploy 配置部署信息。自动识别部署平台、生产 URL、健康检查端点
  和 deploy 命令，并把结果写进 CLAUDE.md。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /setup-deploy

这是 `/land-and-deploy` 的一次性接线工具，用来把“这个项目怎样部署”沉淀到 `CLAUDE.md`。

## 什么时候用

- 第一次想用 `/land-and-deploy`
- 生产平台、URL、健康检查、deploy workflow 改过
- gstack 自动识别部署方式不准时

## 核心流程

1. 先检查 `CLAUDE.md` 里是否已有 Deploy Configuration。
2. 自动识别平台：
   - `fly.toml` -> Fly.io
   - `render.yaml` -> Render
   - `vercel.json` / `.vercel` -> Vercel
   - `netlify.toml` -> Netlify
   - 仅有 workflow -> GitHub Actions only
   - 都没有 -> Custom / Manual
3. 针对不同平台补齐应用名、生产 URL、健康检查方式、部署命令。
4. 把配置写入 `CLAUDE.md` 的 `## Deploy Configuration` 区块。
5. 做一次验证并输出总结。

## 关键规则

- 如果已存在配置，要先展示现状并询问是覆盖、保留还是退出。
- 自动识别不到时，用 `AskUserQuestion` 向用户补采信息，而不是胡乱猜。
- 输出的配置要面向以后复用，确保后续 `/land-and-deploy` 能直接读到。
