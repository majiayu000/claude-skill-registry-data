"""Bounded public-source adapters and offline Recon-ng export intake.

This module collects observations, not verdicts. It has no dependency on the case
database and never installs modules, executes imported content, or follows links
found in a response. Network requests are limited to the two declared providers.
"""

from __future__ import annotations

import base64
import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
from http.client import HTTPException
import io
import ipaddress
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_RESPONSE_BYTES = 10 * 1024 * 1024
MAX_IMPORT_BYTES = 10 * 1024 * 1024
MAX_RETRIES = 2
MAX_SHORT_WAIT = 2.0
USER_AGENT = "investigate-and-fact-check/1.1 (+https://github.com/KhademOHAli1/investigate-and-fact-check)"
ADAPTERS = {
    "certificate-transparency": {
        "name": "Certificate transparency via crt.sh",
        "version": "1.0.0",
        "input_type": "public domain name",
        "output_types": ["host"],
        "required_tools": ["Python 3.10+"],
        "required_keys": [],
        "network_hosts": ["crt.sh"],
        "coverage": "Names in the returned certificate log records; not proof of ownership, active service, or complete historical coverage.",
        "validation": "Fixture tests cover parsing and HTTP behavior; a successful request is recorded per run, not assumed from installation.",
    },
    "github-repositories": {
        "name": "GitHub public repositories",
        "version": "1.0.0",
        "input_type": "declared GitHub account name",
        "output_types": ["repository"],
        "required_tools": ["Python 3.10+"],
        "required_keys": [],
        "optional_key": "An explicitly named environment variable containing a GitHub token",
        "network_hosts": ["api.github.com"],
        "coverage": "Public repositories returned for one declared account, bounded by max_pages. No private repositories, gists, or commit-history collection.",
        "validation": "Fixture tests cover parsing and HTTP behavior; a successful request is recorded per run, not assumed from installation.",
    },
}
ALIASES = {"crtsh": "certificate-transparency", "github-repos": "github-repositories"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


class ConnectorError(ValueError):
    """Input or provider behavior prevents a complete bounded collection."""


@dataclass
class RawArtifact:
    name: str
    data: bytes
    source_url: str
    retrieved_at_utc: str
    observed_at_utc: str
    http_status: int | None = None
    from_cache: bool = False
    content_type: str = "application/json"
    truncated: bool = False

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name, "source_url": self.source_url,
            "retrieved_at_utc": self.retrieved_at_utc,
            "observed_at_utc": self.observed_at_utc, "http_status": self.http_status,
            "from_cache": self.from_cache, "content_type": self.content_type,
            "truncated": self.truncated, "sha256": self.sha256, "bytes": len(self.data),
        }


@dataclass
class CollectionResult:
    adapter: str
    status: str = "succeeded"
    input_value: str = ""
    artifacts: list[RawArtifact] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    requests: list[dict[str, Any]] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """JSON-safe summary; original response bytes are accessed explicitly."""
        return {
            "adapter": self.adapter, "status": self.status, "input_value": self.input_value,
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "observations": self.observations, "requests": self.requests,
            "limitations": self.limitations, "error": self.error, "metadata": self.metadata,
        }


def adapter_catalog() -> dict[str, dict[str, Any]]:
    return json.loads(json.dumps(ADAPTERS))


def _domain(value: str, wildcard: bool = False) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ConnectorError("A domain name is required, without whitespace or URL syntax.")
    value = value.rstrip(".").lower()
    if wildcard and value.startswith("*."):
        value = value[2:]
    try:
        name = value.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise ConnectorError("Invalid domain name.") from error
    if len(name) > 253 or "." not in name:
        raise ConnectorError("A dotted public-style domain name is required.")
    labels = name.split(".")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels):
        raise ConnectorError("Invalid domain name.")
    if labels[-1].isdigit() or labels[-1] in {"localhost", "local", "internal", "localdomain"}:
        raise ConnectorError("Private/local names and IP addresses are not domain inputs.")
    try:
        ipaddress.ip_address(name)
    except ValueError:
        return name
    raise ConnectorError("IP addresses are not domain inputs.")


def _account(value: str) -> str:
    if not isinstance(value, str) or len(value) > 39 or not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", value):
        raise ConnectorError("Use a GitHub account name, not a URL or search query.")
    return value.lower()


