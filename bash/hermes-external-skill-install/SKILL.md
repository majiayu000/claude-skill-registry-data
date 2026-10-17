---
name: hermes-external-skill-install
description: |-
  Install pre-built external AI agent skills from GitHub (agentskills.io / Claude Code / OpenClaw ecosystem) directly into Hermes Agent's skills directory.
  Two methods: (1) `npx skills add` (agentskills.io CLI) — fast but may fail on format, (2) `git clone` fallback — always works, preserves subdirectory skills and assets.
  Use when the user says "装一下这个skill", "安装这个技能", "装个XX", "install this skill", or points to a GitHub repo that contains a SKILL.md.
---

# Hermes 外部 Tool/Skill 安装工作流

Install external tools or skills from GitHub repos into Hermes. Covers two distinct cases:

- **Case A (pure skill):** Repos that are just SKILL.md + references — install directly into Hermes skills directory
- **Case B (tool-with-skill):** Full AI application repos that happen to have a SKILL.md — they need their own dev directory, dependency installation, system requirement verification, API key setup, and THEN symlink into Hermes as a skill

## 触发条件

- 用户指向一个 GitHub 仓库并要求安装（"装一下这个skill"、"安装xx"、"装一下祂"、"install the skill from github.com/...", "看看这个" → "你先安装一下祂"）
- 仓库包含 `SKILL.md`
- 用户提到 `npx skills add` 或 `skills add` 但命令失败
- 用户问"这些 skill 从哪来的"、"给其他 agent 也装这些" → 先查 `references/hermes-management-skills.md` 获取已知来源
- 用户问"ClawHub 里有没有 X" → 直接 `clawhub search` + 参考 `references/clawhub-toon-example.md` 里的评估矩阵模式

## 决策分支: Pure Skill vs Tool-with-Skill vs npm-Package Skill Generator

Before proceeding, classify the source:

| Signal | Pure Skill (Case A) | Tool-with-Skill (Case B) | npm-Package Generator (Case C) | ClawHub Skill (Case D) |
|--------|-------------------|-------------------------|-------------------------------|------------------------|
| Source format | GitHub repo URL | GitHub repo URL | `npm install -g @scope/package` | `clawhub search <query>` then `clawhub install <slug>` |
| Has `SKILL.md` directly | ✅ Yes | ✅ Yes (within repo) | ❌ No — CLI **generates** SKILL.md files | ✅ Yes (in registry) |
| Has `pyproject.toml` / `package.json` | ❌ No | ✅ Yes | ✅ Yes (the npm package itself) | ⚠️ Optional — some are pure docs, some bundle scripts |
| Has system deps | ❌ Minimal | ✅ Yes (ffmpeg, brew, etc.) | ⚠️ May need companion tools (e.g., openspec CLI) | ⚠️ Variable — check `scripts/` field on hub page |
| Workflow | Clone SKILL.md | Clone app + install deps + symlink | `npm install -g` → `tool init` → copy generated skills | `clawhub search` → evaluate → `clawhub install <slug>` (and possibly copy bundled scripts to PATH) |
| Example | `alchaincyf/nuwa-skill` | `browser-use/video-use` | `@rpamis/comet` (generates 28 platform skill sets) | `@bonk-moltbot/toon`, `@zmkkevin/toon-json` |

**Decision rule:** If the user points to an npm package name (or gives a GitHub repo for an npm package) that is a CLI generating SKILL.md files for multiple AI coding platforms, treat as Case C.

**Decision rule (D):** If the user says "找一下有没有 X skill" / "看看有没有装 X" / "装个 X skill" without naming a specific repo, and ClawHub is the installed marketplace CLI (`clawhub --version` to confirm), use **Case D**. Always evaluate multiple candidates before installing — the top-rated search hit is not always the right one. See Case D section below.

---

## Case D: ClawHub Skill Discovery & Evaluation

For users who ask "有没有 X skill" or want to browse the registry without naming a specific repo. ClawHub is the official OpenClaw skill marketplace.

### D0: Confirm ClawHub is installed

```bash
clawhub --version   # should print "ClawHub CLI vX.Y.Z"
```

If not installed: `npm install -g @openclaw/clawhub` (Case C workflow).

### D1: Search — only one command works

**Pitfall:** `clawhub info <slug>` does NOT exist. The CLI only has: `search`, `install`, `update`, `uninstall`, `list`, `pin`, `unpin`, `login`, `logout`, `whoami`, `auth`. Running `clawhub info foo bar` returns a usage error every time.

