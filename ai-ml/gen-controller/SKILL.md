---
name: gen-controller
description: >
  common-rule.md 컨벤션에 맞는 SSR Controller와 Mustache 템플릿을 생성하는 스킬.
  "/gen-controller"를 입력하거나, "컨트롤러 만들어줘", "페이지 만들어줘" 같은 요청에 트리거된다.
  대상 도메인과 필요한 페이지를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Controller

SSR Controller(`@Controller`)와 Mustache 템플릿을 함께 생성하는 스킬이다.

## 언제 사용하는가

- 새 도메인의 SSR 페이지가 필요할 때
- "컨트롤러 만들어줘", "페이지 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 도메인** — 어떤 도메인인지 (예: `Board`)
2. **필요한 페이지** — 목록, 상세, 등록폼, 수정폼 중 필요한 것
3. **인증 필요 여부** — 로그인 체크가 필요한 페이지가 있는지

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 Controller 규칙을 따른다:

### 어노테이션 순서

```java
@RequiredArgsConstructor
@Controller
public class {Domain}Controller {
```

### SSR 규칙

- 반환값은 `String` (Mustache 템플릿 경로)
- `HttpSession`은 생성자 주입
- REST API는 이 컨트롤러에 넣지 않는다 (별도 `ApiController` 파일)

### Controller 예시

```java
package com.example.ajax_demo.board;

import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

@RequiredArgsConstructor
@Controller
public class BoardController {

    private final BoardService boardService;
    private final HttpSession session;

    @GetMapping("/board")
    public String list(Model model) {
        model.addAttribute("boards", boardService.게시글목록());
        return "board/list";
    }

    @GetMapping("/board/{id}")
    public String detail(@PathVariable int id, Model model) {
        model.addAttribute("board", boardService.상세보기(id));
        return "board/detail";
    }

    @GetMapping("/board/save-form")
    public String saveForm() {
        return "board/save-form";
    }

    @PostMapping("/board/save")
    public String save(BoardRequest.SaveOrUpdateDTO reqDTO) {
        User sessionUser = (User) session.getAttribute("sessionUser");
        boardService.게시글쓰기(reqDTO, sessionUser);
        return "redirect:/board";
    }
}
```

### Mustache 템플릿 예시

목록 페이지 (`templates/board/list.mustache`):

```html
{{>layout/header}}

<h1>게시글 목록</h1>
<table>
    <thead>
        <tr>
            <th>번호</th>
            <th>제목</th>
            <th>작성자</th>
        </tr>
    </thead>
    <tbody>
        {{#boards}}
        <tr>
            <td>{{id}}</td>
            <td><a href="/board/{{id}}">{{title}}</a></td>
            <td>{{username}}</td>
        </tr>
        {{/boards}}
    </tbody>
</table>

{{>layout/footer}}
```

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}Controller.java
src/main/resources/templates/{domain}/list.mustache
src/main/resources/templates/{domain}/detail.mustache
src/main/resources/templates/{domain}/save-form.mustache
src/main/resources/templates/{domain}/update-form.mustache
```

## 주의사항

- REST API 엔드포인트는 이 스킬로 생성하지 않는다 → `gen-api-controller` 사용
- Service가 먼저 존재해야 한다. 없으면 사용자에게 알린다
- 레이아웃 파티얼(`layout/header`, `layout/footer`)이 있는지 확인하고 없으면 사용자에게 알린다