def _public_url(value: str) -> str:
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        raise ConnectorError("Invalid public URL.")
    parsed = urlsplit(value)
    try:
        port = parsed.port
    except ValueError as error:
        raise ConnectorError("Invalid URL port.") from error
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ConnectorError("Only HTTP(S) URLs without embedded credentials are accepted.")
    if port not in (None, 80 if parsed.scheme == "http" else 443):
        raise ConnectorError("Nonstandard URL ports are not accepted.")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        _domain(parsed.hostname)
    else:
        if not address.is_global:
            raise ConnectorError("Private or local IP addresses are not accepted.")
    return value


def _provider_url(value: str, host: str) -> str:
    _public_url(value)
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.hostname != host or parsed.fragment or parsed.port not in (None, 443):
        raise ConnectorError("Request left the declared HTTPS provider endpoint.")
    return value


def _local_path(value: str | Path) -> Path:
    path = Path(os.path.abspath(os.path.expanduser(str(value))))
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ConnectorError("Symlink paths are not accepted for import/cache files.")
    return path


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConnectorError("Duplicate JSON keys are not accepted.")
        result[key] = value
    return result


def _parse_json(data: bytes):
    def reject_constant(value):
        raise ConnectorError("Non-finite JSON values are not accepted.")

    try:
        return json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_keys,
                          parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ConnectorError("Response/import is not valid UTF-8 JSON.") from error


def _valid_utc(value: str) -> bool:
    try:
        return isinstance(value, str) and value.endswith("Z") and datetime.fromisoformat(value[:-1] + "+00:00").utcoffset().total_seconds() == 0
    except (ValueError, AttributeError):
        return False


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        raise ConnectorError("Provider redirect refused; no credentials or queries were forwarded.")


def _open(request: Request, timeout: float):
    return build_opener(_NoRedirect()).open(request, timeout=timeout)


def _response_headers(headers):
    canonical = {name.lower(): name for name in ("Content-Type", "Link", "Retry-After", "X-RateLimit-Remaining", "X-RateLimit-Reset")}
    return {canonical.get(name.lower(), name): value for name, value in headers.items()}


