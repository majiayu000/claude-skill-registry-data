---
name: add-error-code
description: Add an error code the API (or the AI service) can return, with its HTTP status and its message in every language. Use when a new expected failure needs its own code, rather than a generic one.
argument-hint: <CODE> <http status>
---

# Add an error code

Clients branch on codes and translate them; they never read messages. The catalog is
`packages/contracts/src/errors.ts`.

1. **Is a generic one enough?** `NOT_FOUND`, `CONFLICT`, `FORBIDDEN`,
   `VALIDATION_FAILED`, `RATE_LIMITED` cover most cases. A new code is for a failure a
   client handles differently (a limit reached, a state that forbids the action).
2. **Declare it** in `ERROR_CODES`, in its section, as `SCREAMING_CASE` with the HTTP
   status that fits: 400/422 bad input, 403 not allowed, 404 absent, 409 conflicting
   state, 429 limited, 502 an upstream failed. Never 500 for an expected case.
3. **Its message** as `errors.<CODE>` in every `packages/i18n/messages/*.json`, with ICU
   arguments for its `params` (strings and numbers only), e.g.
   `"API_KEY_LIMIT_REACHED": "A workspace can have up to {limit} keys."`. A message with
   arguments needs them declared in `ERROR_PARAMS` too (`{ limit: z.number().int() }`):
   then throwing the code without them doesn't compile, and `packages/i18n`'s test fails
   if a message's placeholders and the declared params differ.
4. **Throw it**: `throw new AppError("<CODE>", { params: { ... } })` from
   `@repo/nest-common` in a service; `raise AppError("<CODE>", status, params)` in
   `apps/ai` (`app/errors.py`), with the same code.
5. **Handle it** where a client should react: `errorCode(error) === "<CODE>"` in the
   hook or component, and the message through `errorMessageKey(error)`
   (`packages/client/src/errors.ts`).
6. **Test it**: an integration test that the procedure answers with the code and
   status (`apps/api/test/*.integration.test.ts`).

## Done when

`bun run check-types`, `bun run test` (`packages/i18n`'s test fails until every catalog
has the key) and `bun run test:integration` pass; `bun run gen` leaves
`apps/api/openapi.json` committed.
