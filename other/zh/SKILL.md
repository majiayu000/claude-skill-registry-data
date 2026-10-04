---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 问题解决与分析：针对复杂问题的结构化思维过程。分治法（Divide & Conquer）、根本原因分析（Root Cause Analysis）、SWOT、帕累托法则（Pareto）以及决策启发式方法。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="think banner">

> **中文** — `think` 官方中文版本。


# Think — 问题解决与分析

> 针对复杂问题的结构化思维过程

---

## 问题解决途径

### 1. Divide & Conquer（分治法）

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis（根本原因分析）

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation（放宽约束）

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search（类比搜索）

```
New problem -> Similar known problem -> Adapt solution
```

---

## 分析方法

| 方法 | 应用 |
|------|------|
| **SWOT** | 优势 / 劣势 / 机会 / 威胁 |
| **利弊分析 (Pro/Con)** | 决策制定 |
| **Pareto** | 80/20 优先级排序 |
| **Fishbone** | 根本原因分析（石川图） |

---

## 决策启发式方法

### 不确定性下

```
1. 最坏的情况是什么？
2. 是否可逆？
3. 不采取行动的代价是什么？
```

### 复杂性下

```
1. 最简单的第一步是什么？
2. 专家会怎么做？
3. 80% 的解决方案会是什么？
```

---

## 变更日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*
