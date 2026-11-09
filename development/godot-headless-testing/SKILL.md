---
name: godot-headless-testing
description: 在终端里验证 Godot 4 改动时用，看不到编辑器也能自己跑通。修完脚本报错要确认整个项目没有脚本错误和 GDScript 警告，改完 GDScript 场景 C# 想自己验证，写冒烟测试 自动化测试，配 CI。--headless --import --check-only --script、退出码、从输出判 SCRIPT ERROR、模拟输入、截图、GUT gdUnit4。headless smoke test.
---

# Godot 无头测试与命令行验证

用 Godot 命令行验证改动：参数、失败判定、冒烟脚本、输入模拟、截图、CI。示例在 4.7.2 编辑器版实测，`$GODOT_BIN` 指可执行文件。

## 范围

| 不含 | 去哪 |
|---|---|
| 单个节点或 API 的用法 | 对应领域 skill |
| GDScript 警告的含义与修法 | godot-gdscript |
| C# 构建、源码生成器、命名 | godot-csharp |
| 编辑器插件、`EditorScript` | godot-editor-tooling |
| 性能测量与 Profiler | godot-performance |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 查单个脚本语法 | `--headless --check-only -s x.gd`，退出码 0 或 1 | 正则或自写解析器 |
| 新增 class_name 或资源后 | `--headless --import` | 手改 `.godot/global_script_class_cache.cfg` |
| 跑主场景 N 帧后退出 | `--quit-after N`，配 `--fixed-fps 60` 可复现 | `sleep` 加 kill |
| 加载场景、断言、按结果退出 | SceneTree 脚本加 `quit(code)` | 自己拼 main 循环 |
| 引擎报错也算失败 | `OS.add_logger` 的 Logger 子类计数 4.5+ | 只靠 grep 或只靠退出码 |
| 传参给脚本 | `--` 之后的参数，`OS.get_cmdline_user_args()` 读 | 环境变量或写临时文件 |
| 按键、动作输入 | `Input.action_press`、`Input.parse_input_event` | 直接改节点状态冒充输入 |
| 看画面 | `xvfb-run`，Forward+ 用 `--rendering-driver vulkan`，Compatibility 用 `opengl3` | headless 下截图 |
| 录一段画面 | `--write-movie out/f.png` 或 `.avi`，同样要 xvfb | 循环截图 |
| 查类和方法是否存在 | `ClassDB.class_has_method`、类参考 XML | 凭记忆写 |
| 导出验证 | `--export-pack`，不需要模板 | 手动打 zip |
| 日志留档 | `--log-file`，目录须已存在 | `tee` 之外再造日志类 |
| 单元测试库 | GUT 或 gdUnit4 | 自写断言框架 |

## 做法

### 验证顺序

前一步不过不进下一步。

1. 改了 class_name、资源、自动加载、输入映射：`--import`
2. 每个改动的脚本 `--check-only`
3. 加载全部场景与脚本，看输出里的 ERROR
4. 冒烟脚本，覆盖改到的系统
5. 工程里有 GUT 或 gdUnit4 测试时跑它们

所有命令包进 `gdrun`：

| 处理 | 防什么 |
|---|---|
| 外层 `timeout -s KILL` | 卡死 |
| `</dev/null` | 调试器提示符等输入 |
| 去 ANSI 颜色 | grep 漏匹配 |
| 有失败特征行时退出码改 1 | 运行时错误不改退出码 |

```bash
gdrun() {
	local log rc
	log=$(mktemp)
	timeout -s KILL "${GD_TIMEOUT:-60}" "${GODOT_BIN:-godot}" --headless --no-header --path "${GD_PROJECT:-.}" "$@" </dev/null >"$log" 2>&1
	rc=$?
	sed -i 's/\x1b\[[0-9;]*m//g' "$log"
	cat "$log"
	if [ "$rc" -eq 0 ] && grep -E 'SCRIPT ERROR|Parse Error|^ERROR:|Error importing|Debugger Break|handle_crash|^FAIL:|^LOAD_FAIL|^ENGINE_ERRORS' "$log" | grep -vqE 'resources still in use|RID allocations|singleton'; then
		rc=1
	fi
	rm -f "$log"
	return "$rc"
}

gdrun --import
gdrun --check-only -s scripts/player.gd
gdrun -s tests/load_all.gd
GD_TIMEOUT=120 gdrun -s tests/smoke_level.gd
```

