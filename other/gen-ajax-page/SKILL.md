---
name: gen-ajax-page
description: >
  fetch API 기반 Ajax 인터랙션이 포함된 Mustache 페이지를 생성하는 스킬.
  "/gen-ajax-page"를 입력하거나, "Ajax 페이지 만들어줘", "비동기 페이지 만들어줘" 같은 요청에 트리거된다.
  대상 기능과 호출할 API 엔드포인트를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Ajax Page

fetch API를 사용한 Ajax 인터랙션이 포함된 Mustache 페이지를 생성하는 스킬이다.

## 언제 사용하는가

- 페이지 새로고침 없이 부분 갱신이 필요한 UI를 만들 때
- 중복체크, 댓글 CRUD, 좋아요, 실시간 검증 등 Ajax가 필요한 기능
- "Ajax 페이지 만들어줘", "비동기 페이지 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 기능** — 어떤 기능의 페이지인지 (예: 댓글 목록/등록/삭제, 유저네임 중복체크)
2. **호출할 API 엔드포인트** — 어떤 REST API를 호출하는지 (예: `GET /api/reply`, `POST /api/reply`)
3. **UI 요소** — 필요한 입력 필드, 버튼, 표시 영역
4. **갱신 방식** — 전체 목록 다시 로드 vs 해당 요소만 추가/삭제

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 프론트엔드 규칙을 따른다:

### 기본 원칙

- POST 요청 기본: `<form>` 태그 + `name` 속성으로 제출 (페이지 이동 방식)
- **Ajax가 필요한 경우만** fetch 사용 (중복체크, 부분 갱신 등)

### fetch 패턴

```javascript
async function fetchData() {
    let response = await fetch("/api/board", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let responseBody = await response.json();

    if (responseBody.status === 200) {
        // 성공 처리
        render(responseBody.body);
    } else {
        alert(responseBody.msg);
    }
}
```

### POST/PUT/DELETE 패턴

```javascript
async function saveData() {
    let requestBody = {
        title: document.querySelector("#title").value,
        content: document.querySelector("#content").value
    };

    let response = await fetch("/api/board", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    });
    let responseBody = await response.json();

    if (responseBody.status === 200) {
        // 성공 처리
        alert("저장 완료");
        location.reload();
    } else {
        alert(responseBody.msg);
    }
}
```

### DOM 조작 패턴

```javascript
function render(dataList) {
    let el = document.querySelector("#list-area");
    el.innerHTML = "";

    dataList.forEach(item => {
        el.innerHTML += `
            <div class="item" id="item-${item.id}">
                <span>${item.title}</span>
                <button onclick="deleteItem(${item.id})">삭제</button>
            </div>
        `;
    });
}
```

## 출력 예시 — 댓글 Ajax 페이지

```html
{{>layout/header}}

<h2>댓글</h2>

<!-- 댓글 입력 -->
<div>
    <textarea id="comment" placeholder="댓글을 입력하세요"></textarea>
    <button onclick="replySave()">등록</button>
</div>

<!-- 댓글 목록 -->
<div id="reply-list"></div>

<script>
    let boardId = {{boardId}};

    // 페이지 로드 시 댓글 목록 조회
    replyList();

    async function replyList() {
        let response = await fetch(`/api/board/${boardId}/reply`);
        let responseBody = await response.json();

        if (responseBody.status === 200) {
            renderReplies(responseBody.body);
        } else {
            alert(responseBody.msg);
        }
    }

    function renderReplies(replies) {
        let el = document.querySelector("#reply-list");
        el.innerHTML = "";

        replies.forEach(reply => {
            el.innerHTML += `
                <div class="reply-item" id="reply-${reply.id}">
                    <strong>${reply.username}</strong>
                    <p>${reply.comment}</p>
                    ${reply.isOwner ? `<button onclick="replyDelete(${reply.id})">삭제</button>` : ""}
                </div>
            `;
        });
    }

    async function replySave() {
        let comment = document.querySelector("#comment").value;
        if (!comment.trim()) {
            alert("댓글을 입력하세요");
            return;
        }

        let response = await fetch(`/api/board/${boardId}/reply`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ comment: comment })
        });
        let responseBody = await response.json();

        if (responseBody.status === 200) {
            document.querySelector("#comment").value = "";
            replyList(); // 목록 새로고침
        } else {
            alert(responseBody.msg);
        }
    }

    async function replyDelete(id) {
        let response = await fetch(`/api/board/${boardId}/reply/${id}`, {
            method: "DELETE"
        });
        let responseBody = await response.json();

        if (responseBody.status === 200) {
            replyList(); // 목록 새로고침
        } else {
            alert(responseBody.msg);
        }
    }
</script>

{{>layout/footer}}
```

## 생성 위치

```
src/main/resources/templates/{domain}/{page-name}.mustache
```

## 주의사항

- Ajax가 불필요한 단순 폼 제출은 이 스킬을 사용하지 않는다 → `gen-controller`로 일반 폼 생성
- API 엔드포인트가 먼저 존재해야 한다. 없으면 사용자에게 알린다
- `Resp` 래퍼 응답 구조(`status`, `msg`, `body`)에 맞춰 처리한다
- XSS 방지를 위해 사용자 입력을 innerHTML에 넣을 때 주의한다
