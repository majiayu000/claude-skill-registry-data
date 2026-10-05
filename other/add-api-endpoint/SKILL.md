---
name: add-api-endpoint
description: Add or change a Crucible API endpoint, request or response model, pagination path, repository cache, or scientific metadata write. Use when touching data/api, data/repository, API serialization, or create and edit network flows.
---

# Add a Crucible API endpoint

## Service layer

Add the method in `data/api/CrucibleApiService.kt` and wrap it with `safeCall` so non-2xx responses become `ApiResult.Error` values. The shared client uses `expectSuccess = true`; do not bypass that behavior.

```kotlin
suspend fun getWidget(widgetId: String): ApiResult<Widget> = safeCall {
    client.get("$baseUrl/widgets/$widgetId").body()
}
```

Send `Authorization: Bearer {apiKey}` on authenticated requests. Handle both `ApiResult.Success` and `ApiResult.Error` at call sites.

Choose pagination from the endpoint response:

| Response | Helper |
|---|---|
| Offset and limit list | `fetchAllPages` |
| Sample or dataset keyset cursor list | `fetchAllPagesCursor` |
| Flat search result | No pagination helper |

Use explicit `@SerialName` values for wire fields that must remain stable, including single-word names whose Kotlin property might later be renamed.

## Scientific metadata

Sample and dataset create/update DTOs do not accept `scientific_metadata`; the server silently drops it. Create and edit flows therefore make a structural request and a separate metadata request.

- Metadata `POST` and `PATCH` return `ApiResult<JsonObject>`, not `ApiResult<Unit>`.
- On create, use a plain metadata `POST`.
- On edit, use `diffMetadataWrite` from `ui/common/MetadataEditor.kt`.
- If no key was deleted, `PATCH` only the changed top-level keys.
- If a key was deleted, `POST ?overwrite=true` with the complete object because `PATCH` cannot express deletion.

## Repository and cache

Use `CrucibleRepository` for data that should be cached or observed by multiple consumers. Back it with `ObservableCache`, using `Unit` with `maxSize = 1` for a whole collection or an entity ID for per-entity data. Let `ObservableCache` own TTL and LRU behavior.

Expose observation when screens must react to cache updates. Do not copy an observed repository object into long-lived Compose state.

Skip the repository for a one-shot mutation with nothing to cache. Existing join-request mutations intentionally call `apiClient.service` from their ViewModels; pending join-request counts remain in the repository because several screens consume them.

## Documentation and tests

- Update the endpoint and caching sections of `dev/architecture.md`.
- Add an `Unreleased` changelog entry only for a user-visible change.
- Add a common test for new deterministic branching, parsing, sorting, or cache logic. A direct Ktor wrapper without app logic does not require a unit test.

## Verify

```bash
./scripts/verify-change.sh
```
