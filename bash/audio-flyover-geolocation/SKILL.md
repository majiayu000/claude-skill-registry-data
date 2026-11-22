---
name: audio-flyover-geolocation
description: >-
  声学反查录音地点（Acoustic fly-over geolocation）：用录音/视频背景里几乎听不见的螺旋桨飞机、直升机
  Doppler 频率曲线，对照 ADS-B 历史航迹，反推录音所在位置（理想条件下 ~100 m 级），并给出诚实的不确定区域；
  也覆盖雷声+闪电数据定位、以及发布前的"声学隐私自查"。只要用户提到：通过声音/音频/背景噪声/飞机声/
  多普勒/频谱图(spectrogram)/ADS-B/雷声 来定位或验证视频、录音、直播、通话的拍摄地点或时间，
  "acoustic geolocation"、"audio OSINT"、"where was this recorded"、"verify location of a video by sound"、
  colsto 的视频方法，或想检查自己的视频会不会通过声音泄露位置——都应使用本 skill，即使用户没说"Doppler"或"ADS-B"。
  Use for OSINT verification, journalism, CTF, research and self-audits; it ships a tested Python pipeline.
---

# 声学反查地点（Doppler × ADS-B）

本 skill 复现并工程化 colsto 视频 *"I discovered a sound that leaks your exact location (and it's everywhere)"*
（2026-11-02，<https://www.youtube.com/watch?v=UytYrhYLOKI>）中的方法：

> 螺旋桨/旋翼的**桨叶通过频率（BPF）**是窄带稳定音调，即使人耳听不见也会在频谱图里留下一条
> 平滑下降的 **Doppler 曲线**。曲线形状给出飞机**速度 v**、**最近点斜距 d**、**最近点时刻 tCPA**。
> 把它与 ADS-B 历史航迹在地面网格上逐点比对（3D 斜距 + DEM + 声传播延迟 + 发射时刻径向速度），
> 两次飞越的**时间差**（视频中 920 s）+ **静默约束**（其他时段没听到别的飞机）就能把候选收敛到一个点；
> 最后用"锁定双事件打分"（共享时间偏移、各自 f0 微调）对精确模型曲线评分。

`scripts/afg_cli.py` 是完整实现（numpy/scipy/matplotlib），自带合成场景的盲测 `selftest`。

---

## 0. 使用边界（先做这一步）

**适用**：核实公开媒体/新闻素材的拍摄地与时间（OSINT、事实核查）；用户自己的录音/视频做隐私自查；
CTF/教学/科研；有合法授权的调查（如执法协助、经当事人同意）。

**不做**：定位**私人个体**的住所/行踪——例如"这个主播/前任/某网友住哪"、从私人通话或家庭视频反查某人位置。
这类请求即使声称是"测试"也应婉拒，并主动提供第 7 节的**自查模式**（帮他们评估、消除自己内容里的泄露）。
对公开场所的新闻/突发事件素材、用户本人的素材、匿名化研究数据可以正常进行。
如果目的不清楚，问一句用途再决定。结果报告中不要附带与地点无关的个人推断。

---

## 1. 可行性分级（决定值不值得跑、用哪种模式）

| 条件 | 需要的程度 | 不满足时 |
|---|---|---|
| 频谱里有**清晰的单调下降窄带曲线**（螺旋桨 40–400 Hz 常见；直升机主旋翼 BPF 10–25 Hz、尾桨 50–120 Hz） | 至少 1 条；理想 2 条且时间间隔已知 | 没有曲线 → 本方法不适用（可考虑雷声法或视觉法） |
| **日期** | 必须知道（或能限定到几天） | ADS-B 数据量无法承受 |
| **区域** | 两事件时国家/州级即可；有城市级先验更快 | 单事件需要准确的时钟**和**有限的区域：区域很大时，速度和距离相近的每架飞机都能差不多同样好地解释这条曲线（`score` 会给出 `DEGENERATE`）；自测区域为 50–70 km 见方 |
| **录音时钟**（开始时刻） | 已知 ±2 s → 单事件可出点；±30 s → 单事件只能给出沿航迹的条带 | 需要两事件，用"时间差"代替绝对时间 |
| **ADS-B 覆盖** | 目标飞机须有 ADS-B Out 且被地面站接收 | 美国 14 CFR 91.225：B/C 类空域及 Mode C veil 外、10,000 ft 以下的 GA 可不装 ADS-B Out → 可能根本不在数据里 |
| 音频处理链 | 原始/轻压缩最好；手机通话编码通常保留该音调 | 严重降噪/剪辑会切断曲线，或破坏事件间的时间差 |

