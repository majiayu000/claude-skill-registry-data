---
name: "skill-quality-check"
description: "技能质量检查：版本号统一性、版权信息、硬编码敏感信息、命名规范、代码规范"
author: 思捷娅科技 (SJYKJ)/zhaog100
license: MIT
---

# 技能质量检查

## 触发条件
- 部署新技能前
- 修复技能问题后
- 官家要求检查技能质量时

## 检查项

### 1. 版权信息
检查所有文件头部是否有版权：
```bash
grep -r "Copyright" <skill_dir> --include="*.py" --include="*.sh" --include="*.md"
```
要求：所有文件均有 `MIT License | Copyright (c) 2026 思捷娅科技 (SJYKJ)`
- 检查范围必须包含 `config/*.yaml`（yaml 用注释式 `# 版权` 头）和 README.md（Markdown 尾注），不只查 .py/.sh/.md；yaml 补完版权后逐文件 `yaml.safe_load` 验证语法未破坏

### 2. 版本号统一性
检查所有Python文件版本号：
```bash
grep "^# 版本\|^version\|版本:" <skill_dir>/scripts/*.py
```
要求：所有文件版本号一致（如 v3.3）

### 3. 硬编码敏感信息
检查敏感信息硬编码：
```bash
grep -rn "api_key\|secret\|token\|password\|APP_ID\|APP_SECRET" <skill_dir>/scripts/
```
要求：
- 敏感信息从环境变量读取（`os.environ.get()`）
- 或从配置文件读取（config/ 目录）
- 不得硬编码在代码中

### 4. 命名规范
- Python文件：英文小写+下划线（如 `crawl_wiki.py`）
- 配置文件：放在 `config/` 目录
- 日志文件：放在 `logs/` 目录

### 5. 代码规范
- 使用 `logging` 模块，不得有 `print()` 残留
- 检查：`grep -n "print(" <skill_dir>/scripts/*.py`
- 如果存在print残留，使用Python脚本批量替换为logger.info()
- **入口脚本同样受查**：门面/CLI 入口（entry.py 等）的 print 也违规；修复时用 `sys.stdout.isatty()` 判定——交互终端才 print，管道/cron/非交互场景一律走 logging

### 6. 版权格式（2026-09-05新增）
- 所有技能文件必须使用统一MIT版权格式：
```python
Copyright (c) 2026 思捷娅科技 (SJYKJ)
License: MIT
Author: 小米粒 (Xiaomili) - AI Agent
```
- 检查：`grep -r "Copyright (c) 2026 思捷娅科技" <skill_dir>`
- 参考：`DEVELOPMENT_RULES.md` 文件

### 7. 敏感信息脱敏
- QQ_TARGET：使用环境变量`${QQ_TARGET_USER_ID:-默认值}`
- APP_SECRET：使用`os.environ.get("QQ_APP_SECRET")`
- token：使用环境变量或配置文件占位符`${VAR_NAME}`

## 前置：技能归属分类（2026-09-10新增）

**原则**：只修改自己开发的技能，第三方技能不动。

### 分类方法
```bash
# 方法1：查SKILL.md中的版权标记
grep -r "思捷娅\|SJYKJ" <skill_dir>/SKILL.md

# 方法2：查SKILL.md中的homepage字段（第三方来源标识）
grep -i "homepage:" <skill_dir>/SKILL.md

# 方法3：查Git历史作者
git log --all --format="%an" -- "skills/<skill_name>/"
```

### 分类结果
| 类型 | 标识 | 操作 |
|------|------|------|
| 自己开发 | 含 SJYKJ/思捷娅 版权 | ✅ 可修改 |
| 第三方 | 含 homepage 字段 + 外部URL | ❌ 不动 |
| 疑似自己但无版权 | 无版权标记但作者是zhaog100 | ⚠️ 需确认 |

### 第三方技能清单（已知）
- proactivity → https://clawic.com/skills/proactivity
- self-improving → https://clawic.com/skills/self-improving
- china-exam-info-core → https://www.openclaw.ai
- miliger-qmd-manager → github.com/miliger/qmd-manager
- moltbook-skill → github.com/voidborne-agent/moltbook-skill
- notion/obsidian/playwright/summarize/tavily/weather → 第三方官方

## 自动化关卡（2026-09-30 落地，官家定：发布检查不能靠人记得发指令）

把 7 项 review 挂成自动关卡，不依赖手动触发：

