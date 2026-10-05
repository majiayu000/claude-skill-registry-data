---
name: cafe24-preview
description: Use when previewing local working-tree CSS/JS changes on a live Cafe24 page before deploying through the admin panel — no HMR, deploy round-trips are slow. Triggers - "/cafe24-preview", "배포 전에 미리 보고 싶어", "로컬 수정본 라이브에서 확인해줘", "배포 안 하고 테스트", verifying a fix before Cafe24 admin deploy.
---

# Cafe24 배포 전 로컬 미리보기 (응답 패치)

## Overview

playwright-mcp의 `browser_run_code_unsafe`로 `page.route()`를 걸어, **라이브 페이지가 요청하는 리소스를 로컬 수정본으로 바꿔치기(fulfill)** 한 상태로 렌더링한다. 주입(append) 방식과 달리 브라우저 실행 "전"에 코드가 대체되므로 JS 중복 실행 문제가 없고, **새로고침해도 패치가 유지**된다.

**전제:** 로컬 HTML은 서버에 넣는 템플릿(입력)이지 완성된 출력이 아니다. `{$vars}`·모듈이 포함된 마크업은 로컬에서 변수가 안 풀려 미리보기 불가.

## 미리보기 가능 범위

| 변경 종류 | 미리보기 | 방법 |
|---|---|---|
| 외부 CSS/JS 파일 | ✅ | 파일 요청 인터셉트 → 로컬 내용으로 fulfill |
| 인라인 `<style>`/`<script>` (var-free) | ✅ | HTML 문서 응답 인터셉트 → 블록 마커 단위 치환 |
| `{$vars}`·모듈 포함 마크업 | ❌ | 불가 — 사용자에게 배포 필요 안내 |

## Workflow

0. **대상 페이지 URL은 사용자에게 물어본다 (탐색하지 말 것).** 스킬 인자에 URL이 없으면 AskUserQuestion 등으로 미리보기할 라이브 페이지 URL부터 받는다. curl·크롤링으로 URL을 찾으려 하지 말 것 — labnosh는 비로그인 접근 시 `/admin`으로 리다이렉트되어 상품 링크 탐색이 불가(실측).
1. **파일 매핑 검증 (건너뛰지 말 것).** 로컬 파일명 ≠ 배포 URL이다. 페이지의 네트워크 요청에서 CSS/JS URL을 확인하고, **로컬 수정 대상 셀렉터/함수가 그 응답 본문에 실제로 있는지** 확인한다. 없으면 해당 코드는 인라인 블록으로 배포된 것 → HTML 문서 패치로 전환.
   - labnosh 알려진 매핑: 외부 CSS `labnoshhost.mycafe24.com/assets/styles/product.css`, 외부 JS `assets/scripts/PRODUCT_DETAIL.js`. 단 로컬 `product-detail.css`(~2,800줄) 대부분은 템플릿 인라인일 수 있음 — 반드시 실측.
   - 상세 페이지 URL 형식: `…/product/{이름}/{번호}/…` (`detail.html?product_no=`는 404).
2. **변경분 분류.** git diff를 위 표에 따라 분류. `{$vars}` 포함 변경이 섞여 있으면 그 부분은 미리보기에서 빠진다고 명시.
3. **라우트 설치.** 아래 캐노니컬 코드 사용. Read로 로컬 파일을 읽어 치환 본문을 만든 뒤 코드 문자열에 넣는다.
4. **reload → 검증 → 즉시 종료.** 마커 규칙(`--preview-marker` 등)이나 `getComputedStyle` 실측으로 패치 적용을 확인한다. 적용이 확인되면 **거기서 턴을 끝낸다** — 사용자는 브라우저를 기다리고 있다. 검증 중 부수 이슈(캐스케이드 충돌, 다른 규칙이 이김 등)를 발견해도 원인 조사를 벌이지 말고 한 줄 언급만 하고 멈춘다(실측된 불만). 스크린샷은 사용자가 요청할 때만 — 이 스킬의 목적은 사용자가 패치된 페이지를 브라우저에서 직접 보는 것이다.
5. **열어두기 (기본).** 검증 후 라우트를 설치한 채로 페이지를 열어두고 사용자에게 확인하라고 알린다. 라우트는 같은 page 인스턴스에 남아 **이후의 다른 MCP 도구 호출·새로고침에도 유지**된다. 수정 반복 시 `unrouteAll` 후 재설치.
6. **정리는 사용자가 끝났다고 할 때만.** `page.unrouteAll({ behavior: 'ignoreErrors' })`로 원상 복구. 검증 끝났다고 임의로 복구하지 말 것 — 사용자가 보기 전에 패치가 사라진다(실측된 불만).

