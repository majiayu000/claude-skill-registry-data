---
name: codex-history-recovery
description: 当 Codex Desktop 在切换 ChatGPT 账号、API Key、自定义 provider、model_provider 或 model 后，本地历史记录消失、旧对话缺失、项目历史看起来移动、需要检查/同步/备份/恢复/删除归档历史元数据时使用。该 skill 只处理 ~/.codex 下的历史索引和 rollout 元数据，不暴露密钥，不重写对话正文。
---

# Codex History Recovery

用于诊断和修复 Codex Desktop 历史记录可见性问题，尤其是 provider / model 元数据不一致导致的“旧对话还在本地，但侧边栏看不见”。优先使用随 skill 携带的脚本，因为 Codex Desktop 会从 `rollout-*.jsonl` 重建 `state_5.sqlite`；只改 SQLite 不可靠。

运行命令时，把 `<skill-dir>` 替换成当前 skill 的安装目录。常见目录：

- `~/.agents/skills/codex-history-recovery`
- `~/.codex/skills/codex-history-recovery`
- 项目内 `.agents/skills/codex-history-recovery`

## 安全规则

- 不打印密钥、token、`.env` 值或对话正文。
- 除非用户明确要求迁移项目归属，否则不要修改 `cwd`。默认恢复必须保留每条对话原本所属项目目录。
- 删除归档历史时，绝不能删除 active history。只处理 SQLite 中 `threads.archived` 为 true 的记录、对应的归档 rollout JSONL，以及 `~/.codex/archived_sessions/` 下的孤儿文件。
- 归档删除是破坏性操作。必须先 dry-run，优先使用窄筛选，并依赖脚本自动备份后再 apply。
- 普通账号 / API / provider 切换恢复，只同步：
  - SQLite `threads.model_provider`
  - SQLite `threads.model`
  - JSONL `session_meta.payload.model_provider`
  - JSONL `turn_context.payload.model`
- 如果用户只要求改 provider 或只改 model，使用窄参数，不要同时同步两个字段：
  - `--provider-only --from-provider <old> --provider <new>`
  - `--model-only --from-model <old> --model <new>`
- 重写 rollout JSONL 必须保留文件 mtime；否则 Codex 可能把旧线程显示成最近更新。脚本在 sync 和 restore 中会保留 mtime。
- 写入前优先让用户完全退出 Codex Desktop。如果当前 agent 正在执行修复，无法关闭 Codex，则必须先说明 app 可能缓存或并发写入元数据，再使用 `--allow-running`。
- apply 前必须创建或依赖脚本自动备份。

## 标准恢复流程

1. 只读检查状态：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json status
   ```

2. 只用元数据计数解释可能原因：
   - provider / model mismatch：旧对话仍在本地，但被过滤掉。
   - cwd filtering：对话仍属于原项目目录，这是预期行为。
   - archived chats：只在归档视图可见。
   - missing rollout paths：本地历史文件可能已删除或移动。

3. dry-run 修复：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json sync
   ```

   如果只改 provider：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json --provider openai sync --provider-only --from-provider ccswitch
   ```

   如果只改 model：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json --model gpt-5.5 sync --model-only --from-model old-model
   ```

4. 用户确认且 Codex Desktop 已关闭后 apply：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json sync --apply
   ```

   如果无法关闭 Codex，因为当前 agent 正在执行修复，说明风险后使用：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json sync --apply --allow-running
   ```

   provider-only 且 Codex 仍打开时：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json --provider openai sync --provider-only --from-provider ccswitch --apply --allow-running
   ```

5. 重新运行 status，并提醒用户重启 Codex Desktop 让 UI 重新加载历史。如果之前修复后旧线程显示成“刚刚”或“2 分钟前”，使用时间修复流程。

## 时间修复流程

当恢复后的旧线程显示成“刚刚”或“2 min”时使用。它只修复 SQLite `threads.updated_at`、SQLite `threads.updated_at_ms` 和 rollout 文件 mtime，时间来源是每个 rollout JSONL 内已有的最新时间戳。

dry-run 所有已索引 rollout：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json repair-times
```