1. **`scripts/release_gate.py` 是唯一检查器**（Python，一次性跑全维度；已建好，改检测项只改这个文件，不要另写 shell 审计脚本）。
   - 分级退出码：**硬漏洞 = 脱敏(open_id/token)/硬编码绝对路径/版权缺失** → exit 1 挡 push；**软问题 = print 残留/版本号不一致/命名不规范** → 只告警不挡。
   - print 残留判定时这些放行不算违规：报告/格式输出类文件（report/format/brief/card）、`legacy` 留档、`signals/` 与 `scripts/` 下的输出脚本、`isatty`/`interactive` 门控块内的 print、`fix_print*` 修复脚本本身。
   - 支持 `--self-developed`（只查含 SJYKJ/思捷娅版权的自研 skill，第三方不牵连）。
2. **git pre-push hook**：只检查**本次 push 涉及文件所属的 skill**（从 `git diff --name-only origin/main..HEAD` 提取 `skills/<name>`），**不要扫全仓**——扫全仓会被没改过的第三方/无关 skill 的既有版权缺失挡住本次 push。
3. **每周体检 cron**：周一 9:00 跑 `release_gate.py --self-developed` 扫全仓，硬问题清单推 QQ（全过则报"本周通过"）。

## 执行步骤
1. **分类技能**：判断是自己开发还是第三方（见上）
2. 读取技能目录结构
3. 检查版权信息（grep -l 检查有版权，grep -L 检查无版权）
4. 检查版本号（grep）
5. 检查硬编码（grep）
6. 检查命名规范（ls）
7. 检查代码规范（grep print）
8. 修复后重新检查（若使用修复脚本，脚本文件本身可能缺版权）
9. 生成检查报告

## 常见修复流程
- print残留 → 使用Python脚本批量替换为logger.info()，脚本自身需补版权
- 版权缺失 → grep -L 找出无版权文件，使用edit添加版权块
- 版本不一致 → grep "^# 版本" 找出差异，统一修订版（patch版本）

## 批量审查执行方法（2026-09-28新增）
单个技能逐项 grep 可行；40 个技能全量审查时按以下流程：
1. 先定位自研技能范围（前置分类），再写一个 Python 审计脚本一次性跑全部维度（版权/版本/脱敏/硬编码/print/logging/命名），不要逐技能手敲 grep。
2. Python 审计脚本直接读文件、正则匹配、分类输出；避免在 shell 里写 `$( ... )` 嵌套 + 单引号混用的复杂脚本——本次 4 次因 shell 转义/括号语法报错才改用 Python 脚本，多耗了 4+ 轮。
3. 脱敏检查必须同时验证 gitignore 状态：`git check-ignore <path>` 确认命中路径不会入库；发现的未忽略目录（如 venv/）立即加入 .gitignore 并复验。
4. 版本号对齐规则：子模块脚本（send_qq_*.py 等）版本跟随主 SKILL.md 版本；主版本以 SKILL.md 的 `version:` 字段为准，冲突时升级滞后方。
5. 修复后统一一次 commit + push（zhaog100/xiaomijiao-skills main 分支），commit message 列明各修复项。

## 输出格式
```
=== <skill_name> 技能检查报告 ===
【1. 版权信息】✅/❌
【2. 版本号】✅/❌
【3. 硬编码】✅/❌
【4. 命名规范】✅/❌
【5. 代码规范】✅/❌

修复建议：...
```


## 📤 按技能粒度推送（2026-09-30 新增）

**远端技能仓 `zhaog100/openclaw-skills` 是扁平结构（根目录一个 skill 一个目录），本地 workspace 是 `skills/<name>/` 带前缀。直接整仓 push 会推歪目录，必须按 skill 粒度推。**

### 推送前 3 步（防丢原则：只多不少）
```bash
# 1. 浅 clone 远端做 diff（不影响本地仓）
git clone --depth 1 https://github.com/zhaog100/openclaw-skills.git /tmp/oc-push
# 2. 文件级 diff，确认远端无"本地没有的独有内容"（本地应是超集）
cd /tmp/oc-push/<skill> && find . -type f | grep -vE "__pycache__|/cache/|/reports/" | sort > /tmp/remote.txt
cd <workspace>/skills/<skill> && find . -type f | grep -vE "__pycache__|/cache/|/reports/|backup-" | sort > /tmp/local.txt
comm -23 /tmp/remote.txt /tmp/local.txt   # 远端有本地没有 = 会丢的东西，必须保留
# 3. 拷贝进 clone、保留远端独有（如历史 reports）、清临时目录、commit + push
git checkout HEAD -- <远端独有目录>/   # 保留
rm -rf <本地临时 backup 目录>/
git add -A && git commit -m "..." && git push origin main
```

