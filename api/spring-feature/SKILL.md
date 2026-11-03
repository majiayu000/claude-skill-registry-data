---
name: spring-feature
description: Checklist for adding a backend endpoint or feature slice end to end (migration → entity → repository → service → DTO records → controller → errors → tests → OpenAPI). Use whenever adding or changing a REST endpoint in backend/.
argument-hint: "<METHOD /api/v1/path and purpose>"
---

# /spring-feature: add a backend slice

Follow `backend/CLAUDE.md`. Work top to bottom. Skip steps that don't apply, and say which ones you skipped.

1. **Contract first.** Write the request/response record shapes and status codes, and confirm them with the user if they're non-trivial.
2. **Migration** (if schema changes): new `V{n}__*.sql`. Add indexes for the query you're about to write. Update `docs/DATA_MODEL.md`.
3. **Entity**: protected no-arg constructor, meaningful constructor, getters, intention-revealing methods, `@ManyToOne(fetch = LAZY)`,
   `@Enumerated(EnumType.STRING)`.
4. **Repository**: user-scoped finders (`findByIdAndUserId`). Use a projection record for read-heavy or aggregate queries.
5. **Service**: package-private unless another feature needs it. `@Transactional` / `@Transactional(readOnly = true)`.
   Map entity → DTO here. Throw domain exceptions (`XNotFoundException`) for the advice to translate.
6. **DTOs**: records with Bean Validation annotations on requests. Use a static `from(Entity)` factory on the response record, or a small mapper method in the service.
7. **Controller**: thin. `@Valid @RequestBody`, authenticated user via `@AuthenticationPrincipal` (once auth exists).
   Use 201 + `Location` for creates and 204 for empty responses.
8. **Errors**: new exception types registered in the global `@RestControllerAdvice` → `ProblemDetail`.
9. **Tests**:
   - pure logic → plain JUnit
   - controller → `@WebMvcTest` (happy path, validation 400, not-found 404, and 401/403 once auth exists)
   - repository/native SQL → `@DataJpaTest` + Testcontainers
   - one `@SpringBootTest` happy path if the slice crosses modules
10. **Security check**: is every query scoped by user? Is anything sensitive logged or returned?
11. **OpenAPI**: check `/v3/api-docs` looks right, and remind the user to run `npm run gen:api` in mobile.
12. Run `./mvnw verify` and report results.
