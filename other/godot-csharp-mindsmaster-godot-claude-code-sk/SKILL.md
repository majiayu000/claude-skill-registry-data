---
name: godot-csharp
description: 在 Godot 里写 C# 时用。partial class 与源码生成器、[Export] [Signal] [GlobalClass] [Tool]、信号连接与断开、SignalName PropertyName 与 StringName 缓存、Variant 与 Godot.Collections、IsInstanceValid、async ToSignal、每帧分配。C# scripting in Godot.
---

# Godot C# 写法

C# 脚本的通用规则：源码生成器、命名映射、导出、信号、`StringName`、async。集合与对象生命周期见 references/runtime.md。各领域示例的 C# 写法在对应 skill 的 `references/csharp.md`。

## 范围

| 不含 | 去哪 |
|---|---|
| 各领域示例的 C# 写法 | 对应 skill 的 references/csharp.md |
| GDScript 写法 | godot-gdscript |
| 卡顿排查 | godot-performance |
| `[Tool]` 节点在编辑器里显示与存盘 | godot-scene-authoring |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 数学与随机 | `Mathf.Lerp`、`Mathf.MoveToward`、`GD.Randf`、`GD.RandRange` | 来回转 `double` 的 `System.Math` 调用 |
| 取节点 | `GetNode<T>("%Name")`、`[Export]` 引用、`GetNodeOrNull<T>` | 属性里或 `_Process` 里每次 `GetNode()` |
| 信号 | 生成的事件 `Pressed += OnPressed`，自定义用 `[Signal]` | `Connect("pressed", ...)` 字符串 |
| 名字常量 | `Node2D.PropertyName.Position`、`SignalName.Xxx`、`MethodName.Xxx` | 每次调用传字符串字面量 |
| 等信号与延时 | `await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout)` | `Task.Delay`，不跟 `Engine.TimeScale` 和节点生命周期 |
| 帧末调用 | `CallDeferred(MethodName.Foo)`，lambda 包成 `Callable` 再 `CallDeferred()` | 自建消息队列 |
| 后台计算 | `WorkerThreadPool.AddTask`、`Task.Run` 加 `CallDeferred()` 回主线程 | 自建 `Thread` 池 |
| 数据对象 | `[GlobalClass] partial class X : Resource` 加 `[Export]` | JSON 加手写解析 |
| 输入判断 | 事件模式匹配、`Input.GetVector` | 手写正负键相减 |
| 日志 | `GD.Print`、`GD.PushError`、`GD.PushWarning` | `Console.WriteLine` |

## 做法

### 类与源码生成器

```csharp
using Godot;

[GlobalClass]
public partial class Turret : Node2D
{
    [Export]
    public PackedScene BulletScene { get; set; }

    [Export(PropertyHint.Range, "0,10,0.1,or_greater")]
    public float Cooldown { get; set; } = 0.5f;

    [Export]
    private Marker2D _muzzle;

    private Label _label;
    private float _timer;

    public override void _Ready()
    {
        _label = GetNode<Label>("%Label");
    }

    public override void _Process(double delta)
    {
        _timer -= (float)delta;
    }
}
```

| 规则 | 违反时 |
|---|---|
| 派生自 `GodotObject` 的类写 `partial` | `GD0001` |
| 外层类含此类的嵌套类时外层也 `partial` | `GD0002` |
| `[GlobalClass]` 类不能是泛型 | `GD0402` |
| 挂到节点的脚本类名与 `.cs` 文件名一致，区分大小写 | 脚本挂不上 |
| 有无参构造，构造函数里不调依赖场景树的 API | 引擎创建实例失败 |

- 生成器给每个类补 `PropertyName`、`MethodName`、`SignalName` 嵌套类
- 生成器同时生成注册、导出默认值、热重载的保存与恢复代码
- 自定义类的常量值是 C# 原名，引擎类的值是 snake_case
- `PropertyName` 含非静态、Variant 兼容的字段与属性，含 private 与只读
- `MethodName` 含 Variant 兼容签名的方法，重载共用一个名字，泛型方法没有
- 嵌套类继承基类的同名嵌套类，`Hud.PropertyName.Position` 也能用
- 改 `[Export]` `[Signal]` `[Tool]` 后点编辑器右上角 Build，Inspector 才更新
- `[GlobalClass]` 让类出现在 Add Node 与 Create Resource 对话框，图标用 `[Icon("res://x.svg")]`
- `[Tool]` 让脚本在编辑器里运行，用 `Engine.IsEditorHint()` 区分