```bash
# ✅ Correct
clawhub search <query>

# ❌ Wrong (no such command)
clawhub info <slug>
```

The `search` output is a vertical list with author, name, and a relevance-style score:
```
- Searching
toon  @bonk-moltbot  Toon  (3.690)
toon-adoption-skill  @nelohenriq  TOON  (2.515)
toon-json  @zmkkevin  Shrink JSON in Prompts (TOON Encoder/Decoder)  (2.513)
toonany  @casperkwok  Toonany  (1.490)
```

### D2: Evaluate candidates — the matrix pattern

The top hit by score is **not always the right one**. Pull each candidate's hub page and build a matrix before deciding.

**Pitfall:** The hub URL is `https://hub.openclaw.ai/<author>/<slug>`, NOT `clawhub.dev` (returns 404 / fetch errors) and NOT `clawhub.ai` (different page).

```bash
web_extract urls=["https://hub.openclaw.ai/<author>/<slug>"]
```

Compare on at least these axes:

| Axis | What to check | Why it matters |
|------|---------------|----------------|
| **Positioning** | What is the skill FOR? (encoding tool / spec doc / pipe wrapper / SDK binding) | A pure spec doc with no scripts gives the agent nothing to run |
| **Spec version** | If the skill claims a version (e.g., "TOON v1") and a reference SDK exists with a different version (e.g., `@toon-format/toon` v3.3), flag the mismatch | Round-trip may fail silently |
| **Implementation** | Bundled script? Wraps official CLI? Or pure docs? | Pure docs → agent has to write code each time → unreliable |
| **Dependency** | Self-contained / needs `npx` / needs Python / needs system binary | Drives install path |
| **Reliability** | Author's track record, last updated, recent commits | Stale = likely broken against latest deps |
| **Hermes fit** | Does installing give me a SKILL.md I can read, a script in PATH I can run, or both? | `clawhub install` puts things in `skills/`, NOT `bin/` |

**Decision rule of thumb:**
- If multiple candidates exist, prefer the one using the **official upstream CLI/SDK** over independent reimplementations (avoids version drift).
- Prefer a skill that exposes a **runnable command** over one that just teaches the agent the syntax.
- Avoid "pure teaching" skills (`xxx-adoption`, `xxx-guide`) unless the agent already has a reliable encoder/decoder to use.

### D3: Install — and copy bundled scripts to PATH

```bash
clawhub install <slug>
```

**Pitfall (CRITICAL):** `clawhub install <slug>` puts the SKILL.md and bundled files in `~/.hermes/skills/<dir>/<slug>/`. It does **NOT** copy any executable scripts into `~/.local/bin` or anywhere on `$PATH`. For skills whose value is a wrapper script (e.g., `@bonk-moltbot/toon` ships `scripts/toon` which wraps `npx @toon-format/cli`), `install` alone is insufficient.

**Empty-shell trap (verified 2026-07-12):** A ClawHub skill's SKILL.md may **describe** a `scripts/<bin>` wrapper without shipping one. `clawhub install @bonk-moltbot/toon` produced a package containing only `_meta.json`, `SKILL.md`, `skill-card.md`, `.clawhub/origin.json` — **zero executable files**. The README said "Copy script to PATH: `cp scripts/toon ~/.local/bin/`" but `scripts/` didn't exist. Always verify before recommending the install path:

```bash
# After clawhub install, before any "cp scripts/<bin>" recommendation:
ls ~/.hermes/skills/<dir>/<slug>/scripts/ 2>/dev/null | head
# If empty/missing: skill is doc-only, write your own wrapper or pick a different skill
```

**If the script does exist**, copy + chmod + verify:

```bash
cp ~/.hermes/skills/<dir>/<slug>/scripts/<bin> ~/.local/bin/
chmod +x ~/.local/bin/<bin>
command -v <bin>     # verify
```

If `~/.local/bin` isn't on the user's `$PATH` (Hermes TUI launches from fish via .bashrc — verify with `echo $PATH | tr ':' '\n' | grep local/bin`), symlink into a PATH dir that IS populated:

```bash
ln -sf ~/.hermes/skills/<dir>/<slug>/scripts/<bin> ~/.npm-global/bin/<bin>
# or whichever dir the user's PATH includes
```

