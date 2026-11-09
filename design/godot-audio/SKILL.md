---
name: godot-audio
description: 写音效 音乐 音量设置 脚步声 战斗音乐切换 节奏同步时用，音效在游戏里发闷 模糊 与原文件听感不一样时也用。Audio bus 布局 Music SFX Voice、滑条调音量 linear_to_db、说话时侧链压低音乐、AudioStreamRandomizer 随机音效、max_polyphony 代替播放器池、AudioStreamInteractive 动态音乐、2D 3D 空间音频、3D 距离滤波、WAV 导入压缩、多类音效同时响的混音 分类子总线 响度 LUFS 并发上限 怪物出招压低枪声与音乐。audio bus volume music sfx muffled import mix loudness ducking.
---

# Godot 音频

先建总线布局，播放器用 `bus` 属性选总线，音量只在总线上调。

## 范围

| 不含 | 去哪 |
|---|---|
| 动画里的音频轨道 | godot-animation |
| 设置界面的生效与保存 | godot-ui |
| 播放器放在哪个场景 | godot-scene-architecture |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 音乐 音效 语音分开调音量 | Audio bus 布局加 `AudioServer.set_bus_volume_db` | 每个播放器写常量 `volume_db` |
| 同一音效不重复随机选 | AudioStreamRandomizer，默认 `PLAYBACK_RANDOM_NO_REPEATS` | 手写随机下标加上次记录 |
| 音高音量随机 | AudioStreamRandomizer 的 `random_pitch` `random_volume_offset_db` | `pitch_scale = randf_range()` |
| 同一音效叠播 | `max_polyphony` | 复制多个 AudioStreamPlayer |
| 大量不同的一次性音效 | AudioStreamPolyphonic | 自建播放器池 |
| 战斗探索音乐切换 分层 曲目列表 | AudioStreamInteractive Synchronized Playlist | 多个播放器手动淡入淡出 |
| 节奏游戏的歌曲时间 | `get_playback_position()` 加 `AudioServer.get_time_since_last_mix()` 减输出延迟 | `_process` 的 delta 累加 |
| 限制爆音 | Master 上的 AudioEffectHardLimiter | 逐个调低音量 |
| 说话时压低音乐 | Music 总线 AudioEffectCompressor，`sidechain` 设 Voice | 脚本逐帧调音乐音量 |
| 多类音效同时响 分开调比例 | SFX 下按类别建子总线 | 所有音效挤在一条 SFX |
| 循环 | 导入设置的循环选项 | 运行时改共享 stream 的 `loop` |
| 3D 音效在游戏里发闷 | 查 `attenuation_filter_cutoff_hz` | 把 WAV 转 Ogg 或提高采样率 |

## 做法

### 总线布局

编辑器底部 Audio 面板建 Music SFX Voice，发送到 Master，存为项目设置 `audio/buses/default_bus_layout` 的默认路径 `res://default_bus_layout.tres`：

```ini
[gd_resource type="AudioBusLayout" format=3]

[sub_resource type="AudioEffectHardLimiter" id="AudioEffectHardLimiter_1"]
ceiling_db = -1.0

[resource]
bus/0/effect/0/effect = SubResource("AudioEffectHardLimiter_1")
bus/0/effect/0/enabled = true
bus/1/name = &"Music"
bus/1/volume_db = 0.0
bus/1/send = &"Master"
bus/2/name = &"SFX"
bus/2/volume_db = 0.0
bus/2/send = &"Master"
```

- 播放器 `bus` 填总线名，总线不存在时回退 Master，拼错不报错
- 限幅放 Master 上用 AudioEffectHardLimiter，AudioEffectLimiter 已弃用
- 区域换总线：Area2D Area3D 的 `audio_bus_override` 加 `audio_bus_name`，做洞穴混响
- 区域换总线只对 2D 3D 播放器生效，播放器 `area_mask` 默认 0，要勾上区域的层

### 音量设置

```gdscript
extends HSlider

@export var bus_name: StringName = &"Music"

func _ready() -> void:
	min_value = 0.0
	max_value = 1.0
	step = 0.01
	value = AudioServer.get_bus_volume_linear(AudioServer.get_bus_index(bus_name))
	value_changed.connect(_on_value_changed)

func _on_value_changed(linear: float) -> void:
	var bus := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_volume_linear(bus, linear)
	AudioServer.set_bus_mute(bus, linear <= 0.0)
```

- 滑块用线性 0 到 1，直接当 `volume_db` 听感不均匀
- `AudioServer.set_bus_volume_linear` 与 `get_bus_volume_linear` 4.4+，内部做 `linear_to_db`
- 0 对应负无穷 dB，同时 `set_bus_mute`

### 混音

枪声、怪物出招、命中、UI 会同时响的游戏：