### 命名映射

- 方法属性 snake_case 转大驼峰：`move_and_slide()` 对应 `MoveAndSlide()`，getter setter 合成属性
- `Object` 对应 `GodotObject`，`RID` 对应 `Rid`
- 与属性同名的类内枚举加 Enum 后缀，如 Node.ProcessModeEnum
- `Vector2.RIGHT` 是只读属性 `Vector2.Right`，不能用在 `case` 里
- 接收字符串方法名的引擎 API 传 snake_case，优先用 `Node.MethodName.AddChild` 常量
- 路径函数用 `StringExtensions` 的 `GetBaseName()`，`System.IO.Path` 不认 `res://`
- 全表见 [references/gdscript-csharp.md](references/gdscript-csharp.md)

### 导出

```csharp
#nullable enable
using Godot;
using Godot.Collections;

public partial class Spawner : Node
{
    public enum Kind { Small, Big }

    [Export]
    public PackedScene Scene { get; set; } = null!;

    [Export]
    public Marker2D? Optional { get; set; }

    [Export]
    public Kind Size { get; set; } = Kind.Small;

    [ExportGroup("Waves")]
    [Export]
    public Array<PackedScene> Waves { get; set; } = new();

    [Export(PropertyHint.Enum, "Easy,Hard")]
    public string Difficulty { get; set; } = "Easy";
}
```

| 情况 | 结果 |
|---|---|
| `List<T>`、`System.Collections.Generic.Dictionary` | 不能导出，`GD0102` |
| 静态、只读、只写、索引器 | `GD0101` `GD0103` `GD0104` `GD0105` |
| 非 `Node` 派生的类导出 `Node` 成员 | `GD0107` |
| 复杂初始化表达式 | 生成器得不到默认值 |

- 可导出：基本类型、`string`、`GodotObject` 派生类、`Godot.Collections`、`byte[]` `Vector2[]` 等紧凑数组
- 字段与属性都可导出，任意访问级别
- 默认值由生成器分析初始化表达式得到，不执行 getter
- 启用 nullable 后，必有的引用写 `= null!`，可选的写 `?`
- 导出的 setter 在实例化时先于 `_Ready()` 调用，子节点引用还是 `null`
- `[ExportToolButton("Bake")]` 4.4+，`Callable` 类型的表达式体属性，类要 `[Tool]`

### 信号

```csharp
using Godot;

public partial class Health : Node
{
    [Signal]
    public delegate void ChangedEventHandler(int current, int max);

    [Signal]
    public delegate void DiedEventHandler();

    [Export]
    public int Max { get; set; } = 100;

    private int _current = 100;

    public void Damage(int amount)
    {
        _current = Mathf.Max(0, _current - amount);
        EmitSignalChanged(_current, Max);
        if (_current == 0)
        {
            EmitSignalDied();
        }
    }
}

public partial class Hud : Control
{
    [Export]
    public Health Target { get; set; }

    private Label _label;

    public override void _Ready()
    {
        _label = GetNode<Label>("Label");
    }

    public override void _EnterTree()
    {
        Target.Changed += OnChanged;
    }

    public override void _ExitTree()
    {
        Target.Changed -= OnChanged;
    }

    private void OnChanged(int current, int max)
    {
        _label.Text = $"{current}/{max}";
    }
}
```

- 委托名以 EventHandler 结尾 `GD0201`，返回 `void` `GD0203`，参数 Variant 兼容 `GD0202`
- 生成的事件名去掉后缀，事件不能 `Invoke()`
- 发射用生成的 `EmitSignalChanged(a, b)`，`sealed` 类里是 private，否则 protected
- `EmitSignal(SignalName.X, a, b)` 每次分配 `params` 数组，写成 `EmitSignal(SignalName.X, [a, b])` 不分配
- 引擎信号同样是事件：`button.Pressed += OnPressed`

