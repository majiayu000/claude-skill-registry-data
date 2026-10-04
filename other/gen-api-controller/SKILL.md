---
name: gen-api-controller
description: >
  common-rule.md 컨벤션에 맞는 REST API Controller를 생성하는 스킬.
  "/gen-api-controller"를 입력하거나, "API 컨트롤러 만들어줘", "REST API 만들어줘" 같은 요청에 트리거된다.
  대상 도메인과 필요한 엔드포인트를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Api Controller

REST API Controller(`@RestController`)를 생성하는 스킬이다.

## 언제 사용하는가

- Ajax 호출을 받을 REST API 엔드포인트가 필요할 때
- "API 컨트롤러 만들어줘", "REST API 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 도메인** — 어떤 도메인인지 (예: `Board`)
2. **엔드포인트 목록** — 필요한 API (예: 목록 조회, 등록, 수정, 삭제, 중복체크 등)
3. **인증 필요 여부** — 세션 체크가 필요한 엔드포인트가 있는지

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 Controller 규칙을 따른다:

### 어노테이션 순서

```java
@RequiredArgsConstructor
@RestController
public class {Domain}ApiController {
```

### REST 규칙

- SSR Controller와 **별도 파일**로 분리
- 엔드포인트 주소는 `/api` 접두사 필수
- 응답은 반드시 `Resp<T>` 래퍼 사용 — 날(raw) 반환 금지
- 성공: `Resp.ok(dto)`, 실패: `Resp.fail(HttpStatus, "메시지")`

### 출력 예시

```java
package com.example.ajax_demo.board;

import com.example.ajax_demo._core.utils.Resp;
import com.example.ajax_demo.user.User;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
public class BoardApiController {

    private final BoardService boardService;
    private final HttpSession session;

    @GetMapping("/api/board")
    public ResponseEntity<?> list() {
        List<BoardResponse.DTO> boards = boardService.게시글목록();
        return ResponseEntity.ok(Resp.ok(boards));
    }

    @PostMapping("/api/board")
    public ResponseEntity<?> save(@RequestBody BoardRequest.SaveOrUpdateDTO reqDTO) {
        User sessionUser = (User) session.getAttribute("sessionUser");
        boardService.게시글쓰기(reqDTO, sessionUser);
        return ResponseEntity.ok(Resp.ok(null));
    }

    @PutMapping("/api/board/{id}")
    public ResponseEntity<?> update(@PathVariable int id,
                                    @RequestBody BoardRequest.SaveOrUpdateDTO reqDTO) {
        boardService.게시글수정(id, reqDTO);
        return ResponseEntity.ok(Resp.ok(null));
    }

    @DeleteMapping("/api/board/{id}")
    public ResponseEntity<?> delete(@PathVariable int id) {
        boardService.게시글삭제(id);
        return ResponseEntity.ok(Resp.ok(null));
    }
}
```

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}ApiController.java
```

## 주의사항

- SSR 페이지 라우팅은 이 스킬로 생성하지 않는다 → `gen-controller` 사용
- Service가 먼저 존재해야 한다. 없으면 사용자에게 알린다
- 모든 응답은 `Resp.ok()` / `Resp.fail()` 래퍼 사용
