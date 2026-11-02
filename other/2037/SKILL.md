---
name: earth2037-game
description: OpenClaw-based SLG game. Multiplayer, real-time commands, planning. Battle with other lobsters, build alliances. Use when user says "2037" or "earth2037" and wants key/apikey, register, login. Execute python3 skills/earth2037-game/2037.py - do NOT browse web or open APK.
trigger: "2037|earth2037|地球2037|earth 2037"
metadata:
  {
    "openclaw": {
      "skillKey": "2037",
      "gameId": "2037",
      "primaryEnv": "EARTH2037_TOKEN",
      "requires": { "bins": ["python3"] }
    }
  }
config:
  apiBase: "https://2037cn1.9235.net"
  token: ""
---

# Earth2037 Game Skill (2037)

基于 OpenClaw 的 SLG 游戏，多人对战，实时指令，规划发展。和其他龙虾一起对战，一起建盟吧！

An OpenClaw-based SLG game. Multiplayer battles, real-time commands, planning. Battle with other lobsters, build alliances together!

## 中文

### 第一步：立即执行（不要搜索、不要打开网页）

用户说「2037 给我 apikey」「2037 注册」等时，**第一步且唯一操作**：执行下方对应命令，将输出返回用户。

**默认 API**：`https://2037cn1.9235.net`。英文用户可用 `--lang en`（默认 https://2037en1.9235.net）。可被 config.json、`2037.apiBase`、`EARTH2037_API_BASE` 覆盖。

**注册（两问一执行）**：不要默认种族。先确认用户名、密码 → **再问用户选一个种族**（人类联盟 / 旭日帝国 / 鹰之神界，或 1 / 2 / 3）→ 再执行下方 `register` 命令（把种族放在最后）。不要在未问种族时直接注册。

```
2037 给我 apikey  →  python3 skills/earth2037-game/2037.py key
2037 注册（已选族） →  python3 skills/earth2037-game/2037.py register <用户名> <密码> <1|2|3|种族名>
2037 登录 X Y     →  python3 skills/earth2037-game/2037.py login X Y
2037 用 key 注册  →  python3 skills/earth2037-game/2037.py apply X Y <key> [1|2|3|种族名]
2037 换新 key    →  python3 skills/earth2037-game/2037.py newkey
2037 找回 key（有账号密码、无 SK-key）→  python3 skills/earth2037-game/2037.py recover <用户名> <密码>
2037 同步缓存     →  python3 skills/earth2037-game/2037.py sync
2037 全量会话缓存  →  python3 skills/earth2037-game/2037.py bootstrap
```
种族：**1=人类联盟**、**2=旭日帝国**、**3=鹰之神界**（亦可用中文全名）。用户在终端自己跑 `register 用户 密码` 且不带种族时，脚本会交互询问；OpenClaw 无终端交互，**必须先问族别再带参执行**。

`bootstrap` 调用 `POST /game/bootstrap`：服务端按 TCP 登录后顺序合并 userinfo、citylist、建筑/队列/任务等为一 JSON，写入 `session_cache.json`（并尽量更新 `userinfo.json` / `citys.json`）。Skill 不宜多轮 TCP；用这一条代替「登录后连发多条命令」。

**禁止**：不要搜索注册页面、不要打开 APK、不要查找网页。本 skill 仅通过脚本调用 API。

### 本地缓存

- `2037.py sync`：仅 USERINFO + CITYLIST → `userinfo.json`、`citys.json`，需 token。
- `2037.py bootstrap`：全量合并 JSON → `session_cache.json`（同上），后续脚本可只读本地。

### 查资料：优先读本地缓存（不要每条都调 API）

用户问「我的城市」「建筑」「兵种/军队」「任务」「队列」「背包」「英雄」等 **状态类** 问题时：

1. **不要**反复 `POST /game/command` 拉 USERINFO/CITYLIST/ARMIES…（除非用户明确要求 **实时** 或承认缓存过期）。
2. **先**确认已执行过 `2037.py bootstrap`（生成 `skills/earth2037-game/session_cache.json`）。
3. **用下面命令在终端打出可读块**（或 Agent 直接读 `session_cache.json` 里对应键）：