| 连接方式 | 接收者释放后 |
|---|---|
| 引擎信号 `+=` 实例方法 | 按 `Delegate.Target` 自动断开 |
| 捕获了局部变量的 lambda | 不自动断开，回调访问接收者抛 `ObjectDisposedException` |
| 自定义信号 `+=` | 不自动断开，只写进发射者的托管委托 |
| `Connect(SignalName.X, Callable.From(OnX))` | 回调是接收者实例方法时自动断开 |

- 不自动断开的在 `_EnterTree()` 连接、`_ExitTree()` 里 `-=`，lambda 要保留委托引用
- OneShot 等标志用 `Connect()`：`(uint)GodotObject.ConnectFlags.OneShot`
- GDScript 定义的信号只能字符串连接：`Connect("sig", Callable.From(...))`
- 信号参数是自定义数据时类要继承 `GodotObject`

### StringName 缓存

字符串隐式转 `StringName` 等于 `new StringName(string)`，每次新建带终结器的托管对象并调一次原生，没有缓存。

```csharp
using Godot;

public partial class Flash : Sprite2D
{
    private static readonly StringName s_amount = "flash_amount";
    private ShaderMaterial _material;

    public override void _Ready()
    {
        _material = (ShaderMaterial)Material;
    }

    public override void _Process(double delta)
    {
        _material.SetShaderParameter(s_amount, 0.5f);
        if (Input.IsActionJustPressed(Actions.Jump))
        {
            Modulate = Colors.White;
        }
    }
}

public static class Actions
{
    public static readonly StringName Jump = "jump";
}
```

- 引擎名字用生成常量：`Node2D.PropertyName.Position`、`Button.SignalName.Pressed`、`Node.MethodName.AddChild`
- 输入动作、着色器参数、动画名、分组名、`Call()` `Get()` `Set()` 的名字放 `static readonly StringName`
- 名字只拼一次存起来，`NodePath` 同理

### async 与线程

- 等信号用 `await ToSignal(obj, SignalName.X)`，返回后先查 `IsInsideTree()`
- 没人 `await` 的 `Task` 异常不打印，入口 `try/catch` 并 `GD.PushError`
- 线程里碰场景树只能 `CallDeferred()`
- continuation 在哪个线程、等待对象被释放时的行为见 [references/runtime.md](references/runtime.md)

## 陷阱

| 现象 | 做法 |
|---|---|
| `Vector2 * delta` 编译不过 | `delta` 是 `double`，写 `(float)delta` |
| `Position.X = 1` 报 `CS1612` | `Position = Position with { X = 1 }` |
| `GetNode<T>()` 抛 `InvalidCastException` | 类型不符，可能为空用 `GetNodeOrNull<T>()` 或 `is` 模式匹配 |
| 每帧有 `StringName` `NodePath` 分配 | 字符串隐式转换，改成缓存字段 |
| 热重载后字段回到初始值 | 只读、`init`、静态、`List<T>` 不恢复，实现 `ISerializationListener` 重建 |
| 静态字段指向已释放对象 | 静态字段只放纯 C# 数据与 `StringName` |
| 程序集卸载失败 | 后台 `Task`、`Thread`、字段里的 `Callable` 在 `_ExitTree()` 里取消清理 |
| 把 EditorInterface 当静态类调用编译不过 | C# 里用它的 Singleton 属性 |
| `_Process` 里卡顿 | 每帧分配与跨界开销，见 [references/runtime.md](references/runtime.md) |

## 参考

- [references/gdscript-csharp.md](references/gdscript-csharp.md)：GDScript 与 C# 常用写法对照
- [references/runtime.md](references/runtime.md)：集合与 Variant、对象生命周期、async、输入事件、热重载、线程、跨界开销、每帧分配、托管泄漏排查
- https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_signals.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_collections.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_exports.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/cross_language_scripting.html
