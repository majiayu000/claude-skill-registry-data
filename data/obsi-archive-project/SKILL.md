---
name: obsi-archive-project
description: 완료된 프로젝트를 검증(Dependency Check), 정리(Cleanup) 후 안전하게 연도별 아카이브로 이동시킵니다.
---

# Expert Archive Project Workflow

프로젝트 종료 절차(Closing Ritual)를 수행하여 시스템 무결성을 유지하고 아카이빙합니다.

### 1단계: 사전 검증 (Pre-flight)
1.  **Context Loading**: `this document`를 읽어 종료 절차를 확인합니다.
2.  **Dependency Scan**: 다른 프로젝트에서 이 프로젝트를 링크하고 있는지 확인합니다.
3.  **Knowledge Check**: "지식 베이스로 옮길 노트가 있습니까?" (`obsi-knowledge-harvester` 제안).

### 2단계: 정리 (Cleanup)
1.  **Sanitize**: `.DS_Store`, 빈 폴더를 정리합니다.
2.  **Status Tag**: `#status/active` 태그를 `#status/done`으로 변경합니다.

### 3단계: 이관 (Move)
1.  **Manifest Creation**:
    *   `resources/manifest-template.md`를 사용하여 `_archive_meta.md`를 생성합니다. (종료 사유 등 기록)
2.  **Archive**:
    *   `90_Archives/Projects/{YYYY}/`로 폴더를 이동합니다.
3.  **Index Update**: `10_Projects` 목록에서 제거하고 Archive 목록에 추가합니다.

---

## Standards & Rules

# Archive Project Standards

## Purpose
To move completed work out of sight but keep it accessible (`90_Archives`), ensuring the active workspace remains focused.

## Closing Rituals (The Checklist)
1.  **Dependency Scan**: Ensure no external files link *into* this project.
2.  **Status Update**: Change `#status/active` to `#status/done`.
3.  **Knowledge Harvest**: Before archiving, extract valuable assets to `20_Learning` using `obsi-knowledge-harvester`.
4.  **Cleanup**: Delete `.DS_Store`, empty folders, and temp files.

## Archival Rules
- **Destination**: `90_Archives/Projects/{YYYY}/{Project_Name}`
- **Manifest**: Every archived project must have `_archive_meta.md` explaining *why* it was closed.
