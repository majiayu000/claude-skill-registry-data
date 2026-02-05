---
name: git-commit-guide
description: Git 提交规范（Conventional Commits）
version: 1.0.0
category: collaboration
triggers:
  - git commit
  - 提交规范
  - conventional commits
  - commit message
  - git 规范
scriptPath: check-git.sh
scriptType: bash
autoExecute: true
scriptTimeout: 5
---

# Git 提交规范技能包

遵循 Conventional Commits 规范，提升团队协作质量和代码可维护性。

## 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 基本格式

```
<类型>[可选作用域]: <描述>
```

**示例**：
```
feat(api): 添加用户认证接口
fix(database): 修复连接池泄漏问题
docs(readme): 更新安装说明
```

## 提交类型（Type）

| 类型 | 说明 | 示例 |
|-----|------|------|
| **feat** | 新功能 | `feat(user): 添加用户注册功能` |
| **fix** | Bug 修复 | `fix(login): 修复密码验证错误` |
| **docs** | 文档变更 | `docs(api): 更新 API 文档` |
| **style** | 代码格式（不影响逻辑） | `style: 统一代码缩进` |
| **refactor** | 重构（不是新功能或修复） | `refactor(auth): 优化认证逻辑` |
| **perf** | 性能优化 | `perf(query): 优化数据库查询` |
| **test** | 测试相关 | `test(user): 添加用户模块单元测试` |
| **build** | 构建系统或外部依赖 | `build: 升级 Spring Boot 到 3.0` |
| **ci** | CI 配置文件和脚本 | `ci: 添加 GitHub Actions 配置` |
| **chore** | 其他不修改源代码的变更 | `chore: 更新 .gitignore` |
| **revert** | 回滚之前的提交 | `revert: 回滚 feat(api): xxx` |

## 作用域（Scope）

作用域表示影响的模块或组件，可选但建议添加。

**常见作用域示例**：
- `user` - 用户模块
- `auth` - 认证模块
- `api` - API 接口
- `database` - 数据库
- `config` - 配置
- `ui` - 用户界面

## 描述（Subject）

- 使用祈使句，现在时态
- 首字母小写
- 结尾不加句号
- 简洁明了，控制在 50 字符以内

**✅ 好的描述**：
```
feat(api): 添加用户注册接口
fix(login): 修复密码加密错误
```

**❌ 不好的描述**：
```
feat(api): 添加了用户注册接口。
fix: 修复bug
```

## 正文（Body）

详细说明变更的动机和与之前行为的对比。

**格式要求**：
- 使用祈使句，现在时态
- 应该说明"为什么"而不是"是什么"
- 每行不超过 72 字符

**示例**：
```
fix(auth): 修复 JWT Token 验证失败问题

之前使用的签名算法与解析算法不一致，导致 Token 验证总是失败。
现在统一使用 HS256 算法，并添加了算法一致性检查。
```

## 页脚（Footer）

用于记录不兼容变更和关闭的 Issue。

### Breaking Changes

```
BREAKING CHANGE: 删除了 v1 版本的 API

请迁移到 v2 版本，详见迁移指南。
```

### 关闭 Issue

```
Closes #123
Closes #456, #789
```

## 完整示例

### 示例 1：新功能

```
feat(user): 添加用户头像上传功能

支持上传 JPG、PNG 格式的图片，最大 5MB。
自动生成缩略图并存储到 OSS。

Closes #234
```

### 示例 2：Bug 修复

```
fix(order): 修复订单金额计算错误

在计算优惠券折扣时未考虑最小金额限制，
导致部分订单金额为负数。现已添加金额验证。

Closes #567
```

### 示例 3：破坏性变更

```
feat(api): 重构用户认证 API

BREAKING CHANGE: 移除了 /api/v1/auth 端点

请使用新的 /api/v2/auth 端点，返回格式已变更。
详见 API 文档：https://example.com/api-docs

Closes #890
```

## Git Hooks 配置

### Commit Message 验证

创建 `.git/hooks/commit-msg`：

```bash
#!/bin/bash
commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# 验证格式
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"; then
    echo "错误：提交信息不符合规范"
    echo "格式：<type>(<scope>): <subject>"
    echo "示例：feat(api): 添加用户注册接口"
    exit 1
fi
```

### 使用 Commitizen

```bash
# 安装
npm install -g commitizen cz-conventional-changelog

# 配置
echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc

# 使用
git cz
```

## 最佳实践

1. **每次提交只做一件事**：一个提交应该只解决一个问题或添加一个功能
2. **提交要完整**：确保提交后的代码可以正常运行
3. **频繁提交**：小步快跑，不要积累太多变更
4. **先拉后推**：提交前先 `git pull --rebase`
5. **避免混合变更**：不要在同一个提交中混合多种类型的变更

## 常见问题

### Q: 何时使用 chore 而不是 feat？

A: 如果变更不影响用户或功能（如更新依赖、修改配置），使用 `chore`。

### Q: 重构和性能优化如何区分？

A: 如果主要目的是提升性能，使用 `perf`；如果是改善代码结构，使用 `refactor`。

### Q: 一次提交修复了多个 Bug 怎么办？

A: 建议拆分成多个提交，每个提交只修复一个 Bug。

## 工具推荐

- **Commitizen**：交互式提交信息生成
- **commitlint**：提交信息格式校验
- **husky**：Git Hooks 管理
- **standard-version**：自动生成 CHANGELOG

## 参考资源

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md)