### 判定"新增还是更新"
- 远端该 skill 目录 **404 不存在** → **新增**（整个目录推上去）
- 远端 **已存在** → **更新**（覆盖代码，但保留远端独有历史产物如 reports/）
- 待推清单里**不得有删除项（D）**——有 D 说明会删远端历史，违反"只多不少"

### 凭证脱敏（推公开仓前必查）
- 检查待推的 config/*.json 是否含真实 token/open_id/手机号（应只有 `${VAR}` 占位符）
- `git check-ignore` 确认 cache/reports/.env/pickle 不会入库
- open_id 不得写死默认值，走环境变量/config，缺失要**明确报错**不静默兜底

### 脱敏改动必须同步调用方注入（2026-09-30 踩坑沉淀）
去硬编码 open_id/secret 是"代码侧去硬编码 + 调用方注入替代值"两件事，只做一半即线上故障：
1. 代码改成"读环境变量 `QQ_TARGET_USER_ID`，缺失即拒绝执行"后，立即给每个调用方注入该变量：
   - openclaw cron automation：`openclaw cron edit <id> --command-env "QQ_TARGET_USER_ID=<id>"`（`--command-argv` 必须是 JSON 数组字符串，如 `'["bash","/path/script.sh"]'`；argv 写成空格分隔会报 "must be a JSON array of strings"）
   - CI/shell：env 文件或 export 段
2. 注入后**手动带 env 跑一次全链路**确认 `exit=0`，再算脱敏完成；只验证代码侧不验调用方必踩坑（实例：4 个 cron 未注入 → 定时任务 exit 1 静默不推送）。
3. command 型 automation 的"推送"若由脚本内部走 Gateway REST 完成，cron 层 `lastDeliveryStatus=not-delivered` 是正常（announce 无内容可发），以脚本日志为准，别误判为推送失败。
4. **静默化后必须保留可观测失败信号**：为"不向 QQ 刷技术状态"而清空 cron 入口脚本 stdout 后，失败/漏推会变成双重静默——`status=ok` + `not-delivered` 都读不出真问题，可连续数天无人察觉。因此入口脚本静默时必须把结果写日志（失败记 ERROR），且每次排查"没收到推送"先查**报告产物文件 mtime**与脚本日志是否当日更新，而非只看 cron 状态（status=ok 只证明命令跑完，不证明生成/推送成功）。
5. **门面调度器接管既有 skill 定时任务时，必须让微技能真跑产物生成（子进程独立执行生成脚本并落盘），不得依赖"旧产物文件已存在"作旁路**；旁路会让任务 status=ok 但产物停滞（实例：切门面调度器后 4 天 report mtime 停在旧值、报告未重新生成也未推送）。切换后首个触发点前，手动带 env 实跑一次并确认产物 mtime 推进。

## 📅 定时报告接入门面调度器（2026-10-05 沉淀）

给门面/调度器加"定时出报告"时，**登记配置 ≠ 生效**——必须把三件都做全并各验一次：
2. `openclaw cron add` 真正建 job：`--command-argv '["bash","..."]'`（JSON 数组串）或 agentTurn message 调 `entry.py --schedule <workflow名>`；`--channel qqbot --to <open_id>` 固定推送目标（别走 `last`，会 fail-closed 静默失败）
3. **实跑一次 `entry.py --schedule <workflow名>` 确认出报告**（exit=0）再算接完

高频数据（日更指标/行情）才配 daily；决策类/慢变量类按数据频率分层 weekly/monthly，避免 QQ 重复刷屏——频率由底层数据更新节奏定，不是越多越好。

## 📡 多源采集原则（2026-09-30 新增，官家定，永久）

**数据源只能多不能少、不能限制。信息源包括不限于网站、公众号、官方、研报等所有合理渠道。源越多交叉验证越充分，结论越接近真实。**
- 单源会滞后 + 视角单一 → 多源并行 + 交叉验证；≥2 独立源一致 = high 置信，单源标"待确认"
- 新渠道一律"加"不"删"，不通的源占位保留（失败隔离，单源挂不影响整体）
- JS 渲染源（财联社/东财快讯）纯 requests 抓不到正文 → 用能直接返回文本的源（新华社/金十/公众号 mp.weixin 直采）替代，不硬凑
- 数据源失败一律降级占位，**禁止硬造数据**，主流程不崩
