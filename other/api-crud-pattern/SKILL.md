---
name: api-crud-pattern
description: >
  API backend CRUD 작업 전 domain shape, endpoint baseline, delete/restore,
  recursive delete, identifier, projection, conflict policy, scoped/tree
  resource를 점검하는 스킬. CRUD API 구현, CRUD plan, API CRUD 검토,
  resource CRUD 추가, admin CRUD, soft-delete, restore endpoint,
  recursive delete, scoped resource, tree resource, REST resource design,
  add CRUD endpoint, CRUD review, CRUD API pattern, delete semantics,
  identifier surface, response projection, conflict policy, "CRUD 패턴 확인"
  등의 요청에서 트리거.
---

# API CRUD Pattern

API backend CRUD 작업에서 구현을 바로 시작하기 전에 resource shape와 정책 결정을 정리하는 스킬.
특정 framework, ORM, module wiring, path convention을 강제하지 않는다.

## 이 스킬이 막는 실패

Agents는 CRUD를 단순 boilerplate로 보고 endpoint와 service부터 만들기 쉽다. 이 스킬은 다음 실패를 막는 데 집중한다.

- resource shape를 확정하지 않은 채 top-level CRUD처럼 구현
- soft delete, restore, conflict, recursive delete를 서로 다른 정책으로 처리
- parent scope 검증을 list에는 넣고 detail/update/delete에는 빠뜨림
- ORM entity나 내부 primary key를 API surface로 그대로 노출
- 한 resource의 예외를 고치려다 shared CRUD helper의 전역 동작을 바꿈

## 모드 선언

이 스킬이 활성되면 먼저 CRUD domain을 분류하고, 프로젝트별 결정을 확인한다.

- **Plan 보조**: CRUD 작업 plan에 빠진 domain 결정과 검증 항목을 보강한다.
- **구현 전 점검**: 구현 전에 endpoint, identifier, delete, projection, conflict 정책을 확정한다.
- **Review**: 이미 만든 CRUD API가 domain contract를 새거나 과하게 고정하지 않았는지 확인한다.

이 스킬은 구현 생성기가 아니다. 실제 코드는 현재 repo의 `AGENTS.md`, manifest, framework pattern, 기존 API를 읽은 뒤 작성한다.

## 시작 절차

1. 기존 API 관례를 확인한다.
   - 같은 repo의 유사 resource CRUD를 먼저 읽는다.
   - routing, validation, auth, pagination, error response, test style을 실제 코드에서 확인한다.

2. resource shape를 분류한다.
   - top-level, scoped, child, tree, join/config 중 무엇인지 정한다.
   - CRUD보다 attach/detach, reorder, enable/disable, archive가 domain 언어에 가까운지 확인한다.

3. 기본 정책을 결정한다.
   - public identifier와 internal primary key를 분리할지 확인한다.
   - list/detail/create/update/delete baseline이 필요한지 확인한다.
   - delete가 hard delete, soft delete, archive, deactivate 중 무엇인지 정한다.
   - restore가 필요한 domain인지 정한다.
   - recursive delete가 필요한 경우 opt-in 방식과 기본값을 정한다.
   - list/detail response projection과 relation 노출 범위를 명시한다.
   - unique conflict, not found, invalid parent scope의 error contract를 정한다.

4. 구현 범위를 좁힌다.
   - 해당 resource에 필요 없는 endpoint를 만들지 않는다.
   - framework-specific wiring은 기존 repo pattern을 따른다.
   - schema/table/field 이름은 직접 확인 전 추측하지 않는다.

## 결정 기록 포맷

구현 전 plan, 진행 메모, review 응답에는 아래 정도의 짧은 결정을 남긴다. 긴 코드 예시는 쓰지 않는다.

```markdown
CRUD shape: top-level | scoped | child | tree | join/config
Endpoint baseline: list/detail/create/update/delete 중 포함 항목
Identifier: public surface / internal lookup 기준
Delete semantics: hard | soft | archive | deactivate
Restore: needed | not needed | deferred
Recursive behavior: disallow by default | explicit opt-in | not applicable
Projection: list/detail에서 노출할 field/relation 경계
Conflict policy: unique conflict, soft-deleted row conflict, parent scope mismatch
Verification: unit/e2e/schema/client 중 필요한 확인
```

## 권장 Baseline

대부분의 admin/API CRUD에서는 아래를 baseline 후보로 본다. mandatory contract가 아니라 확인 대상이다.

| 항목             | 확인할 결정                                                 |
| ---------------- | ----------------------------------------------------------- |
| List             | pagination, sort, filter, deleted 포함 여부                 |
| Detail           | identifier 종류, parent scope 검증, relation projection     |
| Create           | required fields, unique conflict, default status            |
| Update           | partial vs full update, immutable fields, conflict handling |
| Delete           | hard/soft/archive 의미, response shape, idempotency         |
| Restore          | soft-delete domain에서 필요한지, conflict 발생 시 정책      |
| Recursive delete | tree/child resource에서 opt-in인지, 기본 차단인지           |

