---
name: bb-find-module-deps
description: "扫描 RTL 目录提取模块层次依赖，拓扑排序后写 file_list.f（叶模块在前，top 在最后），供 Yosys/Verilator 使用。触发场景：(1) bba-guru-rtl 生成 RTL 后生成 file_list；(2) 显式 /bb-find-module-deps。"
user-invocable: true

---

# bb-find-module-deps

## 职责

扫 `designs/<name>/rtl/*.sv`，构建 module → file 映射 + module instantiation 图，Kahn 拓扑排序，写 `file_list.f`。

- 调用者：`bba-guru-rtl`
- 下游：`bb-check-lint`、`bb-invoke-yosys`、`bb-invoke-verilator`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| rtl_dir | path | true | — | `designs/<name>/rtl/` |
| top_module | string | true | — | 顶层名 |
| design_name | string | true | — | — |
| include_dirs | list[path] | false | `[]` | `+incdir+` 列表 |
| defines | list[str] | false | `[]` | `+define+KEY=VAL` |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/file_list.f` |
| `script_path` | `designs/<name>/rtl/gen_filelist_<stamp>.py` |
| `module_count` | int |
| `top_module` | str |
| `order` | list[str]（拓扑序模块名） |
| `valid` | bool |
| `error` | string\|null |

## 4-Phase 执行

### Phase 1 — render_filelist_py

`scripts/render_filelist_py.py` 生成 Python：

```python
# 优先用 verible-verilog-syntax 解析（识别 interface/class/package 与 module，避免误判 — fix M-04）
# 失败时退到正则 fallback
try:
    import subprocess, json
    out = subprocess.check_output(["verible-verilog-syntax", "--export_json", f]).decode()
    ast = json.loads(out)
    # 遍历 ast 找 ModuleDeclaration nodes
except Exception:
    # fallback: 正则 `^\s*module\s+(\w+)` + 排除 interface/class/package 关键字
    pass

# 然后建 dep 图：parent_module → set(child_module)
# Kahn 拓扑（child 先 parent 后）；检测环
# 写 file_list.f：incdir / define / 拓扑序文件
```

### Phase 2 — run_filelist_gen

`scripts/run_filelist.py`：`timeout 180 uv run python <script_path> > <log> 2>&1`

### Phase 3 — parse_filelist

`scripts/parse_filelist.py`：

- 验证 `file_list.f` 存在
- 验证 `top_module` 对应文件是最后一个
- 计数 `module_count`
- log 含 `Cyclic dependency` → `error="cyclic: A->B->A"`

### Phase 4 — return

返回 JSON。`bba-guru-rtl` 直接把 `artifact_path` 传给下游。

## file_list.f 格式

```
+incdir+designs/<name>/rtl/include
+define+TARGET_ASAP7
designs/<name>/rtl/uart_fifo.sv
designs/<name>/rtl/uart_rx.sv
designs/<name>/rtl/uart_tx.sv
designs/<name>/rtl/uart_ctrl.sv
designs/<name>/rtl/uart_top.sv
```

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 进 `bb-check-lint` |
| cyclic | 开 `arch-needs-fix`（模块循环必须重设计） |
| 找不到 top_module | `error="top not found"`，bba-guru-rtl 修正 |

## 资源索引

- `scripts/render_filelist_py.py`、`scripts/run_filelist.py`、`scripts/parse_filelist.py`
- `lib/sv_module_regex.py` — module/instantiation 正则集
- `Gotcha/sv_pitfalls.md` — 接口/类等被误识别为 instantiation
