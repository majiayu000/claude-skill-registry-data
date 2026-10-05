---
name: commit-regroup
description: >
  로컬에만 있는(아직 push 안 한) 잘게 쪼개진 여러 커밋을 논리 단위 몇 개로 다시 묶는다.
  rebase 재정렬 대신 soft-reset + path 재배치로 충돌 없이 재구성하고,
  최종 트리가 원본과 byte-identical인지 검증해 코드 무변경을 보장한다.
  "커밋 묶어줘", "로컬 커밋 grouping", "커밋 정리해줘", "커밋 합쳐줘",
  "커밋 재구성", "스쿼시로 정리", "push 전에 커밋 정리해줘",
  "group local commits", "regroup commits", "squash into logical commits",
  "tidy commits before push", "consolidate local commits" 등에서 트리거.
  단일 커밋 메시지 작성은 commit-msg, worktree squash 시점 판단은 worktree-lifecycle.
---

# Commit Regroup

`origin/<branch>..HEAD`의 잘게 나뉜 로컬 커밋을 논리 단위 몇 개로 다시 묶는 스킬.
이미 끝난 작업의 **히스토리만** 재구성한다 — 코드 변경 내용은 1바이트도 바꾸지 않는다.

## 언제 이 스킬인가

- 로컬 커밋이 remote보다 여러 개 앞서 있고, 그대로 push하면 log가 지저분할 때.
- worktree squash가 아니라 develop/feature에 직접 쌓인 잡다한 커밋을 push 전에 정리할 때.
- 구분: 메시지 후보만 필요하면 commit-msg. worktree→develop squash 시점 판단은 worktree-lifecycle.
- 대상은 **아직 push 안 한** 로컬 커밋만. push된 커밋 rewrite는 공유 히스토리를 깨므로 이 스킬 밖이다.

## 핵심 결정: soft-reset 재배치 > rebase 재정렬

두 방법이 있고, 대부분 soft-reset이 이긴다:

- **rebase 재정렬/fixup**: 커밋별 diff는 보존하되 같은 feature 커밋을 인접하게 옮겨야 한다. 생성 파일(`openapi.json`, lockfile, route tree)·여러 feature가 공유한 파일에서 **충돌이 다발**한다. 환경에 따라 `git rebase -i` 자체가 막혀 있기도 하다.
- **soft-reset + path 재배치** (기본 추천): `git reset <base>`로 최종 트리만 남기고, 변경 파일을 버킷별로 다시 add+commit. **재정렬이 없어 충돌 0**. 비용은 (a) 원본 메시지 폐기·재작성, (b) 한 파일을 여러 feature가 건드렸으면 한 커밋에만 귀속.

feature가 서로의 파일을 리팩터(리네임 등)하며 얽혀 있을수록 soft-reset이 유일하게 깨끗하다 — rebase는 그 지점에서 코드 충돌을 만든다. 커밋별 diff 보존이나 bisect 가능성이 꼭 필요할 때만 rebase를 고려한다.

## 불변식: 최종 트리 = 원본 트리

재구성 전후 트리 해시가 같아야 한다. 이게 "코드는 안 건드리고 묶기만 했다"의 유일한 증거다.

```bash
git rev-parse 'HEAD^{tree}'   # 시작 전 기록
# ... 재구성 후 ...
git rev-parse 'HEAD^{tree}'   # 같아야 함
```

다르면 재구성이 잘못된 것이다. 커밋을 남겨두고 `git diff --stat <orig-head> HEAD`로 원인을 본 뒤, `git reset --hard <orig-head>`(원본은 reflog에 보존)로 되돌리고 분류를 고친다. `scripts/regroup.sh`는 이 검증을 자동으로 하고 실패 시 롤백 명령을 출력한다.

## 워크플로우

