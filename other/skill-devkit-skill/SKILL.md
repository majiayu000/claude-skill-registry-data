---
name: skill-devkit
description: >
  Set up and govern an Agent Skill repo. Use when the user wants to create a
  new skill from an empty folder, or take over an existing skill that has no
  versioning or rules yet. Builds versioning, baselines, changelog, change
  review, trigger phrases, packaging and pre-release checks, then hands future
  upgrades to the repo's own rules.
  从空文件夹新建一个 Agent Skill 技能仓库，或把已有、还没管起来的技能一次性接管：
  搭好版本号、基线、更新记录、改动审核、触发词、打包和发布前检查，之后按仓里写好的规则升级。
  触发：初始化技能仓库、初始化技能、初始化skill、新建一个技能、新建skill、
  创建技能、创建skill、开发一个技能、开发一个skill、帮我做个skill、
  建个skill仓库、把这个技能管起来、接管这个技能、收编这个skill、
  init skill、adopt skill、/skill-devkit、/init-skill、/new-skill、/skill-devkit adopt。
  空文件夹走新建；已有 SKILL.md 但还没管起来走接管。不要用于普通非空目录、
  已经管起来的仓的升级发版、项目日报待办周报。同义说法见 references/04-triggers.md。
metadata:
  short-description: "新建或接管技能仓库：版本、基线、打包、发布前检查"
---

# Skill 开发工具包（skill-devkit）

**从空文件夹新建技能仓库，或接管（收编）已有但还没管起来的技能：版本控制、冻结基线、升级记录、变更门禁、触发词、一键打包、发布审计。问完即落盘；之后升级按那个仓自己写好的规则走。**

一次对话写进文件夹的不是一篇 `SKILL.md`，而是一套能自己发版的开发仓。建好之后不再经过 skill-devkit：升版本、打基线、打 zip、A/B 审核都走那个文件夹自己的文件。

不是业务项目管理，不是常驻升级引擎，不是万能技能合集。

用法见 `examples/`（初始化 01～05、07；收编 17～20；半套恢复见 25；初始化之后升版本见 08、21～23；记升级需求见 24；写规则 / 打包 / 试用见 10、06、16）。能力落点见 README 清单。

## 工作区

初始化：打开**空的**那个文件夹（或本包半套落盘，见恢复节）。收编：打开**已有技能、尚无本包规范**的那个文件夹。本包装在用户级技能目录（探测见 `references/03-skill-roots.md`；Grok 常见为 `~/.grok/skills/`）。禁止把业务项目的 `ai/` 当 Skill 根。禁止在普通非空目录当空仓初始化。

## 路由

用户一句话里已给出的字段，不要再问。半套 / 已规范判定见 `references/00-core.md`（E 先于 C/D）。

| 用户信号 | 工作区 | 加载 |
|---|---|---|
| 初始化 / 开发一个 skill / 新建 / 创建 / 帮我做个 skill / 建个 skill 仓库 / 从零 / 脚手架 / 骨架 / init / scaffold / bootstrap / `/skill-devkit` / `/init-skill` / `/new-skill` | 空（或仅 `.git` / `.DS_Store` / `Thumbs.db`） | `references/01-init.md` |
| 同上 | 半套初始化（C） | `references/01-init.md` 恢复节 |
| 同上 | 已规范（E） | `references/01-init.md` §2（停止） |
| 同上 | 已有 `SKILL.md`、无种子痕迹 | `references/01-init.md` §2（停止，指路收编） |
| 同上 | 非空且无 `SKILL.md`、非半套 | `references/01-init.md` §2（停止，换空文件夹） |
| 收编 / 接管这个技能 / 把这个技能管起来 / 纳入基线 / 改造现有 skill / adopt / retrofit / `/skill-devkit adopt` | 有 `SKILL.md`、无痕迹、无 `governance/` | `references/02-adopt.md` |
| 同上 | 半套收编（D） | `references/02-adopt.md` 恢复节 |
| 同上 | 空 | 停止，指路初始化 |
| 同上 | 已规范（E） | 停止，已规范 |
| 同上 | 非空无 `SKILL.md` | 停止 |
| 升级 / 你是 Agent A / 你是 Agent B / 写 AP / 打基线 / 发版 / 执行升级 / 检查升级效果 / 检查开发仓实际升级效果 / 升级做完了核对一下 | 任意 | 停止。已初始化或收编的仓读它自己的 `governance/rules/skill-governance.md` 与 `upgrade-dual-agent.md` |

硬闸见 `references/00-core.md`。初始化正文 `01-init.md`。收编正文 `02-adopt.md`。探测 `03-skill-roots.md`。同义开口 `04-triggers.md`。

## 硬闸

1. **初始化**只允许 (a) 空文件夹或空 git 仓，或 (b) 本包半套落盘（C）。其它非空不写盘、不问「能不能在这里初始化」。
2. **收编**只允许：根上有 `SKILL.md`，不是本包自己，不在已探测的助手安装目录，版本多源冲突未决不写盘。已规范（E）停止。来源不明的 `governance/`（无种子痕迹）停止。半套收编（D）走恢复，不改正文。
3. 用户确认问答清单之前禁止写盘。
4. 新空仓版本固定 `0.1.0`。收编保留已有版本（无则 0.1.0），不因收编升版。
5. 已规范仓禁止再初始化、禁止再收编。收编禁止改写技能正文与已有规则文件。
6. 禁止生成业务项目管理文件。禁止把 `.git` 建在 `governance/` 里。
7. 禁止给本包或目标仓做用户自动升级。禁止默装进任何已探测的助手技能目录。
8. 初始化或收编结束后不要继续用本包识别该仓。

## 版本

本包：见 `VERSION`。目标仓初始化为 `0.1.0`，收编沿用已有版本，之后由那个仓的 `VERSION` + `governance/` 管。
