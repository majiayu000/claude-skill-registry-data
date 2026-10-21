---
name: memory-sync-abc
description: 多台电脑（家里 / 公司）各有一个 Obsidian 记忆库时，用一个私有 GitHub 仓库做「最新并集」中转，实现双向同步。覆盖白名单 gitignore 设计、代理环境下 git 协议不通时改用 GitHub API 推送、PAT 的安全取法、以及"判断线上状态先查远端不信本地"的原则。
version: 1.0.0
---

# 三库记忆同步（A / B / C）

## 何时用
- 用户在两台及以上电脑上维护同一个知识库 / 记忆库
- 需要跨设备接续同一条主线（求职、项目、写作）
- git 协议被代理 / GFW 挡住，推不上去

## 架构

| 标记 | 位置 | 角色 |
|---|---|---|
| **A** | 家里电脑 Obsidian vault | 主库之一 |
| **B** | GitHub **私有**仓库 | **A 与 C 的最新并集**，只增不删 |
| **C** | 公司电脑 vault | 主库之一 |

核心原则：**只增不删，更新而非覆盖**。两边各自往 B 推，需要时从 B 拉。

## 标准流程

### 1. 白名单式 .gitignore（必须）
私有仓库里只放「记忆类 md」，其他一律不进：

```gitignore
/*
!/.gitignore
!/.gitattributes
!/README.md
!/*.md
!/00_Inbox不知/
!/00_Inbox不知/**
!/01_Projects/
!/01_Projects/**
!/02_Areas/
/02_Areas/*                       # 先排除全部
!/02_Areas/<需要的子目录>/         # 再逐个放行
!/02_Areas/<需要的子目录>/**
```

**不放进仓库的**：`.obsidian/`、`.git/`、附件与大文件（视频 376MB / 归档 179MB / 资源 114MB）、凭据、公司资料。

### 2. 取 PAT（不落盘）
```bash
printf "protocol=https\nhost=github.com\n\n" | git credential fill
```
从输出里取 `password=` 的值，**用完即删**，绝不写进脚本或仓库。

### 3. git 协议不通时改用 GitHub API
现象：私仓 `git push` 必挂（`CONNECT tunnel failed, response 502`），公仓却正常。
解法：用 Git Data API 走 HTTP 单次提交——建 blob → 建 tree → 建 commit → 更新 ref：

```
POST /repos/{repo}/git/blobs          {"content": base64, "encoding": "base64"}
POST /repos/{repo}/git/trees          {"base_tree": <head tree>, "tree": [...]}
POST /repos/{repo}/git/commits        {"message": ..., "tree": ..., "parents": [head]}
PATCH /repos/{repo}/git/refs/heads/main  {"sha": <new commit>}
```

⚠️ >1MB 的文件 `contents` API 不返回 base64（`encoding: "none"`），
要改用 `GET /repos/{repo}/git/blobs/{sha}` 取。

### 4. 拉取（B → 本地）
```bash
# 列远端全部文件
GET /repos/{repo}/git/trees/main?recursive=1
# 取单个文件
GET /repos/{repo}/contents/{path}?ref=main
```

## 铁律：判断"最新状态"先查远端，别只看本地
- MCP 的 `push_files` 之类**不产生本地 commit** → 本地 `git log` 会骗人
- 两个设备各自都可能刚推过内容 → 本地不是权威
- 需要判断现状时，先查 B 库的最近 commit 与文件清单

⚠️ 入口文档可能过期：曾出现「CURRENT.md 停在 10-07」但真正的现状在另一侧的会话笔记里。
**别只看那个写着 CURRENT 的文件**，先看最近 commit 改了什么。

## Example

> 用户：「我周末在家聊了很多，帮我把家里的记忆读回来。」

1. 查 B 库最近 commit（按时间倒序）→ 定位到对方设备推送的时间点
2. 拉那一批新增/修改的 md 到本地缓存目录
3. 读完后**归并**到本地日志：新事实标【事实】+证据来源，冲突项标 ⚠️ 并提问，**不并行保留两个值**
4. 若发现对方记忆里某条与实查不符（如"13 个 skills 实际 12 个"），**重新实查再更正**，不要沿用

## 坑位清单
- `git credential fill` 的凭据可能被系统清理，需要时重新取
- 私有仓库走代理必挂，公仓正常 —— 不要误判成"仓库坏了"
- 两侧都在用同名工具时，笔记里要标清**生成于哪台机器**（如 `C:\Users\19686` vs `C:\Users\EDY`），否则事后分不清来源
- 大附件绝不入库，否则 tarball 拉取极慢

## 隐私与边界
只同步**个人记忆类 md**。密钥、公司资料、聊天截图原文、他人信息一律不进仓库。
PAT 用完即删，不写进任何脚本或提交。