class _Client:
    def __init__(self, result, host, cache_dir, refresh, timeout, token):
        self.result, self.host, self.refresh, self.timeout = result, host, refresh, timeout
        self.token = token
        self.cache = _local_path(cache_dir) if cache_dir is not None else None
        if self.cache is not None:
            self.cache.mkdir(parents=True, exist_ok=True)
            if not self.cache.is_dir():
                raise ConnectorError("Cache path must be a directory.")

    def _artifact(self, data, url, retrieved, observed, status, headers, cached=False, truncated=False):
        artifact = RawArtifact(
            name=f"{self.result.adapter}-{len(self.result.artifacts) + 1:03d}.json",
            data=data, source_url=url, retrieved_at_utc=retrieved, observed_at_utc=observed,
            http_status=status, from_cache=cached,
            content_type=headers.get("Content-Type", "application/json"), truncated=truncated,
        )
        self.result.artifacts.append(artifact)
        return artifact

    def _cache_path(self, url):
        key = hashlib.sha256((url + f"\nauthenticated={bool(self.token)}").encode()).hexdigest()
        return _local_path(self.cache / f"{key}.json")

    def _read_cache(self, url):
        if self.cache is None or self.refresh:
            return None
        path = self._cache_path(url)
        if not path.exists():
            return None
        if not stat.S_ISREG(path.lstat().st_mode) or path.stat().st_size > 2 * MAX_RESPONSE_BYTES:
            raise ConnectorError("Cache entry is not a bounded regular file.")
        cached = _parse_json(path.read_bytes())
        try:
            data = base64.b64decode(cached["body"], validate=True)
            if cached["schema_version"] != 1 or cached["url"] != url or len(data) > MAX_RESPONSE_BYTES:
                raise ValueError
            if hashlib.sha256(data).hexdigest() != cached["sha256"] or not _valid_utc(cached["retrieved_at_utc"]):
                raise ValueError
            headers = cached["headers"]
            if not isinstance(headers, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in headers.items()):
                raise ValueError
        except (KeyError, TypeError, ValueError) as error:
            raise ConnectorError("Cache integrity/shape check failed; use refresh to fetch a new response.") from error
        observed = utc_now()
        artifact = self._artifact(data, url, cached["retrieved_at_utc"], observed, 200, headers, cached=True)
        self.result.requests.append({
            "url": url, "method": "GET", "attempt": 0, "observed_at_utc": observed,
            "retrieved_at_utc": artifact.retrieved_at_utc, "http_status": 200,
            "from_cache": True, "artifact_name": artifact.name, "sha256": artifact.sha256,
        })
        if "Cached responses were reused; this is not a fresh provider check." not in self.result.limitations:
            self.result.limitations.append("Cached responses were reused; this is not a fresh provider check.")
        return artifact, headers

    def _save_cache(self, url, artifact, headers):
        if self.cache is None:
            return
        payload = {
            "schema_version": 1, "url": url, "retrieved_at_utc": artifact.retrieved_at_utc,
            "sha256": artifact.sha256, "body": base64.b64encode(artifact.data).decode("ascii"),
            "headers": {key: headers[key] for key in ("Content-Type", "Link") if key in headers},
        }
        destination = self._cache_path(url)
        fd, temporary = tempfile.mkstemp(prefix=".response-", dir=self.cache)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                json.dump(payload, stream, sort_keys=True)
                stream.write("\n")
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def _delay(self, status, headers, attempt):
        if attempt > MAX_RETRIES:
            return None
        if headers.get("X-RateLimit-Remaining") == "0":
            try:
                delay = float(headers["X-RateLimit-Reset"]) - time.time() + 0.05
            except (KeyError, ValueError):
                return None
            return max(0.0, delay) if delay <= MAX_SHORT_WAIT else None
        retry_after = headers.get("Retry-After")
        if retry_after is not None:
            try:
                delay = float(retry_after)
            except ValueError:
                try:
                    delay = (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds()
                except (ValueError, TypeError):
                    return None
            if delay < 0:
                delay = 0.0
            return delay if delay <= MAX_SHORT_WAIT else None
        if status in (403, 429):
            # GitHub's minimum secondary-limit delay is longer than our bounded
            # short retries. Stop for a later run rather than retrying too soon.
            return None
        return min(MAX_SHORT_WAIT, float(attempt))

    def fetch(self, url):
        _provider_url(url, self.host)
        cached = self._read_cache(url)
        if cached is not None:
            return cached
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        if self.host == "api.github.com":
            headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"})
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(1, MAX_RETRIES + 2):
            observed = utc_now()
            diagnostic = {"url": url, "method": "GET", "attempt": attempt, "observed_at_utc": observed, "from_cache": False}
            self.result.requests.append(diagnostic)
            try:
                with _open(Request(url, headers=headers, method="GET"), self.timeout) as response:
                    status = response.status
                    response_headers = _response_headers(response.headers)
                    data = response.read(MAX_RESPONSE_BYTES + 1)
            except HTTPError as error:
                status, response_headers = error.code, _response_headers(error.headers) if error.headers else {}
                data = error.read(MAX_RESPONSE_BYTES + 1)
                error.close()
            except (URLError, OSError, HTTPException, ConnectorError) as error:
                diagnostic["error"] = type(error).__name__
                raise ConnectorError(f"Network request failed ({type(error).__name__}); no provider response was established.") from error
            retrieved = utc_now()
            too_large = len(data) > MAX_RESPONSE_BYTES
            artifact = self._artifact(data[:MAX_RESPONSE_BYTES], url, retrieved, observed, status, response_headers, truncated=too_large)
            diagnostic.update({"retrieved_at_utc": retrieved, "http_status": status, "artifact_name": artifact.name, "sha256": artifact.sha256})
            if too_large:
                diagnostic["error"] = "response_too_large"
                raise ConnectorError("Provider response exceeded the byte limit; the saved artifact is explicitly truncated.")
            if status == 200:
                self._save_cache(url, artifact, response_headers)
                return artifact, response_headers
            limited = status == 429 or (status == 403 and (response_headers.get("X-RateLimit-Remaining") == "0" or "Retry-After" in response_headers))
            retryable = limited or status in {500, 502, 503, 504}
            delay = self._delay(status, response_headers, attempt) if retryable else None
            if delay is not None:
                diagnostic["retry_delay_seconds"] = delay
                time.sleep(delay)
                continue
            diagnostic["error"] = "rate_limited" if limited else "http_error"
            if limited:
                raise ConnectorError(f"Provider rate limit (HTTP {status}); stop and retry in a later run after the provider's delay/reset.")
            raise ConnectorError(f"Provider returned HTTP {status}; collection stopped.")
        raise ConnectorError("HTTP retry limit reached.")


def _observe(result, artifact, kind, value, **extra):
    duplicate = next((index for index, item in enumerate(result.observations) if item["kind"] == kind and item["value"] == value), None)
    observation = {
        "kind": kind, "value": value, "artifact_name": artifact.name,
        "source_url": artifact.source_url, "origin_module": result.adapter,
        "retrieved_at_utc": artifact.retrieved_at_utc,
        "limitations": "Unverified discovery observation; does not establish ownership or a claim verdict.",
        "provenance_status": "provider-observation", "duplicate_of": duplicate,
    }
    observation.update(extra)
    result.observations.append(observation)


def _ct(result, client, domain):
    url = "https://crt.sh/?" + urlencode({"q": "%." + domain, "output": "json"})
    artifact, _ = client.fetch(url)
    rows = _parse_json(artifact.data)
    if not isinstance(rows, list):
        raise ConnectorError("crt.sh response must be a JSON array.")
    ignored = 0
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("name_value"), str):
            ignored += 1
            continue
        for candidate in row["name_value"].split():
            try:
                host = _domain(candidate, wildcard=True)
            except ConnectorError:
                ignored += 1
                continue
            if host != domain and not host.endswith("." + domain):
                ignored += 1
                continue
            _observe(result, artifact, "host", host, certificate_id=row.get("id"),
                     certificate_name=candidate, certificate_not_before=row.get("not_before", ""),
                     certificate_not_after=row.get("not_after", ""))
    if ignored:
        result.status = "partial" if result.observations else "failed"
        result.limitations.append(f"Ignored {ignored} malformed, non-host, or out-of-scope certificate entries.")


