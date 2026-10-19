---
name: gatekeeper-constraints
description: OPA Gatekeeper ConstraintTemplate 探索文档编写规范。用于在 constraint-explorers/ 目录下创建结构化的 Constraint 深度探索文档，格式参考 k8srequiredlabels.md。当需要深入理解某个 Gatekeeper ConstraintTemplate 的 Rego 逻辑、参数配置、实际用例时使用。
category: gcp
---

# Gatekeeper Constraints — 探索文档编写规范

## 何时使用

用户要求"探索某个 Gatekeeper Constraint"、"生成更多类似 k8srequiredlabels.md 的例子"、或"深入了解某个 Constraint 的用法"时，在此目录下创建探索文档。

## 目录结构

```
OPA-Gatekeeper/constraint-explorers/
├── README.md                      ← 索引 + 分类导航（持续更新）
├── k8srequiredlabels.md           ← 原始参考格式
├── block-loadbalancer-services.md
├── block-nodeport-services.md
├── containerlimits.md
├── allowed-repos.md
├── disallowed-repos.md
├── https-only.md
├── storageclass.md
├── replica-limits.md
├── required-probes.md
├── psp-pod-security.md            ← PSP 全集（单文件）
└── immutable-fields.md            ← 自定义模板（官方库不存在）
```

## 文档标准格式

每个探索文档必须包含以下章节：

### 1. 概述（必须）

```markdown
## 概述
## 核心概念
### 这个 Constraint 做什么
### 模板信息
| 属性 | 值 |
|------|-----|
| **ConstraintTemplate Name** | `k8sxxx` |
| **Kind** | `K8sXxx` |
| **版本** | x.x.x |
| **来源** | [gatekeeper-library](URL) |
### 参数说明
```

### 2. Rego 逻辑解析（必须）

逐行解读策略代码，解释 `input.review`、`violation`、参数传递等核心概念。

### 3. 完整 Constraint YAML（必须）

提供 2-3 个实际可用的 YAML 示例：
- **基础/最简版本**：直接可用
- **生产版本**：含 excludedNamespaces、exemptImages 等
- **差异化版本**：不同参数组合

### 4. 应用命令（必须）

```bash
kubectl apply -f - <<'EOF'
# YAML here
EOF

kubectl get <Kind>
kubectl describe <Kind> <name>
```

### 5. 测试：触发违规（必须）

提供具体的 YAML 或 kubectl 命令来验证 Constraint 生效。

### 6. 实际应用场景（必须）

至少 2-3 个真实场景，说明为什么需要这个 Constraint。

### 7. 常见问题（强烈推荐）

FAQ，覆盖常见误解、边界情况、多环境差异。

### 8. 与其他 Constraint 的配合（推荐）

展示如何与其他 Constraint 协同工作。

### 9. 快速命令参考（必须）

```bash
# 应用 / 查看 / 更新 / 删除
```

### 10. 源文件路径（必须）

指向 gatekeeper-library 的原始 template.yaml 和 samples 目录。

## 模板获取流程

### Step 1: 发现模板

通过 GitHub API 列出 gatekeeper-library 的模板：

```bash
# 列出 general 目录
curl -s "https://api.github.com/repos/open-policy-agent/gatekeeper-library/contents/library/general" \
  | python3 -c "import sys,json; [print(d['name']) for d in json.load(sys.stdin)]"

# 列出 PSP 目录
curl -s "https://api.github.com/repos/open-policy-agent/gatekeeper-library/contents/library/pod-security-policy" \
  | python3 -c "import sys,json; [print(d['name']) for d in json.load(sys.stdin)]"
```

### Step 2: 获取模板内容

```bash
# 获取 template.yaml
curl -s --max-time 20 \
  "https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/<template-name>/template.yaml"
```

### Step 3: 获取 samples

```bash
# 获取 samples 目录结构
curl -s "https://api.github.com/repos/open-policy-agent/gatekeeper-library/contents/library/general/<template-name>/samples"

# 获取单个 sample 文件
curl -s --max-time 20 \
  "https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/<template-name>/samples/<sample-name>/constraint.yaml"
```

### Step 4: 参考已有探索文档

`k8srequiredlabels.md` 是标准格式参考。`block-loadbalancer-services.md` 是最简单的 deny 型模板参考。`containerlimits.md` 是带参数约束的参考。

## 特殊情况处理

### 官方库不存在的模板（如 immutablefields）

1. 在文档标题注明"（自定义模板）"
2. 提供完整的 ConstraintTemplate YAML 代码
3. 说明为什么官方库没有（gatekeeper 认为不属于策略范畴）
4. 提供实用的预制 Constraint 示例

### PSP 模板群

PSP 有 20+ 个模板，合并为**单个文档**（`psp-pod-security.md`），按子模板分节说明，而非每个模板一个文件。

### 命名规则

- 文件名使用 kebab-case：`block-loadbalancer-services.md`
- Rego 包名保持原始：`k8sblockloadbalancer`
- Kind 名称保持原始：`K8sBlockLoadBalancer`

## Git 提交流程

完成一批探索文档后：

```bash
cd /Users/lex/git/gcp
git add OPA-Gatekeeper/constraint-explorers/
git commit -m "docs(gatekeeper): add constraint-explorers — <n> deep-dive guides"
git push
```

**必须推送**：用户习惯是完成即推送，不留在本地。

## 参考来源

- 官方库: https://github.com/open-policy-agent/gatekeeper-library/tree/master/library
- PSP 库: `library/pod-security-policy/` (20+ 模板)
- General 库: `library/general/` (20+ 模板)

## 相关 Skill

- `architectrue`: GKE/GCP 架构总览，包含 Gatekeeper 选型指南