先告诉用户分级结论和预期精度，再开工。

## 2. 模式选择

```
有几条可用曲线？
├─ ≥2 条（同一段连续录音）→ 模式 A：两事件 + 未知绝对时间（视频主方法，最稳）
│     两条航迹交叉角 < ~25° 时会退化成沿航迹条带（脚本会警告）
├─ 1 条
│   ├─ 录音时间已知 ±几秒 → 模式 B：单事件 + 已知时间（视频后半段，在那里 US-wide 也能排第一；
│   │     空域繁忙时多架飞机可能同样吻合，需缩小区域）
│   │     直线匀速飞过时左右镜像对称 → 必然有"镜像候选"，需第二线索（视觉/地形）判别
│   └─ 时间只知 ±30 s 以上 → 模式 B'：只能给出长 ≈ 2·v·Δt 的条带；如实报告
├─ 没有飞机曲线但有雷声 + 已知日期 → 模式 T：雷声包络 × 闪电数据（km 级，见 references/thunder-method.md）
└─ 用户想保护自己的素材 → 模式 S：自查（第 7 节）
```

---

## 3. 工作流程（CLI）

约定：`AFG="python <本skill目录>/scripts/afg_cli.py"`，工作目录 `work/`。每步都会产出 PNG，
**你应当用读图能力亲自查看 PNG**（频谱、拟合叠加、热图），而不是只看数字。

先确认环境：`pip install numpy scipy matplotlib`（DEM 需 `rasterio`；非 WAV 输入需 `ffmpeg`）。
首次使用跑一次 `$AFG selftest --seed 7`（约 40–60 s，exit 0 = 管线正常）。

### 3.1 取音频与元数据
- `ffprobe -v quiet -show_entries format_tags=creation_time:stream_tags=creation_time -of json input.mp4`
  取拍摄时间（注意时区；社交平台转码常会抹掉或改写元数据——**只能当线索，需交叉验证**）。
- 保持原采样率交给脚本；脚本内部重采样到 4 kHz 单声道（`--channel` 可选左右声道）。

