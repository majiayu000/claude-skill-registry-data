---
name: workflow-skill-router
description: 當 Claude Code 任務需要依 single、phased 或 managed-goal 模式選擇正確 SKILL、逐階段重新路由，或尊重使用者指定 SKILL 與輔助能力同意時使用。
---

# Workflow Skill Router V2（Claude Code）

## Claude Code 環境

- 本 Plugin 的 MCP 工具在 Claude Code 中名為 `mcp__plugin_workflow-skill-router_workflow-skill-router__<tool>`，例如 `plan_work`、`propose_support_consent`、`get_router_status`。以下只寫工具短名。
- Claude Code 沒有 native Goal。`goal_binding_id` 一律傳 `null`，不可自行推定 `progress` 或 `steer`；長期、可恢復的工作只能使用 Router-owned work graph（`get_next_work`、`record_work_event`、`evaluate_gate`），結果都是 `authority_mode=router-local` 的 advisory 狀態。
- 目前環境可觀測的能力，是 Claude Code 在對話中列出的 skills（Plugin skill 以 `plugin:skill` 命名）、MCP 工具與 subagents。列出只代表可見，不代表已啟用或已授權；需要啟用 skill 時使用 Skill 工具。
- Workspace Profile 先讀目前 workspace 的 `.claude/workflow-skill-router.json`，不存在時才讀 `.codex/workflow-skill-router.json`。參考文件寫的 `.codex/` 是 Codex 的原生位置。Personal Profile 與本機狀態和 Codex 共用同一個外部資料目錄。
- 所有寫入、執行、傳訊與部署仍由 Claude Code 的 permission mode、approval 與 sandbox 控制；SKILL 同意不等於工具權限。

## 路由規則

先解析 Goal relation：`progress`、`steer`、`status`、`side-question`、`unrelated` 或 `none`。`status` 只讀狀態，不建立工作；`side-question` 與 `unrelated` 不修改 Goal semantic revision。

再選 envelope：單一意圖用 `single`；有兩個以上相異階段用 `phased`，每個 Phase 重新選擇能力；長期、可恢復、跨 repo 或 dependency DAG 用 `managed-goal`，每個 Work Item 再分成 `single` 或 `phased`。

外層 workflow envelope 與目前 Phase／Work Item 的範圍分開判斷。已有明確 `phased` 或 `managed-goal` 上下文時，只處理目前 Phase 不代表把外層改成 `single`。`managed-goal` 是工作組織方式，不代表已有 Native Goal 綁定；未提供既有 Goal 時，`goal_relation` 為 `none`，不可自行推定 `progress`。

在開始實作或呼叫工具前，先明確宣告本次預計使用的 SKILL 與各自用途。

使用者未指定 SKILL 時，Router 自動選擇最小且足以完成工作的 Primary／Supporting SKILL 組合，不為 Router 自己推薦的輔助 SKILL 額外詢問同意；仍須遵守最小路由、能力可用性與 host 權限邊界。

使用者未在當次請求指定 SKILL 時，先解析 Personal Routing Profile。固定優先序是「使用者當次明確指定 SKILL > workspace profile > personal profile > built-in」；system、developer、safety 與 host hard constraints 永遠不能被 Profile 覆寫。Workspace Profile 位置見上方「Claude Code 環境」；personal profiles 放在 Router 外部資料根目錄的 `profiles/personal/*.json`（Windows `%LOCALAPPDATA%\Codex\workflow-skill-router`、macOS `~/Library/Application Support/Codex/workflow-skill-router`、Linux `${XDG_STATE_HOME:-~/.local/state}/codex/workflow-skill-router`），不放在 Plugin cache。Plugin/MCP 負責 deterministic loading；MCP 不可用時只有在 host filesystem access 能讀取固定位置時才能 advisory 套用，並必須標示 `skill-only-fallback`。Profile 只能宣告 matcher、work mode、Phase、Primary、最多三個 immediate support 與 exit gate ID，不得包含自由形式 instructions。Workspace 與 personal 同時匹配時採用 workspace 的完整 Skill Tree，不做隱含 deep merge。

Profile 命中代表 `intended-unverified` 路由偏好，不代表能力已安裝、已曝光、已授權或可啟用；Runtime Capability Discovery 仍是 activation gate。Profile 宣告的 canonical Skill 不可用時保留 intended Skill 並誠實標示 unavailable／degraded，不得靜默改選。Profile 自動路由不額外詢問輔助 SKILL 同意；但只要使用者當次明確指定 SKILL，Profile 必須讓位，任何額外支援仍回到 scoped consent 規則。

