---
name: nsforge-quick-calculate
description: 快速計算（無需會話）。觸發詞：計算, 簡化, 求解, 微分, 積分, 極限, 級數, 不等式, 機率。
---

# 快速計算 Skill

> **⚠️ 每次計算後必須向用戶展示結果！**
> - 在推導中使用 `derivation_show()` 顯示當前狀態
> - 單獨計算用 `print_latex_expression()` (SymPy-MCP)

## 工具分工

| 我想要... | MCP | 工具 |
|-----------|-----|------|
| 簡化/展開/分解 | SymPy | `simplify_expression`, `expand_expression`, `factor_expression` |
| **展開表達式** | **NSForge** | `expand_expression(expr, deep?, modulus?)` 🆕 |
| **因式分解** | **NSForge** | `factor_expression(expr, modulus?)` 🆕 |
| **收集同類項** | **NSForge** | `collect_expression(expr, symbols)` 🆕 |
| **三角化簡** | **NSForge** | `trigsimp_expression(expr, method?)` 🆕 |
| **冪次化簡** | **NSForge** | `powsimp_expression(expr, deep?)` 🆕 |
| **根式化簡** | **NSForge** | `radsimp_expression(expr)` 🆕 |
| **組合函數化簡** | **NSForge** | `combsimp_expression(expr)` 🆕 |
| **部分分式** | **NSForge** | `apart_expression(expr, var)` 🆕🔥🔥 |
| **約分** | **NSForge** | `cancel_expression(expr)` 🆕 |
| **合併分式** | **NSForge** | `together_expression(expr, deep?)` 🆕 |
| 微分/積分 | SymPy | `differentiate_expression`, `integrate_expression` |
| 解方程 | SymPy | `solve_algebraically`, `solve_linear_system` |
| ODE/PDE | SymPy | `dsolve_ode`, `pdsolve_pde` |
| 矩陣 | SymPy | `matrix_*` 系列 |
| 單位換算 | SymPy | `convert_to_units` |
| **Laplace 變換** | **NSForge** | `laplace_transform_expression(expr, t, s)` 🆕🔥🔥 |
| **反 Laplace** | **NSForge** | `inverse_laplace_transform_expression(expr, s, t)` 🆕🔥🔥 |
| **Fourier 變換** | **NSForge** | `fourier_transform_expression(expr, x, k)` 🆕🔥 |
| **反 Fourier** | **NSForge** | `inverse_fourier_transform_expression(expr, k, x)` 🆕🔥 |
| **極限** | **NSForge** | `calculate_limit(expr, var, point, direction?)` |
| **級數展開** | **NSForge** | `calculate_series(expr, var, point?, order?)` |
| **求和 Σ** | **NSForge** | `calculate_summation(expr, index, lower, upper)` |
| **不等式** | **NSForge** | `solve_inequality(ineq, var, domain?)` |
| **不等式系統** | **NSForge** | `solve_inequality_system(ineqs, var)` |
| **定義分佈** | **NSForge** | `define_distribution(type, params, name?)` |
| **統計量** | **NSForge** | `distribution_stats(type, params, stats?)` |
| **機率計算** | **NSForge** | `distribution_probability(type, params, condition)` |
| **假設查詢** | **NSForge** | `query_assumptions(expr, query, assumptions?)` |
| **假設簡化** | **NSForge** | `refine_expression(expr, assumptions)` |
| 數值計算 | NSForge | `evaluate_numeric(expr, values, precision?)` |
| 等價檢查 | NSForge | `symbolic_equal(expr1, expr2)` |

## SymPy-MCP 調用模式

```python
intro("x", ["real"], [])                    # 定義變數
expr = introduce_expression("x**2 - 1")     # 建立表達式
result = simplify_expression(expr)          # 計算
print_latex_expression(result)              # ⚠️ 必須！永遠不要跳過！
```

