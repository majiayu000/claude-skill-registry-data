---
name: nsforge-code-generation
description: 程式碼/報告生成。觸發詞：生成程式碼, Python 函數, LaTeX, 報告, export。
---

# 程式碼生成 Skill

> **⚠️ 生成後必須向用戶展示結果！**
> - 生成的 Python 函數要用程式碼區塊展示
> - 生成的 LaTeX 要渲染給用戶看
> - 生成 Markdown 報告後顯示完整內容

## 工具速查

| 輸出類型 | 工具 |
|----------|------|
| Python 函數 | `generate_python_function(name, description, parameters, steps, return_vars)` |
| LaTeX 公式 | `generate_latex_derivation(steps, title?, include_preamble?)` |
| Markdown 報告 | `generate_derivation_report(title, given, steps, result, assumptions?, limitations?)` |
| SymPy 腳本 | `generate_sympy_script(expressions, operations)` |

## 調用範例

### Python 函數

```python
generate_python_function(
    name="arrhenius_rate",
    description="Calculate rate using Arrhenius equation",
    parameters=[
        {"name": "k_ref", "type": "float", "description": "Reference rate (1/s)"},
        {"name": "E_a", "type": "float", "description": "Activation energy (J/mol)"},
        {"name": "T", "type": "float", "description": "Temperature (K)"}
    ],
    steps=[
        {"description": "Arrhenius equation", "expression": "k_ref * exp(E_a/R * (1/T_ref - 1/T))", "result_var": "k"}
    ],
    return_vars=["k"]
)
```

### LaTeX

```python
generate_latex_derivation(
    steps=[
        {"description": "Base model", "expression": "C = C_0 e^{-kt}"},
        {"description": "Substitute k", "expression": "C = C_0 e^{-k_{ref} e^{...} t}"}
    ],
    title="Temperature-Corrected Elimination"
)
```

### Markdown 報告

```python
generate_derivation_report(
    title="Temperature-Corrected Elimination",
    given=["One-compartment model: $C = C_0 e^{-kt}$"],
    steps=[{"description": "...", "expression": "..."}],
    result="$C(t,T) = ...$",
    assumptions=["First-order elimination"],
    limitations=["Valid for 32-42°C"]
)
```

### SymPy 腳本

```python
generate_sympy_script(
    expressions=[
        {"name": "C_base", "expr": "C_0 * exp(-k*t)", "description": "One-compartment"}
    ],
    operations=[
        {"op": "substitute", "input": "C_base", "var": "k", "replacement": "k_arrhenius"}
    ]
)
```

## 先計算再生成

複雜情況先用 SymPy-MCP 計算（如 `dsolve_ode`），再用 NSForge 生成程式碼。