1. **상태 확인**: `git status --short --branch`, `git log --oneline origin/<branch>..HEAD`. tracked unstaged/staged 변경이 있으면 먼저 정리한다(untracked은 무방 — 건드리지 않는다).
2. **버킷 설계**: 커밋을 `git show --stat`으로 훑어 논리 트랙으로 나눈다. 트랙 1개 = 최종 커밋 1개. 의도/추천을 사용자와 합의하고, 히스토리 rewrite라 실행 전 한 번 확인받는다.
3. **파일 분류 (reset 전 dry-run)**: `git diff --name-status -M origin/<branch> HEAD`의 **모든** path를 정확히 한 버킷에 배정한다. 리네임 `R old new`는 old·new **둘 다** 같은 버킷에. first-match-wins로 구체 패턴을 광범위 패턴보다 위에 둔다. **UNCLASSIFIED 0**과 전수 커버리지를 reset 전에 확인한다 — reset 후에 누락을 발견하면 트리가 깨진다.
4. **실행 + 검증**: `scripts/regroup.sh`에 base·분류 매핑·버킷별 커밋 메시지(순서=커밋 순서)를 넘긴다. 스크립트가 완전성·precondition을 검사하고 reset → 버킷별 add+commit → 트리 동일성 검증까지 한다.
5. **보고**: 새 log + 트리 PASS + 롤백 지점(`<orig-head>`)을 알린다. **push는 하지 않는다** — CI/배포 트리거라 사용자 몫이다.

## 분류기 패턴

버킷 규칙은 매 작업마다 실제 파일 기준으로 새로 짠다(고정하지 않는다). 일회용 분류기로 매핑을 뽑는 게 빠르고 검증 가능하다:

```bash
# 각 path → bucket. 구체 패턴을 위에, 광범위 패턴을 아래에 (first-match-wins).
classify() { case "$1" in
  */pose-logs/*)           echo featureA ;;   # 광범위 dir보다 먼저 매칭돼야 함
  */features/api-keys/*)   echo featureB ;;
  apps/api/openapi.json)   echo featureA ;;   # 생성 파일 → 우세 버킷에 통째로
  package.json|turbo.json) echo misc ;;
  *)                       echo UNCLASSIFIED ;;
esac; }

git diff --name-status -M origin/<branch> HEAD | awk -F'\t' '
  $1 ~ /^R/ { print $2; print $3; next }   # rename: old+new 둘 다
  { print $2 }' | while read -r p; do printf '%s\t%s\n' "$(classify "$p")" "$p"; done
```

UNCLASSIFIED가 0인지 먼저 확인하고, `bucket<TAB>path` 매핑과 `bucket<TAB>subject` 메시지 파일을 `scripts/regroup.sh`로 넘긴다(사용법은 스크립트 상단 주석).

**스크립트 없이 수동**: `git rev-parse 'HEAD^{tree}'` 기록 → `git reset <base>` → 버킷별 `git add -A -- <paths>` + `git commit` → 트리 해시 재비교.

## Gotchas

- **중간 커밋은 단독 빌드 불가**: cumulative diff를 path로 쪼개면 *마지막 커밋(또는 전체)* 에서만 트리가 완결된다. 한 커밋이 아직 없는 다른 커밋의 심볼을 참조할 수 있다. `git log` 정리엔 무해하나 `git bisect` 대상이면 의미 있는 제약 — 보고에 명시한다.
- **공유·생성 파일 귀속**: `openapi.json`·lockfile·`todo.md`·여러 feature가 만진 컴포넌트는 path로 못 쪼갠다. 최종 블롭을 우세 버킷에 통째로 넣고, 커밋 attribution이 살짝 어긋남을 기록한다(트리는 항상 정확). hunk 단위로 쪼개려 `git add -p`에 의존하지 말 것 — 비용 대비 이득이 작고 일부 환경에선 interactive가 막힌다.
- **리네임은 old+new 한 쌍**: `R old new`에서 old(삭제)와 new(추가)가 다른 버킷에 가면 rename이 깨진다. 분류 규칙을 양쪽에 적용해 같은 버킷으로 보낸다. `git add -A -- <path>`가 M/A/D/rename을 일괄 처리한다 — `git add <path>`는 삭제를 못 잡으니 `-A`를 쓴다.
- **untracked은 그대로 둔다**: reset은 untracked을 안 건드린다. `git add .` 대신 버킷 path만 명시해 미추적 파일·다른 사람이 미리 staged한 변경이 휩쓸려 들어가지 않게 한다.
- **원본 보존 = 롤백**: reset 전 HEAD는 reflog/objects에 남는다. 잘못되면 `git reset --hard <orig-head>`로 원복. 스크립트는 이 SHA를 보고에 남긴다.
- **base 검증**: base는 보통 `origin/<branch>`. base가 HEAD의 ancestor인지 확인하고(스크립트가 강제), 이미 push된 지점 너머로는 내려가지 않는다.
