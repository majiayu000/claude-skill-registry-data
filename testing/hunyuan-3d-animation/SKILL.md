---
name: hunyuan-3d-animation
description: Rig and skin characters with HY-3D-Rigging or generate animation from text with HY-3D-Motion through Tencent TokenHub. Use for character rigging, humanoid motion templates, text-to-motion, confirmed native retarget inputs, task queries, and FBX downloads. Arbitrary skeleton retargeting is not supported.
---

# 混元 3D 动画

接入 **HY-3D-Rigging 绑骨蒙皮**与 **HY-3D-Motion 文生动作**。模型生成、网格处理、UV/纹理分别使用同系列 generator、mesh、material 技能。

## 操作选择

- 已有角色需要绑骨或套用动作模板：`rig`（别名 `rigging`），模型 `rigging`，输入 FBX/GLB。
- 根据文字生成动作：`motion`（别名 `text-to-motion`），模型 `motion`，输入动作描述，可不提供角色模型。
- `submit` 只提交，默认绑骨；文生动作须传 `--model motion`。`query` 也保留绑骨默认值，恢复文生动作必须显式指定 `--model motion`。

## 绑骨输入

- 输入是可访问的 HTTPS FBX/GLB 链接；OBJ、本地路径不能直接提交。需要时先准备格式副本，使用用户指定或已授权的存储，不自动上传到第三方。
- 人形输入按文档使用 A Pose 或 T Pose，避免附带坐骑、翅膀和复杂松散部件。动物等非人形采用单一生命体、简洁姿态；形态和姿态需检查模型，不能仅凭扩展名判断。详细来源和范围见 [references/rigging.md](references/rigging.md)。
- 默认只请求绑骨蒙皮，不发送 `motion_type`。用户明确需要模板动作时，用 `list-motions` 查编号，再传 `--motion-type 1..48`；不将模板视为自由文本动作生成。
- 非人形不支持动作模板。`--character-type humanoid|non-humanoid` 只记录已知分类用于本地校验，非人形与模板组合会被拒绝；未填不代表脚本已确认人形。选择模板前依据模型或已知上下文核对分类。
- `--input-size-bytes` 可检查已核验的文件大小，按文档 60mb 保守采用 60,000,000 字节上限。它和角色分类都不发送给 API，不填猜测值；预检不下载远端模型，也不检查姿态、权重或真实文件大小。

## 文生动作输入

- `--prompt` 必填，非空且最多 128 字符；这是字符限制，不按 UTF-8 字节计算。描述清楚人物动作，不擅自改变用户含义。
- `--duration` 为 1～12 的整数秒，未填用服务端默认 5 秒。需要自动估算时用 `--enable-duration-est`；需要固定时长时不启用自动估算。文档未定义两者同时设置的优先级。
- `--enable-mesh` / `--no-mesh` 控制 FBX 是否附带蒙皮网格，默认由服务端开启。`--enable-rewrite` / `--no-rewrite` 控制提示词扩写，`--enable-duration-est` / `--no-duration-est` 控制时长估算，后两者默认关闭；未指定的选项不发送。
- 重定向只适用于文档所述的混元动画模板接口产物。`retarget_file` 的内部字段未公开，不能从一个 FBX 链接猜出对象结构；仅在已有确认过的原生对象时使用 `--retarget-file-json JSON_FILE` 透传。它只校验 JSON，不证明模型来源、骨架兼容或内部字段有效，也不自动执行前置绑骨。详见 [references/motion.md](references/motion.md)。

## 执行与恢复

1. 使用 Python 3.10+，与 `hunyuan-3d-generator` 同级安装，共用客户端 API 版本 1；无需第三方库。执行时将脚本、输入输出解析为绝对路径。
2. 凭据优先读进程环境 `TOKENHUB_API_KEY`，兼容 `HUNYUAN_3D_API_KEY` / `TENCENT_HUNYUAN_API_KEY`。不要把真实密钥写入脚本、命令行或日志；本技能只支持 TokenHub。
3. 准备输入后用 `--dry-run` 预检；用户已授权相应操作且输入充分时提交一次。仅要求完善技能时不调用付费接口。`rig` / `motion` 提交、等待并下载，`submit` 只提交。
4. 收到 ID 后保留 ID、模型和地域。默认并发 1，轮询至少间隔 5 秒；任务 ID 有效期 24 小时。中断、超时或下载失败后用原模型查询原任务；提交结果不确定或缺少 ID 时先检查服务端记录，不自动重提。
5. 下载完成响应中全部资源。区分云端完成、下载和质量检查；需要检查时在 Blender 导入副本，核对骨架、权重、变形，动作还应检查实际时长、根节点位移和脚底滑动。未检查不能保证引擎兼容、蒙皮或动画质量。

## 命令

以下展示命令结构；执行时使用绝对路径。`example.com` 为占位链接。

```powershell
python scripts/hunyuan_animation.py rig --file-url "https://example.com/character.glb" --dry-run
python scripts/hunyuan_animation.py rig --file-url "https://example.com/animal.fbx" --character-type non-humanoid --output-dir rigged
python scripts/hunyuan_animation.py list-motions
python scripts/hunyuan_animation.py rig --file-url "https://example.com/character.glb" --character-type humanoid --motion-type 23 --output-dir walking
python scripts/hunyuan_animation.py submit --file-url "https://example.com/character.fbx"
python scripts/hunyuan_animation.py query JOB_ID --model rigging --wait --download --output-dir rigged
python scripts/hunyuan_animation.py motion --prompt "A person walks forward" --duration 5 --dry-run
python scripts/hunyuan_animation.py motion --prompt "人物向前走三步，然后转身挥手" --enable-rewrite --enable-duration-est --output-dir motions
python scripts/hunyuan_animation.py submit --model motion --prompt "A person jumps" --no-mesh
python scripts/hunyuan_animation.py query MOTION_JOB_ID --model motion --wait --download --output-dir motions
python scripts/hunyuan_animation.py check-auth
```

模型可写短名 `rigging` / `motion` 或完整名 `hy-3d-rigging` / `hy-3d-motion`，须与操作一致。`--base-url` 使用共用客户端的官方 TokenHub 地域白名单，默认广州，恢复时保留原地域。`check-auth` 只读取模型目录，不证明特定模型权限或额度充足。

## 维护

- 请求字段、输入要求和模板来源见 [references/rigging.md](references/rigging.md)。
- 文生动作参数、默认值和重定向限制见 [references/motion.md](references/motion.md)。
- 在本技能目录运行 `python -B -m unittest discover -s scripts -p 'test_*.py' -v`，模拟 HTTP 并阻止真实连接；用 skill-creator 的 `quick_validate.py` 检查结构。
- 若修改共享生成客户端，同时运行同系列其他技能的回归测试。