## 캐노니컬 코드 (browser_run_code_unsafe)

```js
async (page) => {
  await page.unrouteAll({ behavior: 'ignoreErrors' }); // 중복 등록 방지
  await page.route('**/assets/styles/product.css*', async (route) => {
    try {
      const response = await route.fetch();
      let body = await response.text();
      // 기본은 블록 단위 치환 — 로컬 ≠ 배포본이므로 통째 교체는 스타일 전멸 위험.
      // 통째 교체(body = LOCAL_CSS)는 매핑이 1:1로 검증된 경우만.
      body = body.replace(원본블록정규식, 수정블록); // 치환 성공 여부를 플래그로 기록해 반환할 것
      // 반드시 status/contentType/body 명시형으로 fulfill
      await route.fulfill({ status: 200, contentType: 'text/css', body });
    } catch (e) {
      await route.continue(); // 핸들러 예외 = 요청 통째 실패 → 폴백 필수
    }
  });
  await page.reload({ waitUntil: 'load', timeout: 45000 });
  return await page.evaluate(() => /* 패치 적용 검증 */ document.styleSheets.length);
}
```

HTML 문서 패치는 라우트 패턴을 페이지 URL로, 핸들러 첫 줄에 `if (route.request().resourceType() !== 'document') return route.continue();` 추가, contentType은 `'text/html; charset=utf-8'`.

## Common Mistakes (전부 실측된 실패)

| 실수 | 결과 / 올바른 방법 |
|---|---|
| `Buffer.byteLength`로 content-length 계산 | `Buffer is not defined` — 샌드박스에 Node 전역 없음. fulfill이 알아서 계산하므로 헤더 손대지 말 것 |
| `route.fulfill({ response, body })` (원본 response 재사용형) | **조용히 실패** — 패치 미적용인데 에러도 없음. `{ status, contentType, body }` 명시형만 사용 |
| 핸들러 try/catch 없음 | 예외 시 해당 리소스가 통째로 로드 안 됨 (스타일 전멸) |
| `unrouteAll` 없이 재등록 | 이전 핸들러(실패본 포함)가 중첩 실행 |
| 매핑 검증 생략, 파일명만 보고 인터셉트 | 로컬 파일과 배포 파일이 달라 "패치했는데 그대로"로 보임 |
| 배포본을 로컬 파일로 통째 교체 | 배포본에만 있는 규칙이 사라져 스타일 전멸 — 블록 단위 치환이 기본 |
| 치환 성공 여부 확인 없이 fulfill | 정규식 미매칭 시 원본 그대로 서빙되어 "패치했는데 그대로" — 치환 여부를 플래그로 반환할 것 |
| `{$vars}` 포함 블록을 치환 | 날 변수 텍스트 노출로 페이지 깨짐 |
| 검증을 주입 방식 습관대로 "새로고침 금지"로 진행 | 불필요한 제약 — 응답 패치는 새로고침에도 유지됨. 오히려 reload가 정상 검증 경로 |
| 패치 적용 확인 후에도 부수 이슈 원인 조사를 계속 진행 | 사용자는 브라우저만 기다리는 중 — "띄우고 끝"이 역할. 발견 사항은 한 줄 언급 후 즉시 종료(실측된 불만) |
