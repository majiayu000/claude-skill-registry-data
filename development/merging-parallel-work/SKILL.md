---
name: merging-parallel-work
description: 测试中, 用户明确指定执行 merging-parallel-work 时候才执行, 其余情况一律不执行
---

# 并行工作合并

## 触发条件

当 implementing-from-task 判断需要并行执行时自动触发：
- 任务完全独立（无依赖）
- 任务数 >= 2

## 并行执行流程

### 1. 创建 Worktree

为每个独立模块创建 worktree：

```bash
# 主分支
git checkout -b feat-PROJ-12345-main

# 为每个模块创建 worktree
git worktree add ../worktree-module-a -b feat-PROJ-12345-module-a
git worktree add ../worktree-module-b -b feat-PROJ-12345-module-b
```

### 2. 分配任务

每个 worktree 对应一组独立任务：
- worktree-module-a: 任务 T1, T2
- worktree-module-b: 任务 T3, T4

### 3. 并行实现

各 agent 在各自 worktree 中独立工作：
- 实现代码
- 提交变更
- 推送分支

### 4. 合并分支

按顺序合并各模块分支到主分支：

```bash
# 切换到主分支
git checkout feat-PROJ-12345-main

# 合并第一个模块
git merge feat-PROJ-12345-module-a

# 合并第二个模块
git merge feat-PROJ-12345-module-b
```

### 5. 冲突解决

遇到冲突时的 AI 解决策略：

1. **分析冲突类型**
   - Import 语句：合并去重
   - 函数/方法：保留两者（如果不重名）
   - 配置文件：智能合并

2. **尝试自动解决**
   ```bash
   # 查看冲突文件
   git diff --name-only --diff-filter=U

   # 分析冲突内容
   git diff
   ```

3. **解决后验证**
   - 运行 lint 检查
   - 运行测试
   - 确认编译通过

4. **无法自动解决时**
   - 标记 `<<<NEEDS_HUMAN_REVIEW>>>`
   - 记录冲突详情
   - 继续其他任务

### 6. 清理 Worktree

合并完成后清理：

```bash
# 删除 worktree
git worktree remove ../worktree-module-a
git worktree remove ../worktree-module-b

# 删除临时分支
git branch -d feat-PROJ-12345-module-a
git branch -d feat-PROJ-12345-module-b
```

### 7. 创建 MR

调用 /commit-push-pr 创建统一的 Merge Request。

## 冲突解决报告

合并完成后输出报告：

```markdown
## 合并报告

### 合并的分支
- feat-PROJ-12345-module-a ✅
- feat-PROJ-12345-module-b ✅

### 冲突解决
| 文件 | 冲突类型 | 解决方式 |
|------|---------|---------|
| go.mod | 依赖版本 | 使用较新版本 |
| api/handler.go | Import | 合并去重 |

### 需要人工检查
- 无 / 或列出需要检查的文件

### 验证结果
- Lint: ✅
- Test: ✅
- Build: ✅
```

## 回退策略

如果合并失败且无法自动解决：

1. 保留各模块分支
2. 输出详细的冲突信息
3. 建议人工合并步骤
4. 不删除 worktree（供人工处理）