選擇前先讀 capability descriptors 的 `description、domains、stages、availability`，不要只靠名稱猜測。Primary 是負責目前決策瓶頸或第一個可執行 Phase 的 SKILL；Supporting SKILL 只保留目前 Phase 與 immediate exit gate 不可缺少的能力。固定輸出配方是「目前 route = 目前 Phase Primary + immediate exit gate support」；只有必須在目前 Phase 結束前實際啟用的能力，才可列入 support_skills。定義、描述或規劃 exit evidence 不等於啟用 verification SKILL；若 Primary 能自行完成目前 Phase 與 exit gate 定義，support_skills 必須為空。未來 Phase 的能力只記在 phase plan，未來 Phase 的能力不得提前列入目前 support_skills。Phase transition 後建立新 route，不沿用或聚合舊 route。`managed-goal` 以目前 Work Item 的規劃或執行瓶頸決定 Primary；Goal 規劃 Work Item 只選規劃本身需要的能力，未來 Work Item 的 SKILL 只能記在計畫，不得聚合成目前 support_skills，進入該 Work Item 時重新路由。除非任務本身是在維護 Router，否則不得把 workflow-skill-router 自己當成預設 Primary。

`availability` 是 activation gate，不是 semantic selection filter。已驗證 snapshot 指定必要 canonical Skill 時，該 Skill 仍是 intended `primary_skill`；這會保留 intended SKILL 與需求。activation 標成 unavailable／degraded，fallback 只寫在說明中。fallback 不得改寫 primary_skill 或塞入 support_skills。

使用者指定 SKILL 時先鎖定指定項目。只有此情境下，Router 想加入任何額外 SKILL、Plugin 或 MCP 支援角色，才要先說明用途、scope、拒絕後限制與 context cost，取得同意後才能讀取或啟用。Consent route 採固定狀態配方：`proposal-required` 時，support_skills 必須列出具體提案集合，這些項目在 `approved` 前只是 proposed，不是 activated；`approved` 時保留相同 support_skills；`rejected` 時清空 support_skills。使用者拒絕時只能使用指定能力、限縮成果或誠實阻塞，不可靜默替代。

使用者對既有提案回覆同意或拒絕時，這是同一個 Phase 的 consent state transition，不是新的任務，也不得重新做 semantic routing。若 `propose_support_consent` 與 `transition_support_consent` 可用，提出詢問前先以 `propose_support_consent` 持久化目前 Phase 的 concrete support set；收到回覆後只分類 `approved`、`rejected` 或 `unclear` intent。只有明確同意或拒絕才能呼叫 `transition_support_consent`，而且 transition request 不得帶入新的 primary、support set、envelope 或 Goal relation。使用 MCP 回傳的 bound route 作為唯一結果，不可自行重建。

若 intent 為 `unclear`，保持 proposal pending 並釐清，不得推定同意。若 MCP 回報 Phase、scope、Goal revision、plan revision 或 context fingerprint 漂移，必須 fail closed 並重新評估具體提案。只有在 `skill-only-fallback` 才能依上一個 assistant route 做 instruction-level transition；此結果是 advisory，不能宣稱 durable consent enforcement、CAS 或 `hybrid-full`。

若 MCP 可用，使用 capability snapshot、route validation、state/gate 與 evidence。若 MCP 不可用（例如找不到 Python 3.11+ 或 Node.js 24+），明示目前是 `skill-only-fallback`：沒有 durable resume、CAS、完整 drift detection 或 sealed activation instrumentation；不得宣稱 `hybrid-full`，也不得把不可觀測項目算成通過。

所有 R2/R3 行動仍由 Claude Code 的 permission、approval 與 sandbox 控制；SKILL 同意不等於安裝、寫入、部署、傳訊或 production access 授權。

完成工作時，列出本次實際使用的 SKILL；若與執行前宣告不同，要簡短說明新增、移除或替換原因。

若任務需要套用、建立、遷移或說明自訂 Skill Tree，讀取 [Personal Routing Profiles](references/personal-routing-profiles.md)。其他情況依需要讀取 [routing protocol](references/routing-protocol.md)、[Goal protocol](references/goal-protocol.md) 或 [evaluation boundary](references/evaluation-boundary.md)，不要一次載入全部參考資料。
