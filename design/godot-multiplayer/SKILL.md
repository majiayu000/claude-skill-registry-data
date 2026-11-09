---
name: godot-multiplayer
description: 写联机 多人 主机权威 同步 后加入 断线重连时用。ENetMultiplayerPeer 建连、@rpc 与 multiplayer_authority、MultiplayerSpawner MultiplayerSynchronizer 与可见性、传输模式与通道、NAT 与端口转发、ENetConnection 自建传输、预测与校正、两进程无头验收。客户端看不到主机的效果、后加入缺状态、奖励只发给主机时也用。multiplayer rpc replication late join netcode client prediction.
---

# Godot 联机

用高层多人 API 或 `ENetConnection` 搭主机权威联机，并验证客户端看到的和主机一致。

## 范围

| 不含 | 去哪 |
|---|---|
| 单机物理确定性与回放 | godot-animation |
| 两进程测试的通用写法 | godot-headless-testing |
| 场景拆分与节点通信 | godot-scene-architecture |
| 联机时设置菜单不暂停 | godot-ui |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 建连 | `ENetMultiplayerPeer.create_server` `ENetMultiplayerPeer.create_client` | 直接开 `PacketPeerUDP` 拼可靠重传 |
| 远程调用 | `@rpc`，C# 用 `[Rpc]` | 手写消息类型分发 |
| 运行时生成实体 | `MultiplayerSpawner` | 每种实体各写一个生成 RPC |
| 持续同步属性 | `MultiplayerSynchronizer` | 每帧发一条位置 RPC |
| 按玩家裁剪同步 | `MultiplayerSynchronizer.set_visibility_for` `MultiplayerSynchronizer.add_visibility_filter` | RPC 里逐个 `rpc_id` 过滤 |
| 入房鉴权 | `SceneMultiplayer.auth_callback` | 连上后再发第一条 RPC 校验 |
| 接自定义传输 | `MultiplayerPeerExtension` | 改写上层调用 |
| 点对点 穿透 NAT | `WebRTCMultiplayerPeer` 加 `WebRTCPeerConnection.initialize` 的 `iceServers` | 自己打洞 |

- 引擎不提供：大厅、好友邀请、客户端预测、校正重放、按接收者的流量预算
- ENet 不做 NAT 穿透，公网玩家连家用主机要转发 UDP 端口
- 免转发：`WebRTCMultiplayerPeer` 配 STUN TURN 和自建信令服务，原生平台装 webrtc-native 扩展
- 或者接第三方平台的传输

## 做法

### 建连

```gdscript
extends Node

const PORT := 7000
const MAX_CLIENTS := 3

func host() -> Error:
	var peer := ENetMultiplayerPeer.new()
	var error := peer.create_server(PORT, MAX_CLIENTS)
	if error != OK:
		return error
	multiplayer.multiplayer_peer = peer
	return OK

func join(address: String) -> Error:
	var peer := ENetMultiplayerPeer.new()
	var error := peer.create_client(address, PORT)
	if error != OK:
		return error
	multiplayer.multiplayer_peer = peer
	return OK
```

- `create_client` 返回 `OK` 只代表开始连接
- 连上等 `MultiplayerAPI.connected_to_server`，失败看 `MultiplayerAPI.connection_failed`
- 服务器 peer id 固定是 1

### 主机校验

客户端只发意图，结果由主机算：

```gdscript
extends Node

const OPEN_RANGE := 3.0

var players: Dictionary[int, Node3D] = {}
var chest_position := Vector3.ZERO
var opened := false

func request_open() -> void:
	open_chest.rpc_id(1)

@rpc("any_peer", "call_local", "reliable")
func open_chest() -> void:
	if not multiplayer.is_server() or opened:
		return
	var player: Node3D = players.get(multiplayer.get_remote_sender_id())
	if player == null or player.global_position.distance_to(chest_position) > OPEN_RANGE:
		return
	opened = true
```

- 主机本人也是玩家时要 `call_local`，否则主机自己点了没反应
- 身份只取 `MultiplayerAPI.get_remote_sender_id`，不信参数里的玩家 id
- `get_remote_sender_id` 只在 RPC 同步执行期间有效，`await` 后为 0，先存局部变量
- 扣费类请求带版本号或请求 id，防止重复请求按两次算

| `@rpc` 参数 | 默认 |
|---|---|
| 调用权限 | `authority` |
| 本地是否执行 | `call_remote` |
| 传输模式 | `reliable`，C# 的 `[Rpc]` 同样 |
| 通道 | 0 |

- 高频数据显式写传输模式，否则全走可靠
- 两端 RPC 配置要一致，引擎按全部 RPC 的校验和比对

### 传输模式