| 情况 | gdrun 退出码 | 特征输出 |
|---|---|---|
| 正常 | 0 | 脚本自己的 print |
| 解析错误 | 1 | `SCRIPT ERROR: Parse Error: ...` 加 `ERROR: Failed to load script` |
| 运行时错误后没走到 quit | 137 | `SCRIPT ERROR: Cannot call method ...`，随后被 KILL |
| `push_error` | 1 | `ERROR: ...` |
| 导入失败 | 1 | `ERROR: Error importing 'res://bad.png'.` |

- 排除的 `resources still in use` 与 `RID allocations` 来自测试脚本没释放的节点
- 测试脚本自己 `free()` 创建的节点，这两行就不出现

### GDScript 警告

命令行运行默认不打印警告。下面的脚本生成 `override.cfg`，把 Warn 级警告改成 Error。

<!-- check: gdonly -->
```gdscript
extends SceneTree

func _initialize() -> void:
	var cfg := ConfigFile.new()
	for p: Dictionary in ProjectSettings.get_property_list():
		var key: String = p["name"]
		if not key.begins_with("debug/gdscript/warnings/"):
			continue
		if typeof(ProjectSettings.get_setting(key)) == TYPE_INT and ProjectSettings.get_setting(key) == 1:
			cfg.set_value("debug", key.trim_prefix("debug/"), 2)
	cfg.save("res://override.cfg")
	quit()
```

```bash
gdrun -s tests/warn_as_error.gd
gdrun --quit-after 5
gdrun --check-only -s enemies/slime.gd
rm override.cfg
```

- 只有被加载的脚本才报，没挂进场景的脚本逐个 `--check-only`
- 默认关闭的项如 `untyped_declaration` 不在其中
- 要查就在 `override.cfg` 的 `[debug]` 下写 `gdscript/warnings/名字=2`
- `override.cfg` 对之后所有运行生效，用完删掉
- 不用 `--debug` 看警告：解析错误时崩溃 134，运行时错误停在 `debug>`

### 沙箱与只读目录

HOME 不可写时 Godot 报 `Could not create directory`，把三个 XDG 目录指到临时目录。项目目录也不可写时复制一份再跑。

```bash
T=$(mktemp -d)
cp -r . "$T/p"
export XDG_DATA_HOME="$T/d" XDG_CONFIG_HOME="$T/c" XDG_CACHE_HOME="$T/k" GD_PROJECT="$T/p"
mkdir -p "$T/p/tests"
cat > "$T/p/tests/warn_as_error.gd" <<'GD'
# 上一节的脚本全文
GD
gdrun --import
gdrun -s tests/warn_as_error.gd
gdrun --quit-after 5
gdrun --check-only -s enemies/slime.gd
```

- `gdrun` 定义、复制、写脚本、运行放在同一条 Bash 命令里
- 每次 `mktemp -d` 建新副本，不 `rm -rf ./*` 清旧副本
- 修改写回原项目，再重新复制验证
- 副本里的 `override.cfg` 不用删

### 冒烟脚本

继承 SceneTree，从 `_initialize` 开始，失败自己计数，最后 `quit(code)`。

<!-- check: gdonly -->
```gdscript
extends SceneTree

var _failures: int = 0

func _check(ok: bool, msg: String) -> void:
	if not ok:
		_failures += 1
		printerr("FAIL: ", msg)

func _initialize() -> void:
	create_timer(30.0).timeout.connect(quit.bind(2))
	_run()

func _run() -> void:
	var level := (load("res://level.tscn") as PackedScene).instantiate()
	root.add_child(level)
	await physics_frame
	for i: int in 10:
		await physics_frame
	_check(level.is_inside_tree(), "level in tree")
	level.queue_free()
	await process_frame
	quit(1 if _failures > 0 else 0)
```

- 自动加载在 `_initialize` 里已是 `root` 的子节点，在 `_init` 里还不是
- `_initialize` 返回前 `root` 不在树内，`_ready` 没跑
- 用 `global_position` 等全局变换前先 `await process_frame`
- 场景用 `root.add_child` 挂上，进树后 `_ready` 才跑
- 物理相关断言等够 `physics_frame` 再查
- 不用 `assert`，失败计数后 `quit(1)`
- 必须有看门狗：协程里报错后面不执行，进程不退出
- 结尾 `queue_free` 创建的场景再等一帧，退出时无泄漏警告

### 模拟输入

