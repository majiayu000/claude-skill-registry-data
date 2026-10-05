---
name: find-session
description: "按对话标题或正文关键词快速定位 DSH 历史会话并读取内容/统计；用于“根据对话名跟踪对话”“查找之前的会话”“查看某会话 token 消耗”等请求。"
---

# 快速定位与跟踪 DSH 会话

用于用户要求"按对话名/标题找会话""跟踪某个对话""查看某次会话内容或 token 消耗"时。统一入口是本 Skill 包内脚本 `scripts/find_session.py`（相对本 Skill 目录），不临场另写遍历逻辑。

> 路径提示：Skill 包在 `~/.dsh/skills/find-session/`（仓库源在 `skills/find-session/`）。以下命令均假设当前目录为本 Skill 目录，或把 `scripts/find_session.py` 换成绝对路径 `~/.dsh/skills/find-session/scripts/find_session.py`。

## 触发边界

- 适用：按标题关键词搜索会话、按正文关键词搜索会话、读取某会话消息内容、查看会话 token/时间统计、按项目或时间范围过滤。
- 不适用：修改/删除会话、DSH 内部状态变更、跨设备同步。这些不得套用本 Skill。

## 数据源与固定事实

- 索引：`~/.dsh/storages/session_projcache.json`（title/cwd/createdAt/sessionStats/tokenUsage）。
- 内容：`~/.dsh/sessions/<项目>/<session>/session.jsonl.zstd`（多帧 zstd，必须流式解压，单帧 decompress 只解第一帧）。
- 正文搜索默认只扫最近 30 个会话（全量解压 200+ 会话慢），需要全量时加 `--full`。

## 固定执行

1. 标题搜索（快，走索引）：

   ```bash
   python scripts/find_session.py <关键词>                # 列出匹配会话（按时间倒序）
   python scripts/find_session.py <关键词> --content      # 搜索后直接读最新匹配会话内容
   ```

2. 正文全文搜索（慢，需解压）：

   ```bash
   python scripts/find_session.py --grep <关键词>          # 默认最近 30 个会话
   python scripts/find_session.py --grep <关键词> --full   # 全量扫描
   ```

3. 按会话 id 操作：

   ```bash
   python scripts/find_session.py --id <session-id>        # 读取消息内容
   python scripts/find_session.py --id <id> --stats        # token/时间统计
   ```

4. 过滤与排序（标题/正文搜索均生效）：

   ```bash
   python scripts/find_session.py <关键词> --project 桌面    # 按项目路径过滤
   python scripts/find_session.py <关键词> --since 2026-08-01 --until 2026-08-31
   python scripts/find_session.py <关键词> --sort tokens     # time|tokens|turns
   python scripts/find_session.py <关键词> --max 5           # 结果条数上限
   ```

## 输出与失败报告

- 输出完整 token 消耗（未缓存输入 + 缓存读 + 输出 + 缓存写），来自 `tokenUsage.totals`，不用单一 decodeTokens。
- 搜索无匹配时报告"无匹配会话"，不以空结果冒充成功；会话文件缺失时给出明确提示。
- 只读操作，不改动任何会话数据。

## 验证

- 每次使用后核对：搜索关键词是否命中预期会话、token 统计是否与 `~/.dsh/storages/session_projcache.json` 中 `tokenUsage.totals` 一致。
- 改动脚本后回归：至少跑一次标题搜索、一次 `--grep` 正文搜索、一次 `--id --stats`，确认三项路径输出正常。

脚本是唯一入口：

- [find_session.py](scripts/find_session.py)（skill 包内自带，随 Skill 同步）
