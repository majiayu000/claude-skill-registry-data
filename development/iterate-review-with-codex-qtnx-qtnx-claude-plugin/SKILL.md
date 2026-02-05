---
name: iterate-review-with-codex
description: Activate when user mentions "codex review", "code review", "fix pr code review". This skill provides guidance on how to effectively collaborate with codex to do a interate code review.
---

# Iterate Review with Codex

Khi thực hiện code review với codex làm theo các bước sau:

## Guidelines

1. Sử dụng zen codereview để thực hiện review current code changes, vs base branch hoặc theo yêu cầu của người dùng. Lựa chọn review model theo các priority sau (tự động select model tiếp theo nếu một model bị lỗi):

- `gpt-5-pro`: tốt nhất để review
- `gemini-3-pro`: tốt cho review
- `codex`: sử dụng trong trường hợp các model kia không dùng được
  khi thực hiện zen code review cần thực hiện một cophensive review cover logic, egde cases, test cases, test logic, tránh các trường hợp false positive test

2. Review và fix comments của codex trên PR

Step 1: Khi người dùng request fix review của codex trên pr hãy sử dụng gh cli để pull comment mới nhất trong comment hiện tại. Xác nhận comment review nếu là false positive thì comment lại, nếu comment claim đúng thì thực hiện fix nó.
Step 2: Sau khi thực hiện fix hãy commit lại và push lên. Đánh dấu các comment đã được resolve.
Step 3: Sau đó comment lên PR mention @codex thực hiện cophensive review cung cấp toàn bộ comment trong một lần
Step 4: Chờ 5 phút cho codex thực hiện review sau đó lặp lại bước 1.

Iterate (lặp 4 bước) cho đến bao giờ codex like vào PR (không còn issues mới).
