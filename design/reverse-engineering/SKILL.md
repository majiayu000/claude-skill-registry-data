---
name: reverse_engineering
description: 對指定既有專案先按 Phase 03→02→01 逆向蒐證，再將候選結果遞回正向 Phase 01→02→03 SSOT；保留來源、信心與待決契約，按關卡推進 04→06。
---

# 逆向工程主控 Skill

## 範圍與順序

先鎖定使用者指定的專案根目錄；同一資料夾中的其他專案不得混入。保留既有逆向產物，新增資料夾承接新案例。

1. **Phase 03 Reverse**：盤點實際入口、路由、類別與函式、外部依賴和資料庫使用。記錄檔案及行號，區分已觀察、推測、未知。
2. **Phase 02 Reverse**：從證據建立 API 契約、架構、ER／類別／使用案例／順序／操作流程圖。每條邊、角色及欄位都要能回指來源；沒有證據時標記候選或未知。
3. **Phase 01 Reverse**：按使用者操作與業務能力整理需求、SRS、Gherkin 和追溯關係。記下使用者文件與程式現況的衝突，不以現況推定應有行為。
4. **正向 Phase 01**：將逆向候選與補充文件導入專案根 `specs/executable_spec.yaml`，同步 `requirements.feature`、`system_specification.md`、`traceability_matrix.md`。每項 REQ 保留證據、信心、決議與核准狀態。使用專案既有同步器及 `check_spec_integrity.py` 檢查。
5. **正向 Phase 02→03**：從已核准需求逐階段形成設計、實作差異及驗證依據。逆向清單只是候選；未核准或未驗證時保留 `pending`，不能自動填 `evaluator.passed=true` 或 Baseline。
6. **正向 Phase 04→06**：按既有階段關卡處理測試、部署、運維。子 Skill 04～06 可先整理已有檔案的靜態清單，但不得將清單或圖表當成執行、發布或營運驗證。

`@reverse [專案路徑]` 執行前三步並建立可追溯的正向交接資料；`@reverse-code`、`@reverse-design`、`@reverse-requirements` 只執行指定逆向步驟。04～06 子 Skill 在各階段進入正向工作時使用，或依使用者明示要求只做既有素材盤點。

## 入口到結果的追蹤

對每個重點 API／使用者操作，追蹤 UI／Razor／JavaScript 觸發 → HTTP 路由與 Controller 分支 → Service／函式庫 → 資料存取或外部服務 → Session／Cookie／Token／回應或 Redirect。列出條件、呼叫先後、錯誤與副作用；操作手冊提供可依序執行的前置條件、請求、回應及失敗處理。缺少程式或執行證據時明示界限。

## 產物與狀態

`outputs/phase_03_reverse/`、`phase_02_reverse/`、`phase_01_reverse/` 存放逆向證據與候選規格。輸入、必需與可選輸出依 `io_files/phase_0N_reverse_io.yaml`；例如只有表名時 `db_schema_raw.sql` 可以缺席，不能捏造 DDL。專案根四規格才是正向 SSOT。若既有逆向報告把 Phase 01～03 記為「逆向完成」，該字樣僅代表蒐證步驟，不代表正向 Evaluator 或業務核准通過。

新增證據時，先對齊 REQ ID、來源指紋及衝突，再更新 YAML 主體，重新產生衍生文件並執行靜態完整性檢查。業務契約未決時，文件整理繼續，決議與執行驗證保持待確認；到實際關卡才依 `.agents/AGENTS.md` 的 Evaluator 和 SSOT 規則建立 Baseline。

在 `@reverse` 開始及交接時執行 `python scripts/check_reverse_skill_integrity.py --project "<專案目錄>"`，再依 `.agents/AGENTS.md` 執行該專案的 A／B／C／D／S 四規格檢查；兩者分別核對 Skill／IO／逆向產物與正向 SSOT。

## 六個子 Skill

| 子 Skill | 用途 |
|---|---|
| `phase_03_code_restore` | 程式、路由、函式呼叫與資料使用蒐證 |
| `phase_02_design_restore` | 設計與 API／UML 候選還原 |
| `phase_01_requirements_restore` | 需求、SRS、情境與追溯還原 |
| `phase_04_test_restore` | 已有測試盤點；正向關卡下才執行測試 |
| `phase_05_deploy_restore` | 既有部署配置盤點；正向關卡下才發布 |
| `phase_06_ops_restore` | 既有營運配置盤點；正向關卡下才驗證運維 |

每個子 Skill 的細節及 IO 契約見同目錄 `sub_skills/`、`io_files/`。例如 `Demo Project 3/forward_transition.md` 記錄一次完整的逆向→正向交接與未決閘口。