## High-Signal Checklist

### Domain Contract

- resource가 독립 entity인지, parent에 종속된 entity인지 먼저 구분한다.
- public API surface에서 어떤 identifier를 받는지 정한다.
- parent scope가 있으면 모든 read/write/delete 경로에서 같은 scope 검증을 적용한다.
- soft-deleted row가 list/detail/create conflict에 어떤 영향을 주는지 정한다.
- delete가 되돌릴 수 없는 동작이면 기본 endpoint에서 recursive/cascade를 암묵 실행하지 않는다.

### Endpoint & Response

- baseline endpoint는 domain에 맞을 때만 만든다. CRUD 이름에 끌려 불필요한 update/delete를 만들지 않는다.
- response projection은 명시한다. ORM entity 전체를 그대로 노출하지 않는다.
- create/update/delete의 status code와 body 유무는 repo 관례를 확인한 뒤 맞춘다.
- error code/message는 client가 분기할 수 있을 만큼 안정적으로 둔다. 단, 보안 정책상 숨겨야 할 scope mismatch는 기존 정책을 따른다.

### Scoped & Tree Resource

- scoped resource는 list/detail/update/delete 모두에서 같은 parent scope를 검증한다.
- child resource 삭제 시 parent aggregate의 상태, count, ordering이 필요한지 확인한다.
- tree resource는 cycle 방지, 자기 자신 하위로 이동 방지, depth/path 갱신 책임을 명시한다.
- recursive delete/restore는 opt-in으로 두고 영향 범위를 검증 가능하게 만든다.
- subtree 조회가 필요하면 default depth와 `includeChildren`류 옵션의 비용을 먼저 확인한다. 비용을 모르면 기본 노출하지 않는다.

### Validation & Conflict

- unique constraint는 active row 기준인지, soft-deleted row까지 포함하는지 확인한다.
- create가 soft-deleted row와 충돌할 때 restore 유도, conflict 반환, 새 row 생성 중 하나를 정한다.
- update에서 immutable identifier, parent 변경, status 변경을 허용할지 분리한다.
- not found와 out-of-scope는 보안상 같은 응답으로 숨길지, 다른 error code로 줄지 프로젝트 정책을 따른다.

### Verification

- happy path만 있으면 부족하다. 최소한 conflict, not found, scope mismatch, delete/restore 정책 중 해당 domain에 걸리는 항목을 검증한다.
- OpenAPI/client generation이 있는 repo라면 schema 노출과 generated client diff를 검증한다.
- migration or schema 변경이 있으면 table/column/index 이름을 실제 DB schema와 대조한다.

## Review 질문

리뷰 시 아래 질문에 답하지 못하면 구현을 넓히기 전에 멈춘다.

- 이 resource는 top-level, scoped, child, tree 중 무엇인가?
- delete는 되돌릴 수 있는가?
- recursive/cascade 동작은 명시적 opt-in인가?
- public identifier와 internal identifier가 섞이지 않았는가?
- list/detail projection이 의도하지 않은 field나 relation을 노출하지 않는가?
- unique conflict가 soft-deleted row와 active row를 구분하는가?
- parent scope를 우회하는 detail/update/delete 경로가 없는가?
- test가 happy path 외 conflict, not found, scope mismatch를 덮는가?

## Gotchas

- **5 endpoint를 무조건 만들지 말 것**: CRUD처럼 보여도 domain language가 enable/disable, attach/detach, reorder이면 그 동작을 endpoint로 드러내는 편이 낫다.
- **soft delete를 delete endpoint 하나로 끝내지 말 것**: list/detail 기본 조회에서 제외되는지, create conflict에서 어떻게 동작하는지까지 같이 정해야 한다.
- **restore를 자동으로 가정하지 말 것**: restore는 user-facing workflow, audit, conflict policy가 있을 때만 추가한다.
- **recursive delete를 기본값으로 두지 말 것**: parent 삭제가 child 삭제를 암묵 수행하면 영향 범위 검증과 사용자 확인이 어려워진다.
- **shared CRUD helper를 먼저 고치지 말 것**: 한 resource의 경계 조건을 고치려다 모든 CRUD behavior를 바꿀 수 있다. call site나 option으로 격리할 수 있는지 먼저 본다.
- **path convention을 스킬에서 고정하지 말 것**: nested path, query param, header, body 중 무엇을 쓸지는 기존 API 관례와 client ergonomics로 결정한다.
- **schema 이름을 추측하지 말 것**: DB query나 migration 전 실제 table, column, index, relation 이름을 확인한다.