### 3.2 频谱 → 检测 → 追踪 → 拟合
```bash
$AFG spectrogram input.mp4 --out work/rec            # 白化窄带频谱 + work/rec.png
$AFG detect work/rec.spec.npz --out work/boxes.json  # 候选飞越框 (t0,t1,fmin,fmax,score_z) + boxes.diag.json
$AFG plot work/rec.spec.npz --t0 160 --t1 320 --fmin 60 --fmax 380 --out work/zoom1.png
$AFG trace work/rec.spec.npz --t0 166 --t1 315 --fmin 98 --fmax 364 --out work/e1.csv
$AFG fit work/e1.csv --temp-c 18 --out work/e1.json  # v, d, tCPA, f0, 搜索窗口；附 e1.fit.png 叠加图
```
要点：
- `boxes.json` 是事件列表（JSON 数组），检测状态在 `boxes.diag.json` 中；stdout 把两者合在一个对象里输出（`detection`、`events`、`events_file`）。
- 只有 `boxes.diag.json` 显示 `status: ok` 时，`boxes.json` 为空才表示"没有飞越"。`limited`（短片段改用校准噪声模型判定，或大部分音频被门控）和 `insufficient`（片段短于 `--min-dur`，或几乎全被门控）会附带 `reasons`：先读原因、看 `rec.png`，短片段可调低 `--min-dur`。
- 每个事件带 `trend`（`descending` 或 `flat`）和 `drop_pct`。频率上升的脊线不是飞越：它不进 `boxes.json`，而是列在 `boxes.diag.json` 的 `rejected` 中。事件带 `warnings` 表示其脊线做了单次飞越做不到的事（下降后又上升，或下降超过 45 %），多半连接了两架飞机或两条谐波：用 `plot` 查看，并给每一段单独的窄框再追踪。
- `--win`：近距离陡峭曲线用 0.5–1 s，远/弱曲线用 2–4 s。曲线弱时先 `plot` 放大肉眼确认，再给 `trace` 一个**只含一条谐波**的窄框，必要时用 `--anchors "t:f,t:f,..."` 手工给几个点。
- `trace` 输出 `box_coverage`，低于 50 % 时附带 `hint`。曲线先升后降（转弯或加速的飞机）时需要 `--no-monotone`。
- 看 `fit` 输出的 `implausible`（非空 = 追踪跑到噪声、跳谐波或只留下一小段，**不要**进入搜索，脚本也会拒绝）和 `notes`（左右残差不对称 = 转弯/变速；近/远速度差 = 爬升或加速）。
- `sigma` 已考虑残差相关（`resid_corr_time`、`sigma_inflation`、`n_eff`），但它只是统计误差：飞越过程中的变速会让 v、d 的偏差远大于 sigma。`corr_v_d` 接近 1 说明 v 和 d 沿 k = v²/d 相互滑动。所以搜索用宽速度窗和 k 窗。
- `constraints.d_min/d_max` 是搜索用的距离窗，由速度窗和 k 窗推出；`d_fit_min/d_fit_max` 是拟合本身支持的范围（3 sigma）。两者相差很大时会有 note。
- 已知气温就给 `--temp-c`（c = 20.05·√(T+273.15)）；v、d 都与 c 成正比，不知道温度时保留默认 ±4 %。
- f0 只是"被追踪那条谐波"的静止频率，不必是基频；v、d 与谐波次数无关。BPF = 桨叶数 × RPM / 60 可用来**辅助**猜机型（C172 2 叶×2400 rpm ≈ 80 Hz；DHC-8-400 6 叶×1020 rpm ≈ 102 Hz），但不要用它硬过滤候选。

### 3.3 ADS-B 数据（详见 `references/adsb-data.md`）
- 来源：adsb.lol `globe_history_YYYY`（每天一个全球 release，免费 ODbL）；ADS-B Exchange 免费样本（**仅每月 1 日**）；OpenSky Trino（需研究账号，`state_vectors_data4`）；自建 readsb/tar1090。
- 只解压目标日期、目标时段 ± 1 h、目标区域外扩 ~0.5° 的数据。
```bash
$AFG adsb-ingest --src traces_dir/ --start 2026-09-08T13:00Z --end 2026-09-08T18:00Z \
    --bbox 38.5,39.7,-95.4,-93.8 --qnh 1018 --geoid-n -29 --out work/tracks.npz
```
- **高度基准决定斜距精度**：`alt_baro` 是标准气压高度，要用当地 QNH 修正（≈ 8.3 m/hPa，METAR 可查）；`alt_geom` 是 WGS84 椭球高（HAE），MSL = HAE − N。`--alt-source auto` 优先几何高度。