| 模式 | ENet 标志 | 用途 |
|---|---|---|
| `TRANSFER_MODE_RELIABLE` | RELIABLE | 请求 回执 生成 销毁 死亡 |
| `TRANSFER_MODE_UNRELIABLE_ORDERED` | UNRELIABLE_FRAGMENT | 位置快照，晚到的旧包丢弃 |
| `TRANSFER_MODE_UNRELIABLE` | UNSEQUENCED 加 UNRELIABLE_FRAGMENT | 可乱序的高频数据 |

- 不可靠和可靠走不同 ENet 通道，互相没有先后保证
- 后发的不可靠快照可能先于可靠的生成包到达，接收方容忍实体暂时不存在
- 通道号大于 0 时建独立通道，慢消息不挡快消息
- 不可靠数据单包控制在 1364 字节内：MTU 1392 减 ENet 头 4 字节和分片头 24 字节

### 复制

```gdscript
extends MultiplayerSpawner

@export var enemy_scene: PackedScene

func _ready() -> void:
	spawn_function = _create_enemy

func _create_enemy(data: Dictionary) -> Node:
	var enemy: Node3D = enemy_scene.instantiate()
	enemy.position = data["position"]
	return enemy
```

主机调用 `MultiplayerSpawner.spawn`，`spawn_function` 在所有对端执行，返回未入树的节点。

| 项 | 规则 |
|---|---|
| 自动生成 | 只认 `spawn_path` 的直接子节点，场景在可生成列表里 |
| 自动生成的节点名 | `add_child(node, true)` 第二参数要开 |
| `spawn()` 的初始值 | 写在 `spawn_function` 里，所有端走同一份 |
| 可同步的属性 | 不支持 `Resource` 这类 `Object` 属性、实例 id、RID |
| 单节点同步状态超过 `SceneMultiplayer.max_sync_packet_size` | 不发送只报错，默认 1350 |
| `MultiplayerSynchronizer.replication_interval` | 默认 0，每个网络帧同步 |

### 后加入

Spawner 生成的实体和 Synchronizer 状态会补发给新对端。下列不补发，要自己放进全量状态：

| 内容 | 后加入者看到 |
|---|---|
| 已发过的 RPC，如预警、Boss 阶段、门开关 | 看不到 |
| 场景预置节点的变化，如主机上已销毁的预置物 | 本地还在，碰撞也在 |
| 有存续时间的区域效果，只发了开始事件 | 看不到，伤害照常结算 |

- 判断标准：事件发生 10 秒后进房的人眼里，它不是初始值，就属于状态
- 逐项检查表见 [references/sync-checklist.md](references/sync-checklist.md)

### 表现同步

AI 和玩法脚本只在权威端跑时，动作、隐藏、节点生成都只有主机看得见。

| 层 | 职责 |
|---|---|
| 权威端 | 决定发生了什么 |
| 复制层 | 把结果变成状态或事件 |
| 各端表现层 | 只读状态和事件 |

- 新增技能或交互时同时写一条客户端断言，漏同步在主机上看不出来

### 自建传输与预测

| 需求 | 读 |
|---|---|
| 在 `ENetConnection` 上自写协议 | [references/custom-transport.md](references/custom-transport.md)，默认标志 0 的超长包会改成可靠分片 |
| 客户端预测与校正 | [references/authoritative-movement.md](references/authoritative-movement.md)，校正消息带全部影响位移的状态 |

### 两进程验证

```bash
godot --headless --path . res://tests/net_smoke.tscn -- --host 27400
godot --headless --path . res://tests/net_smoke.tscn -- --join 127.0.0.1 27400
```

- 用 `OS.get_cmdline_user_args` 读 `--` 之后的参数
- 主机日志出现就绪标记后再起客户端
- 两边各自断言并以退出码报告，只看主机通过不算验收
- 本机回环没有延迟丢包，给传输层包一层加延迟、抖动、丢包
- 超时按两端加载耗时之和留余量

## 陷阱

| 现象 | 做法 |
|---|---|
| RPC 按渲染帧到达、暂停时也到 | `SceneTree.multiplayer_poll` 开启时每渲染帧轮询一次，暂停也跑 |
| 暂停时自建连接超时 | 轮询 `ENetConnection.service` 的节点设 `PROCESS_MODE_ALWAYS` |
| 主动断开后清理没执行 | `MultiplayerPeer.close` 不触发 `MultiplayerPeer.peer_disconnected` |
| 奖励、治疗只发给主机 | 遍历所有玩家，单机和主机测试都测不出 |
| 远端短按丢失 | 远端输入只存当前状态，做按下锁存 |
| 主机退出后客户端残留局内数据 | 主动离开和被断开两条路径都清全局单例 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/sync-checklist.md](references/sync-checklist.md)：新增同步内容时的逐项检查
- [references/custom-transport.md](references/custom-transport.md)：`ENetConnection` 的发送、超时、断开语义
- [references/authoritative-movement.md](references/authoritative-movement.md)：预测、校正、重放的不变量
- https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html
- https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html
- https://docs.godotengine.org/en/stable/classes/class_enetconnection.html
