---
name: generate-release-notes
description: 为待发布版本整理面向用户的发布说明（更新说明）。当用户说生成发布说明 / release notes / 版本更新说明 / 某版本更新了什么 / 整理更新日志时使用。
disable-model-invocation: true
---

# 生成发布说明

把两个 tag 之间的变化整理成一份**面向使用者**（策划 / 美术等，不是开发者）的版本介绍，落盘为 `docs/release-notes/<version>.md`。

> 第一原则：**读者是使用者，不是提交者**。每条都要能回答「用户会看到什么不同」；答不上来的不写。

> **本 skill 只手动调用**：frontmatter `disable-model-invocation: true` + `agents/openai.yaml` 的 `allow_implicit_invocation: false`，不被模型隐式触发（发版说明必须由用户主动发起）。改动本文件时同步核对这两个开关，别打开隐式调用。

## 产出与边界

| | |
| --- | --- |
| 唯一落点 | 常规发布 `docs/release-notes/<version>.md`；一次性修复用轻量补丁记录 `docs/release-notes/patches/<version>.md`（见「补丁记录」；契约与 frontmatter 表见 `docs/release-notes/README.md`） |
| 归档只读 | `docs/release-notes/archive/*.md` 是历史版本的冻结聚合（按字节校验），不新增、不改写、不重排 |
| 初始状态 | `status: draft`；**用户明确确认后**才改 `reviewed`（发版预检只认 reviewed） |
| 不写 JSON | `apps/editor/resources/release-notes.json` 是编译产物，由 `pnpm release:notes` 从正式稿生成；手改必被漂移校验拦下 |
| 不发版 | 不改 `apps/editor/package.json` 版本、不打 tag、不推送、不碰上传与部署 |
| 不联网 | 不查上游、不更新 vendor fork、不 fetch；事实不确定就标注待核实，不猜 |

## 输入

先确认三件（缺哪件就问，或按下表推断并在交付时说明推断）：

| 输入 | 取值 | 推断规则 |
| --- | --- | --- |
| 待发布版本 | 如 `0.15.0` | `apps/editor/package.json` 已 bump 就用它，否则问 |
| 基准 tag | 上次发布的 tag，如 `v0.14.9` | `git tag --sort=-v:refname \| head -5` 中最大的已发布 tag |
| 目标 SHA | 写进 `sourceTo` | `git rev-parse HEAD` 的完整 SHA（不用会移动的分支名） |

## 1. 定范围

```bash
git log --oneline <base>..<sha>                                            # 通读提交清单
git log --no-merges --pretty=format:'%h %s' <base>..<sha> -- docs/user/    # 强线索：用户可见功能
git diff --stat <base>..<sha>                                              # 影响面
```

- 区间里有回退（revert）或 `<base>` 不是 `<sha>` 的祖先时，**以 `git diff <base>..<sha>` 的实际差异为准**：`git log` 会把被回退掉的提交也列出来。
- `--oneline` 只是线索，不是结论：`chore` 可能用户可见，`feat` 也可能纯内部。拿不准就读 `git show --stat <hash>` 或 diff。

## 2. 筛选

**强信号：改动 `docs/user/` 的提交 = 用户可见功能**（仓库硬约定：改用户可见功能必须同步用户文档）。但它**不是唯一过滤器**——修崩溃、改默认值、改快捷键这类提交可能没动文档。

- **保留**：用户能感知的行为变化——功能、界面、快捷键、提示文案、崩溃与卡顿、性能、安装/更新流程、扩展 API 变化、破坏性变化。
- **不机械排除 `chore` / `refactor` / 依赖指针**：构建产物路径变了、打包体积变了、启动方式变了都是用户可见的；反过来纯测试、纯内部服务的新增也不该写。
- **vendor gitlink 变化**（`vendor/claude-agent-acp`、`vendor/codex-acp`）要读两个 fork 的 old/new SHA 差异（`git -C vendor/<fork> log --oneline <old>..<new>`）：对象缺失就明确报告「无法读取，待核实」，**不联网更新、不凭版本号猜效果**。
- 同一功能的多个提交**合并成一条**（如侧边任务的三处修复）。

## 3. 交叉检查（防「写了但没发出去」）

- 功能在**最终发布树**（`<sha>`）里仍然存在——别把随后被删除或回退的东西写进说明。
- 提到的**菜单路径 / 命令面板命令 / 设置项 / 文档**真实可用：命令 id 与文案能在源码里搜到；`doc:<docId>` 对应的 `docs/user/zh-CN/<docId>.md` 确实存在（编译期会校验，但在落盘之后才报错）。
- 涉及新文档时给文档入口（`doc:...`），别留站外读者点不开的相对路径。

## 4. 表述

正文从 `##` 起（版本标题由应用/站点渲染），推荐结构：