**When the skill is empty-shell but the underlying SDK is installed locally**, write your own minimal wrapper (15-30 lines) rather than skipping. Example: `@toon-format/toon` was already in `~/.npm-global/lib/node_modules/` so a 14-line Node ESM wrapper at `~/.local/bin/toon` was cleaner than installing the broken skill.

### D4: Verify

```bash
skills_list | grep -i <name>          # skill registered
skill_view <name>                     # SKILL.md loads
ls ~/.hermes/skills/<dir>/<slug>/     # files present
[ -x ~/.local/bin/<bin> ] && echo OK  # if bundled a script
```

### D5: Worked example — installing TOON format

See `references/clawhub-toon-example.md` for the full evaluation matrix and install steps from the 2026-07-12 session (4 candidates evaluated, original recommendation `@bonk-moltbot/toon` was **overturned** after install verification: skill shipped without its promised `scripts/toon` wrapper — empty shell). The actual shipped artifact was a 14-line Node ESM wrapper at `~/.local/bin/toon` that imports the locally-installed `@toon-format/toon` SDK directly. Lesson: never recommend an install path without `ls scripts/` after `clawhub install`.

### A1: 判断安装方法

如果用户给的仓库名遵循 `owner/repo` 格式（如 `alchaincyf/nuwa-skill`），先尝试 agentskills.io CLI：

```bash
npx skills add owner/repo
```

如果用户直接给了完整 URL，跳过此步，直接用 A2.

#### A1a: npx skills add 成功判定
- 输出包含 `✔ Skill installed` → 成功，跳到验证
- 输出 `No valid skills found` / `Skills require a SKILL.md with name and description` → 格式不兼容，走 A2
- 输出其他错误 → 检查网络，重试一次，不行走 A2

### A2: git clone 回退方案（通用）

```bash
git clone --depth 1 https://github.com/<owner>/<repo> ~/.hermes/skills/openclaw-imports/<skill-name>
```

#### A2c: 批量 cp 模式（适用于大型仓库，子目录含多个独立 skill）

当仓库很大（数千文件）且技能散落在 `skills/` 子目录中时，clone 到 `~/projects/`（持久参考位置），用 `cp -r` 选择性安装到 Hermes skills 目录：

```bash
# 1. Clone 到持久位置（不是 ~/.hermes/skills/ 下）
git clone --depth 1 https://github.com/<owner>/<repo> ~/projects/<repo>

# 2. 创建分类目标目录
mkdir -p ~/.hermes/skills/<category>/<skill-family>

# 3. 选择性复制需要的 skill 子目录
for skill in skill-a skill-b skill-c; do
  src="$HOME/projects/<repo>/skills/$skill"
  [ -d "$src" ] && cp -r "$src" ~/.hermes/skills/<category>/<skill-family>/$skill
done

# 4. 验证
ls ~/.hermes/skills/<category>/<skill-family>/ | wc -l
```

**使用 cp 而非 ln 的场景**：
- 仓库不仅包含 skills，还有大量非技能资产（测试、CI、源文件）
- 只需要仓库中的一部分 skills
- 需要修改 SKILL.md 以适应 Hermes（如调整 frontmatter）

**选择性复制技巧**：先用 `find ~/projects/<repo>/skills -name 'SKILL.md' | head -20` 查看有哪些 skill，再根据用途筛选。

#### 关键参数
- `--depth 1` — 浅克隆
- 目标路径: `~/.hermes/skills/openclaw-imports/<skill-name>`
- 超时处理：设置 120s+ 超时；如果中途被超时打断，先 `rm -rf` 再重试
- 网络限制：WSL 下若 git clone 超时，显式传递 proxy: `git -c http.proxy=http://127.0.0.1:7890 clone ...`

### A2b: 大规模多技能安装（子目录批量模式）

部分仓库（如 `scientific-agent-skills`）在一个 repo 内含 **数百个技能**，存放在 `scientific-skills/`、`skills/` 等子目录中。直接 clone 到 `~/.hermes/skills/` 会混入非技能文件。正确做法：

1. **克隆到持久化位置**（而不是 `~/.hermes/skills/` 下）：

   ```bash
   mv /tmp/<repo> ~/.hermes/<repo>        # 如果已在 /tmp 中
   # 或直接：
   git clone --depth 1 https://github.com/<owner>/<repo> ~/.hermes/<repo>
   ```