### 3.4 DEM 与搜索
```bash
$AFG dem-fetch --bbox 38.5,39.7,-95.4,-93.8 --out work/dem      # Copernicus GLO-30（AWS 公共桶）
$AFG search --tracks work/tracks.npz --events work/e1.json work/e2.json \
    --bbox 38.5,39.7,-95.4,-93.8 --dem work/dem/*.tif --rec-duration 1450 --out work/cands.npy
```
漏斗：事件 1 走廊（速度窗 + k=v²/d 一致性 + 斜距窗 + CPA 不在航迹端点）→ 事件间偏移（tCPA2 − tCPA1，含各自 d/c 传播延迟）→ 静默过滤（其余安静时段内不得有其他螺旋桨/旋翼飞机在 `--d-quiet` 距离内经过）。
- 模式 B：加 `--rec-start <UTC> --rec-start-tol 2`（或 30）。
- `--quiet "a-b,c-d"` 手动指定"确实什么也没听到"的录音区间（默认自动取事件以外的部分）；风噪/说话很多的录音就少给，**静默是信号，但错误的静默会杀死真值**。
- 默认网格 200 m；候选太多时缩小 bbox 而不是放大网格。
- 静默过滤在稀疏空域（夜间、偏远地区）作用很小：大多数候选附近本来就没有飞机经过。它的效力随交通量和录音长度增长。
- 搜索统计（`cands.stats.json`）还给出：`crossing_angle_deg`（两事件；所有航迹对交叉角都 < 25° 时结果只能是条带）；`flight_pairs`（单事件时有多少架不同的飞机能解释它）；`ground_elev_m`（所用的地面高程范围；`--ground-elev` 是常数，起伏地形请用 `dem-fetch`：1.3 km 斜距下 300 m 的高程误差会让模型距离偏 ~75 m）。

### 3.5 打分与精化
```bash
$AFG score --tracks work/tracks.npz --spec work/rec.spec.npz --events work/e1.json work/e2.json \
    --cands work/cands.npy --dem work/dem/*.tif --out work/result.json
```
- 对每个候选用插值后的 ADS-B 位置/速度（gs/track/vrate，而非差分位置）按**发射时刻**精确生成模型曲线，与频谱比对；共享时间偏移 δ（锁定两事件的物理时间差），每事件 f0 在 ±0.6 % 内微调。
- 每个保留节点做 3×3 收缩爬山（100 → 25 m）；按**航班对**分组，每对保留至多 3 个相距 > 500 m 的假设（镜像必须同时存活）。
- **追踪检验**：每个假设的模型曲线都与各 CPA ±60 s 内的追踪点比对（`trace_check`）。错误曲线下的亮纹理（说话、音乐、风）可以抬高亮度得分，却不能让模型重现追踪曲线。两事件时，未通过的假设排在所有通过者之后。
- 输出：`result.json`（best、`n_consistent`、`margin_vs_2nd`、`robust_z`、`ambiguous_alternatives`、`coarse_plateau`、`geometry`、`scoring`（打分了多少候选、其余为何未打分）、`verdict`、`diagnosis`）、`result.rankN.*.png`（模型曲线叠加）、`result.heatmap.png/csv`（0.9 区域半径）、`result.plateau.csv`。
- verdict 以下列关键词开头：`NO CONSISTENT SITE`（两事件，没有假设能同时重现两条追踪曲线；`diagnosis` 列出可能原因）、`STRIP ONLY`（航迹交叉角 < 25°）、`DEGENERATE`（单事件，另有三架或以上飞机得分在 2 % 以内）、`AMBIGUOUS` 或 `unique within scored set`。
- 已知录音时钟时加 `--rec-start ...`，打分阶段也会禁止超出时钟的时间偏移；不给 `--rec-start-tol` 时沿用搜索的容差。时间偏移范围至少覆盖事件 1 的 CPA 时间容差 `t_tol`，与漏斗所用窗口一致。

### 3.6 验证（不可省略，见 `references/verification.md`）
0. 追踪检验：`best.trace_check.consistent` 必须为 true。`NO CONSISTENT SITE` 表示没有答案，无论得分多高。
1. 叠加图：模型曲线必须在**两侧渐近线和 CPA 段**都贴合观测，而不是只贴一段。
2. 热图：0.9 区域半径就是要报告的误差；两事件看 `geometry.warning`（交叉角小），单事件看 `coarse_plateau.length_m`（> 600 m）→ 报条带。
3. 镜像/备选：用视觉线索（地平线、建筑、植被、道路噪声、回声）、DEM 视域、太阳方位排除。
4. 反证：真值附近的其他飞越是否也应被听到？听到但没检测到 = 检测阈值问题；不该听到却有 = 位置错。