def _next_github_page(headers, account, expected_page):
    link = headers.get("Link", "")
    matches = re.findall(r'<([^>]+)>;\s*rel="([^"]+)"', link)
    next_urls = [url for url, relation in matches if relation == "next"]
    if not next_urls:
        return False
    if len(next_urls) != 1:
        raise ConnectorError("Ambiguous GitHub pagination links.")
    parsed = urlsplit(_provider_url(next_urls[0], "api.github.com"))
    pages = parse_qs(parsed.query).get("page", [])
    if parsed.path != f"/users/{account}/repos" or pages != [str(expected_page)]:
        raise ConnectorError("Unexpected GitHub pagination target; no link was followed.")
    return True


def _github(result, client, account, max_pages):
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/users/{quote(account, safe='')}/repos?" + urlencode({"type": "owner", "sort": "full_name", "direction": "asc", "per_page": 100, "page": page})
        artifact, headers = client.fetch(url)
        rows = _parse_json(artifact.data)
        if not isinstance(rows, list):
            raise ConnectorError("GitHub repositories response must be a JSON array.")
        ignored = 0
        for row in rows:
            try:
                if not isinstance(row, dict) or row.get("private") is not False:
                    raise ConnectorError("Only explicitly public repository records are accepted.")
                value = _public_url(row.get("html_url"))
                parsed = urlsplit(value)
                parts = parsed.path.strip("/").split("/")
                if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.query or parsed.fragment or len(parts) != 2 or parts[0].lower() != account.lower() or parts[1] in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9_.-]+", parts[1]):
                    raise ConnectorError("Unexpected repository identity/URL.")
            except (ConnectorError, TypeError, AttributeError):
                ignored += 1
                continue
            _observe(result, artifact, "repository", value, repository_id=row.get("id"),
                     full_name="/".join(parts), fork=row.get("fork"),
                     default_branch=row.get("default_branch", ""), pushed_at=row.get("pushed_at", ""))
        if ignored:
            result.status = "partial" if result.observations else "failed"
            result.limitations.append(f"Ignored {ignored} malformed, non-public, or out-of-scope GitHub records on page {page}.")
        has_next = _next_github_page(headers, account, page + 1)
        if not has_next:
            return
        if page == max_pages:
            result.status = "partial"
            result.limitations.append(f"Stopped at max_pages={max_pages}; additional repositories were not collected.")