2. **批量创建软链接**：遍历子目录下的每个技能目录，逐一链接到 `~/.hermes/skills/`：

   ```bash
   cd ~/.hermes/skills/
   for dir in ~/.hermes/<repo>/<skills-subdir>/*/; do
       name=$(basename "$dir")
       [ ! -d "$name" ] && ln -s "$dir" "$name"
   done
   ```

3. **验证**：
   - 计数：`ls ~/.hermes/skills/ | wc -l` — 确认总数合理增加
   - 抽查：`skills_list` 确认新技能出现在列表中
   - 内容：`skill_view <任意-skill>` 确认 SKILL.md 可读

4. **注意 symlink 目标路径**：使用绝对路径 `~/.hermes/...` 而非相对路径，避免因目录变更导致断链。

#### 技能名推断
优先使用 SKILL.md 中的 `name:` frontmatter，否则从 repo slug 推断。

### A3: 验证注册状态

```bash
skills_list
skill_view <skill-name>
```

### A4: 处理子目录技能

外部仓库可能将多个技能放在 `examples/` 子目录中。Hermes 会自动发现这些子目录中的 SKILL.md 并注册为独立 skill — 无需额外操作。

---

## Case B: Tool-with-Skill Install (Application Workflow)

For repos that are full AI applications with a skill interface (e.g., `browser-use/video-use`).

### B1: 克隆到开发目录

Clone to `~/Developer/` (NOT directly into Hermes skills dir), because the tool has its own deps, venv, and scripts:

```bash
cd ~/Developer
git clone https://github.com/<owner>/<repo>.git
# If proxy needed: git -c http.proxy=http://127.0.0.1:7890 clone ...
```

### B2: 安装系统依赖

检查 `install.md` 或 `README.md` 了解系统依赖需求。常见的有：

| 依赖 | WSL Arch | macOS |
|------|----------|-------|
| ffmpeg/ffprobe | `pacman -S ffmpeg` | `brew install ffmpeg` |
| yt-dlp | `pip install yt-dlp` 或 `uv pip install yt-dlp` | `brew install yt-dlp` |
| Node.js | `pacman -S nodejs npm` | `brew install node` |

⚠️ 先检查是否已安装（`command -v` 而不是 `which`，在 WSL Arch 下 `which` 可能不存在）：

```bash
command -v ffmpeg && ffprobe -version | head -1
```

### B3: 安装 Python 依赖

The tool likely has its own `pyproject.toml`:

```bash
cd ~/Developer/<repo>
uv sync   # or: pip install -e .
```

Note: If the tool's `.venv` conflicts with Hermes' active venv, that's fine — `uv sync` creates and uses its own `.venv` inside the repo.

### B4: 配置 API Keys

Check if the tool needs API keys. Common key locations: `.env.example` → `.env`.

If a key is needed and not set, ask the user once:
> "I need an `<provider>` API key for transcription / generation. Grab one at `<url>` and paste it here — I'll write it to `~/Developer/<repo>/.env`. Or if you already have it exported, say 'use env'."

Key rules:
- Never echo the key back in tool output
- Never commit `.env`
- After writing, sanity-check with a low-cost call (e.g., 200 response = key works)

### B5: 注册为 Hermes Skill

**两种链接模式**，根据 SKILL.md 位置选择：

**模式 1 — SKILL.md 在仓库根目录**: symlink 整个仓库（`helpers/`、`scripts/` 等相对 SKILL.md 解析）：

```bash
mkdir -p ~/.hermes/skills/<category>
ln -sfn ~/Developer/<repo> ~/.hermes/skills/<category>/<skill-name>
```

**模式 2 — SKILL.md 在子目录**（如 `skills/<name>/SKILL.md`）: 只 symlink 该子目录，不要链整个仓库（仓库根有 docs、examples、viewer 等非技能资产）：

```bash
mkdir -p ~/.hermes/skills/
ln -sf ~/Developer/<repo>/skills/<skill-name> ~/.hermes/skills/<skill-name>
# 或等价: ln -sf ~/projects/<repo>/skills/<skill-name> ~/.hermes/skills/<skill-name>
```

**判定方法**: 查看仓库结构——`ls <repo>/` 看根目录是否有 SKILL.md。如果没有，`find <repo> -name SKILL.md -maxdepth 3` 找到实际位置，按模式 2 处理。

**Category choice rule of thumb:**
- `productivity/` — most AI tools (video, image, editing)
- `devops/` — deployment, monitoring tools
- `creative/` — art, animation tools