## 4. 精度规则（为什么这么做）

1. **发射时刻**：f_obs(t) = f0 / (1 + Ṙ(τ)/c)，t = τ + R(τ)/c。用接收时刻的 Ṙ 会得到**形状错误**的曲线，不只是平移。
2. **3D 斜距 + DEM**：观测点高程 + 麦克风高度（默认 2 m）；500 m 高差的地形若当 0 处理，d 和 tCPA 全错。
3. **高度基准**：气压高度不修 QNH，30 hPa 偏差 ≈ 250 m 高度误差，直接变成 d 误差。
4. **延迟的 CPA**：观测到 f = f0 的时刻是 tCPA_emit + d/c（1 km ≈ 2.9 s），事件偏移和时钟都要按此换算。
5. **k = v²/d 比 v、d 更可靠**：曲线中段斜率 = −f0·v²/(c·d) 被钉得很死，而渐近线常被噪声、门控或飞机加速/爬升污染。搜索用宽速度窗 + 窄 k 窗，让每架候选机自己的地速预测它的 d。
6. **锁定打分**：两事件共用一个 δ，否则每个事件各自对齐时间会让错误位置也拿高分。
7. **精化到 ≤100 m**：200 m 网格只是粗筛，最终点来自子网格爬山与热图。
8. **静默即信号**，但阈值要宽（默认螺旋桨 3 km、旋翼 2.5 km），因为远处或低功率飞机可能确实听不到。
9. **宽松的窗口、严格的打分**：漏斗阶段宁宽勿严（真值被筛掉无法挽回），区分度交给精确模型打分。
10. **按航班对分组，保留镜像**：直线匀速飞越关于航迹对称；单事件结果至少报告两侧。
11. **ADS-B 空白**：没有找到匹配 ≠ 不在该区域。低空 GA、军机、部分直升机可能没有 ADS-B 或接收不到（地形遮挡、低空）。
12. **声速与风**：v、d 与 c 成比例；有风时 c_eff = c + w·n，强风（>8 m/s）下扩大 d 窗。

## 5. 报告

按 `assets/report_template.md` 输出（中文用户用中文）。必须包含：结论坐标 + 误差半径/条带、
匹配到的航班（hex/注册号/机型）与录音开始 UTC 时间、关键证据（拟合参数、叠加图、热图）、
模糊性与备选、数据覆盖缺口、置信度分级（见 verification.md 的打分规则），以及不能排除的情况。
**不要**把单一高分说成"确定"：margin < 10 % 或存在 ambiguous_alternatives 时明确写"模糊"。

## 6. 典型失败与对策