> **❌ 禁止**：計算後不顯示結果就繼續下一步
> **✅ 正確**：每次計算後都用 `print_latex_expression` 或 `derivation_show()` 展示

## NSForge 獨特工具範例

```python
# ═══════════════════════════════════════════════════════════════════
# Phase 1: 進階代數簡化 (10 工具) 🆕
# ═══════════════════════════════════════════════════════════════════

# P0: 基礎代數
expand_expression("(x+1)**2")                           # → x**2 + 2*x + 1
factor_expression("x**2 - 1")                           # → (x-1)*(x+1)
collect_expression("x*y + x**2*y + y", "y")             # → y*(x**2 + x + 1)
trigsimp_expression("sin(x)**2 + cos(x)**2")            # → 1
powsimp_expression("x**2 * x**3")                       # → x**5
radsimp_expression("1/(sqrt(3) + sqrt(2))")             # → -sqrt(2) + sqrt(3)
combsimp_expression("factorial(n)/factorial(n-2)")      # → n*(n-1)

# P1: 有理函數處理 🔥🔥
apart_expression("1/((s+1)*(s+2))", "s")               # → 1/(s+1) - 1/(s+2)
cancel_expression("(x**2-1)/(x-1)")                     # → x + 1
together_expression("1/x + 1/y")                        # → (x + y)/(x*y)

# ═══════════════════════════════════════════════════════════════════
# Phase 2: 積分變換 (4 工具) 🆕
# ═══════════════════════════════════════════════════════════════════

# Laplace 變換 🔥🔥
laplace_transform_expression("exp(-k*t)", "t", "s")    # → 1/(s+k)
laplace_transform_expression("Heaviside(t)", "t", "s") # → 1/s

# 反 Laplace 變換（與 apart 搭配）🔥🔥
inverse_laplace_transform_expression("1/(s+k)", "s", "t")  # → exp(-k*t)

# Fourier 變換 🔥
fourier_transform_expression("exp(-x**2)", "x", "k")   # → sqrt(pi)*exp(-pi**2*k**2)

# 反 Fourier 變換 🔥
inverse_fourier_transform_expression("1/(1+k**2)", "k", "x")  # → pi*exp(-abs(x))

# ═══════════════════════════════════════════════════════════════════
# NSForge 原有工具
# ═══════════════════════════════════════════════════════════════════

# 極限
calculate_limit("sin(x)/x", "x", "0")                    # → 1
calculate_limit("1/x", "x", "0", direction="+")          # → oo

# 級數
calculate_series("exp(x)", "x", "0", order=4)            # Taylor 展開

# 求和
calculate_summation("k", "k", "1", "n")                  # → n*(n+1)/2

# 不等式
solve_inequality("x**2 - 4 < 0", "x")                    # → (-2, 2)
solve_inequality_system(["x > 0", "x < 5"], "x")         # → (0, 5)

# 機率
distribution_stats("normal", {"mean": "mu", "std": "sigma"})
distribution_probability("exponential", {"rate": "1"}, "X < 2")

# 假設
query_assumptions("x**2", "positive", {"x": ["real", "nonzero"]})  # → True
refine_expression("sqrt(x**2)", {"x": ["positive"]})               # → x
```

## 🔥🔥 完整 Laplace 工作流（多隔室 PK）

```python
# 1. 部分分式分解
apart_expression("Dose/(V1*(s + lambda1)*(s + lambda2))", "s")
→ {"result": "A/(s + lambda1) + B/(s + lambda2)"}

# 2. 反 Laplace 變換
inverse_laplace_transform_expression("A/(s + lambda1) + B/(s + lambda2)", "s", "t")
→ {"result": "A*exp(-lambda1*t) + B*exp(-lambda2*t)"}

# 結果：C(t) = A·e^(-λ1·t) + B·e^(-λ2·t)
```

## 需要推導追蹤？

切換到 `nsforge-derivation-workflow` skill。