**Skill name:** Use the repo slug (e.g., `video-use`).

### B6: 验证

```bash
skills_list                    # confirm it shows up
skill_view <skill-name>        # confirm SKILL.md loads
ls ~/.hermes/skills/<category>/<skill-name>/helpers/   # scripts accessible?
```

### B7: 告知用户

告诉用户安装完成 + 下一步怎么做。格式示例：

```
video-use 已安装到 ~/Developer/video-use，已注册为 Hermes skill。
就缺 ElevenLabs API key 了——拿到后放到 .env 里就能用。
用法：把素材丢到文件夹，跑 Hermes 说"edit these into a launch video"即可。
```

---

## Case C: npm-Package Skill Generator Install

For npm packages whose CLI generates SKILL.md files for other AI coding ecosystems (Claude Code, Cursor, OpenCode, etc.) and should be ported to Hermes.

### User Preference

Many users prefer the **native/original** skill files over adapted versions — they want what the tool's ecosystem provides, not a reimplementation. Always install the original CLI and generate its skill files first, then copy/adapt for Hermes.

### C1: Install the npm CLI

```bash
npm install -g @scope/package
```

Verify: `package --version`

### C2: Generate Skill Files for Any Platform

Run the tool's `init` command in a temp directory to generate its skill files:

```bash
mkdir -p /tmp/<tool>-test && cd /tmp/<tool>-test
<tool> init --yes   # or --tools all, etc.
```