| 项 | 做法 |
|---|---|
| 类别子总线 | 每类一条，`send` 指向 SFX，策划在子总线上调比例 |
| 玩家滑块 | 只给 Master Music SFX Ambience 四个 |
| 子总线顺序 | 排在 SFX 之后，`send` 只能指向序号更小的总线 |
| 素材响度 | 短音效最大瞬时 -19 LUFS-M，真峰值不超过 -1 dBTP |
| 类别间差值 | 写在播放器或子总线音量里，换素材不用重调 |
| 高射速武器 | 每发比单发武器轻 2 到 4 dB |
| 并发 | 枪 `max_polyphony` 4 到 8，命中反馈 4 左右 |

用压缩器侧链压低，参数要自己给：

<!-- check: extends Node -->
```gdscript
func _ready() -> void:
	var duck := AudioEffectCompressor.new()
	duck.sidechain = &"Voice"
	duck.threshold = -18.0
	duck.ratio = 1.5
	duck.release_ms = 400.0
	AudioServer.add_bus_effect(AudioServer.get_bus_index(&"Music"), duck)
```

- `threshold` 默认 0 dB，触发声峰值不到 0 dBFS 就完全不压
- 压低量约为 2.08 × 峰值超出 `threshold` 的 dB × (1 − 1/`ratio`)，是常见公式的两倍
- 压低量随触发声响度变化

| 4.7.2 实测，触发峰值 -6 dBFS | 压低 |
|---|---|
| `threshold` -12，`ratio` 2 | 5 dB |
| `threshold` -20，`ratio` 1.2 | 4 dB |
| `threshold` -30，`ratio` 4 | 37 dB |

- 写死 -4 dB 这种固定量，或一个触发同时压多条总线，用电平加 AudioEffectAmplify，见 [references/mixing.md](references/mixing.md)

### 随机音效

编辑器里新建 AudioStreamRandomizer 拖入音效，或代码构造：

```gdscript
extends AudioStreamPlayer

@export var hits: Array[AudioStream] = []

func _ready() -> void:
	var random := AudioStreamRandomizer.new()
	random.playback_mode = AudioStreamRandomizer.PLAYBACK_RANDOM_NO_REPEATS
	random.random_pitch = 1.1
	random.random_volume_offset_db = 2.0
	for hit in hits:
		random.add_stream(-1, hit)
	stream = random
```

- `random_pitch` 是倍率，1.1 表示在 1/1.1 到 1.1 之间随机
- 按半音设用 `random_pitch_semitones` 4.6+
- `random_volume_offset_db` 2.0 表示正负 2 dB
- `add_stream` 第一参数小于 0 追加到末尾，第三参数是权重，默认 1.0

### 同时多声

| 情况 | 做法 |
|---|---|
| 同一音效连续触发，如机枪 | `max_polyphony` 4 到 8，超出时切掉最老的，默认 1 |
| 很多不同的一次性音效 | 一个播放器挂 AudioStreamPolyphonic，用 `play_stream()` |
| 每个实体自己的位置声 | 每个实体一个 AudioStreamPlayer2D 或 3D |

```gdscript
extends AudioStreamPlayer

var _poly: AudioStreamPlaybackPolyphonic

func _ready() -> void:
	var poly := AudioStreamPolyphonic.new()
	poly.polyphony = 16
	bus = &"SFX"
	stream = poly
	play()
	_poly = get_stream_playback()

func play_sfx(sound: AudioStream, gain_db: float = 0.0) -> int:
	return _poly.play_stream(sound, 0.0, gain_db)
```

- 声音走播放器的 `bus`，4.7.2 实测 Stream 播放类型下 `play_stream` 的 `bus` 参数无效
- 要分总线就按总线各挂一个播放器
- 返回播放 ID，给 `stop_stream` `set_stream_volume` `is_stream_playing` 用
- 并发满了返回 `AudioStreamPlaybackPolyphonic.INVALID_ID`

### 动态音乐

4.3+。

| 资源 | 用途 |
|---|---|
| AudioStreamInteractive | 多片段加转场表，在拍点或小节处切换 |
| AudioStreamPlaylist | 顺序或乱序播放子流，可淡入淡出与循环 |
| AudioStreamSynchronized | 多条子流同时开始，用音量加减层 |

- 切换片段：`set(&"parameters/switch_to_clip", &"Combat")`
- 转场表、拍点对齐、分层音量见 [references/dynamic-music.md](references/dynamic-music.md)

### 导入格式

| 素材 | 格式 | 导入设置 |
|---|---|---|
| 短音效 | WAV | `compress/mode` 默认 Quite OK Audio，接近原声，约 PCM 的 1/5，逐位无损选 PCM |
| 音乐 长环境声 | Ogg Vorbis 或 MP3 | 动态音乐的 `bpm` `beat_count` 只有这两种有 |
| 3D 定位音源 | 单声道 WAV | 打开 `force/mono` |

