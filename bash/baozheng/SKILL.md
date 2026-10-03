---
name: baozheng-skills
description: 一站式法律服务平台 — 专业法律咨询 + 要素式/通用起诉状起草 + 刑事专项材料辅助 + 法条分析与法规检索。flk.npc.gov.cn API实时法条优先，不可用时AI知识库降级兜底；以22类法律领域覆盖矩阵约束路由边界；支持35个起诉状模板、5类刑事专项材料辅助；内置Logic Doctor逻辑自检、诉讼时效追踪及10类异常容错处理（含连续失败熔断）；渐进式意图收敛协议（3轮状态机）；混合意图自动任务拆解（按依赖排序→合并→顺序执行）。非标准案由自动使用通用模板。
version: 1.0.1
---

# 包拯 skills 公正廉明包青天,浩然正气满乾坤

## 触发条件 / 不处理边界
触发：中国法律问题咨询、起草起诉状、分析法条、检索法规、刑事基础咨询、刑事控告材料、取保候审申请、刑事辩护意见要点、刑事附带民事、羁押家属沟通、专利侵权、商业秘密、公司解散清算、政府信息公开、涉外送达、消费权益、退一赔三、食品安全、预付卡、网暴、人格尊严、名誉权、隐私权、互联网纠纷、建设工程款。
不处理：非中国法律、执行具体诉讼代理。

## 分级加载
- L1（本文件）：路由表 + 边界说明
- L2（references/）：子技能详细指令，Agent 按路由命中后按需读取

## references 索引

### 子技能
| 文件 | 用途 | 加载条件 |
|:---|:---|:---|
| module-a-consultation.md | 模块A：法律咨询（4步深度分析流程） | 法律问答、纠纷咨询 |
| module-b-complaint.md | 模块B：要素式起诉状（35模板，含民事/行政） | 起草起诉状 |
| module-c-analysis.md | 模块C：法条分析+法规检索（C0-C3） | 分析法条/检索法规 |
| module-d-criminal.md | 模块D：刑事专项材料辅助（5类材料） | 刑事咨询、刑事控告、取保候审、辩护意见要点、附带民事、羁押沟通 |

### 公共模块（跨子技能复用）
| 文件 | 用途 |
|:---|:---|
| shared-statute-engine.md | 法条检索策略（flk.npc.gov.cn API 优先 + AI 知识库降级兜底） |
| shared-error-handling.md | 10类异常容错处理（含连续失败熔断） |
| shared-limitation-periods.md | 诉讼时效速查 |
| shared-disclaimer.md | 全局免责声明 |
| shared-activation-rules.md | 强制激活规则（本Skill优先于通用大模型知识） |
| shared-category-coverage.md | 22类法律领域覆盖矩阵与升级缺口 |
| shared-intent-convergence.md | 渐进式意图收敛协议（3轮状态机+置信度+上下文传递） |
| shared-task-decomposition.md | 自动任务拆解（混合意图→依赖排序→合并→顺序执行） |

### 案由速览（B模块依赖，35个模板）
case-00-general-civil.md / case-01-private-lending.md / case-02-divorce.md / case-03-sales-contract.md / case-04-financial-loan.md / case-05-property-service.md / case-06-credit-card.md / case-07-traffic-accident.md / case-08-labor-dispute.md / case-09-finance-lease.md / case-10-guarantee-insurance.md / case-11-securities-fraud.md / case-12-inheritance.md / case-13-administrative.md / case-14-medical-dispute.md / case-15-real-estate.md / case-16-company-equity.md / case-17-construction-contract.md / case-18-intellectual-property.md / case-19-personality-internet.md / case-20-land-demolition.md / case-21-environmental-protection.md / case-22-foreign-related.md / case-23-insurance-claim.md / case-24-fund-investment.md / case-25-private-fund.md / case-26-trust-dispute.md / case-27-house-lease.md / case-28-personal-injury.md / case-29-patent-dispute.md / case-30-trade-secret.md / case-31-company-dissolution.md / case-32-government-info.md / case-33-foreign-service.md / case-34-consumer-rights.md

## 子任务路由表（L1概览，实际执行以下方"路由与意图收敛"为准）
> 本表仅用于 L1 快速概览意图与模块的对应关系。实际路由决策（直跳/收敛/混合意图）按下方收敛协议执行。
| 意图 | 触发词 | 加载文件 | 输出 |
|:---|:---|:---|:---|
| 法律咨询 | 咨询/怎么办/合法吗/能不能/赔多少 | module-a-consultation.md | 法律分析报告 |
| 起草起诉状 | 起诉/打官司/起诉状/告他/立案 | module-b-complaint.md | 起诉状.docx |
| 分析法条 | 分析这条法律/拆解法条/构成要件 | module-c-analysis.md (C1) | 6维度分析 |
| 法规检索 | 检索法规/涉及哪些法条 | module-c-analysis.md (C2) | 6份交付物 |
| 财税法规 | 税务/增值税/企业所得税 | module-c-analysis.md (C3) | 财税报告 |
| 刑事材料辅助 | 刑事/罪名/量刑/控告/取保候审/强制措施/辩护意见/附带民事/羁押/拘留/逮捕 | module-d-criminal.md | 刑事基础分析/材料清单/5类文书草稿 |
| 消费权益 | 消费/退一赔三/食品安全/预付卡/虚假宣传/七天无理由 | module-b-complaint.md (case-34) | 消费权益纠纷起诉状 |
| 类别覆盖判定 | 婚姻家庭/公司企业/房产/医疗/行政/知识产权/涉外等 | shared-category-coverage.md | 当前承接等级/主路由/升级缺口 |

## 路由与意图收敛
| 意图清晰度 | 处理方式 |
|:----------|:--------|
| 清晰（含领域专有词+行为词） | 直跳目标模块 |
| 模糊（缺领域或意图） | 启动 `shared-intent-convergence.md` 3轮收敛协议 |
| 混合（多意图） | 询问用户偏好，按选择路由（不使用固定优先级） |
| 3轮未收敛 | 兜底路由 module-a |

状态机: S_SKIP(直跳) → S_R1(领域) → S_R2(意图) → S_R3(细节) → S_DISPATCHED(派发)
安全边界触发 → 暂停确认。

## 长任务协议
模块C六步工作流按 Init-Step-Poll 执行（详见 module-c-analysis.md）：
Init：确认检索主题，步骤1+2并行启动；Step：步骤3→4→5→6串行验证；Poll：每步输出进度。
模块A/B/D 步骤较少，按步骤自然推进，每步完成简述进展（如"已完成步骤2/5：法律依据梳理"），无需 Init-Step-Poll；模块D 的 D10 Logic Doctor 自检结果以清单附在输出末尾。

## 依赖安装
技能首次激活时，CodeBuddy 自动检测 `requirements.txt` 并安装缺失的包：
```bash
pip install -r requirements.txt
```
外部依赖：`requests`（flk API 客户端）、`python-docx`（DOCX 生成，缺失时自动降级为纯标准库输出）。

## 安全边界
- 法条引用优先通过 `scripts/flk_npc_client.py` 调用 flk.npc.gov.cn API 获取实时数据，API 不可用时降级到 AI 训练知识库并标注来源
- 起诉状标注"建议由执业律师审核后提交"
- 模块A/B/C/D的最终输出均必须附加 `shared-disclaimer.md` 的免责声明要点
- 失败回退参见 shared-error-handling.md（10类异常容错处理，含连续失败5次熔断）