Key things to verify:
- The tool supports many platforms (28+ in Comet's case). Pick one platform's output (e.g., `.claude/skills/`) as the source.
- Check what it generated: `find /tmp/<tool>-test -name 'SKILL.md'`
- Check for companion scripts: `find /tmp/<tool>-test -name '*.sh'`

### C3: Identify Companion CLI Dependencies

Many skill generators depend on companion CLI tools that are also npm packages:

| Tool | Companion CLI | Install |
|------|--------------|---------|
| Comet (`@rpamis/comet`) | OpenSpec (`@fission-ai/openspec`) | `npm install -g @fission-ai/openspec` |

Initialize the companion tool too:
```bash
mkdir -p /tmp/<companion>-test && cd /tmp/<companion>-test
<companion> init --tools all --force   # generates its own skill set
```

### C4: Copy Skills to Hermes

Create a category directory under `~/.hermes/skills/` and copy all generated skills:

```bash
# Create category
mkdir -p ~/.hermes/skills/<category>

# Copy main tool's skills
for skill in /tmp/<tool>-test/.claude/skills/<tool>-*; do
  name=$(basename "$skill")
  cp -r "$skill" ~/.hermes/skills/<category>/"$name"
done

# Copy companion tool's skills
for skill in /tmp/<companion>-test/.claude/skills/<companion>-*; do
  name=$(basename "$skill")
  cp -r "$skill" ~/.hermes/skills/<category>/"$name"
done

# Copy any companion ecosystem skills (e.g., Superpowers from .agents/skills/)
for skill in /tmp/<tool>-test/.agents/skills/*; do
  name=$(basename "$skill")
  # Skip if Hermes already has an equivalent
  if [ ! -d ~/.hermes/skills/<target-category>/"$name" ] && [ ! -d ~/.hermes/skills/"$name" ]; then
    cp -r "$skill" ~/.hermes/skills/<target-category>/"$name"
  fi
done
```

### C5: Copy Companion Scripts

Tools like Comet include bash scripts for state management, guard checks, validation, and archiving:

```bash
cp /tmp/<tool>-test/.claude/skills/<tool>/scripts/*.sh ~/.hermes/skills/<category>/scripts/
```

### C6: Fix Hermes-Specific Paths (Critical)

The generated SKILL.md files and scripts contain platform-specific path references (e.g., `$HOME/.claude/skills/`) that won't work in Hermes. You must patch them:

**Common fixes needed:**
- Search roots: Add `"$HOME/.hermes/skills/<category>"` to bash script search roots
- Alternative find patterns: Add `-o -path '*/scripts/*.sh'` alongside platform-specific paths
- Error messages: Update to reference Hermes paths

Example (Comet-specific):
```
COMET_SEARCH_ROOTS=( "." "$HOME/.hermes/skills/comet" "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.cursor/skills" )
COMET_GUARD=$(find ... -path '*/comet/scripts/comet-guard.sh' -o -path '*/scripts/comet-guard.sh')
```

### C7: Verify Registration

```bash
# Check via Hermes CLI
hermes skills list 2>/dev/null | grep -i '<tool>'

# Load and verify
skill_view <tool-or-skill-name>
```

### C8: Clean Up Temp Files

```bash
rm -rf /tmp/<tool>-test /tmp/<companion>-test
```

### C9: Save to Memory

Record the installation facts so future sessions know what's available.

### Known Pitfalls

- **Overlapping skills**: The companion ecosystem may include skills that Hermes already has (e.g., Superpowers' subagent-driven-development, TDD, writing-plans). Check before copying to avoid conflicts.
- **Script path resolution**: Generated bash scripts often use hardcoded or narrow search roots. Always add Hermes' skills directory to the search paths and test with a dry run.
- **CLI init fails**: Some tools' `init` commands are interactive-only and lack `--yes`/`--force` flags. In that case, manually create the test directory and inspect the npm package's bundled skill files directly under `node_modules/`.
- **`which` not available**: WSL Arch may lack `which`. Use `command -v` for binary checks.

---

## 快速判断:这是"装 skill 的 skill"问题吗?

当用户问"有没有 X 市场的 skill" / "skill 市场" / "skill 商店"时,先查本 skill 是否覆盖 — 大概率就是这一个。常见来源对照:

| 用户说的 | 真实定位 | 装/查方式 |
|---------|---------|----------|
| "Hermes skill 市场" / "https://hermes-agent.nousresearch.com/docs/zh-Hans/skills" | 本 skill 直接覆盖(12 个注册源、agentskills.io 索引) | `npx skills add <owner/repo>` 或 git clone |
| "AstrBot 插件市场" | **不是本 skill** — 走 `_archive/skill-finder-cn` 或 AstrBot 原生 plugin marketplace | 别误推荐本 skill |
| "Claude Code / OpenCode / Cursor skills" | 同源,SKILL.md 格式通用,本 skill Case A 可装 | 直接装 |
| "Hermes 文档" (查/读) | **不需要 skill** — `hermes-agent` umbrella + `web_extract` / `browser_*` 已经是答案 | 别造新 skill |

**坑**: `_archive/skill-finder-cn` 只覆盖 AstrBot 插件市场。看到"skill 市场"先想本 skill,别跳到 skill-finder-cn。

## 查 Hermes 文档的快捷方式

不需要额外 skill。`hermes-agent` umbrella + `web_extract` 已覆盖。`.md` 后缀 URL 走 `web_extract` 极快:

```bash
# 文档页通常是 HTML,但 raw .md 走 raw.githubusercontent.com / 静态 .md 端点
web_extract urls=["https://hermes-agent.nousresearch.com/docs/zh-Hans/skills"]
# 或 curl 拿 markdown
curl -s https://hermes-agent.nousresearch.com/docs/zh-Hans/<slug>.md
```

JS 重度页(Skills Hub 目录页)用 `browser_console` + `document.body.innerText.slice(0, N)` 拿分类目录,别死等 `browser_snapshot` 超时(30s 必挂)。

## 已知问题 (All Cases)

### 1. npx skills add 格式兼容性

`npx skills add` 底层使用 agentskills.io 的 SKILL.md parser，对 frontmatter 格式要求严格。即使 SKILL.md 包含 `name:` 和 `description:` 字段也可能失败。遇到此情况直接走 git clone 即可。

### 1b. npx skills add 交互式选择卡住

当仓库包含多个 skill 时，`npx skills add` 可能进入交互式选择界面（space to toggle → Enter to confirm），在非 PTY 终端下无法完成。现象：输出停在 `Select skills to install` 提示后不继续。此时直接走 A2 git clone 方案，不重试 npx。

### 2. 大仓库超时

大仓库（含 PNG/JPG/PDF）在 WSL 下 git clone 可能超时：
- 解决：`--depth 1` + 120s timeout
- 如果仍然超时: `curl -L https://api.github.com/repos/owner/repo/tarball | tar xz -C <target> --strip-components=1`

### 3. 网络限制 (WSL)

WSL 下 GitHub/pypi 下载可能因代理问题不稳定：

- `command -v curl` → `curl -s --connect-timeout 5 https://github.com` 检查连通性
- 如果 curl 通但 git 不通，显式传递代理:
  ```bash
  git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone ...
  ```
- 如果还是超时 → 退化为 GitHub tarball 方式（见 #2）
- **AtomGit 国内镜像回退**（GitHub 直连 + 代理均超时时使用）: 部分热门开源项目在 [atomgit.com](https://atomgit.com) 有镜像。将 `github.com/<owner>/<repo>` 替换为 `atomgit.com/<owner>/<repo>`。示例：
  ```bash
  # GitHub 失败时:
  git clone --depth 1 https://atomgit.com/hugohe3/ppt-master.git
  ```
  ⚠️ 不是所有项目都有镜像——先访问 `https://atomgit.com/<owner>/<repo>` 确认存在。

- **大文件 zip 下载不完整风险**: GitHub archive zip 可能超过 500MB。curl 下载时若中途超时或被限速，文件大小不足且 unzip 报 `End-of-central-directory signature not found`。优先用 git clone（可续传），不用 curl + zip。

#### 代理策略区分：git config vs 环境变量

| 目标 | 需要 | 示例 |
|------|------|------|
| `git clone` | `git config --global http.proxy` 或 `-c` 参数 | `git -c http.proxy=http://127.0.0.1:7890 clone ...` |
| `pip install` + httpx 下载 | `HTTP_PROXY` / `HTTPS_PROXY` 环境变量 | `HTTP_PROXY=http://127.0.0.1:7890 pip install ...` |
| Python 运行时 httpx 下载 | 同上，环境变量 | `HTTP_PROXY=... python3 -c "from cloakbrowser import launch; ..."` |

🚨 **痛点案例**: `pip install cloakbrowser` 成功（pip 走代理），但首次 `launch()` 触发 ~200MB Chromium 二进制下载时失败（httpx 不读 git config，需要 `HTTP_PROXY` 环境变量）。解决方案：启动前显式设环境变量。

```bash
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 python3 -c "..."
```

### 4. Symlinked script paths in multi-platform repos

Some external skills (e.g., ui-ux-pro-max) use a multi-platform structure where the `SKILL.md` lives in `.claude/skills/<name>/` but its referenced scripts and data live in `src/<name>/scripts/`. The `.claude/` directory may contain **symlinks** to `src/`. 

This means:
- `skill_view(name)` → `linked_files` may report scripts at `.claude/skills/<name>/scripts/`
- Trying to run from that path may fail or resolve differently
- The actual runnable scripts are at `src/<name>/scripts/`

**Fix:** Before running scripts referenced by linked_files, locate them:
```bash
find ~/.hermes/skills/openclaw-imports/<repo> -name "search.py" -type f
```
Check each result; prefer the one under `src/` (the canonical source) over `.claude/` or `cli/assets/`.

### 5. WSL Arch: `which` 命令不可用

WSL Arch 的最小化安装可能没有 `which` 命令。始终使用 `command -v` 来检查可执行文件是否存在。

### 6. 追溯 skill 来源时，`git remote -v` 不可靠

**陷阱**: 技能目录下的 `git remote -v` 显示的是本地 workspace 跟踪仓库（如 `publieople/hermes-workspace`），**不是**技能的原始安装来源。skill 安装后，其目录可能被本地 workspace 的 git 覆盖，remote 会指向本地仓库而非源头。

**正确做法**: 追溯 skill 来源时，不要只看本地 git remote。优先级：
1. 搜索 session 历史（`session_search`）找安装记录——看当时用的 `npx skills add`、`clawhub install` 还是 `git clone`
2. 检查 `_archive/openclaw-imports/` 下的 `DESCRIPTION.md` 或安装时的会话上下文
3. 在 ClawHub 搜索技能名（`clawhub search <name>` 或网页 clawhub.ai）
4. 比对已知公开仓库（`yfge/skill-finder`、`K-Dense-AI/scientific-agent-skills`、`openclaw/agent-skills` 等）

**常见案例**: 本地 `git remote` 显示 `publieople/hermes-workspace`，但技能实际来自 `clawhub install skill-vetter` 或 `npx skills add yfge/skill-finder`。如果不区分，会把私有 workspace 链接误发给其他 agent 导致无法访问。

## 验证清单

每次安装完成后检查：

- [ ] 代码已 clone 到正确位置（~/Developer/ 或 ~/.hermes/skills/）
- [ ] 系统依赖已安装（ffmpeg 等）
- [ ] Python 依赖已安装
- [ ] API keys 已配置（如需要）
- [ ] Hermes 技能已注册（skills_list + skill_view）
- [ ] 用户知道下一步怎么用
