---
name: baton-debt
description: 扫描并登记技术债标记 BATON-DEBT，输出结构化清单。只读；持久化进入 Baton 现有任务/记忆体系，不另建平行真相。触发：用户要求技术债盘点、债单扫描、BATON-DEBT 查询时使用。
---

# baton-debt（技术债扫描，只读）

## 标记格式（代码内写入时的强制格式）

```text
BATON-DEBT: task=<id>; ceiling=<上限>; revisit_when=<可测触发器>; upgrade=<升级路径>
```

- `task`：关联任务 ID（无则 `none`）。
- `ceiling`：已知上限（如「目录 ≤ 500 文件」「单文件 ≤ 3MB」）。
- `revisit_when`：**可测触发器**（如「E2E 用例超过 60」「文件超过 3MB」）；禁止「以后有空」「未来可能」。
- `upgrade`：升级路径（改什么、为什么现在不做）。

## 扫描与输出

1. 搜索代码库全部 `BATON-DEBT:` 标记。
2. 每条提取 task/ceiling/revisit_when/upgrade/位置，输出：

```text
文件:行号 | task | ceiling | revisit_when | upgrade | 状态(no-trigger=缺可测触发器)
```

3. 无触发器的标记标 `no-trigger` 并要求补正。
4. `git blame` 只作线索，不自动认定责任人。

## 持久化（需要落库时）

- 进入 Baton 现有 `tasks/task_todo.md`（新增债务条目）或追加到 `knowledge/pit_experience.md` 并同步索引；
- 自动维护 `state/archive_index.json` 索引——**不另建第二套项目真相**。

## 边界

- 只读扫描；修改代码必须先过任务 Contract 与用户确认。
- 债务标记是显式声明，不是放纵理由：标记的 ceiling 到达 revisit_when 时按 upgrade 路径执行。