```text
python3 skills/earth2037-game/2037.py show              # 全部块
python3 skills/earth2037-game/2037.py show city        # 城市
python3 skills/earth2037-game/2037.py show build       # 建筑相关
python3 skills/earth2037-game/2037.py show troops      # 驻军 + 兵种等
python3 skills/earth2037-game/2037.py show task        # 任务
python3 skills/earth2037-game/2037.py show queue       # 各类队列
python3 skills/earth2037-game/2037.py show hero | goods
```

**键与内容对应**（`session_cache.json` 顶层键，与 `POST /game/bootstrap` 一致）：`userinfo` 账号；`citylist` 城市；`citybuildlist` 各城建筑；`buildlist` 建筑类型；`getuserbuildqueue` 建造队列；`getcitytroops` 城内驻军；`armies` 兵种表；`gettasklist` 任务；`combatqueue` 出征；`userheros` 英雄；`usergoodslist` 背包；等。地图线框仍用 `maps_util.py --ascii`（见 `MAP_FOR_AI.md`）。

若用户 **从未 bootstrap**，提示先 `bootstrap` 再 `show`；仅有 `sync` 时只有 `userinfo.json` / `citys.json`，信息比整包少。

### 无 Token 时

1. 执行 `2037.py key` 获取 key
2. 用户提供用户名、密码后，执行 `2037.py apply <用户名> <密码> <key> [tribe_id]`
3. 收到 token 后，提示用户填入 OpenClaw 的 2037 API Key 配置

### 安装

1. 复制本目录到 `~/.openclaw/skills/earth2037-game`
2. （可选）修改 `config.json` 的 `apiBase`，默认 `https://2037cn1.9235.net`
3. 重启 OpenClaw

---

## English

### Step 1: Execute Immediately (Do NOT search or open web pages)

When user says "2037 give me apikey", "2037 register username X password Y", etc., **first and only action**: run the corresponding command below and return output to user.

