---
name: lagrangian-core
description: >
  Augmented Lagrangian method for constrained optimization. Handles convex QP,
  smooth NLP, and basic non-convex problems. Trigger on: constrained optimization,
  KKT conditions, Lagrange multipliers, penalty methods, equality/inequality constraints.
license: MIT
metadata:
  version: "0.1.0"
  stage: prototype
---

# Lagrangian Core Skill — v0.1.0

## 能力边界
支持: 凸QP | 光滑NLP | 基础非凸NLP
不支持: 分布式 | Safe RL | 多目标 | 贝叶斯混合

## 核心方法: 增广拉格朗日法 (ALM)
目标: min f(x) s.t. h(x)=0, g(x)≤0

L_ρ = f(x) + Σλ·h(x) + Σμ·g(x) + ρ/2·||h||²

求解步骤:
1. 初始化 x₀, λ₀, μ₀, ρ₀=1.0
2. 内层: min_x L_ρ(x, λ, μ) → x*
3. 更新乘子: λ ← λ + ρ·h(x*), μ ← max(0, μ + ρ·g(x*))
4. 更新惩罚: ρ ← 1.5ρ if ||h||>tol
5. 收敛判断: ||h(x*)||<1e-6 且 ||∇L||<1e-6

## KKT条件验证
∇f + Σλ∇h + Σμ∇g = 0
h(x*) = 0, g(x*) ≤ 0
μ ≥ 0, μ·g(x*) = 0

## 失败处理
输出: 错误类型 + 一行说明

## 输出格式
最优解 x* → 目标值 f(x*) → KKT残差 → 约束状态
