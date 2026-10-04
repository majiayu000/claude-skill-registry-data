---
name: add-booking-endpoint
description: Use when adding a new API endpoint to BookingSystem.Api, to keep controller/service/DTO/test structure consistent with the rest of the codebase.
---

# Adding a new endpoint to BookingSystem.Api

Follow this sequence so new endpoints match the codebase's conventions (see CLAUDE.md):

1. **DTOs first.** Add request/response `record` types to the relevant file in `DTOs/`
   (e.g. `BookingDtos.cs`). Never expose an EF entity directly from a controller.
2. **Service method.** If the endpoint does anything beyond a simple CRUD read, add the
   logic to the matching interface + implementation in `Services/` (e.g.
   `IBookingService` / `BookingService`), not directly in the controller.
   - If the new logic reads then writes state that another request could also be
     writing concurrently, do NOT use a plain read-then-write. Use an atomic
     conditional `UPDATE ... WHERE` (see `BookingService.CreateBookingAsync`) or an EF
     Core concurrency token, and return a distinguishable "conflict" outcome rather
     than throwing.
3. **Controller action.** Thin method: model-bind the request DTO, call the service,
   map the result to the response DTO / appropriate status code
   (`Ok` / `Created` / `Conflict` / `NotFound` — never a bare 500 for an expected
   outcome like "lost the race").
4. **Authorization.** Add `[Authorize]` (already on the controller by default) and
   `[Authorize(Roles = Roles.Admin)]` on the action if it's an admin-only operation.
5. **Test.** Add an xUnit test in `BookingSystem.Tests` for the happy path and for the
   conflict/error path. If the endpoint touches shared mutable state (like a booking or
   slot), add or extend a concurrency test modeled on `ConcurrencyTests.cs`: fire
   several requests with `Task.WhenAll` and assert exactly one wins.
6. **Frontend (optional).** If the endpoint needs a UI, add a small function to
   `frontend/app.js` following the existing `api()` helper pattern — no new frontend
   framework or build step.

Run `dotnet build && dotnet test` before considering the change done.