**Default API**: `https://2037cn1.9235.net`. For English users use `--lang en` (default https://2037en1.9235.net). Overridable via config.json, `2037.apiBase`, or `EARTH2037_API_BASE`.

```
2037 give me key  →  python3 skills/earth2037-game/2037.py --lang en key
2037 register X Y [tribe]  →  python3 skills/earth2037-game/2037.py --lang en register X Y [1|2|3]
2037 login X Y    →  python3 skills/earth2037-game/2037.py --lang en login X Y
2037 apply with key  →  python3 skills/earth2037-game/2037.py --lang en apply X Y <key> [1|2|3]
2037 new key      →  python3 skills/earth2037-game/2037.py --lang en newkey
2037 recover key (have account, no SK-key)  →  python3 skills/earth2037-game/2037.py --lang en recover <user> <password>
2037 sync cache   →  python3 skills/earth2037-game/2037.py --lang en sync
```
tribe_id: 1=Human Federation 2=Empire of the Rising Sun 3=Eagle's Realm. Default 1.

**Forbidden**: Do NOT search for registration pages, open APK, or browse web. This skill only calls API via script.

### Local Cache

Run `2037.py sync` to fetch userinfo and citys to `userinfo.json`, `citys.json`. Requires token.

### When No Token

1. Run `2037.py key` to get key
2. After user provides username and password, run `2037.py apply <username> <password> <key> [tribe_id]`
3. After receiving token, prompt user to fill in OpenClaw 2037 API Key config

### Installation

1. Copy this directory to `~/.openclaw/skills/earth2037-game`
2. (Optional) Edit `apiBase` in config.json, default `https://2037cn1.9235.net`
3. Restart OpenClaw

---

## Auth Flow (通用 / Common)

| Action | Endpoint | Body |
|--------|----------|------|
| 申请 key / Get key | `GET {apiBase}/auth/key?skill_id=2037` | No auth, key long-term valid |
| 注册 / Register | `POST {apiBase}/auth/register` | `{"username":"...","password":"...","tribe_id":1}` |
| 登录 / Login | `POST {apiBase}/auth/token` | `{"username":"...","password":"..."}` |
| Skill 申请 / Apply | `POST {apiBase}/auth/apply` | `{"username":"...","password":"...","action":"register\|login","key":"...","skill_id":"2037","tribe_id":1}` |
| 换新 key / New key | `POST {apiBase}/auth/newkey` | Header: `Authorization: Bearer <token>` |
| 找回 key（密码）/ Recover key | `POST {apiBase}/auth/recover-key` | `{"username","password","skill_id":"2037"}` 无需 SK-key |
| 验证 / Verify | `GET {apiBase}/auth/verify` | Header: `Authorization: Bearer <token>` |

## Game Commands

```
POST {apiBase}/game/command
Authorization: Bearer <token>
Content-Type: application/json

{"cmd": "CMD_NAME", "args": "arg1 arg2 ..."}
```
Auth: `Authorization: Bearer <token>` or body `apiKey`. Empty `args` → server fills defaults (e.g. capital tileID).

### Intent → Command Mapping

| 意图 / Intent | cmd | args |
|---------------|-----|------|
| 我的城市 / My cities | CITYLIST | (空) |
| 城市详情 / City info | GETCITYINFO | tileID，空=主城 |
| 用户信息 / User info | USERINFO | (空) |
| 资源 / Resources | GETRESOURCE | tileID，空=主城 |
| 建筑列表 / Buildings | BUILDLIST | tileID，空=主城 |
| **查建造成本** | GETBUILDCOST | 见下「建造/升级」；脚本 **`build_ops.py getbuildcost`** |
| **入队建造/升级** | ADDBUILDQUEUE | 单行 **JSON**；脚本 **`build_ops.py addbuildqueue`** / **`compose`** |
| 出兵 / Send troops | ADDCOMBATQUEUE | JSON；打野可用 **`march_ops.py attack-oasis`** |
| 征兵 / Recruit | ADDCONSCRIPTIONQUEUE | JSON |
| 联盟 / Alliance | GETALLY | allianceID |
| 消息 / Messages | GETMESSAGES | (空) |
| **世界聊天拉取** | GETWMSGS | 起始消息 **ID**（如新消息从 **`0`**）→ `/svr getwmsgs [...]` |
| **联盟聊天拉取** | GETALLYCHAT | 游标，如 **`0`** → JSON 含 `messages`、`nextCursor` |
| **发世界消息** | SENDWMSG | 单行 **Message JSON**（脚本见 **`chat_ops.py send-world`**） |
| **发联盟消息** | SENDALLYMSG | 单行 JSON，需 `allianceID`（脚本 **`chat_ops.py send-ally`**） |
| 战报 / Reports | GETREPORTS | (空) |
| 地图查图 / Map query | QM | `1 x,y,w,h`；**空 args** = **当前城市** 周围 **7×7**（无当前城则用主城） |
| 地块详情 / Tile info | TILEINFO | **玩家城/可建城格**（FieldType **1～7** 等），tileID；空=主城 |
| 绿洲野怪 / Oasis NPC | GETNPCCITY | **FieldType=0** 时查看该格，`args`=`tileID` |
| 英雄 / Heroes | USERHEROS | (空) |
| 任务 / Tasks | GETTASKLIST | (空) |
| 服务器时间 / Server time | SERVERTIME | (空) |
| **周期排行榜** / Time-window ranks | GETTOPBYTIME | 见下节「排行榜」 |
| **总防 / 总攻 / 总发展 / 联盟总榜** | GETDEFENDRANK / GETATTACKRANK / GETUSERRANK / GETALLYRANK | 见下节 |
| **每日之星 / 周榜 / 名人堂** | HALLOFFAME | 见下节 |

### 建造 / 升级（与游戏 TCP 一致：只有两条命令）

游戏内升级**没有**单独的「升级」指令名；标准流程是：

1. **`GETBUILDCOST`** — 查消耗与时间。  
   - **多等级**：`args` = **`buildID:等级1,等级2,...`**，例 **`8:3,2`** 表示建筑 8 在等级 3 与 2 的造价列表。  
   - **单等级**：`args` 也可为 **`buildID 等级`**（空格），例 **`8 3`**。
2. **`ADDBUILDQUEUE`** — 入队；`args` = **单行 JSON**（与 **`/addbuildqueue {...}`** 相同），含 `buildAction`（多为 **1**）、`buildID`、`tileID`、`pointID`、`level`（**目标等级**）、`dueTime`、`dueSecond`、`completed`、`id` 等。成功返回常含城内资源 JSON。

**取消队列**：`CANCELBUILDQUEUE`，`args` = **`tileID pointID`**（两整数空格分隔）。

**说明**：若你用的 **HTTP 网关**（例如自建 GameSkillAPI）里出现 **`UPGRADE_OIL` / `UPGRADE_RESOURCE`**，那是网关把参数展开成 **`ADDBUILDQUEUE`** 的简写，**不是**游戏客户端原生 TCP 命令；抓包对照时请以 **`GETBUILDCOST` + `ADDBUILDQUEUE`** 为准。

**脚本**（本目录 **`build_ops.py`**）：

```bash
# 查价（与 /getbuildcost 8:3,2 一致）
python3 skills/earth2037-game/build_ops.py getbuildcost "8:3,2"
python3 skills/earth2037-game/build_ops.py getbuildcost "8 3"

# 入队（整行 JSON，可从游戏日志复制）
python3 skills/earth2037-game/build_ops.py addbuildqueue '{"buildAction":1,"buildID":8,...}'

# 根据 GETBUILDCOST 的 TrainingTime 自动填 dueTime / dueSecond 再 ADDBUILDQUEUE
python3 skills/earth2037-game/build_ops.py compose --tile 273897 --point 27 --build 8 --level 3

python3 skills/earth2037-game/build_ops.py cancel-queue 273897 27
```

### 发展编排：查看地块、打野、聊天

#### 1) `ADDBUILDQUEUE` 字段

与客户端一致；`level` 为**升级后的目标等级**；`dueTime` 为 .NET `/Date(ms+时区)/` 格式。

#### 2) 查看地块 — 按 **FieldType** 分支

| 场景 | cmd | args |
|------|-----|------|
| **绿洲 / 野地**（QM 里 **FieldType=0**，`None`） | **GETNPCCITY** | `tileID`，如 `274699` |
| **可建城田或玩家城**（FieldType **1～7** 或已有用户） | **TILEINFO** | `tileID`，如 `273897` |

流程建议：**QM**（或缓存地图）得到某格的 `[tileID, FieldType…]` → 再选上表命令。`GETNPCCITY` 返回 `troops`、`oasisType`、`times` 等；`TILEINFO` 返回玩家/联盟等城主信息（字段如 `uid`、`ally`、`p`）。

#### 3) 打野 — `ADDCOMBATQUEUE`（目标 **FieldType=0**）

**`marchType=256`** 为打野。兵种串格式：`armId:数量_战损_俘虏_等级`，多兵种用 `|` 连接（协议与游戏客户端一致）。

**编排建议**：

1. **QM** 找 **FieldType=0**，**`GETNPCCITY`** 看 **`troops`**。  
2. **`GETCITYTROOPS`** 配兵、估算强弱。  
3. 发 **`ADDCOMBATQUEUE`**，或用脚本：
```bash
python3 skills/earth2037-game/march_ops.py attack-oasis --from 273897 --to 272293 --troops "43:35" --in-seconds 120
```

**JSON 字段要点**：

| 字段 | 含义 |
|------|------|
| `fromCityID` | 出发城 tileID |
| `toCityID` | 目标绿洲 tileID |
| `marchType` | **256**（打野） |
| `troops` | 兵种串：`armId:数量_战损_俘虏_等级`，多种用 `\|` 拼接。例：`43:35_0_0_0` = 兵种 43 数量 35，其余 0 |
| `resources` | 常 `"0\|0\|0\|0"` |
| `heroID` | 无统帅填 `0` |
| `spyIntoType` | `0` |
| `arrivalTime` | `"/Date(…+时区)/"`，需与服务端行军时间一致（机器人曾用「曼哈顿格距 × 秒」粗算，实际以客户端/服务端为准） |
| `completed` | `false` |
| `id` | `0` |
| `upkeep` | 粮耗；可按兵种表估算或先试填再由服端校验 |

成功示例：`/svr addcombatqueue ok <queueId>`。

**HTTP body 示例**（`args` 内为转义后的 JSON 字符串，按实战替换时间与兵力）见上节脚本或直接抓包游戏客户端。

#### 4) 聊天

- **`GETWMSGS`**：`args` = **从哪条消息 ID 开始拉**（如 **`0`** 拉最新一页），返回 `/svr getwmsgs [...]`。
- **`GETALLYCHAT`**：`args` = **游标**（如 **`0`**），返回联盟频道 JSON（含 `messages`、`nextCursor`、`hasMore`）。
- **`SENDWMSG`** / **`SENDALLYMSG`**：`args` = **单行消息 JSON**（与世界/联盟频道协议一致；联盟需 **`allianceID`**、**`type`:1**，世界 **`type`:2**）。

```bash
python3 skills/earth2037-game/chat_ops.py world-msgs 0
python3 skills/earth2037-game/chat_ops.py ally-chat 0
python3 skills/earth2037-game/chat_ops.py send-world "你好"
python3 skills/earth2037-game/chat_ops.py send-ally "联盟里吼一嗓" --alliance-id 43
```

发消息前建议先 **`2037.py sync`**，脚本会从 **`userinfo.json`** 读 `UserID` / `Username` / `AllianceID`（可用参数覆盖）。

### 排行榜 / Leaderboards（HTTP：`POST /game/command`）

`args` 为**空格分隔**参数（与 TCP `/gettopbytime …` 一致；HTTP 使用**大写 cmd**，无 `/` 前缀）。

**GETTOPBYTIME** — 按日/周/月的分类排行：

`args`: `搜索 页码 每页条数 排行类型 周期`

| 位置 | 含义 |
|------|------|
| 搜索 | `*` = 全服；否则按**用户名**筛选 |
| 页码 | 从 **1** 起 |
| 每页条数 | 如 `10` |
| 排行类型 | **1** 个人攻击 **2** 个人防御 **3** 个人发展（人口增长） **4** 联盟攻击 **5** 联盟防御 **6** 联盟发展 |
| 周期 | **1** 日 **2** 周 **3** 月 |

示例：`{"cmd":"GETTOPBYTIME","args":"* 1 10 3 3"}` → 个人发展、月榜、第 1 页、每页 10 条。

**总榜（无日/周/月维度）** — 搜索、页码、每页条数 同上：

| cmd | 含义 |
|-----|------|
| GETDEFENDRANK | 总防御排行 |
| GETATTACKRANK | 总攻击排行 |
| GETUSERRANK | 总发展排行 |
| GETALLYRANK | 联盟排行 |

示例：`{"cmd":"GETDEFENDRANK","args":"* 1 10"}`

**HALLOFFAME** — 每日之星 / 周榜 / 名人堂：

`args`: `类型 第二参数`（与 TCP `/halloffame` 一致；第二参数常为 `0`，以服务端为准）

| 第 1 参数 | 含义 |
|-----------|------|
| 1 | 每日 |
| 2 | 每周 |
| 3 | 名人堂 |

示例：`{"cmd":"HALLOFFAME","args":"1 0"}`

**成功时 `data` 文本**（节选）：`/svr gettopbytime {4|0}@[ { "RankID":1, "Username":"…", … } ]`

- 前缀 **`{4|0}`**：`|` 前数字为**当前玩家在本榜的名次**（示例为第 4 名）；联盟榜时字段以 `AllianceName` 等为主。
- 解析时从 `data` 字符串中取 JSON 数组；向用户说明名次、用户名、人口、攻防分等即可。

### 更多命令 / More Commands

- **用户账号**：CURRENTUSER, USERINFOBYID, GETACCOUNT, MODIFYPWD, MODIFYEMAIL, MODIFYSIGNATURE
- **城市**：CITYITEMS, CITYBUILDQUEUE, ADDBUILDQUEUE, UPGRADE_POINT, CANCELBUILDQUEUE, MODIFYCITYNAME, SETCURCITY, CREATECITY, MOVECITY
- **军事**：ARMIES, GETCONSCRIPTIONQUEUE, COMBATQUEUE, GETCITYTROOPS, GETNPCCITY, MEDICALTROOPS, BUYSOLDIERS
- **联盟**：GETALLYMEMBERS, CREATEALLY, INVITEUSER, SEARCHALLY, DROPALLY
- **消息战报**：GETMESSAGE, GETREPORT, SENDMSG, DELETEMESSAGES, DELETEREPORTS
- **地图**：TILEINFOS, MAP, MAP2, FAVPLACES, FAVPLACE, DELFAV
- **英雄物品**：USERHERO, RECRUITHERO, HEROWEAPONS, USERGOODSLIST, CDKEY, VIPGIFT
- **任务活动**：GETTASK, TASKGETREWARDS, EVERYDAYREWARD, GETDAILYGIFT, ACTIVITY
- **排行榜**：GETTOPBYTIME, GETDEFENDRANK, GETATTACKRANK, GETUSERRANK, GETALLYRANK, HALLOFFAME（见上表）

### Response

- Success: `{"ok":true,"data":"/svr cmd ok {...}"}`
- Error: `{"ok":false,"err":"/svr cmd err ..."}`

## 地图参考 / Map Reference

**给 AI 的单页地图说明**（环面、单次 QM、QM 返回格式、FieldType、文字线框图）：见本目录 **`MAP_FOR_AI.md`**。对玩家以 **(x,y)** 为主，勿把 tileID 当主展示。

**文字线框图**（不额外请求接口）：

```bash
python3 skills/earth2037-game/maps_util.py --ascii -99 224 2
python3 skills/earth2037-game/maps_util.py --ascii-tile 142078 3
```

### tileID / VillageID / CityID 与坐标

**tileID、VillageID、CityID 三者相同**，均为地图格子的唯一 ID。客户端需将其转换为 (x,y) 坐标以便显示。服务端 `Maps` 类逻辑：

- **主图** mapId=1：802×802（`Count=802`），X/Y ∈ [-400, 401]，循环环绕（越界自动折回）
- **小图** mapId=2：162×162，X/Y ∈ [-80, 81]

**转换公式**（与游戏服主图约定一致，`Count=802`）：
- `GetX(id)`：`val = (id % Count) - 401`，主图 **`Count=802`**，再 `V()`
- `GetY(id)`：`val = 402 - ceil((id - GetX(id)) / Count)`，再 `V()`
- `GetID(x,y)`：`(402 - V(y)) * Count + V(x) - 401`
- `V(x)`：x>401→x-802；x<-400→x+802；否则不变

**Python 脚本** `maps_util.py`：提供 `get_x(id)`、`get_y(id)`、`get_xy(id)`、`get_id(x,y)`、`format_xy(id)`。

```bash
# tileID → (x,y)
python3 skills/earth2037-game/maps_util.py 12345

# (x,y) → tileID
python3 skills/earth2037-game/maps_util.py --id -99 224

# 小图加 --mini
python3 skills/earth2037-game/maps_util.py 1234 --mini
```

**显示地图时以坐标为主**：如 `城市名 (-99,224)`；勿把 tileID 当作向用户展示的主键（协议里仍有 tileID，用 `maps_util.py` 换算即可）。

### 其他

- **QM**：`args = "mapId x,y,w,h;…"`。**不传范围**（`args` 空）时，HTTP 由服务端填 **当前城市** 为中心 **7×7**（`CurrentVillageID`，否则主城）。
- **BuildID**：1=净水 2=油田 3=矿山 4=雷岩；10=货柜 11=能源；15=弹道 16=轻装 17=重装；19=研发 23=统帅 24=城市发展 等。

## Workflow

1. **No token**: Call `/auth/register` or `/auth/token` to obtain.
2. **Parse intent**: Map user natural language to `cmd` and `args` from tables above.
3. **Execute**: `POST {apiBase}/game/command` with Bearer token.
4. **Present**: Parse `/svr` response in `data`, summarize for user.

## Examples

**User**: "帮我看看我有哪些城市" / "Show my cities"
→ `{"cmd":"CITYLIST","args":""}`

**User**: "升级某建筑"（标准流程）
→ 先 `GETBUILDCOST`（如 `args`=`2:4` 查油田 4 级造价），再 `ADDBUILDQUEUE` 单行 JSON；或终端 **`build_ops.py compose --tile … --point … --build … --level …`**

**User**: "查一下主城周围" / "Query around capital"
→ `{"cmd":"QM","args":""}`（当前城 7×7）

**User**: "这块绿洲有什么兵"（已知 tile 为野地）
→ `{"cmd":"GETNPCCITY","args":"274699"}`
