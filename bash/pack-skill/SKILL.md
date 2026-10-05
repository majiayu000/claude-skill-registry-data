---
name: pack-skill
description: 将任意 Qoder Skill 项目打包为分发包 zip。自动检测项目结构，包含全部项目文件，仅排除开发者/构建产物。当用户要求打包 skill、生成分发包、创建发布 zip 时使用。
---

# Pack Skill — 通用 Skill 分发包打包

## 触发场景

用户说"打包 skill"、"生成分发包"、"创建发布 zip"、"导出 skill"时调用。

## 设计原则

**包含全部，排除已知**——不预设任何 Skill 特有的目录结构。
任何符合 Qoder Skill 规范的项目（有 SKILL.md）都能打包。

## 执行流程

### Step 1：定位 Skill 根目录

检查当前工作区：

- 仓库根下存在 `ChronoPM-Project/SKILL.md` → Skill 根目录 = `ChronoPM-Project/`（v3.1.1 CR-G）
- 当前目录存在 `SKILL.md` → 当前目录即为 Skill 根目录
- 否则报错退出

### Step 2：读取版本信息

按优先级读取版本号：

1. `VERSION` 文件（纯文本）
2. `skill.json` 的 `version` 字段
3. 都没有 → 报错

同时从 `skill.json` 读取 `name` 字段作为包名（缺省用 `skill`）。

### Step 3：执行打包

运行本 skill 目录下的打包脚本：

**本机主路径（Python）：**

```bash
python tools/pack-skill/scripts/pack.py --skill-root <path>
```

**跨平台参考实现（PowerShell，执行策略受限时不可用）：**

```powershell
powershell -ExecutionPolicy Bypass -File ~/.qoder/skills/pack-skill/scripts/pack.ps1 -SkillRoot <path>
```

脚本逻辑：
1. 扫描 Skill 根目录下全部文件
2. 排除下方黑名单中的路径/模式（排除模型实读自 pack.ps1，单一事实源）
3. 其余全部打入 zip
4. 产物命名：`{BrandName}-Skill-v{version}.zip`（BrandName 取自 skill.json displayName 品牌前缀）
5. **单包（v4.0.0）**：只打 `--skill-root` 指向的那一个技能。`portfolio-skill/`、`query-skill/` 在 ChronoPM-Project 包内，随包打入，不另打 zip。`governance/migrations/`（仅当前 upgrade）与 `governance/contracts/skill-contract.md` 例外放行入包。

**建议先 DryRun 预览：**

```bash
python tools/pack-skill/scripts/pack.py --skill-root <path> --dry-run
```

### Step 4：验证产物

打包完成后检查：

1. **关键文件**：zip 内必须含 `SKILL.md`
2. **包体大小**：输出摘要供用户判断

## 排除清单（黑名单）

以下路径/模式**始终排除**：

| 类别 | 排除项 |
|---|---|
| 版本控制 | `.git/`、`.gitignore` |
| IDE/编辑器 | `.idea/`、`.vscode/`、`.qoder/` |
| 构建缓存 | `__pycache__/`、`*.pyc`、`*.pyo` |
| OS 元数据 | `.DS_Store`、`Thumbs.db` |
| 打包产物 | `*.zip`、`*.tar.gz` |
| 开发者治理 | `governance/`（例外放行 `governance/contracts/skill-contract.md` 与 `governance/migrations/` 当前 upgrade） |
| 测试 | `tests/`（如存在） |
| 架构文档 | `SKILL_BLUEPRINT.md`（开发者侧架构审查文档） |
| 治理规则 | `references/16-skill-governance-rules.md`（Skill 自身变更治理规则，开发者侧） |
| 模块图 | `SKILL_MODULE_MAP.md`（给人看的链路图，不进发行包） |

> **缺 `tests/`、`SKILL_BLUEPRINT.md`、`references/16-skill-governance-rules.md`、`SKILL_MODULE_MAP.md` 不是 bug**——这是产品化裁剪。打包脚本会打印「有意排除」表。
> `source-split-skill/`、`query-skill/`、`portfolio-skill/` **必须进包**（能力目录，不是第二个 Skill）。包内除根 `SKILL.md` 外禁止再有 `SKILL.md`。不要把这些目录列入 `excludeDirs`。
> `governance/` 默认整目录排除，但 `governance/contracts/skill-contract.md`（核心契约）例外放行——因为 `references/` 中 7 个运行时规则文件引用了它第 5 条。
> `SKILL_BLUEPRINT.md` 和 `references/16-skill-governance-rules.md` 是开发者侧架构/治理文档，PM 使用者运行时不需要。
> `tests/` 是"如存在则排除"，不是所有 Skill 都有。
> 如果某个 Skill 项目有自定义的开发者目录需要排除，用户可在打包前告知 AI，AI 通过脚本 `-Exclude` 参数传入。

## 脚本参数

| 参数 | 说明 |
|---|---|
| `-SkillRoot <path>` | Skill 项目根目录（必填） |
| `-OutputDir <path>` | 输出目录（默认同 SkillRoot） |
| `-DryRun` | 仅预览不打包 |
| `-Exclude <string[]>` | 额外排除的目录名（如 `"docs","examples"`） |

## 注意事项

- 脚本不假设任何 Skill 特有的目录结构（如 references/、assets/ 等）
- 新增的 Skill 标准目录不需要修改脚本——因为默认全部包含
- 产物命名：`{BrandName}-Skill-v{version}.zip`（BrandName 取自 skill.json displayName 品牌前缀，无 displayName 时脚本拒绝打包）

## 安装

本 skill 应安装到个人 skill 目录 `~/.qoder/skills/pack-skill/`。

安装命令（PowerShell）：

```powershell
Copy-Item -Recurse -Force "<本项目路径>/tools/pack-skill" "$env:USERPROFILE/.qoder/skills/pack-skill"
```