- 游戏里比原文件闷，先查播放器和总线，WAV 转 Ogg 只多一层有损压缩
- 96 kHz 素材按混音率重采样，开 `force/max_rate` 设 `force/max_rate_hz` 48000
- 立体声素材在 3D 播放器里保留声像宽度，定位不如单声道准

### 循环

| 格式 | 导入选项 | 单位 |
|---|---|---|
| WAV | `edit/loop_mode` `edit/loop_begin` `edit/loop_end` | 采样数，`loop_end` -1 取末尾 |
| Ogg Vorbis MP3 | `loop` `loop_offset` | 秒 |

- WAV 的 `loop_mode` 默认 Detect From WAV，跟随文件元数据
- 改完点 Reimport
- 运行时改共享 stream 的 `loop` 影响所有引用者，要不同行为就导入两份或 `duplicate()`
- 循环音频的播放器不发 `finished`

### 歌曲时间

`get_playback_position()` 按混音块更新，同一块内返回同一值，要加 `AudioServer.get_time_since_last_mix()` 再减输出延迟：

```gdscript
extends AudioStreamPlayer

var _latency: float = AudioServer.get_output_latency()

func song_time() -> float:
	return get_playback_position() + AudioServer.get_time_since_last_mix() - _latency
```

- `get_output_latency()` 开销大，取一次存起来
- 结果有抖动，丢弃比上一帧小的值
- stream 是 AudioStreamInteractive 时 `get_playback_position()` 恒为 0.0
- 另一种：`play()` 前记 `Time.get_ticks_usec()`，延迟取 `AudioServer.get_time_to_next_mix()` 加输出延迟
- 系统时钟法不抖，但长时间播放与声卡时钟漂移，长曲用上面的写法

### 空间音频

| 项 | 2D | 3D |
|---|---|---|
| 衰减 | `attenuation` 指数，默认 1.0 | `attenuation_model` 加 `unit_size` |
| 多普勒 | 无 | `doppler_tracking` |
| 听者 | 无 AudioListener2D 时为视口中心 | 当前 Camera3D |
| 距离高频滤波 | 无 | 默认开，`attenuation_filter_cutoff_hz` 5000，`attenuation_filter_db` -24 |

- 两者都有 `max_distance` `panning_strength` `area_mask`
- 听者放别处用 AudioListener2D 或 AudioListener3D 的 `make_current()`
- 全局声像强度见项目设置 `audio/general/2d_panning_strength` `audio/general/3d_panning_strength`
- 3D 滤波强度按衰减后的音量算，`volume_db` 也计入，低于 0 dB 越多压得越狠
- 不需要空气吸收的游戏，`attenuation_filter_cutoff_hz` 设 20500 关掉

<!-- check: extends Node3D -->
```gdscript
@onready var _gun: AudioStreamPlayer3D = $Gun

func _ready() -> void:
	_gun.unit_size = 15.0
	_gun.volume_db = -8.0
	_gun.attenuation_filter_cutoff_hz = 20500.0
```

- 保留远处发闷又想调小某音效，改素材增益或给它单独总线，总线音量不参与滤波

## 陷阱

| 现象 | 做法 |
|---|---|
| 3D 播放器 `volume_db = -8` 后近处也发闷 | 滤波按 `volume_db` 加距离衰减的总量算。实测镜头 14 m、`unit_size` 15 时 8 kHz 以上压约 24 dB |
| 3D 播放器调低 `volume_db` 几 dB 听不出 | 贴近时距离衰减有十几 dB 正值，`max_db` 截断在 `volume_db` 之后 |
| 玩家不能分开调音乐和音效 | 每个播放器写了 `volume_db`，改用总线 |
| 收尾音效播不完 | 播放器在会 `queue_free()` 的节点上，交给常驻播放器的 `play_stream()` |
| 暂停时菜单音和音乐也停 | 播放器 `process_mode` 设 `Node.PROCESS_MODE_ALWAYS` |
| 侧链压缩器一点不压或压太狠 | `threshold` 默认 0 dB，压低量是常见公式的两倍 |
| 子总线滑块不起作用 | 子总线排在父总线前，`send` 被静默改发 Master |
| 环境和音效滑块管不到某些声音 | `.tscn` 里播放器 `bus` 留空走 Master，每个都写 `bus` |
| 玩家调小语音后音乐压低变少 | `AudioServer.get_bus_peak_volume_left_db` 读推子之后的电平，一般正合适 |
| 网页导出效果器、多普勒、3D 混响不生效 | 默认 sample 播放，设 `playback_type` 为 `AudioServer.PLAYBACK_TYPE_STREAM`，延迟更高 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/mixing.md](references/mixing.md)：分类总线布局、响度测量与目标、并发规则、固定量压低、混音自查
- [references/dynamic-music.md](references/dynamic-music.md)：Interactive 转场、Synchronized 分层、Playlist
- https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html