<!-- check: gdonly -->
```gdscript
extends SceneTree

func _initialize() -> void:
	Input.action_press("jump")
	print(Input.is_action_pressed("jump"))
	Input.action_release("jump")
	var ev := InputEventAction.new()
	ev.action = "ui_accept"
	ev.pressed = true
	Input.parse_input_event(ev)
	await process_frame
	quit()
```

- `Input.action_press` 当场生效，`parse_input_event` 要过一帧
- 动作名不在 InputMap 里时报错，状态恒为 false
- 无头下根窗口第一帧后只有 64x64，窗口外的点击点不到控件
- `await process_frame` 后设 `root.size = Vector2i(1152, 648)` 才能点
- `DisplayServer.window_set_size` 无效
- 点 UI 也可用焦点加 `ui_accept`，或直接 `pressed.emit()`
- 按下之后发松开

### 截图

headless 不渲染，用 xvfb 起真窗口。

```bash
xvfb-run -a -s "-screen 0 1280x720x24" "$GODOT_BIN" --path . --audio-driver Dummy --rendering-driver vulkan -s tests/shot.gd
```

- 脚本里 `await RenderingServer.frame_post_draw` 后 `save_png`，再用 Read 看图
- 装了 `mesa-vulkan-drivers` 时 `vulkan` 跑 Forward+，`opengl3` 跑 Compatibility
- 没有 Vulkan 驱动时 `vulkan` 打 ERROR 后回退 OpenGL 3，会被判失败
- CI 上要么装驱动，要么改 `opengl3`

### 查 API

先看类参考 XML 与 `docs.godotengine.org/en/stable/classes/class_<小写类名>.html`。

<!-- check: gdonly -->
```gdscript
extends SceneTree

func _initialize() -> void:
	print(ClassDB.class_has_method("Node", "queue_free"))
	print(ClassDB.class_get_signal_list("Timer", true).size())
	quit()
```

- `--doctool` 导出的 XML 说明为空，只能确认签名
- `--gdscript-docs` 从脚本的 `##` 注释生成 XML

### C# 工程

- 测试脚本仍用 GDScript，mono 版同时支持两种语言
- 运行前先 `dotnet build`，没构建就跑会卡住
- 构建与运行的实测输出见 [references/csharp.md](references/csharp.md)

## 陷阱

| 现象 | 做法 |
|---|---|
| 运行时 SCRIPT ERROR 后进程卡住，退出码不变 | 套 `timeout -s KILL`，脚本里放看门狗 |
| `--quit-after N` 前报过错，退出码仍是 0 | 靠 grep 或 Logger 计数判失败 |
| `assert` 失败只中断函数，走不到 `quit()` | 测试里不用 `assert`，release 导出里它被忽略 |
| `-d` 遇错停在 `debug>`，EOF 后退出码 0 或崩溃 | 不带 `-d`，输入重定向到 `/dev/null` |
| 缺 `ext_resource` 的 `.tscn` 仍 `load` 出非 null | 同时查输出里的 ERROR |
| `--import` 有导入或语法错误仍退出 0 | 看输出；错误只在首次导入打印 |
| 报 `Identifier "X" not declared`，X 是 class_name | 先 `--import` 建全局缓存，不删类型标注 |
| `--check-only` 报 autoload 名 `Identifier not found` | 误报；SceneTree 脚本用 `root.get_node("名字")` |
| `--quit-after` 与物理帧对不齐 | 加 `--fixed-fps 60` |
| headless 下截图 null，`frame_post_draw` 不触发 | 用 xvfb |
| `--write-movie` 或 `--log-file` 失败 | 输出目录先建好 |
| 标准版跑 `.cs` 报 `No loader found` | 用 mono 版并先 `dotnet build` |
| grep `ERROR:` 命中退出泄漏、ALSA、`singleton` is null | 具体排除这几行，不整类忽略 |
| `WARNING: N ObjectDB instances were leaked` | 测试脚本没 `free` 创建的节点，`--verbose` 看明细 |
| 以为 `--log-file` 会让终端静默 | 两边都有输出 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，mono 版构建、运行、失败输出
- [references/cli-flags.md](references/cli-flags.md)：每个参数的作用与实测输出、退出码表、渲染驱动实测
- [references/smoke-scripts.md](references/smoke-scripts.md)：冒烟脚本全文、加载全部场景、check-only 循环、点按钮、截图、运行时查 API
- [references/ci-and-frameworks.md](references/ci-and-frameworks.md)：下载 Godot 的 URL、导出、GUT 与 gdUnit4 命令行
- https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- https://docs.godotengine.org/en/stable/classes/class_scenetree.html
