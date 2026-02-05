---
name: requirements analysis
description: Waterfall Phase 1 - Requirements Analysis (需求分析)
---

# Phase 1: Requirements Analysis

## Gate: 必須完成需求文件才能進入下一階段

1. Gather Requirements
   User, 請描述您的需求。我會幫您整理成正式的需求文件。

2. Create Requirements Document
   ```bash
   mkdir -p docs/specs
   touch docs/specs/FEATURE_NAME-requirements.md
   ```

3. Document Requirements
   I will create/update `docs/specs/FEATURE_NAME-requirements.md` with:
   - User Stories
   - Acceptance Criteria
   - Non-functional requirements

4. Create Gherkin Feature Files (框架)
   ```bash
   mkdir -p e2e/features
   ```
   I will create `.feature` files with:
   - Feature description (As a... I want... So that...)
   - Scenario titles only (不含 Given/When/Then 細節)
   
   範例：
   ```gherkin
   Feature: Blog CMS
     As a blogger
     I want to create posts
     
     Scenario: Create a new blog post
     Scenario: Publish a draft post
   ```

5. Review Gate
   User, 請審閱：
   - `docs/specs/requirements.md`
   - `e2e/features/*.feature` (Scenario 標題)
   
   **您必須明確說「需求批准」才能進入 Phase 2 (系統設計)。**
   ⚠️ 進入下一階段後，需求將被凍結。