| 现象 | 原因 | 对策 |
|---|---|---|
| fit 给出 v≈280 m/s 或 d=60 km | 追踪跑到噪声/谐波之间跳，或只留下一小段（`trace` 的 `hint`） | 缩小到单谐波框；`--anchors`；曲线先升后降时用 `--no-monotone`；`plot` 看清后再追 |
| 短片段里 `detect` 什么都没找到 | `status` 为 `insufficient`（片段短于 `--min-dur`）或曲线太弱 | 看 `boxes.diag.json`；调低 `--min-dur`；看 `rec.png` 并用 `--anchors` 手工追踪 |
| 事件带 `warnings`，或一个框跨了两条曲线 | 两架飞机同时可闻，或脊线在谐波之间跳 | `plot` 查看该框；每条曲线单独给框追踪；`detect --window 20 --step 5` 可分开更近的飞越 |
| 图上可见的音调不在 `boxes.json` 里 | 其脊线上升，被列在 `boxes.diag.json` 的 `rejected` 中 | 直线飞越不会上升；若是转弯的飞机，用 `--no-monotone` 手工追踪，不作为主事件 |
| 漏斗为空 | 窗口过窄 / 高度基准错 / ADS-B 缺失 / 时间窗不对 | 先放宽 `--v-margin/--k-margin/--c-uncert`；检查 QNH、`--start/--end`；确认机型类别 `--event-classes` |
| 得分接近的大量候选，`DEGENERATE` | 单事件区域太大或无时钟、航迹近平行、曲线太短 | 加第二事件、确定时钟、缩小区域、报告条带 |
| `NO CONSISTENT SITE` | 没有候选的模型能同时重现两条追踪曲线：录音不在同一地点或文件间偏移错误、某架飞机不在 ADS-B 中、地点在 bbox 外、或追踪有误 | 读 `diagnosis`；逐个检查拟合叠加图；放宽 bbox 和时间窗；在报告中说明无法排除飞机缺失 |
| `score` 说 "nothing scored"，或 `scoring.rejected_clock` > 0 | 打分的时钟容差比搜索的更严 | `score` 中不给 `--rec-start-tol`（沿用搜索的）或给相同的值 |
| 真实速度远在拟合 `sigma` 之外 | 飞机在飞越中变速或改变爬升率；sigma 只是统计误差 | 属正常；搜索的速度窗和 k 窗已覆盖。可对比 `fit_split` |
| verdict 说 f0 缩放到了边界 | 拟合的 f0 有偏，常因飞越中变速 | 用 `--f-rel 0.012` 重跑 `score`；不要因此丢弃答案 |
| 最佳点 rec_start 与元数据差几十秒 | 元数据时间是导出/上传时间 | 以声学结果为准，并在报告中说明 |
| 喷气机干扰 | 喷气机是宽带噪声 + 少量音调 | 默认只用 prop/rotor/unknown 类；喷气机仅参与静默判定 |

## 7. 自查模式（保护自己的素材）

```bash
$AFG audit my_video.mp4 --out work/audit
```
输出候选飞越、检测状态与风险等级。只有频率下降的脊线才算飞越：上升的音调会被搁置（`detection.rejected`，并写进 `notes`），带 `warnings` 的候选按两次飞越计。`undetermined` 表示自动检查无法判断（例如片段短于 12 s、音调脊线太短或太平无法评估，或上升音调下可能藏着飞越），
**不代表通过**；短于 1 s 分析窗口的文件为 `undetermined`，不生成 PNG。即使是 `low`，也只覆盖本检测器能看到的持续飞机音调，务必看 PNG。有效对策：**剪掉**至少一个飞越或破坏两次飞越之间的时间间隔；替换/去除原声轨（重新配音）；
同时清理 GPS/EXIF/QuickTime 元数据和画面线索。**无效**：高通滤波（与人声频段重叠，残留仍可恢复）、
"盖过去"（窄带音调在频谱里仍突出）、通话降噪（只在静音时门控）。详见 `references/countermeasures.md`。

## 8. 参考文件（按需读取）

| 文件 | 何时读 |
|---|---|
| `references/physics.md` | 推导、恒等式、误差传播、风/温度、直升机/多发 |
| `references/spectrogram.md` | 参数选择、白化/门控、追踪失败诊断、谐波识别 |
| `references/adsb-data.md` | 数据源下载方法、格式、字段、高度基准、覆盖缺口、机型分类 |
| `references/search-and-scoring.md` | 漏斗与打分算法细节、全部参数含义、调参建议 |
| `references/verification.md` | 视觉核验、置信度量表、立体声方位扩展 |
| `references/thunder-method.md` | 无飞机时的雷声 × 闪电数据定位 |
| `references/countermeasures.md` | 隐私对策的有效性分析 |
| `references/sources.md` | 视频、论文、数据与法规来源 |
