# Optional source connectors and Recon-ng imports

Use these helpers for bounded public-source collection or for importing an existing export into a case. A collected item is an **unverified observation**. Neither the number of returned rows nor agreement between modules establishes independent corroboration, ownership, wrongdoing, or a claim verdict.

The implementation is original Python using the standard library. Recon-ng is not a runtime dependency; its code is not bundled. The core skill and local evidence helpers remain usable without network access.

## Adapter catalog

| Adapter | Input | Output | Network and key requirements | Coverage |
| --- | --- | --- | --- | --- |
| `certificate-transparency` (`crtsh`) | One dotted domain name | Certificate-observed host names within that domain | HTTPS GET to `crt.sh`; no key | Returned public certificate records. Does not establish that a host is active, controlled by a particular party, or covered completely over time. |
| `github-repositories` (`github-repos`) | One declared GitHub account | Public repository URLs and supplied repository metadata | HTTPS GET to `api.github.com`; authentication optional and explicitly selected | Bounded pages of owned public repositories. Does not collect private repositories, gists, or commit history. |
| `recon-ng-import` | Local JSON export, or CSV plus a declared table | Unverified domain, host, or repository leads | Offline; no key | Only selected `domains`, `hosts`, and `repositories` tables. Unsupported tables and rejected rows are reported explicitly. |

`adapter_catalog()` exposes requirements, adapter version, input/output types, coverage, and validation scope. It does not install or execute third-party modules. Python 3.10 or newer is the only runtime requirement.

## Collection behavior

Each network attempt records its actual request URL, time, HTTP status or failure, raw-response artifact name, and SHA-256 digest. Artifact summaries distinguish the original retrieval time from the time this run observed or reused the response. Original response bytes remain available for registration in the case's evidence store. A malformed provider response does not become a successful finding.

The transport has these bounds:

- Provider hosts are fixed in code. Domain/account inputs cannot supply an arbitrary request URL. Redirects are refused.
- The default timeout is 10 seconds per request; the allowed maximum is 30 seconds. Responses are capped at 10 MiB. A retained partial response is labeled `truncated` and the run cannot be reported as a complete collection.
- GitHub defaults to at most three pages of 100 records, with an explicit cap of ten pages. A remaining next-page link at the cap produces `partial` status. Pagination targets outside the expected provider/account are refused.
- At most two retries follow transient HTTP failures. Short waits are capped at two seconds. Longer provider `Retry-After` or rate-limit reset delays stop the run for a later attempt rather than retrying early. GitHub rate limits without an immediately usable delay also stop the run.
- Token values are never placed in request diagnostics or JSON summaries. No token is discovered implicitly. GitHub authentication requires the user to select an environment-variable name explicitly; only that value is sent to the declared GitHub API host.

`succeeded` means the bounded requested collection completed. It does not mean that a claim was verified. `partial` means observations were retained with an incomplete collection, rejected rows, or a page limit. `failed` means no usable observations were established or an input/provider failure prevented completion. Read the limitations and error alongside the status.

## Cache and repeated observations

Caching is optional. A cache entry retains the original response bytes, source URL, retrieval timestamp, and digest. Cache reuse is always labeled `from_cache`; the current run time does not replace the original retrieval time. Use refresh when a new provider check is needed. A corrupt cache entry fails its integrity/shape check rather than being treated as original evidence. A cache digest is an integrity baseline, not authentication of the publisher.

Repeated host names or repository URLs are retained as separate observations with a `duplicate_of` candidate index. Two certificate entries, source modules, or imports may mention the same entity for different reasons. Deduplication must not discard these observations or turn them into independent evidence streams.

## Offline Recon-ng intake

JSON exports must be objects keyed by table name, with an array of row objects for each selected table. CSV requires an explicit table selection; malformed row widths and duplicate headers are rejected. Imports are limited to 10 MiB and refuse symlink paths.

The original export is retained unchanged. Its source URL and original collection time remain unknown unless established separately. The import timestamp records this intake operation only. A row's module label is preserved as reported attribution, not proof of who collected it, when, or whether the underlying record was inspected. Optional reported source/time fields remain separately labeled as reported values.

Prepare a scoped export containing only material authorized for the case. If the export includes unsupported tables, their contents still remain in the preserved raw file and any full checkpoint.

The parser ignores no failure silently: unsupported tables, unsafe URLs, and rejected rows appear in the result. Optional SQL `NULL` columns are accepted where they do not replace the required domain, host, or repository value. No imported instruction, expression, shell command, or SQL statement is executed.

## Python interface

The CLI uses this same interface. For integrations that call the helper directly, add the installed skill's `scripts/` directory to the Python import path:

```python
from casekit.connectors import adapter_catalog, collect, parse_recon_export

result = collect("github-repositories", "octocat", max_pages=1)
summary = result.to_dict()  # JSON-safe metadata; excludes original response bytes
for artifact in result.artifacts:
    original_bytes = artifact.data
    original_digest = artifact.sha256

imported = parse_recon_export("selected-recon-export.json")
```

`CollectionResult` contains `adapter`, `status`, `input_value`, `artifacts`, `observations`, `requests`, `limitations`, `error`, and adapter `metadata`. Each observation names the exact `artifact_name` that produced it. Preserve that mapping when registering evidence. Registering the response or export does not promote every contained assertion to a verified fact.

## Provider documentation and validation

Provider documentation was inspected on 12 November 2026:

- GitHub: [list repositories for a user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), [pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api), and [rate-limit behavior](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). The helper requests API version `2026-03-10`.
- Sectigo's [crt.sh certificate search](https://crt.sh/). Its public JSON query is a service interface rather than a versioned API guarantee; unexpected responses are retained and reported as collection failures.
- Recon-ng's [module repository](https://github.com/lanmaster53/recon-ng-marketplace) and [JSON export implementation](https://github.com/lanmaster53/recon-ng-marketplace/blob/9527714d2bb38886422bab5f1c4724d4a20d3057/modules/reporting/json.py) establish the input shapes being supported.

Fixture tests cover pagination, rate-limit delays, explicit-token handling, caching, malformed and oversized responses, separate repeated observations, untrusted import rows, and symlink refusal. A bounded anonymous GitHub `octocat` request on 12 November 2026 returned eight public repository observations. A crt.sh `example.com` attempt timed out before a response was established, so live crt.sh availability remains unverified. These are provider smoke checks, not guarantees of future availability or multi-client activation tests. Consult the release compatibility record for other checks actually performed.