```markdown
## 本次重点

一段话讲清这个版本最值得升级的地方，并给出操作入口（菜单路径 / 命令面板 / 文档链接）。

## <按场景或模块>

- 每条一行，说清用户看到的变化；翻译掉内部黑话（side task → 侧边任务、plan 卡片 → 计划卡片）。

## 问题修复

## 升级注意事项
```

- 量级参考：20–30 条以内；普通补丁可以很短；**没有用户可见变更也要显式写明**，不能以空正文代替确认。
- **破坏性变化单独成节**：默认值改了、旧行为不再支持、需要用户手动迁移的，写明影响与做法。
- **不写没有证据的性能 / 稳定性承诺**（「更快」「更稳」要么有场景/数字，要么不写）；不按条数凑文案。
- 不支持图片、HTML、脚注、引用式链接与相对路径；链接只允许 `doc:` / `command:` / `https://` / 页内锚点（白名单见 `apps/editor/src/shared/releaseNotes/linkPolicy.json`），其它协议编译失败。
- **裸域名 / 邮箱不会自动成链**（与应用内一致）：`example.com`、`CLAUDE.md`、`install.sh` 这类文本保持文字，要链接就写完整的 `https://…`。
- **页内锚点写标题 slug**（小写、空白转 `-`、去标点、CJK 原样）：`## 升级注意事项` → `#升级注意事项`；锚点必须命中本稿内的标题，否则编译失败。别把文件名/路径写成可点目标——版本介绍页只允许上面四种链接。

## 5. 落盘

```markdown
---
version: 0.15.0
date: 2026-10-09
title: 一句话标题
summary: 一句话摘要（下载页列表用）
status: draft
sourceFrom: v0.14.9
sourceTo: <40 位提交 SHA>
urgency: normal
---

## 本次重点
…
```

- 文件名 `<version>.md` 必须与 frontmatter `version` 一致（不带 `v` 前缀）。
- `date` 由作者明确填写（编译器**不会**用「今天」补）——填与用户确认的计划发布日期。
- `sourceTo` 用完整 SHA；它只是追溯线索，不声称覆盖完整。
- `urgency` 默认 `normal`，**不要顺手改成 `important`**：它是唯一会改变客户端行为的字段（`start`/`default` 模式下后台静默下载）。只有阻塞性 bug / 数据损坏 / 安全事故才够格，且必须单独向用户点明这个后果再改。

### 补丁记录（patch）

一次**修复发布**不要新写一篇独立文章——加一份轻量补丁记录 `docs/release-notes/patches/<version>.md`，编译期归并进它所属的主稿（主稿版本不变，同一篇不会被重复弹出，自动下载的紧急标记也不受影响）。

- frontmatter 只有 `version`、`notesVersion`、`date`、`status`、`sourceFrom`、`sourceTo`、`urgency`，**没有 `title` / `summary`**。
- `notesVersion` 指向**同一 major/minor 系列里、该补丁之前最新的 reviewed 常规主稿**；写错（跨系列 / 引用补丁 / 引用更旧的主稿 / 目标不存在）编译期直接失败。拿不准就列出该系列已有的根目录主稿取最新的一个。
- 正文只写简短修复条目（`## 问题修复` 起），落盘时 `status: draft`，**同样要走完「用户确认后改 `reviewed`」**：`reviewed` 补丁记录必须有非空正文与 `sourceFrom` / `sourceTo`。
- **归并不缩小发布范围**：trunk-based 的补丁版仍带出自上一个 tag 以来的全部提交——定范围、筛选、交叉检查的步骤一个都不能省，只是正文写法更短。步骤可压缩为：定范围只跑 `git log --oneline <上一个 tag>..HEAD` 逐条过一遍，表述只写「修好了什么、触发条件是什么」。

```markdown
---
version: 0.15.2
notesVersion: 0.15.1
date: 2026-10-13
status: draft
sourceFrom: v0.15.1
sourceTo: <40 位提交 SHA>
urgency: normal
---

## 问题修复

- 修好了什么，触发条件是什么。
```

## 6. 复核与确认

1. 交付时**逐条给出证据**（提交 / diff / 文档路径），并列出你拿不准或标了「待核实」的项。
2. 提醒 `sourceTo` 之后若又出现用户可见变化必须补审。
3. **用户明确确认后**才把 `status` 改成 `reviewed`——提交记录或字段本身不是可验证的「人类签名」。
4. 改回 `reviewed` 只改源文件：派生物由发版流程（或 `pnpm release:notes -- --version <version>`）重建，**不要手工同步 JSON**。`pnpm release:notes:check` 的上界是 `apps/editor/package.json` 的当前版本，所以版本号还没 bump 时它是绿的——这不代表派生物已包含新稿。

起草期间 `pnpm release:notes:check` 可随时跑（draft 不进产物），用来确认语法与链接没写错。
