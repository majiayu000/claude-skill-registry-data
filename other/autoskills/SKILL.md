---
name: autoskills
description: >
  扫描项目技术栈，自动安装最佳 AI agent skills。
  用 autoskills CLI 从 skills.sh 安装匹配的 skills。
  中文触发：自动技能、安装技能、技能扫描、装技能、autoskills
tags:
  - autoskills
  - skills
  - install
  - auto-detect
  - stack-detection
version: 1
---

Goal
- 用 autoskills CLI 扫描项目，自动安装匹配的 AI skills。
- 一行命令搞定，无需手动选。

Use when
- 用户说：自动技能、安装技能、技能扫描、装技能、autoskills、skill 安装、自动装技能
- 用户要给新项目快速配好 AI skills
- 用户想知道项目适合什么 skills

CLI
```bash
# 路径
export PATH="$HOME/.npm-global/bin:$PATH"

# 扫描 + 安装（跳过确认）
autoskills -y

# 只预览不装
autoskills --dry-run

# 指定 IDE
autoskills -a claude-code
autoskills -a cursor
autoskills -a claude-code cursor

# 版本
autoskills --version  # v0.2.7
```

安装位置
- skills 装到 `~/.claude/skills/`（symlink → `~/.agents/skills/`）

支持的技术栈
- 前端：React, Next.js, Vue, Nuxt, Svelte, Angular, Astro, Tailwind, shadcn/ui
- 后端：Node.js, Express, Hono, NestJS, Go, Spring Boot
- 移动：Expo, React Native, Flutter, SwiftUI
- 数据：Supabase, Prisma, Drizzle, Zod
- 测试：Vitest, Playwright
- 云：Vercel, Cloudflare, AWS, Terraform
- AI：Vercel AI SDK, ElevenLabs, Remotion

Workflow
1. `cd` 到目标项目目录
2. `autoskills --dry-run` 先看会装什么
3. `autoskills -y` 安装
4. 检查 `~/.claude/skills/` 或项目的 `.claude/skills/`

Manual install fallback（2026-04-23 实测）
- autoskills 的 skills.sh 注册表有部分条目已失效（404）。github/awesome-copilot 的路径从 `skills/*.md` 改成了 `agents/*.agent.md`。wshobson/agents 的 skill 在 `plugins/<category>/skills/<name>/SKILL.md` 子目录内。
- 手动安装流程：
  1. `gh api repos/<owner>/<repo>/contents/<path>` 获取文件
  2. 用 `base64.b64decode(data['content']).decode()` 解码
  3. 保存到 `~/.agents/skills/<name>.md`
  4. `ln -sf "../../.agents/skills/<name>.md" ~/.claude/skills/<name>.md`
- 具体路径：
  - github/awesome-copilot: `agents/<name>.agent.md`
  - wshobson/agents: `plugins/<category>/skills/<name>/SKILL.md`
  - sickn33/antigravity-awesome-skills: `skills/<name>/SKILL.md`
- 验证：`wc -c` 检查文件大小，< 100 字节 = 404 错误页，需删除

Pitfalls
- Node.js >= 22.6.0 必需（当前 v22.13.0 ✓）
- github 源的 skills 可能因网络问题失败，不影响其他源
- 安装可能较慢（从远程下载），设 timeout >= 120s
- `npm link` 后如 PATH 未更新，用全路径 `~/.npm-global/bin/autoskills`
- 安装在 home 目录时会扫描 home 下所有项目文件，可能误检技术栈
- 在具体项目目录下运行更精准
- **PATH 问题**（2026-04-23 实测）：`npm link` 装到 `~/.npm-global/bin/` 但该路径不在默认 PATH 中。需 `echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc` 并重载。或用全路径调用。
- github/awesome-copilot 的 skill 路径已从 `skills/*.md` 变为 `agents/*.agent.md`，autoskills 的适配器未跟上，会 404。手动装：
  ```bash
  curl -sL "https://raw.githubusercontent.com/github/awesome-copilot/main/agents/<name>.agent.md" \
    -o "$HOME/.agents/skills/<name>.md"
  ln -sf "../../.agents/skills/<name>.md" "$HOME/.claude/skills/<name>.md"
  ```
- skills.sh 注册表部分条目已失效（404），autoskills 无法自动处理，需手动验证或跳过
- 安装后检查：`ls ~/.claude/skills/` 和 `ls ~/.agents/skills/` 确认 symlink 有效
