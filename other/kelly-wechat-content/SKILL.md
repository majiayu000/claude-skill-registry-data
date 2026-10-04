---
name: kelly-wechat-content
license: MIT
description: >-
  Build and operate a WeChat editorial content library in Busabase. Use when a
  team wants reusable source material, linked article drafts, an editorial
  kanban board, a publishing calendar, or a source-check and review queue.
  Keeps source documents and article scheduling in two linked Bases; does not
  publish to WeChat or approve an agent's own proposals.
metadata:
  category: marketing
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-wechat-content
    resources:
      - sources
      - articles
    risk: local-write
---

# 公众号内容工作台

把可复用的资料和每篇文章的写作、审核、发布排期分开维护。一个资料可以关联多篇文章，
一篇文章可以关联多个资料。这个包同时是操作 Skill、可安装模板和只读内容工作台。

## 开始工作

1. 先读 Busabase Skill，确认账号、空间和用户指定的本应用目录。
2. 只读取该目录内 `metadata.appId = kelly-wechat-content` 的资源：
   `resourceKey = sources` 是资料库，`resourceKey = articles` 是文章排期。
   不按相似表名接管工作区其他表，也不把演示资料当成用户事实。
3. 安装后的两张表、原生视图和素材 Drive 是数据来源。AirApp 只读这些数据；
   `?demo=1` 是明确选择的演示，连接失败不能自动退回演示。
4. 每张表一次最多读 50 条，保留游标；继续读取必须是另一次明确翻页。
   涉及全量整理时说明范围和批次，不能把全表扫描藏在刷新或搜索里。

## 两张业务表

### 资料库 `sources`

每行一份原始材料。`title` 是人能识别的标题；`kind` 是文章、报告、截图或笔记；
`topic` 是工作流、产品实践或内容增长。`summary` 保存摘要，`url` 保留原文地址，
`attachment` 保存用户后续添加的原始文件。`source-date` 是资料日期，`verified` 表示
来源已人工核对，`notes` 记录适用范围、需要补证据或版权限制。

`search-text` 是这张表里的文字摘录，不是附件的「可搜索文本」。如果上传 PDF 或截图，
想让文件正文可检索，另让 Agent 提取/OCR 并写入对应附件的可搜索文本，再做关键词验证。
仅填元数据或在聊天里给摘要，不能当作已完成正文检索准备。

### 文章排期 `articles`

每行一篇文章。`status` 是 `planned` 选题、`drafting` 写作中、`review` 待审核、
`scheduled` 待发布、`published` 已发布。`owner` 是负责人的名字，
`publish-date` 是计划发布日期，`sources` 是允许多条值的资料库关联。
`outline` 保存提纲，`draft` 保存 Markdown 草稿，`review-note` 保存具体审核意见。
`public-url` 只有真实发布后才填。日期排到了今天，不等于已经发布。

## 日常操作

- **整理资料**：先用标题、来源和主题检查重复，再新增材料；保留出处，未经核实的
  主张放在备注里，不替用户猜事实、统计结果或引用。
- **从资料出选题**：读相关资料，提出文章标题和提纲，为每篇文章关联所用资料；
  不重复复制整份资料。更新同一份资料时，引用仍指向同一记录。
- **写作与审核**：先读取稿件及其关联资料。把修改提交为有说明的 ChangeRequest，
  提出具体待核对项。需要审核时明确要求保留提案，不自行审批或合并。
- **排期**：先查看看板、日历和负责人，给出排期建议；用户确认后再更新日期或状态。
  不凭 `scheduled` 状态调用公众号发布接口。
- **回顾复用**：按资料关联统计哪些文章使用了它。这个是阅读分析，不擅自把文章
  修改成“已发布”或把未核对资料标为“来源已核对”。

两张表已经能承载多对多关系。只有用户明确需要记录每次引用的段落、页码、用途时，
才提出第三张「文章引用」表的结构与迁移方案；不要安装时先替用户扩表。

## 权限与写入

遵循 Busabase Skill 的 ChangeRequest 流程。需要人先检查的草稿/资料更新明确要求审核；
有写入权限时服务端可能立即合入，不能把“有历史”当作“等待审批”。
本 AirApp 不提供批准、退回或对外发布的伪操作，审核由 Busabase 原生变更请求界面进行。
对外发布、截图上传到论坛、订阅任务和第三方账号接入都需要各自明确授权。

## 本包提供什么

- 资料库：全部资料、待核对资料、资料画廊。
- 文章排期：文章列表、进度看板、发布日历、待审核。
- 编辑规范 Doc：引用规则、审核检查和示例工作流程。
- 示例素材 Drive：演示材料及真实运行截图；不会保存密钥或用户数据。
- 内容工作台 AirApp：总览、资料浏览、文章表格/看板/日历和待审核阅读。

查看 `references/scenario.md` 了解示例故事和每个视图的验收路径。

## 演示与安装

当前 `busabase-package@1` 只打包表格视图。因此安装时先建立原生表格和待审核筛选，
AirApp 的看板/日历可直接查看同一批记录。完成安装后，按下面的限定步骤补齐原生
资料画廊、状态看板和发布日历；不能把缺失的视图说成已安装。

```bash
node scripts/setup-views.mjs --base-url <已确认的Busabase地址> --folder <安装目录节点ID>
# 检查预览后，创建本模板声明的三个原生视图：
node scripts/setup-views.mjs --base-url <已确认的Busabase地址> --folder <安装目录节点ID> --yes
```

脚本只处理该目录内已归属本模板的两张表；重复运行不新增视图，不修改已有不同配置的
视图。写入由服务端权限决定立即合入或等待审核；脚本不会自行审核。
通过已连接 Agent 完成安装时，也可以让 Agent 读取 `references/native-views.json`，
按这三个声明提交 View 变更请求并读回核对。

演示记录是虚构编辑团队的数据，安装后可删除或替换。每张表少于 50 行。
演示与实际安装读取同一组记录，关联在安装时转换为目标空间的新记录 ID。
图片文件放在可安装的素材 Drive 中；`busabase-package@1` 不携带记录附件值，
因此附件字段初始可为空。Agent 可在用户授权后将 Drive 中所需文件附到记录。

```bash
npx busabase-cli@latest check ./skills/kelly-wechat-content
npx busabase-cli@latest install ./skills/kelly-wechat-content
```

同一空间已有本模板时，安装器会因全空间唯一的节点 slug 拒绝第二次安装；
明确需要并行保留两套场景时，为第二次安装指定新的 `--into-folder`，并加 `--rename`。
安装后从新目录节点 ID 再运行一次 `setup:views`，工作台会按所属目录读取各自的数据。

已安装实例的资源 ID 属于用户空间，不应写回本模板。源码和包文件保存在
`content/kelly-wechat-content-app/`，本地运行支持 `pnpm dev`；安装后在 Busabase 中运行同一版本。
