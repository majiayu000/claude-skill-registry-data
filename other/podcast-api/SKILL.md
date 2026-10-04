---
name: podcast-api
description: Build, debug, review, and explain Listen Notes Podcast API integrations. Use for podcast or episode search, discovery, metadata, playlist creation, editing and deletion, headless CMS and editorial curation, SDK integration, transcripts, authentication, pagination, mock testing, and API or billing questions.
---

# Podcast API

Use the Listen Notes Podcast API without guessing endpoints, exposing credentials, or treating mock data as real data.

## Sources Of Truth

- Use the live [OpenAPI YAML](https://listen-api.listennotes.com/api/v2/openapi.yaml) for exact methods, parameters, request bodies, response schemas, and endpoint restrictions.
- Use the [tutorial index](https://www.listennotes.com/api/tutorials/) for supported application workflows.
- Use the live [API FAQ](https://www.listennotes.com/api/faq/), [billing FAQ](https://www.listennotes.com/api/billing-faq/), [pricing](https://www.listennotes.com/api/pricing/), and [terms](https://www.listennotes.com/api/terms/) for policies and facts that may change.

Do not copy a remembered schema into an implementation. Verify the relevant OpenAPI operation when network access is available. If it is unavailable, use the bundled endpoint map, state the limitation, and avoid inventing fields.

## Workflow

1. Inspect the target repository before changing it.
   - Identify the language, framework, server-side boundary, HTTP client, environment-variable convention, and test setup.
   - Reuse an installed official SDK or the project's existing HTTP client. Otherwise prefer the language's native HTTP facilities instead of adding a dependency.
   - For SDK versions, playlist method names, and upgrade compatibility, read [official-sdks.md](references/official-sdks.md). Older SDKs may lack playlist writes; do not invent methods on the installed version.
2. Select the operation.
   - Read [endpoint-selection.md](references/endpoint-selection.md).
   - Load only the use-case reference relevant to the request.
   - Confirm the operation in the live OpenAPI document, including plan restrictions and pagination fields.
   - For an editorial feed, curated collection, or headless CMS, read [playlist-cms.md](references/playlist-cms.md). Playlists support both API editing and human curation in Listen Later.
3. Design the security boundary.
   - Read `LISTEN_API_KEY` only in server-side code or a serverless function.
   - Send it as `X-ListenAPI-Key` to the production API.
   - Never place it in browser or mobile bundles, public environment variables, source control, URLs, fixtures, logs, or error messages.
   - If the current architecture cannot protect the key, add a server-side proxy before integrating the API.
4. Implement in the project's style.
   - Keep the production base URL configurable and default it to `https://listen-api.listennotes.com/api/v2`.
   - Encode query parameters and request bodies with structured APIs.
   - Validate inputs at the application's boundary and handle non-2xx responses explicitly.
   - For playlist writes, enforce the application's editor permissions and collection ownership before forwarding requests. Only playlists owned by your admin API account can be modified.
   - For whole-playlist deletion, add confirmation in the application's UI before sending `DELETE /playlists/{id}`. It permanently removes the collection and its saved references and notes; there is no recovery. See [playlist-cms.md](references/playlist-cms.md) for deletion behavior.
   - Follow [integration-rules.md](references/integration-rules.md) for pagination, usage headers, caching, attribution, and error handling.
5. Test without spending quota.
   - Follow [testing.md](references/testing.md).
   - Use `https://listen-api-test.listennotes.com/api/v2` without an API key only for HTTP transport and response-shape tests.
   - Use local mocks or fixtures for parameter behavior, error paths, and pagination logic.
6. Verify the result.
   - Confirm no secret crosses a client boundary or appears in generated output.
   - Confirm the selected endpoint and every field used still exist in OpenAPI.
   - Confirm pagination terminates and does not issue unbounded requests.
   - Confirm UI using API data satisfies the applicable attribution rules.

Do not make a production request unless the user explicitly asks and has arranged a credential. Never print or inspect the credential value.

## Reference Routing

- Endpoint choice and current API surface: [endpoint-selection.md](references/endpoint-selection.md)
- Authentication, errors, pagination, caching, and attribution: [integration-rules.md](references/integration-rules.md)
- Mock server and test strategy: [testing.md](references/testing.md)
- Official SDK versions, package names, and playlist methods: [official-sdks.md](references/official-sdks.md)
- Search, typeahead, genres, charts, and discovery: [search-and-discovery.md](references/search-and-discovery.md)
- Podcast lookup, episode sync, subscriptions, OPML, and webhooks: [library-and-sync.md](references/library-and-sync.md)
- Playlist creation, editing, publication, permanent deletion, and headless CMS: [playlist-cms.md](references/playlist-cms.md)
- Application-owned playlists, audio, embeds, and transcripts: [playlists-and-media.md](references/playlists-and-media.md)
- API keys, usage monitoring, and account operations: [account-and-usage.md](references/account-and-usage.md)
- Product, policy, support, rate-limit, and data questions: [api-faq.md](references/api-faq.md)
- Plans, quotas, charges, cancellation, and payments: [billing-faq.md](references/billing-faq.md)

## Answering Questions

Answer stable technical behavior from the appropriate reference and link to the live source. Re-check the live page before quoting a price, quota, plan entitlement, rate limit, support commitment, or legal/policy requirement. Distinguish API behavior from business policy, and direct account-specific billing issues to `hello@listennotes.com`.