只 dry-run 某次元数据备份涉及的文件：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json repair-times --metadata-backup ~/.codex/history_sync_backups/rollout-provider-model-lines.pre-sync.<timestamp>.jsonl.gz
```

确认预览后 apply：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json repair-times --metadata-backup ~/.codex/history_sync_backups/rollout-provider-model-lines.pre-sync.<timestamp>.jsonl.gz --apply
```

如果 Codex 无法关闭，说明缓存和并发写入风险，再加 `--allow-running`。

## 归档删除流程

使用随附脚本，不要手工改 SQLite 或直接删除 rollout 文件，除非是在恢复一次失败的脚本操作。

1. 只读预览归档删除：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived
   ```

2. 优先缩小选择范围。支持这些筛选：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --cwd /path/to/project
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --older-than-days 30
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --before 2026-04-01
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --rollout-path /absolute/path/to/rollout.jsonl
   ```

3. 用元数据计数和路径解释 dry-run 结果：
   - `archived_threads`：SQLite 记录的归档线程总数。
   - `selected_archived_threads`：筛选命中的记录数。
   - `archived_session_files`：`~/.codex/archived_sessions/` 下的 JSONL 文件数。
   - `selected_orphan_archived_session_files`：未被 SQLite 引用但命中筛选的归档 JSONL 文件。
   - `missing_paths_count`：索引里存在但 rollout 文件已缺失的归档记录数。
   - `selected_cwd_counts_top`：删除集合对应的项目目录分布。

4. 用户同意且 Codex Desktop 已关闭后，用同样筛选 apply：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --older-than-days 30 --apply
   ```

   如果要明确删除所有归档记录，必须加 `--all`：

   ```bash
   python3 <skill-dir>/scripts/codex_history_repair.py --json delete-archived --all --apply
   ```

   如果当前 agent 正在执行删除，无法关闭 Codex，先说明 app 可能缓存或并发写入元数据，用户接受后才使用 `--allow-running`。

5. 告诉用户创建了哪些备份，并让用户重启 Codex Desktop。

## 备份与恢复

手动 SQLite 备份：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json backup
```

sync 命令会创建：

- `~/.codex/history_sync_backups/state_5.sqlite.pre-provider-model-sync.<timestamp>.bak`
- `~/.codex/history_sync_backups/rollout-provider-model-lines.pre-sync.<timestamp>.jsonl.gz`

时间修复会创建：

- `~/.codex/history_sync_backups/state_5.sqlite.pre-repair-times.<timestamp>.bak`

归档删除会创建：

- `~/.codex/history_sync_backups/state_5.sqlite.pre-archived-delete.<timestamp>.bak`
- `~/.codex/history_sync_backups/archived-rollouts.pre-delete.<timestamp>/`

恢复默认是 dry-run：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json restore --sqlite-backup <path> --metadata-backup <path>
```

确认备份路径后才 apply：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json restore --sqlite-backup <path> --metadata-backup <path> --apply
```

## 判断提示

- “历史消失”通常是侧边栏过滤了，本地 JSONL 文件可能仍在。
- `state_5.sqlite` 是索引 / 缓存。JSONL rollout 文件是很多线程元数据字段的持久来源。
- Codex 可能按当前项目 `cwd` 过滤。不要为了“修复”而把所有聊天强行改到当前目录。
- 如果用户希望所有旧聊天都从某一个项目可见，要提醒这会改变项目归属，并可能让其他项目侧边栏看起来变空。
- 归档删除会把归档 JSONL 移到带时间戳的备份目录，并删除选中的归档 SQLite 行；它也处理 `~/.codex/archived_sessions/` 里不再被 SQLite 引用的孤儿文件。它不会重写 active rollout 文件。
- 如果 provider / model sync 成功但 UI 没变化，让用户完全退出并重新打开 Codex Desktop。