def collect(adapter, input_value, cache_dir=None, refresh=False, token_env=None, timeout=10, max_pages=3):
    """Collect bounded public observations; failures are explicit result states."""
    canonical = ALIASES.get(adapter, adapter)
    result = CollectionResult(adapter=canonical, input_value=str(input_value))
    try:
        if canonical not in ADAPTERS:
            raise ConnectorError("Unknown adapter; use the static adapter catalog.")
        result.metadata = dict(ADAPTERS[canonical])
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout <= 30:
            raise ConnectorError("timeout must be greater than 0 and at most 30 seconds.")
        if type(max_pages) is not int or not 1 <= max_pages <= 10:
            raise ConnectorError("max_pages must be an integer from 1 to 10.")
        token = None
        if token_env is not None:
            if canonical != "github-repositories" or not isinstance(token_env, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token_env):
                raise ConnectorError("A token environment-variable name is only supported for GitHub.")
            token = os.environ.get(token_env)
            if not token or any(c.isspace() for c in token):
                raise ConnectorError("The explicitly named token environment variable is missing or invalid.")
        if canonical == "certificate-transparency":
            value = _domain(input_value)
            client = _Client(result, "crt.sh", cache_dir, refresh, timeout, token)
            _ct(result, client, value)
        else:
            value = _account(input_value)
            client = _Client(result, "api.github.com", cache_dir, refresh, timeout, token)
            _github(result, client, value, max_pages)
        result.input_value = value
        result.limitations.insert(0, ADAPTERS[canonical]["coverage"])
    except (ConnectorError, OSError, TypeError, ValueError) as error:
        result.status = "partial" if result.observations else "failed"
        result.error = str(error)
        if 'token' in locals() and token:
            result.error = result.error.replace(token, "[REDACTED]")
    return result


def parse_recon_export(path, table=None):
    """Parse selected Recon-ng JSON/CSV records as unverified offline leads."""
    result = CollectionResult(adapter="recon-ng-import", input_value=str(path))
    supported = {"domains": ("domain", "domain"), "hosts": ("host", "host"), "repositories": ("repository", "url")}
    try:
        source = _local_path(path)
        if not stat.S_ISREG(source.lstat().st_mode) or source.stat().st_size > MAX_IMPORT_BYTES:
            raise ConnectorError("Import must be a bounded regular file.")
        data = source.read_bytes()
        if len(data) > MAX_IMPORT_BYTES:
            raise ConnectorError("Import exceeded the byte limit.")
        artifact = RawArtifact("recon-ng-export" + (".csv" if source.suffix.lower() == ".csv" else ".json"), data, "", "", utc_now(), content_type="text/csv" if source.suffix.lower() == ".csv" else "application/json")
        result.artifacts.append(artifact)
        if table is not None and table not in supported:
            raise ConnectorError("Select domains, hosts, or repositories for import.")
        if source.suffix.lower() == ".csv":
            if table is None:
                raise ConnectorError("CSV import requires an explicit table name.")
            reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
            if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ConnectorError("CSV headers must be nonempty and unique.")
            tables = {table: list(reader)}
        else:
            tables = _parse_json(data)
            if not isinstance(tables, dict):
                raise ConnectorError("Recon-ng JSON export must be an object keyed by table name.")
        result.limitations.append("Imported rows are unverified leads. Original collection URLs, times, and source independence are unknown unless separately established; import time is not original retrieval time.")
        selected_tables = 0
        rejected = 0
        for name, rows in tables.items():
            if name not in supported or (table is not None and name != table):
                result.status = "partial"
                result.limitations.append(f"Table {str(name)!r} was not imported; only selected domains, hosts, and repositories are supported.")
                continue
            selected_tables += 1
            if not isinstance(rows, list):
                raise ConnectorError("Each selected export table must be an array of row objects.")
            kind, value_field = supported[name]
            for row in rows:
                try:
                    if not isinstance(row, dict) or None in row or (source.suffix.lower() == ".csv" and any(value is None for value in row.values())):
                        raise ConnectorError("Malformed row shape.")
                    value = row.get(value_field)
                    value = _public_url(value) if kind == "repository" else _domain(value, wildcard=True)
                    module = row.get("module") or ""
                    if not isinstance(module, str):
                        raise ConnectorError("Module attribution must be a string.")
                    _observe(result, artifact, kind, value, origin_module=module,
                             provenance_status="imported-unverified", imported_table=name,
                             limitations="Imported discovery lead; collection source/time and independence have not been verified.",
                             reported_source_url=row.get("source_url", ""),
                             reported_retrieved_at_utc=row.get("retrieved_at_utc", ""))
                except (ConnectorError, TypeError, AttributeError):
                    rejected += 1
        if selected_tables == 0:
            raise ConnectorError("No selected supported tables were present.")
        if rejected:
            result.status = "partial" if result.observations else "failed"
            result.limitations.append(f"Rejected {rejected} malformed or unsafe export rows; retained the original export artifact.")
    except (ConnectorError, OSError, TypeError, ValueError, UnicodeError, csv.Error) as error:
        result.status = "partial" if result.observations else "failed"
        result.error = str(error)
    return result
